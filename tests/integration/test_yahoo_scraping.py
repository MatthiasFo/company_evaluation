from typing import Dict
import pandas as pd
import pytest
from app import create_app
from src.ports.datamart_port import DataMartPort
from src.ports.datastorage_port import DatastoragePort

from tests.mock_data.mock_yahoo_data import (
    mock_yahoo_aapl_info,
    mock_yahoo_aapl_cashflow,
    mock_yahoo_aapl_income_stmt,
    mock_yahoo_aapl_balance_sheet,
)


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


class MockBigQueryStorageAdapter(DatastoragePort):
    def __init__(self, dataset_id):
        pass

    def store_data_to_tables(self, data: Dict[str, pd.DataFrame]) -> bool:
        for table_name, df in data.items():
            assert "id" in df.columns
            assert "request_timestamp" in df.columns
        return True


class MockBigQueryDataMartAdapter(DataMartPort):
    def __init__(self):
        pass

    def get_remaining_tickers_for_alphavantage_scraper(self):
        assert False

    def get_remaining_tickers_for_fmp_scraper(self):
        assert False

    def get_remaining_tickers_for_yahoo_scraper(self):
        return [
            "AAPL",
        ]

    def get_combined_financial_filings(self):
        assert False

    def get_latest_company_infos(self):
        assert False


@pytest.fixture
def mock_yfinance(mocker):
    mock_ticker = mocker.Mock()
    mock_ticker.info = mock_yahoo_aapl_info

    mock_ticker.cashflow = mock_yahoo_aapl_cashflow
    mock_ticker.income_stmt = mock_yahoo_aapl_income_stmt
    mock_ticker.balance_sheet = mock_yahoo_aapl_balance_sheet

    mock_yf = mocker.patch("yfinance.Ticker", return_value=mock_ticker)
    return mock_yf


def test_fetch_one_new_stocks(client, mocker, mock_yfinance):
    mock_storage_adapter = MockBigQueryStorageAdapter("mock_dataset")
    mocker.patch(
        "src.use_cases.fetch_new_yahoo_company_data.BigQueryStorageAdapter",
        return_value=mock_storage_adapter,
    )
    mock_store_data = mocker.spy(mock_storage_adapter, "store_data_to_tables")

    mocker.patch("src.use_cases.fetch_new_yahoo_company_data.BigQueryDataMartAdapter", MockBigQueryDataMartAdapter)

    # Make a request to the fetch_new_stocks endpoint
    response = client.get("/fetch-new-yahoo-data")

    assert mock_yfinance.called
    assert mock_store_data.called
    # Assert that the response is successful
    assert response.status_code == 200
    assert response.json == {"message": "Fetched 1 new stocks and stored in warehouse"}


if __name__ == "__main__":
    pytest.main()
