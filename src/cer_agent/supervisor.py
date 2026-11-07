"""The supervisor with specialists (D12, article 3's third arm): a Strands supervisor that calls two specialist agents
as tools, on the same front end, tools and gate as the single agent (cer_agent.agent), so the only difference is the
structure.

- Front end: the workflow's single reading (extract.extract), then the rules engine, exactly as the single agent.
- Completeness specialist: checks missing facts and the facts that decide the result, with the same stricter-only
  `patch_facts` (v3c) and `confirm_missing`. A loosening change is held for the approver, as before.
- Policy specialist: read-only. Says which rule the current result rests on and which single fact, read differently,
  would change it, so the supervisor can send completeness back to re-check that fact.
- Supervisor: calls the specialists with a short structured handoff (never the transcript), then `finish`.
  Limits: turns per agent, at most two calls per specialist, and a token budget per case.

The rules engine decides; no agent can set a status, a deadline or a route, or loosen the result.

Usage (from code/, src on PYTHONPATH):
    NOVA_LITE_ARN=... python3 -m cer_agent.supervisor path/to/report.txt [--received YYYY-MM-DD]
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

from cer_agent.agent import VERSION as AGENT_VERSION
from cer_agent.agent import Case, _session
from cer_agent.extract import RETRY_TEMPERATURES, extract, to_facts
from cer_agent.workflow import make_client

SUPERVISOR_TURNS, SPECIALIST_TURNS = 8, 8
CALLS_PER_SPECIALIST = 2
TOKEN_BUDGET = 60_000  # input tokens per case, across every agent; a specialist call past it is refused

SUPERVISOR = """You coordinate the review of how a pipeline field report was read, for a compliance team. A first
reading has been recorded and run through a rules engine; the rules engine decides what the facts mean, and nobody
can set the decision. You have two specialists:
- ask_completeness(instruction): checks the recorded facts against the report and corrects them, quoting the report.
- ask_policy(question): says which rule the current result rests on and which single fact would change it.
Work in this order:
1. ask_completeness to check the missing facts and the facts that decide the result.
2. ask_policy which fact the result hinges on.
3. If policy names a fact worth re-checking, ask_completeness to re-check that one fact against the report.
4. Call finish. escalate=true only if the report contradicts itself or a doubt remains that the rules can't settle;
   missing facts alone go to the field as questions, not to escalation. Then stop.
Give each specialist a one- or two-sentence instruction; they see the report and the current facts themselves."""

COMPLETENESS = """You check how a pipeline field report was read, for a compliance team, following an instruction
from your supervisor. You see the report, the recorded facts and the rules engine's current result.
- For a missing fact the report does answer, call patch_facts with the field, the value and the report's exact words.
  If the report really doesn't say, call confirm_missing(fact, found=false).
- Correct a recorded fact only when the report's own words say otherwise, and quote them. Never remove a doubt the
  report leaves open: "about", "maybe" and "estimated" stay estimated.
- Then reply in one or two sentences: what you changed or confirmed, and anything you couldn't settle."""

POLICY = """You explain a rules engine's result on a pipeline field report, for a compliance team. You can't change
facts. Use rule_text to read a rule if you need it. Reply in at most three sentences: the rule the result rests on,
the single recorded fact that would change the result if it were read differently, and the words in the report to
re-check for it. If no single fact would change it, say so."""

VERSION = hashlib.sha256(
    json.dumps(
        [
            SUPERVISOR,
            COMPLETENESS,
            POLICY,
            SUPERVISOR_TURNS,
            SPECIALIST_TURNS,
            CALLS_PER_SPECIALIST,
            TOKEN_BUDGET,
            AGENT_VERSION,
            "supervisor-1b",
        ],
        sort_keys=True,
    ).encode()  # fmt: skip
).hexdigest()[:8]


def handoff(text: str, limit: int = 600) -> str:
    """A specialist's reply as the supervisor sees it: Nova's <thinking> text removed (it filled the handoff in the
    smoke test, crowding out the answer), then cut to `limit` characters."""
    text = re.sub(r"<thinking>.*?(</thinking>|$)", "", text, flags=re.S).strip()
    return text[:limit] or "(no answer)"


class Team:
    """One case's supervisor, specialists and shared state. Every agent works on the same `Case`, so a patch the
    completeness specialist makes is what the policy specialist and the supervisor see next."""

    def __init__(self, case: Case, model_factory):
        self.case, self.model = case, model_factory
        self.tools = {t.tool_name: t for t in case.tools()}
        self.usage = {"inputTokens": 0, "outputTokens": 0}
        self.calls: list[dict] = []

    def _add(self, usage: dict) -> None:
        for k in self.usage:
            self.usage[k] += usage.get(k, 0)

    def _context(self) -> str:
        c = self.case
        return (f"<report>\n{c.report}\n</report>\n\n<recorded_facts>\n{json.dumps(c.facts_shown())}\n"
                f"</recorded_facts>\n\n<rules_result>\n{c.summary()}\n</rules_result>")  # fmt: skip

    def _specialist(self, name: str, system: str, tools: list, instruction: str) -> str:
        from strands import Agent

        if sum(c["specialist"] == name for c in self.calls) >= CALLS_PER_SPECIALIST:
            return f"{name} has already been asked {CALLS_PER_SPECIALIST} times. Call finish."
        if self.usage["inputTokens"] >= TOKEN_BUDGET:
            return "The token budget for this case is used up. Call finish."
        agent = Agent(model=self.model(), tools=tools, system_prompt=system, callback_handler=None, name=name)
        try:
            result = agent(f"{self._context()}\n\n<instruction>\n{instruction}\n</instruction>",
                           limits={"turns": SPECIALIST_TURNS})  # fmt: skip
            self._add(result.metrics.accumulated_usage)
            reply = handoff(str(result))
        except Exception as e:  # noqa: BLE001 - a specialist's model error is reported to the supervisor, not fatal
            self._add(agent.event_loop_metrics.accumulated_usage)
            reply = f"{name} failed ({type(e).__name__}); the facts are as they were before this call."
        self.calls.append({"specialist": name, "instruction": instruction[:300], "reply": reply})
        return f"{reply}\n\nCurrent rules result: {self.case.summary()}"

    def supervisor_tools(self) -> list:
        from strands import tool

        t = self.tools

        @tool
        def ask_completeness(instruction: str) -> str:
            """Ask the completeness specialist to check or correct recorded facts against the report.
            instruction: one or two sentences on what to check (e.g. "check the missing facts and the volume")."""
            return self._specialist("completeness", COMPLETENESS, [t["patch_facts"], t["confirm_missing"]],
                                    instruction)  # fmt: skip

        @tool
        def ask_policy(question: str) -> str:
            """Ask the policy specialist which rule the result rests on and which single fact would change it."""
            return self._specialist("policy", POLICY, [t["rule_text"]], question)

        return [ask_completeness, ask_policy, t["finish"]]


def run(model_id: str, report: str, received: dt.date | None = None, region: str = "ca-central-1",
        client=None) -> dict:  # fmt: skip
    """The workflow's reading, then the supervisor's review. Returns the rules engine's packet from the reviewed facts,
    the trace (specialist calls, patches, holds, escalation), tokens across every agent, and latency. If every attempt
    fails, the workflow's packet stands, marked."""
    from strands import Agent
    from strands.models import BedrockModel

    t0 = time.perf_counter()
    x = extract(client or make_client(region), model_id, report, received)
    tin, tout, last = x["input_tokens"], x["output_tokens"], None
    for temp in (0, *RETRY_TEMPERATURES):
        case = Case(report, received, x["raw"])

        def model(temp=temp):
            return BedrockModel(model_id=model_id, boto_session=_session(region), temperature=temp, max_tokens=1000,
                                streaming=False)  # fmt: skip

        team = Team(case, model)
        sup = Agent(model=model(), tools=team.supervisor_tools(), system_prompt=SUPERVISOR, callback_handler=None,
                    name="supervisor")  # fmt: skip
        prompt = f"{team._context()}\n\nReview this reading with your specialists, then call finish."
        try:
            result = sup(prompt, limits={"turns": SUPERVISOR_TURNS})
        except Exception as e:  # noqa: BLE001 - a model error ends this attempt; usage so far still counts
            last = e
            team._add(sup.event_loop_metrics.accumulated_usage)
            tin, tout = tin + team.usage["inputTokens"], tout + team.usage["outputTokens"]
            continue
        team._add(result.metrics.accumulated_usage)
        tin, tout = tin + team.usage["inputTokens"], tout + team.usage["outputTokens"]
        trace = {"stop_reason": str(result.stop_reason), "turns": result.metrics.cycle_count, "calls": team.calls}
        break
    else:  # every attempt failed: the workflow's own packet stands
        case, trace = Case(report, received, x["raw"]), {"error": f"{type(last).__name__}: {last}"[:200]}
    pk = dict(case.packet)
    if case.held:  # a suggestion that would loosen the result: a person decides
        pk["route"] = "judgment"
        pk["route_triggers"] = [*pk["route_triggers"], "AGENT-HOLD"]
    pk["agent"] = {"version": VERSION, "arm": "supervisor", "patches": case.patches,
                   "confirmations": case.confirmations, "held": case.held, "finished": case.finished,
                   "escalate": bool(case.finished and case.finished["escalate"]),
                   "workflow_status": Case(report, received, x["raw"]).packet["status"], **trace}  # fmt: skip
    return {"packet": pk, "facts": to_facts(case.raw, received), "input_tokens": tin, "output_tokens": tout,
            "latency_s": time.perf_counter() - t0, "retries": x.get("retries", 0)}  # fmt: skip


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Run the supervisor with specialists on one field report.")
    ap.add_argument("report", type=pathlib.Path)
    ap.add_argument("--received", type=dt.date.fromisoformat)
    args = ap.parse_args(argv)
    arn = os.environ.get("NOVA_LITE_ARN")
    if not arn:
        print("Set NOVA_LITE_ARN (the tagged Nova Lite profile ARN).")
        return 2
    r = run(arn, args.report.read_text(encoding="utf-8"), args.received)
    print(json.dumps(r["packet"]["agent"], indent=2, default=str))
    print(f"{r['packet']['status']} {r['packet']['deadline']} {r['packet']['route']}; tokens in/out "
          f"{r['input_tokens']}/{r['output_tokens']}, {r['latency_s']:.1f} s", file=sys.stderr)  # fmt: skip
    return 0


if __name__ == "__main__":
    sys.exit(main())
