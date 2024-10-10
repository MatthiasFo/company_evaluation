import pytest
import pandas as pd
from unittest.mock import patch
from src.adapters.financial_modeling_prep_adapter import FinancialModelingPrepAdapter
from src.domain.scraper import ApiLimitReached, DataValidationError
from tests.mock_data.mock_fmp_data import (
    fmp_balance_sheet_json,
    fmp_cashflow_json,
    fmp_growth_json,
    fmp_income_json,
    fmp_quote_json,
    fmp_profile_json,
)
import copy


@pytest.fixture
def fmp_adapter():
    with patch("src.adapters.financial_modeling_prep_adapter.GcpSecretManager") as mock_gcp:
        mock_gcp.return_value.get_secret.return_value = "dummy_api_key"
        return FinancialModelingPrepAdapter()


@pytest.fixture
def mock_requests_get():
    with patch("src.adapters.financial_modeling_prep_adapter.requests.get") as mock_get:
        yield mock_get


def test_get_profile_info_success(fmp_adapter, mock_requests_get):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = fmp_profile_json

    result = fmp_adapter.get_profile_info("AAPL")

    assert isinstance(result, pd.DataFrame)
    assert "id" in result.columns
    assert "requestTimestamp" in result.columns
    assert set(["symbol", "companyName", "industry", "country", "sector"]).issubset(result.columns)


def test_get_profile_info_empty_response(fmp_adapter, mock_requests_get):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = []

    with pytest.raises(DataValidationError, match="FMP: Request data is empty."):
        fmp_adapter.get_profile_info("AAPL")


def test_get_profile_info_missing_mandatory_column(fmp_adapter, mock_requests_get):
    incomplete_profile = copy.deepcopy(fmp_profile_json)
    del incomplete_profile[0]["industry"]
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = incomplete_profile

    with pytest.raises(DataValidationError, match="FMP: Mandatory profile column missing for AAPL"):
        fmp_adapter.get_profile_info("AAPL")


def test_get_profile_info_null_value_in_mandatory_column(fmp_adapter, mock_requests_get):
    incomplete_profile = copy.deepcopy(fmp_profile_json)
    incomplete_profile[0]["country"] = "null"
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = incomplete_profile

    with pytest.raises(DataValidationError, match="FMP: Data in mandatory profile column missing for AAPL"):
        fmp_adapter.get_profile_info("AAPL")


def test_get_quote_success(fmp_adapter, mock_requests_get):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = fmp_quote_json

    result = fmp_adapter.get_quote("AAPL")

    assert isinstance(result, pd.DataFrame)
    assert "id" in result.columns
    assert "requestTimestamp" in result.columns
    assert pd.api.types.is_datetime64_any_dtype(result["earningsAnnouncement"])


def test_get_financial_growth_success(fmp_adapter, mock_requests_get):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = fmp_growth_json

    result = fmp_adapter.get_financial_growth("AAPL")

    assert isinstance(result, pd.DataFrame)
    assert "id" in result.columns
    assert "requestTimestamp" in result.columns


def test_get_balance_sheet_success(fmp_adapter, mock_requests_get):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = fmp_balance_sheet_json

    result = fmp_adapter.get_balance_sheet("AAPL")

    assert isinstance(result, pd.DataFrame)
    assert "id" in result.columns
    assert "requestTimestamp" in result.columns
    assert result["cashAndCashEquivalents"].dtype == "int64"


def test_get_balance_sheet_validation_error(fmp_adapter, mock_requests_get):
    incomplete_balance_sheet = copy.deepcopy(fmp_balance_sheet_json)
    incomplete_balance_sheet[0]["cashAndCashEquivalents"] = "invalid"
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = incomplete_balance_sheet

    with pytest.raises(DataValidationError, match="FMP: Data validation failed on balance sheets for AAPL"):
        fmp_adapter.get_balance_sheet("AAPL")


def test_get_cash_flow_success(fmp_adapter, mock_requests_get):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = fmp_cashflow_json

    result = fmp_adapter.get_cash_flow("AAPL")

    assert isinstance(result, pd.DataFrame)
    assert "id" in result.columns
    assert "requestTimestamp" in result.columns
    assert result["netIncome"].dtype == "int64"


def test_get_cash_flow_empty_response(fmp_adapter, mock_requests_get):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = []

    with pytest.raises(DataValidationError, match="FMP: Request data is empty."):
        fmp_adapter.get_cash_flow("AAPL")


def test_get_income_statement_success(fmp_adapter, mock_requests_get):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = fmp_income_json

    result = fmp_adapter.get_income_statement("AAPL")

    assert isinstance(result, pd.DataFrame)
    assert "id" in result.columns
    assert "requestTimestamp" in result.columns
    assert result["revenue"].dtype == "int64"
    assert result["eps"].dtype == "float64"


def test_api_limit_reached(fmp_adapter, mock_requests_get):
    mock_requests_get.return_value.status_code = 429

    with pytest.raises(ApiLimitReached, match="FMP: API limit reached"):
        fmp_adapter.get_profile_info("AAPL")


def test_other_request_error(fmp_adapter, mock_requests_get):
    mock_requests_get.return_value.status_code = 500
    mock_requests_get.return_value.text = "Internal Server Error"

    with pytest.raises(Exception, match="FMP: Request to .* failed with status code 500: Internal Server Error"):
        fmp_adapter.get_profile_info("AAPL")
