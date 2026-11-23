"""The how-to piece's diagram (draw.io, AWS4 style):
2. the pattern: the model reads, code decides, the model drafts, a person approves and files; with the release
   checks every build passes underneath.

Usage (from the project root): python3 -I code/scripts/make_howto_figures.py output
Writes output/howto-figure-02.drawio. PNG: export from draw.io at 200% (Border width 20, grid off), or with the
desktop app's CLI (from a Windows-aware shell):
    "/mnt/c/Program Files/draw.io/draw.io.exe" -x -f png -s 2 -b 20 -o <png> <drawio>
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))  # -I drops the script dir
from drawio_kit import (  # noqa: E402
    AI,
    APPINT,
    CENTER,
    CHECK,
    CODE_FILL,
    CODE_STROKE,
    COMPUTE,
    NOTE_FILL,
    TITLE,
    Diagram,
)  # fmt: skip

CLOUD = "strokeColor=#232F3E;fillColor=none;fontColor=#232F3E;dashed=0;"
REGION = "strokeColor=#00A4A6;fillColor=none;fontColor=#147EBA;dashed=1;"
CODE = {"fill": CODE_FILL, "stroke": CODE_STROKE}
MODEL = {"fill": "#E6F6F7", "stroke": "#01A88D"}  # the model's steps: AI/ML teal
PERSON = {"fill": "#FFF4E5", "stroke": "#B35900"}
LANE = "text;html=1;align=left;verticalAlign=middle;fontSize=12;fontColor=#232F3E;whiteSpace=wrap;"
SIDE = "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"


def figure2(out: pathlib.Path) -> None:
    d = Diagram()
    d.add("title", "<b>The model reads, code decides, a person approves</b><br>The model never makes the decision, "
          "so text in a report has nothing to move. Every build has to prove it before it ships.", TITLE,
          20, 10, 1610, 50)  # fmt: skip
    d.box("report", "<b>Field report</b><br>untrusted text: email,<br>call note, scan", 20, 215, 170, 80,
          fill=NOTE_FILL, extra=CENTER)  # fmt: skip
    d.group("cloud", "AWS Cloud", "group_aws_cloud_alt", CLOUD, 240, 80, 950, 350)
    d.group("region", "Canada (Central) ca-central-1", "group_region", REGION, 260, 115, 910, 300)
    d.icon("sfn", "", APPINT, "step_functions", 290, 150, 36)
    d.add("sfn_t", "<b>AWS Step Functions</b>: one run per report; waits for the approver at $0 and escalates on "
          "the reporting clock", LANE, 336, 150, 780, 36)  # fmt: skip
    d.box("reads", "<b>1 · The model reads</b><br>Nova Lite pulls the facts out<br>in a fixed form. A guardrail<br>"
          "flags suspected attacks;<br>it never edits the input.", 290, 200, 240, 110, **MODEL,
          extra=CENTER)  # fmt: skip
    d.box("decides", "<b>2 · Code decides</b><br>The rules engine:<br>status, clause, deadline.<br>0.2 ms, no model.",
          600, 200, 240, 110, **CODE, extra=CENTER + "strokeWidth=2;")  # fmt: skip
    d.box("drafts", "<b>3 · The model drafts</b><br>Nova Lite writes the notice<br>from the decision. The guardrail"
          "<br>masks personal details<br>in the draft only.", 910, 200, 240, 110, **MODEL, extra=CENTER)  # fmt: skip
    d.icon("bedrock1", "Amazon Bedrock", AI, "bedrock", 386, 330, 48)
    d.icon("lambda", "AWS Lambda", COMPUTE, "lambda", 696, 330, 48)
    d.icon("bedrock2", "Amazon Bedrock", AI, "bedrock", 1006, 330, 48)
    d.box("person", "<b>4 · A person approves</b><br>a named approver:<br>approve, edit or reject,<br>with a reason",
          1250, 200, 170, 110, **PERSON, extra=CENTER)  # fmt: skip
    d.box("cer", "<b>CER</b><br>filed by the person, never by the system", 1490, 205, 140, 100, fill=NOTE_FILL,
          extra=CENTER)  # fmt: skip
    d.edge("e1", "report", "reads", "text", extra=SIDE)
    d.edge("e2", "reads", "decides", "facts", extra=SIDE)
    d.edge("e3", "decides", "drafts", "decision", extra=SIDE)
    d.edge("e4", "drafts", "person", "draft", extra=SIDE)
    d.edge("e5", "person", "cer", "files", extra=SIDE)
    d.box("checks", "<b>Before every release</b> (CI, $0, no model calls): the eval gate on 175 labelled reports, "
          "0 missed and 0 late to ship · the attack check: every attack report keeps its clean answer, "
          "135 results, 0 decisions moved", 20, 460, 1610, 50, extra=CHECK + CENTER)  # fmt: skip
    d.write(out / "howto-figure-02.drawio", "How-to: the pattern", 1650, 530)


if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "output")
    figure2(out)
