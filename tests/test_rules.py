"""The rules engine against the worked examples in input/cer/rules-spec.md. Operators in the spec are fictional."""

import datetime as dt

from cer_agent.rules import COMPANY_PROPERTY, OFF_RIGHT_OF_WAY, RIGHT_OF_WAY, Facts, decide

T0 = dt.datetime(2026, 11, 2, 2, 0)


def test_inc_a_broken_radius_is_serious_and_3h():
    d = decide(Facts(discovered_at=T0, serious_injury=True))
    assert d.status == "reportable" and d.incident_types == ["INC-a"]
    assert d.deadline == "T3" and "T3-INJURY" in d.deadline_rules
    assert d.due_at == T0 + dt.timedelta(hours=3)


def test_inc_b_drilling_mud_in_fish_creek_is_24h():
    d = decide(Facts(env_effect="significant"))
    assert (d.status, d.incident_types, d.deadline) == ("reportable", ["INC-b"], "T24")


def test_minor_env_effect_is_not_reportable():
    d = decide(Facts(env_effect="minor"))
    assert d.status == "not reportable" and "OUT-MINOR-ENV" in d.citations


def test_inc_c_ups_battery_fire_is_24h_without_rupture_or_plume():
    d = decide(Facts(fire_or_explosion=True))
    assert (d.incident_types, d.deadline) == (["INC-c"], "T24")


def test_inc_d_crude_in_station_containment_is_24h():
    d = decide(Facts(release=True, substance="Crude Oil - Sweet", volume_m3=2.0, lands={COMPANY_PROPERTY}))
    assert (d.incident_types, d.deadline, d.route) == (["INC-d"], "T24", "clear-cut")


def test_lvp_at_or_under_1_5_is_out():
    d = decide(Facts(release=True, substance="Crude Oil - Sweet", volume_m3=1.2))
    assert d.status == "not reportable" and "OUT-LVP15" in d.citations


def test_t3_lvp_crude_over_the_right_of_way():
    d = decide(Facts(release=True, substance="Crude Oil - Sweet", volume_m3=3.0, lands={RIGHT_OF_WAY}))
    assert d.deadline == "T3" and "T3-LVP" in d.deadline_rules


def test_inc_e_weld_crack_any_size_is_reportable():
    d = decide(Facts(release=True, substance="Natural Gas - Sweet", volume_m3=5.0, through_pipe_body_or_weld=True))
    assert (d.incident_types, d.deadline) == (["INC-e"], "T24")


def test_packing_weep_under_0_1_kg_s_is_out():
    d = decide(Facts(release=True, substance="Natural Gas - Sweet", volume_m3=5.0, rate_kg_s=0.02))
    assert d.status == "not reportable" and "OUT-GASRATE" in d.citations


def test_planned_blowdown_is_excluded():
    d = decide(Facts(release=True, substance="Natural Gas - Sweet", volume_m3=900.0, planned_venting=True))
    assert d.status == "not reportable" and "OUT-VENT" in d.citations


def test_sour_gas_is_3h_any_size():
    d = decide(Facts(release=True, substance="Natural Gas - Sour", volume_m3=1.0, rate_kg_s=0.2))
    assert d.deadline == "T3" and "T3-SOUR" in d.deadline_rules


def test_propane_40_m3_liquid_is_about_10800_m3_gas_so_24h():
    d = decide(
        Facts(release=True, substance="Propane", volume_m3=40.0, volume_state="liquid", rate_kg_s=0.5, lands=None)
    )
    assert d.incident_types == ["INC-e"] and d.deadline == "T24"


def test_hvp_volume_without_a_unit_is_precautionary_3h():
    d = decide(Facts(release=True, substance="Propane", volume_m3=200.0, rate_kg_s=0.5))
    assert d.status == "precautionary" and d.deadline == "T3" and "volume_state" in d.missing
    assert d.route == "clear-cut"  # missing facts never make a judgment case (D23)


def test_inc_f_mop_threshold_is_10_percent_or_35_kpa():
    assert decide(Facts(pressure_kpa=6700, limit_kpa=6000)).incident_types == ["INC-f"]
    assert decide(Facts(pressure_kpa=6550, limit_kpa=6000)).status == "not reportable"
    assert decide(Facts(pressure_kpa=330, limit_kpa=300)).status == "not reportable"  # 35 kPa floor: line is 335
    assert decide(Facts(pressure_kpa=4810, limit_kpa=4800, limit_type="rop")).incident_types == ["INC-f"]
    assert decide(Facts(other_beyond_design="exposure")).incident_types == ["INC-f"]


def test_rupture_is_3h_whatever_the_volume():
    d = decide(Facts(release=True, substance="Natural Gas - Sweet", volume_m3=10.0, through_pipe_body_or_weld=True,
                     rupture=True))  # fmt: skip
    assert d.deadline == "T3" and "T3-RUPTURE" in d.deadline_rules


def test_route_rupture_with_uncertain_env_effect_is_clear_cut():
    f = Facts(release=True, substance="Natural Gas - Sweet", volume_m3=10.0, through_pipe_body_or_weld=True,
              rupture=True, open_points={"env_effect": ["minor", "significant"]})  # fmt: skip
    d = decide(f)
    assert d.route == "clear-cut" and d.deadline == "T3"


def test_route_missing_volume_on_row_is_precautionary_3h_clear_cut():
    d = decide(Facts(release=True, substance="Crude Oil - Sweet", volume_m3=None, lands={RIGHT_OF_WAY}))
    assert (d.status, d.deadline, d.route) == ("precautionary", "T3", "clear-cut")
    assert d.missing == ["volume_m3"]


def test_route_mud_in_wetland_is_judgment_u1():
    d = decide(Facts(open_points={"env_effect": ["minor", "significant"]}))
    assert d.route == "judgment" and d.route_triggers == ["U1-OPEN"]


def test_route_estimated_1_6_m3_lube_oil_is_judgment_u2_but_metered_is_not():
    est = decide(Facts(release=True, substance="Lube Oil", volume_m3=1.6, volume_estimated=True))
    assert est.route == "judgment" and est.route_triggers == ["U2-NEAR"]
    metered = decide(Facts(release=True, substance="Lube Oil", volume_m3=1.6))
    assert (metered.route, metered.incident_types, metered.deadline) == ("clear-cut", ["INC-d"], "T24")


def test_route_contradictory_location_is_judgment_u3():
    f = Facts(release=True, substance="Crude Oil - Sweet", volume_m3=4.0,
              conflicts={"lands": [{COMPANY_PROPERTY}, {OFF_RIGHT_OF_WAY}]})  # fmt: skip
    d = decide(f)
    assert d.route == "judgment" and d.route_triggers == ["U3-CONFLICT"]
    assert d.deadline == "T3"  # the conservative default until a person or the agent decides


def test_carbon_dioxide_is_a_judgment_substance():
    d = decide(Facts(release=True, substance="Carbon Dioxide", volume_m3=50.0, through_pipe_body_or_weld=True))
    assert d.route == "judgment"


def test_nothing_mentioned_is_not_reportable():
    d = decide(Facts())
    assert (d.status, d.route, d.missing) == ("not reportable", "clear-cut", [])


def test_toxic_non_hydrocarbon_release_opens_the_env_question():
    d = decide(Facts(release=True, substance="Sulphur Dioxide", volume_m3=50.0))
    assert d.route == "judgment" and d.route_triggers == ["U1-OPEN"]
    water = decide(Facts(release=True, substance="Water", volume_m3=50.0))
    assert (water.status, water.route) == ("not reportable", "clear-cut")


def test_carbon_dioxide_with_unknown_rate_is_judgment():
    d = decide(Facts(release=True, substance="Carbon Dioxide", volume_m3=50.0))
    assert d.route == "judgment" and d.deadline in ("T3", "T24")
