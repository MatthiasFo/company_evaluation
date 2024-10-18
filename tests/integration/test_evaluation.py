import random
import string
from typing import Dict
import numpy as np
import pandas as pd
import pytest
from app import create_app
from src.adapters.big_query_data_mart_adapter import BigQueryDataMartAdapter
from src.ports.datastorage_port import DatastoragePort


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
    # This test is important to test, that we iterate through large dataframes and store each processed slice individually
    num_tickers = 4000
    dummy_tickers = ["".join(random.choices(string.ascii_uppercase, k=4)) for _ in range(num_tickers)]
    mock_base_data = pd.DataFrame(
        {
            "id": [f"2024-09-08_{ticker}" for ticker in dummy_tickers],
            "ticker": dummy_tickers,
            "free_cash_flow": np.random.uniform(-1e10, 1e10, num_tickers),
            "revenue_growth": np.random.uniform(-1, 1, num_tickers),
            "shares_outstanding": np.random.randint(1e8, 1e10, num_tickers),
        }
    )

    mocker.patch.object(
        BigQueryDataMartAdapter,
        "get_dcf_base_data",
        return_value=mock_base_data,
    )

    def assert_data_to_tables(data: Dict[str, pd.DataFrame]) -> bool:
        for table_name, dataframe in data.items():
            if table_name == "dcf_model_evaluations":
                expected_columns = [
                    "id",
                    "ticker",
                    "shares_outstanding",
                    "revenue_growth",
                    "free_cash_flow",
                    "normal",
                    "stable",
                    "stable_and_strong_growth",
                    "volatile",
                    "volatile_and_weak_growth",
                ]
                assert set(dataframe.columns) == set(expected_columns)
            else:
                raise ValueError(f"Table name {table_name} not recognized")

    mocker.patch.object(
        MockBigQueryStorageAdapter,
        "store_data_to_tables",
        side_effect=assert_data_to_tables,
    )

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
    pytest.main([__file__])
