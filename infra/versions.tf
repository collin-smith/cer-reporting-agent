terraform {
  required_version = ">= 1.10" # S3 backend native locking (use_lockfile)

  required_providers {
    aws = {
      source = "hashicorp/aws"
      # 6.x carries the newer resources this series needs: aws_bedrockagentcore_* (Runtime, Gateway, Memory),
      # aws_s3vectors_*, S3_VECTORS storage on aws_bedrockagent_knowledge_base, and PROMPT_ATTACK filters on
      # aws_bedrock_guardrail. Checked against the provider docs on 2026-10-29 (latest release 6.71.0).
      version = "~> 6.71"
    }
  }

  # Remote state in S3, so `terraform destroy` never loses track of what it created. Partial config: the bucket
  # name is account-specific and lives in backend.hcl (git-ignored; copy backend.hcl.example). The bucket is
  # created once by hand, outside this stack, so `destroy` can't delete the state it depends on.
  #   terraform init -backend-config=backend.hcl
  # CI runs `terraform init -backend=false`, so it never touches this.
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

# The report-writing models for the synthetic test set (Llama, Mistral) run only in US regions. Synthetic data with
# fictional operators only; the system under test stays in ca-central-1 (D27).
provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"

  default_tags {
    tags = {
      project   = var.project
      managedby = "terraform"
      series    = "cer-reporting-agent"
    }
  }
}
