# Eval run 20261103-165638-workflow-nova-dev

Arm `workflow-nova`, splits ['dev'], 30 cases × 3 passes = 90 results. Cost $0.0174 ($0.00019/case); latency p50 0.8 s, p95 1.1 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 4 | ≤ 0 | **no** | 0/3 |
| late_deadlines | 2 | ≤ 0 | **no** | 1/3 |
| deadline_correct [proposed] | 0.856 | ≥ 0.95 | **no** | 0/3 |
| over_notify [proposed] | 0.000 | ≤ 0.3 | yes | 3/3 |
| missing_recall [proposed] | 1.000 | ≥ 0.9 | yes | 3/3 |
| extraction_accuracy [proposed] | 0.954 | ≥ 0.95 | **no** | 2/3 |
| latency_p95_s [proposed] | 1.116 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.933 | 0.967 | 0.933 | 0.933 | 0.967 |
| deadline_correct | 0.867 | 0.867 | 0.833 | 0.833 | 0.867 |
| route | 0.933 | 0.900 | 0.900 | 0.900 | 0.933 |
| missed_reports | 1 | 1 | 2 | 1 | 2 |
| late_deadlines | 0 | 1 | 1 | 0 | 1 |
| over_notify | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| missing_recall | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| extraction_accuracy | 0.962 | 0.951 | 0.949 | 0.949 | 0.962 |

## Unstable cases (5): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| CL-020 | clear-cut | reportable T24 clear-cut / reportable T24 clear-cut / not reportable None clear-cut | 2/3 |
| JU-110 | judgment | precautionary T3 judgment / precautionary T24 judgment / precautionary T24 judgment | 2/3 |
| JU-124 | judgment | reportable T24 clear-cut / precautionary T24 judgment / precautionary T24 judgment | 2/3 |
| JU-142 | judgment | reportable T3 judgment / reportable T3 clear-cut / reportable T3 clear-cut | 1/3 |
| JU-143 | judgment | reportable T3 judgment / reportable T24 clear-cut / reportable T24 clear-cut | 1/3 |

## Metrics

- **status**: 85/90 = 94.4% (95% CI 88%–98%)
- **missed_reports**: 4/84 = 4.8% (95% CI 2%–12%)
- **late_deadlines**: 2/36 = 5.6% (95% CI 2%–18%)
- **deadline_correct**: 77/90 = 85.6% (95% CI 77%–91%)
- **over_notify**: 0/6 = 0.0% (95% CI 0%–39%)
- **route**: 82/90 = 91.1% (95% CI 83%–95%)
- **incident_types**: 73/90 = 81.1% (95% CI 72%–88%)
- **missing_recall**: 45/45 = 100.0% (95% CI 92%–100%)
- **extraction_accuracy**: 1414/1482 = 95.4% (95% CI 94%–96%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 90/90 = 100.0% (95% CI 96%–100%) |
| discovered_at | 90/90 = 100.0% (95% CI 96%–100%) |
| env_effect | 85/90 = 94.4% (95% CI 88%–98%) |
| fire_linked_to_pipeline | 6/6 = 100.0% (95% CI 61%–100%) |
| fire_or_explosion | 89/90 = 98.9% (95% CI 94%–100%) |
| lands | 52/69 = 75.4% (95% CI 64%–84%) |
| limit_kpa | 90/90 = 100.0% (95% CI 96%–100%) |
| other_beyond_design | 87/90 = 96.7% (95% CI 91%–99%) |
| planned_venting | 69/69 = 100.0% (95% CI 95%–100%) |
| point:env_effect | 0/3 = 0.0% (95% CI 0%–56%) |
| point:serious_injury | 3/3 = 100.0% (95% CI 44%–100%) |
| point:substance | 4/9 = 44.4% (95% CI 19%–73%) |
| point:volume_m3 | 3/3 = 100.0% (95% CI 44%–100%) |
| pressure_kpa | 87/90 = 96.7% (95% CI 91%–99%) |
| rate_estimated | 11/12 = 91.7% (95% CI 65%–99%) |
| rate_kg_s | 69/69 = 100.0% (95% CI 95%–100%) |
| release | 84/90 = 93.3% (95% CI 86%–97%) |
| rupture | 90/90 = 100.0% (95% CI 96%–100%) |
| serious_injury | 82/87 = 94.3% (95% CI 87%–98%) |
| substance | 60/60 = 100.0% (95% CI 94%–100%) |
| through_pipe_body_or_weld | 69/69 = 100.0% (95% CI 95%–100%) |
| toxic_plume | 90/90 = 100.0% (95% CI 96%–100%) |
| volume_estimated | 48/57 = 84.2% (95% CI 73%–91%) |
| volume_m3 | 56/66 = 84.8% (95% CI 74%–92%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 48 | 44/48 = 91.7% (95% CI 80%–97%) | 41/48 = 85.4% (95% CI 73%–93%) |
| judgment | 36 | 35/36 = 97.2% (95% CI 86%–100%) | 30/36 = 83.3% (95% CI 68%–92%) |
| not-reportable | 6 | 6/6 = 100.0% (95% CI 61%–100%) | 6/6 = 100.0% (95% CI 61%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 51 | 51/51 = 100.0% (95% CI 93%–100%) | 44/51 = 86.3% (95% CI 74%–93%) |
| mistral | 39 | 34/39 = 87.2% (95% CI 73%–94%) | 33/39 = 84.6% (95% CI 70%–93%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 90 | 85/90 = 94.4% (95% CI 88%–98%) | 77/90 = 85.6% (95% CI 77%–91%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 54 | 50/54 = 92.6% (95% CI 82%–97%) | 47/54 = 87.0% (95% CI 76%–94%) |
| reviewed | 36 | 35/36 = 97.2% (95% CI 86%–100%) | 30/36 = 83.3% (95% CI 68%–92%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 90 | 85/90 = 94.4% (95% CI 88%–98%) | 77/90 = 85.6% (95% CI 77%–91%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-023 | clear-cut | reportable T24 clear-cut | reportable T3 clear-cut | release | 3/3 |
| CL-046 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | other_beyond_design | 3/3 |
| JU-110 | judgment | precautionary T24 judgment | precautionary T3 judgment | lands | 1/3 |
| JU-124 | judgment | precautionary T24 judgment | reportable T24 clear-cut | volume_estimated, rate_estimated | 1/3 |
| JU-139 | judgment | precautionary T24 judgment | precautionary T3 judgment | lands | 3/3 |
| JU-147 | judgment | reportable T3 judgment | reportable T3 clear-cut | volume_m3, lands, point:substance | 3/3 |
| JU-142 | judgment | reportable T3 judgment | reportable T3 clear-cut | volume_m3, lands | 2/3 |
| JU-143 | judgment | reportable T3 judgment | reportable T24 clear-cut | lands, point:substance | 2/3 |
| CL-020 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | fire_or_explosion | 1/3 |
