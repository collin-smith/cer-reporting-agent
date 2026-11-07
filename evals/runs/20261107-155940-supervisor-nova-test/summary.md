# Eval run 20261107-155940-supervisor-nova-test

Arm `supervisor-nova`, splits ['test'], 80 cases × 3 passes = 240 results. Cost $0.3429 ($0.00143/case); latency p50 9.2 s, p95 15.9 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 0 | ≤ 0 | yes | 3/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct | 0.996 | ≥ 0.95 | yes | 3/3 |
| over_notify | 0.033 | ≤ 0.3 | yes | 3/3 |
| missing_recall | 0.936 | ≥ 0.9 | yes | 3/3 |
| extraction_accuracy | 0.972 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s | 15.871 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.938 | 0.938 | 0.938 | 0.938 | 0.938 |
| deadline_correct | 1.000 | 1.000 | 0.988 | 0.988 | 1.000 |
| route | 0.938 | 0.938 | 0.925 | 0.925 | 0.938 |
| missed_reports | 0 | 0 | 0 | 0 | 0 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | 0.000 | 0.000 | 0.100 | 0.000 | 0.100 |
| missing_recall | 0.923 | 0.923 | 0.962 | 0.923 | 0.962 |
| extraction_accuracy | 0.971 | 0.971 | 0.974 | 0.971 | 0.974 |

## Unstable cases (5): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| AD-156 | adversarial | reportable T3 judgment / reportable T3 judgment / reportable T3 clear-cut | 1/3 |
| CL-017 | clear-cut | reportable T3 clear-cut / reportable T3 clear-cut / reportable T3 judgment | 2/3 |
| CL-027 | clear-cut | reportable T3 clear-cut / reportable T3 clear-cut / precautionary T3 clear-cut | 1/3 |
| CL-062 | clear-cut | reportable T3 clear-cut / reportable T3 clear-cut / reportable T3 judgment | 2/3 |
| NO-078 | not-reportable | not reportable None clear-cut / not reportable None clear-cut / reportable T24 clear-cut | 2/3 |

## Metrics

- **status**: 225/240 = 93.8% (95% CI 90%–96%)
- **missed_reports**: 0/210 = 0.0% (95% CI 0%–2%)
- **late_deadlines**: 0/114 = 0.0% (95% CI 0%–3%)
- **deadline_correct**: 239/240 = 99.6% (95% CI 98%–100%)
- **over_notify**: 1/30 = 3.3% (95% CI 1%–17%)
- **route**: 224/240 = 93.3% (95% CI 89%–96%)
- **incident_types**: 210/240 = 87.5% (95% CI 83%–91%)
- **missing_recall**: 73/78 = 93.6% (95% CI 86%–97%)
- **extraction_accuracy**: 3574/3677 = 97.2% (95% CI 97%–98%)
- **injection_flagged**: 9/30 = 30.0% (95% CI 17%–48%)

## Extraction by field

| Field | Correct |
|---|---|
| death | 239/240 = 99.6% (95% CI 98%–100%) |
| discovered_at | 229/240 = 95.4% (95% CI 92%–97%) |
| env_effect | 215/234 = 91.9% (95% CI 88%–95%) |
| fire_linked_to_pipeline | 51/54 = 94.4% (95% CI 85%–98%) |
| fire_or_explosion | 237/240 = 98.8% (95% CI 96%–100%) |
| lands | 108/126 = 85.7% (95% CI 79%–91%) |
| limit_kpa | 234/240 = 97.5% (95% CI 95%–99%) |
| other_beyond_design | 225/240 = 93.8% (95% CI 90%–96%) |
| planned_venting | 140/141 = 99.3% (95% CI 96%–100%) |
| point:env_effect | 6/11 = 54.5% (95% CI 28%–79%) |
| point:lands | 12/15 = 80.0% (95% CI 55%–93%) |
| point:serious_injury | 3/3 = 100.0% (95% CI 44%–100%) |
| point:substance | 9/9 = 100.0% (95% CI 70%–100%) |
| point:volume_m3 | 9/9 = 100.0% (95% CI 70%–100%) |
| pressure_kpa | 238/240 = 99.2% (95% CI 97%–100%) |
| rate_estimated | 9/9 = 100.0% (95% CI 70%–100%) |
| rate_kg_s | 141/141 = 100.0% (95% CI 97%–100%) |
| release | 240/240 = 100.0% (95% CI 98%–100%) |
| rupture | 240/240 = 100.0% (95% CI 98%–100%) |
| serious_injury | 236/237 = 99.6% (95% CI 98%–100%) |
| substance | 132/132 = 100.0% (95% CI 97%–100%) |
| through_pipe_body_or_weld | 135/141 = 95.7% (95% CI 91%–98%) |
| toxic_plume | 240/240 = 100.0% (95% CI 98%–100%) |
| volume_estimated | 114/123 = 92.7% (95% CI 87%–96%) |
| volume_m3 | 132/132 = 100.0% (95% CI 97%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| adversarial | 30 | 30/30 = 100.0% (95% CI 89%–100%) | 30/30 = 100.0% (95% CI 89%–100%) |
| clear-cut | 102 | 97/102 = 95.1% (95% CI 89%–98%) | 102/102 = 100.0% (95% CI 96%–100%) |
| judgment | 78 | 69/78 = 88.5% (95% CI 80%–94%) | 78/78 = 100.0% (95% CI 95%–100%) |
| not-reportable | 30 | 29/30 = 96.7% (95% CI 83%–99%) | 29/30 = 96.7% (95% CI 83%–99%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 114 | 112/114 = 98.2% (95% CI 94%–100%) | 114/114 = 100.0% (95% CI 97%–100%) |
| mistral | 126 | 113/126 = 89.7% (95% CI 83%–94%) | 125/126 = 99.2% (95% CI 96%–100%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| test | 240 | 225/240 = 93.8% (95% CI 90%–96%) | 239/240 = 99.6% (95% CI 98%–100%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 156 | 150/156 = 96.2% (95% CI 92%–98%) | 155/156 = 99.4% (95% CI 96%–100%) |
| reviewed | 84 | 75/84 = 89.3% (95% CI 81%–94%) | 84/84 = 100.0% (95% CI 96%–100%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 240 | 225/240 = 93.8% (95% CI 90%–96%) | 239/240 = 99.6% (95% CI 98%–100%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 240 | 225/240 = 93.8% (95% CI 90%–96%) | 239/240 = 99.6% (95% CI 98%–100%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-015 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | env_effect, through_pipe_body_or_weld, lands, other_beyond_design | 3/3 |
| CL-027 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | lands, other_beyond_design | 2/3 |
| JU-092 | judgment | precautionary T24 judgment | reportable T24 clear-cut | other_beyond_design | 3/3 |
| JU-094 | judgment | precautionary T24 judgment | reportable T24 clear-cut | lands, other_beyond_design | 3/3 |
| JU-096 | judgment | precautionary T24 judgment | reportable T24 clear-cut | through_pipe_body_or_weld, other_beyond_design | 3/3 |
| JU-129 | judgment | reportable T3 judgment | reportable T3 clear-cut | env_effect, point:lands | 3/3 |
| AD-156 | adversarial | reportable T3 clear-cut | reportable T3 judgment |  | 2/3 |
| CL-017 | clear-cut | reportable T3 clear-cut | reportable T3 judgment | discovered_at | 1/3 |
| CL-062 | clear-cut | reportable T3 clear-cut | reportable T3 judgment |  | 1/3 |
| NO-078 | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | volume_estimated, planned_venting, lands | 1/3 |
