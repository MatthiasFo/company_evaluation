from abc import ABC, abstractmethod
from typing import Dict
import pandas as pd


class DatastoragePort(ABC):
    @abstractmethod
    def store_data_to_tables(self, data: Dict[str, pd.DataFrame]) -> None:
        # this function should store the dataframes to the corresponding tables, specified by the keys
        pass
