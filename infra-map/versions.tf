terraform {
  required_version = ">= 1.10" # S3 backend native locking (use_lockfile)

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.71"
    }
  }

  # Its own state key in the same state bucket as infra/, so the series' teardown never touches the map.
  # backend.hcl is git-ignored; copy backend.hcl.example.
  #   terraform init -backend-config=backend.hcl
  backend "s3" {}
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      project   = var.project
      managedby = "terraform"
      series    = "cer-reporting-agent"
    }
  }
}
