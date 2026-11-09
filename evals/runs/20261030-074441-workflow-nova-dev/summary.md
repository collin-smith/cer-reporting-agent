# Eval run 20261030-074441-workflow-nova-dev

Arm `workflow-nova`, splits ['dev'], 30 cases. Cost $0.0054 ($0.00018/case); latency p50 0.8 s, p95 1.2 s.

## Targets

| Target | Value | Limit | Met |
|---|---|---|---|
| missed_reports | 4 | ≤ 0 | **no** |
| late_deadlines | 2 | ≤ 0 | **no** |
| deadline_correct [proposed] | 0.733 | ≥ 0.95 | **no** |
| over_notify [proposed] | 0.000 | ≤ 0.3 | yes |
| missing_recall [proposed] | 0.667 | ≥ 0.9 | **no** |
| extraction_accuracy [proposed] | 0.900 | ≥ 0.95 | **no** |
| latency_p95_s [proposed] | 1.223 | ≤ 300 | yes |

## Metrics

- **status**: 17/30 = 56.7% (95% CI 39%–73%)
- **missed_reports**: 4/28 = 14.3% (95% CI 6%–31%)
- **late_deadlines**: 2/12 = 16.7% (95% CI 5%–45%)
- **deadline_correct**: 22/30 = 73.3% (95% CI 56%–86%)
- **over_notify**: 0/2 = 0.0% (95% CI 0%–66%)
- **route**: 24/30 = 80.0% (95% CI 63%–90%)
- **incident_types**: 17/30 = 56.7% (95% CI 39%–73%)
- **missing_recall**: 6/9 = 66.7% (95% CI 35%–88%)
- **extraction_accuracy**: 440/489 = 90.0% (95% CI 87%–92%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 30/30 = 100.0% (95% CI 89%–100%) |
| discovered_at | 19/30 = 63.3% (95% CI 46%–78%) |
| env_effect | 24/30 = 80.0% (95% CI 63%–90%) |
| fire_linked_to_pipeline | 2/2 = 100.0% (95% CI 34%–100%) |
| fire_or_explosion | 30/30 = 100.0% (95% CI 89%–100%) |
| lands | 21/23 = 91.3% (95% CI 73%–98%) |
| limit_kpa | 28/30 = 93.3% (95% CI 79%–98%) |
| other_beyond_design | 25/30 = 83.3% (95% CI 66%–93%) |
| planned_venting | 23/23 = 100.0% (95% CI 86%–100%) |
| point:serious_injury | 1/1 = 100.0% (95% CI 21%–100%) |
| point:substance | 0/3 = 0.0% (95% CI 0%–56%) |
| point:volume_m3 | 1/1 = 100.0% (95% CI 21%–100%) |
| pressure_kpa | 27/30 = 90.0% (95% CI 74%–97%) |
| rate_kg_s | 22/23 = 95.7% (95% CI 79%–99%) |
| release | 25/30 = 83.3% (95% CI 66%–93%) |
| rupture | 26/30 = 86.7% (95% CI 70%–95%) |
| serious_injury | 28/29 = 96.6% (95% CI 83%–99%) |
| substance | 20/20 = 100.0% (95% CI 84%–100%) |
| through_pipe_body_or_weld | 23/23 = 100.0% (95% CI 86%–100%) |
| toxic_plume | 30/30 = 100.0% (95% CI 89%–100%) |
| volume_estimated | 18/19 = 94.7% (95% CI 75%–99%) |
| volume_m3 | 17/22 = 77.3% (95% CI 57%–90%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 16 | 8/16 = 50.0% (95% CI 28%–72%) | 11/16 = 68.8% (95% CI 44%–86%) |
| judgment | 12 | 7/12 = 58.3% (95% CI 32%–81%) | 9/12 = 75.0% (95% CI 47%–91%) |
| not-reportable | 2 | 2/2 = 100.0% (95% CI 34%–100%) | 2/2 = 100.0% (95% CI 34%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 17 | 12/17 = 70.6% (95% CI 47%–87%) | 15/17 = 88.2% (95% CI 66%–97%) |
| mistral | 13 | 5/13 = 38.5% (95% CI 18%–64%) | 7/13 = 53.8% (95% CI 29%–77%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 30 | 17/30 = 56.7% (95% CI 39%–73%) | 22/30 = 73.3% (95% CI 56%–86%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 18 | 10/18 = 55.6% (95% CI 34%–75%) | 13/18 = 72.2% (95% CI 49%–88%) |
| proposed | 12 | 7/12 = 58.3% (95% CI 32%–81%) | 9/12 = 75.0% (95% CI 47%–91%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| False | 2 | 0/2 = 0.0% (95% CI 0%–66%) | 2/2 = 100.0% (95% CI 34%–100%) |
| True | 28 | 17/28 = 60.7% (95% CI 42%–76%) | 20/28 = 71.4% (95% CI 53%–85%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields |
|---|---|---|---|---|
| CL-010 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | discovered_at, pressure_kpa, limit_kpa, other_beyond_design |
| CL-012 | clear-cut | reportable T24 clear-cut | precautionary T24 clear-cut | discovered_at, volume_m3 |
| CL-020 | clear-cut | reportable T24 clear-cut | precautionary T3 clear-cut | discovered_at, env_effect, release |
| CL-023 | clear-cut | reportable T24 clear-cut | precautionary T3 clear-cut | env_effect, release |
| CL-030 | clear-cut | precautionary T3 clear-cut | not reportable None clear-cut | discovered_at, release, volume_m3 |
| CL-034 | clear-cut | precautionary T24 clear-cut | reportable T24 clear-cut | discovered_at, volume_m3, other_beyond_design |
| CL-039 | clear-cut | precautionary T3 clear-cut | not reportable None clear-cut | discovered_at, release, volume_m3, volume_estimated |
| CL-051 | clear-cut | reportable T3 clear-cut | precautionary T3 clear-cut |  |
| JU-111 | judgment | precautionary T24 judgment | reportable T3 clear-cut | rupture, other_beyond_design |
| JU-124 | judgment | precautionary T24 judgment | reportable T3 clear-cut | rupture |
| JU-127 | judgment | precautionary T24 judgment | not reportable None clear-cut |  |
| JU-139 | judgment | precautionary T24 judgment | precautionary T24 clear-cut | env_effect |
| JU-142 | judgment | precautionary T3 judgment | reportable T3 clear-cut | rupture, point:substance |
| JU-147 | judgment | precautionary T3 judgment | reportable T3 clear-cut | discovered_at, rupture, point:substance |
