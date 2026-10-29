"""Generate the agentic-workflow diagram (draw.io): supervisor, specialists, tools and the path to approval.
Usage: python3 -I code/scripts/make_agent_workflow_diagram.py output/agentic-ai-agent-workflow.drawio"""
import sys
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

PTS = ("points=[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[0,1,0],[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],"
       "[0,0.25,0],[0,0.5,0],[0,0.75,0],[1,0.25,0],[1,0.5,0],[1,0.75,0]];")
ICON = ("sketch=0;" + PTS + "outlineConnect=0;fontColor=#232F3E;fillColor={fill};strokeColor=#ffffff;dashed=0;"
        "verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;"
        "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{icon};")
RES = ("sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor={fill};strokeColor=none;dashed=0;"
       "verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;"
       "pointerEvents=1;shape=mxgraph.aws4.{icon};")
BOX = ("rounded=1;whiteSpace=wrap;html=1;fontSize=11;verticalAlign=top;align=left;spacingLeft=8;spacingTop=4;"
       "arcSize=6;fontColor=#232F3E;{extra}")
EDGE = ("edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;fontSize=10;"
        "endArrow=block;endFill=1;strokeColor=#545B64;fontColor=#232F3E;labelBackgroundColor=#ffffff;{extra}")

# AWS category colours (from draw.io's Sidebar-AWS4.js)
STORAGE, COMPUTE, DATABASE, APPINT, AI, MGMT = "#7AA116", "#ED7100", "#C925D1", "#E7157B", "#01A88D", "#E7157B"
AGENT_FILL, AGENT_STROKE = "#E6F6F7", "#01A88D"  # agents: AI/ML teal
TOOL_FILL = "#FFFFFF"
NOTE_FILL, NOTE_STROKE = "#F5F5F5", "#545B64"
ESC_STROKE = "#DD344C"

cells = []


def add(cid, value, style, x, y, w, h):
    cells.append(f'<mxCell id="{cid}" value="{escape(value, {chr(34): "&quot;"})}" style="{style}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')


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
        pts = "<Array as=\"points\">" + "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in points) + "</Array>"
    cells.append(f'<mxCell id="{cid}" value="{escape(label)}" style="{style}" edge="1" parent="1" source="{src}" '
                 f'target="{dst}"><mxGeometry relative="1" as="geometry">{pts}</mxGeometry></mxCell>')


# ---------- title ----------
add("title", "<b>CER reporting agent: the agentic workflow</b><br>Only judgment cases reach this step; clear-cut cases "
    "take the fixed workflow (rules + KB lookup). <i>Draft: specialist order and tool names are proposals (brief §8 #8).</i>",
    "text;html=1;align=left;verticalAlign=top;fontSize=16;fontColor=#232F3E;whiteSpace=wrap;", 20, 10, 1300, 60)

# ---------- entry and supervisor ----------
box("case", "<b>Case record</b> from intake: extracted fields, confidence per field, first missing-info list",
    470, 90, 300, 56, fill=NOTE_FILL, extra="align=center;spacingLeft=0;")
box("sup", "<b>Supervisor agent</b> (Strands, agents-as-tools)<br>Chooses which specialists to call and in what order "
    "(usually completeness first). Passes each a structured handoff, never the whole transcript.<br>"
    "Limits: max turns, per-case token budget. Escalates when specialists disagree or confidence is low.",
    400, 180, 440, 110, fill=AGENT_FILL, stroke=AGENT_STROKE, extra="strokeWidth=2;")
icon("ddb", "DynamoDB<br>case state + working memory", DATABASE, "dynamodb", 930, 100)

# ---------- specialists ----------
SPEC_Y, SPEC_W, SPEC_H = 370, 230, 130
specs = [
    ("comp", 60, "<b>Completeness specialist</b><br>in: extracted fields + confidence<br>out: confirmed facts, "
                 "contradictions, missing-info questions ranked by whether they could change the decision"),
    ("pol", 320, "<b>Policy / rules specialist</b><br>in: confirmed facts<br>out: reportable y/n, OPR clause, incident "
                 "types, Significant, guideline citations; flags a decision that hinges on a missing fact"),
    ("risk", 580, "<b>Risk / urgency specialist</b><br>in: facts + policy result<br>out: notification and 12-week due "
                  "dates, urgency level, escalate to a person now?"),
    ("draft", 840, "<b>Drafter</b><br>in: the decision so far<br>out: draft CER notice (or not-reportable log entry) "
                   "+ rationale citing the guidelines"),
    ("rev", 1100, "<b>Reviewer</b><br>in: draft + facts + policy result<br>out: pass, or specific fixes sent back to "
                  "the drafter (figures, dates, clause, nothing invented); 1–2 rounds"),
]
for cid, x, text in specs:
    box(cid, text, x, SPEC_Y, SPEC_W, SPEC_H, fill=AGENT_FILL, stroke=AGENT_STROKE)

# ---------- MCP tool layer ----------
box("mcp", "<b>MCP server</b>: one server for all tools; each agent sees only its own (local over stdio; AgentCore "
    "Gateway when deployed)", 40, 560, 1310, 130, extra="dashed=1;")
tools = [
    ("t_comp", 60, "validate_fields<br>lookup_known_facts"),
    ("t_pol", 320, "search_rules (KB)<br>threshold_calc"),
    ("t_risk", 580, "deadline_calc"),
    ("t_draft", 840, "notice_template<br>cite_clause"),
    ("t_rev", 1100, "check_against_facts<br>schema_validate"),
]
for cid, x, text in tools:
    box(cid, text, x, 610, SPEC_W, 56, fill=TOOL_FILL, stroke=NOTE_STROKE, extra="align=center;spacingLeft=0;")
res("kb", "Knowledge Base on S3 Vectors<br>rules only: Guidelines + OPR", STORAGE, "s3_vectors", 411, 726)

# ---------- decision, branches, approval ----------
box("dec", "<b>Decision record</b> (DynamoDB): same schema as the fixed-workflow path, so the evals compare them "
    "directly", 420, 860, 400, 56, fill=NOTE_FILL, extra="align=center;spacingLeft=0;")
box("ready", "<b>Confident</b>: ready for approval", 290, 960, 260, 44, extra="align=center;spacingLeft=0;")
box("esc", "<b>Escalated</b>: flagged for an expert", 690, 960, 260, 44, stroke=ESC_STROKE,
    extra="align=center;spacingLeft=0;strokeWidth=2;")
icon("sfn", "", APPINT, "step_functions", 444, 1050, 44)
box("appr", "<b>Human approval</b>: Step Functions task-token wait. Approve, edit or reject; "
    "nothing is filed without a person.", 500, 1044, 380, 56, extra="align=left;")

# ---------- side panels ----------
box("single", "<b>Single-agent variant</b> (article 3 comparison)<br>Switched by config: one Strands agent holds all the "
    "specialists' tools and a merged prompt. Same model, tools, output schema and limits. Compared with the fixed "
    "workflow and the supervisor on the same cases.", 1390, 180, 300, 150, fill=NOTE_FILL, extra="dashed=1;")
box("across", "<b>Across every step</b><br>• OpenTelemetry span per agent turn and tool call (tokens, cost, latency)"
    "<br>• Retry, fallback model and circuit breaker on every model call<br>• Guardrails mask PII in and out"
    "<br>• Specialists on Nova Lite or Haiku 5.5; Sonnet 5.5 only on escalation", 1390, 370, 300, 170, fill=NOTE_FILL)
icon("cw", "CloudWatch + AgentCore<br>Observability", MGMT, "cloudwatch_2", 1512, 570)
icon("bedrock", "Bedrock models<br>+ Guardrails", AI, "bedrock", 1512, 700)

# ---------- flows ----------
edge("e_case", "case", "sup")
edge("e_mem", "sup", "ddb", "read / write", extra="exitX=1;exitY=0.15;entryX=0;entryY=0.5;startArrow=block;startFill=1;")
for i, cid in enumerate(["comp", "pol", "risk", "draft"]):
    edge(f"e_h{i}", "sup", cid, "handoff / result" if i == 0 else "",
         extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;startArrow=block;startFill=1;")
edge("e_d2r", "draft", "rev", "", extra="exitX=1;exitY=0.3;entryX=0;entryY=0.3;")
edge("e_r2d", "rev", "draft", "", extra="exitX=0;exitY=0.7;entryX=1;entryY=0.7;")
edge("e_r2s", "rev", "sup", "pass, or still failing → escalate", extra="exitX=0.5;exitY=0;entryX=1;entryY=0.5;")
for cid in ["comp", "pol", "risk", "draft", "rev"]:
    edge(f"e_t_{cid}", cid, f"t_{cid}", dashed=True, extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("e_kb", "t_pol", "kb", "rules lookup", dashed=True, extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("e_dec", "sup", "dec", "merged decision", extra="exitX=0;exitY=0.5;entryX=0;entryY=0.5;",
     points=[(25, 235), (25, 888)])
edge("e_ready", "dec", "ready", extra="exitX=0.3;exitY=1;entryX=0.5;entryY=0;")
edge("e_esc", "dec", "esc", extra="exitX=0.7;exitY=1;entryX=0.5;entryY=0;")
edge("e_ra", "ready", "appr", extra="exitX=0.5;exitY=1;entryX=0.25;entryY=0;")
edge("e_ea", "esc", "appr", extra="exitX=0.5;exitY=1;entryX=0.75;entryY=0;")

xml = ('<mxfile host="app.diagrams.net"><diagram id="agents" name="Agentic workflow"><mxGraphModel dx="1600" dy="1000" '
       'grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
       'pageWidth="1720" pageHeight="1150" background="#ffffff" math="0" shadow="0"><root><mxCell id="0"/>'
       '<mxCell id="1" parent="0"/>' + "".join(cells) + "</root></mxGraphModel></diagram></mxfile>")
ET.fromstring(xml)  # fails loudly if the XML is malformed
open(sys.argv[1], "w", encoding="utf-8").write(xml)
print("wrote", sys.argv[1], len(cells), "cells")
