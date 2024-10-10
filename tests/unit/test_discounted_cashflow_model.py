import pytest
import pandas as pd
from src.domain.discounted_cashflow_model import DCFModel


@pytest.fixture
def mock_info_data():
    return pd.DataFrame(
        [
            {
                "ticker": "AAPL",
                "current_price": 220.82,
                "shares_outstanding": 15204100096,
            },
            {
                "ticker": "RCL",
                "current_price": 161.43,
                "shares_outstanding": 257420000,
            },
        ]
    )


def test_discounted_cashflow_model_basic(mock_info_data):
    mock_filing_data = pd.DataFrame(
        [
            {"free_cash_flow": -580000000.0, "revenue_growth": 0.57230214443914063, "ticker": "RCL"},
            {"free_cash_flow": 99584000000.0, "revenue_growth": -0.028004605303199367, "ticker": "AAPL"},
        ]
    )

    base_data = mock_filing_data.merge(mock_info_data, how="left", on="ticker").set_index("ticker")
    dcf_model = DCFModel(base_data)

    result = dcf_model.estimate_intrinsic_value()

    assert set(result.columns) == set(
        ["ticker", "current_price", "shares_outstanding", "free_cash_flow", "revenue_growth"]
        + [
            "normal",
            "stable",
            "stable_and_strong_growth",
            "volatile",
            "volatile_and_weak_growth",
            "current_price_over_normal_dcf",
        ]
    )
    assert not result.isna().any().any()
    assert result["normal"].min() > 0
    assert result["ticker"].nunique() == 1  # RCL is excluded since it has negative average cash flow


def test_discounted_cashflow_model_zero_free_cash_flow(mock_info_data):
    mock_filing_data = pd.DataFrame([{"free_cash_flow": 0, "revenue_growth": 0.1, "ticker": "AAPL"}])

    base_data = mock_filing_data.merge(mock_info_data, how="left", on="ticker").set_index("ticker")
    dcf_model = DCFModel(base_data)

    result = dcf_model.estimate_intrinsic_value()

    assert len(result) == 0


def test_discounted_cashflow_model_negative_free_cash_flow(mock_info_data):
    mock_filing_data = pd.DataFrame([{"free_cash_flow": -1000000, "revenue_growth": 0.1, "ticker": "AAPL"}])

    base_data = mock_filing_data.merge(mock_info_data, how="left", on="ticker").set_index("ticker")
    dcf_model = DCFModel(base_data)
    result = dcf_model.estimate_intrinsic_value()

    assert len(result) == 0


def test_discounted_cashflow_model_normal_case_result(mock_info_data):
    # normal case config to test the algorithm:
    # 10.5% discount rate
    # 4 percent general growth rate
    # 10 year forecasting horizon
    mock_filing_data = pd.DataFrame([{"free_cash_flow": 72584000000, "revenue_growth": 0.04, "ticker": "AAPL"}])
    base_data = mock_filing_data.merge(mock_info_data, how="left", on="ticker").set_index("ticker")
    dcf_model = DCFModel(base_data)

    result = dcf_model.estimate_intrinsic_value()
    assert result["normal"][0] == pytest.approx(76.3836, rel=1e-2)


if __name__ == "__main__":
    pytest.main()
