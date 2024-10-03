terraform {
  backend "s3" {
    bucket = "do-terraform-2"
    key    = "backends/vpc-clusters/do-vpc-cluster-1/backend.tfstate"
    region = "us-east-2"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.30"
    }
  }
}

