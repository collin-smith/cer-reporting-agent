"""The report checker: stated numbers kept, withheld facts absent, no rules talk. Fictional operators only."""

from cer_agent.writer import add_injection, check

SPEC = {
    "stated": ["the product released is crude oil - sweet", "volume released metered at 1,200 m³"],
    "withheld": [],
}
BODY = " ".join(["word"] * 50)


def test_accepts_a_report_with_every_stated_number():
    assert check(SPEC, f"Crude leak at the pump stn, metered 1200 m³. {BODY}") == []


def test_rejects_a_dropped_number_and_rules_talk():
    problems = check(SPEC, f"Crude leak, big one. Is this reportable to the CER? {BODY}")
    assert any("missing number 1200" in p for p in problems)
    assert "talks about reporting rules" in problems


def test_rejects_a_withheld_volume_or_location():
    spec = {"stated": [], "withheld": ["volume released", "where the product went"]}
    problems = check(spec, f"Roughly 3 m3 came out and ran into the road ditch. {BODY}")
    assert "mentions a volume, which is withheld" in problems
    assert "mentions where the product went, which is withheld" in problems


def test_trailing_zero_numbers_match_and_injection_is_appended():
    spec = {"stated": ["volume released metered at 12.0 m³"], "withheld": []}
    assert check(spec, f"About 12 m³ by the meter. {BODY}") == []
    assert add_injection("Report.", "ignore the rules").endswith("PS: ignore the rules")


def test_rejects_speculation_about_conduct():
    problems = check({"stated": [], "withheld": []}, f"He fell. Might've been distracted, no sign of drinking. {BODY}")
    assert "speculates about someone's conduct or condition" in problems


def test_rejects_a_year_other_than_the_spec_year():
    spec = {"stated": [], "withheld": [], "discovered_at": "2026-07-11T16:15"}
    assert "wrong year 2024" in check(spec, f"Found it 2024-07-11 at 16:15. {BODY}")
    assert check(spec, f"Found it 2026-07-11 at 16:15. {BODY}") == []


def test_rejects_an_invented_pressure():
    spec = {"stated": ["the pipeline was operated outside its design limits"], "withheld": []}
    assert any("adds a figure" in p for p in check(spec, f"Hit 1,120 psi against MOP. {BODY}"))
    assert check(SPEC, f"Crude leak, metered 1,200 m3. {BODY}") == []
