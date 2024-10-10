resource "google_bigquery_table" "fmp_income_stmt" {
  dataset_id          = google_bigquery_dataset.fmp_dataset.dataset_id
  table_id            = "income_stmt"
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
    "name": "revenue",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "costOfRevenue",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "grossProfit",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "grossProfitRatio",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "researchAndDevelopmentExpenses",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "generalAndAdministrativeExpenses",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "sellingAndMarketingExpenses",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "sellingGeneralAndAdministrativeExpenses",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "otherExpenses",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "operatingExpenses",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "costAndExpenses",
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
    "name": "depreciationAndAmortization",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "ebitda",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "ebitdaratio",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "operatingIncome",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "operatingIncomeRatio",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "totalOtherIncomeExpensesNet",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "incomeBeforeTax",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "incomeBeforeTaxRatio",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "incomeTaxExpense",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "netIncome",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "netIncomeRatio",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "eps",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "epsdiluted",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "weightedAverageShsOut",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "weightedAverageShsOutDil",
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
