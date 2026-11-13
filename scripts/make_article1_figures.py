"""Article 1's diagram (draw.io, AWS4 style):
1. the 2 a.m. report, end to end: the field report, Nova Lite reading it into required fields (where "unknown" is an
   answer), the rules engine deciding (missing facts to the worst case, open points to a person), and the decision
   packet the advisor approves. The model reads; the code decides.

Only Bedrock sits inside the AWS Cloud and Region groups: at article 1 the rules engine and the harness ran locally
against Bedrock, and nothing else was deployed for this step.

Usage (from the project root): python3 -I code/scripts/make_article1_figures.py output
Writes output/article-1-figure-01.drawio. PNG: export from draw.io at 200% (Border width 20, grid off), or with the
desktop app's CLI (from a Windows-aware shell):
    "/mnt/c/Program Files/draw.io/draw.io.exe" -x -f png -s 2 -b 20 -o <png> <drawio>
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))  # -I drops the script dir
from drawio_kit import AI, CENTER, CODE_FILL, CODE_STROKE, NOTE_FILL, TITLE, Diagram  # noqa: E402

CLOUD = "strokeColor=#232F3E;fillColor=none;fontColor=#232F3E;dashed=0;"
REGION = "strokeColor=#00A4A6;fillColor=none;fontColor=#147EBA;dashed=1;"
CODE = {"fill": CODE_FILL, "stroke": CODE_STROKE}
PERSON = {"fill": "#FFF4E5", "stroke": "#B35900"}
NOTE = "text;html=1;align=left;verticalAlign=top;fontSize=11;fontColor=#545B64;whiteSpace=wrap;"
LEFT = "align=left;spacingLeft=10;verticalAlign=middle;"


def figure1(out: pathlib.Path) -> None:
    d = Diagram()
    d.add("title", "<b>The 2 a.m. report, end to end</b><br>The model turns the report into facts; plain code decides, "
          "counts the deadline and lists what's missing; a person approves.", TITLE, 20, 10, 1340, 50)  # fmt: skip
    d.box("report", "<b>Field report</b>, 2:07 a.m.<br><br><i>Found product in the ditch past the station fence on "
          "my 01:40 round. Looks like crude, maybe 1.8 m3, hard to tell in the dark. Shut in the line. Not sure if it "
          "reached the creek.</i>", 20, 130, 220, 190, fill=NOTE_FILL, extra=LEFT)  # fmt: skip
    d.group("cloud", "AWS Cloud", "group_aws_cloud_alt", CLOUD, 270, 90, 250, 290)
    d.group("region", "Canada (Central) ca-central-1", "group_region", REGION, 285, 125, 220, 240)
    d.icon("bedrock", "Amazon Bedrock<br>Nova Lite, tagged profile<br>forced tool call", AI, "bedrock", 367, 175)
    d.add("schema", "Every deciding field is required, and \"unknown\" is an answer: a skipped field would read as "
          "\"no\".", NOTE, 300, 285, 190, 60)  # fmt: skip
    d.box("facts", "<b>Facts</b> (the model's only output)<br><br>release: yes, crude<br>volume: 1.8 m³, estimated<br>"
          "where: past the fence<br>discovered: 01:40<br>effect on the creek: <b>unknown</b>", 560, 130, 230, 190,
          **CODE, extra=LEFT)  # fmt: skip
    d.box("rules", "<b>Rules engine</b> (plain Python, no model)<br><br><b>Missing</b> fact: try every value, keep the "
          "answer that can't be wrong in the costly direction (PREC)<br><br><b>Open</b> point: 1.8 is within 25% of "
          "the 1.5 m³ line, so a person decides", 830, 130, 240, 190, **CODE, extra=LEFT)  # fmt: skip
    d.box("packet", "<b>Decision packet</b><br><br>precautionary (PREC)<br>due <b>04:40</b>, 3 h from discovery: past "
          "the fence (T3-LVP)<br>INC-d; INC-b at the worst reading<br>a person decides (U2-NEAR)<br>ask the field: "
          "effect on soil, water, wildlife?", 1110, 110, 250, 230, fill=NOTE_FILL, extra=LEFT)  # fmt: skip
    d.box("person", "<b>The on-call advisor</b> approves, edits or overrides, then phones and files. The system "
          "never files.", 1110, 380, 250, 80, **PERSON, extra=CENTER)  # fmt: skip
    d.edge("e1", "report", "bedrock", "text", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.edge("e2", "bedrock", "facts", "fields", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.edge("e3", "facts", "rules", "", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.edge("e4", "rules", "packet", "", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.edge("e5", "packet", "person", "", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    d.add("measured", "<b>Measured on test</b> (80 reports, 3 passes): facts read right 96.6%; missing facts found "
          "93.6%; packet ready in 1.0 s (p95); about $0.0002 a read. The rules engine agrees with the CER's own record "
          "on 98.8% of 1,952 incidents.", NOTE, 20, 420, 1060, 40)  # fmt: skip
    d.write(out / "article-1-figure-01.drawio", "Article 1: the 2 a.m. report, end to end", 1380, 480)


if __name__ == "__main__":
    figure1(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "output"))
