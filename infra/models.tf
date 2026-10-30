# Application inference profiles: tagged copies of Bedrock's system profiles. Model calls made through a profile ARN
# carry the profile's tags (project=agentic-ai, via default_tags), so Bedrock spend shows up in the tag-filtered
# budgets and in Cost Explorer. Calls made to a bare model ID are untagged and only show in the account-wide view.
# Creating a profile is free; it bills only per call, at the model's normal rate.
#
# Nova Lite has a Canada-only system profile (ca.*, routes to ca-central-1 + ca-west-1). Claude profiles are added
# once Anthropic model access is enabled for the account (brief §8 #2).

# Descriptions allow only letters, digits, ":" and "." with single spaces, "_" or "-" between them (no commas).
resource "aws_bedrock_inference_profile" "nova_lite" {
  name        = "${local.name}-nova-lite"
  description = "Nova Lite via the Canada system profile tagged for project cost tracking"

  model_source {
    copy_from = "arn:aws:bedrock:${var.region}:${local.account_id}:inference-profile/ca.amazon.nova-lite-v1:0"
  }
}

# Test-set report writers (D27): two model families other than the ones under test (Nova, Claude), about half the
# reports each. Llama 4 Maverick via its US cross-region profile; Mistral Large 3 on-demand in us-east-1.
resource "aws_bedrock_inference_profile" "writer_llama" {
  provider    = aws.us_east_1
  name        = "${local.name}-writer-llama4-maverick"
  description = "Llama 4 Maverick for writing synthetic field reports"

  model_source {
    copy_from = "arn:aws:bedrock:us-east-1:${local.account_id}:inference-profile/us.meta.llama4-maverick-17b-instruct-v1:0"
  }
}

resource "aws_bedrock_inference_profile" "writer_mistral" {
  provider    = aws.us_east_1
  name        = "${local.name}-writer-mistral-large3"
  description = "Mistral Large 3 for writing synthetic field reports"

  model_source {
    copy_from = "arn:aws:bedrock:us-east-1::foundation-model/mistral.mistral-large-3-675b-instruct"
  }
}

