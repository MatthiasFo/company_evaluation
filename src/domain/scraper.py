from abc import ABC, abstractmethod
import time
from typing import Dict, List
import random

import pandas as pd
from typing import Callable

from src.ports.datastorage_port import DatastoragePort


class ApiLimitReached(Exception):
    pass


class DataValidationError(Exception):
    pass


class DataSourceInterface(ABC):
    source_name: str

    @abstractmethod
    def fetch_data(self, ticker: str) -> Dict[str, pd.DataFrame]:
        pass


class DataSource(DataSourceInterface):
    def __init__(self, source_name: str, fetch_function: Callable[[str], Dict[str, pd.DataFrame]]):
        self.source_name = source_name
        self._fetch_function = fetch_function

    def fetch_data(self, ticker: str) -> Dict[str, pd.DataFrame]:
        return self._fetch_function(ticker)


class Scraper:
    def __init__(self, data_sources: List[DataSourceInterface], data_storage: DatastoragePort, scraper_name: str):
        self.data_sources = data_sources
        self.data_storage = data_storage
        self.scraper_name = scraper_name

    def scrape_company_data(self, tickers: List[str], api_stock_limit: int, time_limit_in_sec: int) -> str:
        sample_size = min(100, len(tickers))
        if sample_size == 0:
            return "No new tickers to process"
        stock_to_analyze = random.sample(tickers, sample_size)

        count_successes = 0
        start_time = time.time()
        for ticker in stock_to_analyze:
            if (time.time() - start_time) > time_limit_in_sec:
                break
            if count_successes >= api_stock_limit:
                print(f"{self.scraper_name} scraper: Reached {api_stock_limit} successes, exiting loop.")
                break

            print(f"{self.scraper_name} scraper: Processing {ticker}")

            fetched_data = {}
            for data_source in self.data_sources:
                try:
                    print(f"{self.scraper_name} scraper: Fetching {data_source.source_name} for {ticker}")
                    data: Dict = data_source.fetch_data(ticker)
                except ApiLimitReached:
                    print(f"{self.scraper_name} scraper: API limit reached, exiting loop.")
                    return f"{self.scraper_name} scraper: API limit reached after {count_successes} new stocks."
                except DataValidationError as e:
                    print(f"{self.scraper_name} scraper: {str(e)}")
                    fetched_data = None
                    break

                if any(value is None for value in data.values()):
                    print(
                        f"{self.scraper_name} scraper: One of the values in {data_source.source_name} for {ticker} is None, continue with next ticker."
                    )
                    fetched_data = None
                    break

                fetched_data.update(data)

            if fetched_data is None:
                # continue with next ticker if fetched_data is None, which means a mandatory data could not be fetched
                continue

            # For optional data, which fails the data validation, adapters return None and this should not be written to big query
            cleaned_fetched_data = {k: v for k, v in fetched_data.items() if v is not None}

            self.data_storage.store_data_to_tables(cleaned_fetched_data)
            count_successes += 1
        return f"Fetched {count_successes} new stocks and stored in warehouse"


class ScraperFactory:
    @staticmethod
    def create_scraper(
        data_sources: List[DataSourceInterface], data_storage: DatastoragePort, scraper_name: str
    ) -> Scraper:
        return Scraper(data_sources, data_storage, scraper_name)
