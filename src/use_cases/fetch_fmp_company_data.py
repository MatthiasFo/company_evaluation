from src.adapters.big_query_data_mart_adapter import BigQueryDataMartAdapter
from src.adapters.big_query_storage_adapter import BigQueryStorageAdapter, BigQueryStorageDataset, FmpTableName
from src.adapters.financial_modeling_prep_adapter import FinancialModelingPrepAdapter
from src.domain.scraper import DataSource, ScraperFactory


class FmpScraperUseCase:
    def __init__(self):
        self.fmpAdapter = FinancialModelingPrepAdapter()
        self.rawFmpDataAdapter = BigQueryStorageAdapter(BigQueryStorageDataset.FMP.value)
        self.martCombinedAdapter = BigQueryDataMartAdapter()

    def fetch_fmp_company_data(self):
        data_sources = [
            DataSource(
                FmpTableName.PROFILE.value,
                lambda ticker: {FmpTableName.PROFILE.value: self.fmpAdapter.get_profile_info(ticker)},
            ),
            DataSource(
                FmpTableName.QUOTE.value, lambda ticker: {FmpTableName.QUOTE.value: self.fmpAdapter.get_quote(ticker)}
            ),
            DataSource(
                FmpTableName.FINANCIAL_GROWTH.value,
                lambda ticker: {FmpTableName.FINANCIAL_GROWTH.value: self.fmpAdapter.get_financial_growth(ticker)},
            ),
            DataSource(
                FmpTableName.CASH_FLOW_YEARLY.value,
                lambda ticker: {FmpTableName.CASH_FLOW_YEARLY.value: self.fmpAdapter.get_cash_flow(ticker)},
            ),
            DataSource(
                FmpTableName.INCOME_STATEMENT_YEARLY.value,
                lambda ticker: {
                    FmpTableName.INCOME_STATEMENT_YEARLY.value: self.fmpAdapter.get_income_statement(ticker)
                },
            ),
            DataSource(
                FmpTableName.BALANCE_SHEET_YEARLY.value,
                lambda ticker: {FmpTableName.BALANCE_SHEET_YEARLY.value: self.fmpAdapter.get_balance_sheet(ticker)},
            ),
        ]

        scraper = ScraperFactory().create_scraper(
            data_sources=data_sources,
            data_storage=self.rawFmpDataAdapter,
            scraper_name="FMP",
        )
        result_message = scraper.scrape_company_data(
            tickers=self.martCombinedAdapter.get_remaining_tickers_for_fmp_scraper(),
            api_stock_limit=40,
            time_limit_in_sec=1800,
        )

        return {
            "success": True,
            "message": result_message,
        }


if __name__ == "__main__":
    FmpScraperUseCase().fetch_fmp_company_data()
