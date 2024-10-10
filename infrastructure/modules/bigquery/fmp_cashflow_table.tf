resource "google_bigquery_table" "fmp_cashflow" {
  dataset_id          = google_bigquery_dataset.fmp_dataset.dataset_id
  table_id            = "cashflow"
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
    "name": "netIncome",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "depreciationAndAmortization",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "deferredIncomeTax",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "stockBasedCompensation",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "changeInWorkingCapital",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "accountsReceivables",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "inventory",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "accountsPayables",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "otherWorkingCapital",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "otherNonCashItems",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "netCashProvidedByOperatingActivities",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "investmentsInPropertyPlantAndEquipment",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "acquisitionsNet",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "purchasesOfInvestments",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "salesMaturitiesOfInvestments",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "otherInvestingActivites",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "netCashUsedForInvestingActivites",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "debtRepayment",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "commonStockIssued",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "commonStockRepurchased",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "dividendsPaid",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "otherFinancingActivites",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "netCashUsedProvidedByFinancingActivities",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "effectOfForexChangesOnCash",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "netChangeInCash",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "cashAtEndOfPeriod",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "cashAtBeginningOfPeriod",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "operatingCashFlow",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "capitalExpenditure",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "freeCashFlow",
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
