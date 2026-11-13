"""Article 7's architecture diagram (draw.io, AWS4 style), figure 3: the gate at handoff, as deployed.

Left, the gate as it runs every day: outside a VPC, $0 while idle. Right, the VPC hardening window as it was actually
deployed and measured on 2026-11-11 (D55, D56): two private subnets in two AZs, the Bedrock runtime and SNS interface
endpoints, the DynamoDB gateway endpoint, no NAT or internet gateway. The VPC is drawn only because it existed, and
labelled as a window.

Usage (from the project root): python3 -I code/scripts/make_article7_figures.py output
Writes output/article-7-figure-03.drawio. PNG: export from draw.io at 200% (border 20, grid off), or
    "/mnt/c/Program Files/draw.io/draw.io.exe" -x -f png -s 2 -b 20 -o <png> <drawio>
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))  # -I drops the script dir
from drawio_kit import AI, APPINT, CENTER, COMPUTE, DATABASE, FINANCE, ICON, MGMT, NOTE_FILL, TITLE, Diagram  # noqa: E402

NETWORK = "#8C4FFF"
CLOUD = "strokeColor=#232F3E;fillColor=none;fontColor=#232F3E;dashed=0;"
REGION = "strokeColor=#00A4A6;fillColor=none;fontColor=#147EBA;dashed=1;"
VPC = "strokeColor=#8C4FFF;fillColor=none;fontColor=#232F3E;dashed=0;fontStyle=0;"
SUBNET = "grStroke=0;strokeColor=#00A4A6;fillColor=#E6F6F7;fontColor=#147EBA;dashed=0;fontStyle=0;"
PERSON = {"fill": "#FFF4E5", "stroke": "#B35900"}
LANE = "text;html=1;align=left;verticalAlign=top;fontSize=13;fontColor=#232F3E;whiteSpace=wrap;"
NOTE = "text;html=1;align=left;verticalAlign=top;fontSize=11;fontColor=#545B64;whiteSpace=wrap;"


def figure3(out: pathlib.Path) -> None:
    d = Diagram()
    d.add("title", "<b>The gate at handoff</b><br>Every day it runs outside a VPC and costs nothing while it waits. "
          "The VPC on the right existed for one measured window, then came down.", TITLE, 20, 10, 1360, 50)  # fmt: skip
    d.box("report", "<b>Field report</b><br>email, call note, scan", 20, 205, 170, 56, fill=NOTE_FILL, extra=CENTER)
    d.box("person", "<b>Approver</b><br>approve · edit · reject,<br>from the CLI", 20, 395, 170, 70, **PERSON,
          extra=CENTER)  # fmt: skip
    d.group("cloud", "AWS Cloud", "group_aws_cloud_alt", CLOUD, 220, 80, 1160, 680)
    d.group("region", "Canada (Central) ca-central-1", "group_region", REGION, 240, 115, 1120, 625)
    d.add("lane", "<b>Every day:</b> outside a VPC, $0 while idle", LANE, 270, 150, 460, 24)

    d.icon("sfn", "AWS Step Functions<br>one run per report;<br>waits days for a person", APPINT, "step_functions",
           300, 205)  # fmt: skip
    # The Lambda's label sits to its right, so the edges to the services below leave its bottom without crossing it.
    d.add("lambda", "<b>AWS Lambda</b><br>triage · park ·<br>escalate · close", ICON.format(fill=COMPUTE, icon="lambda")
          .replace("verticalLabelPosition=bottom;verticalAlign=top;align=center;",
                   "labelPosition=right;verticalLabelPosition=middle;align=left;verticalAlign=middle;spacingLeft=6;"),
          560, 205, 56, 56)  # fmt: skip
    d.icon("sns", "Amazon SNS<br>pages and alarms<br>by email", APPINT, "sns", 300, 402)
    d.icon("ddb", "Amazon DynamoDB<br>the case record<br>and review queue", DATABASE, "dynamodb", 470, 402)
    d.icon("bedrock", "Amazon Bedrock<br>Nova Lite (Canada), 2 guardrails;<br>fallback Haiku 4.5 (US regions)",
           AI, "bedrock", 660, 402)  # fmt: skip
    d.icon("cw", "Amazon CloudWatch<br>the function's logs and spans;<br>2 alarms (Overdue, Fallbacks)", MGMT,
           "cloudwatch_2", 300, 590)  # fmt: skip
    d.icon("budgets", "AWS Budgets<br>tagged, $50 and $75", FINANCE, "budgets_2", 560, 590)

    d.edge("e_rs", "report", "sfn", "submit", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.edge("e_sl", "sfn", "lambda", "each step", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.edge("e_ls", "lambda", "sns", "", dashed=True, extra="exitX=0.15;exitY=1;entryX=0.5;entryY=0;",
           points=[(568, 372), (328, 372)])  # fmt: skip
    d.edge("e_ld", "lambda", "ddb", "", dashed=True, extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;",
           points=[(588, 385), (498, 385)])  # fmt: skip
    d.edge("e_lb", "lambda", "bedrock", "", dashed=True, extra="exitX=0.85;exitY=1;entryX=0.5;entryY=0;",
           points=[(608, 385), (688, 385)])  # fmt: skip
    d.edge("e_sp", "sns", "person", "page", extra="exitX=0;exitY=0.5;entryX=1;entryY=0.5;")
    d.edge("e_ps", "person", "sfn", "decision", extra="exitX=0.5;exitY=0;entryX=0;entryY=0.9;",
           points=[(105, 330), (250, 330), (250, 255)])  # fmt: skip
    d.edge("e_cs", "cw", "sns", "alarm", extra="exitX=1;exitY=0.5;entryX=1;entryY=0.75;",
           points=[(430, 618), (430, 444)])  # fmt: skip

    # The hardening window, as deployed on 2026-11-11.
    d.group("vpc", "VPC: the hardening window only (measured 2026-11-11, then removed). No NAT or internet gateway.",
            "group_vpc2", VPC, 800, 150, 540, 510)  # fmt: skip
    for i, (x, az) in enumerate(((825, "a"), (1085, "b"))):
        d.group(f"sub{i}", f"Private subnet · AZ {az}", "group_security_group", SUBNET, x, 215, 230, 190)
        d.icon(f"eni{i}", "AWS Lambda<br>the same function's<br>network interface", COMPUTE, "lambda", x + 25,
               275, 48)  # fmt: skip
        d.res(f"ep{i}", "Interface endpoints<br>bedrock-runtime, sns", NETWORK, "endpoints", x + 145, 275)
        d.edge(f"e_ep{i}", f"eni{i}", f"ep{i}", "HTTPS", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.res("gwep", "Gateway endpoint<br>DynamoDB (free)", NETWORK, "endpoints", 850, 440)
    d.add("routes", "Route table: no default route, so the function can reach only Bedrock, SNS and DynamoDB, "
          "whatever text a report carries.", NOTE, 930, 445, 380, 40)  # fmt: skip
    d.add("vpcnote", "<b>Measured:</b> triage 2.5–2.9 s, as outside. 2 endpoints × 2 AZs = $0.044 an hour, about "
          "$32 a month if kept: the operator's security call.<br><b>Down:</b> take the function out with the CLI "
          "and check it left, then delete the network.", NOTE, 825, 545, 500, 80)  # fmt: skip
    d.edge("e_win", "lambda", "vpc", "during the window, the same function moves here", dashed=True,
           extra="exitX=0.5;exitY=0;entryX=0;entryY=0.08;", points=[(588, 190)])  # fmt: skip
    d.write(out / "article-7-figure-03.drawio", "Article 7: the gate at handoff", 1400, 780)


if __name__ == "__main__":
    figure3(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "output"))
