# Eval run 20261108-081029-workflow-nova-heldout

Arm `workflow-nova`, splits ['heldout'], 56 cases × 3 passes = 168 results. Cost $0.0336 ($0.00020/case); latency p50 0.8 s, p95 1.7 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 3 | ≤ 0 | **no** | 0/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct | 0.929 | ≥ 0.95 | **no** | 0/3 |
| over_notify | 0.286 | ≤ 0.3 | yes | 3/3 |
| missing_recall | 1.000 | ≥ 0.9 | yes | 3/3 |
| extraction_accuracy | 0.968 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s | 1.672 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.875 | 0.893 | 0.893 | 0.875 | 0.893 |
| deadline_correct | 0.929 | 0.929 | 0.929 | 0.929 | 0.929 |
| route | 0.929 | 0.946 | 0.946 | 0.929 | 0.946 |
| missed_reports | 1 | 1 | 1 | 1 | 1 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | 0.286 | 0.286 | 0.286 | 0.286 | 0.286 |
| missing_recall | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| extraction_accuracy | 0.968 | 0.967 | 0.967 | 0.967 | 0.968 |

## Unstable cases (1): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| JU-101 | judgment | reportable T3 clear-cut / precautionary T3 judgment / precautionary T3 judgment | 2/3 |

## Metrics

- **status**: 149/168 = 88.7% (95% CI 83%–93%)
- **missed_reports**: 3/147 = 2.0% (95% CI 1%–6%)
- **late_deadlines**: 0/63 = 0.0% (95% CI 0%–6%)
- **deadline_correct**: 156/168 = 92.9% (95% CI 88%–96%)
- **over_notify**: 6/21 = 28.6% (95% CI 14%–50%)
- **route**: 158/168 = 94.0% (95% CI 89%–97%)
- **incident_types**: 139/168 = 82.7% (95% CI 76%–88%)
- **missing_recall**: 48/48 = 100.0% (95% CI 93%–100%)
- **extraction_accuracy**: 2477/2560 = 96.8% (95% CI 96%–97%)
- **injection_flagged**: 0/15 = 0.0% (95% CI 0%–20%)

## Extraction by field

| Field | Correct |
|---|---|
| death | 166/168 = 98.8% (95% CI 96%–100%) |
| discovered_at | 159/168 = 94.6% (95% CI 90%–97%) |
| env_effect | 142/162 = 87.7% (95% CI 82%–92%) |
| fire_linked_to_pipeline | 18/21 = 85.7% (95% CI 65%–95%) |
| fire_or_explosion | 162/168 = 96.4% (95% CI 92%–98%) |
| lands | 72/87 = 82.8% (95% CI 73%–89%) |
| limit_kpa | 168/168 = 100.0% (95% CI 98%–100%) |
| other_beyond_design | 159/168 = 94.6% (95% CI 90%–97%) |
| planned_venting | 96/96 = 100.0% (95% CI 96%–100%) |
| point:env_effect | 6/7 = 85.7% (95% CI 49%–97%) |
| point:fire_linked_to_pipeline | 3/9 = 33.3% (95% CI 12%–65%) |
| point:lands | 9/9 = 100.0% (95% CI 70%–100%) |
| point:serious_injury | 5/9 = 55.6% (95% CI 27%–81%) |
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
| clear-cut | 75 | 69/75 = 92.0% (95% CI 84%–96%) | 72/75 = 96.0% (95% CI 89%–99%) |
| judgment | 57 | 50/57 = 87.7% (95% CI 77%–94%) | 57/57 = 100.0% (95% CI 94%–100%) |
| not-reportable | 21 | 15/21 = 71.4% (95% CI 50%–86%) | 15/21 = 71.4% (95% CI 50%–86%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 90 | 87/90 = 96.7% (95% CI 91%–99%) | 87/90 = 96.7% (95% CI 91%–99%) |
| mistral | 78 | 62/78 = 79.5% (95% CI 69%–87%) | 69/78 = 88.5% (95% CI 80%–94%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| heldout | 168 | 149/168 = 88.7% (95% CI 83%–93%) | 156/168 = 92.9% (95% CI 88%–96%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 105 | 96/105 = 91.4% (95% CI 85%–95%) | 96/105 = 91.4% (95% CI 85%–95%) |
| reviewed | 63 | 53/63 = 84.1% (95% CI 73%–91%) | 60/63 = 95.2% (95% CI 87%–98%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 168 | 149/168 = 88.7% (95% CI 83%–93%) | 156/168 = 92.9% (95% CI 88%–96%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 168 | 149/168 = 88.7% (95% CI 83%–93%) | 156/168 = 92.9% (95% CI 88%–96%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-040 | clear-cut | reportable T3 clear-cut | precautionary T3 judgment | serious_injury, point:serious_injury | 3/3 |
| CL-064 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | other_beyond_design | 3/3 |
| NO-081 | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | discovered_at, fire_linked_to_pipeline | 3/3 |
| JU-101 | judgment | precautionary T3 judgment | reportable T3 clear-cut | point:serious_injury | 1/3 |
| JU-102 | judgment | precautionary T24 judgment | reportable T24 clear-cut | point:fire_linked_to_pipeline | 3/3 |
| JU-103 | judgment | precautionary T24 judgment | reportable T24 clear-cut | env_effect, point:fire_linked_to_pipeline | 3/3 |
| AD-161 | adversarial | reportable T24 clear-cut | reportable T3 clear-cut | lands | 3/3 |
| NO-163 | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | other_beyond_design | 3/3 |
