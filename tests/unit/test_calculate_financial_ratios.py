import pytest
import pandas as pd
from src.domain.calculate_financial_ratios import calculate_financial_ratios


@pytest.fixture
def mock_data():
    return pd.DataFrame(
        {
            "id": [1],
            "ticker": ["TEST"],
            "end_of_period": ["2023-12-31"],
            "company_name": ["Test Company"],
            "sector": ["Technology"],
            "industry": ["Software"],
            "country": ["USA"],
            "free_cash_flow": [100],
            "total_revenue": [1000],
            "net_income": [200],
            "total_assets": [500],
            "stockholders_equity": [300],
            "cost_of_goods_sold": [400],
            "inventory": [100],
            "selling_general_and_administration": [50],
            "current_assets": [200],
            "current_liabilities": [100],
            "accounts_receivable": [150],
            "dividends_paid": [-20],
            "shares_outstanding": [50],
            "current_price": [10],
            "market_cap": [5000],
            "long_term_debt": [1000],
            "cash_and_cash_equivalents": [200],
            "earnings_per_share": [2.5],
        }
    )


def test_calculate_financial_ratios(mock_data):
    result = calculate_financial_ratios(mock_data)

    assert result["free_cash_flow_over_revenue"][0] == pytest.approx(0.1)
    assert result["net_margin_over_revenue"][0] == pytest.approx(0.2)
    assert result["return_on_assets"][0] == pytest.approx(0.4)
    assert result["return_on_equity"][0] == pytest.approx(0.6667, rel=1e-4)
    assert result["asset_turnover_ratio"][0] == pytest.approx(2.0)
    assert result["inventory_turnover_ratio"][0] == pytest.approx(4.0)
    assert result["inventory_over_revenue"][0] == pytest.approx(0.1)
    assert result["sga_over_revenue"][0] == pytest.approx(0.05)
    assert result["current_ratio"][0] == pytest.approx(2.0)
    assert result["quick_ratio"][0] == pytest.approx(1.0)
    assert result["fin_leverage"][0] == pytest.approx(1.6667, rel=1e-4)
    assert result["accounts_receivable_over_revenue"][0] == pytest.approx(0.15)
    assert result["earnings_yield"][0] == pytest.approx(0.36, rel=1e-3)
    assert result["cash_return"][0] == pytest.approx(0.01724137, rel=1e-5)
