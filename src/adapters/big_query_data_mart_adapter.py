from enum import Enum
from typing import List
from google.cloud import bigquery
import pandas as pd

from src.ports.datamart_port import DataMartPort


class MartTables(Enum):
    DCF_BASE_DATA = "dcf_model_base_data"
    REMAINING_TICKERS_FOR_FMP_SCRAPER = "remaining_tickers_for_fmp_scraper"
    REMAINING_TICKERS_FOR_YAHOO_SCRAPER = "remaining_tickers_for_yahoo_scraper"
    REMAINING_TICKERS_FOR_ALPHAVANTAGE_SCRAPER = "remaining_tickers_for_alphavantage_scraper"


class BigQueryDataMartAdapter(DataMartPort):
    _project_id = "your-own-project-id"
    _dataset_name = "marts"
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

    def get_dcf_base_data(self) -> pd.DataFrame:
        data = self._get_select_stmt_from_table(
            table_name=MartTables.DCF_BASE_DATA.value,
            select_stmt="*",
        )

        integer_columns = ["shares_outstanding"]
        float_columns = [
            "free_cash_flow",
            "revenue_growth",
        ]

        data[integer_columns] = data[integer_columns].astype(int)
        data[float_columns] = data[float_columns].astype(float)

        return data
