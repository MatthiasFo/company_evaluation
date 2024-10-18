resource "google_bigquery_table" "discounted_cashflow_model" {
  dataset_id          = google_bigquery_dataset.dcf_model_dataset.dataset_id
  table_id            = "dcf_model_evaluations"
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
        "name": "ticker",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "name": "shares_outstanding",
        "type": "INTEGER",
        "mode": "REQUIRED"
    },
    {
        "name": "revenue_growth",
        "type": "FLOAT",
        "mode": "REQUIRED"
    },
    {
        "name": "free_cash_flow",
        "type": "FLOAT",
        "mode": "REQUIRED"
    },
    {
        "name": "normal",
        "type": "FLOAT",
        "mode": "REQUIRED"
    },
    {
        "name": "stable",
        "type": "FLOAT",
        "mode": "REQUIRED"
    },
    {
        "name": "stable_and_strong_growth",
        "type": "FLOAT",
        "mode": "REQUIRED"
    },
    {
        "name": "volatile",
        "type": "FLOAT",
        "mode": "REQUIRED"
    },
    {
        "name": "volatile_and_weak_growth",
        "type": "FLOAT",
        "mode": "REQUIRED"
    }
]
EOF
}