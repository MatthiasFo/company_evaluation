resource "google_bigquery_table" "fmp_profile" {
  dataset_id          = google_bigquery_dataset.fmp_dataset.dataset_id
  table_id            = "profile"
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
    "name": "price",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "beta",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "volAvg",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "mktCap",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "lastDiv",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "range",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "changes",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "companyName",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "currency",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "cik",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "isin",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "cusip",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "exchange",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "exchangeShortName",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "industry",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "website",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "description",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "ceo",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "sector",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "country",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "fullTimeEmployees",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "phone",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "address",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "city",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "state",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "zip",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "dcfDiff",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "dcf",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "image",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "defaultImage",
    "type": "BOOLEAN",
    "mode": "NULLABLE"
  },
  {
    "name": "isEtf",
    "type": "BOOLEAN",
    "mode": "NULLABLE"
  },
  {
    "name": "isActivelyTrading",
    "type": "BOOLEAN",
    "mode": "NULLABLE"
  },
  {
    "name": "isAdr",
    "type": "BOOLEAN",
    "mode": "NULLABLE"
  },
  {
    "name": "isFund",
    "type": "BOOLEAN",
    "mode": "NULLABLE"
  }
]
EOF
}
