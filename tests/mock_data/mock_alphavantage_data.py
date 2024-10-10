import json

with open("tests/mock_data/alphavantage_cash_flow.json") as file:
    alphavantage_cashflow_json = json.load(file)

with open("tests/mock_data/alphavantage_income_statement.json") as file:
    alphavantage_income_json = json.load(file)

with open("tests/mock_data/alphavantage_balance_sheet.json") as file:
    alphavantage_balance_sheet_json = json.load(file)
