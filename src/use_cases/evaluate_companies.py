from src.adapters.big_query_data_mart_adapter import BigQueryDataMartAdapter
from src.adapters.big_query_storage_adapter import BigQueryStorageAdapter, BigQueryStorageDataset
from src.domain.discounted_cashflow_model import DCFModel


class CompanyEvaluation:
    def __init__(self):
        self._dataStorage = BigQueryStorageAdapter(BigQueryStorageDataset.DCF_MODEL.value)
        self._dataMart = BigQueryDataMartAdapter()

    def evaluate_companies(self):
        fin_stmts = self._dataMart.get_dcf_base_data()
        chunk_size = 3000
        full_size = len(fin_stmts)
        for i in range(0, len(fin_stmts), chunk_size):
            print(f"Processing {i} to {i + chunk_size} of {full_size} total.")
            dcfModel = DCFModel(fin_stmts[i : i + chunk_size])
            intrinsic_values = dcfModel.estimate_intrinsic_value()
            self._dataStorage.store_data_to_tables(
                {
                    "dcf_model_evaluations": intrinsic_values,
                },
            )
            print(f"Processed {i + len(intrinsic_values)} rows of {full_size} total.")

        return {
            "success": True,
            "message": f"Generated {fin_stmts.shape[0]} fin ratios",
        }


if __name__ == "__main__":
    CompanyEvaluation().evaluate_companies()
