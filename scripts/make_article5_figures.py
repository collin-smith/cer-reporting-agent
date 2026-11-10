"""Article 5's diagrams (draw.io, AWS4 style):
1. where the MCP server runs: today a local process over stdio, calling Nova Lite on Bedrock in Canada; next (stage 6,
   not built) a hosted endpoint, AgentCore Gateway in front of a Lambda in a VPC, reaching Bedrock through an
   interface endpoint.
3. two clients, one server: Claude Code on the public tools, our reviewing agent on the review tools. The order each
   model sees, and what an error looks like on the client's side.

Figure 2 is a chart: code/scripts/chart_article5.py.

Usage (from the project root): python3 -I code/scripts/make_article5_figures.py output
Writes output/article-5-figure-0{1,3}.drawio. PNGs: export each from draw.io at 200%, or with the desktop app's CLI
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
    COMPUTE,
    ESC_STROKE,
    NOTE_FILL,
    TITLE,
    Diagram,
)  # fmt: skip

CLOUD = "strokeColor=#232F3E;fillColor=none;fontColor=#232F3E;dashed=0;"
REGION = "strokeColor=#00A4A6;fillColor=none;fontColor=#147EBA;dashed=1;"
VPC = "strokeColor=#8C4FFF;fillColor=none;fontColor=#232F3E;dashed=0;fontStyle=0;"
SUBNET = "strokeColor=#00A4A6;fillColor=#E6F6F7;fontColor=#147EBA;dashed=0;fontStyle=0;"
LOCAL = "rounded=1;arcSize=3;dashed=1;fillColor=none;strokeColor=#545B64;fontColor=#232F3E;fontStyle=1;fontSize=12;" \
        "verticalAlign=top;align=left;spacingLeft=10;spacingTop=4;html=1;whiteSpace=wrap;"  # fmt: skip
NETWORK, SECURITY = "#8C4FFF", "#DD344C"
CODE = {"fill": CODE_FILL, "stroke": CODE_STROKE}
AGENT = {"fill": AGENT_FILL, "stroke": AGENT_STROKE}
LANE = "text;html=1;align=left;verticalAlign=top;fontSize=13;fontColor=#232F3E;whiteSpace=wrap;"
NOTE = "text;html=1;align=left;verticalAlign=top;fontSize=11;fontColor=#545B64;whiteSpace=wrap;"
NEXT = "dashed=1;strokeColor=#8C4FFF;"
GOOD, BAD = "#1D8102", ESC_STROKE


def figure1(out: pathlib.Path) -> None:
    d = Diagram()
    d.add("title", "<b>Where the MCP server runs</b><br>Today a local process that a client starts over stdio; the "
          "only cloud call is the model. Next, a hosted endpoint inside a VPC (stage 6, not built).", TITLE, 20, 10,
          1340, 50)  # fmt: skip
    # --- now: local ---
    d.add("now", "<b>Now</b>: measured on dev (D47)", LANE, 20, 75, 400, 24)
    d.add("local", "Your machine (local, no hosting cost)", LOCAL, 20, 105, 860, 330)
    d.box("cc", "<b>Claude Code</b><br>any MCP client; reads .mcp.json, starts the server", 40, 150, 190, 60,
          fill=NOTE_FILL, extra=CENTER)  # fmt: skip
    d.box("ours", "<b>Our eval client</b> (mcp_client.py)<br>strict check, and the reviewing agent (Strands on "
          "Nova Lite)", 40, 300, 190, 74, **AGENT, extra=CENTER)  # fmt: skip
    d.box("server", "<b>MCP server</b>: cer_agent.mcp_server, one process per client<br>public tools: triage_report "
          "· decide · rule_text · draft_notice<br>--review adds: read_report · open_case · patch_facts · "
          "confirm_missing · finish · case_result", 300, 140, 560, 76, **CODE, extra="strokeWidth=2;")  # fmt: skip
    d.edge("e1", "cc", "server", "stdio")
    d.edge("e2", "ours", "server", "stdio, --review", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.75;",
           points=[(265, 337), (265, 197)])  # fmt: skip
    for i, (key, label) in enumerate([
        ("reader", "<b>Reader</b><br>3 layouts, strictest answer"),
        ("rules", "<b>Rules engine</b><br>decides; $0"),
        ("spec", "<b>Rules spec</b><br>rules-spec.md; $0"),
        ("drafter", "<b>Drafter</b><br>a notice for a person"),
    ]):  # fmt: skip
        d.box(key, label, 300 + i * 145, 270, 125, 54, **CODE, extra=CENTER)
        d.edge(f"s{key}", "server", key, dashed=True, extra="endArrow=none;exitY=1;entryY=0;")
    d.add("same", "The same Python the workflow and the in-process agent run. The rules engine decides every "
          "packet; a model only reads and drafts.", NOTE, 300, 340, 560, 34)  # fmt: skip
    d.add("cost", "Added time: a median 4.9 ms a report (strict check) and 31 ms a case (agent), plus a ~10 s start "
          "once per run.", NOTE, 300, 380, 560, 34)  # fmt: skip
    # cloud, now
    d.group("cloud", "AWS Cloud", "group_aws_cloud_alt", CLOUD, 920, 105, 440, 330)
    d.group("region", "Canada (Central) ca-central-1", "group_region", REGION, 940, 145, 400, 270)
    d.icon("bedrock", "Amazon Bedrock: Nova Lite<br>tagged inference profile", AI, "bedrock", 1050, 215, 56)
    d.icon("iam", "IAM: the caller's<br>own credentials", SECURITY, "identity_and_access_management", 1210, 215, 56)
    d.add("pub", "Public Bedrock endpoint over HTTPS, signed with the caller's credentials. Cost tagged to the "
          "series.", NOTE, 960, 325, 360, 40)  # fmt: skip
    d.edge("e3", "server", "bedrock", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;",
           points=[(900, 178), (900, 243)])  # fmt: skip
    d.add("e3label", "InvokeModel<br>(Reader, Drafter)", "text;html=1;align=center;fontSize=10;fontColor=#232F3E;",
          945, 205, 100, 30)  # fmt: skip
    # --- next: hosted ---
    d.add("next", "<b>Next</b>: stage 6 hardening, priced before it runs; not built", LANE, 20, 490, 600, 24)
    d.box("client2", "<b>Any MCP client</b><br>Claude Code, a team's agent<br>(Streamable HTTP)", 40, 600, 190, 70,
          fill=NOTE_FILL, extra=CENTER)  # fmt: skip
    d.group("cloud2", "AWS Cloud", "group_aws_cloud_alt", CLOUD, 270, 520, 1090, 300)
    d.group("region2", "Canada (Central) ca-central-1", "group_region", REGION, 290, 555, 1050, 250)
    d.icon("gw", "AgentCore Gateway<br>MCP endpoint, OAuth in", AI, "bedrock_agentcore", 340, 600, 56)
    d.group("vpc", "VPC", "group_vpc2", VPC, 520, 580, 560, 210)
    d.group("subnet", "Private subnet, 1 AZ, no NAT", "group_security_group", SUBNET, 545, 615, 510, 160)
    d.icon("lambda", "Lambda: the same<br>MCP tools", COMPUTE, "lambda", 600, 655, 56)
    d.res("vpce", "Interface endpoints<br>bedrock-runtime, logs", NETWORK, "endpoints", 880, 659, 48)
    d.icon("bedrock2", "Bedrock: Nova Lite<br>tagged profile", AI, "bedrock", 1180, 655, 56)
    d.edge("n1", "client2", "gw", "HTTPS", extra=NEXT)
    d.edge("n2", "gw", "lambda", "invoke", extra=NEXT)
    d.edge("n3", "lambda", "vpce", extra=NEXT)
    d.edge("n4", "vpce", "bedrock2", "PrivateLink", extra=NEXT)
    d.add("nextnote", "Same tools, same order, same errors; the transport changes. Torn down the same day it's "
          "measured (nuke.sh --check).", NOTE, 40, 690, 210, 70)  # fmt: skip
    # legend
    d.box("lg1", "our Python code", 20, 840, 130, 30, **CODE, extra=CENTER)
    d.box("lg2", "a model chooses the next step", 170, 840, 200, 30, **AGENT, extra=CENTER)
    d.add("lg3", "Dashed purple: the next step, not built.", NOTE, 390, 846, 400, 24)
    d.write(out / "article-5-figure-01.drawio", "Article 5: where the MCP server runs", 1380, 890)


def tools(d: Diagram, prefix: str, names: list[tuple[str, str]], x: int, y: int, w: int) -> None:
    """A tool list as the model sees it, top to bottom: one row per tool, numbered."""
    for i, (name, note) in enumerate(names):
        stroke = AGENT_STROKE if prefix != "cc" else CODE_STROKE
        d.box(f"{prefix}{i}", f"<b>{i + 1}. {name}</b>  {note}", x, y + i * 34, w, 28, fill="#FFFFFF",
              stroke=stroke, extra="verticalAlign=middle;spacingTop=0;")  # fmt: skip


def figure3(out: pathlib.Path) -> None:
    d = Diagram()
    d.add("title", "<b>Two clients, one server</b><br>Each client gets the tools its job needs, in the server's "
          "order. The words are the same as in-process; the order and the errors were the parts that moved.",
          TITLE, 20, 10, 1300, 50)  # fmt: skip
    d.box("server", "<b>MCP server</b><br>one copy of the tool code (the <i>Case</i> methods); the in-process agent "
          "and the server take the same descriptions", 470, 90, 380, 64, **CODE,
          extra=CENTER + "strokeWidth=2;")  # fmt: skip
    # Claude Code, public scope
    d.box("cc", "<b>Claude Code</b> (public scope)<br>a person asks; Claude picks the tools", 20, 200, 400, 50,
          fill=NOTE_FILL, extra=CENTER)  # fmt: skip
    tools(d, "cc", [("triage_report", "the strict check, Nova Lite"), ("decide", "rules only, $0"),
                    ("rule_text", "one rule's text, $0"), ("draft_notice", "for a person to approve")], 20, 270,
          400)  # fmt: skip
    d.edge("e1", "server", "cc", "4 public tools", extra="exitX=0.2;exitY=1;entryX=0.5;entryY=0;")
    # our agent, review scope
    d.box("ag", "<b>Our reviewing agent</b> (--review scope)<br>the client code runs the case; the model sees 4 "
          "tools", 900, 200, 400, 50, **AGENT, extra=CENTER)  # fmt: skip
    tools(d, "ag", [("rule_text", ""), ("patch_facts", "stricter only (D38)"), ("confirm_missing", ""),
                    ("finish", "")], 900, 270, 195)  # fmt: skip
    d.add("aghead", "<b>Server order</b> (kept for MCP, D48)<br>0.16 no-op patches a case", NOTE, 900, 410, 195, 40)
    for i, name in enumerate(["patch_facts", "confirm_missing", "rule_text", "finish"]):
        d.box(f"ip{i}", f"<b>{i + 1}. {name}</b>", 1105, 270 + i * 34, 195, 28, fill="#FFFFFF", stroke="#B9B8B3",
              extra="verticalAlign=middle;spacingTop=0;fontColor=#545B64;")  # fmt: skip
    d.add("iphead", "<b>In-process order</b> (articles 2–3)<br>0.88 no-op patches a case", NOTE, 1105, 410, 195, 40)
    d.add("drv", "Called by the client code, not the model: read_report · open_case · case_result", NOTE, 900, 455,
          400, 24)  # fmt: skip
    d.edge("e2", "server", "ag", "10 review tools", extra="exitX=0.8;exitY=1;entryX=0.5;entryY=0;")
    d.add("order", "Same answers either way (91 of 99 right, 3 missed, both). The order changed how often the model "
          "re-sent a value already recorded.", NOTE, 470, 300, 380, 50)  # fmt: skip
    # errors across the wire
    d.add("errhead", "<b>What a client sees when a call is wrong</b>: decide({\"lands\": \"farm\"})", LANE, 20, 490,
          900, 24)  # fmt: skip
    d.box("err1", "<b>Ordinary exception</b> (the SDK keeps its text on the server)<br>client gets: <i>Error "
          "executing tool decide</i><br>a model can't tell what to fix", 20, 522, 420, 60, fill="#FCEBEC", stroke=BAD,
          extra="strokeWidth=2;")  # fmt: skip
    d.box("err2", "<b>ToolError</b> (what the server raises)<br>client gets: <i>lands must be a list. Example: "
          "{\"lands\": [\"company_property\"]}.</i><br>the D38 helpful errors survive the transport", 470, 522, 450,
          60, fill="#FFFFFF", stroke=GOOD, extra="strokeWidth=2;")  # fmt: skip
    d.add("errnote", "Found by a test before any spend: every deliberate error is now a ToolError.", NOTE, 20, 590,
          900, 24)  # fmt: skip
    d.write(out / "article-5-figure-03.drawio", "Article 5: two clients, one server", 1320, 625)


if __name__ == "__main__":
    o = pathlib.Path(sys.argv[1])
    figure1(o)
    figure3(o)
