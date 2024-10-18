from abc import ABC, abstractmethod
from typing import List
import pandas as pd


class DataMartPort(ABC):
    @abstractmethod
    def get_remaining_tickers_for_alphavantage_scraper(self) -> List[str]:
        pass

    @abstractmethod
    def get_remaining_tickers_for_fmp_scraper(self) -> List[str]:
        pass

    @abstractmethod
    def get_remaining_tickers_for_yahoo_scraper(self) -> List[str]:
        pass

    @abstractmethod
    def get_dcf_base_data(self) -> pd.DataFrame:
        pass
