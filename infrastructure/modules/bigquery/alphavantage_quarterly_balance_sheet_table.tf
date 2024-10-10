resource "google_bigquery_table" "alphavantage_balance_sheets_quarterly" {
  dataset_id          = google_bigquery_dataset.alphavantage_dataset.dataset_id
  table_id            = "balance_sheets_quarterly"
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
    "name": "totalAssets",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "totalCurrentAssets",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "cashAndCashEquivalentsAtCarryingValue",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "cashAndShortTermInvestments",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "inventory",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "currentNetReceivables",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "totalNonCurrentAssets",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "propertyPlantEquipment",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "accumulatedDepreciationAmortizationPPE",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "intangibleAssets",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "intangibleAssetsExcludingGoodwill",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "goodwill",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "investments",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "longTermInvestments",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "shortTermInvestments",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "otherCurrentAssets",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "otherNonCurrentAssets",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "totalLiabilities",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "totalCurrentLiabilities",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "currentAccountsPayable",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "deferredRevenue",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "currentDebt",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "shortTermDebt",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "totalNonCurrentLiabilities",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "capitalLeaseObligations",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "longTermDebt",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "currentLongTermDebt",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "longTermDebtNoncurrent",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "shortLongTermDebtTotal",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "otherCurrentLiabilities",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "otherNonCurrentLiabilities",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "totalShareholderEquity",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "treasuryStock",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "retainedEarnings",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "commonStock",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "commonStockSharesOutstanding",
    "type": "INTEGER",
    "mode": "NULLABLE"
  }
]
EOF
}
