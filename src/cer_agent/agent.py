"""The single agent (D12, article 3's first agent arm): one Strands agent on Nova Lite that reads the report, checks
its own reading against what the rules need, and can send the case to a person.

The agent decides the facts; the rules engine decides what they mean. It records what the report says with the same
`record_facts` schema and reading rules as the fixed workflow (extract.TOOL, extract.SYSTEM), so any difference in the
results comes from the loop, not from new wording. Each `record_facts` call runs the rules and shows the agent the
decision, the missing facts and the open points. The agent may then:
- look up a rule's text (`rule_text`) to check a threshold or a definition;
- before a missing fact becomes a question for the field, look for it in the report (`confirm_missing`): if the
  report answers it, the quote is checked against the report and the agent records the facts again;
- finish, escalating to a person if it is unsure (`finish`).

The packet is always the rules engine's, computed from the agent's last `record_facts`. The agent can't set a status
or a deadline, so it can't talk its way past "when in doubt, notify".

Usage (from code/, src on PYTHONPATH):
    NOVA_LITE_ARN=... python3 -m cer_agent.agent path/to/report.txt [--received YYYY-MM-DD]
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import sys
import time

from cer_agent import drafter
from cer_agent.extract import RETRY_TEMPERATURES, normalise, to_facts
from cer_agent.extract import SYSTEM as READING_RULES
from cer_agent.extract import TOOL as RECORD_TOOL
from cer_agent.judge import in_report
from cer_agent.workflow import packet

PROJECT = pathlib.Path(__file__).resolve().parents[3]
RULES_SPEC = PROJECT / "input" / "cer" / "rules-spec.md"
MAX_TURNS = 8

SYSTEM = f"""You triage pipeline field reports for a compliance team. You decide what the report says; a rules
engine decides what that means for reporting. You can't set the decision yourself.

How to work:
1. Call record_facts with what the report says.
2. Read the result. For each missing fact, look for it in the report again. If the report does answer it (for
   example "inside the fence" answers where the product went), call confirm_missing with found=true and the
   report's exact words, then call record_facts again with the corrected facts. If the report really doesn't say,
   call confirm_missing with found=false; it becomes a question for the field.
3. For each open point (an estimate near a threshold, a contradiction, a test with no number), check the report
   and, if useful, the rule with rule_text. Don't resolve a genuine doubt by guessing: leave it open.
4. Call finish. Escalate if an open point remains, the report contradicts itself, or you aren't sure you read it
   right. Then stop.

Reading rules for record_facts:
{READING_RULES}"""

VERSION = hashlib.sha256(json.dumps([SYSTEM, RECORD_TOOL, MAX_TURNS, "agent-1"], sort_keys=True).encode()).hexdigest()[
    :8
]


def rule_passage(rule_id: str, limit: int = 1500) -> str:
    """The rules-spec text for a rule ID. A rule is either a heading ("### PREC — ...", up to the next heading) or a
    table row ("| `T3-LVP` | ... |"), followed by its "*Interpretation of `T3-LVP`:*" paragraph if there is one."""
    lines = RULES_SPEC.read_text(encoding="utf-8").splitlines()
    rid = re.escape(rule_id)
    for i, ln in enumerate(lines):
        if re.match(rf"^#+ {rid}\b", ln):
            out = [ln]
            for nxt in lines[i + 1 :]:
                if nxt.startswith("#"):
                    break
                out.append(nxt)
            return "\n".join(out).strip()[:limit]
    rows = [ln for ln in lines if re.match(rf"^\|\s*`{rid}`\s*\|", ln)]
    if not rows:
        return f"No rule {rule_id} in the rules spec."
    notes = []
    for i, ln in enumerate(lines):
        if ln.startswith(f"*Interpretation of `{rule_id}`"):
            for nxt in lines[i:]:
                if not nxt.strip():
                    break
                notes.append(nxt)
    return "\n".join(rows + ([""] + notes if notes else [])).strip()[:limit]


class Case:
    """One report's tools and state. A fresh instance per run, so tool state never leaks between cases."""

    def __init__(self, report: str, received: dt.date | None):
        self.report, self.received = normalise(report), received
        self.raw: dict | None = None
        self.packet: dict | None = None
        self.records = 0
        self.confirmations: list[dict] = []
        self.finished: dict | None = None

    def summary(self) -> str:
        pk = self.packet
        return json.dumps({
            "status": pk["status"], "deadline": pk["deadline"], "incident_types": pk["incident_types"],
            "missing_facts": {m: drafter.QUESTIONS.get(m, m) for m in pk["missing"]},
            "open_points": [drafter.TRIGGERS.get(t, t) for t in pk["route_triggers"]],
            "note": "Check each missing fact against the report before it goes to the field.",
        })  # fmt: skip

    def tools(self) -> list:
        from strands import tool
        from strands.tools.tools import PythonAgentTool

        def record_facts(tool_use, **_):
            self.raw, self.records = dict(tool_use["input"]), self.records + 1
            self.packet = packet(to_facts(self.raw, self.received), {"raw": self.raw})
            return {"toolUseId": tool_use["toolUseId"], "status": "success", "content": [{"text": self.summary()}]}

        @tool
        def rule_text(rule_id: str) -> str:
            """The rules spec's text for one rule ID (e.g. T3-LVP, INC-d, PREC, U2-NEAR)."""
            return rule_passage(rule_id.strip())

        @tool
        def confirm_missing(fact: str, found: bool, quote: str = "") -> str:
            """Before a missing fact becomes a question for the field: found=true with the report's exact words if
            the report does answer it, or found=false if it really doesn't say."""
            ok = found and bool(quote) and in_report(quote, self.report)
            self.confirmations.append({"fact": fact, "found": found, "quote": quote, "quote_in_report": ok})
            if found and not ok:
                return "That quote isn't in the report. Quote the report's exact words, or confirm it's not stated."
            if found:
                return "Confirmed in the report. Call record_facts again with that fact filled in."
            return f"Recorded: the report doesn't say. '{fact}' stays a question for the field."

        @tool
        def finish(escalate: bool, reason: str) -> str:
            """End the case. escalate=true sends it to a person with the reason; use it when unsure."""
            self.finished = {"escalate": escalate, "reason": reason}
            return "Done. Stop now."

        spec = {
            "name": RECORD_TOOL["name"],
            "description": RECORD_TOOL["description"] + " Runs the rules engine "
            "and returns the decision, missing facts and open points.",
            "inputSchema": RECORD_TOOL["inputSchema"],
        }
        return [PythonAgentTool("record_facts", spec, record_facts), rule_text, confirm_missing, finish]


def run(model_id: str, report: str, received: dt.date | None = None, region: str = "ca-central-1") -> dict:
    """Run the agent on one report. Returns the rules engine's packet from the agent's last reading, the agent's
    trace (records, confirmations, escalation), tokens and latency. A malformed model reply is retried warmer."""
    from strands import Agent
    from strands.models import BedrockModel

    t0, temps, last = time.perf_counter(), (0, *RETRY_TEMPERATURES), None
    tin = tout = 0
    for attempt, temp in enumerate(temps):
        case = Case(report, received)
        model = BedrockModel(model_id=model_id, region_name=region, temperature=temp, max_tokens=1500, streaming=False)
        agent = Agent(model=model, tools=case.tools(), system_prompt=SYSTEM, callback_handler=None)
        try:
            result = agent(f"<report>\n{case.report}\n</report>", limits={"turns": MAX_TURNS})
        except Exception as e:  # noqa: BLE001 - a model error ends this attempt; usage so far still counts
            last = e
            usage = agent.event_loop_metrics.accumulated_usage
            tin, tout = tin + usage.get("inputTokens", 0), tout + usage.get("outputTokens", 0)
            continue
        usage = result.metrics.accumulated_usage
        tin, tout = tin + usage.get("inputTokens", 0), tout + usage.get("outputTokens", 0)
        if case.packet is None:  # never recorded facts: try again warmer
            last = RuntimeError("agent finished without calling record_facts")
            continue
        pk = dict(case.packet)
        esc = bool(case.finished and case.finished["escalate"])
        pk["agent"] = {"version": VERSION, "records": case.records, "confirmations": case.confirmations,
                       "finished": case.finished, "escalate": esc, "stop_reason": str(result.stop_reason),
                       "turns": result.metrics.cycle_count}  # fmt: skip
        return {"packet": pk, "facts": to_facts(case.raw, received), "input_tokens": tin, "output_tokens": tout,
                "latency_s": time.perf_counter() - t0, "retries": attempt}  # fmt: skip
    raise RuntimeError(f"agent failed after {len(temps)} attempts: {last}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Run the single agent on one field report.")
    ap.add_argument("report", type=pathlib.Path)
    ap.add_argument("--received", type=dt.date.fromisoformat)
    args = ap.parse_args(argv)
    arn = os.environ.get("NOVA_LITE_ARN")
    if not arn:
        print("Set NOVA_LITE_ARN (terraform output nova_lite_profile_arn).")
        return 2
    r = run(arn, args.report.read_text(encoding="utf-8"), args.received)
    print(json.dumps(r["packet"], indent=2, default=str))
    print(f"tokens in/out {r['input_tokens']}/{r['output_tokens']}, {r['latency_s']:.1f} s", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
