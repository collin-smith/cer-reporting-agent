"""The $0 eval gate: it passes on the committed code and baseline, and its comparison flags anything worse."""

from cer_agent import gate, rules

BASE = {"run": {"n": 10, "status": 9, "route": 8, "missed": 0, "late": 0, "over_notify": 1}}


def test_compare_flags_only_changes_for_the_worse():
    same = {"run": {"counts": dict(BASE["run"])}}
    assert gate.compare(BASE, same) == []
    better = {"run": {"counts": {**BASE["run"], "status": 10, "over_notify": 0}}}
    assert gate.compare(BASE, better) == []
    worse = {"run": {"counts": {**BASE["run"], "missed": 1, "route": 7}}}
    assert gate.compare(BASE, worse) == ["run: route 7 < baseline 8", "run: missed 1 > baseline 0"]
    assert gate.compare(BASE, {}) == ["run: no longer gated"]


def test_gate_passes_on_the_committed_code_and_fails_on_a_threshold_bug(monkeypatch):
    assert gate.main([]) == 0
    monkeypatch.setattr(rules, "LVP_LINE_M3", 2.0)  # INC-d is 1.5 m3: a mis-set threshold must fail the gate
    assert gate.main([]) == 1
