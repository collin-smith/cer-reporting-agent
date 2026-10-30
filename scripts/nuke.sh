#!/usr/bin/env bash
# Run at the end of every build session. Stops or deletes anything of this project's that bills while idle,
# and reports anything in the account that would. Does NOT run `terraform destroy`: that's a separate decision.
#
# Usage:
#   ./scripts/nuke.sh           # clean up this project's idle-billing items, then report spend
#   ./scripts/nuke.sh --check   # report only, change nothing; exits 1 if anything bills while idle
#
# Scope: only items named agentic-ai* (or tagged project=agentic-ai) are ever changed. The account is shared
# (StudySite), so everything else is reported, never touched.
set -euo pipefail

REGION="${REGION:-ca-central-1}"
PROJECT="${PROJECT:-agentic-ai}"
CHECK=0
[[ "${1:-}" == "--check" ]] && CHECK=1
FOUND=0
OTHER=0 # items outside this project: reported, never changed

say() { printf '\n=== %s ===\n' "$1"; }
clean() { echo "none — good"; }
# found <description> <command...>: report the item; outside --check, also run the command.
found() {
  local what="$1"
  shift
  FOUND=$((FOUND + 1))
  if ((CHECK)); then
    echo "!! $what"
  else
    "$@" >/dev/null
    echo "fixed: $what"
  fi
}
# report <description>: count and print an item this script never changes.
report() {
  FOUND=$((FOUND + 1))
  OTHER=$((OTHER + 1))
  echo "!! $1"
}
awsr() { aws "$@" --region "$REGION" --output text; }

((CHECK)) && echo "CHECK MODE: reporting only, nothing will be changed."

# Fail early and clearly. On WSL the usual cause is clock drift after Windows sleeps.
if ! err=$(aws sts get-caller-identity --region "$REGION" --output text 2>&1 >/dev/null); then
  echo
  if [[ "$err" == *"Signature expired"* || "$err" == *"SignatureDoesNotMatch"* ]]; then
    echo "!! The local clock is off, so AWS rejects the request. Fix it, then re-run:"
    echo "     sudo ntpdate time.windows.com"
  else
    echo "!! Can't reach AWS with the current credentials:"
    echo "   $err"
  fi
  echo "NOT CHECKED: nothing was inspected or changed."
  exit 2
fi

say "Bedrock provisioned throughput (bills per hour; this series never uses it)"
items=$(awsr bedrock list-provisioned-model-throughputs --query 'provisionedModelSummaries[].provisionedModelName')
for p in $items; do report "provisioned throughput $p (delete it in the console)"; done
[[ -z "${items// /}" ]] && clean

say "OpenSearch Serverless collections (the Knowledge Base default; bills ~\$175+/month idle; we use S3 Vectors)"
items=$(awsr opensearchserverless list-collections --query 'collectionSummaries[].name' 2>/dev/null || true)
for c in $items; do report "OpenSearch Serverless collection $c"; done
[[ -z "${items// /}" ]] && clean

say "AgentCore runtimes named ${PROJECT}* (deployed only for the Stage 7 window)"
n=0
while IFS=$'\t' read -r id name; do
  [[ -z "${name:-}" || "$name" != ${PROJECT}* ]] && continue
  n=$((n + 1))
  found "AgentCore runtime $name" aws bedrock-agentcore-control delete-agent-runtime \
    --agent-runtime-id "$id" --region "$REGION"
done < <(awsr bedrock-agentcore-control list-agent-runtimes \
  --query 'agentRuntimes[].[agentRuntimeId,agentRuntimeName]' 2>/dev/null || true)
((n == 0)) && clean

say "Step Functions executions still running (${PROJECT}* state machines)"
n=0
for sm in $(awsr stepfunctions list-state-machines --query "stateMachines[?starts_with(name, '${PROJECT}')].stateMachineArn"); do
  for x in $(awsr stepfunctions list-executions --state-machine-arn "$sm" --status-filter RUNNING \
    --query 'executions[].executionArn'); do
    n=$((n + 1))
    found "execution ${x##*:}" aws stepfunctions stop-execution --execution-arn "$x" --region "$REGION"
  done
done
((n == 0)) && clean

say "EventBridge rules named ${PROJECT}* (enabled rules start runs while you're away)"
items=$(awsr events list-rules --name-prefix "$PROJECT" --query "Rules[?State=='ENABLED'].Name")
for r in $items; do found "EventBridge rule $r ENABLED" aws events disable-rule --name "$r" --region "$REGION"; done
[[ -z "${items// /}" ]] && clean

say "Lambda provisioned concurrency (bills while idle; never used here)"
n=0
for f in $(awsr lambda list-functions --query 'Functions[].FunctionName'); do
  pc=$(awsr lambda list-provisioned-concurrency-configs --function-name "$f" \
    --query 'length(ProvisionedConcurrencyConfigs)' 2>/dev/null || echo 0)
  if [[ "$pc" != "0" ]]; then
    n=$((n + 1))
    report "Lambda $f has provisioned concurrency"
  fi
done
((n == 0)) && clean

say "DynamoDB tables named ${PROJECT}* on provisioned capacity (should be on-demand)"
n=0
for t in $(awsr dynamodb list-tables --query "TableNames[?starts_with(@, '${PROJECT}')]"); do
  mode=$(awsr dynamodb describe-table --table-name "$t" --query 'Table.BillingModeSummary.BillingMode')
  if [[ "$mode" != "PAY_PER_REQUEST" ]]; then
    n=$((n + 1))
    report "DynamoDB table $t is $mode (switch it to on-demand in Terraform)"
  fi
done
((n == 0)) && clean

say "NAT gateways and interface VPC endpoints tagged project=${PROJECT} (Stage 6 hardening run only)"
items=$(awsr ec2 describe-nat-gateways --filter "Name=tag:project,Values=${PROJECT}" Name=state,Values=available \
  --query 'NatGateways[].NatGatewayId')
items+=" $(awsr ec2 describe-vpc-endpoints --filters "Name=tag:project,Values=${PROJECT}" \
  Name=vpc-endpoint-type,Values=Interface --query 'VpcEndpoints[].VpcEndpointId')"
for i in $items; do report "$i (remove with terraform: it's part of the VPC stack)"; done
[[ -z "${items// /}" ]] && clean

say "Log groups named /aws/*/${PROJECT}* with no retention (logs then bill forever)"
n=0
for g in $(awsr logs describe-log-groups --query "logGroups[?retentionInDays==null].logGroupName"); do
  [[ "$g" == *"${PROJECT}"* ]] || continue
  n=$((n + 1))
  found "log group $g: setting 14-day retention" aws logs put-retention-policy --log-group-name "$g" \
    --retention-in-days 14 --region "$REGION"
done
((n == 0)) && clean

# Cost Explorer sums floats, so $0 can come back as -1e-09. Print dollars and cents.
usd() { awk '{ v = $1 + 0; if (v < 0.005 && v > -0.005) v = 0; printf "$%.2f\n", v }'; }

say "Spend tagged project=${PROJECT}, before credits"
# Two Cost Explorer queries ($0.01 each). Usage only: the Free plan books an equal negative credit.
series_start="${SERIES_START:-2026-10-01}"
month_start="$(date -u +%Y-%m-01)"
tomorrow="$(date -u -d tomorrow +%Y-%m-%d)"
q() {
  aws ce get-cost-and-usage --region us-east-1 --time-period "Start=$1,End=${tomorrow}" \
    --granularity MONTHLY --metrics UnblendedCost \
    --filter "{\"And\":[{\"Tags\":{\"Key\":\"project\",\"Values\":[\"${PROJECT}\"]}},{\"Dimensions\":{\"Key\":\"RECORD_TYPE\",\"Values\":[\"Usage\"]}}]}" \
    --query 'sum(ResultsByTime[].to_number(Total.UnblendedCost.Amount))' --output text 2>/dev/null
}
if month=$(q "$month_start") && series=$(q "$series_start"); then
  printf "  %-22s %8s   <- alerts at \$50 / \$75, teardown at \$100\n" "this month" "$(usd <<<"$month")"
  printf "  %-22s %8s   <- series cap \$300\n" "series since ${series_start}" "$(usd <<<"$series")"
else
  echo "(Cost Explorer not queryable yet — check the console)"
fi
echo "(Cost Explorer lags up to ~24 h. Bedrock calls are tagged only when made through the project's inference"
echo " profiles (terraform output); calls to a bare model ID show only in the account-wide view.)"

echo
if ((CHECK)); then
  if ((FOUND)); then
    echo "NOT CLEAN: $FOUND item(s) still billing or scheduled."
    (((FOUND - OTHER) > 0)) && echo "  $((FOUND - OTHER)) from this project: run ./scripts/nuke.sh to fix them."
    ((OTHER > 0)) && echo "  $OTHER need a manual step or belong elsewhere in the account (listed above)."
    exit 1
  fi
  echo "CLEAN: nothing billing while idle. Safe to pause."
else
  echo "done ($((FOUND - OTHER)) item(s) fixed). Confirm with: ./scripts/nuke.sh --check"
  ((OTHER > 0)) && echo "$OTHER item(s) were NOT changed: review them (listed above)."
  echo "Full teardown when the series ends:  terraform -chdir=infra destroy"
fi
