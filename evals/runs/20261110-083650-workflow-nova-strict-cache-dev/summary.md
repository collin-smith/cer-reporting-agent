# Eval run 20261110-083650-workflow-nova-strict-cache-dev

Arm `workflow-nova-strict-cache`, splits ['dev'], 1 cases × 2 passes = 2 results. Cost $0.0006 ($0.00029/case); latency p50 1.2 s, p95 1.7 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 0 | ≤ 0 | yes | 2/2 |
| late_deadlines | 0 | ≤ 0 | yes | 2/2 |
| deadline_correct | 1.000 | ≥ 0.95 | yes | 2/2 |
| over_notify | n/a | ≤ 0.3 | **no** | 0/2 |
| missing_recall | n/a | ≥ 0.9 | **no** | 0/2 |
| extraction_accuracy | 1.000 | ≥ 0.95 | yes | 2/2 |
| latency_p95_s | 1.692 | ≤ 300 | yes | 2/2 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Min | Max |
|---|---|---|---|---|
| status | 1.000 | 1.000 | 1.000 | 1.000 |
| deadline_correct | 1.000 | 1.000 | 1.000 | 1.000 |
| route | 1.000 | 1.000 | 1.000 | 1.000 |
| missed_reports | 0 | 0 | 0 | 0 |
| late_deadlines | 0 | 0 | 0 | 0 |
| over_notify | n/a | n/a | n/a | n/a |
| missing_recall | n/a | n/a | n/a | n/a |
| extraction_accuracy | 1.000 | 1.000 | 1.000 | 1.000 |

## Unstable cases (0): the answer changed between passes

None.

## Metrics

- **status**: 2/2 = 100.0% (95% CI 34%–100%)
- **missed_reports**: 0/2 = 0.0% (95% CI 0%–66%)
- **late_deadlines**: n/a
- **deadline_correct**: 2/2 = 100.0% (95% CI 34%–100%)
- **over_notify**: n/a
- **route**: 2/2 = 100.0% (95% CI 34%–100%)
- **incident_types**: 2/2 = 100.0% (95% CI 34%–100%)
- **missing_recall**: n/a
- **extraction_accuracy**: 22/22 = 100.0% (95% CI 85%–100%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 2/2 = 100.0% (95% CI 34%–100%) |
| discovered_at | 2/2 = 100.0% (95% CI 34%–100%) |
| env_effect | 2/2 = 100.0% (95% CI 34%–100%) |
| fire_or_explosion | 2/2 = 100.0% (95% CI 34%–100%) |
| limit_kpa | 2/2 = 100.0% (95% CI 34%–100%) |
| other_beyond_design | 2/2 = 100.0% (95% CI 34%–100%) |
| pressure_kpa | 2/2 = 100.0% (95% CI 34%–100%) |
| release | 2/2 = 100.0% (95% CI 34%–100%) |
| rupture | 2/2 = 100.0% (95% CI 34%–100%) |
| serious_injury | 2/2 = 100.0% (95% CI 34%–100%) |
| toxic_plume | 2/2 = 100.0% (95% CI 34%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 2 | 2/2 = 100.0% (95% CI 34%–100%) | 2/2 = 100.0% (95% CI 34%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 2 | 2/2 = 100.0% (95% CI 34%–100%) | 2/2 = 100.0% (95% CI 34%–100%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| test | 2 | 2/2 = 100.0% (95% CI 34%–100%) | 2/2 = 100.0% (95% CI 34%–100%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 2 | 2/2 = 100.0% (95% CI 34%–100%) | 2/2 = 100.0% (95% CI 34%–100%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 2 | 2/2 = 100.0% (95% CI 34%–100%) | 2/2 = 100.0% (95% CI 34%–100%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 2 | 2/2 = 100.0% (95% CI 34%–100%) | 2/2 = 100.0% (95% CI 34%–100%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
