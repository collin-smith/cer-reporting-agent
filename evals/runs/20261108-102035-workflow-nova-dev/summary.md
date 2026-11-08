# Eval run 20261108-102035-workflow-nova-dev

Arm `workflow-nova`, splits ['dev'], 33 cases × 3 passes = 99 results. Cost $0.0202 ($0.00020/case); latency p50 0.8 s, p95 1.0 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 2 | ≤ 0 | **no** | 1/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct | 0.949 | ≥ 0.95 | **no** | 1/3 |
| over_notify | 0.000 | ≤ 0.3 | yes | 3/3 |
| missing_recall | 0.933 | ≥ 0.9 | yes | 3/3 |
| extraction_accuracy | 0.985 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s | 0.990 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.970 | 0.939 | 0.939 | 0.939 | 0.970 |
| deadline_correct | 0.970 | 0.939 | 0.939 | 0.939 | 0.970 |
| route | 0.939 | 0.909 | 0.909 | 0.909 | 0.939 |
| missed_reports | 0 | 1 | 1 | 0 | 1 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| missing_recall | 0.933 | 0.933 | 0.933 | 0.933 | 0.933 |
| extraction_accuracy | 0.989 | 0.983 | 0.983 | 0.983 | 0.989 |

## Unstable cases (1): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| JU-127 | judgment | precautionary T24 judgment / not reportable None clear-cut / not reportable None clear-cut | 1/3 |

## Metrics

- **status**: 94/99 = 94.9% (95% CI 89%–98%)
- **missed_reports**: 2/93 = 2.2% (95% CI 1%–8%)
- **late_deadlines**: 0/36 = 0.0% (95% CI 0%–10%)
- **deadline_correct**: 94/99 = 94.9% (95% CI 89%–98%)
- **over_notify**: 0/6 = 0.0% (95% CI 0%–39%)
- **route**: 91/99 = 91.9% (95% CI 85%–96%)
- **incident_types**: 92/99 = 92.9% (95% CI 86%–97%)
- **missing_recall**: 42/45 = 93.3% (95% CI 82%–98%)
- **extraction_accuracy**: 1559/1583 = 98.5% (95% CI 98%–99%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 99/99 = 100.0% (95% CI 96%–100%) |
| discovered_at | 99/99 = 100.0% (95% CI 96%–100%) |
| env_effect | 97/99 = 98.0% (95% CI 93%–99%) |
| fire_linked_to_pipeline | 6/6 = 100.0% (95% CI 61%–100%) |
| fire_or_explosion | 99/99 = 100.0% (95% CI 96%–100%) |
| lands | 60/69 = 87.0% (95% CI 77%–93%) |
| limit_kpa | 99/99 = 100.0% (95% CI 96%–100%) |
| other_beyond_design | 99/99 = 100.0% (95% CI 96%–100%) |
| planned_venting | 69/69 = 100.0% (95% CI 95%–100%) |
| point:env_effect | 0/5 = 0.0% (95% CI 0%–43%) |
| point:serious_injury | 3/3 = 100.0% (95% CI 44%–100%) |
| point:substance | 9/9 = 100.0% (95% CI 70%–100%) |
| point:volume_m3 | 3/3 = 100.0% (95% CI 44%–100%) |
| pressure_kpa | 99/99 = 100.0% (95% CI 96%–100%) |
| rate_estimated | 7/12 = 58.3% (95% CI 32%–81%) |
| rate_kg_s | 69/69 = 100.0% (95% CI 95%–100%) |
| release | 99/99 = 100.0% (95% CI 96%–100%) |
| rupture | 99/99 = 100.0% (95% CI 96%–100%) |
| serious_injury | 96/96 = 100.0% (95% CI 96%–100%) |
| substance | 60/60 = 100.0% (95% CI 94%–100%) |
| through_pipe_body_or_weld | 69/69 = 100.0% (95% CI 95%–100%) |
| toxic_plume | 99/99 = 100.0% (95% CI 96%–100%) |
| volume_estimated | 57/57 = 100.0% (95% CI 94%–100%) |
| volume_m3 | 63/66 = 95.5% (95% CI 87%–98%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 57 | 57/57 = 100.0% (95% CI 94%–100%) | 54/57 = 94.7% (95% CI 86%–98%) |
| judgment | 36 | 31/36 = 86.1% (95% CI 71%–94%) | 34/36 = 94.4% (95% CI 82%–98%) |
| not-reportable | 6 | 6/6 = 100.0% (95% CI 61%–100%) | 6/6 = 100.0% (95% CI 61%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 57 | 55/57 = 96.5% (95% CI 88%–99%) | 55/57 = 96.5% (95% CI 88%–99%) |
| mistral | 42 | 39/42 = 92.9% (95% CI 81%–98%) | 39/42 = 92.9% (95% CI 81%–98%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 99 | 94/99 = 94.9% (95% CI 89%–98%) | 94/99 = 94.9% (95% CI 89%–98%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 63 | 63/63 = 100.0% (95% CI 94%–100%) | 60/63 = 95.2% (95% CI 87%–98%) |
| reviewed | 36 | 31/36 = 86.1% (95% CI 71%–94%) | 34/36 = 94.4% (95% CI 82%–98%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 99 | 94/99 = 94.9% (95% CI 89%–98%) | 94/99 = 94.9% (95% CI 89%–98%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 99 | 94/99 = 94.9% (95% CI 89%–98%) | 94/99 = 94.9% (95% CI 89%–98%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-034 | clear-cut | precautionary T24 clear-cut | precautionary T3 judgment | volume_m3, lands | 3/3 |
| JU-124 | judgment | precautionary T24 judgment | reportable T24 clear-cut | rate_estimated | 3/3 |
| JU-127 | judgment | precautionary T24 judgment | not reportable None clear-cut | rate_estimated | 2/3 |
