from abc import ABC, abstractmethod
from typing import Dict
import pandas as pd


class AlphavantagePort(ABC):
    @abstractmethod
    def get_balance_sheet(self, ticker: str) -> Dict[str, pd.DataFrame]:
        pass

    @abstractmethod
    def get_cash_flow(self, ticker: str) -> Dict[str, pd.DataFrame]:
        pass

    @abstractmethod
    def get_income_statement(self, ticker: str) -> Dict[str, pd.DataFrame]:
        pass
