"""The single agent (D12, article 3's agent arm): a Strands agent on Nova Lite that reviews the fixed workflow's
reading of a report, corrects it where the report says otherwise, and can send the case to a person.

The agent decides the facts; the rules engine decides what they mean. v2 (after v1's dev run, D37):
- It starts from the workflow's own reading: code runs the same single extraction first (extract.extract), so the
  agent can only add to the workflow, not re-read the report worse inside a longer prompt.
- It changes one fact at a time with `patch_facts(field, value, quote)`: the quote must be the report's own words
  (checked by code), and every other fact is kept. v1's `record_facts` replaced the whole reading, so a partial
  second call wiped facts and turned reportable cases into "not reportable".
- `confirm_missing` only accepts the facts the rules list as missing.
- `rule_text` looks up a rule; `finish` ends the case, escalating only for doubt the facts can't settle.

The packet is always the rules engine's, computed from the current facts. The agent can't set a status or a
deadline, so it can't talk its way past "when in doubt, notify".

v3 (D38): patches can only make the result stricter. A quote check proves the words are in the report, not that they
support the change (v2's two misses quoted real words that didn't). So a patch goes in only if the rules engine's
result is at least as strict afterwards (notify, deadline, due time, route); one that would loosen it is held as a
suggestion for the approver, the facts stay as read, and the case goes to a person (route trigger AGENT-HOLD).

Usage (from code/, src on PYTHONPATH):
    NOVA_LITE_ARN=... python3 -m cer_agent.agent path/to/report.txt [--received YYYY-MM-DD]
"""

from __future__ import annotations

import argparse
import datetime as dt
import functools
import hashlib
import html
import json
import os
import pathlib
import re
import sys
import time

from cer_agent import drafter
from cer_agent.extract import RETRY_TEMPERATURES, extract, normalise, to_facts
from cer_agent.extract import TOOL as RECORD_TOOL
from cer_agent.judge import in_report
from cer_agent.workflow import make_client, packet

RULES_SPEC = pathlib.Path(__file__).resolve().parents[2] / "docs" / "rules-spec.md"  # the repo root is code/
MAX_TURNS = 10
FIELDS = RECORD_TOOL["inputSchema"]["json"]["properties"]
# The rules' missing facts -> the record_facts fields that answer them.
MISSING_FIELDS = {
    "death": ["death"], "serious_injury": ["injury"], "env_effect": ["env_effect"],
    "fire_or_explosion": ["fire_or_explosion"], "rupture": ["rupture"], "toxic_plume": ["toxic_plume"],
    "release": ["release"], "substance": ["substance"], "volume_m3": ["volume", "volume_unit", "volume_basis"],
    "volume_state": ["volume_state"], "through_pipe_body_or_weld": ["through_pipe_body_or_weld"],
    "rate_kg_s": ["rate", "rate_unit", "rate_basis"], "lands": ["lands"], "sipr_for_safety": ["limit_type"],
}  # fmt: skip

SYSTEM = """You review how a pipeline field report was read, for a compliance team. A first reading of the report
has already been recorded and run through a rules engine. You check that reading against the report and correct it
where the report says otherwise. The rules engine decides what the facts mean; you can't set the decision.

How to work:
1. Read the report, the recorded facts and the rules engine's result.
2. For each missing fact, look for it in the report. If the report does answer it (for example "inside the fence"
   answers where the product went), call patch_facts with the field, the value and the report's exact words. If the
   report really doesn't say, call confirm_missing(fact, found=false): it becomes a question for the field.
3. Check the facts that decide the result (substance, volume or rate and whether it's estimated or measured, where
   the product went, injuries) against the report. Correct a fact only when the report's own words say otherwise,
   and quote them. Never remove a doubt the report leaves open: "about", "maybe" and "estimated" stay estimated.
4. Call finish. Set escalate=true only if the report contradicts itself or something the rules can't settle
   remains; missing facts alone are not a reason to escalate (they go to the field as questions). Then stop."""

VERSION = hashlib.sha256(
    json.dumps([SYSTEM, MISSING_FIELDS, MAX_TURNS, "agent-3c"], sort_keys=True).encode()
).hexdigest()[:8]


def rule_passage(rule_id: str, limit: int = 1500) -> str:
    """The rules-spec text for a rule ID. A rule is either a heading ("### PREC — ...", up to the next heading) or a
    table row ("| `T3-LVP` | ... |"), followed by its "*Interpretation of `T3-LVP`:*" paragraph if there is one."""
    if not RULES_SPEC.exists():  # a packaged install without the repo's docs/
        return f"The rules spec isn't available here, so there's no text for {rule_id}."
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


DEADLINE_RANK = {None: 0, "T24": 1, "T3": 2}


def loosening(before: dict, after: dict) -> list[str]:
    """How `after` is less strict than `before` (empty if it's at least as strict). "Reportable" and
    "precautionary" both notify, so moving between them isn't loosening on its own; the deadline and route decide."""
    out = []
    if before["status"] != "not reportable" and after["status"] == "not reportable":
        out.append(f"status {before['status']} -> not reportable")
    if DEADLINE_RANK[after["deadline"]] < DEADLINE_RANK[before["deadline"]]:
        out.append(f"deadline {before['deadline']} -> {after['deadline']}")
    elif after["deadline"] == before["deadline"] and before["due_at"] and after["due_at"] \
            and after["due_at"] > before["due_at"]:  # fmt: skip
        out.append(f"due {before['due_at']} -> {after['due_at']}")
    if before["route"] == "judgment" and after["route"] == "clear-cut":
        out.append("route judgment -> clear-cut")
    return out


def example(spec: dict):
    """A valid value for a schema node, shown in error messages so the agent learns the format (D38: 156 of 275
    patch calls on test were rejected, mostly for format, e.g. 8-10 tries at volume_alternatives on one case)."""
    types = spec.get("type") if isinstance(spec.get("type"), list) else [spec.get("type")]
    if "array" not in types:
        if "enum" in spec:
            return next(v for v in spec["enum"] if v not in ("not_stated", "not_given", "unknown"))
        return 1.5 if "number" in types else "text"
    item = spec.get("items", {})
    if item.get("type") == "array":  # one list per account: two accounts that differ
        allowed = item.get("items", {}).get("enum", ["a", "b"])
        return [[allowed[0]], [allowed[-1]]]
    if item.get("type") == "number":
        return [1.2, 2.0]
    return [example(item)]


def check(spec: dict, value, path: str) -> str | None:
    """Why `value` doesn't fit the schema node (None if it does): type and allowed values at every level, so a list
    of lists is checked all the way down (lands_alternatives once took junk such as ':[')."""
    types = spec.get("type") if isinstance(spec.get("type"), list) else [spec.get("type")]
    if value is None:
        return None if "null" in types else f"{path} can't be empty"
    if "array" in types:
        if not isinstance(value, list):
            return f"{path} must be a list"
        return next((e for i, v in enumerate(value) if (e := check(spec.get("items", {}), v, f"{path}[{i}]"))), None)
    if "enum" in spec:
        return None if value in spec["enum"] else f"{path} must be one of: {', '.join(map(str, spec['enum']))}"
    if "number" in types:
        ok = isinstance(value, int | float) and not isinstance(value, bool)
        return None if ok else f"{path} must be a number"
    return None if isinstance(value, str) else f"{path} must be text"


def _parse(value):
    """The agent's value as data: JSON if it parses, with two forms it often sends made into JSON first:
    HTML-escaped quotes (&quot;) and a tuple such as (1.2, 2.0)."""
    if not isinstance(value, str):
        return value
    text = html.unescape(value).strip()
    if text.startswith("(") and text.endswith(")"):
        text = f"[{text[1:-1]}]"
    if text in ("null", "None"):
        return None
    try:
        return json.loads(text)
    except ValueError:
        return text


def _value(field: str, value):
    """The patch value in the record_facts schema's type, or an error message that shows a correct example."""
    spec = FIELDS[field]
    v = _parse(value)
    if spec.get("type") == "array" and not isinstance(v, list):
        v = [v]  # one item given for a list
    err = check(spec, v, field)
    if not err:
        return v, None
    hint = f" Example: {json.dumps(example(spec))}."
    if spec.get("type") != "array" and f"{field}_alternatives" in FIELDS:
        hint += f" For two accounts or a range, use {field}_alternatives."
    return None, err + "." + hint


class Case:
    """One report's tools and state. A fresh instance per run, so tool state never leaks between cases."""

    def __init__(self, report: str, received: dt.date | None, raw: dict):
        self.report, self.received = normalise(report), received
        self.raw = dict(raw)
        self.packet = self._decide()
        self.patches: list[dict] = []
        self.confirmations: list[dict] = []
        self.held: list[dict] = []  # loosening patches, for the approver as suggestions
        self.finished: dict | None = None

    def _decide(self) -> dict:
        return packet(to_facts(self.raw, self.received), {"raw": self.raw})

    def facts_shown(self) -> dict:
        return {k: v for k, v in self.raw.items() if v not in (None, "", [], "not_given", "not_stated")}

    def summary(self) -> str:
        pk = self.packet
        return json.dumps({
            "status": pk["status"], "deadline": pk["deadline"], "incident_types": pk["incident_types"],
            "missing_facts": {m: {"question": drafter.QUESTIONS.get(m, m), "fields": MISSING_FIELDS.get(m, [m])}
                              for m in pk["missing"]},
            "open_points": [drafter.TRIGGERS.get(t, t) for t in pk["route_triggers"]],
        })  # fmt: skip

    # The tools' logic, shared by the in-process agent (`tools`, Strands) and the MCP server (cer_agent.mcp_server).
    # Each docstring is the description the model sees, so both transports show the agent the same words.
    def patch_facts(self, field: str, value: str, quote: str) -> str:
        """Correct one recorded fact. field: a record_facts field name; value: the new value as JSON (a list
        as a JSON list, e.g. ["company_property"]; volume_alternatives [1.2, 2.0]; lands_alternatives one list
        per account, e.g. [["company_property"], ["off_right_of_way"]]); quote: the report's exact words that
        say it. Other facts are kept."""
        if field not in FIELDS:
            return f"No field {field!r}. Fields: {', '.join(FIELDS)}"
        v, err = _value(field, value)
        if err:
            return err
        if v == self.raw.get(field):  # nothing to change: say so before any quote check, so the agent moves on
            self.patches.append({"field": field, "from": v, "to": v, "quote": quote, "accepted": False,
                                 "noop": True})  # fmt: skip
            return f"{field} is already {json.dumps(v)}; nothing to change. Go on to the next fact."
        ok = bool(quote) and in_report(quote, self.report)
        self.patches.append({"field": field, "from": self.raw.get(field), "to": v, "quote": quote,
                             "accepted": ok})  # fmt: skip
        if not ok:
            return "Not changed: that quote isn't in the report. Quote the report's exact words."
        before = (self.packet["status"], self.packet["deadline"])
        prior, old_packet = self.raw.get(field), self.packet
        self.raw[field] = v
        try:
            new_packet = self._decide()
        except (TypeError, ValueError) as e:  # a value the rules can't use: undo, and say so
            self.raw[field] = prior
            self.patches[-1]["accepted"] = False
            return f"Not changed: {field}={v!r} can't be used ({e})."
        if looser := loosening(old_packet, new_packet):  # only a person can loosen the result
            self.raw[field] = prior
            self.patches[-1].update(accepted=False, held=looser)
            self.held.append({"field": field, "from": prior, "to": v, "quote": quote, "would": looser})
            return (f"Held for the approver, not changed: {field}={v!r} would loosen the result "
                    f"({'; '.join(looser)}). It goes to a person as a suggestion with your quote. "
                    f"Carry on with the other facts.")  # fmt: skip
        self.packet = new_packet
        after = (self.packet["status"], self.packet["deadline"])
        note = "" if before == after else f" The result changed from {before} to {after}."
        return f"Changed {field} to {v!r}.{note} Now: {self.summary()}"

    def confirm_missing(self, fact: str, found: bool) -> str:
        """For a fact on the missing list: found=false if the report really doesn't say (it becomes a question
        for the field). If the report does say, use patch_facts instead."""
        if fact not in self.packet["missing"]:
            return f"{fact!r} isn't missing. Missing now: {', '.join(self.packet['missing']) or 'none'}."
        self.confirmations.append({"fact": fact, "found": found})
        if found:
            fields = ", ".join(MISSING_FIELDS.get(fact, [fact]))
            return f"Then correct it with patch_facts on {fields}, quoting the report."
        return f"Recorded: the report doesn't say. {fact!r} stays a question for the field."

    @staticmethod
    def rule_text(rule_id: str) -> str:
        """The rules spec's text for one rule ID (e.g. T3-LVP, INC-d, PREC, U2-NEAR)."""
        return rule_passage(rule_id.strip())

    def finish(self, escalate: bool, reason: str) -> str:
        """End the case. escalate=true sends it to a person: only for a contradiction or a doubt the rules
        can't settle, not for missing facts."""
        self.finished = {"escalate": escalate, "reason": reason}
        return "Done. Stop now."

    def tools(self, stop_at_finish: bool = False) -> list:
        """The four tools as Strands tools, for the in-process agent. stop_at_finish (article 4): `finish` also ends
        the loop, as the LangGraph build's graph does, instead of sending "Done. Stop now." back for one more turn."""
        from strands import ToolContext, tool

        def patch_facts(field: str, value: str, quote: str) -> str:
            return self.patch_facts(field, value, quote)

        def confirm_missing(fact: str, found: bool) -> str:
            return self.confirm_missing(fact, found)

        def rule_text(rule_id: str) -> str:
            return self.rule_text(rule_id)

        def finish(escalate: bool, reason: str) -> str:
            return self.finish(escalate, reason)

        def finish_and_stop(escalate: bool, reason: str, tool_context: ToolContext) -> str:
            tool_context.agent.cancel(after_current_tools=True)  # no model call after this tool batch
            return self.finish(escalate, reason)

        fns = [patch_facts, confirm_missing, rule_text, finish]
        for f in fns:
            f.__doc__ = getattr(Case, f.__name__).__doc__
        tools = [tool(f) for f in fns]
        if stop_at_finish:
            finish_and_stop.__doc__ = Case.finish.__doc__
            finish_and_stop.__annotations__["tool_context"] = ToolContext  # the class, not the string this module's
            # `from __future__ import annotations` leaves, so Strands recognises the context parameter
            tools[-1] = tool(name="finish", context=True)(finish_and_stop)
        return tools

    def result(self, workflow_status: str, trace: dict) -> dict:
        """The packet the case ends with: the rules engine's, from the reviewed facts, with the agent's trace. A
        held suggestion (it would loosen the result) sends the case to a person."""
        pk = dict(self.packet)
        if self.held:
            pk["route"] = "judgment"
            pk["route_triggers"] = [*pk["route_triggers"], "AGENT-HOLD"]
        pk["agent"] = {"version": VERSION, "patches": self.patches, "confirmations": self.confirmations,
                       "held": self.held, "finished": self.finished,
                       "escalate": bool(self.finished and self.finished["escalate"]),
                       "workflow_status": workflow_status, **trace}  # fmt: skip
        return pk


@functools.cache
def _session(region: str):
    """One boto3 session per region, shared by every case's model. A new session per case re-reads botocore's
    service definitions: about 9 s a case with the venv on the Windows drive, found by tracing (D40)."""
    import boto3

    return boto3.Session(region_name=region)


def run(model_id: str, report: str, received: dt.date | None = None, region: str = "ca-central-1",
        client=None, stop_at_finish: bool = False) -> dict:  # fmt: skip
    """The workflow's reading first (one extraction), then the agent's review. Returns the rules engine's packet
    from the reviewed facts, the agent's trace (patches, confirmations, escalation), tokens and latency. A malformed
    model reply in the review is retried warmer; if every attempt fails, the workflow's packet stands, marked."""
    from strands import Agent
    from strands.models import BedrockModel

    t0 = time.perf_counter()
    x = extract(client or make_client(region), model_id, report, received)
    tin, tout, last = x["input_tokens"], x["output_tokens"], None
    for temp in (0, *RETRY_TEMPERATURES):
        case = Case(report, received, x["raw"])
        prompt = (
            f"<report>\n{case.report}\n</report>\n\n<recorded_facts>\n{json.dumps(case.facts_shown())}\n"
            f"</recorded_facts>\n\n<rules_result>\n{case.summary()}\n</rules_result>"
        )
        model = BedrockModel(model_id=model_id, boto_session=_session(region), temperature=temp, max_tokens=1000,
                             streaming=False)  # fmt: skip
        agent = Agent(model=model, tools=case.tools(stop_at_finish), system_prompt=SYSTEM, callback_handler=None)
        try:
            result = agent(prompt, limits={"turns": MAX_TURNS})
        except Exception as e:  # noqa: BLE001 - a model error ends this attempt; usage so far still counts
            last = e
            usage = agent.event_loop_metrics.accumulated_usage
            tin, tout = tin + usage.get("inputTokens", 0), tout + usage.get("outputTokens", 0)
            continue
        usage = result.metrics.accumulated_usage
        tin, tout = tin + usage.get("inputTokens", 0), tout + usage.get("outputTokens", 0)
        trace = {"stop_reason": str(result.stop_reason), "turns": result.metrics.cycle_count,
                 **({"stop_at_finish": True} if stop_at_finish else {})}  # fmt: skip
        break
    else:  # every review attempt failed: the workflow's own packet stands
        case, trace = Case(report, received, x["raw"]), {"error": f"{type(last).__name__}: {last}"[:200]}
    pk = case.result(Case(report, received, x["raw"]).packet["status"], trace)
    return {"packet": pk, "facts": to_facts(case.raw, received), "input_tokens": tin, "output_tokens": tout,
            "latency_s": time.perf_counter() - t0, "retries": x.get("retries", 0)}  # fmt: skip


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
