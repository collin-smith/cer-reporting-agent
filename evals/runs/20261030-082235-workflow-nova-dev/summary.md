# Eval run 20261030-082235-workflow-nova-dev

Arm `workflow-nova`, splits ['dev'], 30 cases. Cost $0.0054 ($0.00018/case); latency p50 0.8 s, p95 1.2 s.

## Targets

| Target | Value | Limit | Met |
|---|---|---|---|
| missed_reports | 3 | ≤ 0 | **no** |
| late_deadlines | 3 | ≤ 0 | **no** |
| deadline_correct [proposed] | 0.700 | ≥ 0.95 | **no** |
| over_notify [proposed] | 0.000 | ≤ 0.3 | yes |
| missing_recall [proposed] | 0.889 | ≥ 0.9 | **no** |
| extraction_accuracy [proposed] | 0.905 | ≥ 0.95 | **no** |
| latency_p95_s [proposed] | 1.179 | ≤ 300 | yes |

## Metrics

- **status**: 19/30 = 63.3% (95% CI 46%–78%)
- **missed_reports**: 3/28 = 10.7% (95% CI 4%–27%)
- **late_deadlines**: 3/12 = 25.0% (95% CI 9%–53%)
- **deadline_correct**: 21/30 = 70.0% (95% CI 52%–83%)
- **over_notify**: 0/2 = 0.0% (95% CI 0%–66%)
- **route**: 24/30 = 80.0% (95% CI 63%–90%)
- **incident_types**: 19/30 = 63.3% (95% CI 46%–78%)
- **missing_recall**: 8/9 = 88.9% (95% CI 56%–98%)
- **extraction_accuracy**: 446/493 = 90.5% (95% CI 88%–93%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 29/30 = 96.7% (95% CI 83%–99%) |
| discovered_at | 24/30 = 80.0% (95% CI 63%–90%) |
| env_effect | 25/30 = 83.3% (95% CI 66%–93%) |
| fire_linked_to_pipeline | 2/2 = 100.0% (95% CI 34%–100%) |
| fire_or_explosion | 30/30 = 100.0% (95% CI 89%–100%) |
| lands | 20/23 = 87.0% (95% CI 68%–95%) |
| limit_kpa | 29/30 = 96.7% (95% CI 83%–99%) |
| other_beyond_design | 26/30 = 86.7% (95% CI 70%–95%) |
| planned_venting | 23/23 = 100.0% (95% CI 86%–100%) |
| point:serious_injury | 0/1 = 0.0% (95% CI 0%–79%) |
| point:substance | 0/3 = 0.0% (95% CI 0%–56%) |
| point:volume_m3 | 1/1 = 100.0% (95% CI 21%–100%) |
| pressure_kpa | 29/30 = 96.7% (95% CI 83%–99%) |
| rate_estimated | 2/4 = 50.0% (95% CI 15%–85%) |
| rate_kg_s | 21/23 = 91.3% (95% CI 73%–98%) |
| release | 25/30 = 83.3% (95% CI 66%–93%) |
| rupture | 28/30 = 93.3% (95% CI 79%–98%) |
| serious_injury | 27/29 = 93.1% (95% CI 78%–98%) |
| substance | 20/20 = 100.0% (95% CI 84%–100%) |
| through_pipe_body_or_weld | 23/23 = 100.0% (95% CI 86%–100%) |
| toxic_plume | 30/30 = 100.0% (95% CI 89%–100%) |
| volume_estimated | 16/19 = 84.2% (95% CI 62%–94%) |
| volume_m3 | 16/22 = 72.7% (95% CI 52%–87%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 16 | 10/16 = 62.5% (95% CI 39%–82%) | 11/16 = 68.8% (95% CI 44%–86%) |
| judgment | 12 | 7/12 = 58.3% (95% CI 32%–81%) | 8/12 = 66.7% (95% CI 39%–86%) |
| not-reportable | 2 | 2/2 = 100.0% (95% CI 34%–100%) | 2/2 = 100.0% (95% CI 34%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 17 | 12/17 = 70.6% (95% CI 47%–87%) | 12/17 = 70.6% (95% CI 47%–87%) |
| mistral | 13 | 7/13 = 53.8% (95% CI 29%–77%) | 9/13 = 69.2% (95% CI 42%–87%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 30 | 19/30 = 63.3% (95% CI 46%–78%) | 21/30 = 70.0% (95% CI 52%–83%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 18 | 12/18 = 66.7% (95% CI 44%–84%) | 13/18 = 72.2% (95% CI 49%–88%) |
| proposed | 12 | 7/12 = 58.3% (95% CI 32%–81%) | 8/12 = 66.7% (95% CI 39%–86%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| False | 2 | 0/2 = 0.0% (95% CI 0%–66%) | 1/2 = 50.0% (95% CI 9%–91%) |
| True | 28 | 19/28 = 67.9% (95% CI 49%–82%) | 20/28 = 71.4% (95% CI 53%–85%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields |
|---|---|---|---|---|
| CL-010 | clear-cut | reportable T24 clear-cut | precautionary T3 clear-cut | release, pressure_kpa, limit_kpa, other_beyond_design |
| CL-012 | clear-cut | reportable T24 clear-cut | precautionary T3 clear-cut | volume_m3 |
| CL-023 | clear-cut | reportable T24 clear-cut | precautionary T3 clear-cut | death, serious_injury, env_effect, release |
| CL-030 | clear-cut | precautionary T3 clear-cut | not reportable None clear-cut | release, volume_m3 |
| CL-046 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | other_beyond_design |
| CL-051 | clear-cut | reportable T3 clear-cut | precautionary T3 clear-cut | volume_m3 |
| JU-100 | judgment | precautionary T3 judgment | precautionary T3 clear-cut | release, other_beyond_design, point:serious_injury |
| JU-111 | judgment | precautionary T24 judgment | reportable T3 clear-cut | volume_m3, rupture, other_beyond_design |
| JU-124 | judgment | precautionary T24 judgment | reportable T24 clear-cut | volume_estimated, rate_estimated |
| JU-127 | judgment | precautionary T24 judgment | not reportable None clear-cut | rate_estimated |
| JU-142 | judgment | precautionary T3 judgment | reportable T24 clear-cut | point:substance |
| JU-147 | judgment | precautionary T3 judgment | reportable T24 clear-cut | discovered_at, point:substance |
