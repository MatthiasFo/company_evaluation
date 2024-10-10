import enum
from typing import Dict, List, Any
import pandas as pd
import requests
from src.domain.scraper import ApiLimitReached, DataValidationError
from src.ports.alphavantage_port import AlphavantagePort
from src.adapters.gcp_secret_manager import GcpSecretManager


class AlphavantageReportTypes(enum.Enum):
    ANNUALLY = "annualReports"
    QUARTERLY = "quarterlyReports"


class AlphavantageFunctions(enum.Enum):
    BALANCE_SHEET = "BALANCE_SHEET"
    INCOME_STATEMENT = "INCOME_STATEMENT"
    CASH_FLOW = "CASH_FLOW"


class AlphavantageAdapter(AlphavantagePort):
    _base_url = "https://www.alphavantage.co/query"
    _gcp_secret_id = "alphavantage-api-key"
    _api_key = None

    def __init__(self):
        self._api_key = GcpSecretManager().get_secret(self._gcp_secret_id)

    def get_balance_sheet(self, ticker: str) -> Dict[str, pd.DataFrame]:
        request_data = self._make_request(AlphavantageFunctions.BALANCE_SHEET.value, ticker)
        int_columns = [
            "totalAssets",
            "totalCurrentAssets",
            "cashAndCashEquivalentsAtCarryingValue",
            "cashAndShortTermInvestments",
            "inventory",
            "currentNetReceivables",
            "totalNonCurrentAssets",
            "propertyPlantEquipment",
            "intangibleAssets",
            "intangibleAssetsExcludingGoodwill",
            "goodwill",
            "investments",
            "longTermInvestments",
            "shortTermInvestments",
            "otherCurrentAssets",
            "totalLiabilities",
            "totalCurrentLiabilities",
            "currentAccountsPayable",
            "deferredRevenue",
            "currentDebt",
            "shortTermDebt",
            "totalNonCurrentLiabilities",
            "capitalLeaseObligations",
            "longTermDebt",
            "currentLongTermDebt",
            "longTermDebtNoncurrent",
            "shortLongTermDebtTotal",
            "otherCurrentLiabilities",
            "otherNonCurrentLiabilities",
            "totalShareholderEquity",
            "treasuryStock",
            "retainedEarnings",
            "commonStock",
            "commonStockSharesOutstanding",
        ]
        return self._split_into_annual_and_quarterly_and_validate(request_data, int_columns)

    def get_cash_flow(self, ticker: str) -> Dict[str, pd.DataFrame]:
        request_data = self._make_request(AlphavantageFunctions.CASH_FLOW.value, ticker)
        int_columns = [
            "operatingCashflow",
            "paymentsForOperatingActivities",
            "changeInOperatingLiabilities",
            "changeInOperatingAssets",
            "depreciationDepletionAndAmortization",
            "capitalExpenditures",
            "changeInReceivables",
            "changeInInventory",
            "profitLoss",
            "cashflowFromInvestment",
            "cashflowFromFinancing",
            "dividendPayout",
            "dividendPayoutCommonStock",
            "proceedsFromRepaymentsOfShortTermDebt",
            "proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet",
            "proceedsFromRepurchaseOfEquity",
            "netIncome",
        ]
        return self._split_into_annual_and_quarterly_and_validate(request_data, int_columns)

    def get_income_statement(self, ticker: str) -> Dict[str, pd.DataFrame]:
        request_data = self._make_request(AlphavantageFunctions.INCOME_STATEMENT.value, ticker)
        int_columns = [
            "grossProfit",
            "totalRevenue",
            "costOfRevenue",
            "costofGoodsAndServicesSold",
            "operatingIncome",
            "sellingGeneralAndAdministrative",
            "researchAndDevelopment",
            "operatingExpenses",
            "netInterestIncome",
            "interestIncome",
            "interestExpense",
            "nonInterestIncome",
            "otherNonOperatingIncome",
            "depreciation",
            "depreciationAndAmortization",
            "incomeBeforeTax",
            "incomeTaxExpense",
            "interestAndDebtExpense",
            "netIncomeFromContinuingOperations",
            "comprehensiveIncomeNetOfTax",
            "ebit",
            "ebitda",
            "netIncome",
        ]
        return self._split_into_annual_and_quarterly_and_validate(request_data, int_columns)

    def _make_request(self, function: str, ticker: str) -> Dict[str, Any]:
        url = f"{self._base_url}?function={function}&symbol={ticker}&apikey={self._api_key}"
        print(f"alphavantage: Request to url: {url}")
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(
                f"alphavantage: Request to {url} failed with status code {response.status_code}: {response.text}"
            )

        request_data = response.json()

        if not isinstance(request_data, dict):
            raise DataValidationError(f"alphavantage: response data is not a dictionary")
        if "Information" in request_data.keys():
            raise ApiLimitReached(f"alphavantage: {request_data['Information']}")
        if "symbol" not in request_data.keys():
            raise DataValidationError(f"alphavantage: response data does not contain a symbol")
        return request_data

    def _split_into_annual_and_quarterly_and_validate(
        self, request_data: Dict[str, Any], int_columns: List[str]
    ) -> Dict[str, pd.DataFrame]:
        reports = {}
        pd.set_option("future.no_silent_downcasting", True)
        for report_type in AlphavantageReportTypes:
            if report_type.value not in request_data.keys():
                reports[report_type.value] = self._handle_data_validation_issue(
                    report_type, f"alphavantage: No {report_type.value} in response data"
                )
                continue

            report = pd.DataFrame(request_data[report_type.value])
            if report.empty:
                reports[report_type.value] = self._handle_data_validation_issue(
                    report_type, f"alphavantage: {report_type.value} is empty"
                )

            report["requestTimestamp"] = pd.Timestamp.now().strftime("%Y-%m-%d %X")
            report["report_type"] = report_type.value
            try:
                report[int_columns] = report[int_columns].replace("None", 0).round().astype(int)
                report["symbol"] = request_data["symbol"]
            except:
                reports[report_type.value] = self._handle_data_validation_issue(
                    report_type, f"alphavantage: Failed to convert {report_type.value} to int"
                )
            report = self._enhance_with_fiscal_date_ending_id(report)
            reports[report_type.value] = report
        return reports

    def _handle_data_validation_issue(self, report_type: AlphavantageReportTypes, error_message: str) -> None:
        if report_type.value == AlphavantageReportTypes.ANNUALLY.value:
            raise DataValidationError(error_message)
        print(error_message)
        return None

    def _enhance_with_fiscal_date_ending_id(self, fin_statement: pd.DataFrame) -> pd.DataFrame:
        fin_statement["id"] = (
            fin_statement["fiscalDateEnding"]
            + "_"
            + fin_statement["report_type"]
            + "_"
            + fin_statement["symbol"].apply(lambda x: x.replace(".", "_").replace(" ", "_"))
        )
        return fin_statement
