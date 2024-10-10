import pandas as pd
from src.adapters.big_query_data_mart_adapter import BigQueryDataMartAdapter
from src.adapters.big_query_storage_adapter import BigQueryStorageAdapter, BigQueryStorageDataset
from src.domain.financial_evaluator import FinancialEvaluator


class CompanyEvaluation:
    def __init__(self):
        self._dataStorage = BigQueryStorageAdapter(BigQueryStorageDataset.CURATED_DATA.value)
        self._dataMart = BigQueryDataMartAdapter()

    def evaluate_companies(self):
        fin_stmts = self._retrieve_company_data()
        chunk_size = 3000
        full_size = len(fin_stmts)
        for i in range(0, len(fin_stmts), chunk_size):
            finacialEvluator = FinancialEvaluator(fin_stmts[i : i + chunk_size])
            indicators_over_time = finacialEvluator.get_ratios_and_trends()
            intrinsic_values = finacialEvluator.get_current_evaluation()
            self._store_evaluation(indicators_over_time, intrinsic_values)
            print(f"Processed {i + len(indicators_over_time)} rows of {full_size} total.")

        return {
            "success": True,
            "message": f"Generated {fin_stmts.shape[0]} fin ratios",
        }

    def _retrieve_company_data(self) -> pd.DataFrame:
        combined_fin_stmts = self._dataMart.get_combined_financial_filings()
        company_infos = self._dataMart.get_latest_company_infos()

        # TODO: This merging could also be moved with DBT into BigQuery
        fin_stmts_with_info = combined_fin_stmts.merge(
            company_infos[
                [
                    "id",
                    "request_timestamp",
                    "ticker",
                    "company_name",
                    "sector",
                    "industry",
                    "country",
                    # the following are momentary values,
                    # so this mixes time series data with momentary data
                    # but currently we do not have better data
                    "market_cap",
                    "current_price",
                    "shares_outstanding",
                    "earnings_per_share",
                    "price_earnings_ratio",
                ]
            ],
            how="left",
            on="ticker",
        )

        mandatory_columns = [
            "id",
            "ticker",
            "company_name",
            "country",
            "sector",
            "industry",
            "end_of_period",
        ]

        fin_stmts_with_info = fin_stmts_with_info.dropna(subset=mandatory_columns)
        return fin_stmts_with_info

    def _store_evaluation(self, time_series_evaluation: pd.DataFrame, indicators_with_intrinsic_value: pd.DataFrame):
        self._dataStorage.store_data_to_tables(
            {
                "financial_ratios_over_time": time_series_evaluation,
                "intrinsic_value_and_ratio_evaluations": indicators_with_intrinsic_value,
            },
        )
        return


if __name__ == "__main__":
    CompanyEvaluation().evaluate_companies()
