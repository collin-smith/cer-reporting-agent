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
