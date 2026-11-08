# Eval run 20261108-112146-workflow-nova-strict-dev

Arm `workflow-nova-strict`, splits ['dev'], 4 cases × 3 passes = 12 results. Cost $0.0067 ($0.00056/case); latency p50 0.9 s, p95 2.2 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 0 | ≤ 0 | yes | 3/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct | 0.833 | ≥ 0.95 | **no** | 1/3 |
| over_notify | 0.333 | ≤ 0.3 | **no** | 1/3 |
| missing_recall | n/a | ≥ 0.9 | **no** | 0/3 |
| extraction_accuracy | 0.948 | ≥ 0.95 | **no** | 0/3 |
| latency_p95_s | 2.188 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.500 | 0.750 | 0.500 | 0.500 | 0.750 |
| deadline_correct | 0.750 | 1.000 | 0.750 | 0.750 | 1.000 |
| route | 0.500 | 0.750 | 0.500 | 0.500 | 0.750 |
| missed_reports | 0 | 0 | 0 | 0 | 0 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | 0.500 | 0.000 | 0.500 | 0.000 | 0.500 |
| missing_recall | n/a | n/a | n/a | n/a | n/a |
| extraction_accuracy | 0.948 | 0.948 | 0.948 | 0.948 | 0.948 |

## Unstable cases (1): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| NO-164 | not-reportable | precautionary T24 judgment / not reportable None clear-cut / precautionary T24 judgment | 1/3 |

## Metrics

- **status**: 7/12 = 58.3% (95% CI 32%–81%)
- **missed_reports**: 0/6 = 0.0% (95% CI 0%–39%)
- **late_deadlines**: n/a
- **deadline_correct**: 10/12 = 83.3% (95% CI 55%–95%)
- **over_notify**: 2/6 = 33.3% (95% CI 10%–70%)
- **route**: 7/12 = 58.3% (95% CI 32%–81%)
- **incident_types**: 7/12 = 58.3% (95% CI 32%–81%)
- **missing_recall**: n/a
- **extraction_accuracy**: 165/174 = 94.8% (95% CI 90%–97%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 12/12 = 100.0% (95% CI 76%–100%) |
| discovered_at | 12/12 = 100.0% (95% CI 76%–100%) |
| env_effect | 9/9 = 100.0% (95% CI 70%–100%) |
| fire_or_explosion | 12/12 = 100.0% (95% CI 76%–100%) |
| lands | 3/6 = 50.0% (95% CI 19%–81%) |
| limit_kpa | 12/12 = 100.0% (95% CI 76%–100%) |
| other_beyond_design | 9/12 = 75.0% (95% CI 47%–91%) |
| planned_venting | 6/6 = 100.0% (95% CI 61%–100%) |
| point:env_effect | 3/3 = 100.0% (95% CI 44%–100%) |
| pressure_kpa | 12/12 = 100.0% (95% CI 76%–100%) |
| rate_kg_s | 6/6 = 100.0% (95% CI 61%–100%) |
| release | 12/12 = 100.0% (95% CI 76%–100%) |
| rupture | 12/12 = 100.0% (95% CI 76%–100%) |
| serious_injury | 12/12 = 100.0% (95% CI 76%–100%) |
| substance | 6/6 = 100.0% (95% CI 61%–100%) |
| through_pipe_body_or_weld | 3/6 = 50.0% (95% CI 19%–81%) |
| toxic_plume | 12/12 = 100.0% (95% CI 76%–100%) |
| volume_estimated | 6/6 = 100.0% (95% CI 61%–100%) |
| volume_m3 | 6/6 = 100.0% (95% CI 61%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| judgment | 6 | 3/6 = 50.0% (95% CI 19%–81%) | 6/6 = 100.0% (95% CI 61%–100%) |
| not-reportable | 6 | 4/6 = 66.7% (95% CI 30%–90%) | 4/6 = 66.7% (95% CI 30%–90%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 3 | 3/3 = 100.0% (95% CI 44%–100%) | 3/3 = 100.0% (95% CI 44%–100%) |
| mistral | 9 | 4/9 = 44.4% (95% CI 19%–73%) | 7/9 = 77.8% (95% CI 45%–94%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| heldout | 3 | 3/3 = 100.0% (95% CI 44%–100%) | 3/3 = 100.0% (95% CI 44%–100%) |
| test | 9 | 4/9 = 44.4% (95% CI 19%–73%) | 7/9 = 77.8% (95% CI 45%–94%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| reviewed | 12 | 7/12 = 58.3% (95% CI 32%–81%) | 10/12 = 83.3% (95% CI 55%–95%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 12 | 7/12 = 58.3% (95% CI 32%–81%) | 10/12 = 83.3% (95% CI 55%–95%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 12 | 7/12 = 58.3% (95% CI 32%–81%) | 10/12 = 83.3% (95% CI 55%–95%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| JU-092 | judgment | precautionary T24 judgment | reportable T24 clear-cut | lands, other_beyond_design | 3/3 |
| NO-164 | not-reportable | not reportable None clear-cut | precautionary T24 judgment |  | 2/3 |
