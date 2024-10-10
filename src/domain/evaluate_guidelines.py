import pandas as pd

from src.domain.calculate_trends_over_time import FinancialTrends
from src.domain.calculate_financial_ratios import FinancialRatios


class GuidelinesEvaluator:
    # Define threshold values as class properties
    THRESHOLD_ECONOMIC_MOAT_ROA = 0.06
    THRESHOLD_ECONOMIC_MOAT_ROE = 0.15
    THRESHOLD_ECONOMIC_MOAT_NET_MARGIN = 0.15
    THRESHOLD_ECONOMIC_MOAT_FREE_CASH_FLOW = 0.05

    THRESHOLD_FINANCIAL_HEALTH_CURRENT_RATIO = 1.5
    THRESHOLD_FINANCIAL_HEALTH_QUICK_RATIO = 1.0
    THRESHOLD_FINANCIAL_HEALTH_FIN_LEVERAGE = 4.0

    BASE_YIELD = 0.06  # take 6% based on the estimate from The Intelligent Investor page 85 ff
    THRESHOLD_MANAGEMENT_SHARES_GROWTH = 0.02

    def __init__(self, fin_indicators: pd.DataFrame):
        self.fin_indicators = fin_indicators

    def evaluate_guidelines(self) -> pd.Series:
        moat_score = self._evaluate_economic_moat()
        financial_health_score = self._evaluate_financial_health()
        total_score = moat_score.add(financial_health_score, fill_value=0)

        yield_score = self._evaluate_yields()
        total_score = total_score.add(yield_score, fill_value=0)

        efficiency_score = self._evaluate_efficiency()
        total_score = total_score.add(efficiency_score, fill_value=0)

        management_score = self._evaluate_mgmt()
        total_score = total_score.add(management_score, fill_value=0)

        return total_score

    def _evaluate_economic_moat(self) -> pd.Series:
        return (
            self._evaluate_indicator(
                self.fin_indicators[FinancialRatios.RETURN_ON_ASSETS.value], ">=", self.THRESHOLD_ECONOMIC_MOAT_ROA
            )
            .add(
                self._evaluate_indicator(
                    self.fin_indicators[FinancialRatios.RETURN_ON_EQUITY.value], ">=", self.THRESHOLD_ECONOMIC_MOAT_ROE
                )
            )
            .add(
                self._evaluate_indicator(
                    self.fin_indicators[FinancialRatios.NET_MARGIN_OVER_REVENUE.value],
                    ">=",
                    self.THRESHOLD_ECONOMIC_MOAT_NET_MARGIN,
                )
            )
            .add(
                self._evaluate_indicator(
                    self.fin_indicators[FinancialRatios.FREE_CASH_FLOW_OVER_REVENUE.value],
                    ">=",
                    self.THRESHOLD_ECONOMIC_MOAT_FREE_CASH_FLOW,
                )
            )
        )

    def _evaluate_financial_health(self) -> pd.Series:
        # use different thresholds for financial companies since they are usually highly leveraged
        # TODO: define these thresholds
        idx_nonfin = self.fin_indicators["sector"] != "Financial Services"
        return (
            self._evaluate_indicator(
                self.fin_indicators.loc[idx_nonfin, FinancialRatios.CURRENT_RATIO.value],
                ">=",
                self.THRESHOLD_FINANCIAL_HEALTH_CURRENT_RATIO,
            )
            .add(
                self._evaluate_indicator(
                    self.fin_indicators.loc[idx_nonfin, FinancialRatios.QUICK_RATIO.value],
                    ">=",
                    self.THRESHOLD_FINANCIAL_HEALTH_QUICK_RATIO,
                )
            )
            .add(
                self._evaluate_indicator(
                    self.fin_indicators.loc[idx_nonfin, FinancialRatios.FIN_LEVERAGE.value],
                    "<=",
                    self.THRESHOLD_FINANCIAL_HEALTH_FIN_LEVERAGE,
                )
            )
        )

    def _evaluate_yields(self) -> pd.Series:
        return self._evaluate_indicator(
            self.fin_indicators[FinancialRatios.EARNINGS_YIELD.value], ">=", self.BASE_YIELD
        ).add(self._evaluate_indicator(self.fin_indicators[FinancialRatios.CASH_RETURN.value], ">=", self.BASE_YIELD))

    def _evaluate_efficiency(self) -> pd.Series:
        return (
            self._evaluate_indicator(
                self.fin_indicators[FinancialRatios.SGA_OVER_REVENUE.value],
                "<=",
                self.fin_indicators[FinancialRatios.SGA_OVER_REVENUE.value + "_competition"],
            )
            .add(self._evaluate_indicator(self.fin_indicators[FinancialTrends.SGA_OVER_REVENUE_CHANGE.value], "<=", 0))
            .add(
                self._evaluate_indicator(
                    self.fin_indicators[FinancialTrends.INVENTORY_OVER_REVENUE_CHANGE.value],
                    "<=",
                    0,
                )
            )
        )

    def _evaluate_mgmt(self) -> pd.Series:
        return self._evaluate_indicator(
            self.fin_indicators[FinancialTrends.ACCOUNTS_RECEIVABLE_OVER_REVENUE_CHANGE.value],
            "<=",
            0,
        ).add(
            self._evaluate_indicator(
                self.fin_indicators[FinancialTrends.SHARES_GROWTH.value], "<=", self.THRESHOLD_MANAGEMENT_SHARES_GROWTH
            )
        )

    def _evaluate_indicator(self, indicator: pd.Series, eval_func: str, threshold: float | pd.Series) -> pd.Series:
        if eval_func == ">=":
            com_result = indicator >= threshold
        elif eval_func == "<=":
            com_result = indicator <= threshold
        else:
            raise ValueError(f"Unknown evaluation function {eval_func}. Only <= and >= allowed.")
        return com_result.fillna(False).astype(int)
