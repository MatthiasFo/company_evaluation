import pandas as pd
import json

# Define the file paths for Yahoo data
yahoo_data_files = {
    "aapl": {
        "cashflow": "tests/mock_data/yahoo_aapl_cashflow.json",
        "balance_sheet": "tests/mock_data/yahoo_aapl_balance_sheet.json",
        "info": "tests/mock_data/yahoo_aapl_info.json",
        "income_stmt": "tests/mock_data/yahoo_aapl_income_stmt.json",
    },
    "sie": {
        "cashflow": "tests/mock_data/yahoo_sie_cashflow.json",
        "balance_sheet": "tests/mock_data/yahoo_sie_balance_sheet.json",
        "info": "tests/mock_data/yahoo_sie_info.json",
        "income_stmt": "tests/mock_data/yahoo_sie_income_stmt.json",
    },
}


# company info is a dictionary
with open(yahoo_data_files["aapl"]["info"]) as file:
    mock_yahoo_aapl_info = json.load(file)
with open(yahoo_data_files["sie"]["info"]) as file:
    mock_yahoo_sie_info = json.load(file)

# financial statements are dataframes with their end of period as columns and the data as rows
mock_yahoo_aapl_cashflow = pd.read_json(yahoo_data_files["aapl"]["cashflow"])
mock_yahoo_aapl_balance_sheet = pd.read_json(yahoo_data_files["aapl"]["balance_sheet"])
mock_yahoo_aapl_income_stmt = pd.read_json(yahoo_data_files["aapl"]["income_stmt"])

mock_yahoo_sie_cashflow = pd.read_json(yahoo_data_files["sie"]["cashflow"])
mock_yahoo_sie_balance_sheet = pd.read_json(yahoo_data_files["sie"]["balance_sheet"])
mock_yahoo_sie_income_stmt = pd.read_json(yahoo_data_files["sie"]["income_stmt"])
