# Eval run 20261103-170409-workflow-nova-dev

Arm `workflow-nova`, splits ['dev'], 30 cases × 3 passes = 90 results. Cost $0.0177 ($0.00020/case); latency p50 0.8 s, p95 1.1 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 3 | ≤ 0 | **no** | 0/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct [proposed] | 0.833 | ≥ 0.95 | **no** | 0/3 |
| over_notify [proposed] | 0.000 | ≤ 0.3 | yes | 3/3 |
| missing_recall [proposed] | 0.956 | ≥ 0.9 | yes | 3/3 |
| extraction_accuracy [proposed] | 0.941 | ≥ 0.95 | **no** | 0/3 |
| latency_p95_s [proposed] | 1.080 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.933 | 0.933 | 0.933 | 0.933 | 0.933 |
| deadline_correct | 0.833 | 0.833 | 0.833 | 0.833 | 0.833 |
| route | 0.767 | 0.767 | 0.767 | 0.767 | 0.767 |
| missed_reports | 1 | 1 | 1 | 1 | 1 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| missing_recall | 0.933 | 1.000 | 0.933 | 0.933 | 1.000 |
| extraction_accuracy | 0.941 | 0.941 | 0.939 | 0.939 | 0.941 |

## Unstable cases (5): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| JU-110 | judgment | precautionary T3 clear-cut / precautionary T24 judgment / precautionary T24 judgment | 2/3 |
| JU-111 | judgment | precautionary T3 clear-cut / precautionary T24 clear-cut / precautionary T24 clear-cut | 0/3 |
| JU-126 | judgment | precautionary T24 judgment / precautionary T3 clear-cut / precautionary T3 clear-cut | 1/3 |
| JU-127 | judgment | precautionary T24 judgment / precautionary T3 clear-cut / precautionary T3 clear-cut | 1/3 |
| JU-147 | judgment | reportable T3 clear-cut / reportable T3 judgment / reportable T3 judgment | 2/3 |

## Metrics

- **status**: 84/90 = 93.3% (95% CI 86%–97%)
- **missed_reports**: 3/84 = 3.6% (95% CI 1%–10%)
- **late_deadlines**: 0/36 = 0.0% (95% CI 0%–10%)
- **deadline_correct**: 75/90 = 83.3% (95% CI 74%–90%)
- **over_notify**: 0/6 = 0.0% (95% CI 0%–39%)
- **route**: 69/90 = 76.7% (95% CI 67%–84%)
- **incident_types**: 75/90 = 83.3% (95% CI 74%–90%)
- **missing_recall**: 43/45 = 95.6% (95% CI 85%–99%)
- **extraction_accuracy**: 1397/1485 = 94.1% (95% CI 93%–95%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 90/90 = 100.0% (95% CI 96%–100%) |
| discovered_at | 90/90 = 100.0% (95% CI 96%–100%) |
| env_effect | 86/90 = 95.6% (95% CI 89%–98%) |
| fire_linked_to_pipeline | 6/6 = 100.0% (95% CI 61%–100%) |
| fire_or_explosion | 90/90 = 100.0% (95% CI 96%–100%) |
| lands | 53/69 = 76.8% (95% CI 66%–85%) |
| limit_kpa | 90/90 = 100.0% (95% CI 96%–100%) |
| other_beyond_design | 87/90 = 96.7% (95% CI 91%–99%) |
| planned_venting | 69/69 = 100.0% (95% CI 95%–100%) |
| point:env_effect | 0/6 = 0.0% (95% CI 0%–39%) |
| point:serious_injury | 3/3 = 100.0% (95% CI 44%–100%) |
| point:substance | 9/9 = 100.0% (95% CI 70%–100%) |
| point:volume_m3 | 3/3 = 100.0% (95% CI 44%–100%) |
| pressure_kpa | 90/90 = 100.0% (95% CI 96%–100%) |
| rate_estimated | 7/12 = 58.3% (95% CI 32%–81%) |
| rate_kg_s | 62/69 = 89.9% (95% CI 81%–95%) |
| release | 84/90 = 93.3% (95% CI 86%–97%) |
| rupture | 90/90 = 100.0% (95% CI 96%–100%) |
| serious_injury | 86/87 = 98.9% (95% CI 94%–100%) |
| substance | 60/60 = 100.0% (95% CI 94%–100%) |
| through_pipe_body_or_weld | 69/69 = 100.0% (95% CI 95%–100%) |
| toxic_plume | 90/90 = 100.0% (95% CI 96%–100%) |
| volume_estimated | 48/57 = 84.2% (95% CI 73%–91%) |
| volume_m3 | 35/66 = 53.0% (95% CI 41%–65%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 48 | 42/48 = 87.5% (95% CI 75%–94%) | 42/48 = 87.5% (95% CI 75%–94%) |
| judgment | 36 | 36/36 = 100.0% (95% CI 90%–100%) | 27/36 = 75.0% (95% CI 59%–86%) |
| not-reportable | 6 | 6/6 = 100.0% (95% CI 61%–100%) | 6/6 = 100.0% (95% CI 61%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 51 | 51/51 = 100.0% (95% CI 93%–100%) | 43/51 = 84.3% (95% CI 72%–92%) |
| mistral | 39 | 33/39 = 84.6% (95% CI 70%–93%) | 32/39 = 82.1% (95% CI 67%–91%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 90 | 84/90 = 93.3% (95% CI 86%–97%) | 75/90 = 83.3% (95% CI 74%–90%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 54 | 48/54 = 88.9% (95% CI 78%–95%) | 48/54 = 88.9% (95% CI 78%–95%) |
| reviewed | 36 | 36/36 = 100.0% (95% CI 90%–100%) | 27/36 = 75.0% (95% CI 59%–86%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 90 | 84/90 = 93.3% (95% CI 86%–97%) | 75/90 = 83.3% (95% CI 74%–90%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-007 | clear-cut | reportable T3 clear-cut | precautionary T3 clear-cut | volume_m3 | 3/3 |
| CL-023 | clear-cut | reportable T24 clear-cut | reportable T3 clear-cut | release | 3/3 |
| CL-046 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | other_beyond_design | 3/3 |
| JU-110 | judgment | precautionary T24 judgment | precautionary T3 clear-cut | volume_m3, lands | 1/3 |
| JU-111 | judgment | precautionary T24 judgment | precautionary T3 clear-cut | volume_m3, lands | 3/3 |
| JU-114 | judgment | precautionary T24 judgment | precautionary T24 clear-cut | volume_m3 | 3/3 |
| JU-124 | judgment | precautionary T24 judgment | precautionary T3 clear-cut | volume_m3, volume_estimated, rate_kg_s, rate_estimated | 3/3 |
| JU-142 | judgment | reportable T3 judgment | reportable T3 clear-cut | volume_m3, lands | 3/3 |
| JU-143 | judgment | reportable T3 judgment | reportable T3 clear-cut | volume_m3 | 3/3 |
| JU-147 | judgment | reportable T3 judgment | reportable T3 clear-cut | volume_m3, lands | 1/3 |
| JU-126 | judgment | precautionary T24 judgment | precautionary T3 clear-cut | volume_m3, rate_kg_s, lands | 2/3 |
| JU-127 | judgment | precautionary T24 judgment | precautionary T3 clear-cut | volume_m3, rate_kg_s, rate_estimated, lands | 2/3 |
