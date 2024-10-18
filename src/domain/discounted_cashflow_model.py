from typing import TypedDict
import pandas as pd
import numpy as np


class DcfConfig(TypedDict):
    discount_rate: float
    general_growth_rate: float


class GrowthForecastConfig(TypedDict):
    forecast_period: int
    general_growth_rate: float


class DCFModel:
    def __init__(self, base_data: pd.DataFrame):
        # The base data must contain the following columns:
        # ticker (index)
        # free_cash_flow,
        # revenue_growth,
        # shares_outstanding,
        self.base_data = base_data
        self.model_configs = {
            "stable": {
                "discount_rate": 0.09,
                "general_growth_rate": 0.04,
            },
            "stable_and_strong_growth": {
                "discount_rate": 0.09,
                "general_growth_rate": 0.08,
            },
            "volatile": {
                "discount_rate": 0.15,
                "general_growth_rate": 0.04,
            },
            "volatile_and_weak_growth": {
                "discount_rate": 0.15,
                "general_growth_rate": 0.02,
            },
            "normal": {
                "discount_rate": 0.105,
                "general_growth_rate": 0.04,
            },
        }

    def estimate_intrinsic_value(self) -> pd.DataFrame:
        # taken from book "five rules for successful stock investing" (kindl) page 146-147
        anual_cashflow = self.base_data["free_cash_flow"]
        revenue_growth = self.base_data["revenue_growth"]
        shares_outstanding = self.base_data["shares_outstanding"]
        for label, model_config in self.model_configs.items():
            intrinsic_company_value = self._estimate_intrinsic_value_with_discounted_cash_flow(
                revenue_growth=revenue_growth,
                free_cashflow_annually=anual_cashflow,
                config=model_config,
            )
            self.base_data = self.base_data.join(pd.DataFrame({label: intrinsic_company_value / shares_outstanding}))

        # remove all zero or negative evaluations because they are not meaningful
        proper_evaluations = self.base_data.loc[
            (self.base_data.loc[:, [x for x in self.model_configs.keys()]] > 0).any(axis=1)
        ].copy()
        return proper_evaluations

    def _generate_growth_forecast(self, revenue_growth: pd.DataFrame, config: GrowthForecastConfig) -> pd.DataFrame:
        # generate a growth rate for each stock over time
        pd.set_option("future.no_silent_downcasting", True)  # to avoid warning
        current_growth_rate = revenue_growth.fillna(config["general_growth_rate"]).astype("float64")
        df_growth_rate = pd.DataFrame(
            columns=[i for i in range(config["forecast_period"])],
            index=current_growth_rate.index,
            dtype="float64",
        )
        df_growth_rate.loc[:, 0] = current_growth_rate
        df_growth_rate.iloc[:, -1:] = config["general_growth_rate"]
        df_growth_rate.interpolate(inplace=True, axis=1)

        return df_growth_rate

    def _estimate_intrinsic_value_with_discounted_cash_flow(
        self, revenue_growth: pd.Series, free_cashflow_annually: pd.Series, config: DcfConfig
    ):
        forecase_period = 10  # years

        growth_forecast = self._generate_growth_forecast(
            revenue_growth=revenue_growth,
            config={
                "forecast_period": forecase_period,
                "general_growth_rate": config["general_growth_rate"],
            },
        )

        df_discount_rate = pd.DataFrame(
            config["discount_rate"],
            index=growth_forecast.index,
            columns=growth_forecast.columns,
        )

        df_exponent = pd.DataFrame(
            np.ones((len(growth_forecast), 1)) * np.linspace(1, forecase_period, forecase_period),
            index=growth_forecast.index,
            columns=growth_forecast.columns,
        )
        num_tickers = len(free_cashflow_annually.index)
        df_free_cash_flow = pd.DataFrame(
            free_cashflow_annually.values.reshape(num_tickers, 1) * np.ones((num_tickers, forecase_period)),
            index=free_cashflow_annually.index,
            columns=growth_forecast.columns,
        )
        df_forecast_cf = df_free_cash_flow * ((1 + growth_forecast) ** df_exponent)
        df_discounted_cf = df_forecast_cf / ((1 + df_discount_rate) ** df_exponent)

        # Calculate the terminal value
        perpetuity_value = (
            df_forecast_cf.iloc[:, -1:]
            * (1 + config["general_growth_rate"])
            / (config["discount_rate"] - config["general_growth_rate"])
        )
        discounted_perpetuity_value = perpetuity_value / (1 + config["discount_rate"]) ** forecase_period

        total_equity_value = df_discounted_cf.sum(axis=1).add(
            discounted_perpetuity_value.sum(axis=1)  # use sum just to convert shape to fit sum of discounted cashflows
        )

        return total_equity_value
