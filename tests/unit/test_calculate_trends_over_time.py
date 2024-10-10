import pandas as pd
import pytest
from src.domain.calculate_trends_over_time import calculate_trends_over_time


def test_calculate_trends_over_time():
    ratios_data = {
        "ticker": ["A", "A", "B", "B"],
        "end_of_period": ["2021-12-31", "2022-12-31", "2021-12-31", "2022-12-31"],
        "sga_over_revenue": [0.1, 0.15, 0.2, 0.25],
        "inventory_over_revenue": [0.3, 0.35, 0.4, 0.45],
        "accounts_receivable_over_revenue": [0.5, 0.55, 0.6, 0.65],
    }
    ratios_df = pd.DataFrame(ratios_data)

    shares_growth_data = {
        "ticker": ["A", "A", "B", "B"],
        "end_of_period": ["2021-12-31", "2022-12-31", "2021-12-31", "2022-12-31"],
        "shares_growth": [0.02, 0.03, 0.01, 0.04],
    }
    shares_growth_df = pd.DataFrame(shares_growth_data)

    expected_data = {
        "ticker": ["A", "A", "B", "B"],
        "end_of_period": ["2021-12-31", "2022-12-31", "2021-12-31", "2022-12-31"],
        "sga_over_revenue_change": [None, 0.05, None, 0.05],
        "inventory_over_revenue_change": [None, 0.05, None, 0.05],
        "accounts_receivable_over_revenue_change": [None, 0.05, None, 0.05],
        "shares_growth": [0.02, 0.03, 0.01, 0.04],
    }
    expected_df = pd.DataFrame(expected_data)

    result_df = calculate_trends_over_time(ratios_df, shares_growth_df)

    pd.testing.assert_frame_equal(result_df, expected_df)
