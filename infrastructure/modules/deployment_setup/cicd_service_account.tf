resource "google_service_account" "cicd_service_account" {
  account_id   = "cicd-service-account"
  display_name = "CI/CD Service Account"
}

resource "google_project_iam_member" "cicd_service_account_account_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${google_service_account.cicd_service_account.email}"
}

resource "google_project_iam_member" "cicd_service_account_cloud_run" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${google_service_account.cicd_service_account.email}"
}

resource "google_project_iam_binding" "cicd_service_account_artifact_registry" {
  project = var.project_id
  role    = "roles/artifactregistry.repoAdmin"
  members = [
    "serviceAccount:${google_service_account.cicd_service_account.email}"
  ]
}