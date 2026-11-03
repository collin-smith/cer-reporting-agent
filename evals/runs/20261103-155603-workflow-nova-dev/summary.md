# Eval run 20261103-155603-workflow-nova-dev

Arm `workflow-nova`, splits ['dev'], 30 cases × 3 passes = 90 results. Cost $0.0165 ($0.00018/case); latency p50 0.9 s, p95 1.2 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 7 | ≤ 0 | **no** | 0/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct [proposed] | 0.767 | ≥ 0.95 | **no** | 0/3 |
| over_notify [proposed] | 0.333 | ≤ 0.3 | **no** | 1/3 |
| missing_recall [proposed] | 0.978 | ≥ 0.9 | yes | 3/3 |
| extraction_accuracy [proposed] | 0.958 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s [proposed] | 1.249 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.867 | 0.867 | 0.833 | 0.833 | 0.867 |
| deadline_correct | 0.767 | 0.767 | 0.767 | 0.767 | 0.767 |
| route | 0.900 | 0.900 | 0.867 | 0.867 | 0.900 |
| missed_reports | 3 | 2 | 2 | 2 | 3 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | 0.000 | 0.500 | 0.500 | 0.000 | 0.500 |
| missing_recall | 0.933 | 1.000 | 1.000 | 0.933 | 1.000 |
| extraction_accuracy | 0.964 | 0.958 | 0.954 | 0.954 | 0.964 |

## Unstable cases (3): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| CL-034 | clear-cut | not reportable None clear-cut / precautionary T24 clear-cut / precautionary T24 clear-cut | 2/3 |
| JU-111 | judgment | precautionary T3 judgment / precautionary T3 judgment / reportable T3 clear-cut | 0/3 |
| NO-090 | not-reportable | not reportable None clear-cut / precautionary T24 clear-cut / precautionary T24 clear-cut | 1/3 |

## Metrics

- **status**: 77/90 = 85.6% (95% CI 77%–91%)
- **missed_reports**: 7/84 = 8.3% (95% CI 4%–16%)
- **late_deadlines**: 0/36 = 0.0% (95% CI 0%–10%)
- **deadline_correct**: 69/90 = 76.7% (95% CI 67%–84%)
- **over_notify**: 2/6 = 33.3% (95% CI 10%–70%)
- **route**: 80/90 = 88.9% (95% CI 81%–94%)
- **incident_types**: 69/90 = 76.7% (95% CI 67%–84%)
- **missing_recall**: 44/45 = 97.8% (95% CI 88%–100%)
- **extraction_accuracy**: 1422/1484 = 95.8% (95% CI 95%–97%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 90/90 = 100.0% (95% CI 96%–100%) |
| discovered_at | 90/90 = 100.0% (95% CI 96%–100%) |
| env_effect | 85/90 = 94.4% (95% CI 88%–98%) |
| fire_linked_to_pipeline | 6/6 = 100.0% (95% CI 61%–100%) |
| fire_or_explosion | 90/90 = 100.0% (95% CI 96%–100%) |
| lands | 65/69 = 94.2% (95% CI 86%–98%) |
| limit_kpa | 90/90 = 100.0% (95% CI 96%–100%) |
| other_beyond_design | 86/90 = 95.6% (95% CI 89%–98%) |
| planned_venting | 69/69 = 100.0% (95% CI 95%–100%) |
| point:env_effect | 0/5 = 0.0% (95% CI 0%–43%) |
| point:serious_injury | 3/3 = 100.0% (95% CI 44%–100%) |
| point:substance | 6/9 = 66.7% (95% CI 35%–88%) |
| point:volume_m3 | 2/3 = 66.7% (95% CI 21%–94%) |
| pressure_kpa | 90/90 = 100.0% (95% CI 96%–100%) |
| rate_estimated | 6/12 = 50.0% (95% CI 25%–75%) |
| rate_kg_s | 69/69 = 100.0% (95% CI 95%–100%) |
| release | 84/90 = 93.3% (95% CI 86%–97%) |
| rupture | 77/90 = 85.6% (95% CI 77%–91%) |
| serious_injury | 84/87 = 96.6% (95% CI 90%–99%) |
| substance | 58/60 = 96.7% (95% CI 89%–99%) |
| through_pipe_body_or_weld | 69/69 = 100.0% (95% CI 95%–100%) |
| toxic_plume | 90/90 = 100.0% (95% CI 96%–100%) |
| volume_estimated | 48/57 = 84.2% (95% CI 73%–91%) |
| volume_m3 | 65/66 = 98.5% (95% CI 92%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 48 | 44/48 = 91.7% (95% CI 80%–97%) | 38/48 = 79.2% (95% CI 66%–88%) |
| judgment | 36 | 29/36 = 80.6% (95% CI 65%–90%) | 27/36 = 75.0% (95% CI 59%–86%) |
| not-reportable | 6 | 4/6 = 66.7% (95% CI 30%–90%) | 4/6 = 66.7% (95% CI 30%–90%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 51 | 46/51 = 90.2% (95% CI 79%–96%) | 40/51 = 78.4% (95% CI 65%–88%) |
| mistral | 39 | 31/39 = 79.5% (95% CI 64%–89%) | 29/39 = 74.4% (95% CI 59%–85%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 90 | 77/90 = 85.6% (95% CI 77%–91%) | 69/90 = 76.7% (95% CI 67%–84%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 54 | 48/54 = 88.9% (95% CI 78%–95%) | 42/54 = 77.8% (95% CI 65%–87%) |
| reviewed | 36 | 29/36 = 80.6% (95% CI 65%–90%) | 27/36 = 75.0% (95% CI 59%–86%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 90 | 77/90 = 85.6% (95% CI 77%–91%) | 69/90 = 76.7% (95% CI 67%–84%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-012 | clear-cut | precautionary T24 clear-cut | precautionary T3 clear-cut | rupture | 3/3 |
| CL-023 | clear-cut | reportable T24 clear-cut | reportable T3 clear-cut | release | 3/3 |
| CL-034 | clear-cut | precautionary T24 clear-cut | not reportable None clear-cut | volume_m3 | 1/3 |
| CL-046 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | other_beyond_design | 3/3 |
| JU-111 | judgment | precautionary T24 judgment | precautionary T3 judgment | rupture | 3/3 |
| JU-124 | judgment | precautionary T24 judgment | reportable T3 clear-cut | volume_estimated, rate_estimated, rupture | 3/3 |
| JU-127 | judgment | precautionary T24 judgment | not reportable None clear-cut | rate_estimated | 3/3 |
| JU-147 | judgment | reportable T3 judgment | reportable T3 clear-cut | point:substance | 3/3 |
| NO-090 | not-reportable | not reportable None clear-cut | precautionary T24 clear-cut | substance | 2/3 |
