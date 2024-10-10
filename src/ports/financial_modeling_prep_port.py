from abc import ABC, abstractmethod
import pandas as pd


class FinancialModelingPrepPort(ABC):
    @abstractmethod
    def get_profile_info(self, ticker: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_quote(self, ticker: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_financial_growth(self, ticker: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_balance_sheet(self, ticker: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_cash_flow(self, ticker: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_income_statement(self, ticker: str) -> pd.DataFrame:
        pass
