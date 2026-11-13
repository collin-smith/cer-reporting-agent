#!/usr/bin/env bash
# Step 1 of taking down the VPC window (D57): move the approval Lambda out of the VPC with the CLI, then prove it.
#
# Why not Terraform alone: setting vpc_config's lists to [] plans the change, but hashicorp/aws 6.71.0 never sends
# it (CloudTrail, 2026-11-11). The apply then deletes the endpoints, the function loses Bedrock and SNS, and the
# subnets wait on its network interfaces until the apply times out (45 min). Check the function, not the plan.
#
# Usage:
#   ./scripts/vpc_detach.sh            # detach, wait, verify; exits 1 if the function is still in a VPC
#   ./scripts/vpc_detach.sh --check    # verify only, change nothing
# Then step 2: terraform apply (vpc_window back to false). $0: Lambda configuration calls are free.
set -euo pipefail

REGION="${REGION:-ca-central-1}"
FN="${FN:-agentic-ai-approval}"

vpc_id() {
  aws lambda get-function-configuration --function-name "$FN" --region "$REGION" \
    --query 'VpcConfig.VpcId' --output text 2>/dev/null || echo "?"
}

now="$(vpc_id)"
if [[ "$now" == "?" ]]; then
  echo "Can't read $FN in $REGION (missing, or no credentials)." >&2
  exit 1
fi
if [[ -z "$now" || "$now" == "None" ]]; then
  echo "$FN is outside any VPC. Safe to run terraform apply to remove the network."
  exit 0
fi
echo "$FN is in $now."
if [[ "${1:-}" == "--check" ]]; then
  echo "Run ./scripts/vpc_detach.sh (without --check) before deleting the network." >&2
  exit 1
fi

aws lambda update-function-configuration --function-name "$FN" --region "$REGION" \
  --vpc-config SubnetIds=[],SecurityGroupIds=[] --query 'LastUpdateStatus' --output text
aws lambda wait function-updated-v2 --function-name "$FN" --region "$REGION"

now="$(vpc_id)"
if [[ -n "$now" && "$now" != "None" ]]; then
  echo "Still in $now after the update. Don't apply: the network can't be deleted yet." >&2
  exit 1
fi
echo "$FN left the VPC. Now: terraform apply (vpc_window=false) to remove the endpoints, subnets and security group."
