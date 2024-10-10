resource "google_bigquery_table" "fmp_quote" {
  dataset_id          = google_bigquery_dataset.fmp_dataset.dataset_id
  table_id            = "quote"
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
    "name": "name",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "price",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "changesPercentage",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "change",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "dayLow",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "dayHigh",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "yearHigh",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "yearLow",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "marketCap",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "priceAvg50",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "priceAvg200",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "exchange",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "volume",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "avgVolume",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "open",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "previousClose",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "eps",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "pe",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "earningsAnnouncement",
    "type": "DATETIME",
    "mode": "NULLABLE"
  },
  {
    "name": "sharesOutstanding",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "timestamp",
    "type": "INTEGER",
    "mode": "NULLABLE"
  }
]
EOF
}
