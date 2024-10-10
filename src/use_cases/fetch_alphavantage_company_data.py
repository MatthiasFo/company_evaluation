from abc import ABC
from typing import Dict

import pandas as pd
from src.adapters.alphavantage_adapter import AlphavantageAdapter, AlphavantageFunctions, AlphavantageReportTypes
from src.adapters.big_query_data_mart_adapter import BigQueryDataMartAdapter
from src.adapters.big_query_storage_adapter import AlphavantageTableName, BigQueryStorageDataset, BigQueryStorageAdapter
from src.domain.scraper import DataSource, ScraperFactory


class AlphavantageScraperUseCase(ABC):
    def __init__(self):
        self.alphavantageAdapter = AlphavantageAdapter()
        self.rawAlphavantageDataAdapter = BigQueryStorageAdapter(BigQueryStorageDataset.ALPHAVANTAGE.value)
        self.martCombinedAdapter = BigQueryDataMartAdapter()

    def fetch_alphavantage_company_data(self):
        data_sources = [
            DataSource(AlphavantageFunctions.CASH_FLOW.value, lambda ticker: self._split_cashflows(ticker)),
            DataSource(AlphavantageFunctions.BALANCE_SHEET.value, lambda ticker: self._split_balance_sheets(ticker)),
            DataSource(
                AlphavantageFunctions.INCOME_STATEMENT.value, lambda ticker: self._split_income_statements(ticker)
            ),
        ]

        scraper = ScraperFactory().create_scraper(
            data_sources=data_sources,
            data_storage=self.rawAlphavantageDataAdapter,
            scraper_name="Alphavantage",
        )
        result_message = scraper.scrape_company_data(
            tickers=self.martCombinedAdapter.get_remaining_tickers_for_alphavantage_scraper(),
            api_stock_limit=25,
            time_limit_in_sec=1800,
        )

        return {
            "success": True,
            "message": result_message,
        }

    def _split_cashflows(self, ticker: str) -> Dict[AlphavantageTableName, pd.DataFrame]:
        results = self.alphavantageAdapter.get_cash_flow(ticker)
        return {
            AlphavantageTableName.CASH_FLOWS_ANNUALLY.value: results[AlphavantageReportTypes.ANNUALLY.value],
            AlphavantageTableName.CASH_FLOWS_QUARTERLY.value: results[AlphavantageReportTypes.QUARTERLY.value],
        }

    def _split_balance_sheets(self, ticker) -> Dict[AlphavantageTableName, pd.DataFrame]:
        results = self.alphavantageAdapter.get_balance_sheet(ticker)
        return {
            AlphavantageTableName.BALANCE_SHEETS_ANNUALLY.value: results[AlphavantageReportTypes.ANNUALLY.value],
            AlphavantageTableName.BALANCE_SHEETS_QUARTERLY.value: results[AlphavantageReportTypes.QUARTERLY.value],
        }

    def _split_income_statements(self, ticker) -> Dict[AlphavantageTableName, pd.DataFrame]:
        results = self.alphavantageAdapter.get_income_statement(ticker)
        return {
            AlphavantageTableName.INCOME_STATEMENTS_ANNUALLY.value: results[AlphavantageReportTypes.ANNUALLY.value],
            AlphavantageTableName.INCOME_STATEMENTS_QUARTERLY.value: results[AlphavantageReportTypes.QUARTERLY.value],
        }


if __name__ == "__main__":
    AlphavantageScraperUseCase().fetch_alphavantage_company_data()
