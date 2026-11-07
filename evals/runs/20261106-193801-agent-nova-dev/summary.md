# Eval run 20261106-193801-agent-nova-dev

Arm `agent-nova`, splits ['dev'], 30 cases × 3 passes = 90 results. Cost $0.0755 ($0.00084/case); latency p50 12.7 s, p95 23.4 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 2 | ≤ 0 | **no** | 1/3 |
| late_deadlines | 1 | ≤ 0 | **no** | 2/3 |
| deadline_correct | 0.956 | ≥ 0.95 | **no** | 2/3 |
| over_notify | 0.000 | ≤ 0.3 | yes | 3/3 |
| missing_recall | 0.933 | ≥ 0.9 | yes | 3/3 |
| extraction_accuracy | 0.987 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s | 23.446 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.967 | 0.933 | 0.933 | 0.933 | 0.967 |
| deadline_correct | 0.967 | 0.967 | 0.933 | 0.933 | 0.967 |
| route | 0.933 | 0.933 | 0.900 | 0.900 | 0.933 |
| missed_reports | 0 | 1 | 1 | 0 | 1 |
| late_deadlines | 0 | 0 | 1 | 0 | 1 |
| over_notify | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| missing_recall | 0.933 | 0.933 | 0.933 | 0.933 | 0.933 |
| extraction_accuracy | 0.988 | 0.986 | 0.988 | 0.986 | 0.988 |

## Unstable cases (3): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| CL-034 | clear-cut | precautionary T3 judgment / precautionary T24 judgment / precautionary T3 judgment | 0/3 |
| CL-046 | clear-cut | reportable T24 clear-cut / not reportable None clear-cut / reportable T24 clear-cut | 2/3 |
| JU-143 | judgment | reportable T3 judgment / reportable T3 judgment / not reportable None clear-cut | 2/3 |

## Metrics

- **status**: 85/90 = 94.4% (95% CI 88%–98%)
- **missed_reports**: 2/84 = 2.4% (95% CI 1%–8%)
- **late_deadlines**: 1/36 = 2.8% (95% CI 0%–14%)
- **deadline_correct**: 86/90 = 95.6% (95% CI 89%–98%)
- **over_notify**: 0/6 = 0.0% (95% CI 0%–39%)
- **route**: 83/90 = 92.2% (95% CI 85%–96%)
- **incident_types**: 85/90 = 94.4% (95% CI 88%–98%)
- **missing_recall**: 42/45 = 93.3% (95% CI 82%–98%)
- **extraction_accuracy**: 1463/1482 = 98.7% (95% CI 98%–99%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 90/90 = 100.0% (95% CI 96%–100%) |
| discovered_at | 90/90 = 100.0% (95% CI 96%–100%) |
| env_effect | 89/90 = 98.9% (95% CI 94%–100%) |
| fire_linked_to_pipeline | 6/6 = 100.0% (95% CI 61%–100%) |
| fire_or_explosion | 90/90 = 100.0% (95% CI 96%–100%) |
| lands | 62/69 = 89.9% (95% CI 81%–95%) |
| limit_kpa | 90/90 = 100.0% (95% CI 96%–100%) |
| other_beyond_design | 89/90 = 98.9% (95% CI 94%–100%) |
| planned_venting | 69/69 = 100.0% (95% CI 95%–100%) |
| point:env_effect | 0/3 = 0.0% (95% CI 0%–56%) |
| point:serious_injury | 3/3 = 100.0% (95% CI 44%–100%) |
| point:substance | 9/9 = 100.0% (95% CI 70%–100%) |
| point:volume_m3 | 3/3 = 100.0% (95% CI 44%–100%) |
| pressure_kpa | 90/90 = 100.0% (95% CI 96%–100%) |
| rate_estimated | 9/12 = 75.0% (95% CI 47%–91%) |
| rate_kg_s | 69/69 = 100.0% (95% CI 95%–100%) |
| release | 89/90 = 98.9% (95% CI 94%–100%) |
| rupture | 90/90 = 100.0% (95% CI 96%–100%) |
| serious_injury | 87/87 = 100.0% (95% CI 96%–100%) |
| substance | 60/60 = 100.0% (95% CI 94%–100%) |
| through_pipe_body_or_weld | 69/69 = 100.0% (95% CI 95%–100%) |
| toxic_plume | 90/90 = 100.0% (95% CI 96%–100%) |
| volume_estimated | 57/57 = 100.0% (95% CI 94%–100%) |
| volume_m3 | 63/66 = 95.5% (95% CI 87%–98%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 48 | 47/48 = 97.9% (95% CI 89%–100%) | 45/48 = 93.8% (95% CI 83%–98%) |
| judgment | 36 | 32/36 = 88.9% (95% CI 75%–96%) | 35/36 = 97.2% (95% CI 86%–100%) |
| not-reportable | 6 | 6/6 = 100.0% (95% CI 61%–100%) | 6/6 = 100.0% (95% CI 61%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 51 | 51/51 = 100.0% (95% CI 93%–100%) | 51/51 = 100.0% (95% CI 93%–100%) |
| mistral | 39 | 34/39 = 87.2% (95% CI 73%–94%) | 35/39 = 89.7% (95% CI 76%–96%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 90 | 85/90 = 94.4% (95% CI 88%–98%) | 86/90 = 95.6% (95% CI 89%–98%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 54 | 53/54 = 98.1% (95% CI 90%–100%) | 51/54 = 94.4% (95% CI 85%–98%) |
| reviewed | 36 | 32/36 = 88.9% (95% CI 75%–96%) | 35/36 = 97.2% (95% CI 86%–100%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 90 | 85/90 = 94.4% (95% CI 88%–98%) | 86/90 = 95.6% (95% CI 89%–98%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 90 | 85/90 = 94.4% (95% CI 88%–98%) | 86/90 = 95.6% (95% CI 89%–98%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-034 | clear-cut | precautionary T24 clear-cut | precautionary T3 judgment | volume_m3, lands | 3/3 |
| JU-124 | judgment | precautionary T24 judgment | reportable T24 clear-cut | rate_estimated | 3/3 |
| CL-046 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | other_beyond_design | 1/3 |
| JU-143 | judgment | reportable T3 judgment | not reportable None clear-cut | release | 1/3 |
