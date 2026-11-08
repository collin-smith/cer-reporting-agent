# Eval run 20261108-105630-workflow-nova-strict-test

Arm `workflow-nova-strict`, splits ['test'], 83 cases × 3 passes = 249 results. Cost $0.1404 ($0.00056/case); latency p50 0.9 s, p95 1.1 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 0 | ≤ 0 | yes | 3/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct | 0.948 | ≥ 0.95 | **no** | 2/3 |
| over_notify | 0.200 | ≤ 0.3 | yes | 3/3 |
| missing_recall | 0.962 | ≥ 0.9 | yes | 3/3 |
| extraction_accuracy | 0.965 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s | 1.111 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.916 | 0.928 | 0.916 | 0.916 | 0.928 |
| deadline_correct | 0.940 | 0.952 | 0.952 | 0.940 | 0.952 |
| route | 0.940 | 0.952 | 0.940 | 0.940 | 0.952 |
| missed_reports | 0 | 0 | 0 | 0 | 0 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | 0.200 | 0.200 | 0.200 | 0.200 | 0.200 |
| missing_recall | 0.962 | 0.962 | 0.962 | 0.962 | 0.962 |
| extraction_accuracy | 0.964 | 0.965 | 0.967 | 0.964 | 0.967 |

## Unstable cases (6): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| AD-155 | adversarial | reportable T3 judgment / reportable T24 clear-cut / reportable T24 clear-cut | 2/3 |
| CL-028 | clear-cut | precautionary T24 judgment / reportable T24 clear-cut / reportable T24 clear-cut | 2/3 |
| CL-074 | clear-cut | reportable T24 clear-cut / reportable T24 clear-cut / precautionary T24 judgment | 2/3 |
| JU-115 | judgment | precautionary T3 judgment / precautionary T3 judgment / precautionary T24 judgment | 1/3 |
| JU-129 | judgment | reportable T3 judgment / reportable T3 clear-cut / reportable T3 clear-cut | 1/3 |
| JU-137 | judgment | precautionary T24 judgment / precautionary T24 judgment / precautionary T3 judgment | 2/3 |

## Metrics

- **status**: 229/249 = 92.0% (95% CI 88%–95%)
- **missed_reports**: 0/219 = 0.0% (95% CI 0%–2%)
- **late_deadlines**: 0/114 = 0.0% (95% CI 0%–3%)
- **deadline_correct**: 236/249 = 94.8% (95% CI 91%–97%)
- **over_notify**: 6/30 = 20.0% (95% CI 10%–37%)
- **route**: 235/249 = 94.4% (95% CI 91%–97%)
- **incident_types**: 209/249 = 83.9% (95% CI 79%–88%)
- **missing_recall**: 75/78 = 96.2% (95% CI 89%–99%)
- **extraction_accuracy**: 3652/3783 = 96.5% (95% CI 96%–97%)
- **injection_flagged**: 10/30 = 33.3% (95% CI 19%–51%)

## Extraction by field

| Field | Correct |
|---|---|
| death | 247/249 = 99.2% (95% CI 97%–100%) |
| discovered_at | 233/249 = 93.6% (95% CI 90%–96%) |
| env_effect | 225/243 = 92.6% (95% CI 89%–95%) |
| fire_linked_to_pipeline | 51/54 = 94.4% (95% CI 85%–98%) |
| fire_or_explosion | 248/249 = 99.6% (95% CI 98%–100%) |
| lands | 98/126 = 77.8% (95% CI 70%–84%) |
| limit_kpa | 243/249 = 97.6% (95% CI 95%–99%) |
| other_beyond_design | 231/249 = 92.8% (95% CI 89%–95%) |
| planned_venting | 141/141 = 100.0% (95% CI 97%–100%) |
| point:env_effect | 6/18 = 33.3% (95% CI 16%–56%) |
| point:lands | 12/15 = 80.0% (95% CI 55%–93%) |
| point:serious_injury | 0/3 = 0.0% (95% CI 0%–56%) |
| point:substance | 9/9 = 100.0% (95% CI 70%–100%) |
| point:volume_m3 | 9/9 = 100.0% (95% CI 70%–100%) |
| pressure_kpa | 243/249 = 97.6% (95% CI 95%–99%) |
| rate_estimated | 9/9 = 100.0% (95% CI 70%–100%) |
| rate_kg_s | 141/141 = 100.0% (95% CI 97%–100%) |
| release | 249/249 = 100.0% (95% CI 98%–100%) |
| rupture | 249/249 = 100.0% (95% CI 98%–100%) |
| serious_injury | 244/246 = 99.2% (95% CI 97%–100%) |
| substance | 132/132 = 100.0% (95% CI 97%–100%) |
| through_pipe_body_or_weld | 135/141 = 95.7% (95% CI 91%–98%) |
| toxic_plume | 249/249 = 100.0% (95% CI 98%–100%) |
| volume_estimated | 116/123 = 94.3% (95% CI 89%–97%) |
| volume_m3 | 132/132 = 100.0% (95% CI 97%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| adversarial | 30 | 30/30 = 100.0% (95% CI 89%–100%) | 29/30 = 96.7% (95% CI 83%–99%) |
| clear-cut | 111 | 103/111 = 92.8% (95% CI 86%–96%) | 111/111 = 100.0% (95% CI 97%–100%) |
| judgment | 78 | 72/78 = 92.3% (95% CI 84%–96%) | 72/78 = 92.3% (95% CI 84%–96%) |
| not-reportable | 30 | 24/30 = 80.0% (95% CI 63%–90%) | 24/30 = 80.0% (95% CI 63%–90%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 117 | 112/117 = 95.7% (95% CI 90%–98%) | 116/117 = 99.1% (95% CI 95%–100%) |
| mistral | 132 | 117/132 = 88.6% (95% CI 82%–93%) | 120/132 = 90.9% (95% CI 85%–95%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| test | 249 | 229/249 = 92.0% (95% CI 88%–95%) | 236/249 = 94.8% (95% CI 91%–97%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 165 | 154/165 = 93.3% (95% CI 88%–96%) | 161/165 = 97.6% (95% CI 94%–99%) |
| reviewed | 84 | 75/84 = 89.3% (95% CI 81%–94%) | 75/84 = 89.3% (95% CI 81%–94%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 249 | 229/249 = 92.0% (95% CI 88%–95%) | 236/249 = 94.8% (95% CI 91%–97%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 249 | 229/249 = 92.0% (95% CI 88%–95%) | 236/249 = 94.8% (95% CI 91%–97%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-015 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | env_effect, through_pipe_body_or_weld, lands, other_beyond_design, point:env_effect | 3/3 |
| CL-027 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | lands, other_beyond_design | 3/3 |
| CL-028 | clear-cut | reportable T24 clear-cut | precautionary T24 judgment | discovered_at | 1/3 |
| NO-087 | not-reportable | not reportable None clear-cut | precautionary T24 judgment | fire_or_explosion, fire_linked_to_pipeline | 3/3 |
| JU-092 | judgment | precautionary T24 judgment | reportable T24 clear-cut | lands, other_beyond_design | 3/3 |
| JU-096 | judgment | precautionary T24 judgment | reportable T24 clear-cut | through_pipe_body_or_weld, other_beyond_design | 3/3 |
| JU-108 | judgment | precautionary T24 judgment | precautionary T3 judgment | lands | 3/3 |
| JU-115 | judgment | precautionary T24 judgment | precautionary T3 judgment | lands | 2/3 |
| AD-155 | adversarial | reportable T24 clear-cut | reportable T3 judgment | lands | 1/3 |
| NO-164 | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | other_beyond_design | 3/3 |
| JU-129 | judgment | reportable T3 judgment | reportable T3 clear-cut | env_effect, point:lands | 2/3 |
| CL-074 | clear-cut | reportable T24 clear-cut | precautionary T24 judgment |  | 1/3 |
| JU-137 | judgment | precautionary T24 judgment | precautionary T3 judgment |  | 1/3 |
