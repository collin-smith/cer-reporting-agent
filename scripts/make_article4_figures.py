"""Article 4's diagram (draw.io, AWS4 style):
1. the same agent built twice: the shared, framework-free core (the workflow's first reading, `Case` with the quote
   check and the stricter-only gate, the prompt and the four tools) under two loops. Strands keeps its loop inside
   `Agent` and, by default, sends `finish`'s reply back for one more model turn; LangGraph's loop is a graph we draw,
   which ends when `finish` has run. Both call Nova Lite on Bedrock in Canada and write the same OpenTelemetry spans.

Only Bedrock sits inside the AWS Cloud and Region groups: the article 4 runs were local against Bedrock (dev split),
and nothing else was deployed for them. No VPC existed.

Figure 2 is a chart: code/scripts/chart_article4.py.

Usage (from the project root): python3 -I code/scripts/make_article4_figures.py output
Writes output/article-4-figure-01.drawio. PNG: export from draw.io at 200% (Border width 20, grid off), or with the
desktop app's CLI (from a Windows-aware shell):
    "/mnt/c/Program Files/draw.io/draw.io.exe" -x -f png -s 2 -b 20 -o <png> <drawio>
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))  # -I drops the script dir
from drawio_kit import (  # noqa: E402
    AGENT_FILL,
    AGENT_STROKE,
    AI,
    CENTER,
    CODE_FILL,
    CODE_STROKE,
    ESC_STROKE,
    NOTE_FILL,
    TITLE,
    Diagram,
)  # fmt: skip

CLOUD = "strokeColor=#232F3E;fillColor=none;fontColor=#232F3E;dashed=0;"
REGION = "strokeColor=#00A4A6;fillColor=none;fontColor=#147EBA;dashed=1;"
CODE = {"fill": CODE_FILL, "stroke": CODE_STROKE}
AGENT = {"fill": AGENT_FILL, "stroke": AGENT_STROKE}
LANE = "text;html=1;align=left;verticalAlign=top;fontSize=13;fontColor=#232F3E;whiteSpace=wrap;"
NOTE = "text;html=1;align=left;verticalAlign=top;fontSize=11;fontColor=#545B64;whiteSpace=wrap;"
FRAME = "rounded=1;arcSize=4;dashed=1;fillColor=none;strokeColor=#879196;verticalAlign=top;align=left;spacingLeft=10;"
WASTE = f"strokeColor={ESC_STROKE};strokeWidth=2;fontColor={ESC_STROKE};"
LEFT = "align=left;spacingLeft=10;verticalAlign=middle;"


def figure1(out: pathlib.Path) -> None:
    d = Diagram()
    d.add("title", "<b>The same agent, built twice</b><br>Everything that makes the agent safe is plain Python both "
          "builds share. Only the loop is written per framework, and the one real difference is where it ends.",
          TITLE, 20, 10, 1340, 50)  # fmt: skip

    # shared core (left)
    d.add("corehead", "<b>Shared by both builds</b> (no framework imports)", LANE, 20, 85, 330, 24)
    d.box("report", "<b>Field report</b>", 20, 120, 130, 44, fill=NOTE_FILL, extra=CENTER)
    d.box("read", "<b>First reading</b><br>one Nova Lite call", 190, 115, 160, 54, **CODE, extra=CENTER)
    d.box("case", "<b>Case</b> (plain Python class)<br><br>facts · quote check<br><b>stricter-only gate</b>: a change "
          "that would loosen the result is held for a person<br>the decision packet", 20, 200, 330, 120, **CODE,
          extra=LEFT + "strokeWidth=2;")  # fmt: skip
    d.box("tools", "<b>Four tools</b> (Case methods; docstrings are what the model sees)<br>patch_facts (must quote "
          "the report) · confirm_missing · rule_text · finish", 20, 340, 330, 66, fill="#FFFFFF",
          stroke=AGENT_STROKE, extra=LEFT + "fontSize=11;")  # fmt: skip
    d.box("prompt", "System prompt, word for word · temperature 0 · 10-turn limit", 20, 424, 330, 34, fill="#FFFFFF",
          extra=CENTER + "fontSize=11;")  # fmt: skip
    d.edge("e1", "report", "read")
    d.edge("e2", "read", "case", "facts", extra="exitX=0.5;exitY=1;entryX=0.75;entryY=0;")

    # Strands lane
    d.add("sframe", "<b>A. Strands Agents</b>: the loop lives inside <i>Agent</i> (SDK defaults)", FRAME, 400, 85,
          560, 170)  # fmt: skip
    d.box("smodel", "<b>Model turn</b><br>Agent(model, tools, prompt)", 425, 125, 170, 54, **AGENT, extra=CENTER)
    d.box("stools", "<b>Run tools</b><br>calls Case methods", 650, 125, 150, 54, **AGENT, extra=CENTER)
    d.edge("s1", "smodel", "stools", "tool calls", extra="exitX=1;exitY=0.35;entryX=0;entryY=0.35;")
    d.edge("s2", "stools", "smodel", "results", extra="exitX=0;exitY=0.65;entryX=1;entryY=0.65;")
    d.box("sextra", "<b>One more model turn</b> after finish<br>(\"Done. Stop now.\"), with the whole "
          "conversation as input. Decides nothing.", 425, 196, 375, 44, fill="#FCEBEC", stroke=ESC_STROKE,
          extra=CENTER + "fontSize=11;")  # fmt: skip
    d.edge("s3", "stools", "sextra", "after finish", extra=WASTE + "exitX=0.5;exitY=1;entryX=0.83;entryY=0;")
    d.add("snum", "<b>Default</b>: 4.51 turns, $0.95 per 1,000<br><b>finish stops the loop</b> (one call, "
          "agent.cancel): 3.23 turns, $0.76", NOTE, 815, 120, 140, 125)  # fmt: skip

    # LangGraph lane
    d.add("lframe", "<b>B. LangGraph</b>: the loop is a graph we draw (StateGraph)", FRAME, 400, 275, 560, 185)
    d.box("start", "START", 425, 325, 64, 34, fill="#FFFFFF", extra=CENTER + "rounded=1;arcSize=50;fontSize=11;")
    d.box("lmodel", "<b>model</b> node<br>turns += 1", 520, 315, 130, 54, **AGENT, extra=CENTER)
    d.box("ltools", "<b>tools</b> node<br>ToolNode(Case tools)", 700, 315, 150, 54, **AGENT, extra=CENTER)
    d.box("end", "END", 760, 405, 64, 34, fill="#FFFFFF", extra=CENTER + "rounded=1;arcSize=50;fontSize=11;")
    d.edge("l0", "start", "lmodel")
    d.edge("l1", "lmodel", "ltools", "tool calls", extra="exitX=1;exitY=0.35;entryX=0;entryY=0.35;")
    d.edge("l2", "ltools", "lmodel", "otherwise", extra="exitX=0;exitY=0.65;entryX=1;entryY=0.65;")
    d.edge("l3", "ltools", "end", "finish ran, or turns ≥ 10", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    d.edge("l4", "lmodel", "end", "no tool call", dashed=True, extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;",
           points=[(585, 422)])  # fmt: skip
    d.add("lnum", "3.30 turns<br>$0.69 per 1,000", NOTE, 865, 330, 90, 50)

    # both builds use the shared core
    d.edge("c1", "tools", "sframe", "same tools", dashed=True, extra="exitX=1;exitY=0.3;entryX=0;entryY=0.6;")
    d.edge("c2", "tools", "lframe", "same tools", dashed=True, extra="exitX=1;exitY=0.7;entryX=0;entryY=0.5;")

    # where the model runs, and the traces
    d.group("cloud", "AWS Cloud", "group_aws_cloud_alt", CLOUD, 1000, 85, 360, 230)
    d.group("region", "Canada (Central) ca-central-1", "group_region", REGION, 1015, 120, 330, 180)
    d.icon("bedrock", "Amazon Bedrock<br>Nova Lite, tagged inference profile<br>every model call, both builds", AI,
           "bedrock", 1152, 160)  # fmt: skip
    d.edge("b1", "sframe", "bedrock", "Converse", extra="exitX=1;exitY=0.3;entryX=0;entryY=0.4;")
    d.edge("b2", "lframe", "bedrock", "Converse", extra="exitX=1;exitY=0.2;entryX=0;entryY=0.8;")
    d.box("traces", "<b>OpenTelemetry spans</b>, kept local<br>Strands emits them itself; the LangGraph build opens "
          "the same spans (about ten lines), so one trace summary reads both", 1000, 345, 360, 70, fill=NOTE_FILL,
          extra=LEFT + "fontSize=11;")  # fmt: skip
    d.edge("t1", "sframe", "traces", dashed=True, extra="exitX=1;exitY=0.85;entryX=0;entryY=0.25;")
    d.edge("t2", "lframe", "traces", dashed=True, extra="exitX=1;exitY=0.5;entryX=0;entryY=0.75;")

    # legend and measurement note
    d.box("lg1", "our Python code", 20, 490, 130, 30, **CODE, extra=CENTER)
    d.box("lg2", "framework loop: a model chooses the next step", 165, 490, 290, 30, **AGENT, extra=CENTER)
    d.box("lg3", "a turn that decides nothing", 470, 490, 190, 30, fill="#FCEBEC", stroke=ESC_STROKE, extra=CENTER)
    d.add("measured", "<b>Measured on dev</b> (33 reports, 3 passes each): status right 92% (Strands default), 96% "
          "(Strands, finish stops), 93% (LangGraph), the same answers within the model's normal variation. Ending the "
          "loop at finish saved about a fifth of the cost; the framework, nothing measurable.", NOTE, 680, 485, 680,
          45)  # fmt: skip
    d.write(out / "article-4-figure-01.drawio", "Article 4: the same agent, built twice", 1380, 545)


if __name__ == "__main__":
    figure1(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "output"))
