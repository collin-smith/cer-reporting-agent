"""The CER reporting rules as code (input/cer/rules-spec.md). Every result cites the spec's rule IDs.

Facts come in three states, and the difference matters:
- absent: the report doesn't mention it (booleans default to False);
- missing: the report mentions it but the value isn't known (None). PREC decides: the worst plausible answer, as a
  precautionary notice, with the fact listed as missing. Missing facts never make a case a judgment case (D23).
- open: the report gives it, but the rule has no numeric test, a value is an estimate near a threshold, or the
  report contradicts itself. ROUTE decides: if the open point could change the answer, the case is a judgment case.

`decide(facts)` evaluates the rules once per combination of plausible values and compares the outcomes.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import itertools
from dataclasses import dataclass, field

# --- SUB-CLASS: which release rule a substance falls under ---

GAS, SOUR, HVP, LVP, NON_HC, JUDGE = "GAS", "SOUR", "HVP", "LVP", "NON-HC", "JUDGE"

SUBSTANCE_CLASS = {
    "natural gas - sweet": GAS, "fuel gas": GAS,
    "natural gas - sour": SOUR, "hydrogen sulphide": SOUR,
    "propane": HVP, "butane": HVP, "natural gas liquids": HVP, "mixed hvp hydrocarbons": HVP,
    "crude oil - sweet": LVP, "crude oil - sour": LVP, "crude oil - synthetic": LVP, "condensate": LVP,
    "gasoline": LVP, "diesel fuel": LVP, "jet fuel": LVP, "lube oil": LVP, "waste oil": LVP, "hydraulic fluid": LVP,
    "water": NON_HC, "contaminated water": NON_HC, "produced water": NON_HC, "drilling fluid": NON_HC,
    "sulphur": NON_HC, "sulphur dioxide": NON_HC, "amine": NON_HC, "glycol": NON_HC, "methanol": NON_HC,
    "pulp slurry": NON_HC, "potassium carbonate": NON_HC, "potassium hydroxide (caustic solution)": NON_HC,
    "odourant": NON_HC,
    "carbon dioxide": JUDGE, "condensate - unstabilized": JUDGE,
}  # fmt: skip

# VOL-UNIT: liquid-to-gas expansion at standard conditions. Propane ~270 is the published ratio; the other HVP
# products use the same factor as a conservative stand-in (a higher factor reaches the 30,000 m³ line sooner).
EXPANSION = {"propane": 270.0, "butane": 270.0, "natural gas liquids": 270.0, "mixed hvp hydrocarbons": 270.0}

LVP_LINE_M3 = 1.5  # INC-d: "in excess of 1.5 m³"
GAS_RATE_LINE_KG_S = 0.1  # INC-e clause 1
GAS_T3_LINE_M3 = 30_000.0  # T3-GAS30K
NEAR_BAND = 0.25  # U2-NEAR: an estimate within ±25% of a line (D23)
SIPR_FACTOR = 1.10
MOP_MARGIN, MOP_FLOOR_KPA = 0.10, 35.0

COMPANY_PROPERTY, RIGHT_OF_WAY, OFF_RIGHT_OF_WAY = "company_property", "right_of_way", "off_right_of_way"

# INC-b lists "release of a toxic substance" as an example that needs notification. A release of one of these, with
# no assessment of the effect, raises the significance question (U1-OPEN) rather than being ruled out.
TOXIC_NON_HC = {"sulphur dioxide", "amine", "odourant", "methanol", "glycol", "potassium hydroxide (caustic solution)"}


def substance_class(substance: str | None) -> str | None:
    if substance is None:
        return None
    return SUBSTANCE_CLASS.get(substance.strip().casefold(), JUDGE)


@dataclass
class Facts:
    """What intake extracted from a field report. Booleans: False = not mentioned, None = mentioned but unknown."""

    discovered_at: dt.datetime | None = None
    # INC-a
    death: bool | None = False
    serious_injury: bool | None = False
    # INC-b
    env_effect: str | None = "none"  # "none" | "minor" | "significant"; None = unknown
    historical_contamination: bool = False
    # INC-c
    fire_or_explosion: bool | None = False
    fire_linked_to_pipeline: bool | None = True  # "caused by or impacts" the pipeline
    # Releases (INC-d, INC-e)
    release: bool | None = False
    substance: str | None = None
    volume_m3: float | None = None
    volume_state: str | None = None  # "liquid" | "gas"; needed for HVP (VOL-UNIT)
    volume_estimated: bool = False
    rate_kg_s: float | None = None
    rate_estimated: bool = False
    through_pipe_body_or_weld: bool | None = False
    planned_venting: bool = False
    gas_release_qualifies: bool | None = None  # set when the record already establishes it (back-test)
    lands: set[str] | None = field(default_factory=lambda: {COMPANY_PROPERTY})  # None = not stated
    # T3 triggers that aren't incident types
    rupture: bool | None = False
    toxic_plume: bool | None = False
    # INC-f
    pressure_kpa: float | None = None
    limit_kpa: float | None = None
    limit_type: str = "mop"  # "mop" (design/approved/qualified/amended) | "rop" | "sipr"
    sipr_for_safety: bool | None = True
    temperature_c: float | None = None
    design_temperature_c: float | None = None
    other_beyond_design: str | None = None  # "exposure" | "slope_movement" | "inappropriate_product"
    # Open points the intake flagged: field name -> the plausible values (U1-OPEN, U3-CONFLICT)
    open_points: dict[str, list] = field(default_factory=dict)
    conflicts: dict[str, list] = field(default_factory=dict)


@dataclass(frozen=True)
class Outcome:
    reportable: bool
    incident_types: tuple[str, ...]
    deadline: str | None  # "T3" | "T24" | None
    triggers: tuple[str, ...]  # the T3-* rules met
    excluded: tuple[str, ...]  # OUT-* rules applied


@dataclass
class Decision:
    status: str  # "reportable" | "not reportable" | "precautionary"
    incident_types: list[str]
    deadline: str | None
    deadline_rules: list[str]
    due_at: dt.datetime | None
    missing: list[str]
    route: str  # "clear-cut" | "judgment"
    route_triggers: list[str]
    citations: list[str]
    outcomes_considered: int


# --- One evaluation, with every fact known ---


def _inc_f(f: Facts) -> bool:
    if f.other_beyond_design:
        return True
    if f.temperature_c is not None and f.design_temperature_c is not None and f.temperature_c > f.design_temperature_c:
        return True
    if f.pressure_kpa is None or f.limit_kpa is None:
        return False
    if f.limit_type == "rop":
        return f.pressure_kpa > f.limit_kpa
    if f.limit_type == "sipr":
        return bool(f.sipr_for_safety) and f.pressure_kpa > SIPR_FACTOR * f.limit_kpa
    return f.pressure_kpa > f.limit_kpa + max(MOP_MARGIN * f.limit_kpa, MOP_FLOOR_KPA)


def _gas_volume_m3(f: Facts) -> float:
    if f.volume_m3 is None:
        return 0.0
    if f.volume_state == "liquid":
        return f.volume_m3 * EXPANSION.get((f.substance or "").casefold(), 270.0)
    return f.volume_m3


def evaluate(f: Facts) -> Outcome:
    """Apply the rules to fully known facts. Callers resolve None values first (see decide)."""
    types, triggers, excluded = [], [], []
    if f.death or f.serious_injury:
        types.append("INC-a")
        triggers += ["T3-DEATH"] if f.death else []
        triggers += ["T3-INJURY"] if f.serious_injury else []
    if f.historical_contamination:
        excluded.append("OUT-NOC")
    elif f.env_effect == "significant":
        types.append("INC-b")
    elif f.env_effect == "minor":
        excluded.append("OUT-MINOR-ENV")
    if f.fire_or_explosion and f.fire_linked_to_pipeline:
        types.append("INC-c")
    if f.release:
        cls = substance_class(f.substance)
        if cls == LVP:
            if (f.volume_m3 or 0) > LVP_LINE_M3:
                types.append("INC-d")
                if f.lands and f.lands - {COMPANY_PROPERTY}:
                    triggers.append("T3-LVP")
            else:
                excluded.append("OUT-LVP15")
        elif cls in (GAS, SOUR, HVP):
            qualifies = f.gas_release_qualifies
            if qualifies is None:
                qualifies = bool(f.through_pipe_body_or_weld) or (f.rate_kg_s or 0) > GAS_RATE_LINE_KG_S
            if f.planned_venting:
                excluded.append("OUT-VENT")
            elif qualifies:
                types.append("INC-e")
                if cls == SOUR:
                    triggers.append("T3-SOUR")
                if _gas_volume_m3(f) > GAS_T3_LINE_M3:
                    triggers.append("T3-GAS30K")
            else:
                excluded.append("OUT-GASRATE")
    if _inc_f(f):
        types.append("INC-f")
    elif f.pressure_kpa is not None and f.limit_kpa is not None:
        excluded.append("OUT-PRESSURE")
    reportable = bool(types)
    if reportable:
        triggers += ["T3-RUPTURE"] if f.rupture else []
        triggers += ["T3-PLUME"] if f.toxic_plume else []
    deadline = ("T3" if triggers else "T24") if reportable else None
    return Outcome(reportable, tuple(types), deadline, tuple(triggers) if reportable else (), tuple(excluded))


# --- Expanding unknown and open points into plausible values ---


def _near(value: float | None, line: float) -> bool:
    return value is not None and abs(value - line) <= NEAR_BAND * line


def _missing_points(f: Facts) -> dict[str, list]:
    """Mentioned-but-unknown facts that a rule needs (PREC). Each maps to the values it could take."""
    pts: dict[str, list] = {}
    if f.death is None:
        pts["death"] = [False, True]
    if f.serious_injury is None:
        pts["serious_injury"] = [False, True]
    if f.env_effect is None:
        pts["env_effect"] = ["none", "significant"]
    if f.fire_or_explosion is None:
        pts["fire_or_explosion"] = [False, True]
    if f.rupture is None:
        pts["rupture"] = [False, True]
    if f.toxic_plume is None:
        pts["toxic_plume"] = [False, True]
    if f.release is None:
        pts["release"] = [False, True]
    if f.release is not False:
        cls = substance_class(f.substance)
        if f.substance is None:
            pts["substance"] = ["crude oil - sweet", "natural gas - sour"]
        if f.volume_m3 is None and cls != NON_HC:
            pts["volume_m3"] = [0.0, 1e9]
        if cls == HVP and f.volume_m3 is not None and f.volume_state is None:
            pts["volume_state"] = ["gas", "liquid"]
        if cls in (GAS, SOUR, HVP, JUDGE, None) and f.gas_release_qualifies is None:
            if f.through_pipe_body_or_weld is None:
                pts["through_pipe_body_or_weld"] = [False, True]
            elif not f.through_pipe_body_or_weld and f.rate_kg_s is None:
                pts["rate_kg_s"] = [0.0, 1.0]
        if f.lands is None:
            pts["lands"] = [{COMPANY_PROPERTY}, {OFF_RIGHT_OF_WAY}]
    if f.limit_type == "sipr" and f.sipr_for_safety is None:
        pts["sipr_for_safety"] = [False, True]
    return pts


def _open_points(f: Facts) -> dict[str, tuple[str, list]]:
    """Points that make a case a judgment case if they change the answer: name -> (trigger, values)."""
    pts: dict[str, tuple[str, list]] = {k: ("U1-OPEN", v) for k, v in f.open_points.items()}
    pts.update({k: ("U3-CONFLICT", v) for k, v in f.conflicts.items()})
    if substance_class(f.substance) == JUDGE and f.release is not False and "substance" not in pts:
        pts["substance"] = ("U1-OPEN", ["natural gas - sweet", "water"])  # treated as gas, or as neither
    toxic = (f.substance or "").casefold() in TOXIC_NON_HC
    if f.release and toxic and f.env_effect == "none" and "env_effect" not in pts:
        pts["env_effect"] = ("U1-OPEN", ["none", "significant"])
    if f.volume_estimated and f.volume_m3 is not None and "volume_m3" not in pts:
        cls = substance_class(f.substance)
        if cls == LVP and _near(f.volume_m3, LVP_LINE_M3):
            pts["volume_m3"] = ("U2-NEAR", [LVP_LINE_M3 * (1 - NEAR_BAND), LVP_LINE_M3 * (1 + NEAR_BAND)])
        elif cls in (GAS, SOUR, HVP) and _near(_gas_volume_m3(f), GAS_T3_LINE_M3):
            scale = f.volume_m3 / _gas_volume_m3(f)
            pts["volume_m3"] = ("U2-NEAR", [GAS_T3_LINE_M3 * s * scale for s in (1 - NEAR_BAND, 1 + NEAR_BAND)])
    if f.rate_estimated and _near(f.rate_kg_s, GAS_RATE_LINE_KG_S) and "rate_kg_s" not in pts:
        pts["rate_kg_s"] = ("U2-NEAR", [GAS_RATE_LINE_KG_S * (1 - NEAR_BAND), GAS_RATE_LINE_KG_S * (1 + NEAR_BAND)])
    return pts


def _variants(base: Facts, points: dict[str, list]):
    names = list(points)
    for values in itertools.product(*(points[n] for n in names)):
        yield dict(zip(names, values, strict=True))


def _key(o: Outcome) -> tuple:
    return (o.reportable, o.deadline)


def _worst(outcomes: list[Outcome]) -> Outcome:
    """The answer that can't be wrong in the costly direction: reportable if any is, the earliest deadline."""
    rank = {None: 0, "T24": 1, "T3": 2}
    return max(outcomes, key=lambda o: (o.reportable, rank[o.deadline], len(o.incident_types)))


def decide(f: Facts) -> Decision:
    missing = _missing_points(f)
    open_ = _open_points(f)
    outcomes_by_open: dict[str, list[Outcome]] = {}  # keyed by the open values (sets aren't hashable)
    for open_values in _variants(f, {k: v for k, (_, v) in open_.items()}):
        for miss_values in _variants(f, missing):
            o = evaluate(dataclasses.replace(f, **open_values, **miss_values))
            outcomes_by_open.setdefault(repr(sorted(open_values.items(), key=str)), []).append(o)
    # Per open-point combination, PREC resolves the missing facts to the worst case.
    resolved = [_worst(os) for os in outcomes_by_open.values()]
    judgment = len({_key(o) for o in resolved}) > 1
    route_triggers = sorted({trig for name, (trig, _) in open_.items() if judgment})
    every = [o for os in outcomes_by_open.values() for o in os]
    final = _worst(resolved)
    precautionary = final.reportable and (judgment or len({_key(o) for o in every}) > 1)
    status = "precautionary" if precautionary else ("reportable" if final.reportable else "not reportable")
    deadline_rules = list(final.triggers) or (["T24"] if final.deadline == "T24" else [])
    if precautionary:
        deadline_rules.append("PREC")
    due = None
    if f.discovered_at and final.deadline:
        due = f.discovered_at + dt.timedelta(hours=3 if final.deadline == "T3" else 24)
    citations = sorted(set(final.incident_types) | set(deadline_rules) | set(final.excluded))
    if final.reportable:
        citations.append("DIR-84")
    return Decision(
        status=status,
        incident_types=list(final.incident_types),
        deadline=final.deadline,
        deadline_rules=deadline_rules,
        due_at=due,
        missing=sorted(missing),
        route="judgment" if judgment else "clear-cut",
        route_triggers=route_triggers,
        citations=citations,
        outcomes_considered=len(every),
    )
