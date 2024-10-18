from typing import Dict
import pytest
import pandas as pd
from app import create_app

from src.ports.datamart_port import DataMartPort
from src.ports.datastorage_port import DatastoragePort
from tests.mock_data.mock_fmp_data import (
    fmp_balance_sheet_json,
    fmp_quote_json,
    fmp_cashflow_json,
    fmp_income_json,
    fmp_growth_json,
    fmp_profile_json,
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


uri_fmp_quote = "https://financialmodelingprep.com/api/v3/quote/AAPL?apikey=mocked"
uri_fmp_balance_sheet = (
    "https://financialmodelingprep.com/api/v3/balance-sheet-statement/AAPL?apikey=mocked&period=annual"
)
uri_fmp_cash_flow = "https://financialmodelingprep.com/api/v3/cash-flow-statement/AAPL?apikey=mocked&period=annual"
uri_fmp_income_statement = "https://financialmodelingprep.com/api/v3/income-statement/AAPL?apikey=mocked&period=annual"
uri_fmp_financial_growth = "https://financialmodelingprep.com/api/v3/financial-growth/AAPL?apikey=mocked&period=annual"
uri_fmp_profile = "https://financialmodelingprep.com/api/v3/profile/AAPL?apikey=mocked"


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
        return []

    def get_remaining_tickers_for_fmp_scraper(self):
        return ["AAPL"]

    def get_remaining_tickers_for_yahoo_scraper(self):
        return []

    def get_dcf_base_data(self):
        return pd.DataFrame()


def test_fmp_scraping(client, mocker):
    mock_storage_adapter = MockBigQueryStorageAdapter("mock_dataset")
    mocker.patch(
        "src.use_cases.fetch_fmp_company_data.BigQueryStorageAdapter",
        return_value=mock_storage_adapter,
    )
    mock_store_data = mocker.spy(mock_storage_adapter, "store_data_to_tables")

    mocker.patch("src.use_cases.fetch_fmp_company_data.BigQueryDataMartAdapter", MockBigQueryDataMartAdapter)

    mocker.patch("src.adapters.financial_modeling_prep_adapter.GcpSecretManager", MockSecretManager)

    with requests_mock.Mocker() as mocker:
        mocker.get(uri_fmp_quote, json=fmp_quote_json)
        mocker.get(uri_fmp_balance_sheet, json=fmp_balance_sheet_json)
        mocker.get(uri_fmp_cash_flow, json=fmp_cashflow_json)
        mocker.get(uri_fmp_income_statement, json=fmp_income_json)
        mocker.get(uri_fmp_financial_growth, json=fmp_growth_json)
        mocker.get(uri_fmp_profile, json=fmp_profile_json)

        response = client.get("/fetch-new-fmp-data")

        assert mock_store_data.called
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main()
