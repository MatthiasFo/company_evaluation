from enum import Enum
from typing import List
from google.cloud import bigquery
import pandas as pd

from src.ports.datamart_port import DataMartPort


class MartTables(Enum):
    CURRENT_COMPANY_INFO = "current_company_infos"
    COMBINED_FINANCIAL_STATEMENTS = "combined_financial_filings"
    REMAINING_TICKERS_FOR_FMP_SCRAPER = "remaining_tickers_for_fmp_scraper"
    REMAINING_TICKERS_FOR_YAHOO_SCRAPER = "remaining_tickers_for_yahoo_scraper"
    REMAINING_TICKERS_FOR_ALPHAVANTAGE_SCRAPER = "remaining_tickers_for_alphavantage_scraper"


class BigQueryDataMartAdapter(DataMartPort):
    _project_id = "whatever-your-project-is"
    _dataset_name = "marts"
    _where_stmt_for_evaluation = "where ticker not in (select ticker from `curated_data.financial_ratios_over_time`)"
    _dataset = None
    _client = None

    def __init__(self):
        self._client = bigquery.Client(project=self._project_id)
        self._dataset = bigquery.Dataset(f"{self._project_id}.{self._dataset_name}")

    def _get_select_stmt_from_table(self, table_name: str, select_stmt: str, where_stmt=None) -> pd.DataFrame:
        table_id = f"{self._project_id}.{self._dataset_name}.{table_name}"
        query = f"SELECT {select_stmt} FROM `{table_id}`"
        if where_stmt:
            query = query + " " + where_stmt
        query_job = self._client.query(query)
        rows = query_job.result()
        df_result = rows.to_dataframe()
        return df_result

    def get_remaining_tickers_for_alphavantage_scraper(self) -> List[str]:
        data = self._get_select_stmt_from_table(
            table_name=MartTables.REMAINING_TICKERS_FOR_ALPHAVANTAGE_SCRAPER.value,
            select_stmt="ticker",
        )
        return [x[0] for x in data.values]

    def get_remaining_tickers_for_fmp_scraper(self) -> List[str]:
        data = self._get_select_stmt_from_table(
            table_name=MartTables.REMAINING_TICKERS_FOR_FMP_SCRAPER.value,
            select_stmt="ticker",
        )
        return [x[0] for x in data.values]

    def get_remaining_tickers_for_yahoo_scraper(self) -> List[str]:
        data = self._get_select_stmt_from_table(
            table_name=MartTables.REMAINING_TICKERS_FOR_YAHOO_SCRAPER.value,
            select_stmt="ticker",
        )
        return [x[0] for x in data.values]

    def get_combined_financial_filings(self) -> pd.DataFrame:
        # TODO: select only the last 5 years
        # TODO: select only stocks that have not been evaluated yet for the current period
        data = self._get_select_stmt_from_table(
            table_name=MartTables.COMBINED_FINANCIAL_STATEMENTS.value,
            select_stmt="*",
            where_stmt=self._where_stmt_for_evaluation
            + " and end_of_period > date_sub(current_date(), interval 10 year)",
        )

        integer_columns = [
            "total_revenue",
            "net_income",
            "cost_of_goods_sold",
            "selling_general_and_administration",
            "free_cash_flow",
            "dividends_paid",
            "stockholders_equity",
            "total_assets",
            "accounts_receivable",
            "cash_and_cash_equivalents",
            "current_assets",
            "current_liabilities",
            "inventory",
            "long_term_debt",
        ]

        float_columns = ["revenue_growth", "shares_growth"]

        data[integer_columns] = data[integer_columns].astype(float)  # use float because it can contain NaNs
        data[float_columns] = data[float_columns].astype(float)

        return data

    def get_latest_company_infos(self) -> pd.DataFrame:
        data = self._get_select_stmt_from_table(
            table_name=MartTables.CURRENT_COMPANY_INFO.value,
            select_stmt="*",
            where_stmt=self._where_stmt_for_evaluation,
        )

        integer_columns = [
            "market_cap",
            "shares_outstanding",
        ]

        float_columns = ["current_price", "earnings_per_share", "price_earnings_ratio"]

        data[integer_columns] = data[integer_columns].astype(float)  # use float because it can contain NaNs
        data[float_columns] = data[float_columns].astype(float)

        return data
