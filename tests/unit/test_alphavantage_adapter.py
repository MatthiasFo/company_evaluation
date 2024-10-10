import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.adapters.alphavantage_adapter import AlphavantageAdapter
from src.domain.scraper import ApiLimitReached, DataValidationError
from tests.mock_data.mock_alphavantage_data import (
    alphavantage_cashflow_json,
    alphavantage_income_json,
    alphavantage_balance_sheet_json,
)


@pytest.fixture
def alphavantage_adapter():
    with patch("src.adapters.alphavantage_adapter.GcpSecretManager") as mock_gcp:
        mock_gcp.return_value.get_secret.return_value = "dummy_api_key"
        return AlphavantageAdapter()


@pytest.fixture
def mock_requests_get():
    with patch("src.adapters.alphavantage_adapter.requests.get") as mock_get:
        yield mock_get


def test_get_balance_sheet_success(alphavantage_adapter, mock_requests_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = alphavantage_balance_sheet_json
    mock_requests_get.return_value = mock_response

    result = alphavantage_adapter.get_balance_sheet("IBM")

    assert "annualReports" in result
    assert "quarterlyReports" in result
    assert isinstance(result["annualReports"], pd.DataFrame)
    assert isinstance(result["quarterlyReports"], pd.DataFrame)
    assert result["annualReports"]["totalAssets"].iloc[0] == 135241000000
    assert result["quarterlyReports"]["totalAssets"].iloc[0] == 137169000000


def test_get_cash_flow_success(alphavantage_adapter, mock_requests_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = alphavantage_cashflow_json
    mock_requests_get.return_value = mock_response

    result = alphavantage_adapter.get_cash_flow("IBM")

    assert "annualReports" in result
    assert "quarterlyReports" in result
    assert isinstance(result["annualReports"], pd.DataFrame)
    assert isinstance(result["quarterlyReports"], pd.DataFrame)
    assert result["annualReports"]["operatingCashflow"].iloc[0] == 13931000000
    assert result["quarterlyReports"]["operatingCashflow"].iloc[0] == 4168000000


def test_get_income_statement_success(alphavantage_adapter, mock_requests_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = alphavantage_income_json
    mock_requests_get.return_value = mock_response

    result = alphavantage_adapter.get_income_statement("IBM")

    assert "annualReports" in result
    assert "quarterlyReports" in result
    assert isinstance(result["annualReports"], pd.DataFrame)
    assert isinstance(result["quarterlyReports"], pd.DataFrame)
    assert result["annualReports"]["totalRevenue"].iloc[0] == 61860000000
    assert result["quarterlyReports"]["totalRevenue"].iloc[0] == 14462000000


def test_get_cash_flow_api_limit_reached(alphavantage_adapter, mock_requests_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"Information": "API limit reached"}
    mock_requests_get.return_value = mock_response

    with pytest.raises(ApiLimitReached):
        alphavantage_adapter.get_cash_flow("IBM")


def test_get_income_statement_data_validation_error(alphavantage_adapter, mock_requests_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"symbol": "IBM"}  # Missing 'annualReports'
    mock_requests_get.return_value = mock_response

    with pytest.raises(DataValidationError):
        alphavantage_adapter.get_income_statement("IBM")


def test_incomplete_balance_sheet(alphavantage_adapter, mock_requests_get):
    incomplete_data = alphavantage_balance_sheet_json.copy()
    incomplete_data["annualReports"][0]["totalAssets"] = "None"
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = incomplete_data
    mock_requests_get.return_value = mock_response

    result = alphavantage_adapter.get_balance_sheet("IBM")

    assert "annualReports" in result
    assert "quarterlyReports" in result
    assert result["annualReports"]["totalAssets"].iloc[0] == 0  # Default to 0 for 'None' values


def test_empty_cash_flow(alphavantage_adapter, mock_requests_get):
    empty_data = alphavantage_cashflow_json.copy()
    empty_data["annualReports"] = []
    empty_data["quarterlyReports"] = []
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = empty_data
    mock_requests_get.return_value = mock_response

    with pytest.raises(DataValidationError):
        alphavantage_adapter.get_cash_flow("IBM")


def test_empty_income_statement(alphavantage_adapter, mock_requests_get):
    empty_data = alphavantage_income_json.copy()
    empty_data["annualReports"] = []
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = empty_data
    mock_requests_get.return_value = mock_response

    with pytest.raises(DataValidationError):
        alphavantage_adapter.get_income_statement("IBM")


def test_request_failure(alphavantage_adapter, mock_requests_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_requests_get.return_value = mock_response

    with pytest.raises(Exception, match="Request to .* failed with status code 404"):
        alphavantage_adapter.get_balance_sheet("IBM")


def test_enhance_with_fiscal_date_ending_id(alphavantage_adapter):
    data = {"fiscalDateEnding": ["2022-12-31"], "report_type": ["annualReports"], "symbol": ["IBM"]}
    df = pd.DataFrame(data)

    result = alphavantage_adapter._enhance_with_fiscal_date_ending_id(df)

    assert "id" in result.columns
    assert result["id"].iloc[0] == "2022-12-31_annualReports_IBM"


if __name__ == "__main__":
    pytest.main()
