import pandas as pd
import pytest
from src.domain.financial_evaluator import FinancialEvaluator


@pytest.fixture
def financial_evaluator() -> FinancialEvaluator:
    """Fixture to set up a sample FinancialEvaluator instance with extended mock data."""
    fin_stmts = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "filing_id": [1, 2, 3, 4, 5],
            "ticker": ["AAPL", "AAPL", "AAPL", "GOOGL", "GOOGL"],
            "end_of_period": ["2021-12-31", "2022-12-31", "2023-12-31", "2021-12-31", "2022-12-31"],
            "company_name": ["Apple Inc.", "Apple Inc.", "Apple Inc.", "Alphabet Inc.", "Alphabet Inc."],
            "sector": ["Technology", "Technology", "Technology", "Communication Services", "Communication Services"],
            "industry": [
                "Consumer Electronics",
                "Consumer Electronics",
                "Consumer Electronics",
                "Internet Content & Information",
                "Internet Content & Information",
            ],
            "country": ["USA", "USA", "USA", "USA", "USA"],
            "free_cash_flow": [100, 150, 200, 250, 300],
            "total_revenue": [1000, 1200, 1400, 2000, 2200],
            "revenue_growth": [100, 200, 200, 600, 200],
            "net_income": [200, 250, 300, 400, 450],
            "total_assets": [5000, 5500, 6000, 7000, 7500],
            "stockholders_equity": [3000, 3200, 3500, 4000, 4200],
            "cost_of_goods_sold": [600, 700, 800, 1000, 1100],
            "inventory": [100, 120, 140, 200, 220],
            "selling_general_and_administration": [150, 180, 200, 300, 320],
            "current_assets": [2000, 2200, 2400, 3000, 3200],
            "current_liabilities": [1000, 1100, 1200, 1500, 1600],
            "accounts_receivable": [300, 350, 400, 500, 550],
            "dividends_paid": [-50, -60, -70, -80, -90],
            "shares_outstanding": [1000, 1000, 1000, 2000, 2000],
            "current_price": [150, 160, 170, 2500, 2600],
            "market_cap": [1500000, 1600000, 1700000, 2500000, 2600000],
            "long_term_debt": [500, 600, 700, 800, 900],
            "cash_and_cash_equivalents": [200, 250, 300, 400, 450],
            "shares_growth": [0.02, 0.03, 0.04, 0.01, 0.02],
            "earnings_per_share": [0.02, 0.03, 0.04, 0.01, 0.02],
        }
    )
    return FinancialEvaluator(fin_stmts)


def test_evaluate_time_series(financial_evaluator: FinancialEvaluator):
    """Test the evaluate_time_series method."""
    result = financial_evaluator.get_ratios_and_trends()
    assert isinstance(result, pd.DataFrame)

    expected_columns = [
        "id",
        "ticker",
        "company_name",
        "country",
        "industry",
        "sector",
        "end_of_period",
        "free_cash_flow_over_revenue",
        "net_margin_over_revenue",
        "return_on_assets",
        "return_on_equity",
        "asset_turnover_ratio",
        "inventory_turnover_ratio",
        "inventory_over_revenue",
        "sga_over_revenue",
        "current_ratio",
        "quick_ratio",
        "fin_leverage",
        "accounts_receivable_over_revenue",
        "earnings_yield",
        "cash_return",
        "guideline_score",
        "free_cash_flow_over_revenue_competition",
        "net_margin_over_revenue_competition",
        "return_on_assets_competition",
        "return_on_equity_competition",
        "asset_turnover_ratio_competition",
        "inventory_turnover_ratio_competition",
        "inventory_over_revenue_competition",
        "sga_over_revenue_competition",
        "current_ratio_competition",
        "quick_ratio_competition",
        "fin_leverage_competition",
        "accounts_receivable_over_revenue_competition",
        "earnings_yield_competition",
        "cash_return_competition",
        "filing_id",
        "total_revenue",
        "net_income",
        "cost_of_goods_sold",
        "selling_general_and_administration",
        "free_cash_flow",
        "dividends_paid",
        "stockholders_equity",
        "total_assets",
        "accounts_receivable",
        "cash_and_cash_equivalents",
        "current_assets",
        "current_liabilities",
        "inventory",
        "long_term_debt",
        "revenue_growth",
        "shares_growth",
        "sga_over_revenue_change",
        "inventory_over_revenue_change",
        "accounts_receivable_over_revenue_change",
        "sga_over_revenue_change_competition",
        "inventory_over_revenue_change_competition",
        "accounts_receivable_over_revenue_change_competition",
        "shares_growth_competition",
    ]
    assert [x for x in expected_columns if x not in result.columns] == []


def test_evaluate_current_value(financial_evaluator: FinancialEvaluator):
    """Test the evaluate_current_value method."""
    result = financial_evaluator.get_current_evaluation()

    expected_columns = [
        "ticker",
        "company_name",
        "country",
        "industry",
        "sector",
        "free_cash_flow_over_revenue",
        "net_margin_over_revenue",
        "return_on_assets",
        "return_on_equity",
        "asset_turnover_ratio",
        "inventory_turnover_ratio",
        "inventory_over_revenue",
        "sga_over_revenue",
        "current_ratio",
        "quick_ratio",
        "fin_leverage",
        "accounts_receivable_over_revenue",
        "earnings_yield",
        "cash_return",
        "guideline_score",
        "free_cash_flow_over_revenue_competition",
        "net_margin_over_revenue_competition",
        "return_on_assets_competition",
        "return_on_equity_competition",
        "asset_turnover_ratio_competition",
        "inventory_turnover_ratio_competition",
        "inventory_over_revenue_competition",
        "sga_over_revenue_competition",
        "current_ratio_competition",
        "quick_ratio_competition",
        "fin_leverage_competition",
        "accounts_receivable_over_revenue_competition",
        "earnings_yield_competition",
        "cash_return_competition",
        "revenue_growth",
        "shares_growth",
        "sga_over_revenue_change",
        "inventory_over_revenue_change",
        "accounts_receivable_over_revenue_change",
        "sga_over_revenue_change_competition",
        "inventory_over_revenue_change_competition",
        "accounts_receivable_over_revenue_change_competition",
        "shares_growth_competition",
        "current_price",
        "normal",
        "stable",
        "stable_and_strong_growth",
        "volatile",
        "volatile_and_weak_growth",
        "current_price_over_normal_dcf",
        "free_cash_flow",
        "shares_outstanding",
        "guideline_score_competition",
    ]

    assert isinstance(result, pd.DataFrame)
    assert [x for x in expected_columns if x not in result.columns] == []


if __name__ == "__main__":
    pytest.main()
