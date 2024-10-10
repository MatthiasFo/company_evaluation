resource "google_bigquery_table" "fmp_balance_sheet" {
  dataset_id          = google_bigquery_dataset.fmp_dataset.dataset_id
  table_id            = "balance_sheet"
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
    "name": "requestTimestamp",
    "type": "DATETIME",
    "mode": "REQUIRED"
  },
  {
    "name": "symbol",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "date",
    "type": "DATE",
    "mode": "NULLABLE"
  },
  {
    "name": "reportedCurrency",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "cik",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "fillingDate",
    "type": "DATE",
    "mode": "REQUIRED"
  },
  {
    "name": "acceptedDate",
    "type": "DATETIME",
    "mode": "NULLABLE"
  },
  {
    "name": "calendarYear",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "period",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "cashAndCashEquivalents",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "shortTermInvestments",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "cashAndShortTermInvestments",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "netReceivables",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "inventory",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "otherCurrentAssets",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "totalCurrentAssets",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "propertyPlantEquipmentNet",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "goodwill",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "intangibleAssets",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "goodwillAndIntangibleAssets",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "longTermInvestments",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "taxAssets",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "otherNonCurrentAssets",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "totalNonCurrentAssets",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "otherAssets",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "totalAssets",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "accountPayables",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "shortTermDebt",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "taxPayables",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "deferredRevenue",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "otherCurrentLiabilities",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "totalCurrentLiabilities",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "longTermDebt",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "deferredRevenueNonCurrent",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "deferredTaxLiabilitiesNonCurrent",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "otherNonCurrentLiabilities",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "totalNonCurrentLiabilities",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "otherLiabilities",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "capitalLeaseObligations",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "totalLiabilities",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "preferredStock",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "commonStock",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "retainedEarnings",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "accumulatedOtherComprehensiveIncomeLoss",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "othertotalStockholdersEquity",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "totalStockholdersEquity",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "totalEquity",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "totalLiabilitiesAndStockholdersEquity",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "minorityInterest",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "totalLiabilitiesAndTotalEquity",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "totalInvestments",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "totalDebt",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "netDebt",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "link",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "finalLink",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF
}
