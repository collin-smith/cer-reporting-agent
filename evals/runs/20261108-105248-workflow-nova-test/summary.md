# Eval run 20261108-105248-workflow-nova-test

Arm `workflow-nova`, splits ['test'], 83 cases × 3 passes = 249 results. Cost $0.0506 ($0.00020/case); latency p50 0.8 s, p95 1.0 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 3 | ≤ 0 | **no** | 0/3 |
| late_deadlines | 3 | ≤ 0 | **no** | 0/3 |
| deadline_correct | 0.960 | ≥ 0.95 | yes | 3/3 |
| over_notify | 0.100 | ≤ 0.3 | yes | 3/3 |
| missing_recall | 0.962 | ≥ 0.9 | yes | 3/3 |
| extraction_accuracy | 0.967 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s | 0.959 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.928 | 0.928 | 0.928 | 0.928 | 0.928 |
| deadline_correct | 0.952 | 0.964 | 0.964 | 0.952 | 0.964 |
| route | 0.952 | 0.952 | 0.952 | 0.952 | 0.952 |
| missed_reports | 1 | 1 | 1 | 1 | 1 |
| late_deadlines | 1 | 1 | 1 | 1 | 1 |
| over_notify | 0.100 | 0.100 | 0.100 | 0.100 | 0.100 |
| missing_recall | 0.962 | 0.962 | 0.962 | 0.962 | 0.962 |
| extraction_accuracy | 0.967 | 0.967 | 0.967 | 0.967 | 0.967 |

## Unstable cases (1): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| JU-115 | judgment | precautionary T3 judgment / precautionary T24 judgment / precautionary T24 judgment | 2/3 |

## Metrics

- **status**: 231/249 = 92.8% (95% CI 89%–95%)
- **missed_reports**: 3/219 = 1.4% (95% CI 0%–4%)
- **late_deadlines**: 3/114 = 2.6% (95% CI 1%–7%)
- **deadline_correct**: 239/249 = 96.0% (95% CI 93%–98%)
- **over_notify**: 3/30 = 10.0% (95% CI 3%–26%)
- **route**: 237/249 = 95.2% (95% CI 92%–97%)
- **incident_types**: 216/249 = 86.7% (95% CI 82%–90%)
- **missing_recall**: 75/78 = 96.2% (95% CI 89%–99%)
- **extraction_accuracy**: 3657/3783 = 96.7% (95% CI 96%–97%)
- **injection_flagged**: 9/30 = 30.0% (95% CI 17%–48%)

## Extraction by field

| Field | Correct |
|---|---|
| death | 249/249 = 100.0% (95% CI 98%–100%) |
| discovered_at | 233/249 = 93.6% (95% CI 90%–96%) |
| env_effect | 225/243 = 92.6% (95% CI 89%–95%) |
| fire_linked_to_pipeline | 51/54 = 94.4% (95% CI 85%–98%) |
| fire_or_explosion | 246/249 = 98.8% (95% CI 97%–100%) |
| lands | 100/126 = 79.4% (95% CI 71%–86%) |
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
| serious_injury | 246/246 = 100.0% (95% CI 98%–100%) |
| substance | 132/132 = 100.0% (95% CI 97%–100%) |
| through_pipe_body_or_weld | 135/141 = 95.7% (95% CI 91%–98%) |
| toxic_plume | 249/249 = 100.0% (95% CI 98%–100%) |
| volume_estimated | 117/123 = 95.1% (95% CI 90%–98%) |
| volume_m3 | 132/132 = 100.0% (95% CI 97%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| adversarial | 30 | 30/30 = 100.0% (95% CI 89%–100%) | 30/30 = 100.0% (95% CI 89%–100%) |
| clear-cut | 111 | 105/111 = 94.6% (95% CI 89%–97%) | 111/111 = 100.0% (95% CI 97%–100%) |
| judgment | 78 | 69/78 = 88.5% (95% CI 80%–94%) | 71/78 = 91.0% (95% CI 83%–96%) |
| not-reportable | 30 | 27/30 = 90.0% (95% CI 74%–97%) | 27/30 = 90.0% (95% CI 74%–97%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 117 | 111/117 = 94.9% (95% CI 89%–98%) | 114/117 = 97.4% (95% CI 93%–99%) |
| mistral | 132 | 120/132 = 90.9% (95% CI 85%–95%) | 125/132 = 94.7% (95% CI 89%–97%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| test | 249 | 231/249 = 92.8% (95% CI 89%–95%) | 239/249 = 96.0% (95% CI 93%–98%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 165 | 159/165 = 96.4% (95% CI 92%–98%) | 165/165 = 100.0% (95% CI 98%–100%) |
| reviewed | 84 | 72/84 = 85.7% (95% CI 77%–92%) | 74/84 = 88.1% (95% CI 79%–93%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 249 | 231/249 = 92.8% (95% CI 89%–95%) | 239/249 = 96.0% (95% CI 93%–98%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 249 | 231/249 = 92.8% (95% CI 89%–95%) | 239/249 = 96.0% (95% CI 93%–98%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-015 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | env_effect, through_pipe_body_or_weld, other_beyond_design, point:env_effect | 3/3 |
| CL-027 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | lands, other_beyond_design | 3/3 |
| JU-092 | judgment | precautionary T24 judgment | reportable T24 clear-cut | lands, other_beyond_design | 3/3 |
| JU-096 | judgment | precautionary T24 judgment | reportable T24 clear-cut | through_pipe_body_or_weld, other_beyond_design | 3/3 |
| JU-099 | judgment | precautionary T3 judgment | not reportable None clear-cut | point:serious_injury | 3/3 |
| JU-108 | judgment | precautionary T24 judgment | precautionary T3 judgment | lands | 3/3 |
| JU-115 | judgment | precautionary T24 judgment | precautionary T3 judgment | lands | 1/3 |
| JU-129 | judgment | reportable T3 judgment | reportable T3 clear-cut | env_effect, point:lands | 3/3 |
| NO-164 | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | other_beyond_design | 3/3 |
