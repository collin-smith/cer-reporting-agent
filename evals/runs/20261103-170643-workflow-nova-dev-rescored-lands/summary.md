# Eval run 20261103-170643-workflow-nova-dev-rescored-lands

Arm `workflow-nova`, splits ['dev'], 30 cases × 3 passes = 90 results. Cost $0.0180 ($0.00020/case); latency p50 0.8 s, p95 1.1 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 3 | ≤ 0 | **no** | 0/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct | 0.911 | ≥ 0.95 | **no** | 0/3 |
| over_notify | 0.167 | ≤ 0.3 | **no** | 2/3 |
| missing_recall | 0.933 | ≥ 0.9 | yes | 3/3 |
| extraction_accuracy | 0.978 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s | 1.139 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.900 | 0.933 | 0.933 | 0.900 | 0.933 |
| deadline_correct | 0.867 | 0.933 | 0.933 | 0.867 | 0.933 |
| route | 0.933 | 0.900 | 0.933 | 0.900 | 0.933 |
| missed_reports | 1 | 1 | 1 | 1 | 1 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | 0.500 | 0.000 | 0.000 | 0.000 | 0.500 |
| missing_recall | 0.933 | 0.933 | 0.933 | 0.933 | 0.933 |
| extraction_accuracy | 0.974 | 0.978 | 0.982 | 0.974 | 0.982 |

## Unstable cases (3): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| JU-100 | judgment | precautionary T3 judgment / precautionary T3 clear-cut / precautionary T3 judgment | 2/3 |
| JU-111 | judgment | precautionary T3 judgment / precautionary T24 judgment / precautionary T24 judgment | 2/3 |
| NO-090 | not-reportable | precautionary T24 clear-cut / not reportable None clear-cut / not reportable None clear-cut | 2/3 |

## Metrics

- **status**: 83/90 = 92.2% (95% CI 85%–96%)
- **missed_reports**: 3/84 = 3.6% (95% CI 1%–10%)
- **late_deadlines**: 0/36 = 0.0% (95% CI 0%–10%)
- **deadline_correct**: 82/90 = 91.1% (95% CI 83%–95%)
- **over_notify**: 1/6 = 16.7% (95% CI 3%–56%)
- **route**: 83/90 = 92.2% (95% CI 85%–96%)
- **incident_types**: 76/90 = 84.4% (95% CI 76%–91%)
- **missing_recall**: 42/45 = 93.3% (95% CI 82%–98%)
- **extraction_accuracy**: 1449/1482 = 97.8% (95% CI 97%–98%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 87/90 = 96.7% (95% CI 91%–99%) |
| discovered_at | 89/90 = 98.9% (95% CI 94%–100%) |
| env_effect | 90/90 = 100.0% (95% CI 96%–100%) |
| fire_linked_to_pipeline | 6/6 = 100.0% (95% CI 61%–100%) |
| fire_or_explosion | 90/90 = 100.0% (95% CI 96%–100%) |
| lands | 63/69 = 91.3% (95% CI 82%–96%) |
| limit_kpa | 90/90 = 100.0% (95% CI 96%–100%) |
| other_beyond_design | 87/90 = 96.7% (95% CI 91%–99%) |
| planned_venting | 69/69 = 100.0% (95% CI 95%–100%) |
| point:env_effect | 0/3 = 0.0% (95% CI 0%–56%) |
| point:serious_injury | 3/3 = 100.0% (95% CI 44%–100%) |
| point:substance | 9/9 = 100.0% (95% CI 70%–100%) |
| point:volume_m3 | 3/3 = 100.0% (95% CI 44%–100%) |
| pressure_kpa | 90/90 = 100.0% (95% CI 96%–100%) |
| rate_estimated | 9/12 = 75.0% (95% CI 47%–91%) |
| rate_kg_s | 69/69 = 100.0% (95% CI 95%–100%) |
| release | 83/90 = 92.2% (95% CI 85%–96%) |
| rupture | 90/90 = 100.0% (95% CI 96%–100%) |
| serious_injury | 84/87 = 96.6% (95% CI 90%–99%) |
| substance | 59/60 = 98.3% (95% CI 91%–100%) |
| through_pipe_body_or_weld | 69/69 = 100.0% (95% CI 95%–100%) |
| toxic_plume | 90/90 = 100.0% (95% CI 96%–100%) |
| volume_estimated | 57/57 = 100.0% (95% CI 94%–100%) |
| volume_m3 | 63/66 = 95.5% (95% CI 87%–98%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 48 | 45/48 = 93.8% (95% CI 83%–98%) | 42/48 = 87.5% (95% CI 75%–94%) |
| judgment | 36 | 33/36 = 91.7% (95% CI 78%–97%) | 35/36 = 97.2% (95% CI 86%–100%) |
| not-reportable | 6 | 5/6 = 83.3% (95% CI 44%–97%) | 5/6 = 83.3% (95% CI 44%–97%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 51 | 50/51 = 98.0% (95% CI 90%–100%) | 47/51 = 92.2% (95% CI 81%–97%) |
| mistral | 39 | 33/39 = 84.6% (95% CI 70%–93%) | 35/39 = 89.7% (95% CI 76%–96%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 90 | 83/90 = 92.2% (95% CI 85%–96%) | 82/90 = 91.1% (95% CI 83%–95%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 54 | 50/54 = 92.6% (95% CI 82%–97%) | 47/54 = 87.0% (95% CI 76%–94%) |
| reviewed | 36 | 33/36 = 91.7% (95% CI 78%–97%) | 35/36 = 97.2% (95% CI 86%–100%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 90 | 83/90 = 92.2% (95% CI 85%–96%) | 82/90 = 91.1% (95% CI 83%–95%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-023 | clear-cut | reportable T24 clear-cut | reportable T3 clear-cut | release | 3/3 |
| CL-034 | clear-cut | precautionary T24 clear-cut | precautionary T24 judgment | volume_m3 | 3/3 |
| CL-046 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | other_beyond_design | 3/3 |
| NO-090 | not-reportable | not reportable None clear-cut | precautionary T24 clear-cut | discovered_at, substance | 1/3 |
| JU-111 | judgment | precautionary T24 judgment | precautionary T3 judgment | lands | 1/3 |
| JU-124 | judgment | precautionary T24 judgment | reportable T24 clear-cut | rate_estimated | 3/3 |
| JU-100 | judgment | precautionary T3 judgment | precautionary T3 clear-cut | release | 1/3 |
