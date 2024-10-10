import pandas as pd
import json

# Read the JSON file
with open("tests/mock_data/bq_combined_filings.json") as file:
    bq_combined_filings_json = json.load(file)

# Read the JSON files
with open("tests/mock_data/bq_company_infos.json") as file:
    bq_company_infos_json = json.load(file)

mock_bq_combined_filings = pd.DataFrame(bq_combined_filings_json)
mock_bq_company_infos = pd.DataFrame(bq_company_infos_json)
