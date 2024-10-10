module "bigquery" {
  source     = "./modules/bigquery"
  project_id = local.project_id
  region     = local.region
}

module "deployment_setup" {
  source     = "./modules/deployment_setup"
  project_id = local.project_id
  region     = local.region
}

module "schedulers" {
  source     = "./modules/schedulers"
  project_id = local.project_id
  region     = local.region
}
