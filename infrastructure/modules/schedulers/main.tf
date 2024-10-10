resource "google_service_account" "scheduer_service_account" {
  project      = var.project_id
  account_id   = "scheduler-sa"
  description  = "Cloud Scheduler service account; used to trigger scheduled Cloud Run jobs."
  display_name = "scheduler-sa"
}

resource "google_cloud_run_service_iam_member" "scheduler_cloudrun_invoker" {
  project  = var.project_id
  location = var.region
  service  = "stock-eval-service"
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.scheduer_service_account.email}"
}

resource "google_project_service" "cloudscheduler" {
  project = var.project_id
  service = "cloudscheduler.googleapis.com"
}

resource "google_cloud_scheduler_job" "yahoo_scheduler" {
  project     = var.project_id
  region      = var.region
  name        = "fetch-new-stocks-from-yahoo"
  description = "Scheduler to fetch data from yahoo finance"

  schedule  = "*/15 * * * *"
  time_zone = "UTC"

  attempt_deadline = "840s"

  http_target {
    uri         = "${local.cloudrun_url}/fetch-new-yahoo-data"
    http_method = "GET"
    oidc_token {
      service_account_email = google_service_account.scheduer_service_account.email
    }
  }
}

resource "google_cloud_scheduler_job" "fmp_scheduler" {
  project     = var.project_id
  region      = var.region
  name        = "fetch-new-stocks-from-fmp"
  description = "Scheduler to fetch data from FMP"

  schedule  = "0 8 * * *"
  time_zone = "UTC"

  attempt_deadline = "900s"

  http_target {
    uri         = "${local.cloudrun_url}/fetch-new-fmp-data"
    http_method = "GET"
    oidc_token {
      service_account_email = google_service_account.scheduer_service_account.email
    }
  }
}

resource "google_cloud_scheduler_job" "alphavantage_scheduler" {
  project     = var.project_id
  region      = var.region
  name        = "fetch-new-stocks-from-alphavantage"
  description = "Scheduler to fetch data from Alphavantage"

  schedule  = "0 10 * * *"
  time_zone = "UTC"

  attempt_deadline = "900s"

  http_target {
    uri         = "${local.cloudrun_url}/fetch-new-alphavantage-data"
    http_method = "GET"
    oidc_token {
      service_account_email = google_service_account.scheduer_service_account.email
    }
  }
}


