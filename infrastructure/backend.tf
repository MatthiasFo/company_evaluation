terraform {
  backend "gcs" {
    bucket = "put-your-terraform-state-bucket-here"
    prefix = "terraform/state"
  }
}
