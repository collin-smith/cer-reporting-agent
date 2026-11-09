# Eval run 20261109-102527-agent-nova-lg-dev

Arm `agent-nova-lg`, splits ['dev'], 33 cases × 3 passes = 99 results. Cost $0.0642 ($0.00065/case); latency p50 4.2 s, p95 8.8 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 2 | ≤ 0 | **no** | 1/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct | 0.970 | ≥ 0.95 | **no** | 2/3 |
| over_notify | 0.167 | ≤ 0.3 | **no** | 2/3 |
| missing_recall | 0.889 | ≥ 0.9 | **no** | 2/3 |
| extraction_accuracy | 0.985 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s | 8.828 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.939 | 0.939 | 0.909 | 0.909 | 0.939 |
| deadline_correct | 1.000 | 0.970 | 0.939 | 0.939 | 1.000 |
| route | 0.909 | 0.909 | 0.879 | 0.879 | 0.909 |
| missed_reports | 0 | 1 | 1 | 0 | 1 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | 0.000 | 0.000 | 0.500 | 0.000 | 0.500 |
| missing_recall | 0.800 | 0.933 | 0.933 | 0.800 | 0.933 |
| extraction_accuracy | 0.981 | 0.991 | 0.985 | 0.981 | 0.991 |

## Unstable cases (4): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| CL-007 | clear-cut | reportable T3 judgment / reportable T3 clear-cut / reportable T3 clear-cut | 2/3 |
| CL-051 | clear-cut | reportable T3 clear-cut / precautionary T3 clear-cut / precautionary T3 clear-cut | 2/3 |
| JU-127 | judgment | precautionary T24 judgment / not reportable None clear-cut / not reportable None clear-cut | 1/3 |
| NO-090 | not-reportable | not reportable None clear-cut / not reportable None clear-cut / precautionary T24 judgment | 2/3 |

## Metrics

- **status**: 92/99 = 92.9% (95% CI 86%–97%)
- **missed_reports**: 2/93 = 2.2% (95% CI 1%–8%)
- **late_deadlines**: 0/36 = 0.0% (95% CI 0%–10%)
- **deadline_correct**: 96/99 = 97.0% (95% CI 91%–99%)
- **over_notify**: 1/6 = 16.7% (95% CI 3%–56%)
- **route**: 89/99 = 89.9% (95% CI 82%–94%)
- **incident_types**: 92/99 = 92.9% (95% CI 86%–97%)
- **missing_recall**: 40/45 = 88.9% (95% CI 77%–95%)
- **extraction_accuracy**: 1559/1582 = 98.5% (95% CI 98%–99%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 99/99 = 100.0% (95% CI 96%–100%) |
| discovered_at | 99/99 = 100.0% (95% CI 96%–100%) |
| env_effect | 97/99 = 98.0% (95% CI 93%–99%) |
| fire_linked_to_pipeline | 6/6 = 100.0% (95% CI 61%–100%) |
| fire_or_explosion | 99/99 = 100.0% (95% CI 96%–100%) |
| lands | 64/69 = 92.8% (95% CI 84%–97%) |
| limit_kpa | 98/99 = 99.0% (95% CI 94%–100%) |
| other_beyond_design | 99/99 = 100.0% (95% CI 96%–100%) |
| planned_venting | 69/69 = 100.0% (95% CI 95%–100%) |
| point:env_effect | 0/4 = 0.0% (95% CI 0%–49%) |
| point:serious_injury | 3/3 = 100.0% (95% CI 44%–100%) |
| point:substance | 9/9 = 100.0% (95% CI 70%–100%) |
| point:volume_m3 | 3/3 = 100.0% (95% CI 44%–100%) |
| pressure_kpa | 98/99 = 99.0% (95% CI 94%–100%) |
| rate_estimated | 7/12 = 58.3% (95% CI 32%–81%) |
| rate_kg_s | 68/69 = 98.6% (95% CI 92%–100%) |
| release | 99/99 = 100.0% (95% CI 96%–100%) |
| rupture | 99/99 = 100.0% (95% CI 96%–100%) |
| serious_injury | 96/96 = 100.0% (95% CI 96%–100%) |
| substance | 59/60 = 98.3% (95% CI 91%–100%) |
| through_pipe_body_or_weld | 69/69 = 100.0% (95% CI 95%–100%) |
| toxic_plume | 99/99 = 100.0% (95% CI 96%–100%) |
| volume_estimated | 57/57 = 100.0% (95% CI 94%–100%) |
| volume_m3 | 63/66 = 95.5% (95% CI 87%–98%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 57 | 56/57 = 98.2% (95% CI 91%–100%) | 57/57 = 100.0% (95% CI 94%–100%) |
| judgment | 36 | 31/36 = 86.1% (95% CI 71%–94%) | 34/36 = 94.4% (95% CI 82%–98%) |
| not-reportable | 6 | 5/6 = 83.3% (95% CI 44%–97%) | 5/6 = 83.3% (95% CI 44%–97%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 57 | 54/57 = 94.7% (95% CI 86%–98%) | 54/57 = 94.7% (95% CI 86%–98%) |
| mistral | 42 | 38/42 = 90.5% (95% CI 78%–96%) | 42/42 = 100.0% (95% CI 92%–100%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 99 | 92/99 = 92.9% (95% CI 86%–97%) | 96/99 = 97.0% (95% CI 91%–99%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 63 | 61/63 = 96.8% (95% CI 89%–99%) | 62/63 = 98.4% (95% CI 92%–100%) |
| reviewed | 36 | 31/36 = 86.1% (95% CI 71%–94%) | 34/36 = 94.4% (95% CI 82%–98%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 99 | 92/99 = 92.9% (95% CI 86%–97%) | 96/99 = 97.0% (95% CI 91%–99%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 99 | 92/99 = 92.9% (95% CI 86%–97%) | 96/99 = 97.0% (95% CI 91%–99%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-007 | clear-cut | reportable T3 clear-cut | reportable T3 judgment |  | 1/3 |
| CL-034 | clear-cut | precautionary T24 clear-cut | precautionary T24 judgment | volume_m3 | 3/3 |
| CL-051 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | rate_kg_s | 1/3 |
| JU-124 | judgment | precautionary T24 judgment | reportable T24 clear-cut | rate_estimated | 3/3 |
| JU-127 | judgment | precautionary T24 judgment | not reportable None clear-cut | rate_estimated | 2/3 |
| NO-090 | not-reportable | not reportable None clear-cut | precautionary T24 judgment | substance | 1/3 |
