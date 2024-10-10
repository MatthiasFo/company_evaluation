import numpy as np
import pandas as pd
from enum import Enum


class FinancialRatios(Enum):
    FREE_CASH_FLOW_OVER_REVENUE = "free_cash_flow_over_revenue"
    NET_MARGIN_OVER_REVENUE = "net_margin_over_revenue"
    RETURN_ON_ASSETS = "return_on_assets"
    RETURN_ON_EQUITY = "return_on_equity"
    ASSET_TURNOVER_RATIO = "asset_turnover_ratio"
    INVENTORY_TURNOVER_RATIO = "inventory_turnover_ratio"
    INVENTORY_OVER_REVENUE = "inventory_over_revenue"
    SGA_OVER_REVENUE = "sga_over_revenue"
    CURRENT_RATIO = "current_ratio"
    QUICK_RATIO = "quick_ratio"
    FIN_LEVERAGE = "fin_leverage"
    ACCOUNTS_RECEIVABLE_OVER_REVENUE = "accounts_receivable_over_revenue"
    EARNINGS_YIELD = "earnings_yield"
    CASH_RETURN = "cash_return"


def calculate_financial_ratios(fin_stmts_with_info: pd.DataFrame) -> pd.DataFrame:
    financial_ratios = fin_stmts_with_info[
        [
            "id",
            "ticker",
            "end_of_period",
            "company_name",
            "sector",
            "industry",
            "country",
        ]
    ].copy()

    # profitablity ratios
    financial_ratios.loc[:, FinancialRatios.FREE_CASH_FLOW_OVER_REVENUE.value] = (
        fin_stmts_with_info["free_cash_flow"] / fin_stmts_with_info["total_revenue"]
    )
    financial_ratios.loc[:, FinancialRatios.NET_MARGIN_OVER_REVENUE.value] = (
        fin_stmts_with_info["net_income"] / fin_stmts_with_info["total_revenue"]
    )
    financial_ratios.loc[:, FinancialRatios.RETURN_ON_ASSETS.value] = (
        fin_stmts_with_info["net_income"] / fin_stmts_with_info["total_assets"]
    )
    financial_ratios.loc[:, FinancialRatios.RETURN_ON_EQUITY.value] = (
        fin_stmts_with_info["net_income"] / fin_stmts_with_info["stockholders_equity"]
    )

    # efficiency ratios
    financial_ratios.loc[:, FinancialRatios.ASSET_TURNOVER_RATIO.value] = (
        fin_stmts_with_info["total_revenue"] / fin_stmts_with_info["total_assets"]
    )
    financial_ratios.loc[:, FinancialRatios.INVENTORY_TURNOVER_RATIO.value] = (
        fin_stmts_with_info["cost_of_goods_sold"] / fin_stmts_with_info["inventory"]
    )
    financial_ratios.loc[:, FinancialRatios.INVENTORY_OVER_REVENUE.value] = (
        fin_stmts_with_info["inventory"] / fin_stmts_with_info["total_revenue"]
    )
    financial_ratios.loc[:, FinancialRatios.SGA_OVER_REVENUE.value] = (
        fin_stmts_with_info["selling_general_and_administration"] / fin_stmts_with_info["total_revenue"]
    )
    # operating_ratio = 100 * (cost_of_goods_sold + operating_expenses) / revenue
    # (need to find operating expenses in yahoo data)

    # financial health ratios
    financial_ratios.loc[:, FinancialRatios.CURRENT_RATIO.value] = (
        fin_stmts_with_info["current_assets"] / fin_stmts_with_info["current_liabilities"]
    )
    financial_ratios.loc[:, FinancialRatios.QUICK_RATIO.value] = (
        fin_stmts_with_info["current_assets"] - fin_stmts_with_info["inventory"]
    ) / fin_stmts_with_info["current_liabilities"]
    financial_ratios.loc[:, FinancialRatios.FIN_LEVERAGE.value] = (
        fin_stmts_with_info["total_assets"] / fin_stmts_with_info["stockholders_equity"]
    )
    # management (should manage credit sales correctly and not dilute my stake in the company)
    financial_ratios.loc[:, FinancialRatios.ACCOUNTS_RECEIVABLE_OVER_REVENUE.value] = (
        fin_stmts_with_info["accounts_receivable"] / fin_stmts_with_info["total_revenue"]
    )

    # return ratios (yield)
    # these calculations mix time series data with momentary data :-(
    financial_ratios.loc[:, FinancialRatios.EARNINGS_YIELD.value] = (
        (
            fin_stmts_with_info["net_income"]
            # TODO: Check if it is correct to use all dividends paid. normaly only the preferred stock dividents are deducted from net_income
            + fin_stmts_with_info["dividends_paid"]  # dividents paid is negative, so we add it
        )
        / fin_stmts_with_info["shares_outstanding"]
    ).fillna(fin_stmts_with_info["earnings_per_share"]) / fin_stmts_with_info["current_price"]

    financial_ratios.loc[:, FinancialRatios.CASH_RETURN.value] = fin_stmts_with_info["free_cash_flow"] / (
        fin_stmts_with_info["market_cap"]
        + fin_stmts_with_info["long_term_debt"]
        - fin_stmts_with_info["cash_and_cash_equivalents"]
    )  # free cash flow / enterprise value

    # remove infinite values
    financial_ratios = financial_ratios.replace([np.inf, -np.inf], np.nan)

    return financial_ratios
