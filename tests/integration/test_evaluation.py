import random
import string
from typing import Dict
import numpy as np
import pandas as pd
import pytest
from app import create_app
from src.adapters.big_query_data_mart_adapter import BigQueryDataMartAdapter
from src.ports.datastorage_port import DatastoragePort
from tests.mock_data.mock_bq_data import (
    mock_bq_combined_filings,
    mock_bq_company_infos,
)


class MockBigQueryStorageAdapter(DatastoragePort):
    def __init__(self, dataset_id):
        pass

    def store_data_to_tables(self, data: Dict[str, pd.DataFrame]) -> bool:
        pass


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_evaluate_companies(client, mocker):
    def dummy_get_select_stmt_from_table(table_name: str, select_stmt: str, where_stmt=None):
        if not hasattr(dummy_get_select_stmt_from_table, "call_count"):
            dummy_get_select_stmt_from_table.call_count = 0
        dummy_get_select_stmt_from_table.call_count += 1
        if table_name == "combined_financial_filings":
            return mock_bq_combined_filings
        elif table_name == "current_company_infos":
            return mock_bq_company_infos
        else:
            raise ValueError(f"Table name {table_name} not recognized")

    mocker.patch.object(
        BigQueryDataMartAdapter, "_get_select_stmt_from_table", side_effect=dummy_get_select_stmt_from_table
    )

    def assert_data_to_tables(data: Dict[str, pd.DataFrame]) -> bool:
        for table_name, dataframe in data.items():
            if table_name == "financial_ratios_over_time":
                assert dataframe.shape[0] == 8
                return 8
            elif table_name == "intrinsic_value_and_ratio_evaluations":
                assert dataframe.shape[0] == 1
                return 1
            else:
                raise ValueError(f"Table name {table_name} not recognized")

    mocker.patch.object(MockBigQueryStorageAdapter, "store_data_to_tables", side_effect=assert_data_to_tables)

    mock_storage_adapter = MockBigQueryStorageAdapter("mock_dataset")
    mocker.patch(
        "src.use_cases.evaluate_companies.BigQueryStorageAdapter",
        return_value=mock_storage_adapter,
    )
    mock_store_data = mocker.spy(mock_storage_adapter, "store_data_to_tables")

    response = client.get("/evaluate-companies")

    assert mock_store_data.called
    assert response.status_code == 200


def test_evaluate_companies_with_large_dataframes(client, mocker):
    # This test is important to test, that we iterate through large dataframes and store each processed slice individually
    num_rows = 4000
    num_tickers = 1000
    dummy_tickers = ["".join(random.choices(string.ascii_uppercase, k=4)) for _ in range(num_tickers)]
    periods = pd.date_range(start="2012-12-31", periods=int(np.ceil(num_rows / num_tickers)), freq="YE")
    expanded_tickers = [ticker for ticker in dummy_tickers for _ in periods]
    expanded_periods = [period for _ in dummy_tickers for period in periods]

    mock_filing_data = pd.DataFrame(
        {
            "filing_id": [f"{p}-{t}" for p, t in zip(expanded_periods, expanded_tickers)],
            "end_of_period": expanded_periods,
            "free_cash_flow": np.random.uniform(-1e10, 1e10, num_rows),
            "revenue_growth": np.random.uniform(-1, 1, num_rows),
            "ticker": expanded_tickers,
            "net_income": np.random.uniform(-1e10, 1e10, num_rows),
            "total_revenue": np.random.uniform(1e7, 1e12, num_rows),
            "total_assets": np.random.uniform(1e7, 1e12, num_rows),
            "stockholders_equity": np.random.uniform(1e6, 1e11, num_rows),
            "cost_of_goods_sold": np.random.uniform(1e6, 1e11, num_rows),
            "inventory": np.random.uniform(1e5, 1e10, num_rows),
            "selling_general_and_administration": np.random.uniform(1e6, 1e11, num_rows),
            "current_assets": np.random.uniform(1e6, 1e11, num_rows),
            "current_liabilities": np.random.uniform(1e6, 1e11, num_rows),
            "accounts_receivable": np.random.uniform(1e5, 1e10, num_rows),
            "dividends_paid": np.random.uniform(-1e9, 1e9, num_rows),
            "long_term_debt": np.random.uniform(1e7, 1e12, num_rows),
            "cash_and_cash_equivalents": np.random.uniform(1e5, 1e10, num_rows),
            "shares_growth": np.random.uniform(1e5, 1e10, num_rows),
        }
    )

    mock_info_data = pd.DataFrame(
        {
            "id": [f"2024-09-08_{ticker}" for ticker in dummy_tickers],
            "ticker": dummy_tickers,
            "request_timestamp": ["2024-09-08T00:00:00"] * num_tickers,
            "company_name": ["".join(random.choices(string.ascii_letters, k=20)) for _ in range(num_tickers)],
            "sector": np.random.choice(["Technology", "Consumer Cyclical", "Financial Services"], num_tickers),
            "industry": ["".join(random.choices(string.ascii_letters, k=20)) for _ in range(num_tickers)],
            "country": ["United States"] * num_tickers,
            "current_price": np.random.uniform(100, 300, num_tickers),
            "shares_outstanding": np.random.randint(1e8, 1e10, num_tickers),
            "market_cap": np.random.uniform(1e9, 1e12, num_tickers),
            "earnings_per_share": np.random.uniform(1, 10, num_tickers),
            "price_earnings_ratio": np.random.uniform(10, 50, num_tickers),
        }
    )

    mocker.patch.object(BigQueryDataMartAdapter, "get_combined_financial_filings", return_value=mock_filing_data)
    mocker.patch.object(BigQueryDataMartAdapter, "get_latest_company_infos", return_value=mock_info_data)

    mock_storage_adapter = MockBigQueryStorageAdapter("mock_dataset")
    mocker.patch(
        "src.use_cases.evaluate_companies.BigQueryStorageAdapter",
        return_value=mock_storage_adapter,
    )
    mock_store_data = mocker.spy(mock_storage_adapter, "store_data_to_tables")

    response = client.get("/evaluate-companies")

    assert mock_store_data.call_count == 2
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main()
