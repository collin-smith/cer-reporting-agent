"""Article 3's diagrams (draw.io, AWS4 style):
1. three designs on the same front end: the fixed workflow (strict check), one reviewing agent, a supervisor with two
   specialists. The rules engine decides in all three; what differs is who chooses the next step.
3. where the miss started: CL-064 step by step, the reviewers after the reading, and the fix in the reading.

Figures 2 and 4 are charts: code/scripts/chart_article3.py.

Usage (from the project root): python3 -I code/scripts/make_article3_figures.py output
Writes output/article-3-figure-0{1,3}.drawio. PNGs: export each from draw.io at 200%, or with the desktop app's CLI
(from a Windows-aware shell):
    "/mnt/c/Program Files/draw.io/draw.io.exe" -x -f png -s 2 -o <png> <drawio>
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
MISS = f"strokeColor={ESC_STROKE};strokeWidth=3;"
FIX = "strokeColor=#1D8102;strokeWidth=3;"


def figure1(out: pathlib.Path) -> None:
    d = Diagram()
    d.add("title", "<b>Three designs, one front end</b><br>The rules engine decides in all three. What changes is who "
          "chooses the next step: the code, one model, or a model directing two others.", TITLE, 20, 10, 1340,
          50)  # fmt: skip
    rows = [  # (key, y, lane text, metrics)
        ("wf", 100, "<b>A. Fixed workflow</b><br>the code sets every step", "$0.60 per 1,000 reports · p95 1.8 s"),
        ("ag", 250, "<b>B. One reviewing agent</b><br>the model chooses its next tool, up to 10 turns",
         "$0.90 per 1,000 reports · p95 13 s"),
        ("sv", 440, "<b>C. Supervisor + two specialists</b><br>a model directs two others, each with its own tools",
         "$1.52 per 1,000 reports · p95 16 s"),
    ]  # fmt: skip
    for key, y, lane, metrics in rows:
        d.add(f"{key}lane", lane, LANE, 20, y, 180, 60)
        d.add(f"{key}cost", metrics, NOTE, 20, y + (82 if key == "sv" else 62), 180, 40)
        d.box(f"{key}report", "<b>Field report</b>", 210, y + 10, 100, 50, fill=NOTE_FILL, extra=CENTER)
        read = "<b>Read</b><br>3 layouts, strictest answer" if key == "wf" else "<b>Read</b><br>one reading"
        d.box(f"{key}read", read, 340, y + 10, 140, 50, **CODE, extra=CENTER)
        d.box(f"{key}rules", "<b>Rules engine</b><br>decides", 510, y + 10, 120, 50, **CODE,
              extra=CENTER + "strokeWidth=2;")  # fmt: skip
        d.box(f"{key}packet", "<b>Decision packet</b><br>draft, judge, approver", 1060, y + 10, 160, 50,
              fill=NOTE_FILL, extra=CENTER)  # fmt: skip
        d.res(f"{key}approver", "Approver", "#232F3E", "user", 1260, y + 11, 48)
        d.edge(f"{key}e1", f"{key}report", f"{key}read")
        d.edge(f"{key}e2", f"{key}read", f"{key}rules")
        d.edge(f"{key}e9", f"{key}packet", f"{key}approver")
    d.edge("wfe3", "wfrules", "wfpacket")
    # B: one agent with four tools; a patch goes back through the rules engine
    d.box("agent", "<b>Reviewing agent</b> (Strands)<br>checks the reading against the report", 680, 250, 200, 70,
          **AGENT, extra=CENTER)  # fmt: skip
    d.box("agtools", "<b>Tools</b>: patch_facts (stricter only; a loosening change is held for the approver) · "
          "confirm_missing · rule_text · finish", 680, 340, 340, 38, fill="#FFFFFF", stroke=AGENT_STROKE,
          extra="fontSize=10;")  # fmt: skip
    d.edge("age3", "agrules", "agent")
    d.edge("age4", "agent", "agrules", "a patch is re-decided", dashed=True,
           extra="exitX=0.25;exitY=0;entryX=0.75;entryY=0;", points=[(730, 235), (600, 235)])  # fmt: skip
    d.edge("age5", "agent", "agpacket", "finish")
    d.edge("age6", "agent", "agtools", dashed=True, extra="endArrow=none;")
    # C: supervisor, two specialists
    d.box("sup", "<b>Supervisor</b><br>asks, then finishes<br>≤ 2 calls per specialist", 680, 440, 180, 70, **AGENT,
          extra=CENTER)  # fmt: skip
    d.box("comp", "<b>Completeness specialist</b><br>patch_facts · confirm_missing", 660, 550, 190, 54, **AGENT,
          extra=CENTER + "fontSize=10;")  # fmt: skip
    d.box("pol", "<b>Policy specialist</b><br>rule_text (read-only)", 870, 550, 170, 54, **AGENT,
          extra=CENTER + "fontSize=10;")  # fmt: skip
    d.edge("sve3", "svrules", "sup")
    d.edge("sve4", "sup", "comp", "short handoff", extra="exitX=0.3;exitY=1;entryX=0.5;entryY=0;")
    d.edge("sve5", "sup", "pol", extra="exitX=0.8;exitY=1;entryX=0.5;entryY=0;")
    d.edge("sve6", "sup", "svpacket", "finish")
    # where the models run
    d.group("cloud", "AWS Cloud", "group_aws_cloud_alt", CLOUD, 1100, 540, 250, 175)
    d.group("region", "Canada (Central) ca-central-1", "group_region", REGION, 1115, 575, 220, 125)
    d.icon("bedrock", "Amazon Bedrock: Nova Lite<br>tagged inference profile", AI, "bedrock", 1201, 612, 48)
    # legend
    d.box("lg1", "our Python code", 210, 640, 130, 30, **CODE, extra=CENTER)
    d.box("lg2", "a model chooses the next step", 360, 640, 200, 30, **AGENT, extra=CENTER)
    d.add("lg3", "Every model call (reading, agent, supervisor, specialists) goes to Nova Lite on Bedrock in Canada, "
          "through one tagged profile.", NOTE, 580, 640, 470, 40)  # fmt: skip
    d.write(out / "article-3-figure-01.drawio", "Article 3: three designs", 1370, 730)


def figure3(out: pathlib.Path) -> None:
    d = Diagram()
    d.add("title", "<b>Where the miss started</b><br>CL-064, a held-out report. The rules were right for the facts "
          "they were given; the facts were wrong from the first step.", TITLE, 20, 10, 1300, 50)  # fmt: skip
    d.box("report", "<b>The report says</b><br>“SCADA showed flow at 110% of max design rate for about 3 mins… No "
          "product released, just running outside design limits.”", 20, 100, 250, 100, fill=NOTE_FILL,
          extra=CENTER)  # fmt: skip
    d.box("read", "<b>1 Read</b> (Nova Lite)<br>beyond design: <b>none</b><br>12 of 12 runs, every layout", 320,
          110, 200, 80, **CODE, extra=CENTER + MISS)  # fmt: skip
    d.box("rules", "<b>2 Rules engine</b><br>no beyond-design fact →<br><b>not reportable</b><br>(right for the facts "
          "it got)", 570, 105, 190, 90, **CODE, extra=CENTER)  # fmt: skip
    d.box("result", "<b>Missed report</b><br>the regulator is never told", 810, 115, 180, 70, fill="#FCEBEC",
          stroke=ESC_STROKE, extra=CENTER)  # fmt: skip
    d.edge("e1", "report", "read")
    d.edge("e2", "read", "rules")
    d.edge("e3", "rules", "result")
    d.add("marker", "<b>The error starts here</b>", "text;html=1;align=center;fontSize=12;fontColor=#DD344C;",
          320, 80, 200, 24)  # fmt: skip
    # after the reading: reviewers
    d.add("after", "<b>Adding AI after the reading</b> (held-out, 3 runs each)", LANE, 570, 352, 420, 24)
    d.box("agent", "<b>One reviewing agent</b><br>caught it 0 of 3 times<br>~5× the workflow's cost", 570, 275,
          190, 70, **AGENT, extra=CENTER)  # fmt: skip
    d.box("sup", "<b>Supervisor + specialists</b><br>caught it 1 of 3 times<br>~7× the workflow's cost", 800, 275,
          190, 70, **AGENT, extra=CENTER)  # fmt: skip
    d.edge("e4", "rules", "agent", dashed=True, extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    d.edge("e5", "rules", "sup", dashed=True, extra="exitX=0.75;exitY=1;entryX=0.5;entryY=0;",
           points=[(712, 230), (895, 230)])  # fmt: skip
    # the fix, at the reading
    d.add("fixhead", "<b>Fixing the step where it started</b> (D44)", LANE, 20, 390, 500, 24)
    d.box("fix", "<b>Reworded instruction</b> for the beyond-design fact: flow above its design rate, throughput above "
          "its rating, vibration past its design, or the report saying outside design limits. Same model, same cost "
          "per report.", 20, 425, 500, 70, fill="#FFFFFF", stroke="#1D8102", extra="strokeWidth=2;")  # fmt: skip
    d.edge("e6", "fix", "read", "changes step 1", extra=FIX + "exitX=0.6;exitY=0;entryX=0.5;entryY=1;")
    d.box("newcases", "<b>9 new reports</b> that describe the condition the way CL-064 does<br>before: 8 of 18 runs "
          "right · after: <b>9 of 9</b> on dev, test and fresh held-out", 570, 425, 420, 70, fill=NOTE_FILL,
          extra=CENTER)  # fmt: skip
    d.edge("e7", "fix", "newcases")
    d.add("note", "Measured on the new reports. Strict check + reader fix on test: 0 missed, 0 late, "
          "$0.60 per 1,000 reports. CL-064 itself isn't "
          "re-scored: the held-out set was already used.", NOTE, 20, 520, 970, 30)  # fmt: skip
    d.write(out / "article-3-figure-03.drawio", "Article 3: where the miss started", 1010, 560)


if __name__ == "__main__":
    o = pathlib.Path(sys.argv[1])
    figure1(o)
    figure3(o)
