"""Generate the agentic-workflow diagram (draw.io), three pages: now, the single agent as built (v3, D37-D38); next,
the supervisor with specialists (article 3's third arm); later, the production layer (articles 2 and 5-7).
Usage: python3 -I code/scripts/make_agent_workflow_diagram.py output/agentic-ai-agent-workflow.drawio"""

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
BOX = (
    "rounded=1;whiteSpace=wrap;html=1;fontSize=11;verticalAlign=top;align=left;spacingLeft=8;spacingTop=4;"
    "arcSize=6;fontColor=#232F3E;{extra}"
)
EDGE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;fontSize=10;"
    "endArrow=block;endFill=1;strokeColor=#545B64;fontColor=#232F3E;labelBackgroundColor=#ffffff;{extra}"
)

# AWS category colours (from draw.io's Sidebar-AWS4.js)
STORAGE, COMPUTE, DATABASE, APPINT, AI, MGMT = "#7AA116", "#ED7100", "#C925D1", "#E7157B", "#01A88D", "#E7157B"
FINANCE = "#7AA116"
AGENT_FILL, AGENT_STROKE = "#E6F6F7", "#01A88D"  # agents: AI/ML teal
TOOL_FILL = "#FFFFFF"
NOTE_FILL, NOTE_STROKE = "#F5F5F5", "#545B64"
ESC_STROKE = "#DD344C"
GROUP = (
    "sketch=0;outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=1;container=0;"
    "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.{gr};verticalAlign=top;align=left;spacingLeft=30;{extra}"
)
CODE_FILL, CODE_STROKE = "#FFFFFF", "#232F3E"  # our own Python code, not an AWS service

cells = []


def add(cid, value, style, x, y, w, h):
    cells.append(
        f'<mxCell id="{cid}" value="{escape(value, {chr(34): "&quot;"})}" style="{style}" vertex="1" parent="1">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
    )


def box(cid, value, x, y, w, h, fill="none", stroke=NOTE_STROKE, extra=""):
    add(cid, value, BOX.format(extra=f"fillColor={fill};strokeColor={stroke};{extra}"), x, y, w, h)


def icon(cid, label, fill, name, x, y, size=56):
    add(cid, label, ICON.format(fill=fill, icon=name), x, y, size, size)


def res(cid, label, fill, name, x, y, size=48):
    add(cid, label, RES.format(fill=fill, icon=name), x, y, size, size)


def edge(cid, src, dst, label="", dashed=False, extra="", points=()):
    style = EDGE.format(extra=("dashed=1;" if dashed else "") + extra)
    pts = ""
    if points:
        pts = '<Array as="points">' + "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in points) + "</Array>"
    cells.append(
        f'<mxCell id="{cid}" value="{escape(label)}" style="{style}" edge="1" parent="1" source="{src}" '
        f'target="{dst}"><mxGeometry relative="1" as="geometry">{pts}</mxGeometry></mxCell>'
    )


# ================= page 2: next, the supervisor (article 3's third arm) =================
add(
    "title",
    "<b>Next: supervisor with specialists</b> (article 3's third arm; planned, not built)<br>Same front end, rules "
    "engine and stricter-only tools as the single agent. Specialist split and tool names are proposals "
    "(brief §8 #8). Production pieces are on the next page.",
    "text;html=1;align=left;verticalAlign=top;fontSize=16;fontColor=#232F3E;whiteSpace=wrap;",
    20, 10, 1440, 60,
)  # fmt: skip
box("case", "<b>Same front end as now</b>: field report → extract → rules engine. Only judgment cases go to the "
    "supervisor; clear-cut cases take the fixed workflow.", 400, 90, 440, 60, fill=NOTE_FILL,
    extra="align=center;spacingLeft=0;")  # fmt: skip
box("sup", "<b>Supervisor agent</b> (Strands, agents-as-tools)<br>Chooses which specialists to call and in what "
    "order. Passes each a structured handoff, never the whole transcript.<br>Limits: max turns, per-case token "
    "budget. Escalates when specialists disagree.", 400, 190, 440, 100, fill=AGENT_FILL, stroke=AGENT_STROKE,
    extra="strokeWidth=2;")  # fmt: skip
SPEC_Y, SPEC_W, SPEC_H = 370, 230, 130
specs = [
    ("comp", 60, "<b>Completeness specialist</b><br>in: report + recorded facts<br>out: quoted, stricter-only "
     "patches; missing facts confirmed; questions ranked by whether they could change the decision"),
    ("pol", 320, "<b>Policy specialist</b><br>in: reviewed facts<br>out: the rules engine's decision (it can't set "
     "one) and the rules that hinge on a missing or disputed fact"),
    ("risk", 580, "<b>Risk / urgency specialist</b><br>in: facts + decision<br>out: urgency; escalate to a person "
     "now? Deadlines come from the rules engine"),
    ("draft", 840, "<b>Drafter</b> (existing <i>drafter.py</i>)<br>in: the packet<br>out: draft notice or file "
     "note; code renders the decision, the model writes PIR-5–13"),
]  # fmt: skip
box("tframe", "<b>Tools</b> (Strands @tool, in-process, as on the single agent; every check is code)", 40, 540, 1050,
    120, extra="dashed=1;")  # fmt: skip
for cid, x, text in specs:
    box(cid, text, x, SPEC_Y, SPEC_W, SPEC_H, fill=AGENT_FILL, stroke=AGENT_STROKE)
tools = [
    ("t_comp", 60, "patch_facts (stricter-only)<br>confirm_missing"),
    ("t_pol", 320, "decide (the rules engine)<br>rule_text"),
    ("t_risk", 580, "rule_text<br>read the packet's deadline"),
    ("t_draft", 840, "render + check (code)<br>narrative (Nova Lite)"),
]
for cid, x, text in tools:
    box(cid, text, x, 585, SPEC_W, 56, fill=TOOL_FILL, stroke=NOTE_STROKE, extra="align=center;spacingLeft=0;")
box("dec", "<b>Packet</b>: the rules engine's, in the same schema as every other arm, so the evals compare them "
    "directly", 420, 720, 400, 56, fill=NOTE_FILL, extra="align=center;spacingLeft=0;")  # fmt: skip
box("judge", "<b>Judge</b> (existing <i>judge.py</i>): code checks the decision parts; Nova Lite the narrative",
    420, 810, 400, 50, **{"fill": CODE_FILL, "stroke": CODE_STROKE}, extra="align=center;spacingLeft=0;")  # fmt: skip
box("ready", "<b>Clear</b>: ready for approval", 290, 900, 260, 44, extra="align=center;spacingLeft=0;")
box("esc", "<b>Escalated</b>: a person decides", 690, 900, 260, 44, stroke=ESC_STROKE,
    extra="align=center;spacingLeft=0;strokeWidth=2;")  # fmt: skip
res("human", "", "#232F3E", "user", 480, 990, 40)
box("appr", "<b>Approver</b>: approve, edit or reject. Nothing is filed without a person.", 530, 985, 300, 50)
add("cloud", "AWS Cloud", GROUP.format(gr="group_aws_cloud_alt", extra="strokeColor=#232F3E;fillColor=none;"
    "fontColor=#232F3E;dashed=0;"), 1130, 90, 340, 260)  # fmt: skip
add("region", "Canada (Central) ca-central-1", GROUP.format(gr="group_region", extra="strokeColor=#00A4A6;"
    "fillColor=none;fontColor=#147EBA;dashed=1;"), 1150, 130, 300, 200)  # fmt: skip
icon("bedrock", "Amazon Bedrock: Nova Lite<br>tagged inference profile", AI, "bedrock", 1272, 180, 56)
box("compare", "<b>What article 3 compares</b><br>Same cases, model, tools and limits: the fixed workflow (and the "
    "strictest-of-layouts check), the single agent (v3) and this supervisor. Each with accuracy, stability, cost "
    "and latency.<br>The supervisor is kept only if it earns its cost.", 1130, 400, 340, 170,
    fill=NOTE_FILL)  # fmt: skip

edge("e_case", "case", "sup")
for i, cid in enumerate(["comp", "pol", "risk", "draft"]):
    edge(f"e_h{i}", "sup", cid, "handoff / result" if i == 0 else "",
         extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;startArrow=block;startFill=1;")  # fmt: skip
for cid in ["comp", "pol", "risk", "draft"]:
    edge(f"e_t_{cid}", cid, f"t_{cid}", dashed=True, extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("e_dec", "sup", "dec", "packet", extra="exitX=0;exitY=0.5;entryX=0;entryY=0.5;", points=[(25, 240), (25, 748)])
edge("e_dj", "dec", "judge", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("e_ready", "judge", "ready", extra="exitX=0.3;exitY=1;entryX=0.5;entryY=0;")
edge("e_esc", "judge", "esc", extra="exitX=0.7;exitY=1;entryX=0.5;entryY=0;")
edge("e_ra", "ready", "appr", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;", points=[(420, 1010)])
edge("e_ea", "esc", "appr", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;", points=[(820, 1010)])
edge("e_sb", "sup", "bedrock", "each turn", dashed=True, extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;",
     points=[(1100, 240), (1100, 208)])  # fmt: skip
planned = cells[:]
cells.clear()

# ================= page 1: the single agent as built (v3) =================
add(
    "title",
    "<b>The single agent as built</b> (v3, <code>cer_agent.agent</code>): the agent reviews the workflow's reading and "
    "can change facts, one at a time, only in the stricter direction. The rules engine makes every decision.",
    "text;html=1;align=left;verticalAlign=top;fontSize=16;fontColor=#232F3E;whiteSpace=wrap;",
    20, 10, 1440, 50,
)  # fmt: skip
C = {"fill": CODE_FILL, "stroke": CODE_STROKE}
CTR = "align=center;spacingLeft=0;"
box("report", "<b>Field report</b><br>(text)", 40, 120, 170, 60, fill=NOTE_FILL, extra=CTR)
box("extract", "<b>1. Extract</b> (code, one model call)<br>normalise, then <i>record_facts</i>: the fixed "
    "workflow's own reading", 260, 110, 210, 90, **C)  # fmt: skip
box("rules", "<b>2. Rules engine</b> (code, <i>rules.py</i>)<br>status, deadline, route, missing facts. "
    "Only the rules engine decides.", 520, 110, 230, 90, **C, extra="strokeWidth=2;")  # fmt: skip
box("agent", "<b>3. Review agent</b> (Strands 1.64 on Nova Lite, up to 10 turns)<br>Sees the report, the recorded "
    "facts and the rules result. Checks the reading against the report. Can change facts; can't set a status, a "
    "deadline or a route.", 260, 280, 490, 100, fill=AGENT_FILL, stroke=AGENT_STROKE,
    extra="strokeWidth=2;")  # fmt: skip
TOOLS = [
    ("patch", 40, "<b>patch_facts</b>(field, value, quote)<br>one fact at a time; every other fact kept"),
    ("confirm", 290, "<b>confirm_missing</b>(fact, found)<br>only facts the rules list as missing; not found → "
     "a question for the field"),
    ("ruletext", 540, "<b>rule_text</b>(rule_id)<br>the rules spec's text for one rule"),
    ("finish", 790, "<b>finish</b>(escalate, reason)<br>escalate only for doubt the rules can't settle"),
]  # fmt: skip
box("tooltitle", "<b>Tools</b> (Strands @tool; every check is code, not prompt)", 30, 420, 990, 120, extra="dashed=1;")
for cid, x, text in TOOLS:
    box(cid, text, x, 450, 220, 80, fill=TOOL_FILL, stroke=NOTE_STROKE)
GATES = [
    ("g1", "Value fits the field's type"),
    ("g2", "Quote is the report's own words"),
    ("g3", "Rules engine re-decides on the change"),
    ("g4", "At least as strict? (notify, deadline, due time, route)"),
]
for i, (cid, text) in enumerate(GATES):
    box(cid, text, 40, 600 + i * 80, 220, 52, **C, extra=CTR + ("strokeWidth=2;" if cid == "g4" else ""))
box("reject", "<b>Not changed</b><br>the reason goes back to the agent", 300, 600, 200, 132, fill=NOTE_FILL, extra=CTR)
box("rulesspec", "<i>input/cer/rules-spec.md</i>", 540, 600, 200, 44, fill=NOTE_FILL, extra=CTR)
box("applied", "<b>Applied</b><br>new result back to the agent", 40, 940, 220, 56, fill=AGENT_FILL, stroke=AGENT_STROKE,
    extra=CTR)  # fmt: skip
box("held", "<b>Held for the approver</b><br>facts unchanged; suggestion and quote kept; route → judgment "
    "(AGENT-HOLD)", 300, 930, 260, 76, stroke=ESC_STROKE, extra=CTR + "strokeWidth=2;")  # fmt: skip
box("packet", "<b>4. Packet</b><br>the rules engine's, from the reviewed facts, plus the agent's trace (patches, "
    "holds, escalation)", 790, 600, 230, 90, fill=NOTE_FILL)  # fmt: skip
box("drafter", "<b>5. Drafter</b> (<i>drafter.py</i>)<br>code renders the decision; Nova Lite writes PIR-5–13 "
    "only; held suggestions listed", 790, 740, 230, 80, **C)  # fmt: skip
box("judge", "<b>6. Judge</b> (<i>judge.py</i>)<br>code checks the decision parts; Nova Lite checks the narrative, "
    "quotes verified", 790, 860, 230, 80, **C)  # fmt: skip
res("human", "", "#232F3E", "user", 790, 985, 40)
box("approver", "<b>Approver</b>: approve, edit or reject. Sees held suggestions. Nothing is filed.", 840, 975, 230,
    60, extra="align=left;")  # fmt: skip

add("cloud", "AWS Cloud", GROUP.format(gr="group_aws_cloud_alt", extra="strokeColor=#232F3E;fillColor=none;"
    "fontColor=#232F3E;dashed=0;"), 1090, 70, 380, 300)  # fmt: skip
add("region", "Canada (Central) ca-central-1", GROUP.format(gr="group_region", extra="strokeColor=#00A4A6;"
    "fillColor=none;fontColor=#147EBA;dashed=1;"), 1110, 110, 340, 240)  # fmt: skip
icon("bedrock", "Amazon Bedrock: Nova Lite<br>tagged inference profile<br><i>agentic-ai-nova-lite</i>", AI, "bedrock",
     1252, 170, 56)  # fmt: skip
box("cant", "<b>What the agent can't do</b> (enforced in the tools)<br>• set a status, deadline or route<br>• loosen "
    "the result: that goes to a person as a suggestion<br>• change a fact without the report's words<br>• confirm a "
    "fact the rules don't list as missing<br>• file anything", 1090, 420, 380, 150, fill=NOTE_FILL)  # fmt: skip
box("notyet", "<b>Not in the as-built path yet</b><br>• per-stage tracing (article 2)<br>• MCP server for the "
    "tools (article 5)<br>• Step Functions approval wait, DynamoDB case state<br>• drafter and judge run as "
    "separate steps on saved packets", 1090, 610, 380, 120, extra="dashed=1;")  # fmt: skip

edge("p_r2e", "report", "extract")
edge("p_e2r", "extract", "rules", "facts")
edge("p_r2a", "rules", "agent", "report + facts + result", extra="exitX=0.75;exitY=1;entryX=0.75;entryY=0;")
for cid, _x, _ in TOOLS:
    edge(f"p_a_{cid}", "agent", cid, extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("p_p2g", "patch", "g1", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
for a, b in (("g1", "g2"), ("g2", "g3"), ("g3", "g4")):
    edge(f"p_{a}{b}", a, b, "yes", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("p_g1x", "g1", "reject", "no", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.2;")
edge("p_g2x", "g2", "reject", "no", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.8;")
edge("p_g4y", "g4", "applied", "yes", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("p_g4n", "g4", "held", "no: would loosen", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;", points=[(430, 866)])
edge("p_loop", "applied", "rules", "rules re-decide", extra="exitX=0;exitY=0.5;entryX=0.25;entryY=1;",
     points=[(20, 968), (20, 240), (577, 240)])  # fmt: skip
edge("p_rt", "ruletext", "rulesspec", dashed=True, extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("p_fin", "finish", "packet", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("p_held", "held", "packet", "AGENT-HOLD", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.7;",
     points=[(765, 968), (765, 663)])  # fmt: skip
edge("p_pd", "packet", "drafter", dashed=True, extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("p_dj", "drafter", "judge", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("p_ja", "judge", "approver", extra="exitX=0.5;exitY=1;entryX=0.4;entryY=0;")
edge("p_xb", "extract", "bedrock", "1 call", dashed=True, extra="exitX=0.5;exitY=0;entryX=0;entryY=0.5;",
     points=[(365, 95), (1220, 95), (1220, 198)])  # fmt: skip
edge("p_ab", "agent", "bedrock", "each turn", dashed=True, extra="exitX=1;exitY=0.5;entryX=1;entryY=0.5;",
     points=[(1340, 330), (1340, 198)])  # fmt: skip
as_built = cells[:]
cells.clear()

# ================= page 3: later, the production layer (articles 2 and 5-7) =================
add(
    "title",
    "<b>Later: the production layer</b> (articles 2 and 5–7; planned)<br>It wraps whichever agent design wins article "
    "3. Built so far: budgets, alerts, the state bucket and tagged model profiles. The full deployment, with the web "
    "front end, is in <i>agentic-ai-architecture.drawio</i>.",
    "text;html=1;align=left;verticalAlign=top;fontSize=16;fontColor=#232F3E;whiteSpace=wrap;",
    20, 10, 1440, 60,
)  # fmt: skip
add("cloud", "AWS Cloud", GROUP.format(gr="group_aws_cloud_alt", extra="strokeColor=#232F3E;fillColor=none;"
    "fontColor=#232F3E;dashed=0;"), 20, 80, 1460, 840)  # fmt: skip
add("region", "Canada (Central) ca-central-1", GROUP.format(gr="group_region", extra="strokeColor=#00A4A6;"
    "fillColor=none;fontColor=#147EBA;dashed=1;"), 40, 120, 1420, 780)  # fmt: skip
add("vpc", "VPC: hardening run (article 6, stretch). Default runs use public endpoints with IAM.",
    GROUP.format(gr="group_vpc2", extra="strokeColor=#8C4FFF;fillColor=none;fontColor=#232F3E;dashed=0;"
    "fontStyle=0;"), 560, 150, 240, 300)  # fmt: skip
add("subnet", "Private subnet (one AZ)", GROUP.format(gr="group_security_group", extra="grStroke=0;"
    "strokeColor=#00A4A6;fillColor=#E6F6F7;fontColor=#147EBA;dashed=0;"), 580, 210, 200, 210)  # fmt: skip
icon("reports", "S3: field reports", STORAGE, "s3", 80, 190)
icon("eb", "EventBridge rule", APPINT, "eventbridge", 230, 190)
icon("sfn", "Step Functions<br>orchestrator (D7)", APPINT, "step_functions", 380, 190)
res("human", "Approver<br>task-token wait (article 6)", "#232F3E", "user", 388, 330, 40)
icon("agentfn", "Lambda: the agent<br>(article 3's winner)", COMPUTE, "lambda", 652, 250)
icon("gateway", "AgentCore Gateway: MCP<br>tools (article 5; stdio first)", AI, "bedrock_agentcore", 880, 180)
res("kb", "Knowledge Base on S3 Vectors<br>rules text only (D15)", STORAGE, "s3_vectors", 1084, 184)
icon("runtime", "AgentCore Runtime<br>(article 7 deploy window)", AI, "bedrock_agentcore", 880, 360)
icon("bedrock", "Bedrock models + Guardrails<br>PII, denied topics, prompt attacks<br>retries, fallback model, "
     "circuit breaker (article 6)", AI, "bedrock", 420, 560)  # fmt: skip
icon("ddb", "DynamoDB<br>case state + memory<br>(article 7)", DATABASE, "dynamodb", 662, 560)
icon("cw", "CloudWatch + AgentCore<br>Observability: a span per stage<br>(tracing from article 2)", MGMT,
     "cloudwatch_2", 880, 560)  # fmt: skip
icon("budgets", "AWS Budgets (deployed)<br>+ $100 action once the<br>first IAM role exists", FINANCE, "budgets_2",
     1120, 560)  # fmt: skip
icon("sns", "SNS alerts<br>(deployed)", APPINT, "sns", 1300, 560, size=48)
box("byarticle", "<b>By article</b><br>• <b>2</b> tracing on every stage (extract, review, decide, draft, judge); "
    "CI gate on the eval targets<br>• <b>5</b> one MCP server for the tools, used by the agent and by Claude Code; "
    "tool-design changes measured by the evals<br>• <b>6</b> Guardrails, the prompt-injection set, the human "
    "approval gate, retries / fallback model / circuit breaker, VPC hardening (stretch)<br>• <b>7</b> AgentCore "
    "Runtime + Gateway deploy window, memory, caching, model cascade, dashboards, cost per case",
    60, 730, 1380, 140, fill=NOTE_FILL)  # fmt: skip

edge("l_r2e", "reports", "eb", "report lands")
edge("l_e2s", "eb", "sfn")
edge("l_s2a", "sfn", "agentfn", "start case", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;",
     points=[(520, 218), (520, 278)])  # fmt: skip
edge("l_s2h", "sfn", "human", "approval", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("l_a2g", "agentfn", "gateway", "tool calls", extra="exitX=1;exitY=0.3;entryX=0;entryY=0.5;",
     points=[(840, 267), (840, 208)])  # fmt: skip
edge("l_g2k", "gateway", "kb", "rules lookup", dashed=True, extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
edge("l_a2r", "agentfn", "runtime", "moves to", dashed=True, extra="exitX=1;exitY=0.9;entryX=0;entryY=0.5;",
     points=[(820, 300), (820, 388)])  # fmt: skip
edge("l_a2b", "agentfn", "bedrock", "model calls", extra="exitX=0.25;exitY=1;entryX=0.5;entryY=0;")
edge("l_a2d", "agentfn", "ddb", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;startArrow=block;startFill=1;")
edge("l_a2c", "agentfn", "cw", "traces", dashed=True, extra="exitX=0.75;exitY=1;entryX=0.5;entryY=0;")
edge("l_b2s", "budgets", "sns", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
production = cells[:]


def page(pid, name, cs, w, h):
    return (
        f'<diagram id="{pid}" name="{name}"><mxGraphModel dx="1600" dy="1000" grid="1" gridSize="10" guides="1" '
        f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{w}" pageHeight="{h}" '
        'background="#ffffff" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
        + "".join(cs)
        + "</root></mxGraphModel></diagram>"
    )


xml = (
    '<mxfile host="app.diagrams.net">'
    + page("asbuilt", "Now: single agent (v3)", as_built, 1500, 1080)
    + page("agents", "Next: supervisor (article 3, planned)", planned, 1500, 1060)
    + page("production", "Later: production layer (articles 2, 5–7, planned)", production, 1500, 940)
    + "</mxfile>"
)
ET.fromstring(xml)  # fails loudly if the XML is malformed
pathlib.Path(sys.argv[1]).write_text(xml, encoding="utf-8")
print("wrote", sys.argv[1], len(as_built), "+", len(planned), "+", len(production), "cells")
