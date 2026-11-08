# CER incident reporting — rules spec (draft v0.1, 2026-10-29)

> **Read this first.** This is an independent interpretation of the Canada Energy Regulator's *Event Reporting
> Guidelines*, written for a portfolio project. It is not affiliated with or endorsed by the CER, it hasn't been
> reviewed by anyone who has filed a CER report, and it must not be used to decide real reporting obligations. For
> the official rules, see the [Guidelines](https://www.cer-rec.gc.ca/en/about/acts-regulations/cer-act-regulations-guidance-notes-related-documents/canada-energy-regulator-event-reporting-guidelines/2024-revised-event-reporting-guidelines.pdf).
>
> Quoted text is reproduced, for non-commercial purposes, from *Event Reporting Guidelines* (revised December
> 2024) by the Canada Energy Regulator. It is a copy of the version available at
> https://www.cer-rec.gc.ca/en/about/acts-regulations/cer-act-regulations-guidance-notes-related-documents/canada-energy-regulator-event-reporting-guidelines/2024-revised-event-reporting-guidelines.pdf, and this reproduction has not been produced in affiliation with, or with the endorsement of, the CER.
> Quoted text remains the Crown's and isn't covered by this repository's licence, which applies only to the
> interpretation and the code.

**Source:** CER *Event Reporting Guidelines*, revised December 2024, in force 2025-03-12
([PDF](https://www.cer-rec.gc.ca/en/about/acts-regulations/cer-act-regulations-guidance-notes-related-documents/canada-energy-regulator-event-reporting-guidelines/2024-revised-event-reporting-guidelines.pdf); downloaded 2026-10-29, SHA-256 `81785d1ac820232a8ab69f5493e6b2610c967900c12892739a0b96042e2b6181`). Section numbers are the
Guidelines' own. Page numbers are the printed page numbers. Deadlines in §5.2.3–5.2.6 come from flowchart images, not
text; they're transcribed here and marked *(flowchart)*.

**Status:** draft, written by Collin and Claude. **Not reviewed by anyone who has filed a CER report.** Open questions
are in §6 and are flagged inline as **[Q-n]**.

**How it's used:** rules code, test-set labels and the policy specialist's citations refer to a rule ID (e.g. `T3-LVP`),
never to a paraphrase. A rule's quote is word for word. Anything that isn't a quote is labelled *Interpretation*.

**Scope:** onshore pipelines under the OPR (Guidelines §4, §5, §13.1). Out of scope: Processing Plant Regulations (§6),
damage prevention (§7), offshore and Norman Wells (§8–§11), power lines (§12). See [Q-1] for processing plants.

All worked examples use fictional operators.

---

## 1. Is it an incident? (OPR definition, §5.1)

> **incident** means an occurrence that results in
> (a) the death of or serious injury to a person;
> (b) a significant adverse effect on the environment;
> (c) an unintended fire or explosion;
> (d) an unintended or uncontained release of LVP hydrocarbons in excess of 1.5 m³;
> (e) an unintended or uncontrolled release of gas or HVP hydrocarbons;
> (f) the operation of a pipeline beyond its design limits as determined under CSA Z662 or CSA Z276 or any operating
> limits imposed by the Regulator.

An occurrence is reportable if any of `INC-a` to `INC-f` is met. More than one can apply, and each one found is listed.

### INC-a — Death or serious injury (§5.1, §5.2.1, p. 4–5)

> **serious injury** includes an injury that results in (a) the fracture of a major bone; (b) the amputation of a body
> part; (c) the loss of sight in one or both eyes; (d) internal hemorrhage; (e) third degree burns; (f)
> unconsciousness; or (g) the loss of a body part or function of a body part.

> The CER considers each of the following to be a "major bone": skull, mandible, spine, scapula, sternum, rib, pelvis,
> femur, humerus, fibula, tibia, radius, and ulna.

> The OPR does not differentiate between different types of persons. Therefore, companies must report a death or
> serious injury to any person relating to the construction, operation, or abandonment of its pipeline regardless of
> whether the death or serious injury was to a pipeline company employee, a contractor working for the pipeline
> company, or a member of the public.

Precautionary triggers (§5.2.1): notification is required for death or serious injury that is

> suspected of being related to, or caused by, pipeline construction, operation, or abandonment activities
> (regardless of time or location of discovery); […] occurred or was discovered on a work site, company owned or
> leased lands, pipeline right-of-way, or work camp; […] involving a vehicle or mobile equipment being operated in
> relation to pipeline construction, operation, or abandonment activities; and […] where a company's determination has
> been contradicted by a third-party authority (e.g., physician, coroner, provincial occupational health and safety, or
> worker's compensation board or similar).

*Interpretation:* "includes" means the list isn't closed. A fracture of a bone not on the list (e.g., a finger or a
clavicle) is not a serious injury by itself under (a). Treat it as a judgment case unless another item applies.

**Example.** A contractor for *Prairie Midstream Ltd.* falls from a pipe rack at a valve site and breaks a wrist (the
radius). → `INC-a` (radius is a major bone). Deadline `T3-HARM`.
**Counter-example.** The same fall, but the worker sprains an ankle and returns to work next day. → Not `INC-a`.

### INC-b — Significant adverse effect on the environment (§5.2.2, p. 6)

> "significant adverse effect on the environment" is an unauthorized impairment of or damage to the environment
> resulting in harm to human life, wildlife, or vegetation. Significance considers moderate to major effect,
> magnitude, intensity and consequence. Events resulting in a minor adverse effect on the environment do not require
> notification.

Examples listed as requiring notification (§5.2.2):

> release of a toxic substance; release of drilling fluid or sediment into a sensitive location or ecosystem (e.g.,
> watercourse, wetland, or critical habitat); unintended physical alteration of a fish-bearing watercourse […];
> destruction of critical habitat […]; any unauthorized mortality of an individual special status wildlife or fish
> species […]; and any unauthorized mortality of a non-special status wildlife or fish species that might cause a
> negative effect to that species' local or regional population.

> A significant adverse effect on the environment that is caused by residual contamination from a historical event or
> accumulation of contaminants over time should be reported through OERS as a Notice of Contamination.

*Interpretation:* this is the main judgment rule; "moderate to major" has no numeric threshold. Historical
contamination is routed to `OUT-NOC` (a different filing), not to an incident.

**Example.** During a horizontal directional drill crossing, *Aspen Ridge Pipelines Inc.* loses drilling mud into a
fish-bearing creek. → `INC-b`. Deadline `T24`.
**Counter-example.** A 20 L hydraulic oil drip onto gravel inside a fenced compressor station, cleaned up the same
shift. → Minor effect; not `INC-b`. (Not `INC-d` either: under 1.5 m³.)

### INC-c — Unintended fire or explosion (§5.2.3, p. 7)

> "an unintended fire or explosion" means any unintended fire or explosion that is caused by or impacts the
> construction, operation or abandonment of a pipeline.

> Events that require notification to the CER include but are not limited to: flash fires; battery explosion; arc
> flash/blast that has rendered the equipment inoperable or unsafe to operate and/or on equipment rated with nominal
> voltages of 240 V AC and above, or 100 V DC and above; fire caused by an arc, or a cable fault or a breakdown of any
> component of the uninterruptible power system or the back-up generator; wildland or forest fires that damage
> pipeline infrastructure or impact the construction, operation or abandonment of a pipeline (e.g., pipeline
> shut-in); and welding or housekeeping related fires

**Example.** A UPS battery bank at a *Northline Gas Transmission* meter station catches fire; no injuries. → `INC-c`.
Deadline `T24` (no rupture or toxic plume).
**Counter-example.** A wildfire burns 2 km from the right of way; no damage, no shut-in. → Not `INC-c`.

### INC-d — LVP hydrocarbon release over 1.5 m³ (§5.1, §5.2.4, p. 8)

> (d) an unintended or uncontained release of LVP hydrocarbons in excess of 1.5 m³

> **release** Includes discharge, spray, spill, leak, seep, pour, emit, dump and exhaust.

*Interpretation:* "in excess of" means strictly greater than 1.5 m³; exactly 1.5 m³ is not `INC-d`. Which substances
count as LVP is set by `SUB-CLASS` below.

**Example.** 2.0 m³ of sweet crude seeps from a pinhole at a *Prairie Midstream Ltd.* pump station into a lined
containment area. → `INC-d`. Deadline `T24` (stayed on company property, no rupture or plume).
**Counter-example.** 1.2 m³ of crude, same place. → Not `INC-d` (and not `INC-b` if the effect is minor).

### INC-e — Unintended or uncontrolled release of gas or HVP hydrocarbons (§5.2.5, p. 9–10)

> An event that is not part of planned pipeline maintenance or normal operation and occurs during the construction,
> operation or abandonment of a pipeline and results in:
> 1. a release of gas or HVP hydrocarbons occurring at a rate greater than 0.1 kg/second due to any malfunctioning or
>    faulty part of a pipeline, facility or appurtenance including but not limited to seals, packing, gaskets,
>    o-rings, plugs, valves, including where such release occurs elsewhere than at the malfunctioning or faulty part;
> 2. a release of any size that occurs through the body of the pipeline or a welded connection.

> Events that do not fall under this definition include but are not limited to: intended and controlled flaring or
> venting of natural gas or hydrocarbons, including venting through properly functioning pressure relief valves or
> pressure safety valves that is part of planned pipeline maintenance or normal operation.

Release-rate estimate the Guidelines offer (§5.2.5, p. 10), with a 0.85 discharge coefficient built in:

> ṁ = (D² P / 160) · √(M / T)  — ṁ gas discharge rate (kg/s); D release hole diameter (m); P pressure inside the
> pipeline (Pa gauge); M molecular weight of the gas (g/mol); T gas temperature inside the pipeline (K)

Duration, in order: actual duration if start and end are known; else from the last inspection/surveillance/site
visit to discovery; else "a minimum 30 days or the date the facility/pipeline was commissioned whichever is less".

*Interpretation:* the PDF text layer garbles this equation; the form above is checked against the rendered
page (p. 10). The rules engine uses it only to test the 0.1 kg/s line when
a report gives hole size, pressure and temperature.

**Example.** A weld crack on a *Northline Gas Transmission* lateral leaks sweet gas at a rate too small to measure. →
`INC-e` via clause 2 (any size, through a welded connection). Deadline `T24` unless volume > 30,000 m³.
**Counter-example.** A valve packing weeps sweet gas at an estimated 0.02 kg/s. → Not `INC-e` (under 0.1 kg/s, not
through pipe body or weld). Not reportable unless another rule applies.
**Counter-example.** Planned blowdown through a working PSV during maintenance. → Excluded.

### INC-f — Operation beyond design limits (§5.2.6, p. 11–12)

> The operation, for any amount of time, of a pipeline beyond the criteria for which the pipeline was designed and/or
> the operation of the pipeline beyond criteria imposed by the CER to mitigate a condition on the pipeline. This
> includes any condition that triggered an engineering assessment to be conducted to determine continued fitness for
> service of the pipeline.

> Events that require notification to the CER include but are not limited to:
> - operation of a pipeline at a pressure above the design pressure or Approved MOP, Qualified MOP, or Amended MOP by
>   more than 10% or 35 kPa, whichever is greater;
> - operation of a pipeline at a pressure greater than 100% of any ROP;
> - operation of a pipeline at a pressure greater than 110% of any company's SIPR implemented for safety and/or
>   integrity reasons;
> - operation of a pipeline at a temperature greater than the design temperature;
> - slope movements that exceed what was predicted at the design stage or were not predicted in the design stage;
> - unintended exposures of pipelines including in waterbodies (e.g., rivers, wetlands) and on land; and
> - the introduction of an inappropriate product into the pipeline (e.g., sour product in a line or facility designed
>   for sweet product; any exceedance of product's chemical properties as defined in the tariff limits).

> When the type of MOP is not indicated, the default is the qualified MOP as per the CSA Z662 MOP definition.

| Limit in the report | Reportable when pressure is above |
|---|---|
| Design pressure / Approved / Qualified / Amended MOP (default: Qualified) | MOP + max(10% × MOP, 35 kPa) |
| ROP (imposed by Commission or inspection officer) | 100% of ROP |
| SIPR (company, for safety/integrity) | 110% of SIPR |
| Design temperature | 100% of design temperature |

*Interpretation:* the 35 kPa floor governs for MOPs under 350 kPa. A SIPR set for commercial, not safety or
integrity, reasons isn't covered by the third bullet **[Q-3]**.

**Example.** MOP 6,000 kPa; a control fault takes an *Aspen Ridge Pipelines Inc.* segment to 6,700 kPa for 4 minutes.
Threshold 6,600 kPa. → `INC-f`. Deadline `T24`.
**Counter-example.** Same segment peaks at 6,550 kPa. → Not `INC-f` (≤ 6,600 kPa).
**Example.** ROP 4,800 kPa; pressure reaches 4,810 kPa. → `INC-f` (any amount over a ROP).
**Example.** A spring flood scours cover and exposes 15 m of pipe in a riverbed. → `INC-f` (unintended exposure).

### SUB-CLASS — Which release rule a substance falls under (§5.1, §6.2.2 footnote 13, p. 14)

The OPR defines LVP and HVP only "as defined in CSA Z662", which the Guidelines don't quote. The one definition they
do quote is in the processing-plant section:

> For the purposes of reporting under the PPR companies should use the following definition of HVP hydrocarbons:
> hydrocarbons or hydrocarbon mixtures in the liquid or quasi-liquid state with a vapour pressure greater than 110 kPa
> absolute at 38 °C.

*Interpretation:* we use the same 110 kPa / 38 °C line for pipelines, assuming CSA Z662 draws it in the same place.
Classes are set per substance, by its name in the field report or in the CER `Substance` column. The CER
`Release Type` column is **not** used: the CER methodology defines it as "the primary product being transported in
the pipeline", not the substance released. (It's also inconsistent: the methodology lists natural gas liquids under
Liquid, but the data files all NGL releases under Gas.)

| Class | Release rule | Substances (CER `Substance` values) |
|---|---|---|
| `GAS` | `INC-e` | Natural Gas – Sweet; Fuel Gas |
| `SOUR` | `INC-e` + `T3-SOUR` (3 h, any size) | Natural Gas – Sour; Hydrogen Sulphide |
| `HVP` | `INC-e` | Propane; Butane; Natural Gas Liquids; Mixed HVP Hydrocarbons |
| `LVP` | `INC-d` (only > 1.5 m³) | Crude Oil – Sweet, Sour, Synthetic; Condensate; Gasoline; Diesel Fuel; Jet Fuel; Lube Oil; Waste Oil; Hydraulic Fluid |
| `NON-HC` | Neither `INC-d` nor `INC-e`; reportable only through `INC-b` | Water; Contaminated Water; Produced Water; Drilling Fluid; Sulphur; Sulphur Dioxide; Amine; Glycol; Methanol; Pulp slurry; Potassium Carbonate; Potassium Hydroxide; Odourant |
| `JUDGE` | Judgment case; the output says why | Carbon Dioxide; any substance not listed here |

Decisions inside the table (agreed 2026-10-29):

- **Condensate → `LVP`.** Stabilized condensate is LVP. A report that says *unstabilized* condensate is a `JUDGE` case,
  because unstabilized condensate can be above 110 kPa.
- **Gasoline → `LVP`.** Its vapour pressure is normally below 110 kPa. Winter blends come close, but they're not
  treated as HVP.
- **Carbon dioxide → `JUDGE`.** OPR (e) says "gas" without saying hydrocarbon, but the §5.2.5 guidance covers only
  natural gas and HVP hydrocarbons.
- **Sour crude → `LVP`, not `SOUR`.** §4.1 names only "sour natural gas or hydrogen sulfide". Sour crude becomes 3 h
  only if the report says H2S was released (then `T3-SOUR` applies as well).

**Example.** 40 m³ of liquid propane escapes from a fitting at a *Northline Gas Transmission* storage site. → `HVP`,
`INC-e`; about 10,800 m³ as gas (see `VOL-UNIT`), so not `T3-GAS30K`. Deadline `T24` unless rupture or plume.
**Counter-example.** 40 m³ of produced water spills onto a lease pad. → `NON-HC`: not `INC-d` or `INC-e`. Reportable
only if the effect on the environment is significant (`INC-b`).

### VOL-UNIT — Volume unit for the 30,000 m³ test (§4.1)

*Interpretation (not quoted):* the 30,000 m³ line in `T3-GAS30K` is read as gas volume at standard conditions (the
§5.2.5 volume formula uses 1 atm and 288 K). HVP releases are usually reported as liquid volumes: in the CER data
propane peaks at 37 m³ and the NGL median is 0.00075 m³.

- The rules engine needs a stated unit (liquid or gas) for every `HVP` volume. It converts liquid to gas with an
  expansion factor per substance (propane about 270; others to be set when the engine is written, from published
  liquid/gas ratios). For propane, the 3 h line is about 111 m³ of liquid.
- If a field report gives an `HVP` volume without saying liquid or gas, the result goes through `PREC`: a
  precautionary 3 h notice, with "volume unit" listed as missing.
- `GAS` and `SOUR` volumes are taken as gas volumes.

---

## 2. When must the first notice go in? (§4, p. 3; flowcharts in §5.2.1–5.2.6)

The clock starts at **discovery**, not occurrence:

> The verbal notification and written input into OERS must be completed as soon as possible and no later than 3 hours
> after the event was discovered.

### T3 — Verbal and written notification within 3 hours (§4.1)

> Phone the TSB Reporting Hotline at 819-997-7887; and then Submit a Preliminary Incident Report via OERS.

Triggered by any of (§4.1, quoted):

| Rule ID | Trigger |
|---|---|
| `T3-DEATH` | "a death" |
| `T3-INJURY` | "a serious injury as defined in the Canadian Energy Regulator Onshore Pipeline Regulations" |
| `T3-LVP` | "an unintended or uncontained release of LVP hydrocarbons in excess of 1.5 m3 that leaves company property or occurs on or off the right of way" |
| `T3-GAS30K` | "an unintended or uncontrolled release of gas or HVP hydrocarbons > 30,000 m³" |
| `T3-SOUR` | "any unintended or uncontrolled release of sour natural gas or hydrogen sulfide" |
| `T3-RUPTURE` | "an instantaneous release that immediately impacts the operation of a pipeline segment such that the pressure of the segment cannot be maintained" |
| `T3-PLUME` | "a band of service fluid or other contaminant (e.g., hydrogen sulfide or smoke) resulting from an incident that causes people, including employees, to take protective measures (e.g., muster, shelter-in-place or evacuation)" |

Flowcharts *(flowchart)*: §5.2.1 death/serious injury → always 3 h. §5.2.3 fire/explosion, §5.2.6 beyond design
limits → 3 h if rupture and/or toxic plume, else 24 h. §5.2.4 LVP → 3 h if rupture/plume, or if the release "leave[s]
company property or occur[s] on or off the right of way", else 24 h. §5.2.5 gas/HVP → 3 h if rupture/plume, or any
sour gas/H2S, or sweet gas/HVP > 30,000 m³, else 24 h.

*Interpretation of `T3-LVP`:* footnote 7 (p. 5) defines company owned or leased lands as lands "excluding the Right of
Way, on which above-ground energy infrastructure or Facilities are located". So the Guidelines treat three kinds of
land as separate, and the PIR asks for them ("affected lands (e.g., affects the pipeline right of way; off company
property)", `PIR-12`). The CER data records them as three yes/no columns: `Affects Company Property`,
`Affects Pipeline right-of-way`, `Affects off Pipeline right-of-way`. Agreed 2026-10-29:

| The release affected… | `INC-d` deadline |
|---|---|
| Company property only (station, terminal, valve site) | `T24` |
| The right of way, with or without company property | `T3-LVP` |
| Anything off the right of way or off company property | `T3-LVP` |
| Not stated in the report | `PREC`: 3 h, with "affected lands" (`PIR-12`) listed as missing |

Check against the CER data (snapshot 2026-10-28): of 92 LVP releases over 1.5 m³, 83 affect company property, 11 the
right of way and 10 land off it, so this reading puts about 80 at 24 h. (The §5.2.4 flowchart's start box reads "An
intended or uncontained release", taken as a typo for "unintended".)

**Example.** 3 m³ of crude surfaces in a farmer's field over the right of way. → `INC-d`, `T3-LVP`.
**Example.** A *Northline Gas Transmission* line ruptures; downstream pressure can't be held. → `INC-e`,
`T3-RUPTURE`, whatever the volume.
**Example.** A small sour-gas fitting leak at 0.2 kg/s sets off an H2S alarm and the crew musters upwind. → `INC-e`,
`T3-SOUR` and `T3-PLUME`.

### T24 — Written notification within 24 hours (§4.2)

> For all other events that require companies to "immediately" notify or report, but which do not meet any of the
> definitions in section 4.1, companies must submit a written notification via OERS as soon as possible and no later
> than 24 hours after the event was discovered.

§5.2.2 (environment) gives 24 h directly *(text box)*.

### TIME-COMBINE — More than one type

*Interpretation (not quoted):* when several `INC-*` apply, the earliest deadline wins. If any `T3-*` trigger is met,
the deadline is 3 h, otherwise 24 h. Every applicable rule ID is still listed in the output.

**Example.** A sweet-gas release of 5,000 m³ catches fire and the crew evacuates the station because of smoke. →
`INC-c`, `INC-e`; `T3-PLUME` → 3 h.

### PREC — When in doubt, notify (§3.2, p. 2)

> The CER expects companies to take a precautionary approach to event reporting. This means that even if there is some
> doubt as to whether an event needs to be reported, the CER expects the company to notify the CER on a precautionary
> basis. In other words, companies should adopt a "when in doubt, notify" approach. There is a selection in OERS that
> allows a company to indicate when it is reporting an event on a precautionary basis.

Footnote 3: the 3 h and 24 h timelines "Includes precautionary notifications."

*Interpretation:* this is the system's tie-break. When a rule depends on a fact the report doesn't give (volume,
rate, injury severity, whether it left the site), the output is **"notify, precautionary"** with the deadline the
worst plausible case would carry, plus a list of the missing facts. It never returns "not reportable" on missing
data. A wrong "not reportable" costs more than a wrong precautionary notice, and the eval scores it that way.

*Operator policy (X1, decision D29):* the status is **precautionary** only when reportability itself is in doubt, i.e.
some plausible reading of a missing or open fact is not reportable. A case that is reportable on every reading is
**reportable**, at the deadline of the stricter reading; `PREC` is still cited for that deadline, the notice says the
deadline was taken at the stricter reading, and the case is still routed to judgment if an open point decides the
deadline. (Example: a 4 m³ crude spill reported both inside the fence and in the road ditch is reportable, `T3-LVP`,
judgment.)

---

## 3. Later reports

### DIR-84 — Detailed Incident Report within 12 weeks (§5.2, p. 5)

> The information required for a DIR must be submitted via OERS within 12 weeks (84 days) of the company's
> notification to the CER. […] For complex incidents, companies may request an extension for submission of a DIR via
> the Send a Message to the CER function within OERS.

*Interpretation:* the 84 days run from the notification date (CER column `Reported Date`), not discovery.

### PIR-SAT — When the first notice counts as the PIR (footnote 5, p. 5)

> Where the CER requires verbal and written notification within 3 hours, completion of both will satisfy all
> requirements for a notification and a PIR. Where CER requires written notification within 24 hours, the submission
> of a PIR via OERS will satisfy all requirements for a notification and a PIR.

### RELIEF — Inspection officer relief (§5.3, p. 12–13)

> If a company has submitted a Preliminary Incident Report (whether precautionary or not) and additional information
> demonstrates the event did not meet an OPR incident reporting requirement, the company can submit a request for
> inspection officer relief and provide justification via the Send a Message to the CER function in OERS.

Out of scope for decisions; mentioned in the drafted notice when the result is precautionary.

---

## 4. What the notice must contain (completeness check)

### PIR-FIELDS (§13.1.1, p. 27)

> Companies must provide the following information via OERS (to the extent known at time of preliminary reporting):

| Field ID | Quoted requirement |
|---|---|
| `PIR-1` | type of incident (e.g. serious injury, operation beyond design limits) |
| `PIR-2` | company contact information |
| `PIR-3` | whether the PIR is precautionary |
| `PIR-4` | date and time of occurrence and/or discovery |
| `PIR-5` | how the incident was discovered (e.g., scheduled patrol, landowner) |
| `PIR-6` | specific details as applicable based on the type of incident (e.g. equipment/components involved; type of serious injury, type of substance and estimate of approximate volume released, pipe exposure details) |
| `PIR-7` | description of any immediate concerns for the safety of persons, the safety of regulated facilities, or the protection of property and the environment |
| `PIR-8` | narrative of the complete description of the circumstances leading up to and resulting from the event and the extent of any damage, including the consequences on the pipeline, property, and the environment |
| `PIR-9` | narrative description of all actions taken or planned to address the consequences of the event including any evacuation |
| `PIR-10` | regulated facility details (pipeline name/facility name) |
| `PIR-11` | event location with GPS coordinates to 8 decimal places |
| `PIR-12` | affected lands (e.g., affects the pipeline right of way; off company property) |
| `PIR-13` | nearest populated center, land use, and population density |

*Interpretation:* "to the extent known" means a missing field doesn't block the notice; it's listed as missing, with
`PIR-4`, `PIR-6` and `PIR-12` marked as the ones that can change the deadline.

### DIR-FIELDS (§13.1.2, p. 28)

Root cause ("at least one immediate cause" and "at least one basic (root) cause"), corrective actions, preventive
actions at similar locations, preventive actions for systemic causes, failed-component details, operating conditions
at discovery, maintenance history, environmental impacts. Not in the agent's scope (the agent drafts the first
notice only); listed so the drafted notice can say what will be needed by day 84.

---

## 5. Not reportable as an OPR incident

| Rule ID | Case | Source |
|---|---|---|
| `OUT-LVP15` | LVP release ≤ 1.5 m³, minor environmental effect, no other type | §5.1 (d), §5.2.2 |
| `OUT-GASRATE` | Gas/HVP release ≤ 0.1 kg/s from a faulty part, not through pipe body or weld | §5.2.5 |
| `OUT-VENT` | Intended, controlled flaring/venting, or venting through a working PRV/PSV during planned maintenance or normal operation | §5.2.5 |
| `OUT-MINOR-ENV` | "Events resulting in a minor adverse effect on the environment do not require notification." | §5.2.2 |
| `OUT-PRESSURE` | Pressure within MOP + max(10%, 35 kPa), ≤ ROP, ≤ 110% SIPR | §5.2.6 |
| `OUT-NOC` | Historical or accumulated contamination → Notice of Contamination, not an incident | §5.2.2 |

Each `OUT-*` result still goes through `PREC`: if a deciding fact is missing, the answer is precautionary, not "out".

---

## 5a. Routing: clear-cut or judgment (`ROUTE`, decision D23)

Not a CER rule: this is the system's own rule for which path a case takes. It runs as plain code after intake has
extracted the facts, and test-set labels use the same rule, so a case's label and its route always agree.

**Principle.** A case is a **judgment** case only if something uncertain could change the answer: whether it's
reportable, or which deadline (3 h or 24 h) applies. The router works out the answer for each plausible value of each
uncertain point. If every version gives the same answer, the case is **clear-cut** and goes to the fixed workflow.

**What counts as uncertain** (any one is enough, if it changes the answer):

| Trigger | Meaning |
|---|---|
| `U1-OPEN` | The deciding rule has no numeric test: `INC-b` significance; an injury not on the serious-injury list; whether a fire was "caused by or impacts" the pipeline (`INC-c`); `SUB-CLASS` = `JUDGE`; slope movement "beyond what was predicted" (`INC-f`) |
| `U2-NEAR` | A value the report gives as an estimate is within ±25% of a threshold: 1.125–1.875 m³ (`INC-d`), 22,500–37,500 m³ gas-equivalent (`T3-GAS30K`), 0.075–0.125 kg/s (`INC-e`). Measured values (e.g. SCADA pressure, metered volume) are taken as exact, with no band |
| `U3-CONFLICT` | The report contradicts itself on a deciding fact (two volumes, two locations, two substances) |

**Missing facts don't make a case a judgment case.** `PREC` already decides them mechanically (precautionary notice,
worst plausible deadline, missing facts listed). The system never guesses a missing value; it asks the field for it.

**Worked examples** (fictional operators):

- **Clear-cut.** *Prairie Midstream Ltd.*: "metered loss of 4.2 m³ sweet crude from tank seal, contained in station
  berm". `LVP`, measured, above 1.5, company property only → `INC-d`, `T24`. Nothing uncertain.
- **Clear-cut, uncertainty doesn't matter.** *Northline Gas Transmission*: rupture on a sweet gas line; "possible
  impact on a nearby creek, being assessed". `INC-b` is uncertain, but `T3-RUPTURE` already sets 3 h, and the case is
  reportable either way → clear-cut.
- **Clear-cut by `PREC`.** *Aspen Ridge Pipelines Inc.*: crude seep on the right of way, "volume not yet known".
  Missing volume → precautionary 3 h notice, follow-up asks for volume.
- **Judgment, `U1-OPEN`.** Drilling mud runs across the right of way to the edge of a wetland at an HDD crossing;
  "crews deployed silt fence, nobody has confirmed any got in". Reportable only through `INC-b`, and whether any
  reached the wetland is open (`P1`). (Mud *seen in* the wetland is not judgment: `INC-b` by the Guidelines' own
  example, `T24`.)
- **Judgment, `U2-NEAR`.** "Estimated 1.6 m³ of lube oil" inside a pump station. At 1.6 it's `INC-d` (`T24`); at
  1.3 it isn't reportable. The estimate is inside the band, so the answer can flip.
- **Not `U2-NEAR`.** "Metered 1.6 m³": measured, so `INC-d`, `T24`, clear-cut.
- **Judgment, `U3-CONFLICT`.** The report says "spill contained inside the station fence" and later "oil observed in
  the road ditch". Company property only → `T24`; off property → `T3-LVP`. The answer depends on which is true.

---

## 5b. Operator policy: readings of the grey areas (approved by the compliance team)

The Guidelines leave a few questions open. These are the operator's readings of them, approved by Collin as the
simulated compliance team's approver (label review, `output/label-review.md`; decision D28). They decide the
test-set labels, they are what the rules engine and intake prompt implement, and they go into the knowledge base next
to the Guidelines so the agents apply the same rules. All are provisional until a CER filer reviews this spec.

| ID | Policy | Rules it reads |
|---|---|---|
| `P1` | Drilling fluid or sediment **seen in** a watercourse or wetland is a significant effect: reportable, `T24`. If the report doesn't confirm any got in (it reached the right of way or a wetland's edge, "not sure if any got in"), it's an open point: precautionary, `T24`, judgment; ask the field "Did any reach the water or wetland?" The test is whether anyone saw it in the water, not distance. | `INC-b`, `U1-OPEN` |
| `P2` | A release of a **toxic substance** (amine, methanol, odourant, sulphur dioxide, caustic, glycol) whose effect hasn't been assessed is an open point: precautionary, `T24`, judgment; ask "Has the effect on soil, water or wildlife been assessed?" Glycol stays: reports rarely say which glycol, and ethylene glycol is toxic. | `INC-b`, `U1-OPEN` (`TOXIC_NON_HC`) |
| `P3` | A fracture of a bone **on the major-bone list** is a serious injury: reportable, `T3`. A fracture of a **finger or toe** only, with nothing else on the serious-injury list, is not reportable. A fracture of **any other unlisted bone** (collarbone, kneecap, hand, wrist, foot, ankle) is an open point: precautionary, `T3`, judgment, until a CER filer advises (Q-7). | `INC-a`, `T3-INJURY`, `U1-OPEN` |
| `P4` | A **fire near the facility** whose origin, or effect on the pipeline, is unknown: precautionary, `T24`, judgment; ask "Did the fire start at, or affect, our pipeline or work?" | `INC-c`, `U1-OPEN` |
| `P5` | **Carbon dioxide** is treated as a gas for the release rules: through the pipe body or weld, or above 0.1 kg/s, is precautionary, `T24` (`T3` above 30,000 m³), judgment. | `INC-e`, `SUB-CLASS` (`JUDGE`) |
| `P6` | An **estimated** volume or rate within ±25% of a threshold (1.5 m³ liquid, 30,000 m³ gas, 0.1 kg/s) is judgment, at the deadline the higher value would get; precautionary only if the threshold decides reportability (so 1.5 m³ and 0.1 kg/s, but not 30,000 m³ for gas already reportable through the pipe body). **Metered** values are exact. | `U2-NEAR` (D23, D29) |

## 6. Open questions (for the CER-filer review)

- **[Q-1] Processing plants.** The CER incident data mixes pipelines and facilities. Does it include PPR plants, whose
  thresholds differ (e.g., liquid releases > 0.1 m³ for flammable categories 1–3, §6.2.3)? Check the
  `Pipeline or Facility Type` column in the back-test; if plants are present, either add PPR rules or exclude them.
  *Checked 2026-10-29:* 82 records are `Processing` (and 661 are blank), so plants are present. Proposed: exclude
  `Processing` from the back-test and say so; blanks stay in.
- **[Q-2] LVP vs. HVP.** *Closed 2026-10-29 → `SUB-CLASS` and `VOL-UNIT`.* Still worth asking the reviewer: does
  CSA Z662 draw the line at 110 kPa / 38 °C, and are condensate and gasoline right as LVP?
- **[Q-3] SIPR purpose.** Is a commercial SIPR exceedance reportable under the general definition?
- **[Q-4] `T3-LVP` reading.** *Closed 2026-10-29 → table under `T3-LVP`.* Still worth asking the reviewer: is a
  release that stays inside a station fence but reaches the right of way next to it treated as 3 h in practice?
- **[Q-5] Earlier guideline versions.** These rules apply from 2025-03-12. Which versions applied 2008–2025, and did the
  3 h / 24 h split exist? Until that's known, the back-test checks deadlines only for incidents discovered on or
  after 2025-03-12 and checks incident types and Significant for all years (brief §4, improvements item 2).
- **[Q-7] Unlisted fractures (`P3`).** Does the CER expect a 3-hour notice for a fracture of a bone not on the
  major-bone list (collarbone, kneecap, hand, wrist, foot, ankle)? Is a finger or toe fracture alone ever reported?
  Until answered, `P3` treats the former as precautionary 3 h and the latter as not reportable.
- **[Q-8] "Precautionary" when only the deadline is in doubt (X1, D29).** OERS lets a company report "on a
  precautionary basis". Is that selection meant only for doubt over *whether* an event is reportable, as `PREC` now
  reads it, or also for an event that is certainly reportable but whose 3 h / 24 h deadline was taken at the stricter
  reading (a location conflict, an unconfirmed H2S alarm)?
- **[Q-6] "Significant" flag.** *Closed 2026-10-29 → `SIG` in §7.* Full definition found in the CER glossary;
  the data follows it consistently (see §7).

## 7. Back-test notes (for the rules engine, not rules)

### SIG — the CER `Significant` column (for the back-test only)

Source: CER Interactive Pipeline Map glossary,
https://www.cer-rec.gc.ca/en/safety-environment/industry-performance/interactive-pipeline/glossary-terms.html (date
modified 2022-08-05; read 2026-10-29). Not part of the Guidelines and not a reporting rule.

> A significant incident is an acute event that results in: death; a serious injury (as defined in the OPR); a fire
> or explosion that causes a pipeline or facility to be inoperative; a LVP hydrocarbon release in excess of 1.5 m³
> that leaves company property or the right-of-way; a rupture; or a toxic plume (as defined in CSA Z662).

How the flag is applied in the data (snapshot 2026-10-28; `code/scripts/companion_analysis.py`, findings §3a):

| Rule ID | Condition | Significant in the data |
|---|---|---|
| `SIG-HARM` | Death or serious injury | 137 of 137 |
| `SIG-SOUR` | Any sour gas or H2S release | 57 of 57 (not in the glossary wording; matches `T3-SOUR`) |
| `SIG-GAS30K` | Sweet gas release > 30,000 m³ | 51 of 52 (not in the glossary wording; matches `T3-GAS30K`) |
| `SIG-LVP` | `LVP` > 1.5 m³ off company property | 16 of 16 |
| `SIG-RUPTURE` | Rupture of a hydrocarbon line | 15 of 17; ruptures of water/slurry lines (`NON-HC`) are never Significant (0 of 12) |
| `SIG-ENV` | Adverse environmental effects, year ≤ 2024 | 84 of 84; from 2025 only 1 of 10, so the back-test applies it only before 2025 |

Not testable from the data: "fire or explosion that causes a pipeline or facility to be inoperative" and "toxic
plume" have no column. The back-test reports agreement on the testable rules and lists the rest as unscored.
`SIG-*` is close to the `T3-*` set, which gives the deadline back-test a second check for years before 2025 (Q-5).

- The CER file has `Reported Date` as a date only, so a 3 h deadline can't be checked to the hour. The back-test can
  check "same or next calendar day as discovery" as a proxy and must say so.
- `Discovered Date and Time` carries a time-zone word (e.g. "Mountain"); parse it, don't drop it.
- CER `Incident Types` maps to `INC-*` like this: Fatality / Serious Injury → `INC-a`; Adverse Environmental Effects →
  `INC-b`; Fire, Explosion → `INC-c`; Release of Substance → `INC-d` (`LVP`) or `INC-e` (`GAS`, `SOUR`, `HVP`) by
  `SUB-CLASS` on the `Substance` column; Operation Beyond Design Limits → `INC-f`.
- The CER records "Release of Substance" for `NON-HC` substances too (about 75 records), so the back-test expects that
  type for them without expecting `INC-d` or `INC-e`.
- Three lube-oil releases of 1.5 m³ or less (0.0001, 0.115 and exactly 1.5 m³) are recorded as incidents. Expect a
  few disagreements like this. They're likely precautionary reports or another rule, so they're logged, not treated as
  rule errors.
- `HVP` volumes in the CER file are treated as liquid volumes and converted under `VOL-UNIT`. The back-test says so.
- `Rupture` column → `T3-RUPTURE`. `Affects Pipeline right-of-way` = Yes or `Affects off Pipeline right-of-way` = Yes or
`Off Company Property` = Yes → `T3-LVP` (for `LVP` over 1.5 m³). `SOUR` substances →
  `T3-SOUR`. No column for toxic plume; `Emergency Level` and evacuation fields are the nearest proxies.
- Data-quality note for the companion piece: `Release Type` files NGL under Gas, while the methodology lists it under
  Liquid.

### Back-test results (2026-10-29, snapshot 2026-10-28)

`code/src/cer_agent/backtest.py` → `output/backtest-report.md`. 1,952 records (82 processing-plant records excluded):
98.8% reportable under the engine (239 precautionary, a deciding fact missing); `SIG-*` agrees with the CER flag on
99.2% of 1,265 testable records. The 23 records the rules don't make reportable are mostly non-hydrocarbon releases
with no recorded environmental effect: logged as data findings (`output/findings-log.md`).
Two engine fixes came out of it: `JUDGE` substances need the release-rate check, and a release of a toxic
non-hydrocarbon substance (`TOXIC_NON_HC` in `rules.py`) opens the `INC-b` question (U1-OPEN).

