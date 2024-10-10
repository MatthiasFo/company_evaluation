from abc import ABC, abstractmethod
import pandas as pd


class YahooFinancePort(ABC):
    @abstractmethod
    def get_company_info(self, ticker: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_cashflow_quarterly(self, ticker: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_cashflow(self, ticker: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_income_stmt_quarterly(self, ticker: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_income_stmt(self, ticker: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_balance_sheet_quarterly(self, ticker: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_balance_sheet(self, ticker: str) -> pd.DataFrame:
        pass
