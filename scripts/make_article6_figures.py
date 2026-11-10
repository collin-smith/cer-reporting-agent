"""Article 6's diagrams (draw.io, AWS4 style):
1. the approval gate: the Step Functions states (triage, wait on a task token, escalate on the clock, close; any
   triage failure to a person) and the services behind them.
2. when the model fails: SDK retries, the reader's temperature steps, the fallback model, then a person; with the
   measured retry budget.

Usage (from the project root): python3 -I code/scripts/make_article6_figures.py output
Writes output/article-6-figure-0{1,2}.drawio. PNGs: export each from draw.io at 200% (Border width 20, grid off), or
with the desktop app's CLI (from a Windows-aware shell):
    "/mnt/c/Program Files/draw.io/draw.io.exe" -x -f png -s 2 -b 20 -o <png> <drawio>
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))  # -I drops the script dir
from drawio_kit import (  # noqa: E402
    AI,
    APPINT,
    CENTER,
    CODE_FILL,
    CODE_STROKE,
    COMPUTE,
    DATABASE,
    ESC_STROKE,
    NOTE_FILL,
    TITLE,
    Diagram,
)  # fmt: skip

CLOUD = "strokeColor=#232F3E;fillColor=none;fontColor=#232F3E;dashed=0;"
REGION = "strokeColor=#00A4A6;fillColor=none;fontColor=#147EBA;dashed=1;"
CODE = {"fill": CODE_FILL, "stroke": CODE_STROKE}
FAIL = {"fill": "#FDEDEF", "stroke": ESC_STROKE}
PERSON = {"fill": "#FFF4E5", "stroke": "#B35900"}
LANE = "text;html=1;align=left;verticalAlign=top;fontSize=13;fontColor=#232F3E;whiteSpace=wrap;"
NOTE = "text;html=1;align=left;verticalAlign=top;fontSize=11;fontColor=#545B64;whiteSpace=wrap;"
RED = f"strokeColor={ESC_STROKE};fontColor={ESC_STROKE};"
GOOD = "strokeColor=#1D8102;fontColor=#1D8102;"
JUMP = "jumpStyle=arc;jumpSize=10;"
CHOICE = "rhombus;whiteSpace=wrap;html=1;fontSize=11;fontColor=#232F3E;fillColor=#FFFFFF;strokeColor=#232F3E;"


def figure1(out: pathlib.Path) -> None:
    d = Diagram()
    d.add("title", "<b>The approval gate</b><br>Nothing is filed without a named person. An unanswered case gets "
          "louder on the reporting clock; a failed triage still reaches a person.", TITLE,
          20, 10, 1340, 50)  # fmt: skip
    d.box("report", "<b>Field report</b><br>email, call note, scan", 20, 262, 180, 56, fill=NOTE_FILL, extra=CENTER)
    d.box("person", "<b>Approver</b> (on call; backup)<br>approve · edit · reject<br>from the CLI, with a reason",
          20, 545, 180, 86, **PERSON, extra=CENTER)  # fmt: skip
    d.group("cloud", "AWS Cloud", "group_aws_cloud_alt", CLOUD, 240, 80, 1120, 650)
    d.group("region", "Canada (Central) ca-central-1", "group_region", REGION, 260, 115, 1080, 595)
    d.add("sfn", "<b>AWS Step Functions</b> (Standard): one execution per report", LANE, 300, 160, 500, 24)
    # row A
    d.box("triage", "<b>Triage</b><br>guardrail flags · strict check<br>decides · draft · mask PII", 300, 250, 190,
          80, **CODE, extra=CENTER)  # fmt: skip
    d.box("wait", "<b>Wait for approval</b><br>task token on the case; $0 while it waits; timeout = the next "
          "escalation mark", 610, 250, 210, 80, **CODE, extra=CENTER + "strokeWidth=2;")  # fmt: skip
    d.box("close", "<b>Close</b><br>who, when, why;<br>a diff of any edit", 1040, 250, 170, 80, **CODE,
          extra=CENTER)  # fmt: skip
    # row B
    d.box("failed", "<b>Triage failed</b><br>raw report in place of a draft; top of the queue; page now", 300, 410,
          190, 70, **FAIL, extra=CENTER)  # fmt: skip
    d.box("escalate", "<b>Escalate</b><br>3 h case: backup at 60 min, both at 150<br>24 h case: 8 h, 20 h", 668,
          410, 200, 70, **CODE, extra=CENTER)  # fmt: skip
    d.add("overdue_q", "Past the<br>deadline?", CHOICE, 900, 405, 110, 80)
    d.box("overdue", "<b>OVERDUE</b><br>the run fails: red in the console", 1060, 410, 150, 70, **FAIL,
          extra=CENTER)  # fmt: skip
    # edges
    d.edge("e_report", "report", "triage", "", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.edge("e_tw", "triage", "wait", "draft + flags", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.edge("e_tf", "triage", "failed", "", extra=RED + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    d.edge("e_fw", "failed", "wait", "as a 3-hour case", extra=RED + "exitX=1;exitY=0.5;entryX=0.1;entryY=1;",
           points=[(631, 445)])  # fmt: skip
    d.edge("e_we", "wait", "escalate", "timeout", extra="exitX=0.75;exitY=1;entryX=0.5;entryY=0;")
    d.edge("e_eq", "escalate", "overdue_q", "", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.edge("e_qw", "overdue_q", "wait", "no: page, wait for the next mark",
           extra="exitX=0.5;exitY=0;entryX=0.95;entryY=1;", points=[(955, 370), (810, 370)])  # fmt: skip
    d.edge("e_qo", "overdue_q", "overdue", "yes", extra=RED + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.edge("e_wc", "wait", "close", "the decision resumes the run", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.edge("e_pw", "person", "wait", "decision + token", extra=JUMP + "exitX=0.5;exitY=0;entryX=0;entryY=0.8;",
           points=[(110, 375), (580, 375), (580, 314)])  # fmt: skip
    d.add("anyerr", "any error", "text;html=1;align=left;fontSize=10;fontColor=#DD344C;", 400, 340, 70, 20)
    # services
    d.add("svc", "Every state is one call to the same Lambda function.", NOTE, 300, 505, 400, 20)
    d.icon("sns", "Amazon SNS<br>pages by email", APPINT, "sns", 340, 560, 56)
    d.icon("lambda", "AWS Lambda<br>triage · park · escalate · close", COMPUTE, "lambda", 580, 560, 56)
    d.icon("ddb", "Amazon DynamoDB<br>the case record; queue<br>index sorted by deadline", DATABASE, "dynamodb",
           820, 560, 56)  # fmt: skip
    d.icon("bedrock", "Amazon Bedrock<br>Nova Lite; Haiku 5.5 fallback;<br>two guardrails", AI, "bedrock", 1060, 560,
           56)  # fmt: skip
    d.edge("s1", "lambda", "sns", dashed=True)
    d.edge("s2", "lambda", "ddb", dashed=True)
    d.edge("s3", "lambda", "bedrock", dashed=True, extra="exitX=0.5;exitY=0;entryX=0.5;entryY=0;",
           points=[(608, 547), (1088, 547)])  # fmt: skip
    d.edge("e_page", "sns", "person", "page", extra="exitX=0;exitY=0.5;entryX=1;entryY=0.5;")
    d.add("cost", "Measured: in the queue within 7 s; pages on schedule; per case $0.0008–0.0013 of AI and "
          "$0.0001–0.0003 of workflow. A case that waits 20 hours costs what one approved in 20 seconds does.", NOTE,
          20, 745, 1340, 34)  # fmt: skip
    d.write(out / "article-6-figure-01.drawio", "Article 6: the approval gate", 1380, 790)


def figure2(out: pathlib.Path) -> None:
    d = Diagram()
    d.add("title", "<b>When the model fails</b><br>Each layer catches a different failure. Whatever gets through all "
          "of them reaches a person, never nowhere.", TITLE, 20, 10, 1340, 50)  # fmt: skip
    w, y, h = 220, 150, 110
    xs = [20, 310, 590, 870, 1150]
    d.box("read", "<b>Nova Lite reads the report</b><br>three layouts in parallel,<br>each its own reading", xs[0], y,
          w - 20, h, **CODE, extra=CENTER)  # fmt: skip
    d.box("sdk", "<b>1. AWS SDK retries</b><br>throttling, 500/503, model not ready: backoff and the adaptive rate "
          "limiter.<br><b>3 retries</b> (not 10)", xs[1], y, w, h, **CODE, extra=CENTER)  # fmt: skip
    d.box("temp", "<b>2. The reader retries</b><br>a malformed tool call, at temperature 0.3 then 0.7 (the SDK "
          "doesn't retry it)", xs[2], y, w, h, **CODE, extra=CENTER)  # fmt: skip
    d.box("fb", "<b>3. Fallback model</b><br>Claude Haiku 5.5, Canada profile: another provider, same country, "
          "its own client", xs[3], y, w, h, **CODE, extra=CENTER + "strokeWidth=2;")  # fmt: skip
    d.box("person", "<b>A person</b><br>triage failed: the raw report at the top of the queue, approver paged",
          xs[4], y, w, h, **PERSON, extra=CENTER)  # fmt: skip
    d.edge("f1", "read", "sdk", "error", extra=RED)
    d.edge("f2", "sdk", "temp", "fails", extra=RED)
    d.edge("f3", "temp", "fb", "fails", extra=RED)
    d.edge("f4", "fb", "person", "fails", extra=RED)
    d.edge("skip", "read", "person", "validation, access denied, a bug: ours to fix, not retried or switched",
           extra=RED + "dashed=1;exitX=0.5;exitY=0;entryX=0.5;entryY=0;", points=[(120, 110), (1255, 110)])  # fmt: skip
    d.box("answer", "<b>An answer</b> → the rules decide → the draft for the approver (any fallback reading is "
          "flagged on it)", 310, 330, 780, 50, fill="#EAF5E6", stroke="#1D8102", extra=CENTER)  # fmt: skip
    for i, key in enumerate(("sdk", "temp", "fb")):
        d.edge(f"ok{i}", key, "answer", "answers", extra=GOOD + "exitX=0.5;exitY=1;entryY=0;"
               f"entryX={(xs[i + 1] + w / 2 - 310) / 780:.3f};")  # fmt: skip
    d.box("draft", "<b>The draft fails the same way:</b> Nova Lite → Haiku 5.5 → a draft rendered from the rules "
          "alone, saying which fields no model wrote. The decision never needs a model.", 310, 400, 780, 46,
          fill=NOTE_FILL, extra=CENTER)  # fmt: skip
    d.add("measured", "<b>Measured with injected errors, $0</b> (a hook inside the SDK; 83 test reports; nine "
          "failure types): at 10 SDK retries, throttling that doesn't stop waited 196 s (median) and up to 262 s per "
          "reading before the fallback, past the Lambda's 120 s timeout. At 3: the fallback answers in 5–26 s, and "
          "a short burst still recovers.", NOTE, 20, 470, 1340, 40)  # fmt: skip
    d.write(out / "article-6-figure-02.drawio", "Article 6: when the model fails", 1380, 520)


if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "output")
    figure1(out)
    figure2(out)
