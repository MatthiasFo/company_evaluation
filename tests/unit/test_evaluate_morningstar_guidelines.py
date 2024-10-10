import pytest
import pandas as pd
from src.domain.calculate_trends_over_time import FinancialTrends
from src.domain.evaluate_guidelines import GuidelinesEvaluator
from src.domain.calculate_financial_ratios import FinancialRatios


@pytest.fixture
def financial_data_economic_moat():
    return pd.DataFrame(
        {
            FinancialRatios.RETURN_ON_ASSETS.value: [0.07, 0.05, 0.08],
            FinancialRatios.RETURN_ON_EQUITY.value: [0.16, 0.14, 0.12],
            FinancialRatios.NET_MARGIN_OVER_REVENUE.value: [0.16, 0.14, 0.10],
            FinancialRatios.FREE_CASH_FLOW_OVER_REVENUE.value: [0.06, 0.04, 0.05],
        }
    )


@pytest.fixture
def financial_data_financial_health():
    return pd.DataFrame(
        {
            "sector": ["Technology", "Technology", "Financial Services"],
            FinancialRatios.CURRENT_RATIO.value: [1.6, 1.4, 1.6],
            FinancialRatios.QUICK_RATIO.value: [1.1, 0.9, 1.1],
            FinancialRatios.FIN_LEVERAGE.value: [3.5, 4.5, 5.0],
        }
    )


@pytest.fixture
def financial_data_yields():
    return pd.DataFrame(
        {
            FinancialRatios.EARNINGS_YIELD.value: [0.07, 0.05, 0.03],
            FinancialRatios.CASH_RETURN.value: [0.07, 0.05, 0.06],
        }
    )


@pytest.fixture
def financial_data_efficiency():
    return pd.DataFrame(
        {
            FinancialRatios.SGA_OVER_REVENUE.value + "_competition": [0.1, 0.1, 0.1],
            FinancialRatios.SGA_OVER_REVENUE.value: [0.15, 0.05, 0.05],
            FinancialTrends.SGA_OVER_REVENUE_CHANGE.value: [0.1, 0.0, -0.1],
            FinancialTrends.INVENTORY_OVER_REVENUE_CHANGE.value: [0.2, 0.2, -0.1],
        }
    )


@pytest.fixture
def financial_data_management():
    return pd.DataFrame(
        {
            FinancialTrends.ACCOUNTS_RECEIVABLE_OVER_REVENUE_CHANGE.value: [0, -0.1, 0.1],
            FinancialTrends.SHARES_GROWTH.value: [0.01, 0.03, 0.03],
        }
    )


def test_guidelines_evaluator(
    financial_data_economic_moat,
    financial_data_financial_health,
    financial_data_yields,
    financial_data_efficiency,
    financial_data_management,
):
    combined_data = pd.concat(
        [
            financial_data_economic_moat,
            financial_data_financial_health,
            financial_data_yields,
            financial_data_efficiency,
            financial_data_management,
        ],
        axis=1,
    )
    evaluator = GuidelinesEvaluator(combined_data)
    result = evaluator.evaluate_guidelines()

    expected_result = pd.Series([11, 3, 6], dtype=int)
    pd.testing.assert_series_equal(result.astype(int), expected_result)


def test_economic_moat_evaluation(financial_data_economic_moat):
    evaluator = GuidelinesEvaluator(financial_data_economic_moat)
    result = evaluator._evaluate_economic_moat()

    expected_result = pd.Series([4, 0, 2])
    pd.testing.assert_series_equal(result, expected_result)


def test_financial_health_evaluation(financial_data_financial_health):
    evaluator = GuidelinesEvaluator(financial_data_financial_health)
    result = evaluator._evaluate_financial_health()

    expected_result = pd.Series([3, 0])
    pd.testing.assert_series_equal(result, expected_result)


def test_yield_evaluation(financial_data_yields):
    evaluator = GuidelinesEvaluator(financial_data_yields)
    result = evaluator._evaluate_yields()

    expected_result = pd.Series([2, 0, 1])
    pd.testing.assert_series_equal(result, expected_result)


def test_efficiency_evaluation(financial_data_efficiency):
    evaluator = GuidelinesEvaluator(financial_data_efficiency)
    result = evaluator._evaluate_efficiency()

    expected_result = pd.Series([0, 2, 3])
    pd.testing.assert_series_equal(result, expected_result)


def test_management_evaluation(financial_data_management):
    evaluator = GuidelinesEvaluator(financial_data_management)
    result = evaluator._evaluate_mgmt()

    expected_result = pd.Series([2, 1, 0])
    pd.testing.assert_series_equal(result, expected_result)


if __name__ == "__main__":
    pytest.main()
