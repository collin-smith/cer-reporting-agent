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
