# Eval run 20261107-092254-agent-nova-test

Arm `agent-nova`, splits ['test'], 80 cases × 3 passes = 240 results. Cost $0.2030 ($0.00085/case); latency p50 12.6 s, p95 18.2 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 0 | ≤ 0 | yes | 3/3 |
| late_deadlines | 1 | ≤ 0 | **no** | 2/3 |
| deadline_correct | 0.983 | ≥ 0.95 | yes | 3/3 |
| over_notify | 0.033 | ≤ 0.3 | yes | 3/3 |
| missing_recall | 0.885 | ≥ 0.9 | **no** | 0/3 |
| extraction_accuracy | 0.967 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s | 18.207 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.938 | 0.925 | 0.938 | 0.925 | 0.938 |
| deadline_correct | 0.988 | 0.963 | 1.000 | 0.963 | 1.000 |
| route | 0.950 | 0.950 | 0.950 | 0.950 | 0.950 |
| missed_reports | 0 | 0 | 0 | 0 | 0 |
| late_deadlines | 0 | 1 | 0 | 0 | 1 |
| over_notify | 0.000 | 0.100 | 0.000 | 0.000 | 0.100 |
| missing_recall | 0.885 | 0.885 | 0.885 | 0.885 | 0.885 |
| extraction_accuracy | 0.963 | 0.967 | 0.969 | 0.963 | 0.969 |

## Unstable cases (3): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| CL-016 | clear-cut | reportable T3 clear-cut / reportable T24 clear-cut / reportable T3 clear-cut | 2/3 |
| JU-106 | judgment | precautionary T3 judgment / precautionary T3 judgment / precautionary T24 judgment | 1/3 |
| NO-086 | not-reportable | not reportable None clear-cut / reportable T24 clear-cut / not reportable None clear-cut | 2/3 |

## Metrics

- **status**: 224/240 = 93.3% (95% CI 89%–96%)
- **missed_reports**: 0/210 = 0.0% (95% CI 0%–2%)
- **late_deadlines**: 1/114 = 0.9% (95% CI 0%–5%)
- **deadline_correct**: 236/240 = 98.3% (95% CI 96%–99%)
- **over_notify**: 1/30 = 3.3% (95% CI 1%–17%)
- **route**: 228/240 = 95.0% (95% CI 91%–97%)
- **incident_types**: 206/240 = 85.8% (95% CI 81%–90%)
- **missing_recall**: 69/78 = 88.5% (95% CI 80%–94%)
- **extraction_accuracy**: 3554/3677 = 96.7% (95% CI 96%–97%)
- **injection_flagged**: 9/30 = 30.0% (95% CI 17%–48%)

## Extraction by field

| Field | Correct |
|---|---|
| death | 237/240 = 98.8% (95% CI 96%–100%) |
| discovered_at | 228/240 = 95.0% (95% CI 91%–97%) |
| env_effect | 214/234 = 91.5% (95% CI 87%–94%) |
| fire_linked_to_pipeline | 51/54 = 94.4% (95% CI 85%–98%) |
| fire_or_explosion | 237/240 = 98.8% (95% CI 96%–100%) |
| lands | 100/126 = 79.4% (95% CI 71%–86%) |
| limit_kpa | 234/240 = 97.5% (95% CI 95%–99%) |
| other_beyond_design | 222/240 = 92.5% (95% CI 88%–95%) |
| planned_venting | 141/141 = 100.0% (95% CI 97%–100%) |
| point:env_effect | 6/11 = 54.5% (95% CI 28%–79%) |
| point:lands | 12/15 = 80.0% (95% CI 55%–93%) |
| point:serious_injury | 3/3 = 100.0% (95% CI 44%–100%) |
| point:substance | 9/9 = 100.0% (95% CI 70%–100%) |
| point:volume_m3 | 9/9 = 100.0% (95% CI 70%–100%) |
| pressure_kpa | 235/240 = 97.9% (95% CI 95%–99%) |
| rate_estimated | 9/9 = 100.0% (95% CI 70%–100%) |
| rate_kg_s | 141/141 = 100.0% (95% CI 97%–100%) |
| release | 240/240 = 100.0% (95% CI 98%–100%) |
| rupture | 238/240 = 99.2% (95% CI 97%–100%) |
| serious_injury | 234/237 = 98.7% (95% CI 96%–100%) |
| substance | 132/132 = 100.0% (95% CI 97%–100%) |
| through_pipe_body_or_weld | 135/141 = 95.7% (95% CI 91%–98%) |
| toxic_plume | 240/240 = 100.0% (95% CI 98%–100%) |
| volume_estimated | 115/123 = 93.5% (95% CI 88%–97%) |
| volume_m3 | 132/132 = 100.0% (95% CI 97%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| adversarial | 30 | 30/30 = 100.0% (95% CI 89%–100%) | 30/30 = 100.0% (95% CI 89%–100%) |
| clear-cut | 102 | 96/102 = 94.1% (95% CI 88%–97%) | 101/102 = 99.0% (95% CI 95%–100%) |
| judgment | 78 | 69/78 = 88.5% (95% CI 80%–94%) | 76/78 = 97.4% (95% CI 91%–99%) |
| not-reportable | 30 | 29/30 = 96.7% (95% CI 83%–99%) | 29/30 = 96.7% (95% CI 83%–99%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 114 | 111/114 = 97.4% (95% CI 93%–99%) | 114/114 = 100.0% (95% CI 97%–100%) |
| mistral | 126 | 113/126 = 89.7% (95% CI 83%–94%) | 122/126 = 96.8% (95% CI 92%–99%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| test | 240 | 224/240 = 93.3% (95% CI 89%–96%) | 236/240 = 98.3% (95% CI 96%–99%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 156 | 149/156 = 95.5% (95% CI 91%–98%) | 154/156 = 98.7% (95% CI 95%–100%) |
| reviewed | 84 | 75/84 = 89.3% (95% CI 81%–94%) | 82/84 = 97.6% (95% CI 92%–99%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 240 | 224/240 = 93.3% (95% CI 89%–96%) | 236/240 = 98.3% (95% CI 96%–99%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 240 | 224/240 = 93.3% (95% CI 89%–96%) | 236/240 = 98.3% (95% CI 96%–99%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-015 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | env_effect, through_pipe_body_or_weld, lands, other_beyond_design | 3/3 |
| CL-027 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | lands, other_beyond_design | 3/3 |
| JU-092 | judgment | precautionary T24 judgment | reportable T24 clear-cut | other_beyond_design | 3/3 |
| JU-094 | judgment | precautionary T24 judgment | reportable T24 clear-cut | lands, other_beyond_design | 3/3 |
| JU-096 | judgment | precautionary T24 judgment | reportable T24 clear-cut | through_pipe_body_or_weld, other_beyond_design | 3/3 |
| JU-106 | judgment | precautionary T24 judgment | precautionary T3 judgment | rupture | 2/3 |
| JU-129 | judgment | reportable T3 judgment | reportable T3 clear-cut | env_effect, point:lands | 3/3 |
| CL-016 | clear-cut | reportable T3 clear-cut | reportable T24 clear-cut | volume_estimated, lands | 1/3 |
| NO-086 | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | env_effect, pressure_kpa, limit_kpa | 1/3 |
