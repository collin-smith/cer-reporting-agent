# Eval run 20261103-160020-workflow-nova-dev

Arm `workflow-nova`, splits ['dev'], 30 cases × 3 passes = 90 results. Cost $0.0173 ($0.00019/case); latency p50 0.8 s, p95 1.2 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 3 | ≤ 0 | **no** | 1/3 |
| late_deadlines | 1 | ≤ 0 | **no** | 2/3 |
| deadline_correct [proposed] | 0.867 | ≥ 0.95 | **no** | 0/3 |
| over_notify [proposed] | 0.000 | ≤ 0.3 | yes | 3/3 |
| missing_recall [proposed] | 0.911 | ≥ 0.9 | **no** | 2/3 |
| extraction_accuracy [proposed] | 0.953 | ≥ 0.95 | **no** | 2/3 |
| latency_p95_s [proposed] | 1.185 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.900 | 0.967 | 0.933 | 0.900 | 0.967 |
| deadline_correct | 0.867 | 0.900 | 0.833 | 0.833 | 0.900 |
| route | 0.833 | 0.833 | 0.833 | 0.833 | 0.833 |
| missed_reports | 2 | 0 | 1 | 0 | 2 |
| late_deadlines | 0 | 0 | 1 | 0 | 1 |
| over_notify | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| missing_recall | 0.867 | 0.933 | 0.933 | 0.867 | 0.933 |
| extraction_accuracy | 0.949 | 0.951 | 0.957 | 0.949 | 0.957 |

## Unstable cases (6): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| CL-034 | clear-cut | not reportable None clear-cut / precautionary T24 clear-cut / precautionary T24 clear-cut | 2/3 |
| CL-046 | clear-cut | not reportable None clear-cut / reportable T24 clear-cut / not reportable None clear-cut | 1/3 |
| CL-055 | clear-cut | reportable T24 clear-cut / reportable T3 clear-cut / reportable T3 clear-cut | 1/3 |
| JU-100 | judgment | precautionary T3 judgment / precautionary T3 clear-cut / precautionary T3 clear-cut | 1/3 |
| JU-142 | judgment | reportable T3 clear-cut / reportable T3 clear-cut / reportable T3 judgment | 1/3 |
| JU-143 | judgment | reportable T3 clear-cut / reportable T3 judgment / reportable T24 clear-cut | 1/3 |

## Metrics

- **status**: 84/90 = 93.3% (95% CI 86%–97%)
- **missed_reports**: 3/84 = 3.6% (95% CI 1%–10%)
- **late_deadlines**: 1/36 = 2.8% (95% CI 0%–14%)
- **deadline_correct**: 78/90 = 86.7% (95% CI 78%–92%)
- **over_notify**: 0/6 = 0.0% (95% CI 0%–39%)
- **route**: 75/90 = 83.3% (95% CI 74%–90%)
- **incident_types**: 62/90 = 68.9% (95% CI 59%–78%)
- **missing_recall**: 41/45 = 91.1% (95% CI 79%–96%)
- **extraction_accuracy**: 1412/1482 = 95.3% (95% CI 94%–96%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 90/90 = 100.0% (95% CI 96%–100%) |
| discovered_at | 90/90 = 100.0% (95% CI 96%–100%) |
| env_effect | 78/90 = 86.7% (95% CI 78%–92%) |
| fire_linked_to_pipeline | 6/6 = 100.0% (95% CI 61%–100%) |
| fire_or_explosion | 90/90 = 100.0% (95% CI 96%–100%) |
| lands | 61/69 = 88.4% (95% CI 79%–94%) |
| limit_kpa | 89/90 = 98.9% (95% CI 94%–100%) |
| other_beyond_design | 88/90 = 97.8% (95% CI 92%–99%) |
| planned_venting | 69/69 = 100.0% (95% CI 95%–100%) |
| point:env_effect | 0/3 = 0.0% (95% CI 0%–56%) |
| point:serious_injury | 3/3 = 100.0% (95% CI 44%–100%) |
| point:substance | 4/9 = 44.4% (95% CI 19%–73%) |
| point:volume_m3 | 3/3 = 100.0% (95% CI 44%–100%) |
| pressure_kpa | 90/90 = 100.0% (95% CI 96%–100%) |
| rate_estimated | 9/12 = 75.0% (95% CI 47%–91%) |
| rate_kg_s | 69/69 = 100.0% (95% CI 95%–100%) |
| release | 80/90 = 88.9% (95% CI 81%–94%) |
| rupture | 90/90 = 100.0% (95% CI 96%–100%) |
| serious_injury | 74/87 = 85.1% (95% CI 76%–91%) |
| substance | 60/60 = 100.0% (95% CI 94%–100%) |
| through_pipe_body_or_weld | 69/69 = 100.0% (95% CI 95%–100%) |
| toxic_plume | 90/90 = 100.0% (95% CI 96%–100%) |
| volume_estimated | 48/57 = 84.2% (95% CI 73%–91%) |
| volume_m3 | 62/66 = 93.9% (95% CI 85%–98%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 48 | 45/48 = 93.8% (95% CI 83%–98%) | 40/48 = 83.3% (95% CI 70%–91%) |
| judgment | 36 | 33/36 = 91.7% (95% CI 78%–97%) | 32/36 = 88.9% (95% CI 75%–96%) |
| not-reportable | 6 | 6/6 = 100.0% (95% CI 61%–100%) | 6/6 = 100.0% (95% CI 61%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 51 | 51/51 = 100.0% (95% CI 93%–100%) | 43/51 = 84.3% (95% CI 72%–92%) |
| mistral | 39 | 33/39 = 84.6% (95% CI 70%–93%) | 35/39 = 89.7% (95% CI 76%–96%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 90 | 84/90 = 93.3% (95% CI 86%–97%) | 78/90 = 86.7% (95% CI 78%–92%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 54 | 51/54 = 94.4% (95% CI 85%–98%) | 46/54 = 85.2% (95% CI 73%–92%) |
| reviewed | 36 | 33/36 = 91.7% (95% CI 78%–97%) | 32/36 = 88.9% (95% CI 75%–96%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 90 | 84/90 = 93.3% (95% CI 86%–97%) | 78/90 = 86.7% (95% CI 78%–92%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-023 | clear-cut | reportable T24 clear-cut | reportable T3 clear-cut | release | 3/3 |
| CL-034 | clear-cut | precautionary T24 clear-cut | not reportable None clear-cut | volume_m3 | 1/3 |
| CL-046 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | other_beyond_design | 2/3 |
| JU-110 | judgment | precautionary T24 judgment | precautionary T3 clear-cut | serious_injury, env_effect | 3/3 |
| JU-124 | judgment | precautionary T24 judgment | reportable T24 clear-cut | volume_estimated, rate_estimated | 3/3 |
| JU-142 | judgment | reportable T3 judgment | reportable T3 clear-cut | volume_m3, lands, point:substance | 2/3 |
| JU-143 | judgment | reportable T3 judgment | reportable T3 clear-cut | serious_injury, env_effect | 2/3 |
| JU-147 | judgment | reportable T3 judgment | reportable T3 clear-cut | serious_injury | 3/3 |
| CL-055 | clear-cut | reportable T24 clear-cut | reportable T3 clear-cut | release | 2/3 |
| JU-100 | judgment | precautionary T3 judgment | precautionary T3 clear-cut | release | 2/3 |
