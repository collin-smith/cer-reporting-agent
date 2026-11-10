"""The approval gate (article 6, D51): nothing leaves without a person, and an unanswered case escalates.

Step Functions (infra/approval.tf) runs four steps, all in this module's Lambda `handler`:

  triage    guardrail flags on the report (detect only), the strict check, the draft, PII masking on the draft;
            writes the case record. A 3-hour case pages the primary approver at once.
  park      called with a task token (.waitForTaskToken): stores the token on the case and waits. The state machine's
            timeout is the time to the next escalation.
  escalate  on timeout: pages the next level (D25: 3 h cases backup at 60 min, both at 150 min "file the
            precautionary notice now"; 24 h and not-reportable cases backup at 8 h, both at 20 h), then parks again.
            Past the deadline the case is OVERDUE and the run fails, so it shows in the console as failed.
  close     the approver's decision (approve, edit, reject), sent by the CLI with SendTaskSuccess; written to the
            case with who, when, a reason and a diff of any edit.

Times run from discovery, as in D25. TIME_SCALE is real seconds per scheduled minute (60 in production); the
measured run used 1, so 60 minutes took a minute.

The approver's CLI (the same module, no API Gateway yet):
  python -m cer_agent.approval submit AD-148 CL-004 ...    # start runs on test-set reports (demo)
  python -m cer_agent.approval queue                        # what's waiting, most urgent first
  python -m cer_agent.approval show CASE                    # draft, flags, history
  python -m cer_agent.approval approve CASE --by NAME
  python -m cer_agent.approval edit CASE --by NAME --draft FILE [--status S --reason R]
  python -m cer_agent.approval reject CASE --by NAME --reason R
  python -m cer_agent.approval measure CASE ...             # transitions, timings and cost per run ($0 reads)
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import json
import os
import pathlib
import re
import sys
import time

TABLE = os.environ.get("CASES_TABLE", "agentic-ai-cases")
STATE_MACHINE = os.environ.get("STATE_MACHINE_NAME", "agentic-ai-approval")
REGION = "ca-central-1"
OPEN = ("PENDING_APPROVAL", "ESCALATED")

# Escalation settings (D25), minutes from discovery: (minute, who is paged, message). Settings, not CER rules.
SCHEDULE = {
    "T3": [(60, "backup", "Not approved after 60 minutes: paging the backup approver."),
           (150, "primary+backup", "Not approved after 150 minutes: file the precautionary notice now.")],
    "T24": [(480, "backup", "Not approved after 8 hours: paging the backup approver."),
            (1200, "primary+backup", "Not approved after 20 hours: file the precautionary notice now.")],
}  # fmt: skip
DEADLINE_MIN = {"T3": 180, "T24": 1440}

# Prices (USD): Nova Lite per 1M tokens; guardrails per 1K text units (Price List, ca-central-1, 2026-11-09).
PRICE_IN, PRICE_OUT = 0.06, 0.24
# The fallback model (D52): Claude Haiku 5.5 through the Canada profile, per 1M tokens (D19's first-party price).
FALLBACK_PRICE_IN, FALLBACK_PRICE_OUT = 0.10, 0.50
GUARD_PRICE = {"contentPolicyUnits": 0.15, "topicPolicyUnits": 0.15, "sensitiveInformationPolicyUnits": 0.10}
# Step Functions Standard, per state transition; Lambda per GB-second (x86) and per request.
SFN_TRANSITION, LAMBDA_GB_S, LAMBDA_REQ = 0.000025, 0.0000166667, 0.0000002

DECISIONS = {"approve": "APPROVED", "edit": "EDITED_AND_APPROVED", "reject": "REJECTED"}


def now() -> str:
    return dt.datetime.now(dt.UTC).isoformat(timespec="seconds")


def _table():
    import boto3

    return boto3.resource("dynamodb", region_name=REGION).Table(TABLE)


def _event(kind: str, **detail) -> dict:
    return {"at": now(), "event": kind, **{k: v for k, v in detail.items() if v is not None}}


def _append(table, case_id: str, event: dict, **sets):
    """Append to the case history (never rewritten) and set any other attributes."""
    names = {"#h": "history", **{f"#k{i}": k for i, k in enumerate(sets)}}
    values = {f":v{i}": v for i, v in enumerate(sets.values())}
    expr = "SET #h = list_append(#h, :e)" + "".join(f", #k{i} = :v{i}" for i in range(len(sets)))
    table.update_item(Key={"case_id": case_id}, UpdateExpression=expr, ExpressionAttributeNames=names,
                      ExpressionAttributeValues={":e": [event], **values})  # fmt: skip


# --- Guardrails (standalone ApplyGuardrail, D50) ---


def guardrail_flags(client, guardrail_id: str, text: str) -> tuple[list[str], dict]:
    """Reviewer flags from the reports guardrail (detect mode): the denied topic, a prompt attack or any harm filter at
    MEDIUM confidence or above. Blocks nothing."""
    r = client.apply_guardrail(guardrailIdentifier=guardrail_id, guardrailVersion="DRAFT", source="INPUT",
                               content=[{"text": {"text": text}}])  # fmt: skip
    flags = []
    for a in r.get("assessments", []):
        for f in a.get("contentPolicy", {}).get("filters", []):
            if f["confidence"] in ("MEDIUM", "HIGH"):
                flags.append(f"{f['type'].lower().replace('_', ' ')} ({f['confidence'].lower()} confidence)")
        for t in a.get("topicPolicy", {}).get("topics", []):
            flags.append(f"denied topic: {t['name']}")
    return flags, r.get("usage", {})


def mask_draft(client, guardrail_id: str, text: str) -> tuple[str, list[str], dict]:
    """Phone numbers, emails and SINs masked in the draft (drafts guardrail)."""
    r = client.apply_guardrail(guardrailIdentifier=guardrail_id, guardrailVersion="DRAFT", source="OUTPUT",
                               content=[{"text": {"text": text}}])  # fmt: skip
    found = [e["type"] for a in r.get("assessments", [])
             for e in a.get("sensitiveInformationPolicy", {}).get("piiEntities", [])]  # fmt: skip
    masked = r["outputs"][0]["text"] if r["action"] == "GUARDRAIL_INTERVENED" and r.get("outputs") else text
    return masked, found, r.get("usage", {})


def _guard_cost(*usages: dict) -> float:
    return sum(n * GUARD_PRICE.get(k, 0) / 1000 for u in usages for k, n in u.items() if isinstance(n, int))


# --- Escalation clock ---


def marks(deadline: str | None, elapsed_min: float, scale: float) -> list[int]:
    """Seconds after triage at which each wait ends: the two escalations, then the deadline. A case already past a
    mark gets 1 s, so it escalates at once."""
    key = deadline or "T24"  # not reportable still needs a person (D25); it runs on the 24 h settings
    mins = [m for m, _, _ in SCHEDULE[key]] + [DEADLINE_MIN[key]]
    return [max(1, round((m - elapsed_min) * scale)) for m in mins]


def wait_s(state: dict) -> int:
    return max(1, state["marks"][state["level"]] - int(time.time() - state["start"]))


# --- Lambda steps ---


def draft_with_fallback(primary: tuple, fallback: tuple | None, report: str, pk: dict, operator: str | None) -> dict:
    """The draft by Nova Lite, else by the fallback model, else rendered from the rules alone (D52). The decision and
    deadline never need a model to draft; only the narrative does, so a model failure costs the narrative, not the
    case."""
    from cer_agent.drafter import draft, render
    from cer_agent.workflow import FALLBACK_ON, error_code

    errors = []
    for model, (client, model_id) in (("primary", primary), ("fallback", fallback)):
        if client is None:
            continue
        try:
            return {**draft(client, model_id, report, pk, operator), "model": model, "errors": errors}
        except Exception as e:
            if error_code(e) not in FALLBACK_ON:
                raise
            errors.append(error_code(e))
    banner = (f"> **No model could draft this ({', '.join(errors)}).** The decision, deadline and reasons below come "
              "from the rules; PIR-5 to PIR-13 are blank because no model wrote them, not because the report is "
              "silent. Fill them from the field report at the end.\n\n")  # fmt: skip
    text = banner + render(pk, {}, operator) + "\n\n---\n\n**Field report:**\n\n" + report
    return {"text": text, "input_tokens": 0, "output_tokens": 0, "model": "rules only", "errors": errors}


def triage(event: dict) -> dict:
    import boto3

    from cer_agent.workflow import make_client, run_strict

    case_id, report = event["case_id"], event["report"]
    received = dt.date.fromisoformat(event["received"]) if event.get("received") else None
    table = _table()
    table.put_item(Item={"case_id": case_id, "status": "IN_PROGRESS", "due_at": "9999",
                         "history": [_event("intake", source=event.get("source"))]},
                   ConditionExpression="attribute_not_exists(case_id) OR #s = :p",  # a retried triage starts over
                   ExpressionAttributeNames={"#s": "status"},
                   ExpressionAttributeValues={":p": "IN_PROGRESS"})  # fmt: skip
    t0 = time.time()
    bedrock = boto3.client("bedrock-runtime", region_name=REGION)
    flags, u_in = guardrail_flags(bedrock, os.environ["REPORTS_GUARDRAIL"], report)
    # Few retries per model, so Nova's retries and the fallback's both fit in the Lambda's timeout (D52).
    retries = int(os.environ.get("MODEL_RETRIES", "3"))
    client, model = make_client(max_attempts=retries), os.environ["MODEL_ARN"]
    fb_arn = os.environ.get("FALLBACK_MODEL_ARN")
    fallback = (make_client(max_attempts=retries), fb_arn) if fb_arn else None
    r = run_strict(client, model, report, received, fallback)
    pk = r["packet"]
    d = draft_with_fallback((client, model), fallback or (None, None), report, pk, event.get("operator"))
    if r["fallback"]["readings"]:
        flags = [*flags, f"read by the fallback model ({r['fallback']['readings']} of {r['calls']} readings; "
                         f"Nova Lite: {', '.join(r['fallback']['errors'])})"]  # fmt: skip
    if d["model"] != "primary":
        flags = [*flags, f"drafted by {'the fallback model' if d['model'] == 'fallback' else 'the rules only'}"
                         f" (Nova Lite: {', '.join(d['errors'])})"]  # fmt: skip
    text, pii, u_out = mask_draft(bedrock, os.environ["DRAFTS_GUARDRAIL"], d["text"])
    if flags:
        text = f"> **Check:** {'; '.join(flags)}. Read the field report before approving.\n\n" + text
    fb_in = r["fallback"]["input_tokens"] + (d["input_tokens"] if d["model"] == "fallback" else 0)
    fb_out = r["fallback"]["output_tokens"] + (d["output_tokens"] if d["model"] == "fallback" else 0)
    tokens_in = r["input_tokens"] + (d["input_tokens"] if d["model"] == "primary" else 0)
    tokens_out = r["output_tokens"] + (d["output_tokens"] if d["model"] == "primary" else 0)
    cost = ((tokens_in * PRICE_IN + tokens_out * PRICE_OUT + fb_in * FALLBACK_PRICE_IN + fb_out * FALLBACK_PRICE_OUT)
            / 1e6 + _guard_cost(u_in, u_out))  # fmt: skip
    scale = float(os.environ.get("TIME_SCALE", "60"))
    state = {"case_id": case_id, "deadline": pk["deadline"], "level": 0, "start": int(time.time()),
             "marks": marks(pk["deadline"], float(event.get("elapsed_min", 0)), scale)}  # fmt: skip
    state["wait_s"] = wait_s(state)
    _append(table, case_id, _event("triaged", status=pk["status"], deadline=pk["deadline"], route=pk["route"],
                                   flags=flags, masked=pii, seconds=f"{time.time() - t0:.1f}",
                                   fallback_readings=r["fallback"]["readings"], drafted_by=d["model"]),
            report=report, packet=json.dumps(pk, default=str), draft=text, flags=flags,
            due_at=pk["due_at"] or "9999", decision_status=pk["status"], deadline=pk["deadline"] or "none",
            ai_cost_usd=f"{cost:.6f}", marks=state["marks"])  # fmt: skip
    if pk["deadline"] == "T3":
        notify(table, case_id, "primary", "New 3-hour case: approve or edit the draft now.")
    return state


def park(event: dict) -> None:
    state, token = event["case"], event["token"]
    status = "ESCALATED" if state["level"] >= 2 else "PENDING_APPROVAL"
    _append(_table(), state["case_id"], _event("waiting", level=state["level"], wait_s=state["wait_s"]),
            status=status, token=token, level=state["level"])  # fmt: skip


def escalate(event: dict) -> dict:
    state, table = dict(event["case"]), _table()
    state["level"] += 1
    steps = SCHEDULE[state["deadline"] or "T24"]
    if state["level"] > len(steps):
        _append(table, state["case_id"], _event("overdue"), status="OVERDUE")
        notify(table, state["case_id"], "primary+backup", "The reporting deadline passed with no approval.")
        return {**state, "overdue": True}
    _, who, msg = steps[state["level"] - 1]
    notify(table, state["case_id"], who, msg)
    state["wait_s"] = wait_s(state)
    return {**state, "overdue": False}


def close(event: dict) -> dict:
    state, d = event["case"], event["decision"]
    status = DECISIONS[d["decision"]]
    if (d["decision"] == "reject" or d.get("status_override")) and not d.get("reason"):
        raise ValueError("a rejection or an override needs a written reason")
    table = _table()
    item = table.get_item(Key={"case_id": state["case_id"]})["Item"]
    diff = None
    if d.get("draft") is not None:
        diff = "".join(difflib.unified_diff(item["draft"].splitlines(True), d["draft"].splitlines(True),
                                            "draft", "approved", n=1))  # fmt: skip
    sets = {"status": status, "final_draft": d.get("draft", item["draft"]) if status != "REJECTED" else None}
    _append(table, state["case_id"], _event("decided", decision=status, by=d["by"], reason=d.get("reason"),
                                            status_override=d.get("status_override"), diff=diff,
                                            level=state["level"]),
            **{k: v for k, v in sets.items() if v is not None})  # fmt: skip
    table.update_item(Key={"case_id": state["case_id"]}, UpdateExpression="REMOVE #t",
                      ExpressionAttributeNames={"#t": "token"})  # fmt: skip
    return {**state, "status": status}


def notify(table, case_id: str, who: str, message: str):
    """Page by SNS (D25: email in the demo). NOTIFY=off records the page without sending it."""
    sent = os.environ.get("NOTIFY", "on") == "on" and os.environ.get("TOPIC_ARN")
    if sent:
        import boto3

        boto3.client("sns", region_name=REGION).publish(
            TopicArn=os.environ["TOPIC_ARN"], Subject=f"[CER triage] {case_id}: {who}"[:100],
            Message=f"{message}\n\nCase {case_id}. Review: python -m cer_agent.approval show {case_id}")  # fmt: skip
    _append(table, case_id, _event("paged", who=who, message=message, sent=bool(sent)))


def triage_failed(event: dict) -> dict:
    """Triage raised (a model error that outlasted its retries, a timeout, a bug). The case must not vanish: it goes to
    the top of the queue as a report to read by hand, the primary approver is paged, and it waits on the 3-hour clock,
    the strictest there is."""
    case_id, err = event["case_id"], event.get("error") or {}
    kind = err.get("Error", "error")
    try:
        cause = json.loads(err.get("Cause") or "{}").get("errorMessage", "")
    except ValueError:
        cause = err.get("Cause", "")
    table = _table()
    note = (f"# Triage failed: read this report by hand\n\nThe system couldn't read this report ({kind}). Decide "
            f"whether it must be reported and by when, as if it were a 3-hour case, and file by hand.\n\n"
            f"## Field report\n\n{event.get('report', '')}\n")  # fmt: skip
    table.update_item(Key={"case_id": case_id},
                      UpdateExpression="SET #h = list_append(if_not_exists(#h, :empty), :e), #s = :s, due_at = :d, "
                                       "draft = :n, flags = :f, decision_status = :u, deadline = :u, report = :r",
                      ExpressionAttributeNames={"#h": "history", "#s": "status"},
                      ExpressionAttributeValues={":empty": [], ":e": [_event("triage_failed", error=kind,
                                                                              cause=cause[:500])],
                                                 ":s": "IN_PROGRESS", ":d": "0000", ":n": note,
                                                 ":f": [f"triage failed: {kind}"], ":u": "unknown",
                                                 ":r": event.get("report", "")})  # fmt: skip
    notify(table, case_id, "primary", f"Triage failed ({kind}): read this report by hand now.")
    state = {
        "case_id": case_id,
        "deadline": "T3",
        "level": 0,
        "start": int(time.time()),
        "marks": marks("T3", float(event.get("elapsed_min", 0)), float(os.environ.get("TIME_SCALE", "60"))),
    }
    state["wait_s"] = wait_s(state)
    return state


def handler(event, context=None):
    steps = {"triage": triage, "triage_failed": triage_failed, "park": park, "escalate": escalate, "close": close}
    return steps[event["step"]](event)


# --- Approver CLI ---


def _sfn():
    import boto3

    return boto3.client("stepfunctions", region_name=REGION)


def _state_machine_arn() -> str:
    for page in _sfn().get_paginator("list_state_machines").paginate():
        for m in page["stateMachines"]:
            if m["name"] == STATE_MACHINE:
                return m["stateMachineArn"]
    raise SystemExit(f"No state machine {STATE_MACHINE}: apply infra/approval.tf first.")


def submit(case_ids: list[str], run_tag: str) -> list[str]:
    """Start a run per test-set report, as if it arrived at discovery (elapsed 0)."""
    path = pathlib.Path(__file__).resolve().parents[2] / "evals/cases/cases.jsonl"
    cases = {c["id"]: c for c in map(json.loads, path.read_text(encoding="utf-8").splitlines())}
    arn, out = _state_machine_arn(), []
    for cid in case_ids:
        c = cases[cid]
        case_id = f"{cid}-{run_tag}"
        _sfn().start_execution(stateMachineArn=arn, name=case_id, input=json.dumps(
            {"case_id": case_id, "report": c["report"], "received": c["discovered_at"][:10], "operator": c["operator"],
             "source": f"test set {cid}", "elapsed_min": 0}))  # fmt: skip
        out.append(case_id)
    return out


def queue() -> list[dict]:
    from boto3.dynamodb.conditions import Key

    rows = []
    for st in OPEN:
        rows += _table().query(IndexName="queue", KeyConditionExpression=Key("status").eq(st))["Items"]
    return sorted(rows, key=lambda r: r["due_at"])


def override_mismatch(status: str, draft: str) -> str | None:
    """Why an edited draft contradicts a status override, or None. The approved text is what gets filed, so it must
    say what the approver decided: PIR-3 Yes only for precautionary; a file note only for not reportable."""
    if status not in ("reportable", "precautionary", "not reportable"):
        return f"unknown status {status!r}"
    note = "# File note" in draft and "# Draft Preliminary Incident Report" not in draft
    if status == "not reportable":
        return None if note else "a not-reportable override needs the file note, not a draft notice"
    if note:
        return "a reportable or precautionary override needs a draft notice, not a file note"
    m = re.search(r"\*\*PIR-3 Precautionary:\*\*\s*(Yes|No)", draft)
    if not m:
        return "the draft has no PIR-3 line"
    if (m.group(1) == "Yes") != (status == "precautionary"):
        return f"PIR-3 says {m.group(1)!r} but the override is {status!r}; edit PIR-3 too"
    return None


def decide(
    case_id: str,
    decision: str,
    by: str,
    reason: str | None = None,
    draft_file: pathlib.Path | None = None,
    status_override: str | None = None,
):
    if (decision == "reject" or status_override) and not reason:
        raise SystemExit("A rejection or an override needs --reason.")
    if status_override and (problem := override_mismatch(status_override, draft_file.read_text(encoding="utf-8"))):
        raise SystemExit(f"The edited draft doesn't match the override: {problem}")
    item = _table().get_item(Key={"case_id": case_id}).get("Item")
    if not item or item.get("status") not in OPEN or not item.get("token"):
        raise SystemExit(f"{case_id} isn't waiting for a decision (status {item and item.get('status')}).")
    out = {"decision": decision, "by": by, "reason": reason, "status_override": status_override}
    if draft_file:
        out["draft"] = draft_file.read_text(encoding="utf-8")
    try:
        _sfn().send_task_success(taskToken=item["token"], output=json.dumps(out))
    except Exception as e:  # the case escalated between reading the token and sending it: read it again
        code = getattr(e, "response", {}).get("Error", {}).get("Code")
        if code in ("TaskTimedOut", "InvalidToken", "TaskDoesNotExist"):
            raise SystemExit(f"{case_id} escalated just now; run the command again.") from e
        raise


def measure(case_ids: list[str]) -> dict:
    """Per run, from Step Functions' own history ($0): transitions, wall time to the queue, decision time, Lambda
    billed time; plus the AI cost the triage step recorded."""
    arn, sfn, table = _state_machine_arn(), _sfn(), _table()
    region_arn = arn.replace(":stateMachine:", ":execution:")
    rows = []
    for cid in case_ids:
        ex = f"{region_arn}:{cid}"
        events = [e for p in sfn.get_paginator("get_execution_history").paginate(executionArn=ex)
                  for e in p["events"]]  # fmt: skip
        desc = sfn.describe_execution(executionArn=ex)
        entered = [e for e in events if e["type"].endswith("StateEntered")]
        t0 = events[0]["timestamp"]
        parked = next((e["timestamp"] for e in events if e["type"] == "TaskSubmitted"
                       and "waitForTaskToken" in json.dumps(e.get("taskSubmittedEventDetails", {}))), None)  # fmt: skip
        lam_ms = 0
        for e in events:  # Lambda task durations: scheduled -> succeeded, excluding the token waits
            if e["type"] == "TaskSucceeded":
                start = next(x for x in events if x["id"] == e["previousEventId"])
                if start["type"] == "TaskStarted":
                    lam_ms += (e["timestamp"] - start["timestamp"]).total_seconds() * 1000
        item = table.get_item(Key={"case_id": cid}).get("Item", {})
        mem_gb = 0.5
        infra = len(entered) * SFN_TRANSITION + lam_ms / 1000 * mem_gb * LAMBDA_GB_S + 4 * LAMBDA_REQ
        rows.append({"case": cid, "status": item.get("status"), "run": desc["status"],
                     "decision": item.get("decision_status"), "deadline": item.get("deadline"),
                     "transitions": len(entered),
                     "to_queue_s": round((parked - t0).total_seconds(), 1) if parked else None,
                     "total_s": round(((desc.get("stopDate") or dt.datetime.now(dt.UTC)) - t0).total_seconds(), 1),
                     "pages": sum(1 for h in item.get("history", []) if h["event"] == "paged"),
                     "ai_cost_usd": float(item.get("ai_cost_usd", 0)), "infra_cost_usd": round(infra, 7)})  # fmt: skip
    return {"runs": rows}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="The approval gate: submit, queue, show, decide, measure.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("submit")
    s.add_argument("ids", nargs="+")
    s.add_argument("--tag", default=dt.datetime.now().strftime("%H%M%S"))
    sub.add_parser("queue")
    for name in ("show", "history"):
        sub.add_parser(name).add_argument("case")
    for name in DECISIONS:
        p = sub.add_parser(name)
        p.add_argument("case")
        p.add_argument("--by", required=True)
        p.add_argument("--reason")
        if name == "edit":
            p.add_argument("--draft", type=pathlib.Path, required=True)
            p.add_argument("--status", dest="status_override")
    m = sub.add_parser("measure")
    m.add_argument("cases", nargs="+")
    args = ap.parse_args(argv)
    if args.cmd == "submit":
        print("\n".join(submit(args.ids, args.tag)))
    elif args.cmd == "queue":
        for r in queue():
            print(f"{r['status']:<17} {r['due_at'][:16]:<17} {r.get('deadline', ''):<5} "
                  f"{r.get('decision_status', ''):<15} {r['case_id']}")  # fmt: skip
    elif args.cmd in ("show", "history"):
        item = _table().get_item(Key={"case_id": args.case}).get("Item")
        if not item:
            raise SystemExit(f"No case {args.case}.")
        if args.cmd == "show":
            print(
                f"{item['case_id']}: {item['status']}  (rules: {item.get('decision_status')}, "
                f"{item.get('deadline')}, due {item.get('due_at')})\n"
            )
            print(item.get("draft", "(no draft yet)"))
        print(json.dumps(item.get("history", []), indent=2, default=str))
    elif args.cmd in DECISIONS:
        decide(args.case, args.cmd, args.by, args.reason, getattr(args, "draft", None),
               getattr(args, "status_override", None))  # fmt: skip
        print(f"{args.case}: {DECISIONS[args.cmd]} sent.")
    elif args.cmd == "measure":
        print(json.dumps(measure(args.cases), indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
