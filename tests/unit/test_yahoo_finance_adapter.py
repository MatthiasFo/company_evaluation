import pytest
import pandas as pd
from unittest.mock import Mock, patch
from src.adapters.yahoo_finance_adapter import YahooFinanceAdapter
from src.domain.scraper import DataValidationError
from tests.mock_data.mock_yahoo_data import (
    mock_yahoo_aapl_info,
    mock_yahoo_sie_info,
    mock_yahoo_aapl_cashflow,
    mock_yahoo_aapl_balance_sheet,
    mock_yahoo_aapl_income_stmt,
    mock_yahoo_sie_cashflow,
    mock_yahoo_sie_balance_sheet,
    mock_yahoo_sie_income_stmt,
)


@pytest.fixture
def yahoo_finance_adapter():
    return YahooFinanceAdapter()


@pytest.fixture
def mock_yf_ticker():
    mock_ticker = Mock()
    mock_ticker.info = mock_yahoo_aapl_info
    mock_ticker.cashflow = mock_yahoo_aapl_cashflow
    mock_ticker.quarterly_cashflow = mock_yahoo_aapl_cashflow
    mock_ticker.balance_sheet = mock_yahoo_aapl_balance_sheet
    mock_ticker.quarterly_balance_sheet = mock_yahoo_aapl_balance_sheet
    mock_ticker.income_stmt = mock_yahoo_aapl_income_stmt
    mock_ticker.quarterly_income_stmt = mock_yahoo_aapl_income_stmt
    return mock_ticker


def test_company_officers_removed_from_info(yahoo_finance_adapter, mock_yf_ticker):
    with patch("yfinance.Ticker", return_value=mock_yf_ticker):
        company_info = yahoo_finance_adapter.get_company_info("AAPL")
    assert "companyOfficers" not in company_info.columns


def test_minimal_company_info_present(yahoo_finance_adapter, mock_yf_ticker):
    with patch("yfinance.Ticker", return_value=mock_yf_ticker):
        company_info = yahoo_finance_adapter.get_company_info("AAPL")
    minimal_info = ["industry", "country", "ticker", "sector", "request_timestamp"]
    assert all(info in company_info.columns for info in minimal_info)


def test_filings_have_end_of_period_column(yahoo_finance_adapter, mock_yf_ticker):
    with patch("yfinance.Ticker", return_value=mock_yf_ticker):
        cashflow = yahoo_finance_adapter.get_cashflow("AAPL")
        balance_sheet = yahoo_finance_adapter.get_balance_sheet("AAPL")
        income_stmt = yahoo_finance_adapter.get_income_stmt("AAPL")

    assert "end_of_period" in cashflow.columns
    assert "end_of_period" in balance_sheet.columns
    assert "end_of_period" in income_stmt.columns


def test_missing_minimal_info_raises_error(yahoo_finance_adapter):
    incomplete_info = {
        "industry": "Technology",
        # 'country': 'United States',
        "ticker": "TSLA",
        # 'sector' is missing
    }
    mock_ticker = Mock()
    mock_ticker.info = incomplete_info

    with patch("yfinance.Ticker", return_value=mock_ticker) as mock_yfinance_ticker:
        mock_yfinance_ticker.return_value.info = incomplete_info
        with pytest.raises(DataValidationError, match="Yahoo: Skipping AAPL since missing: sector | country"):
            yahoo_finance_adapter.get_company_info("TSLA")


def test_column_name_formatting(yahoo_finance_adapter, mock_yf_ticker):
    with patch("yfinance.Ticker", return_value=mock_yf_ticker):
        company_info = yahoo_finance_adapter.get_company_info("AAPL")

    assert all(col.islower() and " " not in col and "." not in col for col in company_info.columns)


def test_id_generation(yahoo_finance_adapter, mock_yf_ticker):
    with patch("yfinance.Ticker", return_value=mock_yf_ticker):
        company_info = yahoo_finance_adapter.get_company_info("AAPL")
        cashflow = yahoo_finance_adapter.get_cashflow("AAPL")

    assert "id" in company_info.columns
    assert "id" in cashflow.columns
    assert all(company_info["id"].str.contains("AAPL"))
    assert all(cashflow["id"].str.contains("AAPL"))


def test_different_tickers(yahoo_finance_adapter):
    mock_aapl_ticker = Mock()
    mock_aapl_ticker.info = mock_yahoo_aapl_info
    mock_aapl_ticker.cashflow = mock_yahoo_aapl_cashflow
    mock_aapl_ticker.balance_sheet = mock_yahoo_aapl_balance_sheet
    mock_aapl_ticker.income_stmt = mock_yahoo_aapl_income_stmt

    mock_sie_ticker = Mock()
    mock_sie_ticker.info = mock_yahoo_sie_info
    mock_sie_ticker.cashflow = mock_yahoo_sie_cashflow
    mock_sie_ticker.balance_sheet = mock_yahoo_sie_balance_sheet
    mock_sie_ticker.income_stmt = mock_yahoo_sie_income_stmt

    with patch("yfinance.Ticker", side_effect=[mock_aapl_ticker, mock_sie_ticker]):
        aapl_info = yahoo_finance_adapter.get_company_info("AAPL")
        aapl_cashflow = yahoo_finance_adapter.get_cashflow("AAPL")
        aapl_balance_sheet = yahoo_finance_adapter.get_balance_sheet("AAPL")
        aapl_income_stmt = yahoo_finance_adapter.get_income_stmt("AAPL")

        sie_info = yahoo_finance_adapter.get_company_info("SIE.DE")
        sie_cashflow = yahoo_finance_adapter.get_cashflow("SIE.DE")
        sie_balance_sheet = yahoo_finance_adapter.get_balance_sheet("SIE.DE")
        sie_income_stmt = yahoo_finance_adapter.get_income_stmt("SIE.DE")

    assert aapl_info["ticker"].iloc[0] == "AAPL"
    assert sie_info["ticker"].iloc[0] == "SIE.DE"

    assert "AAPL" in aapl_cashflow["ticker"].values
    assert "AAPL" in aapl_balance_sheet["ticker"].values
    assert "AAPL" in aapl_income_stmt["ticker"].values

    assert "SIE.DE" in sie_cashflow["ticker"].values
    assert "SIE.DE" in sie_balance_sheet["ticker"].values
    assert "SIE.DE" in sie_income_stmt["ticker"].values


if __name__ == "__main__":
    pytest.main()
