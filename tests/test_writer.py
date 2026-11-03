"""The report checker: stated numbers kept, withheld facts absent, no rules talk. Fictional operators only."""

from cer_agent.writer import add_injection, check, prompt

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


def test_rejects_a_report_without_the_time_it_was_found():
    spec = {**SPEC, "discovered_at": "2026-05-26T16:15"}
    ok = f"Crude leak at the pump stn, found 4:15 pm, metered 1200 m³. {BODY}"
    assert check(spec, ok) == []
    assert check(spec, ok.replace("4:15 pm", "this afternoon")) == ["missing the time it was found (16:15)"]
    # A key ruling on the time (cases.KEY_RULINGS) is what the report must carry.
    ruled = {**spec, "facts": {"discovered_at": "2026-05-26T08:45:00"}}
    assert check(ruled, f"Crude leak, valve let go around 0845, metered 1200 m³. {BODY}") == []


def test_states_the_time_as_a_fact():
    context = dict.fromkeys(("what_happened", "detail", "equipment", "activity", "how_discovered"), "")
    spec = {**SPEC, "discovered_at": "2026-05-26T16:15", "operator": "Prairie Midstream Ltd.", "town": "Gretna",
            "province": "MB", "style": "texts", "reporter": "field operator", "context": context}  # fmt: skip
    assert "FACTS:\n- found at 16:15 on May 26" in prompt(spec)


def test_no_release_case_rejects_a_described_release_or_an_open_fire():
    spec = {"stated": [], "withheld": [], "facts": {"release": False, "fire_or_explosion": True,
            "fire_linked_to_pipeline": True, "open_points": {}}}  # fmt: skip
    assert check(spec, f"Fire at our compressor. Nothing leaked, no sheen. {BODY}") == []
    assert any("describes a release" in p for p in check(spec, f"Fire at our compressor, small sheen. {BODY}"))
    assert any("what fed the fire" in p for p in check(spec, f"Fire at our site, not sure what's burning. {BODY}"))
    assert any("away from our facility" in p for p in check(spec, f"Fire near our pipeline, nothing leaked. {BODY}"))


def test_a_toxic_plume_needs_people_to_evacuate_or_shelter():
    spec = {"stated": [], "withheld": [], "facts": {"toxic_plume": True}}
    assert check(spec, f"Smoke was bad, people nearby had to shelter in place. {BODY}") == []
    assert check(spec, f"Smoke was bad, had to clear the guys out. {BODY}") == [
        "the fumes must make people evacuate or shelter, in those words"
    ]
