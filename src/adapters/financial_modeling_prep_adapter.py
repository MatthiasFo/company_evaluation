import enum
from typing import Dict
import pandas as pd
import requests
from src.domain.scraper import ApiLimitReached, DataValidationError
from src.ports.financial_modeling_prep_port import FinancialModelingPrepPort
from src.adapters.gcp_secret_manager import GcpSecretManager


class FmpEndpoints(enum.Enum):
    PROFILE = "profile"
    QUOTE = "quote"
    FINANCIAL_GROWTH = "financial-growth"
    BALANCE_SHEET = "balance-sheet-statement"
    INCOME_STATEMENT = "income-statement"
    CASH_FLOW = "cash-flow-statement"


class FinancialModelingPrepAdapter(FinancialModelingPrepPort):
    _base_url = "https://financialmodelingprep.com/api/v3"
    _gcp_secret_id = "fmp-api-key"
    _api_key = None
    _default_period = "annual"

    def __init__(self):
        self._api_key = GcpSecretManager().get_secret(self._gcp_secret_id)

    def get_profile_info(self, ticker: str) -> pd.DataFrame:
        request_data = self._make_request_to_fmp(FmpEndpoints.PROFILE.value, ticker)
        profile_data = self._enhance_with_id(request_data)

        mandatory_columns = ["symbol", "companyName", "industry", "country", "sector"]
        if not set(mandatory_columns).issubset(profile_data.columns):
            raise DataValidationError(f"FMP: Mandatory profile column missing for {ticker}")
        if (
            profile_data[mandatory_columns].isnull().any().any()
            or (profile_data[mandatory_columns] == "null").any().any()
        ):
            raise DataValidationError(f"FMP: Data in mandatory profile column missing for {ticker}")
        return profile_data

    def get_quote(self, ticker: str) -> pd.DataFrame:
        request_data = self._make_request_to_fmp(FmpEndpoints.QUOTE.value, ticker)
        quote_data = self._enhance_with_id(request_data)

        try:
            quote_data["earningsAnnouncement"] = pd.to_datetime(quote_data["earningsAnnouncement"])
        except:
            quote_data["earningsAnnouncement"] = None
        return quote_data

    def get_financial_growth(self, ticker: str) -> pd.DataFrame:
        request_data = self._make_request_to_fmp(
            FmpEndpoints.FINANCIAL_GROWTH.value, ticker, period=self._default_period
        )
        return self._enhance_with_id(request_data)

    def get_balance_sheet(self, ticker: str) -> pd.DataFrame:
        request_data = self._make_request_to_fmp(FmpEndpoints.BALANCE_SHEET.value, ticker, period=self._default_period)
        balance_sheet = self._enhance_with_id(request_data)

        int_columns = [
            "cashAndCashEquivalents",
            "shortTermInvestments",
            "cashAndShortTermInvestments",
            "netReceivables",
            "inventory",
            "otherCurrentAssets",
            "totalCurrentAssets",
            "propertyPlantEquipmentNet",
            "goodwill",
            "intangibleAssets",
            "goodwillAndIntangibleAssets",
            "longTermInvestments",
            "taxAssets",
            "otherNonCurrentAssets",
            "totalNonCurrentAssets",
            "otherAssets",
            "totalAssets",
            "accountPayables",
            "shortTermDebt",
            "taxPayables",
            "deferredRevenue",
            "otherCurrentLiabilities",
            "totalCurrentLiabilities",
            "longTermDebt",
            "deferredRevenueNonCurrent",
            "deferredTaxLiabilitiesNonCurrent",
            "otherNonCurrentLiabilities",
            "totalNonCurrentLiabilities",
            "otherLiabilities",
            "capitalLeaseObligations",
            "totalLiabilities",
            "preferredStock",
            "commonStock",
            "retainedEarnings",
            "accumulatedOtherComprehensiveIncomeLoss",
            "othertotalStockholdersEquity",
            "totalStockholdersEquity",
            "totalEquity",
            "totalLiabilitiesAndStockholdersEquity",
            "minorityInterest",
            "totalLiabilitiesAndTotalEquity",
            "totalInvestments",
            "totalDebt",
            "netDebt",
        ]
        try:
            balance_sheet[int_columns] = balance_sheet[int_columns].round().astype(int)
        except:
            raise DataValidationError(f"FMP: Data validation failed on balance sheets for {ticker}")
        return balance_sheet

    def get_cash_flow(self, ticker: str) -> pd.DataFrame:
        request_data = self._make_request_to_fmp(FmpEndpoints.CASH_FLOW.value, ticker, period=self._default_period)
        cashflow_stmts = self._enhance_with_id(request_data)

        int_columns = [
            "netIncome",
            "depreciationAndAmortization",
            "deferredIncomeTax",
            "stockBasedCompensation",
            "changeInWorkingCapital",
            "accountsReceivables",
            "inventory",
            "accountsPayables",
            "otherWorkingCapital",
            "otherNonCashItems",
            "netCashProvidedByOperatingActivities",
            "investmentsInPropertyPlantAndEquipment",
            "acquisitionsNet",
            "purchasesOfInvestments",
            "salesMaturitiesOfInvestments",
            "otherInvestingActivites",
            "netCashUsedForInvestingActivites",
            "debtRepayment",
            "commonStockIssued",
            "commonStockRepurchased",
            "dividendsPaid",
            "otherFinancingActivites",
            "netCashUsedProvidedByFinancingActivities",
            "effectOfForexChangesOnCash",
            "netChangeInCash",
            "cashAtEndOfPeriod",
            "cashAtBeginningOfPeriod",
            "operatingCashFlow",
            "capitalExpenditure",
            "freeCashFlow",
        ]
        try:
            cashflow_stmts[int_columns] = cashflow_stmts[int_columns].round().astype(int)
        except:
            raise DataValidationError(f"FMP: Data validation failed on cashflow statements for {ticker}")
        return cashflow_stmts

    def get_income_statement(self, ticker: str) -> pd.DataFrame:
        request_data = self._make_request_to_fmp(
            FmpEndpoints.INCOME_STATEMENT.value, ticker, period=self._default_period
        )
        income_stmts = self._enhance_with_id(request_data)

        int_columns = [
            "revenue",
            "costOfRevenue",
            "grossProfit",
            "researchAndDevelopmentExpenses",
            "generalAndAdministrativeExpenses",
            "sellingAndMarketingExpenses",
            "sellingGeneralAndAdministrativeExpenses",
            "otherExpenses",
            "operatingExpenses",
            "costAndExpenses",
            "interestIncome",
            "interestExpense",
            "depreciationAndAmortization",
            "ebitda",
            "operatingIncome",
            "totalOtherIncomeExpensesNet",
            "incomeBeforeTax",
            "incomeTaxExpense",
            "netIncome",
            "weightedAverageShsOut",
            "weightedAverageShsOutDil",
        ]
        float_columns = [
            "grossProfitRatio",
            "ebitdaratio",
            "operatingIncomeRatio",
            "incomeBeforeTaxRatio",
            "netIncomeRatio",
            "eps",
            "epsdiluted",
        ]
        try:
            income_stmts[int_columns] = income_stmts[int_columns].round().astype(int)
            income_stmts[float_columns] = income_stmts[float_columns].astype(float)
        except:
            raise DataValidationError(f"FMP: Data validation failed on income statements for {ticker}")
        return income_stmts

    def _make_request_to_fmp(self, request_data: str, ticker: str, period=None):
        url = f"{self._base_url}/{request_data}/{ticker}?apikey={self._api_key}"
        if period:
            url += f"&period={period}"

        print(f"Request to url: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        if response.status_code == 429:
            raise ApiLimitReached("FMP: API limit reached")
        else:
            raise Exception(f"FMP: Request to {url} failed with status code {response.status_code}: {response.text}")

    def _enhance_with_id(self, request_data: Dict) -> pd.DataFrame:
        fin_statement = pd.DataFrame(request_data)
        if fin_statement.empty:
            raise DataValidationError("FMP: Request data is empty.")

        fin_statement["requestTimestamp"] = pd.Timestamp.now().strftime("%Y-%m-%d %X")
        if "period" in fin_statement.columns and "calendarYear" in fin_statement.columns:
            fin_statement = self._enhance_with_calendar_year_id(fin_statement)
        else:
            fin_statement = self._enhance_with_request_timestamp_id(fin_statement)
        return fin_statement

    def _enhance_with_calendar_year_id(self, fin_statement: pd.DataFrame) -> pd.DataFrame:
        fin_statement["id"] = (
            fin_statement["calendarYear"]
            + "_"
            + fin_statement["period"]
            + "_"
            + fin_statement["symbol"].apply(lambda x: self._remove_dots_and_spaces(x))
        )
        return fin_statement

    def _enhance_with_request_timestamp_id(self, company_info: pd.DataFrame) -> pd.DataFrame:
        company_info["id"] = (
            pd.Timestamp.now().strftime("%Y-%m-%d")
            + "_"
            + self._remove_dots_and_spaces(company_info["symbol"].values[0])
        )
        return company_info

    def _remove_dots_and_spaces(self, string: str) -> str:
        return string.replace(".", "_").replace(" ", "_")
