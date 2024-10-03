terraform {
  backend "s3" {
    bucket = "do-terraform-2"
    key    = "backends/applications/stock-ml/backend.tfstate"
    region = "us-east-2"
  }
}
