from enum import Enum
import pandas as pd

from src.domain.calculate_financial_ratios import FinancialRatios


class FinancialTrends(Enum):
    SGA_OVER_REVENUE_CHANGE = "sga_over_revenue_change"
    INVENTORY_OVER_REVENUE_CHANGE = "inventory_over_revenue_change"
    ACCOUNTS_RECEIVABLE_OVER_REVENUE_CHANGE = "accounts_receivable_over_revenue_change"
    SHARES_GROWTH = "shares_growth"


def calculate_trends_over_time(ratios: pd.DataFrame, shares_growth: pd.DataFrame) -> pd.DataFrame:
    columns_for_diff = {
        FinancialRatios.SGA_OVER_REVENUE.value: FinancialTrends.SGA_OVER_REVENUE_CHANGE.value,
        FinancialRatios.INVENTORY_OVER_REVENUE.value: FinancialTrends.INVENTORY_OVER_REVENUE_CHANGE.value,
        FinancialRatios.ACCOUNTS_RECEIVABLE_OVER_REVENUE.value: FinancialTrends.ACCOUNTS_RECEIVABLE_OVER_REVENUE_CHANGE.value,
    }

    ratio_trends = (
        ratios.set_index(["ticker", "end_of_period"])
        .sort_index()
        .groupby(level="ticker")[[x for x in columns_for_diff.keys()]]
        .diff()
    )
    ratio_trends.rename(columns=columns_for_diff, inplace=True)
    ratio_trends.reset_index(inplace=True)

    financial_trends = ratio_trends.merge(
        shares_growth,
        on=["ticker", "end_of_period"],
        how="left",
    )

    return financial_trends
