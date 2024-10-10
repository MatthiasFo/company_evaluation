resource "google_project_service" "secret_manager" {
  project = local.project_id
  service = "secretmanager.googleapis.com"
}

resource "google_secret_manager_secret" "fmp_api_key" {
  secret_id = "fmp-api-key"

  replication {
    user_managed {
      replicas {
        location = "europe-west3"
      }
    }
  }
}

resource "google_secret_manager_secret_iam_member" "cloudrun_access_fmp_key" {
  secret_id = google_secret_manager_secret.fmp_api_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${local.default_compute_service_account}"
}

resource "google_secret_manager_secret" "alphavantage_api_key" {
  secret_id = "alphavantage-api-key"

  replication {
    user_managed {
      replicas {
        location = "europe-west3"
      }
    }
  }
}

resource "google_secret_manager_secret_iam_member" "cloudrun_access_alphavantage_key" {
  secret_id = google_secret_manager_secret.alphavantage_api_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${local.default_compute_service_account}"
}