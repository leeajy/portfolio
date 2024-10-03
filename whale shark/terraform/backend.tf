terraform {
  backend "s3" {
    bucket = "do-terraform-2"
    key    = "backends/applications/whale-shark/backend.tfstate"
    region = "us-east-2"
  }
}
