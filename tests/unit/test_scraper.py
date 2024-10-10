import pytest
from unittest.mock import MagicMock
from src.domain.scraper import Scraper, ApiLimitReached, DataValidationError
from src.ports.datastorage_port import DatastoragePort
from src.domain.scraper import DataSourceInterface


@pytest.fixture
def scraper():
    data_storage = MagicMock(spec=DatastoragePort)
    data_source = MagicMock(spec=DataSourceInterface)
    data_source.source_name = "TestDataSource"
    return Scraper([data_source], data_storage, "TestScraper"), data_source, data_storage


def test_no_new_tickers(scraper):
    scraper_instance, data_source, data_storage = scraper
    result = scraper_instance.scrape_company_data([], api_stock_limit=5, time_limit_in_sec=10)
    assert result == "No new tickers to process"


def test_treatment_of_none_in_report_data(scraper):
    scraper_instance, data_source, data_storage = scraper
    data_source.fetch_data.side_effect = [{"data": None}]
    result = scraper_instance.scrape_company_data(["AAPL"], api_stock_limit=5, time_limit_in_sec=10)
    assert result == "Fetched 0 new stocks and stored in warehouse"
    data_storage.store_data_to_tables.assert_not_called()


def test_api_limit_reached(scraper):
    scraper_instance, data_source, data_storage = scraper
    data_source.fetch_data.side_effect = ApiLimitReached
    result = scraper_instance.scrape_company_data(["AAPL"], api_stock_limit=1, time_limit_in_sec=10)
    assert result == "TestScraper scraper: API limit reached after 0 new stocks."


def test_data_validation_error(scraper):
    scraper_instance, data_source, data_storage = scraper
    data_source.fetch_data.side_effect = DataValidationError("Validation error")
    result = scraper_instance.scrape_company_data(["AAPL"], api_stock_limit=5, time_limit_in_sec=10)
    assert result == "Fetched 0 new stocks and stored in warehouse"
    data_storage.store_data_to_tables.assert_not_called()


def test_successful_data_fetching(scraper):
    scraper_instance, data_source, data_storage = scraper
    data_source.fetch_data.return_value = {"data": "valid_data"}
    result = scraper_instance.scrape_company_data(["AAPL"], api_stock_limit=5, time_limit_in_sec=10)
    assert result == "Fetched 1 new stocks and stored in warehouse"
    data_storage.store_data_to_tables.assert_called_once_with({"data": "valid_data"})


def test_exceeding_api_stock_limit(scraper):
    scraper_instance, data_source, data_storage = scraper
    data_source.fetch_data.return_value = {"data": "valid_data"}
    result = scraper_instance.scrape_company_data(["AAPL", "MSFT", "GOOGL"], api_stock_limit=2, time_limit_in_sec=10)
    assert result == "Fetched 2 new stocks and stored in warehouse"
    data_storage.store_data_to_tables.assert_called()
