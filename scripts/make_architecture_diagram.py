"""Generate the agentic-AI architecture diagram (draw.io, AWS4 icons).

Usage: python3 -I code/scripts/make_architecture_diagram.py output/agentic-ai-architecture.drawio
"""

import pathlib
import sys
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

PTS = (
    "points=[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[0,1,0],[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],"
    "[0,0.25,0],[0,0.5,0],[0,0.75,0],[1,0.25,0],[1,0.5,0],[1,0.75,0]];"
)
ICON = (
    "sketch=0;" + PTS + "outlineConnect=0;fontColor=#232F3E;fillColor={fill};strokeColor=#ffffff;dashed=0;"
    "verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;"
    "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{icon};"
)
RES = (
    "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor={fill};strokeColor=none;dashed=0;"
    "verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;"
    "pointerEvents=1;shape=mxgraph.aws4.{icon};"
)
GROUP = (
    "sketch=0;outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=1;"
    "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.{gr};verticalAlign=top;align=left;spacingLeft=30;{extra}"
)
BOX = (
    "rounded=1;whiteSpace=wrap;html=1;fontSize=11;verticalAlign=top;align=left;spacingLeft=8;spacingTop=4;"
    "arcSize=4;{extra}"
)
EDGE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;fontSize=10;"
    "endArrow=block;endFill=1;strokeColor=#545B64;fontColor=#232F3E;labelBackgroundColor=#ffffff;{extra}"
)

# AWS category colours (from draw.io's Sidebar-AWS4.js)
STORAGE, COMPUTE, DATABASE, APPINT = "#7AA116", "#ED7100", "#C925D1", "#E7157B"
AI, SECURITY, NETWORK, MGMT, FINANCE = "#01A88D", "#DD344C", "#8C4FFF", "#E7157B", "#7AA116"

cells = []


def add(cid, value, style, x, y, w, h):
    cells.append(
        f'<mxCell id="{cid}" value="{escape(value, {chr(34): "&quot;"})}" style="{style}" vertex="1" parent="1">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
    )


def icon(cid, label, fill, name, x, y, size=56):
    add(cid, label, ICON.format(fill=fill, icon=name), x, y, size, size)


def res(cid, label, fill, name, x, y, size=48):
    add(cid, label, RES.format(fill=fill, icon=name), x, y, size, size)


def edge(cid, src, dst, label="", dashed=False, extra=""):
    style = EDGE.format(extra=("dashed=1;" if dashed else "") + extra)
    cells.append(
        f'<mxCell id="{cid}" value="{escape(label)}" style="{style}" edge="1" parent="1" source="{src}" '
        f'target="{dst}"><mxGeometry relative="1" as="geometry"/></mxCell>'
    )


# ---------- containers (drawn first so they sit behind) ----------
add(
    "title",
    "<b>CER reporting agent: architecture</b><br>Does this field report have to go to the regulator, and by when?",
    "text;html=1;align=left;verticalAlign=top;fontSize=16;fontColor=#232F3E;",
    20,
    10,
    700,
    50,
)
add(
    "cloud",
    "AWS Cloud",
    GROUP.format(gr="group_aws_cloud_alt", extra="strokeColor=#232F3E;fillColor=none;fontColor=#232F3E;dashed=0;"),
    250,
    70,
    1460,
    960,
)
add(
    "region",
    "Region: ca-central-1 (infrastructure and data stay in Canada)",
    GROUP.format(gr="group_region", extra="strokeColor=#00A4A6;fillColor=none;fontColor=#147EBA;dashed=1;"),
    270,
    110,
    1150,
    900,
)
add(
    "us",
    "US regions: cross-region inference (us.* profiles)",
    GROUP.format(gr="group_region", extra="strokeColor=#00A4A6;fillColor=none;fontColor=#147EBA;dashed=1;"),
    1440,
    110,
    250,
    210,
)
add(
    "demo",
    "<b>Demo front end</b> (stretch) · quotas + daily spend kill switch",
    BOX.format(extra="dashed=1;fillColor=none;strokeColor=#DD344C;fontColor=#232F3E;"),
    290,
    150,
    640,
    170,
)
add(
    "orch",
    "<b>Intake + orchestration</b> (core)",
    BOX.format(extra="fillColor=none;strokeColor=#E7157B;fontColor=#232F3E;"),
    290,
    350,
    440,
    200,
)
add(
    "vpc",
    "VPC: hardened deployment (Stage 5 run, stretch). Default runs and the demo use the same Lambdas "
    "outside the VPC, on public endpoints with IAM. No NAT gateway.",
    GROUP.format(gr="group_vpc2", extra="strokeColor=#8C4FFF;fillColor=none;fontColor=#232F3E;dashed=0;fontStyle=0;"),
    750,
    350,
    650,
    420,
)
add(
    "subnet",
    "Private subnet (one AZ)",
    GROUP.format(
        gr="group_security_group", extra="grStroke=0;strokeColor=#00A4A6;fillColor=#E6F6F7;fontColor=#147EBA;dashed=0;"
    ),
    770,
    420,
    490,
    330,
)
add(
    "managed",
    "<b>Managed services</b> (regional, outside the VPC)",
    BOX.format(extra="fillColor=none;strokeColor=#AAB7B8;fontColor=#232F3E;"),
    290,
    800,
    1110,
    190,
)

# ---------- outside AWS ----------
res("visitors", "Registered visitors", "#232F3D", "users", 70, 180)
res("reviewer", "Reviewer<br>(approves each case)", "#232F3D", "user", 70, 400)
res(
    "laptop",
    "Laptop: Strands dev runs,<br>eval harness, MCP server<br>(stdio), Claude Code",
    "#232F3D",
    "client",
    70,
    580,
)
add(
    "github",
    "<b>GitHub</b><br>Public repo · Actions runs<br>tier-1 evals on every PR ($0)",
    BOX.format(extra="fillColor=#F5F5F5;strokeColor=#545B64;fontColor=#232F3E;align=center;spacingLeft=0;"),
    20,
    740,
    160,
    70,
)
add(
    "langfuse",
    "<b>Langfuse</b> (stretch)<br>2nd OTel destination,<br>one comparison",
    BOX.format(extra="dashed=1;fillColor=#F5F5F5;strokeColor=#545B64;fontColor=#232F3E;align=center;spacingLeft=0;"),
    20,
    900,
    160,
    70,
)

# ---------- demo front end ----------
icon("cf", "CloudFront", NETWORK, "cloudfront", 320, 200)
icon("site", "S3 static site", STORAGE, "s3", 470, 200)
icon("cognito", "Cognito<br>sign-up / sign-in", SECURITY, "cognito", 620, 200)
icon("apigw", "API Gateway<br>usage plans (quota)", APPINT, "api_gateway", 790, 200)

# ---------- intake + orchestration ----------
icon("reports", "S3: field reports", STORAGE, "s3", 320, 410)
icon("eb", "EventBridge rule", APPINT, "eventbridge", 460, 410)
icon("sfn", "Step Functions<br>orchestrator +<br>approval wait", APPINT, "step_functions", 610, 410)

# ---------- VPC / private subnet ----------
icon("lintake", "Lambda: intake,<br>completeness, rules", COMPUTE, "lambda", 810, 480)
icon("lsup", "Lambda: supervisor +<br>specialists (Strands)", COMPUTE, "lambda", 1000, 480)
icon("acrt", "AgentCore Runtime<br>(deploy window)", AI, "bedrock_agentcore", 810, 630)
icon("acgw", "AgentCore Gateway<br>MCP tools", AI, "bedrock_agentcore", 1000, 630)
res("gwep", "Gateway endpoints<br>S3, DynamoDB (free)", NETWORK, "endpoints", 1310, 470)
res(
    "ifep",
    "Interface endpoints, 1 AZ<br>bedrock-runtime, logs, sts<br>(torn down by nuke.sh)",
    NETWORK,
    "endpoints",
    1160,
    634,
)

# ---------- managed services ----------
icon("ddb", "DynamoDB<br>case state + memory", DATABASE, "dynamodb", 330, 860)
icon("bedrock", "Bedrock: Nova Lite (ca.*)<br>+ Guardrails (PII)", AI, "bedrock", 520, 860)
res("vectors", "Knowledge Base on<br>S3 Vectors (rules corpus)", STORAGE, "s3_vectors", 720, 864)
icon("acmem", "AgentCore Memory<br>(stretch)", AI, "bedrock_agentcore", 910, 860)
icon("cw", "CloudWatch + AgentCore<br>Observability (OTel traces)", MGMT, "cloudwatch_2", 1100, 860)
icon("claude", "Bedrock: Claude Haiku 5.5 /<br>Sonnet 5.5 (checkpoints)", AI, "bedrock", 1537, 180)
icon("budgets", "AWS Budgets<br>alerts $50 / $75 a month,<br>teardown at $100", FINANCE, "budgets_2", 1537, 420)

# ---------- flows ----------
edge("e1", "visitors", "cf", "browse")
edge("e2", "cf", "site")
edge("e3", "site", "cognito", "sign in")
edge("e4", "cognito", "apigw", "JWT")
edge("e5", "apigw", "sfn", "start case", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("e6", "reports", "eb", "object created")
edge("e7", "eb", "sfn", "start case")
edge("e8", "sfn", "lintake", "1. intake")
edge("e9", "lintake", "lsup", "2. judgment cases")
edge("e10", "sfn", "reviewer", "3. approval (task token)", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
edge("e11", "lsup", "acgw", "MCP tool calls")
edge("e12", "lsup", "claude", "us.* at checkpoints", dashed=True, extra="exitX=1;exitY=0.25;entryX=0;entryY=0.5;")
edge("e13", "subnet", "bedrock", "model calls + retry / fallback", extra="exitX=0.1;exitY=1;entryX=0.5;entryY=0;")
edge("e14", "sfn", "ddb", "case state", extra="exitX=0;exitY=1;entryX=0.5;entryY=0;")
edge("e15", "subnet", "vectors", "rules lookup", extra="exitX=0.3;exitY=1;entryX=0.5;entryY=0;")
edge("e16", "subnet", "cw", "OTel traces", dashed=True, extra="exitX=0.8;exitY=1;entryX=0.5;entryY=0;")
edge("e17", "laptop", "bedrock", "dev runs (Nova Lite)", dashed=True)
edge("e18", "laptop", "github", "push")
edge("e19", "laptop", "langfuse", "OTel export", dashed=True)

xml = (
    '<mxfile host="app.diagrams.net"><diagram id="arch" name="Architecture"><mxGraphModel dx="1600" dy="1000" '
    'grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
    'pageWidth="1740" pageHeight="1060" background="#ffffff" math="0" shadow="0"><root><mxCell id="0"/>'
    '<mxCell id="1" parent="0"/>' + "".join(cells) + "</root></mxGraphModel></diagram></mxfile>"
)
ET.fromstring(xml)  # fails loudly if the XML is malformed
pathlib.Path(sys.argv[1]).write_text(xml, encoding="utf-8")
print("wrote", sys.argv[1], len(cells), "cells")
