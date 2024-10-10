resource "google_bigquery_table" "alphavantage_cashflows_annually" {
  dataset_id          = google_bigquery_dataset.alphavantage_dataset.dataset_id
  table_id            = "cashflows_annually"
  project             = var.project_id
  deletion_protection = false # This table can always be re-generated from raw data
  schema              = <<EOF
[
  {
    "name": "id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "symbol",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "requestTimestamp",
    "type": "DATETIME",
    "mode": "REQUIRED"
  },
  {
    "name": "fiscalDateEnding",
    "type": "DATE",
    "mode": "NULLABLE"
  },
  {
    "name": "reportedCurrency",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "operatingCashflow",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "paymentsForOperatingActivities",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "proceedsFromOperatingActivities",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "changeInOperatingLiabilities",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "changeInOperatingAssets",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "depreciationDepletionAndAmortization",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "capitalExpenditures",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "changeInReceivables",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "changeInInventory",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "profitLoss",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "cashflowFromInvestment",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "cashflowFromFinancing",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "proceedsFromRepaymentsOfShortTermDebt",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "paymentsForRepurchaseOfCommonStock",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "paymentsForRepurchaseOfEquity",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "paymentsForRepurchaseOfPreferredStock",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "dividendPayout",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "dividendPayoutCommonStock",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "dividendPayoutPreferredStock",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "proceedsFromIssuanceOfCommonStock",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "proceedsFromIssuanceOfPreferredStock",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "proceedsFromRepurchaseOfEquity",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "proceedsFromSaleOfTreasuryStock",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "changeInCashAndCashEquivalents",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "changeInExchangeRate",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "netIncome",
    "type": "INTEGER",
    "mode": "NULLABLE"
  }
]
EOF
}
