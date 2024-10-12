import pandas as pd
from src.domain.calculate_financial_ratios import (
    FinancialRatios,
    calculate_financial_ratios,
)
from src.domain.calculate_trends_over_time import FinancialTrends, calculate_trends_over_time
from src.domain.discounted_cashflow_model import DCFModel
from src.domain.evaluate_guidelines import GuidelinesEvaluator


class FinancialEvaluator:
    def __init__(self, fin_stmts: pd.DataFrame):
        """Initialize the FinancialEvaluator with financial statements."""
        self._fin_stmts = fin_stmts
        self._evaluated_data = pd.DataFrame()
        self._intrinsic_value = pd.DataFrame()

    def get_ratios_and_trends(self) -> pd.DataFrame:
        if len(self._evaluated_data) == 0:
            self._evaluate_time_series()
        return self._evaluated_data

    def get_current_evaluation(self) -> pd.DataFrame:
        if len(self._intrinsic_value) == 0:
            self._run_discounted_cashflow_model()

        if len(self._evaluated_data) == 0:
            self._evaluate_time_series()

        return self._merge_ratios_trends_and_dcf_results()

    def _evaluate_time_series(self):
        self._evaluated_data = self._calculate_trends_and_ratios()
        self._add_competition_averages()
        self._add_guideline_scores()

    def _calculate_trends_and_ratios(self) -> pd.DataFrame:
        """Evaluate the financial statements and return the enriched DataFrame."""
        ratios = calculate_financial_ratios(self._fin_stmts)

        trends = calculate_trends_over_time(
            ratios=ratios,
            shares_growth=self._fin_stmts[["id", "ticker", "end_of_period", "shares_growth"]],
        )
        return self._merge_ratios_with_trends(ratios, trends)

    def _run_discounted_cashflow_model(self):
        mean_over_period = (
            self._fin_stmts.loc[:, ["ticker", "free_cash_flow", "revenue_growth"]].groupby("ticker").mean()
        )
        base_data = self._fin_stmts.loc[:, ["ticker", "shares_outstanding", "current_price"]].groupby("ticker").max()

        dcf_model = DCFModel(base_data.merge(mean_over_period, left_index=True, right_index=True))
        self._intrinsic_value = dcf_model.estimate_intrinsic_value()

    def _merge_ratios_trends_and_dcf_results(self) -> pd.DataFrame:
        list_of_numeric_columns = (
            [ratio.value for ratio in FinancialRatios]
            + [trend.value for trend in FinancialTrends]
            + ["guideline_score"]
        )
        agg_ratios_for_ticker = self._evaluated_data[list_of_numeric_columns + ["ticker"]].groupby("ticker").mean()

        columns_to_use = self._intrinsic_value.columns.difference(agg_ratios_for_ticker.columns)
        ratios_trends_dcf = agg_ratios_for_ticker.merge(self._intrinsic_value[columns_to_use], on="ticker")

        agg_ratios_for_competitors = (
            self._evaluated_data[list_of_numeric_columns + ["sector", "country"]].groupby(["sector", "country"]).mean()
        )

        ratios_trends_dcf_sector = ratios_trends_dcf.merge(
            self._fin_stmts.loc[:, ["id", "ticker", "sector", "country", "company_name", "industry"]], on="ticker"
        )

        ratios_trends_dcf_competition = ratios_trends_dcf_sector.merge(
            agg_ratios_for_competitors,
            on=["sector", "country"],
            how="left",
            suffixes=("", "_competition"),
        )
        return ratios_trends_dcf_competition

    def _merge_ratios_with_trends(self, ratios: pd.DataFrame, trends: pd.DataFrame) -> pd.DataFrame:
        """Merge the calculated ratios and trends into the original DataFrame."""
        merge_on_columns = ["ticker", "end_of_period"]
        ratios.set_index(merge_on_columns, inplace=True)
        trends.set_index(merge_on_columns, inplace=True)

        ratio_columns_to_use = ratios.columns.difference(self._fin_stmts.columns).to_list()
        trend_columns_to_use = trends.columns.difference(self._fin_stmts.columns).to_list()
        ratios_and_stmts = self._fin_stmts.set_index(merge_on_columns).merge(
            ratios.loc[:, ratio_columns_to_use],
            left_index=True,
            right_index=True,
            how="left",
        )
        ratios_and_stmts_and_trends = ratios_and_stmts.merge(
            trends.loc[:, trend_columns_to_use],
            left_index=True,
            right_index=True,
            how="left",
        )
        return ratios_and_stmts_and_trends.reset_index(merge_on_columns, inplace=False)

    def _add_competition_averages(self) -> None:
        sector_averages = (
            self._evaluated_data[
                [ratio.value for ratio in FinancialRatios]
                + [trend.value for trend in FinancialTrends]
                + ["sector", "country", "end_of_period"]
            ]
            .groupby(["sector", "country", "end_of_period"])
            .mean()
        )

        self._evaluated_data = self._evaluated_data.merge(
            sector_averages,
            on=["sector", "country", "end_of_period"],
            how="left",
            suffixes=("", "_competition"),
        )

    def _add_guideline_scores(self) -> None:
        """Add guideline scores to the evaluated data."""
        guidelines_evaluator = GuidelinesEvaluator(self._evaluated_data)
        self._evaluated_data["guideline_score"] = guidelines_evaluator.evaluate_guidelines()
