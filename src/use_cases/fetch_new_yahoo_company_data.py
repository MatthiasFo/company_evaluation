from src.adapters.big_query_data_mart_adapter import BigQueryDataMartAdapter
from src.adapters.big_query_storage_adapter import BigQueryStorageAdapter, BigQueryStorageDataset, YahooTableName
from src.adapters.yahoo_finance_adapter import YahooFinanceAdapter
from src.domain.scraper import DataSource, ScraperFactory


class YahoooScraperUseCase:
    def __init__(self):
        self.yahooFinanceAdapter = YahooFinanceAdapter()
        self.rawYahooDataAdapter = BigQueryStorageAdapter(BigQueryStorageDataset.YAHOO.value)
        self.martCombinedAdapter = BigQueryDataMartAdapter()

    def fetch_yahoo_company_data(self):
        data_sources = [
            DataSource(
                YahooTableName.COMPANY_INFO.value,
                lambda ticker: {YahooTableName.COMPANY_INFO.value: self.yahooFinanceAdapter.get_company_info(ticker)},
            ),
            DataSource(
                YahooTableName.CASH_FLOW_YEARLY.value,
                lambda ticker: {YahooTableName.CASH_FLOW_YEARLY.value: self.yahooFinanceAdapter.get_cashflow(ticker)},
            ),
            DataSource(
                YahooTableName.INCOME_STATEMENT_YEARLY.value,
                lambda ticker: {
                    YahooTableName.INCOME_STATEMENT_YEARLY.value: self.yahooFinanceAdapter.get_income_stmt(ticker)
                },
            ),
            DataSource(
                YahooTableName.BALANCE_SHEET_YEARLY.value,
                lambda ticker: {
                    YahooTableName.BALANCE_SHEET_YEARLY.value: self.yahooFinanceAdapter.get_balance_sheet(ticker)
                },
            ),
        ]

        scraper = ScraperFactory().create_scraper(
            data_sources=data_sources,
            data_storage=self.rawYahooDataAdapter,
            scraper_name="Yahoo",
        )
        result_message = scraper.scrape_company_data(
            tickers=self.martCombinedAdapter.get_remaining_tickers_for_yahoo_scraper(),
            api_stock_limit=50,
            time_limit_in_sec=600,
        )

        return {
            "success": True,
            "message": result_message,
        }


if __name__ == "__main__":
    YahoooScraperUseCase().fetch_yahoo_company_data()
