# ruff: noqa: E501  (embedded HTML/CSS template)
"""Write the judge-calibration review sheet (D35) as one self-contained HTML page for Collin.

Groups the 60 drafts by how closely to read them (1: meant to pass, 2: real flaws, 3: planted flaws), shows each
field report beside its draft, highlights the lines Nova wrote (PIR-5 to PIR-13) and, for planted flaws, the exact
line changed. Agree / disagree and notes are kept in the browser (localStorage); "Copy my disagreements" gives the
text to paste back. $0, no AI.

Usage (from code/):  PYTHONPATH=src python scripts/review_html.py   -> output/judge-calibration-review.html
"""

from __future__ import annotations

import glob
import html
import json
import pathlib
import re

CODE = pathlib.Path(__file__).resolve().parents[1]
CASES = {c["id"]: c for c in map(json.loads, (CODE / "evals/cases/cases.jsonl").read_text("utf-8").splitlines())}
# Worth a closer look, with the reason shown on the card (read 2026-11-05).
ATTENTION = {
    "CL-021": "PIR-7 says 'potential gas release'; the report confirms an open vent and a gas smell. Fair, or overstated?",
    "CL-051": "PIR-8 copies the report almost word for word, including the 'skip checks' jumper. Fine for a notice?",
    "CL-029": "PIR-8 'everything remained inside the pipe' for 'everything stayed inside pipe'. Faithful?",
    "AD-149": "PIR-8 'severe leg injury' for 'leg's busted bad - femur'. Fair?",
    "AD-156": "PIR-10 gives the operator's name as the facility. Acceptable, or should it be 'not stated'?",
    "JU-099": "PIR-10 gives the operator's name as the facility. Acceptable, or should it be 'not stated'?",
    "JU-119": "PIR-9 'Patrol team headed to the site' is the only action. Fine?",
    "JU-096": "Subtle: 'released at a rate of 3.0 m³'. Would you reject a draft for calling a volume a rate?",
    "CL-046": "Subtle: who called whom is reversed. Would you reject the draft for it?",
    "CL-030": "'Scheduled patrol' when the supervisor 'just got to site'. Clear invention, or fair reading?",
    "JU-144": "Policy: is leaving out 'taken at the stricter reading' a fault you'd reject a draft for?",
    "JU-142": "Policy: is leaving out 'taken at the stricter reading' a fault you'd reject a draft for?",
}
OUT = CODE.parent / "output/judge-calibration-review.html"
NOVA_LINE = re.compile(r"^\*\*PIR-(?:[5-9]|1[0-3]) ")

GROUPS = {
    1: ("Read carefully", "Meant to pass", "Read every highlighted (Nova-written) line against the report. Pass only "
        "if every statement is in the report, nothing is invented or overstated, and no person is named."),
    2: ("Check the fault", "Real faults", "Nova really made these. Is the fault in the note real, and would you "
        "reject or edit the draft for it?"),
    3: ("Skim", "Planted faults", "Code made one edit (highlighted in red). Confirm it's a real error. Everything "
        "else in the draft is Nova's unread output, so you may spot a second fault: that only adds to the fail."),
}  # fmt: skip


def group(it: dict) -> int:
    return 1 if it["intended"] == "pass" else 2 if it["source"].startswith("real") else 3


def base_texts() -> dict[str, str]:
    """The unedited drafts, so a planted edit can be shown as the changed lines."""
    out = {}
    for path in [*glob.glob(str(CODE / "evals/drafts/20261105-161234-*/drafts.jsonl")),
                 str(CODE / "evals/drafts/test-strict-replay-rep1/drafts.jsonl")]:  # fmt: skip
        for d in map(json.loads, pathlib.Path(path).read_text("utf-8").splitlines()):
            out[d["id"]] = d["text"]
    return out


def inline(s: str) -> str:
    s = html.escape(s)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)


def render_draft(text: str, changed: set[str]) -> str:
    rows = []
    for ln in text.strip().splitlines():
        cls = ["ln"]
        if ln in changed:
            cls.append("planted")
        elif NOVA_LINE.match(ln):
            cls.append("nova")
        if ln.startswith("# "):
            rows.append(f'<div class="{" ".join(cls)} h">{inline(ln[2:])}</div>')
        elif ln.startswith("> "):
            rows.append(f'<div class="{" ".join(cls)} warn">{inline(ln[2:])}</div>')
        elif ln.startswith("- "):
            rows.append(f'<div class="{" ".join(cls)} li">• {inline(ln[2:])}</div>')
        elif ln.strip():
            rows.append(f'<div class="{" ".join(cls)}">{inline(ln)}</div>')
        else:
            rows.append('<div class="gap"></div>')
    return "\n".join(rows)


def card(it: dict, base: dict[str, str]) -> str:
    g = group(it)
    changed = set()
    if g == 3 and it["case_id"] in base:
        before = set(base[it["case_id"]].splitlines())
        changed = {ln for ln in it["draft"].splitlines() if ln not in before}
        removed = [ln for ln in base[it["case_id"]].splitlines() if ln not in set(it["draft"].splitlines())]
    else:
        removed = []
    pk = it["packet"]
    key = CASES[it["case_id"]]["expected"]
    flags = []
    if (pk["status"], pk["deadline"]) != (key["status"], key["deadline"]):
        flags.append(
            f'<p class="flag key">The decision here differs from the answer key ({key["status"]}, '
            f"{key['deadline'] or 'no deadline'}): the decision engine got this case wrong. <b>Judge the "
            f"draft against the decision shown</b>, not whether the decision is right.</p>"
        )
    if it["case_id"] in ATTENTION:
        flags.append(f'<p class="flag look"><b>Worth a closer look:</b> {inline(ATTENTION[it["case_id"]])}</p>')
    removed_html = "".join(f'<div class="ln removed">Removed: {inline(ln)}</div>' for ln in removed
                           if ln.strip() and ln not in changed)  # fmt: skip
    crit = ", ".join(it["criteria"]) or "none"
    return f"""
<section class="card g{g}" id="{it["cal_id"]}" data-group="{g}" data-id="{it["cal_id"]}" data-look="{int(it["case_id"] in ATTENTION)}">
  <header>
    <span class="id">{it["cal_id"]}</span>
    <span class="tag g{g}">{GROUPS[g][0]}</span>
    <span class="tag {it["intended"]}">Intended: {it["intended"].upper()}</span>
    <span class="meta">criterion: {html.escape(crit)} · case {it["case_id"]} · {it["set"]} set · {html.escape(it["source"])}</span>
  </header>
  {"".join(flags)}
  <p class="why"><b>Why this label:</b> {inline(it["note"])}</p>
  <p class="decision"><b>Decision (from code):</b> {pk["status"]}, {pk["deadline"] or "no deadline"}, route
     {pk["route"]}, missing: {", ".join(pk["missing"]) or "none"}</p>
  <div class="cols">
    <div class="col"><h4>Field report</h4><pre>{html.escape(it["report"].strip())}</pre></div>
    <div class="col"><h4>Draft notice</h4>{render_draft(it["draft"], changed)}{removed_html}</div>
  </div>
  <footer>
    <span>Would you approve this draft as written?</span>
    <button class="agree">Agree with the label</button>
    <button class="disagree">Disagree</button>
    <input class="note" placeholder="Why you disagree (a few words)">
  </footer>
</section>"""  # fmt: skip


def main() -> int:
    items = [json.loads(ln) for ln in (CODE / "evals/judge/calibration.jsonl").read_text("utf-8").splitlines()]
    items.sort(key=lambda it: (group(it), it["cal_id"]))
    base = base_texts()
    counts = {g: sum(group(it) == g for it in items) for g in GROUPS}
    tabs = "".join(f'<button class="tab" data-g="{g}">{g}. {GROUPS[g][1]} <small>({counts[g]}) · {GROUPS[g][0]}'
                   f"</small></button>" for g in GROUPS)  # fmt: skip
    guides = "".join(f'<div class="guide" data-g="{g}"><b>{g}. {GROUPS[g][1]}: {GROUPS[g][0].lower()}.</b> '
                     f"{GROUPS[g][2]}</div>" for g in GROUPS)  # fmt: skip
    page = TEMPLATE.replace("{{TABS}}", tabs).replace("{{GUIDES}}", guides).replace(
        "{{CARDS}}", "\n".join(card(it, base) for it in items)).replace("{{N}}", str(len(items)))  # fmt: skip
    OUT.write_text(page, encoding="utf-8")
    print(f"{len(items)} drafts -> {OUT}")
    return 0


TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Judge calibration review (D35)</title>
<style>
:root { --ink:#1d2433; --muted:#5b6475; --line:#d9dee7; --bg:#f6f7f9; --nova:#fff6d6; --planted:#ffe0e0;
        --pass:#1a7f4b; --fail:#b42318; --g1:#1f5fbf; --g2:#9a5b00; --g3:#5b6475; }
* { box-sizing: border-box; }
body { margin:0; font: 15px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; color:var(--ink); background:var(--bg); }
.top { position:sticky; top:0; z-index:5; background:#fff; border-bottom:1px solid var(--line); padding:12px 24px; }
h1 { font-size:20px; margin:0 0 4px; }
.lead { color:var(--muted); margin:0 0 10px; max-width:1100px; }
.tabs { display:flex; gap:8px; flex-wrap:wrap; align-items:center; }
.tab { border:1px solid var(--line); background:#fff; border-radius:8px; padding:6px 12px; cursor:pointer; font:inherit; }
.tab.on { background:var(--ink); color:#fff; border-color:var(--ink); }
.tab small { opacity:.75; }
.progress { margin-left:auto; color:var(--muted); }
.copy { border:0; background:var(--g1); color:#fff; border-radius:8px; padding:7px 14px; cursor:pointer; font:inherit; }
.legend { margin-top:8px; color:var(--muted); font-size:13px; }
.legend span { padding:1px 6px; border-radius:4px; }
main { padding:16px 24px 80px; max-width:1400px; }
.guide { display:none; background:#fff; border:1px solid var(--line); border-left:4px solid var(--g1);
         border-radius:8px; padding:10px 14px; margin-bottom:14px; }
.guide.on { display:block; }
.card { background:#fff; border:1px solid var(--line); border-radius:10px; margin:0 0 18px; padding:14px 16px; }
.card.hidden { display:none; }
.card.done-agree { border-left:6px solid var(--pass); }
.card.done-disagree { border-left:6px solid var(--fail); }
header { display:flex; flex-wrap:wrap; gap:8px; align-items:center; }
.id { font-weight:700; font-size:17px; }
.tag { font-size:12px; font-weight:600; padding:2px 8px; border-radius:999px; border:1px solid currentColor; }
.tag.g1 { color:var(--g1); } .tag.g2 { color:var(--g2); } .tag.g3 { color:var(--g3); }
.tag.pass { color:var(--pass); } .tag.fail { color:var(--fail); }
.meta { color:var(--muted); font-size:13px; }
.why, .decision { margin:8px 0 0; }
.flag { margin:8px 0 0; padding:6px 10px; border-radius:6px; }
.flag.key { background:#eef3ff; border-left:4px solid var(--g1); }
.flag.look { background:#fff1c2; border-left:4px solid var(--g2); }
.cols { display:grid; grid-template-columns: 1fr 1.25fr; gap:16px; margin-top:12px; }
@media (max-width: 1000px) { .cols { grid-template-columns: 1fr; } }
h4 { margin:0 0 6px; font-size:13px; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); }
pre { white-space:pre-wrap; font: 14px/1.5 ui-monospace, Consolas, monospace; background:var(--bg);
      border:1px solid var(--line); border-radius:8px; padding:10px; margin:0; }
.ln { padding:1px 6px; border-radius:4px; }
.ln.h { font-weight:700; }
.ln.li { padding-left:14px; }
.ln.warn { background:#fff1c2; }
.ln.nova { background:var(--nova); }
.ln.planted, .ln.removed { background:var(--planted); }
.ln.removed { text-decoration: line-through; color:var(--fail); }
.gap { height:8px; }
footer { display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin-top:12px; padding-top:10px;
         border-top:1px solid var(--line); }
footer span { color:var(--muted); margin-right:4px; }
footer button { border:1px solid var(--line); background:#fff; border-radius:8px; padding:6px 12px; cursor:pointer; font:inherit; }
footer button.agree.on { background:var(--pass); color:#fff; border-color:var(--pass); }
footer button.disagree.on { background:var(--fail); color:#fff; border-color:var(--fail); }
.note { flex:1; min-width:240px; font:inherit; padding:6px 10px; border:1px solid var(--line); border-radius:8px; display:none; }
.card.done-disagree .note { display:block; }
#out { display:none; position:fixed; inset:auto 24px 24px auto; width:min(560px, 90vw); background:#fff;
       border:1px solid var(--line); border-radius:10px; padding:12px; box-shadow:0 8px 30px rgba(0,0,0,.15); z-index:9; }
#out textarea { width:100%; height:180px; font: 13px ui-monospace, Consolas, monospace; }
</style></head><body>
<div class="top">
  <h1>Judge calibration review: {{N}} drafts</h1>
  <p class="lead">For each draft ask one question: <b>would you approve it as written?</b> Click <i>Agree</i> if
  that matches the intended label, <i>Disagree</i> (with a few words) if not. Your answers are saved in this
  browser. When done, click <b>Copy my disagreements</b> and paste the text into the chat. Anything not marked
  counts as agreed.</p>
  <div class="tabs">{{TABS}}<button class="tab" data-g="look">⚑ Closer look</button><button class="tab" data-g="all">All</button>
    <span class="progress" id="progress"></span><button class="copy" id="copy">Copy my disagreements</button></div>
  <div class="legend"><span style="background:var(--nova)">yellow</span> = written by Nova from the report (where
  faults hide) · <span style="background:var(--planted)">red</span> = the planted edit · everything else is
  written by code from the decision.</div>
</div>
<main>{{GUIDES}}{{CARDS}}</main>
<div id="out"><b>Paste this into the chat:</b><textarea id="outtext" readonly></textarea>
  <button id="close">Close</button></div>
<script>
const KEY = "cer-judge-calibration-review-v1";
const state = JSON.parse(localStorage.getItem(KEY) || "{}");
const save = () => localStorage.setItem(KEY, JSON.stringify(state));
const cards = [...document.querySelectorAll(".card")];
function paint(card) {
  const s = state[card.dataset.id] || {};
  card.classList.toggle("done-agree", s.v === "agree");
  card.classList.toggle("done-disagree", s.v === "disagree");
  card.querySelector(".agree").classList.toggle("on", s.v === "agree");
  card.querySelector(".disagree").classList.toggle("on", s.v === "disagree");
  card.querySelector(".note").value = s.note || "";
}
function progress() {
  const done = cards.filter(c => state[c.dataset.id]?.v).length;
  const dis = cards.filter(c => state[c.dataset.id]?.v === "disagree").length;
  document.getElementById("progress").textContent = `${done} of ${cards.length} reviewed · ${dis} disagreements`;
}
cards.forEach(card => {
  const id = card.dataset.id;
  card.querySelector(".agree").onclick = () => { state[id] = { v: "agree" }; save(); paint(card); progress(); };
  card.querySelector(".disagree").onclick = () => { state[id] = { v: "disagree", note: state[id]?.note || "" };
    save(); paint(card); progress(); card.querySelector(".note").focus(); };
  card.querySelector(".note").oninput = e => { state[id] = { v: "disagree", note: e.target.value }; save(); };
  paint(card);
});
function show(g) {
  document.querySelectorAll(".tab").forEach(t => t.classList.toggle("on", t.dataset.g === g));
  document.querySelectorAll(".guide").forEach(x => x.classList.toggle("on", x.dataset.g === g));
  cards.forEach(c => c.classList.toggle("hidden",
    g === "look" ? c.dataset.look !== "1" : g !== "all" && c.dataset.group !== g));
  window.scrollTo(0, 0);
}
document.querySelectorAll(".tab").forEach(t => t.onclick = () => show(t.dataset.g));
document.getElementById("copy").onclick = () => {
  const lines = cards.filter(c => state[c.dataset.id]?.v === "disagree")
    .map(c => `${c.dataset.id}: ${state[c.dataset.id].note || "(no note)"}`);
  const done = cards.filter(c => state[c.dataset.id]?.v).length;
  const text = `Calibration review: ${done} of ${cards.length} reviewed; unmarked count as agreed.\\n` +
    (lines.length ? "Disagreements:\\n" + lines.join("\\n") : "No disagreements.");
  document.getElementById("outtext").value = text;
  document.getElementById("out").style.display = "block";
  navigator.clipboard?.writeText(text).catch(() => {});
};
document.getElementById("close").onclick = () => document.getElementById("out").style.display = "none";
show("1"); progress();
</script></body></html>
"""

if __name__ == "__main__":
    raise SystemExit(main())
