# Eval run 20261108-110138-workflow-nova-dev

Arm `workflow-nova`, splits ['dev'], 3 cases × 3 passes = 9 results. Cost $0.0018 ($0.00020/case); latency p50 0.8 s, p95 1.1 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 0 | ≤ 0 | yes | 3/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct | 1.000 | ≥ 0.95 | yes | 3/3 |
| over_notify | n/a | ≤ 0.3 | **no** | 0/3 |
| missing_recall | n/a | ≥ 0.9 | **no** | 0/3 |
| extraction_accuracy | 0.970 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s | 1.101 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| deadline_correct | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| route | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| missed_reports | 0 | 0 | 0 | 0 | 0 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | n/a | n/a | n/a | n/a | n/a |
| missing_recall | n/a | n/a | n/a | n/a | n/a |
| extraction_accuracy | 0.970 | 0.970 | 0.970 | 0.970 | 0.970 |

## Unstable cases (0): the answer changed between passes

None.

## Metrics

- **status**: 9/9 = 100.0% (95% CI 70%–100%)
- **missed_reports**: 0/9 = 0.0% (95% CI 0%–30%)
- **late_deadlines**: n/a
- **deadline_correct**: 9/9 = 100.0% (95% CI 70%–100%)
- **over_notify**: n/a
- **route**: 9/9 = 100.0% (95% CI 70%–100%)
- **incident_types**: 9/9 = 100.0% (95% CI 70%–100%)
- **missing_recall**: n/a
- **extraction_accuracy**: 96/99 = 97.0% (95% CI 91%–99%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 9/9 = 100.0% (95% CI 70%–100%) |
| discovered_at | 6/9 = 66.7% (95% CI 35%–88%) |
| env_effect | 9/9 = 100.0% (95% CI 70%–100%) |
| fire_or_explosion | 9/9 = 100.0% (95% CI 70%–100%) |
| limit_kpa | 9/9 = 100.0% (95% CI 70%–100%) |
| other_beyond_design | 9/9 = 100.0% (95% CI 70%–100%) |
| pressure_kpa | 9/9 = 100.0% (95% CI 70%–100%) |
| release | 9/9 = 100.0% (95% CI 70%–100%) |
| rupture | 9/9 = 100.0% (95% CI 70%–100%) |
| serious_injury | 9/9 = 100.0% (95% CI 70%–100%) |
| toxic_plume | 9/9 = 100.0% (95% CI 70%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 9 | 9/9 = 100.0% (95% CI 70%–100%) | 9/9 = 100.0% (95% CI 70%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 6 | 6/6 = 100.0% (95% CI 61%–100%) | 6/6 = 100.0% (95% CI 61%–100%) |
| mistral | 3 | 3/3 = 100.0% (95% CI 44%–100%) | 3/3 = 100.0% (95% CI 44%–100%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| heldout | 9 | 9/9 = 100.0% (95% CI 70%–100%) | 9/9 = 100.0% (95% CI 70%–100%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 9 | 9/9 = 100.0% (95% CI 70%–100%) | 9/9 = 100.0% (95% CI 70%–100%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 9 | 9/9 = 100.0% (95% CI 70%–100%) | 9/9 = 100.0% (95% CI 70%–100%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 9 | 9/9 = 100.0% (95% CI 70%–100%) | 9/9 = 100.0% (95% CI 70%–100%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
