# CER reporting agent

**Does this field report have to go to the regulator, and by when?**

A measured, observable multi-agent system on AWS that triages pipeline-incident field reports against the Canada
Energy Regulator's (CER) reporting rules. It decides whether a report is reportable, under which clause and by what
deadline, lists what's missing, and drafts the notice. A person approves every decision.

The running question: **when does an AI agent earn its cost over a fixed workflow, and when do multiple agents earn
theirs over one?** Every result is reported with accuracy, cost and latency.

> **Status: design stage.** The architecture is settled and the build has not started. So far this repo holds the
> scripts for the CER incident map and the architecture diagrams.

## What's here now

| Path | What it does |
| --- | --- |
| `scripts/build_map.py` + `scripts/map-template.html` | Builds an interactive map of the CER's public pipeline-incident data |
| `scripts/make_architecture_diagram.py` | Generates the AWS architecture diagram (draw.io, AWS4 icons) |
| `scripts/make_agent_workflow_diagram.py` | Generates the agentic workflow diagram: supervisor, specialists, MCP tools, path to human approval |

## Planned stack

Strands Agents (supervisor with specialist agents; one specialist also built in LangGraph for comparison), Amazon
Bedrock (Nova Lite, Claude Haiku 5.5), Step Functions + EventBridge, DynamoDB, a Bedrock Knowledge Base on S3 Vectors
holding the reporting rules, one MCP server for all tools, OpenTelemetry tracing, Terraform, and an eval harness that
runs in GitHub Actions on every pull request.

## Data

[CER Pipeline Incident Data](https://www.cer-rec.gc.ca/open/incident/pipeline-incidents-comprehensive-data.csv),
published under the Open Government Licence – Canada. The data is not stored in this repo.

## Disclaimer

A demonstration on public CER data. Not regulatory advice. Not affiliated with or endorsed by the Canada Energy
Regulator or any pipeline operator.
