resource "google_bigquery_dataset" "yahoo_finance_dataset" {
  dataset_id = "yahoo_finance"
  project    = var.project_id
  location   = var.region
}

resource "google_bigquery_dataset" "curated_dataset" {
  dataset_id = "curated_data"
  project    = var.project_id
  location   = var.region
}

resource "google_bigquery_dataset" "fmp_dataset" {
  dataset_id = "financial_modeling_prep"
  project    = var.project_id
  location   = var.region
}

resource "google_bigquery_dataset" "alphavantage_dataset" {
  dataset_id = "alphavantage"
  project    = var.project_id
  location   = var.region
}


resource "google_service_account" "dbt_runner" {
  account_id   = "dbt-runner"
  display_name = "DBT Runner Service Account"
}

resource "google_project_iam_member" "dbt_runner_bigquery_admin" {
  project = var.project_id
  role    = "roles/bigquery.admin"
  member  = "serviceAccount:${google_service_account.dbt_runner.email}"
}

resource "google_service_account_iam_binding" "impersonate_binding" {
  service_account_id = google_service_account.dbt_runner.id
  role               = "roles/iam.serviceAccountTokenCreator"

  members = [
    "serviceAccount:746482649780-compute@developer.gserviceaccount.com"
  ]
}
