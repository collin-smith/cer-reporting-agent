# Eval run 20261109-103607-agent-nova-stop-dev

Arm `agent-nova-stop`, splits ['dev'], 33 cases × 3 passes = 99 results. Cost $0.0707 ($0.00071/case); latency p50 3.6 s, p95 11.7 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 1 | ≤ 0 | **no** | 2/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct | 0.960 | ≥ 0.95 | **no** | 2/3 |
| over_notify | 0.000 | ≤ 0.3 | yes | 3/3 |
| missing_recall | 0.889 | ≥ 0.9 | **no** | 1/3 |
| extraction_accuracy | 0.983 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s | 11.700 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.970 | 0.970 | 0.939 | 0.939 | 0.970 |
| deadline_correct | 0.970 | 0.970 | 0.939 | 0.939 | 0.970 |
| route | 0.909 | 0.939 | 0.909 | 0.909 | 0.939 |
| missed_reports | 0 | 0 | 1 | 0 | 1 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| missing_recall | 0.867 | 0.867 | 0.933 | 0.867 | 0.933 |
| extraction_accuracy | 0.977 | 0.985 | 0.987 | 0.977 | 0.987 |

## Unstable cases (2): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| CL-055 | clear-cut | reportable T24 judgment / reportable T24 clear-cut / reportable T24 clear-cut | 2/3 |
| JU-127 | judgment | precautionary T24 judgment / precautionary T24 judgment / not reportable None clear-cut | 2/3 |

## Metrics

- **status**: 95/99 = 96.0% (95% CI 90%–98%)
- **missed_reports**: 1/93 = 1.1% (95% CI 0%–6%)
- **late_deadlines**: 0/36 = 0.0% (95% CI 0%–10%)
- **deadline_correct**: 95/99 = 96.0% (95% CI 90%–98%)
- **over_notify**: 0/6 = 0.0% (95% CI 0%–39%)
- **route**: 91/99 = 91.9% (95% CI 85%–96%)
- **incident_types**: 93/99 = 93.9% (95% CI 87%–97%)
- **missing_recall**: 40/45 = 88.9% (95% CI 77%–95%)
- **extraction_accuracy**: 1555/1582 = 98.3% (95% CI 98%–99%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 99/99 = 100.0% (95% CI 96%–100%) |
| discovered_at | 99/99 = 100.0% (95% CI 96%–100%) |
| env_effect | 95/99 = 96.0% (95% CI 90%–98%) |
| fire_linked_to_pipeline | 6/6 = 100.0% (95% CI 61%–100%) |
| fire_or_explosion | 99/99 = 100.0% (95% CI 96%–100%) |
| lands | 60/69 = 87.0% (95% CI 77%–93%) |
| limit_kpa | 97/99 = 98.0% (95% CI 93%–99%) |
| other_beyond_design | 99/99 = 100.0% (95% CI 96%–100%) |
| planned_venting | 69/69 = 100.0% (95% CI 95%–100%) |
| point:env_effect | 0/4 = 0.0% (95% CI 0%–49%) |
| point:serious_injury | 3/3 = 100.0% (95% CI 44%–100%) |
| point:substance | 9/9 = 100.0% (95% CI 70%–100%) |
| point:volume_m3 | 3/3 = 100.0% (95% CI 44%–100%) |
| pressure_kpa | 98/99 = 99.0% (95% CI 94%–100%) |
| rate_estimated | 8/12 = 66.7% (95% CI 39%–86%) |
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
| judgment | 36 | 32/36 = 88.9% (95% CI 75%–96%) | 35/36 = 97.2% (95% CI 86%–100%) |
| not-reportable | 6 | 6/6 = 100.0% (95% CI 61%–100%) | 6/6 = 100.0% (95% CI 61%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 57 | 56/57 = 98.2% (95% CI 91%–100%) | 56/57 = 98.2% (95% CI 91%–100%) |
| mistral | 42 | 39/42 = 92.9% (95% CI 81%–98%) | 39/42 = 92.9% (95% CI 81%–98%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 99 | 95/99 = 96.0% (95% CI 90%–98%) | 95/99 = 96.0% (95% CI 90%–98%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 63 | 63/63 = 100.0% (95% CI 94%–100%) | 60/63 = 95.2% (95% CI 87%–98%) |
| reviewed | 36 | 32/36 = 88.9% (95% CI 75%–96%) | 35/36 = 97.2% (95% CI 86%–100%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 99 | 95/99 = 96.0% (95% CI 90%–98%) | 95/99 = 96.0% (95% CI 90%–98%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 99 | 95/99 = 96.0% (95% CI 90%–98%) | 95/99 = 96.0% (95% CI 90%–98%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-034 | clear-cut | precautionary T24 clear-cut | precautionary T3 judgment | volume_m3, lands | 3/3 |
| CL-055 | clear-cut | reportable T24 clear-cut | reportable T24 judgment |  | 1/3 |
| JU-124 | judgment | precautionary T24 judgment | reportable T24 clear-cut | rate_estimated | 3/3 |
| JU-127 | judgment | precautionary T24 judgment | not reportable None clear-cut | rate_estimated | 1/3 |
