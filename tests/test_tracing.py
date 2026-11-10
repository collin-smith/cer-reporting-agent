"""Per-stage tracing without a model: spans nest under the case, carry tokens, and the summary adds them up."""

import json

from cer_agent import tracing


def test_spans_nest_under_the_case_and_the_summary_counts_tokens(tmp_path):
    path = tmp_path / "traces.jsonl"
    provider = tracing.setup(path)
    with tracing.span("case", id="CL-001"):
        with tracing.span("extract") as s:
            tracing.usage(s, 2000, 300)
        with tracing.span("decide", status="reportable"):
            pass
    provider.shutdown()
    spans = {s["name"]: s for s in map(json.loads, path.read_text().splitlines())}
    assert spans["extract"]["parent_id"] == spans["case"]["span_id"] == spans["decide"]["parent_id"]
    assert spans["case"]["attributes"]["cer.id"] == "CL-001"
    rows = {r["stage"]: r for r in tracing.summary(list(spans.values()))}
    assert rows["extract"]["input_tokens"] == 2000 and rows["extract"]["cost_usd"] == (2000 * 0.064 + 300 * 0.256) / 1e6
    assert list(rows)[:3] == ["case", "extract", "decide"]
    assert "| extract | 1 | 1 |" in tracing.render(list(rows.values()))


def test_an_error_is_recorded_on_its_span(tmp_path):
    path = tmp_path / "traces.jsonl"
    provider = tracing.setup(path)
    try:
        with tracing.span("draft"):
            raise ValueError("model reply malformed")
    except ValueError:
        pass
    provider.shutdown()
    (s,) = map(json.loads, path.read_text().splitlines())
    assert s["status"] == "ERROR" and s["errors"] == ["model reply malformed"]


def test_without_setup_spans_are_free_and_write_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(tracing, "_provider", None)
    with tracing.span("decide") as s:
        tracing.usage(s, 1, 1)
    assert not list(tmp_path.iterdir())
