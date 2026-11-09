# Eval run 20261030-074330-workflow-nova-dev

Arm `workflow-nova`, splits ['dev'], 30 cases. Cost $0.0055 ($0.00018/case); latency p50 0.9 s, p95 1.2 s.

## Targets

| Target | Value | Limit | Met |
|---|---|---|---|
| missed_reports | 9 | ≤ 0 | **no** |
| late_deadlines | 4 | ≤ 0 | **no** |
| deadline_correct [proposed] | 0.500 | ≥ 0.95 | **no** |
| over_notify [proposed] | 0.000 | ≤ 0.3 | yes |
| missing_recall [proposed] | 0.222 | ≥ 0.9 | **no** |
| extraction_accuracy [proposed] | 0.859 | ≥ 0.95 | **no** |
| latency_p95_s [proposed] | 1.218 | ≤ 300 | yes |

## Metrics

- **status**: 16/30 = 53.3% (95% CI 36%–70%)
- **missed_reports**: 9/28 = 32.1% (95% CI 18%–51%)
- **late_deadlines**: 4/12 = 33.3% (95% CI 14%–61%)
- **deadline_correct**: 15/30 = 50.0% (95% CI 33%–67%)
- **over_notify**: 0/2 = 0.0% (95% CI 0%–66%)
- **route**: 23/30 = 76.7% (95% CI 59%–88%)
- **incident_types**: 16/30 = 53.3% (95% CI 36%–70%)
- **missing_recall**: 2/9 = 22.2% (95% CI 6%–55%)
- **extraction_accuracy**: 420/489 = 85.9% (95% CI 83%–89%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 30/30 = 100.0% (95% CI 89%–100%) |
| discovered_at | 22/30 = 73.3% (95% CI 56%–86%) |
| env_effect | 26/30 = 86.7% (95% CI 70%–95%) |
| fire_linked_to_pipeline | 2/2 = 100.0% (95% CI 34%–100%) |
| fire_or_explosion | 30/30 = 100.0% (95% CI 89%–100%) |
| lands | 20/23 = 87.0% (95% CI 68%–95%) |
| limit_kpa | 29/30 = 96.7% (95% CI 83%–99%) |
| other_beyond_design | 27/30 = 90.0% (95% CI 74%–97%) |
| planned_venting | 23/23 = 100.0% (95% CI 86%–100%) |
| point:serious_injury | 0/1 = 0.0% (95% CI 0%–79%) |
| point:substance | 0/3 = 0.0% (95% CI 0%–56%) |
| point:volume_m3 | 1/1 = 100.0% (95% CI 21%–100%) |
| pressure_kpa | 28/30 = 93.3% (95% CI 79%–98%) |
| rate_kg_s | 21/23 = 91.3% (95% CI 73%–98%) |
| release | 22/30 = 73.3% (95% CI 56%–86%) |
| rupture | 15/30 = 50.0% (95% CI 33%–67%) |
| serious_injury | 28/29 = 96.6% (95% CI 83%–99%) |
| substance | 20/20 = 100.0% (95% CI 84%–100%) |
| through_pipe_body_or_weld | 15/23 = 65.2% (95% CI 45%–81%) |
| toxic_plume | 29/30 = 96.7% (95% CI 83%–99%) |
| volume_estimated | 16/19 = 84.2% (95% CI 62%–94%) |
| volume_m3 | 16/22 = 72.7% (95% CI 52%–87%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 16 | 4/16 = 25.0% (95% CI 10%–49%) | 7/16 = 43.8% (95% CI 23%–67%) |
| judgment | 12 | 10/12 = 83.3% (95% CI 55%–95%) | 6/12 = 50.0% (95% CI 25%–75%) |
| not-reportable | 2 | 2/2 = 100.0% (95% CI 34%–100%) | 2/2 = 100.0% (95% CI 34%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 17 | 13/17 = 76.5% (95% CI 53%–90%) | 10/17 = 58.8% (95% CI 36%–78%) |
| mistral | 13 | 3/13 = 23.1% (95% CI 8%–50%) | 5/13 = 38.5% (95% CI 18%–64%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 30 | 16/30 = 53.3% (95% CI 36%–70%) | 15/30 = 50.0% (95% CI 33%–67%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 18 | 6/18 = 33.3% (95% CI 16%–56%) | 9/18 = 50.0% (95% CI 29%–71%) |
| proposed | 12 | 10/12 = 83.3% (95% CI 55%–95%) | 6/12 = 50.0% (95% CI 25%–75%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| False | 2 | 0/2 = 0.0% (95% CI 0%–66%) | 1/2 = 50.0% (95% CI 9%–91%) |
| True | 28 | 16/28 = 57.1% (95% CI 39%–73%) | 14/28 = 50.0% (95% CI 33%–67%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields |
|---|---|---|---|---|
| CL-007 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | rate_kg_s, through_pipe_body_or_weld, lands, rupture |
| CL-010 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | pressure_kpa, limit_kpa, other_beyond_design |
| CL-012 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | release, volume_m3, through_pipe_body_or_weld |
| CL-018 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | discovered_at, env_effect, volume_m3, lands, rupture |
| CL-023 | clear-cut | reportable T24 clear-cut | precautionary T3 clear-cut | env_effect, release, rupture |
| CL-030 | clear-cut | precautionary T3 clear-cut | not reportable None clear-cut | discovered_at, release, volume_m3 |
| CL-034 | clear-cut | precautionary T24 clear-cut | not reportable None clear-cut | release, volume_m3, through_pipe_body_or_weld |
| CL-039 | clear-cut | precautionary T3 clear-cut | not reportable None clear-cut | discovered_at, release, volume_m3, volume_estimated |
| CL-043 | clear-cut | precautionary T3 clear-cut | not reportable None clear-cut | release, volume_estimated |
| CL-046 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | other_beyond_design |
| CL-051 | clear-cut | reportable T3 clear-cut | precautionary T3 clear-cut |  |
| CL-057 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | discovered_at, release, volume_m3, lands, rupture |
| JU-100 | judgment | precautionary T3 judgment | not reportable None clear-cut | point:serious_injury |
| JU-110 | judgment | precautionary T24 judgment | precautionary T3 judgment | rupture |
| JU-111 | judgment | precautionary T24 judgment | reportable T3 clear-cut | rupture, other_beyond_design |
| JU-124 | judgment | precautionary T24 judgment | precautionary T3 clear-cut | volume_estimated, rupture |
| JU-127 | judgment | precautionary T24 judgment | precautionary T3 clear-cut | through_pipe_body_or_weld, rupture |
| JU-139 | judgment | precautionary T24 judgment | precautionary T3 judgment | through_pipe_body_or_weld, rupture |
| JU-142 | judgment | precautionary T3 judgment | precautionary T3 clear-cut | rupture, point:substance |
| JU-143 | judgment | precautionary T3 judgment | precautionary T3 clear-cut | through_pipe_body_or_weld, rupture, pressure_kpa, point:substance |
| JU-147 | judgment | precautionary T3 judgment | precautionary T3 clear-cut | discovered_at, rupture, point:substance |
