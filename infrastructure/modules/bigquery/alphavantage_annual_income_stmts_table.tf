resource "google_bigquery_table" "alphavantage_income_stmts_annually" {
  dataset_id          = google_bigquery_dataset.alphavantage_dataset.dataset_id
  table_id            = "income_stmts_annually"
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
    "name": "grossProfit",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "totalRevenue",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "costOfRevenue",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "costofGoodsAndServicesSold",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "operatingIncome",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "sellingGeneralAndAdministrative",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "researchAndDevelopment",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "operatingExpenses",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "investmentIncomeNet",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "netInterestIncome",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "interestIncome",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "interestExpense",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "nonInterestIncome",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "otherNonOperatingIncome",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "depreciation",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "depreciationAndAmortization",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "incomeBeforeTax",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "incomeTaxExpense",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "interestAndDebtExpense",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "netIncomeFromContinuingOperations",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "comprehensiveIncomeNetOfTax",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "ebit",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "ebitda",
    "type": "INTEGER",
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
