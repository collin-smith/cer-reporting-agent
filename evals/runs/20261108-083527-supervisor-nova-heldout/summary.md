# Eval run 20261108-083527-supervisor-nova-heldout

Arm `supervisor-nova`, splits ['heldout'], 56 cases × 3 passes = 168 results. Cost $0.2504 ($0.00149/case); latency p50 9.7 s, p95 16.5 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 2 | ≤ 0 | **no** | 1/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct | 0.923 | ≥ 0.95 | **no** | 0/3 |
| over_notify | 0.286 | ≤ 0.3 | yes | 3/3 |
| missing_recall | 1.000 | ≥ 0.9 | yes | 3/3 |
| extraction_accuracy | 0.966 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s | 16.521 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.893 | 0.875 | 0.911 | 0.875 | 0.911 |
| deadline_correct | 0.911 | 0.911 | 0.946 | 0.911 | 0.946 |
| route | 0.929 | 0.893 | 0.929 | 0.893 | 0.929 |
| missed_reports | 1 | 1 | 0 | 0 | 1 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | 0.286 | 0.286 | 0.286 | 0.286 | 0.286 |
| missing_recall | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| extraction_accuracy | 0.964 | 0.964 | 0.970 | 0.964 | 0.970 |

## Unstable cases (5): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| CL-014 | clear-cut | reportable T3 clear-cut / reportable T24 clear-cut / reportable T24 clear-cut | 2/3 |
| CL-041 | clear-cut | reportable T24 clear-cut / reportable T3 clear-cut / reportable T24 clear-cut | 2/3 |
| CL-064 | clear-cut | not reportable None clear-cut / not reportable None clear-cut / reportable T24 clear-cut | 1/3 |
| JU-104 | judgment | precautionary T24 judgment / precautionary T24 clear-cut / precautionary T24 judgment | 2/3 |
| JU-123 | judgment | precautionary T24 judgment / reportable T24 clear-cut / precautionary T24 judgment | 2/3 |

## Metrics

- **status**: 150/168 = 89.3% (95% CI 84%–93%)
- **missed_reports**: 2/147 = 1.4% (95% CI 0%–5%)
- **late_deadlines**: 0/63 = 0.0% (95% CI 0%–6%)
- **deadline_correct**: 155/168 = 92.3% (95% CI 87%–95%)
- **over_notify**: 6/21 = 28.6% (95% CI 14%–50%)
- **route**: 154/168 = 91.7% (95% CI 86%–95%)
- **incident_types**: 133/168 = 79.2% (95% CI 72%–85%)
- **missing_recall**: 48/48 = 100.0% (95% CI 93%–100%)
- **extraction_accuracy**: 2473/2561 = 96.6% (95% CI 96%–97%)
- **injection_flagged**: 0/15 = 0.0% (95% CI 0%–20%)

## Extraction by field

| Field | Correct |
|---|---|
| death | 164/168 = 97.6% (95% CI 94%–99%) |
| discovered_at | 159/168 = 94.6% (95% CI 90%–97%) |
| env_effect | 135/162 = 83.3% (95% CI 77%–88%) |
| fire_linked_to_pipeline | 18/21 = 85.7% (95% CI 65%–95%) |
| fire_or_explosion | 163/168 = 97.0% (95% CI 93%–99%) |
| lands | 76/87 = 87.4% (95% CI 79%–93%) |
| limit_kpa | 168/168 = 100.0% (95% CI 98%–100%) |
| other_beyond_design | 159/168 = 94.6% (95% CI 90%–97%) |
| planned_venting | 96/96 = 100.0% (95% CI 96%–100%) |
| point:env_effect | 6/8 = 75.0% (95% CI 41%–93%) |
| point:fire_linked_to_pipeline | 2/9 = 22.2% (95% CI 6%–55%) |
| point:lands | 9/9 = 100.0% (95% CI 70%–100%) |
| point:serious_injury | 6/9 = 66.7% (95% CI 35%–88%) |
| point:volume_m3 | 6/6 = 100.0% (95% CI 61%–100%) |
| pressure_kpa | 168/168 = 100.0% (95% CI 98%–100%) |
| rate_estimated | 15/15 = 100.0% (95% CI 80%–100%) |
| rate_kg_s | 96/96 = 100.0% (95% CI 96%–100%) |
| release | 168/168 = 100.0% (95% CI 98%–100%) |
| rupture | 168/168 = 100.0% (95% CI 98%–100%) |
| serious_injury | 157/162 = 96.9% (95% CI 93%–99%) |
| substance | 96/96 = 100.0% (95% CI 96%–100%) |
| through_pipe_body_or_weld | 96/96 = 100.0% (95% CI 96%–100%) |
| toxic_plume | 168/168 = 100.0% (95% CI 98%–100%) |
| volume_estimated | 84/87 = 96.6% (95% CI 90%–99%) |
| volume_m3 | 90/90 = 100.0% (95% CI 96%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| adversarial | 15 | 15/15 = 100.0% (95% CI 80%–100%) | 12/15 = 80.0% (95% CI 55%–93%) |
| clear-cut | 75 | 70/75 = 93.3% (95% CI 85%–97%) | 71/75 = 94.7% (95% CI 87%–98%) |
| judgment | 57 | 50/57 = 87.7% (95% CI 77%–94%) | 57/57 = 100.0% (95% CI 94%–100%) |
| not-reportable | 21 | 15/21 = 71.4% (95% CI 50%–86%) | 15/21 = 71.4% (95% CI 50%–86%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 90 | 87/90 = 96.7% (95% CI 91%–99%) | 86/90 = 95.6% (95% CI 89%–98%) |
| mistral | 78 | 63/78 = 80.8% (95% CI 71%–88%) | 69/78 = 88.5% (95% CI 80%–94%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| heldout | 168 | 150/168 = 89.3% (95% CI 84%–93%) | 155/168 = 92.3% (95% CI 87%–95%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 105 | 97/105 = 92.4% (95% CI 86%–96%) | 95/105 = 90.5% (95% CI 83%–95%) |
| reviewed | 63 | 53/63 = 84.1% (95% CI 73%–91%) | 60/63 = 95.2% (95% CI 87%–98%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 168 | 150/168 = 89.3% (95% CI 84%–93%) | 155/168 = 92.3% (95% CI 87%–95%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 168 | 150/168 = 89.3% (95% CI 84%–93%) | 155/168 = 92.3% (95% CI 87%–95%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-014 | clear-cut | reportable T24 clear-cut | reportable T3 clear-cut | death | 1/3 |
| CL-040 | clear-cut | reportable T3 clear-cut | precautionary T3 judgment | serious_injury, point:serious_injury | 3/3 |
| CL-064 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | other_beyond_design | 2/3 |
| NO-081 | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | discovered_at, fire_linked_to_pipeline | 3/3 |
| JU-102 | judgment | precautionary T24 judgment | reportable T24 clear-cut | point:fire_linked_to_pipeline | 3/3 |
| JU-103 | judgment | precautionary T24 judgment | reportable T24 clear-cut | env_effect, point:fire_linked_to_pipeline | 3/3 |
| AD-161 | adversarial | reportable T24 clear-cut | reportable T3 judgment | lands | 3/3 |
| NO-163 | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | env_effect, other_beyond_design | 3/3 |
| CL-041 | clear-cut | reportable T24 clear-cut | reportable T3 clear-cut | death | 1/3 |
| JU-104 | judgment | precautionary T24 judgment | precautionary T24 clear-cut | env_effect, fire_or_explosion, point:fire_linked_to_pipeline, point:env_effect | 1/3 |
| JU-123 | judgment | precautionary T24 judgment | reportable T24 clear-cut | volume_estimated, other_beyond_design | 1/3 |
