"""Intake mapping: the model's answers become Facts with the three states kept apart. No model calls."""

import datetime as dt

from cer_agent.extract import to_facts
from cer_agent.rules import COMPANY_PROPERTY, OFF_RIGHT_OF_WAY, decide

BASE = {"death": "no", "injury": "none", "env_effect": "none", "fire_or_explosion": "no", "release": "no",
        "rupture": "no", "toxic_plume": "no"}  # fmt: skip


def test_units_are_converted_in_code():
    f = to_facts({**BASE, "release": "yes", "substance": "crude oil - sweet", "volume": 2000, "volume_unit": "L",
                  "lands": ["company_property"], "discovered_time": "16:15"}, dt.date(2026, 7, 11))  # fmt: skip
    assert f.volume_m3 == 2.0 and f.lands == {COMPANY_PROPERTY}
    assert f.discovered_at == dt.datetime(2026, 7, 11, 16, 15)
    assert decide(f).status == "reportable"


def test_unknown_is_missing_and_unclear_is_open():
    f = to_facts({**BASE, "release": "unknown"})
    assert f.release is None and "release" in decide(f).missing
    f = to_facts({**BASE, "injury": "unclear"})
    assert f.open_points["serious_injury"] == [False, True] and decide(f).route == "judgment"


def test_disagreeing_accounts_become_conflicts():
    f = to_facts({**BASE, "release": "yes", "substance": "crude oil - sweet", "volume": 1, "volume_alternatives": [2.5],
                  "lands_alternatives": [["company_property"], ["off_right_of_way"]]})  # fmt: skip
    assert f.conflicts["volume_m3"] == [1.0, 2.5]
    assert f.conflicts["lands"] == [{COMPANY_PROPERTY}, {OFF_RIGHT_OF_WAY}]
    assert decide(f).route == "judgment"


def test_no_release_means_nothing_left_the_site():
    assert to_facts(BASE).lands == {COMPANY_PROPERTY}


def test_dates_take_missing_parts_from_the_received_date():
    rx = dt.date(2026, 4, 4)
    at = lambda d, t="00:20": to_facts({"discovered_date": d, "discovered_time": t}, rx).discovered_at  # noqa: E731
    assert at("2023-04-04") == dt.datetime(2026, 4, 4, 0, 20)  # invented year ("apr 4")
    assert at("2023-01-04") == dt.datetime(2026, 4, 4, 0, 20)  # invented month too ("on the 4th")
    assert at("2020-03-28") == dt.datetime(2026, 3, 28, 0, 20)  # invented year, recent month kept
    assert at("2026-04-02") == dt.datetime(2026, 4, 2, 0, 20)  # a stated recent date is kept
    assert at("2025-12-30", "23:00") == dt.datetime(2025, 12, 30, 23, 0)  # a plausible year is kept as stated
    assert to_facts({"discovered_date": "2025-12-31", "discovered_time": "23:00"},
                    dt.date(2026, 1, 2)).discovered_at == dt.datetime(2025, 12, 31, 23, 0)  # year boundary  # fmt: skip


def test_an_unknown_date_keeps_the_time_and_odd_time_formats_parse():
    rx = dt.date(2026, 1, 20)
    for t in ("17:30", "1730", "17h30", "17.30"):
        assert to_facts({"discovered_date": "unknown", "discovered_time": t}, rx).discovered_at == dt.datetime(
            2026, 1, 20, 17, 30
        )
    assert to_facts({"discovered_time": "0845"}, rx).discovered_at == dt.datetime(2026, 1, 20, 8, 45)
    assert to_facts({"discovered_time": "unknown"}, rx).discovered_at is None
    assert to_facts({"discovered_time": "25:00"}, rx).discovered_at is None


def test_a_zero_rate_is_a_blank():
    assert to_facts({"release": "yes", "rate": 0.0, "rate_unit": "kg/s"}).rate_kg_s is None


def test_a_rupture_without_a_quote_stays_a_rupture():
    # A missed rupture is a late 3 h notice: the evidence field steers the model but never overrides a yes.
    assert to_facts({**BASE, "rupture": "yes"}).rupture is True
    assert to_facts({**BASE, "rupture": "yes", "rupture_quote": "line ruptured"}).rupture is True


def test_h2s_detected_on_a_sweet_line_is_a_conflict():
    gas = {**BASE, "release": "yes", "substance": "natural gas - sweet", "through_pipe_body_or_weld": "yes",
           "volume": 300}  # fmt: skip
    f = to_facts({**gas, "h2s_detected": "yes"})
    assert f.conflicts["substance"] == ["natural gas - sour", "natural gas - sweet"]
    assert (decide(f).deadline, decide(f).route) == ("T3", "judgment")
    assert "substance" not in to_facts({**gas, "h2s_detected": "no"}).conflicts


def test_a_location_conflict_counts_the_stated_account():
    # JU-128: inside the fence in lands, the road ditch only in lands_alternatives.
    f = to_facts({**BASE, "release": "yes", "substance": "crude oil - sweet", "volume": 2.5, "volume_basis": "metered",
                  "lands": ["company_property"], "lands_alternatives": [["off_right_of_way"]]})  # fmt: skip
    assert sorted(map(sorted, f.conflicts["lands"])) == [["company_property"], ["off_right_of_way"]]
    assert (decide(f).deadline, decide(f).route) == ("T3", "judgment")


def test_a_malformed_tool_call_is_retried_then_raised():
    import datetime as dt

    import pytest

    from cer_agent.extract import MODEL_ERROR_RETRIES, extract

    class ModelError(Exception):
        response = {"Error": {"Code": "ModelErrorException"}}

    ok = {"output": {"message": {"content": [{"toolUse": {"input": {"release": "no"}}}]}},
          "usage": {"inputTokens": 10, "outputTokens": 5}}  # fmt: skip

    class Client:
        def __init__(self, fails):
            self.fails, self.calls, self.seen = fails, 0, []

        def converse(self, **kw):
            self.seen.append(kw)
            self.calls += 1
            if self.calls <= self.fails:
                raise ModelError()
            return ok

    c = Client(fails=1)
    x = extract(c, "m", "report", dt.date(2026, 7, 1))
    assert x["raw"] == {"release": "no"} and c.calls == 2 and x["retries"] == 1
    assert [kw["inferenceConfig"]["temperature"] for kw in c.seen] == [0, 0.3]
    with pytest.raises(ModelError):
        extract(Client(fails=MODEL_ERROR_RETRIES + 1), "m", "report")


def test_prompt_cache_point_only_when_switched_on(monkeypatch):
    """D53: CER_PROMPT_CACHE=1 adds a cache point after the system prompt (Nova takes none in tools), and the
    reading carries Bedrock's cache counts."""
    from cer_agent.extract import CACHE_POINT, extract

    reply = {"output": {"message": {"content": [{"toolUse": {"input": {"release": "no"}}}]}},
             "usage": {"inputTokens": 200, "outputTokens": 5, "cacheReadInputTokens": 2600}}  # fmt: skip

    class Client:
        def __init__(self):
            self.seen = []

        def converse(self, **kw):
            self.seen.append(kw)
            return reply

    monkeypatch.delenv("CER_PROMPT_CACHE", raising=False)
    c = Client()
    extract(c, "m", "report")
    assert CACHE_POINT not in c.seen[0]["system"]
    monkeypatch.setenv("CER_PROMPT_CACHE", "1")
    x = extract(c, "m", "report")
    assert c.seen[1]["system"][-1] == CACHE_POINT and "cachePoint" not in str(c.seen[1]["toolConfig"])
    assert (x["input_tokens"], x["cache_read_tokens"], x["cache_write_tokens"]) == (200, 2600, 0)
