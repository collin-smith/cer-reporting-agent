"""Per-stage tracing (article 2): one OpenTelemetry span per stage of each case, written to a local JSONL file.

Our own stages (extract, decide, draft, judge) open spans with `span()`; the agent's review comes from Strands,
which emits OpenTelemetry spans of its own (invoke_agent, each event-loop cycle, each model call with token counts,
each tool call) to the same provider. Without `setup()`, OpenTelemetry's default no-op provider makes every span
free, so tracing costs nothing unless a run asks for it.

Local JSONL first ($0, no AWS). In the deployed gate (article 7, D58) the same spans go to stdout, so into the
Lambda's CloudWatch log group, without touching the instrumented code.

Usage:
    python -m cer_agent.tracing summary path/to/traces.jsonl   # per-stage table
"""

from __future__ import annotations

import argparse
import contextlib
import json
import math
import pathlib
import statistics
import sys
import threading

from opentelemetry import trace

TRACER = "cer_agent"
MAX_TEXT = 300  # long attribute strings (prompts, reports) are cut: the trace is for timing and flow, not content
_lock = threading.Lock()
_provider = None  # ours, once setup() runs; OpenTelemetry allows the global provider to be set only once


def record(s) -> dict:
    """One finished span as a flat dict. Span events (Strands records the prompt and completion text as events) are
    dropped, except exceptions."""
    attrs = {k: (v[:MAX_TEXT] if isinstance(v, str) else list(v) if isinstance(v, tuple) else v)
             for k, v in (s.attributes or {}).items()}  # fmt: skip
    errors = [e.attributes.get("exception.message", "")[:MAX_TEXT] for e in s.events if e.name == "exception"]
    return {
        "trace_id": f"{s.context.trace_id:032x}", "span_id": f"{s.context.span_id:016x}",
        "parent_id": f"{s.parent.span_id:016x}" if s.parent else None, "name": s.name,
        "start_ms": s.start_time / 1e6, "duration_ms": (s.end_time - s.start_time) / 1e6,
        "status": s.status.status_code.name, "attributes": attrs, **({"errors": errors} if errors else {}),
    }  # fmt: skip


class JsonlExporter:
    """An OpenTelemetry span exporter that appends one JSON line per finished span to a file."""

    def __init__(self, path: pathlib.Path):
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)

    def export(self, spans) -> object:
        from opentelemetry.sdk.trace.export import SpanExportResult

        lines = [json.dumps(record(s), default=str) for s in spans]
        with _lock, self.path.open("a", encoding="utf-8") as fh:
            fh.write("".join(line + "\n" for line in lines))
        return SpanExportResult.SUCCESS

    def shutdown(self) -> None:
        pass

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True


class StdoutExporter(JsonlExporter):
    """The same lines on stdout, marked `"cer_span": 1` (article 7, D58). In Lambda, stdout is the function's log
    group, so the gate's spans land in CloudWatch Logs with no exporter endpoint, agent or extra permission, and Logs
    Insights queries them (`filter ispresent(cer_span)`)."""

    def __init__(self, stream=None):
        self.stream = stream

    def export(self, spans) -> object:
        from opentelemetry.sdk.trace.export import SpanExportResult

        out = self.stream or sys.stdout
        with _lock:
            out.write("".join(json.dumps({"cer_span": 1, **record(s)}, default=str) + "\n" for s in spans))
            out.flush()
        return SpanExportResult.SUCCESS


def setup(path: pathlib.Path | None, stream=None):
    """Send every span (ours and Strands') to `path`, or to stdout (or `stream`) when `path` is None. Returns the
    provider; call its shutdown() at the end."""
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor

    provider = TracerProvider(resource=Resource.create({"service.name": "cer-reporting-agent"}))
    provider.add_span_processor(SimpleSpanProcessor(JsonlExporter(path) if path else StdoutExporter(stream)))
    global _provider
    _provider = provider
    trace.set_tracer_provider(provider)  # for Strands' spans (ignored with a warning if already set)
    return provider


@contextlib.contextmanager
def span(name: str, **attrs):
    """A span for one of our stages, as the current span (children nest under it). Attributes are prefixed
    `cer.`; set more inside with `s.set_attribute`. An exception is recorded on the span and re-raised."""
    with (_provider or trace).get_tracer(TRACER).start_as_current_span(name) as s:
        for k, v in attrs.items():
            if v is not None:
                s.set_attribute(f"cer.{k}", v)
        yield s


def usage(s, input_tokens: int, output_tokens: int, retries: int = 0, cache_read: int = 0,
          cache_write: int = 0) -> None:  # fmt: skip
    """Token counts on our model-calling spans, under the same names Strands uses, so the summary adds them up."""
    s.set_attribute("gen_ai.usage.input_tokens", input_tokens)
    s.set_attribute("gen_ai.usage.output_tokens", output_tokens)
    if cache_read or cache_write:
        s.set_attribute("gen_ai.usage.cache_read_input_tokens", cache_read)
        s.set_attribute("gen_ai.usage.cache_write_input_tokens", cache_write)
    if retries:
        s.set_attribute("cer.retries", retries)


# --- Summary ---


# Span name -> stage label. Strands names its spans "invoke_agent <name>" and "execute_tool <tool>".
def stage(name: str) -> str:
    if name.startswith("invoke_agent"):
        return "review (agent)"
    if name.startswith("execute_tool"):
        return "  tool: " + name.split(" ", 1)[1]
    return {"chat": "  model call (agent)", "execute_event_loop_cycle": "  agent turn"}.get(name, name)


def _p(values: list[float], q: float) -> float:
    v = sorted(values)
    return v[min(len(v) - 1, math.ceil(q * len(v)) - 1)] if v else 0.0


def summary(spans: list[dict], price_in: float = 0.064, price_out: float = 0.256) -> list[dict]:
    """Per stage: spans, cases it ran in, p50 / p95 time, tokens, cost (USD per 1M tokens: Nova Lite list price by
    default), and the stage's share of total case time (spans nest, so the shares of nested stages overlap)."""
    cases = [s for s in spans if s["name"] == "case"]
    case_ms = sum(s["duration_ms"] for s in cases) or 1.0
    groups: dict[str, list[dict]] = {}
    for s in spans:
        groups.setdefault(stage(s["name"]), []).append(s)
    out = []
    for name, ss in groups.items():
        tin = sum(s["attributes"].get("gen_ai.usage.input_tokens", 0) for s in ss)
        tout = sum(s["attributes"].get("gen_ai.usage.output_tokens", 0) for s in ss)
        if name.startswith("review"):  # the agent's tokens are on its model-call spans; don't count them twice
            tin = tout = 0
        out.append({"stage": name, "spans": len(ss), "cases": len({s["trace_id"] for s in ss}),
                    "p50_ms": statistics.median(ms := [s["duration_ms"] for s in ss]), "p95_ms": _p(ms, 0.95),
                    "input_tokens": tin, "output_tokens": tout, "cost_usd": (tin * price_in + tout * price_out) / 1e6,
                    "share": sum(s["duration_ms"] for s in ss) / case_ms,
                    "errors": sum(s["status"] == "ERROR" for s in ss)})  # fmt: skip
    order = ["case", "extract", "review (agent)", "decide", "draft", "judge (code)", "judge (model)"]
    return sorted(out, key=lambda r: (order.index(r["stage"]) if r["stage"] in order else 2.5, r["stage"]))


def render(rows: list[dict]) -> str:
    lines = ["| Stage | Spans | Cases | p50 | p95 | Tokens in / out | Cost | Share of case time | Errors |",
             "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for r in rows:
        lines.append(f"| {r['stage']} | {r['spans']} | {r['cases']} | {r['p50_ms'] / 1000:.2f} s | "
                     f"{r['p95_ms'] / 1000:.2f} s | {r['input_tokens']:,} / {r['output_tokens']:,} | "
                     f"${r['cost_usd']:.5f} | {r['share']:.0%} | {r['errors']} |")  # fmt: skip
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Summarise a traces.jsonl file by stage.")
    ap.add_argument("command", choices=["summary"])
    ap.add_argument("path", type=pathlib.Path)
    args = ap.parse_args(argv)
    spans = [json.loads(line) for line in args.path.read_text(encoding="utf-8").splitlines()]
    print(render(summary(spans)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
