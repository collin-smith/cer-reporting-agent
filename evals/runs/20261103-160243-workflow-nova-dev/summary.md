# Eval run 20261103-160243-workflow-nova-dev

Arm `workflow-nova`, splits ['dev'], 30 cases × 3 passes = 90 results. Cost $0.0167 ($0.00019/case); latency p50 0.8 s, p95 1.0 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 6 | ≤ 0 | **no** | 0/3 |
| late_deadlines | 3 | ≤ 0 | **no** | 0/3 |
| deadline_correct [proposed] | 0.822 | ≥ 0.95 | **no** | 0/3 |
| over_notify [proposed] | 0.000 | ≤ 0.3 | yes | 3/3 |
| missing_recall [proposed] | 0.933 | ≥ 0.9 | yes | 3/3 |
| extraction_accuracy [proposed] | 0.952 | ≥ 0.95 | **no** | 2/3 |
| latency_p95_s [proposed] | 1.031 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.900 | 0.867 | 0.867 | 0.867 | 0.900 |
| deadline_correct | 0.800 | 0.833 | 0.833 | 0.800 | 0.833 |
| route | 0.833 | 0.833 | 0.833 | 0.833 | 0.833 |
| missed_reports | 2 | 2 | 2 | 2 | 2 |
| late_deadlines | 1 | 1 | 1 | 1 | 1 |
| over_notify | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| missing_recall | 0.933 | 0.933 | 0.933 | 0.933 | 0.933 |
| extraction_accuracy | 0.949 | 0.951 | 0.955 | 0.949 | 0.955 |

## Unstable cases (1): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| JU-124 | judgment | precautionary T3 clear-cut / reportable T24 clear-cut / reportable T24 clear-cut | 0/3 |

## Metrics

- **status**: 79/90 = 87.8% (95% CI 79%–93%)
- **missed_reports**: 6/84 = 7.1% (95% CI 3%–15%)
- **late_deadlines**: 3/36 = 8.3% (95% CI 3%–22%)
- **deadline_correct**: 74/90 = 82.2% (95% CI 73%–89%)
- **over_notify**: 0/6 = 0.0% (95% CI 0%–39%)
- **route**: 75/90 = 83.3% (95% CI 74%–90%)
- **incident_types**: 66/90 = 73.3% (95% CI 63%–81%)
- **missing_recall**: 42/45 = 93.3% (95% CI 82%–98%)
- **extraction_accuracy**: 1411/1482 = 95.2% (95% CI 94%–96%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 90/90 = 100.0% (95% CI 96%–100%) |
| discovered_at | 90/90 = 100.0% (95% CI 96%–100%) |
| env_effect | 84/90 = 93.3% (95% CI 86%–97%) |
| fire_linked_to_pipeline | 6/6 = 100.0% (95% CI 61%–100%) |
| fire_or_explosion | 90/90 = 100.0% (95% CI 96%–100%) |
| lands | 60/69 = 87.0% (95% CI 77%–93%) |
| limit_kpa | 90/90 = 100.0% (95% CI 96%–100%) |
| other_beyond_design | 84/90 = 93.3% (95% CI 86%–97%) |
| planned_venting | 69/69 = 100.0% (95% CI 95%–100%) |
| point:env_effect | 0/3 = 0.0% (95% CI 0%–56%) |
| point:serious_injury | 3/3 = 100.0% (95% CI 44%–100%) |
| point:substance | 3/9 = 33.3% (95% CI 12%–65%) |
| point:volume_m3 | 3/3 = 100.0% (95% CI 44%–100%) |
| pressure_kpa | 90/90 = 100.0% (95% CI 96%–100%) |
| rate_estimated | 6/12 = 50.0% (95% CI 25%–75%) |
| rate_kg_s | 68/69 = 98.6% (95% CI 92%–100%) |
| release | 84/90 = 93.3% (95% CI 86%–97%) |
| rupture | 90/90 = 100.0% (95% CI 96%–100%) |
| serious_injury | 81/87 = 93.1% (95% CI 86%–97%) |
| substance | 57/60 = 95.0% (95% CI 86%–98%) |
| through_pipe_body_or_weld | 69/69 = 100.0% (95% CI 95%–100%) |
| toxic_plume | 90/90 = 100.0% (95% CI 96%–100%) |
| volume_estimated | 48/57 = 84.2% (95% CI 73%–91%) |
| volume_m3 | 56/66 = 84.8% (95% CI 74%–92%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 48 | 45/48 = 93.8% (95% CI 83%–98%) | 39/48 = 81.2% (95% CI 68%–90%) |
| judgment | 36 | 28/36 = 77.8% (95% CI 62%–88%) | 29/36 = 80.6% (95% CI 65%–90%) |
| not-reportable | 6 | 6/6 = 100.0% (95% CI 61%–100%) | 6/6 = 100.0% (95% CI 61%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 51 | 48/51 = 94.1% (95% CI 84%–98%) | 45/51 = 88.2% (95% CI 77%–94%) |
| mistral | 39 | 31/39 = 79.5% (95% CI 64%–89%) | 29/39 = 74.4% (95% CI 59%–85%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 90 | 79/90 = 87.8% (95% CI 79%–93%) | 74/90 = 82.2% (95% CI 73%–89%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 54 | 51/54 = 94.4% (95% CI 85%–98%) | 45/54 = 83.3% (95% CI 71%–91%) |
| reviewed | 36 | 28/36 = 77.8% (95% CI 62%–88%) | 29/36 = 80.6% (95% CI 65%–90%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 90 | 79/90 = 87.8% (95% CI 79%–93%) | 74/90 = 82.2% (95% CI 73%–89%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-023 | clear-cut | reportable T24 clear-cut | reportable T3 clear-cut | release | 3/3 |
| CL-030 | clear-cut | precautionary T3 clear-cut | precautionary T24 clear-cut | substance | 3/3 |
| CL-046 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | other_beyond_design | 3/3 |
| JU-111 | judgment | precautionary T24 judgment | reportable T3 clear-cut | volume_m3, lands, other_beyond_design | 3/3 |
| JU-124 | judgment | precautionary T24 judgment | precautionary T3 clear-cut | volume_m3, volume_estimated, rate_kg_s, rate_estimated | 3/3 |
| JU-127 | judgment | precautionary T24 judgment | not reportable None clear-cut | rate_estimated | 3/3 |
| JU-142 | judgment | reportable T3 judgment | reportable T3 clear-cut | volume_m3, lands, point:substance | 3/3 |
| JU-147 | judgment | reportable T3 judgment | reportable T3 clear-cut | lands, point:substance | 3/3 |
