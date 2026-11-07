"""Article 2's diagrams (draw.io, AWS4 style):
1. where each check sits: the fixed workflow with the five checks overlaid;
2. the judge's layers: code checks on the rendered parts, Nova Lite on the narrative, the quote check;
3. replay in CI: live eval runs save the model's readings; every push re-scores them with the new code.

Usage (from the project root): python3 -I code/scripts/make_article2_figures.py output
Writes output/article-2-figure-0{1,2,3}.drawio. PNGs for the article: export each from draw.io at 200%, or with the
desktop app's CLI (from a Windows-aware shell):
    "/mnt/c/Program Files/draw.io/draw.io.exe" -x -f png -s 2 -o <png> <drawio>
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))  # -I drops the script dir
from drawio_kit import AI, CENTER, CHECK, CHECK_STROKE, CODE_FILL, CODE_STROKE, NOTE_FILL, TITLE, Diagram  # noqa: E402

CLOUD = "strokeColor=#232F3E;fillColor=none;fontColor=#232F3E;dashed=0;"
REGION = "strokeColor=#00A4A6;fillColor=none;fontColor=#147EBA;dashed=1;"
CODE = {"fill": CODE_FILL, "stroke": CODE_STROKE}
CHECK_EDGE = f"strokeColor={CHECK_STROKE};"
LANE = "text;html=1;align=left;verticalAlign=middle;fontSize=13;fontStyle=1;fontColor=#545B64;"


def figure1(out: pathlib.Path) -> None:
    d = Diagram()
    d.add("title", "<b>Where each check sits</b><br>The fixed workflow, with the checks the team keeps after handoff "
          "(blue).", TITLE, 20, 10, 1300, 50)  # fmt: skip
    # the system, left to right
    d.box("report", "<b>Field report</b><br>email, text, form", 40, 250, 130, 64, fill=NOTE_FILL, extra=CENTER)
    d.box("read", "<b>Read</b><br>three layouts, strictest answer", 210, 250, 170, 64, **CODE, extra=CENTER)
    d.box("rules", "<b>Rules engine</b><br>decides status, deadline, route", 420, 250, 180, 64, **CODE,
          extra=CENTER + "strokeWidth=2;")  # fmt: skip
    d.box("packet", "<b>Decision packet</b><br>with rule IDs and questions", 640, 250, 170, 64, fill=NOTE_FILL,
          extra=CENTER)  # fmt: skip
    d.box("draft", "<b>Draft notice</b><br>code renders the decision; model writes the narrative", 850, 250, 190, 64,
          **CODE, extra=CENTER)  # fmt: skip
    d.box("judge", "<b>Judge</b><br>code checks + model", 1080, 250, 140, 64, **CODE, extra=CENTER)
    d.res("approver", "Approver<br>nothing filed<br>without a person", "#232F3E", "user", 1270, 258, 48)
    for i, (a, b) in enumerate([("report", "read"), ("read", "rules"), ("rules", "packet"), ("packet", "draft"),
                                ("draft", "judge"), ("judge", "approver")]):  # fmt: skip
        d.edge(f"p{i}", a, b)
    # the checks
    d.box("testset", "<b>Test set</b>: 166 reports with known answers<br>dev 30 · test 80 · held-out 56 (untouched)",
          40, 90, 330, 64, fill=NOTE_FILL, extra=CENTER)  # fmt: skip
    d.box("oracle", "<b>1 Oracle</b><br>the rules engine on the answer key's facts: 166 / 166", 410, 90, 200, 64,
          extra=CHECK + CENTER)  # fmt: skip
    d.box("harness", "<b>2 Eval harness</b><br>every decision vs. the answer: missed, late, over-notify, route, "
          "missing facts; 3 passes", 640, 80, 290, 84, extra=CHECK + CENTER)  # fmt: skip
    d.box("measured", "<b>3 Measured judge</b><br>checked against 60 hand-labelled drafts: 4.9% of flawed drafts "
          "pass", 970, 90, 260, 64, extra=CHECK + CENTER)  # fmt: skip
    d.box("trace", "<b>5 Tracing</b>: a span per stage (time, tokens, cost), OpenTelemetry to traces.jsonl", 210,
          350, 1010, 34, extra=CHECK + CENTER + "dashed=1;")  # fmt: skip
    d.edge("t1", "testset", "oracle", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.edge("t2", "testset", "harness", extra="exitX=0.5;exitY=0;entryX=0.5;entryY=0;", points=[(205, 60), (785, 60)])
    d.edge("c1", "oracle", "rules", dashed=True, extra=CHECK_EDGE + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    d.edge("c2", "harness", "packet", dashed=True, extra=CHECK_EDGE + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;",
           points=[(725, 200)])  # fmt: skip
    d.edge("c3", "measured", "judge", dashed=True, extra=CHECK_EDGE + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    # where it runs
    d.group("cloud", "AWS Cloud", "group_aws_cloud_alt", CLOUD, 210, 430, 420, 190)
    d.group("region", "Canada (Central) ca-central-1", "group_region", REGION, 230, 470, 380, 135)
    d.icon("bedrock", "Amazon Bedrock: Nova Lite<br>tagged inference profile", AI, "bedrock", 470, 500, 56)
    calls = {"read": (295, 0.25), "draft": (945, 0.75), "judge": (1150, 0.75)}  # source x, entry point on Bedrock
    for i, (src, (x, entry)) in enumerate(calls.items()):  # through the clear strip above the AWS group
        d.edge(f"m{i}", src, "bedrock", "model calls" if src == "read" else "", dashed=True,
               extra=f"exitX=0.5;exitY=1;entryX={entry};entryY=0;",
               points=[(x, 410), (470 + 56 * entry, 410)])  # fmt: skip
    d.box("runs", "<b>Saved eval runs</b><br>the model's readings, kept from live runs (3 passes, priced first)", 700,
          450, 230, 70, fill=NOTE_FILL, extra=CENTER)  # fmt: skip
    d.box("gate", "<b>4 CI gate</b> (GitHub Actions, every push, $0)<br>re-scores the saved readings with the new "
          "code: oracle, targets, baseline. Fails the build if anything is worse.", 980, 450, 300, 90,
          extra=CHECK + CENTER)  # fmt: skip
    d.edge("g1", "runs", "gate", "replayed", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.write(out / "article-2-figure-01.drawio", "Article 2: where each check sits", 1360, 660)


def figure2(out: pathlib.Path) -> None:
    d = Diagram()
    d.add("title", "<b>The judge's layers</b><br>Code checks what code can check; the model reads only the narrative, "
          "and code verifies its quotes.", TITLE, 20, 10, 1200, 50)  # fmt: skip
    d.box("draft", "<b>Draft notice</b><br>for the approver", 40, 200, 160, 70, fill=NOTE_FILL, extra=CENTER)
    d.box("rendered", "<b>Parts rendered from the decision</b><br>deadline, reasons, precautionary wording, "
          "questions for the field", 260, 90, 250, 80, fill=NOTE_FILL, extra=CENTER)  # fmt: skip
    d.box("narrative", "<b>Narrative fields</b><br>what happened, actions taken, immediate concerns", 260, 300, 250,
          80, fill=NOTE_FILL, extra=CENTER)  # fmt: skip
    d.box("codechk", "<b>Code checks</b><br>compared with the decision exactly; no model, $0", 580, 90, 240, 80,
          extra=CHECK + CENTER)  # fmt: skip
    d.box("model", "<b>Model judge</b> (Nova Lite)<br>faithful to the report? clean (no names, phone numbers, "
          "instructions or rule claims)? Quotes the report's words for each statement", 580, 290, 240, 100, **CODE,
          extra=CENTER)  # fmt: skip
    d.box("quote", "<b>Quote check</b> (code)<br>are the quoted words really in the report?", 880, 300, 200, 80,
          extra=CHECK + CENTER)  # fmt: skip
    d.box("verdict", "<b>Verdict</b><br>pass, or flagged for a second look, with the reason", 1130, 195, 170, 80,
          fill=NOTE_FILL, extra=CENTER + "strokeWidth=2;")  # fmt: skip
    d.edge("e1", "draft", "rendered", extra="exitX=0.5;exitY=0;entryX=0;entryY=0.5;", points=[(120, 130)])
    d.edge("e2", "draft", "narrative", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;", points=[(120, 340)])
    d.edge("e3", "rendered", "codechk")
    d.edge("e4", "narrative", "model")
    d.edge("e5", "model", "quote")
    d.edge("e6", "codechk", "verdict", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;", points=[(1215, 130)])
    d.edge("e7", "quote", "verdict", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=1;", points=[(1215, 340)])
    d.group("cloud", "AWS Cloud", "group_aws_cloud_alt", CLOUD, 560, 420, 280, 170)
    d.group("region", "ca-central-1", "group_region", REGION, 575, 455, 250, 125)
    d.icon("bedrock", "Amazon Bedrock: Nova Lite", AI, "bedrock", 676, 490, 48)
    d.edge("m1", "model", "bedrock", dashed=True, extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    d.box("numbers", "<b>Measured on 40 hand-labelled drafts, 3 passes</b><br>Flawed drafts that pass: the model's "
          "own verdicts 77% → with the quote check 23% → with the code checks <b>4.9%</b> (target ≤ 5%).<br>Good "
          "drafts flagged: 8% → 51% → 51%. The quote check is the source of the flags.", 880, 440, 450, 90,
          fill=NOTE_FILL)  # fmt: skip
    d.write(out / "article-2-figure-02.drawio", "Article 2: the judge's layers", 1360, 610)


def figure3(out: pathlib.Path) -> None:
    d = Diagram()
    d.add("title", "<b>Replay in CI</b><br>Live runs save the model's readings; every push re-scores them with the new "
          "code, with no model calls.", TITLE, 20, 10, 1200, 50)  # fmt: skip
    d.add("lane1", "Live eval run: by hand, 3 passes, priced first", LANE, 40, 70, 600, 30)
    d.box("cases", "<b>Test set</b><br>166 reports with known answers", 40, 110, 180, 64, fill=NOTE_FILL,
          extra=CENTER)  # fmt: skip
    d.box("harness", "<b>Eval harness</b><br>runs each report through the system", 270, 110, 200, 64, **CODE,
          extra=CENTER)  # fmt: skip
    d.box("runs", "<b>Saved eval runs</b><br>the model's raw readings and scores, committed to the repo", 540, 110,
          280, 64, fill=NOTE_FILL, extra=CENTER)  # fmt: skip
    d.group("cloud", "AWS Cloud", "group_aws_cloud_alt", CLOUD, 250, 250, 240, 150)
    d.group("region", "ca-central-1", "group_region", REGION, 265, 285, 210, 110)
    d.icon("bedrock", "Amazon Bedrock: Nova Lite", AI, "bedrock", 346, 312, 48)
    d.edge("l1", "cases", "harness")
    d.edge("l2", "harness", "runs")
    d.edge("l3", "harness", "bedrock", "model calls", dashed=True, extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    d.add("lane2", "Every push: GitHub Actions, no model calls, $0", LANE, 40, 420, 600, 30)
    d.box("push", "<b>Push</b><br>a code, rules or prompt change", 40, 460, 180, 84, fill=NOTE_FILL, extra=CENTER)
    d.box("tests", "<b>Unit tests</b><br>lint, 112 tests", 270, 460, 200, 84, **CODE, extra=CENTER)
    d.box("gate", "<b>Eval gate</b><br>1 oracle: 166 / 166<br>2 strictest check meets the targets (dev, test)<br>"
          "3 no frozen run worse than the baseline", 540, 460, 280, 84, extra=CHECK + CENTER)  # fmt: skip
    d.box("baseline", "<b>Baseline</b><br>gate-baseline.json; changes only by an explicit command, in review", 880,
          290, 230, 70, fill=NOTE_FILL, extra=CENTER)  # fmt: skip
    d.box("result", "<b>Build passes, or fails</b><br>naming every count that got worse", 880, 460, 230, 84,
          fill=NOTE_FILL, extra=CENTER + "strokeWidth=2;")  # fmt: skip
    d.edge("p1", "push", "tests")
    d.edge("p2", "tests", "gate")
    d.edge("p3", "gate", "result")
    d.edge("r1", "runs", "gate", "replayed with the new code", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    d.edge("b1", "baseline", "gate", extra="exitX=0;exitY=0.5;entryX=0.75;entryY=0;", points=[(750, 325)])
    d.box("limit", "<b>The limit:</b> replay can't see the model change. A new model version needs a live run; a "
          "scheduled one comes with the production work (article 7).", 40, 580, 1070, 40, fill=NOTE_FILL,
          extra=CENTER + "dashed=1;")  # fmt: skip
    d.write(out / "article-2-figure-03.drawio", "Article 2: replay in CI", 1150, 640)


if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "output")
    figure1(out)
    figure2(out)
    figure3(out)
