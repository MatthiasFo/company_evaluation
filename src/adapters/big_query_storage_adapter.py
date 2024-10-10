from enum import Enum
from typing import Dict
from google.cloud import bigquery
import pandas as pd

from src.ports.datastorage_port import DatastoragePort


class BigQueryStorageDataset(Enum):
    YAHOO = "yahoo_finance"
    FMP = "financial_modeling_prep"
    ALPHAVANTAGE = "alphavantage"
    CURATED_DATA = "curated_data"


class YahooTableName(Enum):
    COMPANY_INFO = "company_info"
    CASH_FLOW_QUARTERLY = "cash_flow_quarterly"
    CASH_FLOW_YEARLY = "cash_flow_yearly"
    INCOME_STATEMENT_QUARTERLY = "income_statement_quarterly"
    INCOME_STATEMENT_YEARLY = "income_statement_yearly"
    BALANCE_SHEET_QUARTERLY = "balance_sheet_quarterly"
    BALANCE_SHEET_YEARLY = "balance_sheet_yearly"


class AlphavantageTableName(Enum):
    CASH_FLOWS_ANNUALLY = "cashflows_annually"
    INCOME_STATEMENTS_ANNUALLY = "income_stmts_annually"
    BALANCE_SHEETS_ANNUALLY = "balance_sheets_annually"
    CASH_FLOWS_QUARTERLY = "cashflows_quarterly"
    INCOME_STATEMENTS_QUARTERLY = "income_stmts_quarterly"
    BALANCE_SHEETS_QUARTERLY = "balance_sheets_quarterly"


class FmpTableName(Enum):
    PROFILE = "profile"
    QUOTE = "quote"
    FINANCIAL_GROWTH = "financial_growth"
    CASH_FLOW_YEARLY = "cashflow"
    INCOME_STATEMENT_YEARLY = "income_stmt"
    BALANCE_SHEET_YEARLY = "balance_sheet"


class BigQueryStorageAdapter(DatastoragePort):
    _project_id = "whatever-your-project-is"
    _dataset_name = None
    _dataset = None
    _client = None

    def __init__(self, dataset_name: str):
        self._dataset_name = dataset_name
        self._client = bigquery.Client(project=self._project_id)
        self._dataset = bigquery.Dataset(f"{self._project_id}.{self._dataset_name}")

    def _get_select_stmt_from_table(self, table_name: str, select_stmt: str) -> pd.DataFrame:
        table_id = f"{self._project_id}.{self._dataset_name}.{table_name}"
        query = f"SELECT {select_stmt} FROM `{table_id}`"
        query_job = self._client.query(query)
        rows = query_job.result()
        df_result = rows.to_dataframe()
        return df_result

    def store_data_to_tables(self, data: Dict[str, pd.DataFrame]) -> bool:
        for table_name, dataframe in data.items():
            self._insert_rows_without_duplicates(table_name, dataframe)
        return True

    def _insert_rows(self, table_name: str, rows_to_insert: pd.DataFrame) -> int:
        table_id = f"{self._project_id}.{self._dataset_name}.{table_name}"
        bq_table = self._client.get_table(table_id)
        errors = self._client.insert_rows_from_dataframe(
            table=bq_table,
            dataframe=rows_to_insert,
            row_ids=rows_to_insert["id"].values.tolist(),
            ignore_unknown_values=True,
        )
        if not any(errors):  # big query returns list or list of lists
            print(f"New rows ({rows_to_insert.shape[0]}) have been added to {table_id}.")
            return rows_to_insert.shape[0]
        else:
            print("Encountered errors while inserting rows to {}: {}".format(table_id, errors))
            raise Exception(errors)

    def _insert_rows_without_duplicates(self, table_name: str, rows_to_insert: pd.DataFrame) -> int:
        existing_ids = [
            row[0] for row in self._get_select_stmt_from_table(table_name, "id").values.tolist()
        ]  # big query dataframe returns a list of lists
        new_rows_to_insert = rows_to_insert.drop(rows_to_insert[[id in existing_ids for id in rows_to_insert.id]].index)
        if new_rows_to_insert.empty:
            print(f"No new rows to insert into {table_name}.")
            return 0
        return self._insert_rows(table_name=table_name, rows_to_insert=new_rows_to_insert)
