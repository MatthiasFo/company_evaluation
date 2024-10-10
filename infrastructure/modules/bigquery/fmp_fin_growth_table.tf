resource "google_bigquery_table" "fmp_fin_growth" {
  dataset_id          = google_bigquery_dataset.fmp_dataset.dataset_id
  table_id            = "financial_growth"
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
    "name": "revenueGrowth",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "grossProfitGrowth",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "ebitgrowth",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "operatingIncomeGrowth",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "netIncomeGrowth",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "epsgrowth",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "epsdilutedGrowth",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "weightedAverageSharesGrowth",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "weightedAverageSharesDilutedGrowth",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "dividendsperShareGrowth",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "operatingCashFlowGrowth",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "freeCashFlowGrowth",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "tenYRevenueGrowthPerShare",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "fiveYRevenueGrowthPerShare",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "threeYRevenueGrowthPerShare",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "tenYOperatingCFGrowthPerShare",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "fiveYOperatingCFGrowthPerShare",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "threeYOperatingCFGrowthPerShare",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "tenYNetIncomeGrowthPerShare",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "fiveYNetIncomeGrowthPerShare",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "threeYNetIncomeGrowthPerShare",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "tenYShareholdersEquityGrowthPerShare",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "fiveYShareholdersEquityGrowthPerShare",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "threeYShareholdersEquityGrowthPerShare",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "tenYDividendperShareGrowthPerShare",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "fiveYDividendperShareGrowthPerShare",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "threeYDividendperShareGrowthPerShare",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "receivablesGrowth",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "inventoryGrowth",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "assetGrowth",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "bookValueperShareGrowth",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "debtGrowth",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "rdexpenseGrowth",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "sgaexpensesGrowth",
    "type": "FLOAT",
    "mode": "NULLABLE"
  }
]
EOF
}
