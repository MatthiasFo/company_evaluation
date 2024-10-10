import pandas as pd
import json

# Read the JSON file
with open("tests/mock_data/fmp_balance_sheet.json") as file:
    fmp_balance_sheet_json = json.load(file)

# Read the JSON files
with open("tests/mock_data/fmp_cashflow_stmt.json") as file:
    fmp_cashflow_json = json.load(file)

with open("tests/mock_data/fmp_financial_growth.json") as file:
    fmp_growth_json = json.load(file)

with open("tests/mock_data/fmp_income_stmt.json") as file:
    fmp_income_json = json.load(file)

with open("tests/mock_data/fmp_quote.json") as file:
    fmp_quote_json = json.load(file)

with open("tests/mock_data/fmp_profile.json") as file:
    fmp_profile_json = json.load(file)
