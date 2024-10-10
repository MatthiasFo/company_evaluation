from typing import Dict
import pandas as pd
import yfinance as yf
from requests import Session
from requests_cache import CacheMixin
from requests_ratelimiter import LimiterMixin
from pyrate_limiter import Duration, RequestRate, Limiter
from src.domain.scraper import DataValidationError
from src.ports.yahoo_finance_port import YahooFinancePort


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass


class YahooFinanceAdapter(YahooFinancePort):
    _session = None
    _tickers: Dict[str, yf.Ticker] = {}

    def __init__(self, requests_per_minute=6):
        self._session = CachedLimiterSession(limiter=Limiter(RequestRate(requests_per_minute, Duration.SECOND * 60)))

    def _get_yahoo_ticker(self, ticker: str) -> yf.Ticker:
        if ticker not in self._tickers.keys():
            self._tickers[ticker] = yf.Ticker(ticker, session=self._session)
        return self._tickers[ticker]

    def get_company_info(self, ticker: str) -> pd.DataFrame:
        info = self._get_yahoo_ticker(ticker).info
        # it is a nested field and we do not currently use it
        info.pop("companyOfficers", None)

        company_info_dict = {**info, "ticker": ticker}
        available_data = set(company_info_dict.keys())
        minimal_company_info = ["industry", "country", "ticker", "sector"]
        if not set(minimal_company_info).issubset(available_data):
            missing_info = set(minimal_company_info) - set(available_data)
            raise DataValidationError(f"Yahoo: Skipping {ticker} since missing: {' | '.join(missing_info)}")

        raw_df = pd.DataFrame([company_info_dict])
        return self._use_proper_column_names_and_add_identifiers(raw_df, ticker)

    def get_cashflow_quarterly(self, ticker: str) -> pd.DataFrame:
        raw_df = self._get_yahoo_ticker(ticker).quarterly_cashflow
        data_column_df = self._convert_time_columns_df_to_data_column_df(raw_df)
        return self._use_proper_column_names_and_add_identifiers(data_column_df, ticker)

    def get_cashflow(self, ticker: str) -> pd.DataFrame:
        raw_df = self._get_yahoo_ticker(ticker).cashflow
        data_column_df = self._convert_time_columns_df_to_data_column_df(raw_df)
        return self._use_proper_column_names_and_add_identifiers(data_column_df, ticker)

    def get_income_stmt_quarterly(self, ticker: str) -> pd.DataFrame:
        raw_df = self._get_yahoo_ticker(ticker).quarterly_income_stmt
        data_column_df = self._convert_time_columns_df_to_data_column_df(raw_df)
        return self._use_proper_column_names_and_add_identifiers(data_column_df, ticker)

    def get_income_stmt(self, ticker: str) -> pd.DataFrame:
        raw_df = self._get_yahoo_ticker(ticker).income_stmt
        data_column_df = self._convert_time_columns_df_to_data_column_df(raw_df)
        return self._use_proper_column_names_and_add_identifiers(data_column_df, ticker)

    def get_balance_sheet_quarterly(self, ticker: str) -> pd.DataFrame:
        raw_df = self._get_yahoo_ticker(ticker).quarterly_balance_sheet
        data_column_df = self._convert_time_columns_df_to_data_column_df(raw_df)
        return self._use_proper_column_names_and_add_identifiers(data_column_df, ticker)

    def get_balance_sheet(self, ticker: str) -> pd.DataFrame:
        raw_df = self._get_yahoo_ticker(ticker).balance_sheet
        data_column_df = self._convert_time_columns_df_to_data_column_df(raw_df)
        return self._use_proper_column_names_and_add_identifiers(data_column_df, ticker)

    def _convert_time_columns_df_to_data_column_df(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        transposed_statement = raw_df.transpose().reset_index(names="end_of_period")
        transposed_statement["end_of_period"] = transposed_statement["end_of_period"].astype(str)
        return transposed_statement

    def _use_proper_column_names_and_add_identifiers(self, df: pd.DataFrame, ticker: str) -> pd.DataFrame:
        df.columns = [x.replace(" ", "_").replace(".", "_").lower() for x in df.columns]
        df["request_timestamp"] = pd.Timestamp.now().strftime(
            "%Y-%m-%d"
        )  # must stay in date format because it must match big query schema (legacy mistake)
        df["ticker"] = ticker
        if "end_of_period" in df.columns:
            df = self._enhance_with_end_of_period_id(df)
        else:
            df = self._enhance_with_request_timestamp_id(df)
        return df

    def _enhance_with_end_of_period_id(self, fin_statement: pd.DataFrame) -> pd.DataFrame:
        fin_statement["id"] = (
            fin_statement["end_of_period"].astype(str)
            + "_"
            + fin_statement["ticker"].apply(lambda x: self._remove_dots_and_spaces(x))
        )
        return fin_statement

    def _enhance_with_request_timestamp_id(self, company_info: pd.DataFrame) -> pd.DataFrame:
        company_info["id"] = (
            company_info["request_timestamp"]
            + "_"
            + company_info["ticker"].apply(lambda x: self._remove_dots_and_spaces(x))
        )
        return company_info

    def _remove_dots_and_spaces(self, string: str) -> str:
        return string.replace(".", "_").replace(" ", "_")
