# CER reporting agent

**Does this field report have to go to the regulator, and by when?**

A measured, observable multi-agent system on AWS that triages pipeline-incident field reports against the Canada
Energy Regulator's (CER) reporting rules. It decides whether a report is reportable, under which clause and by what
deadline, lists what's missing, and drafts the notice. A person approves every decision.

The running question: **when does an AI agent earn its cost over a fixed workflow, and when do multiple agents earn
theirs over one?** Every result is reported with accuracy, cost and latency.

> **Status: baseline built.** The rules engine, the 162-case test set, the fixed workflow (Nova Lite reads the
> report, the rules engine decides) and the tier-1 eval harness are in place. The agents come next.

## What's here now

| Path | What it does |
| --- | --- |
| `infra/` | Terraform: tag-filtered budgets (monthly alerts at $50/$75/$100, $300 series cap), an SNS alert topic, and a tagged Bedrock inference profile so model spend is tracked |
| `scripts/nuke.sh` | Stops anything of this project's that bills while idle; `--check` reports only and exits 1 if anything is found |
| `scripts/companion_analysis.py` | The companion piece's analysis of the CER incident data (tables and charts) |
| `scripts/article_html.py`, `table_gen.py`, `chart_gen.py` | Render article drafts as HTML, with tables and charts as images for Medium |
| `scripts/build_map.py` + `scripts/map-template.html` | Builds an interactive map of the CER's public pipeline-incident data |
| `scripts/make_architecture_diagram.py`, `make_agent_workflow_diagram.py` | Generate the architecture and agent-workflow diagrams (draw.io, AWS4 icons) |
| `src/cer_agent/rules.py`, `backtest.py` | The CER reporting rules as code, and the back-test against the CER's own records |
| `src/cer_agent/cases.py`, `writer.py` | Build the test-set specs from real records, and write them up as messy field reports (checked for leaks) |
| `src/cer_agent/extract.py`, `workflow.py` | The fixed workflow: one forced tool call reads the report, plain code converts units and the rules decide |
| `src/cer_agent/evals.py`, `evals/config.toml` | Tier-1 eval harness: decision, deadline, route, missing facts and per-field extraction, with 95% intervals, cost and latency; results in `evals/runs/` |
| `evals/cases/` | The test set: 162 synthetic field reports with expected answers (dev / test / held-out splits) |

## Setup

Python 3.12 and [uv](https://docs.astral.sh/uv/):

```bash
uv sync --extra dev
uv run ruff check . && uv run pytest -q
```

Infrastructure (Terraform >= 1.10, region `ca-central-1`). Create the state bucket once, by hand, so `terraform
destroy` can never delete its own state:

```bash
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
aws s3api create-bucket --bucket agentic-ai-tfstate-$ACCOUNT --region ca-central-1 \
  --create-bucket-configuration LocationConstraint=ca-central-1
aws s3api put-bucket-versioning --bucket agentic-ai-tfstate-$ACCOUNT --versioning-configuration Status=Enabled
aws s3api put-public-access-block --bucket agentic-ai-tfstate-$ACCOUNT --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
aws s3api put-bucket-tagging --bucket agentic-ai-tfstate-$ACCOUNT --tagging 'TagSet=[{Key=project,Value=agentic-ai}]'

cd infra
cp backend.hcl.example backend.hcl            # set the account ID
cp terraform.tfvars.example terraform.tfvars  # set alert_email
terraform init -backend-config=backend.hcl
terraform plan -out=base.plan && terraform apply base.plan
```

Confirm the SNS subscription email, then run `./scripts/nuke.sh --check` before every pause.

Evals (from `code/`). The oracle arm is free and also runs in CI; the workflow arm calls Nova Lite (about $0.0002
a case) through the tagged profile:

```bash
PYTHONPATH=src python -m cer_agent.evals --arm oracle --splits dev test heldout
NOVA_LITE_ARN=$(terraform -chdir=infra output -raw nova_lite_profile_arn) PYTHONPATH=src python -m cer_agent.evals
PYTHONPATH=src python -m cer_agent.evals --rescore RUN_ID   # re-score saved output after a scorer change, $0
```

## Planned stack

Strands Agents (supervisor with specialist agents; one specialist also built in LangGraph for comparison), Amazon
Bedrock (Nova Lite, Claude Haiku 5.5), Step Functions + EventBridge, DynamoDB, a Bedrock Knowledge Base on S3 Vectors
holding the reporting rules, one MCP server for all tools, OpenTelemetry tracing, Terraform, and an eval harness that
runs in GitHub Actions on every pull request.

## Data

[CER Pipeline Incident Data](https://www.cer-rec.gc.ca/open/incident/pipeline-incidents-comprehensive-data.csv),
published under the Open Government Licence – Canada. The data is not stored in this repo.

## Disclaimer

A demonstration on public CER data. Not regulatory advice. The field reports in `evals/cases/` are synthetic:
the operators named in them are fictional, places are generalized to the nearest town, and dates are moved to 2026. Not affiliated with or endorsed by the Canada Energy
Regulator or any pipeline operator.
