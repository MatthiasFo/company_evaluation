from typing import Dict
import pytest
import pandas as pd
from app import create_app
import copy

from src.ports.datamart_port import DataMartPort
from src.ports.datastorage_port import DatastoragePort
from tests.mock_data.mock_alphavantage_data import (
    alphavantage_balance_sheet_json,
    alphavantage_cashflow_json,
    alphavantage_income_json,
)
import requests_mock


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


uri_alphavantage_balance_sheet = "https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=mocked"
uri_alphavantage_cash_flow = "https://www.alphavantage.co/query?function=CASH_FLOW&symbol=IBM&apikey=mocked"
uri_alphavantage_income_statement = (
    "https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=mocked"
)


class MockSecretManager:
    def __init__(self):
        pass

    def get_secret(self, secret_id):
        return "mocked"


class MockBigQueryStorageAdapter(DatastoragePort):
    def __init__(self, dataset_id):
        pass

    def store_data_to_tables(self, data: Dict[str, pd.DataFrame]) -> bool:
        for table_name, df in data.items():
            assert "id" in df.columns
            assert "requestTimestamp" in df.columns
        return True


class MockBigQueryDataMartAdapter(DataMartPort):
    def __init__(self):
        pass

    def get_remaining_tickers_for_alphavantage_scraper(self):
        return ["IBM"]

    def get_remaining_tickers_for_fmp_scraper(self):
        return []

    def get_remaining_tickers_for_yahoo_scraper(self):
        return []

    def get_dcf_base_data(self):
        return pd.DataFrame()


def test_alphavantage_scraping(client, mocker):
    mock_storage_adapter = MockBigQueryStorageAdapter("mock_dataset")
    mocker.patch(
        "src.use_cases.fetch_alphavantage_company_data.BigQueryStorageAdapter",
        return_value=mock_storage_adapter,
    )
    mock_store_data = mocker.spy(mock_storage_adapter, "store_data_to_tables")

    mocker.patch("src.use_cases.fetch_alphavantage_company_data.BigQueryDataMartAdapter", MockBigQueryDataMartAdapter)

    mocker.patch("src.adapters.alphavantage_adapter.GcpSecretManager", MockSecretManager)

    with requests_mock.Mocker() as mocker:
        mocker.get(uri_alphavantage_balance_sheet, json=alphavantage_balance_sheet_json)
        mocker.get(uri_alphavantage_cash_flow, json=alphavantage_cashflow_json)
        mocker.get(uri_alphavantage_income_statement, json=alphavantage_income_json)
        response = client.get("/fetch-new-alphavantage-data")

        assert mock_store_data.called
        assert response.status_code == 200


def test_alphavantage_scraping_incomplete_balance_sheet(client, mocker):
    mock_storage_adapter = MockBigQueryStorageAdapter("mock_dataset")
    mocker.patch(
        "src.use_cases.fetch_alphavantage_company_data.BigQueryStorageAdapter",
        return_value=mock_storage_adapter,
    )
    mock_store_data = mocker.spy(mock_storage_adapter, "store_data_to_tables")

    mocker.patch("src.use_cases.fetch_alphavantage_company_data.BigQueryDataMartAdapter", MockBigQueryDataMartAdapter)

    mocker.patch("src.adapters.alphavantage_adapter.GcpSecretManager", MockSecretManager)

    incomplete_balance_sheet = copy.deepcopy(alphavantage_balance_sheet_json)
    incomplete_balance_sheet["annualReports"][1].pop("totalAssets")
    incomplete_balance_sheet["annualReports"][1].pop("cashAndCashEquivalentsAtCarryingValue")
    incomplete_balance_sheet["annualReports"][1].pop("inventory")

    with requests_mock.Mocker() as mocker:
        mocker.get(uri_alphavantage_balance_sheet, json=incomplete_balance_sheet)
        mocker.get(uri_alphavantage_cash_flow, json=alphavantage_cashflow_json)
        mocker.get(uri_alphavantage_income_statement, json=alphavantage_income_json)

        response = client.get("/fetch-new-alphavantage-data")

        assert not mock_store_data.called
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main()
