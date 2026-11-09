# Eval run 20261030-074052-workflow-nova-dev

Arm `workflow-nova`, splits ['dev'], 30 cases. Cost $0.0049 ($0.00016/case); latency p50 0.7 s, p95 1.1 s.

## Targets

| Target | Value | Limit | Met |
|---|---|---|---|
| missed_reports | 6 | ≤ 0 | **no** |
| late_deadlines | 4 | ≤ 0 | **no** |
| deadline_correct [proposed] | 0.400 | ≥ 0.95 | **no** |
| over_notify [proposed] | 0.000 | ≤ 0.3 | yes |
| missing_recall [proposed] | 0.333 | ≥ 0.9 | **no** |
| extraction_accuracy [proposed] | 0.855 | ≥ 0.95 | **no** |
| latency_p95_s [proposed] | 1.055 | ≤ 300 | yes |

## Metrics

- **status**: 14/30 = 46.7% (95% CI 30%–64%)
- **missed_reports**: 6/28 = 21.4% (95% CI 10%–40%)
- **late_deadlines**: 4/12 = 33.3% (95% CI 14%–61%)
- **deadline_correct**: 12/30 = 40.0% (95% CI 25%–58%)
- **over_notify**: 0/2 = 0.0% (95% CI 0%–66%)
- **route**: 21/30 = 70.0% (95% CI 52%–83%)
- **incident_types**: 10/30 = 33.3% (95% CI 19%–51%)
- **missing_recall**: 3/9 = 33.3% (95% CI 12%–65%)
- **extraction_accuracy**: 419/490 = 85.5% (95% CI 82%–88%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 30/30 = 100.0% (95% CI 89%–100%) |
| discovered_at | 22/30 = 73.3% (95% CI 56%–86%) |
| env_effect | 25/30 = 83.3% (95% CI 66%–93%) |
| fire_linked_to_pipeline | 1/2 = 50.0% (95% CI 9%–91%) |
| fire_or_explosion | 30/30 = 100.0% (95% CI 89%–100%) |
| lands | 19/23 = 82.6% (95% CI 63%–93%) |
| limit_kpa | 27/30 = 90.0% (95% CI 74%–97%) |
| other_beyond_design | 22/30 = 73.3% (95% CI 56%–86%) |
| planned_venting | 23/23 = 100.0% (95% CI 86%–100%) |
| point:lands | 0/1 = 0.0% (95% CI 0%–79%) |
| point:serious_injury | 0/1 = 0.0% (95% CI 0%–79%) |
| point:substance | 0/3 = 0.0% (95% CI 0%–56%) |
| point:volume_m3 | 1/1 = 100.0% (95% CI 21%–100%) |
| pressure_kpa | 27/30 = 90.0% (95% CI 74%–97%) |
| rate_kg_s | 23/23 = 100.0% (95% CI 86%–100%) |
| release | 23/30 = 76.7% (95% CI 59%–88%) |
| rupture | 19/30 = 63.3% (95% CI 46%–78%) |
| serious_injury | 29/29 = 100.0% (95% CI 88%–100%) |
| substance | 16/20 = 80.0% (95% CI 58%–92%) |
| through_pipe_body_or_weld | 22/23 = 95.7% (95% CI 79%–99%) |
| toxic_plume | 29/30 = 96.7% (95% CI 83%–99%) |
| volume_estimated | 15/19 = 78.9% (95% CI 57%–91%) |
| volume_m3 | 16/22 = 72.7% (95% CI 52%–87%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 16 | 4/16 = 25.0% (95% CI 10%–49%) | 6/16 = 37.5% (95% CI 18%–61%) |
| judgment | 12 | 8/12 = 66.7% (95% CI 39%–86%) | 4/12 = 33.3% (95% CI 14%–61%) |
| not-reportable | 2 | 2/2 = 100.0% (95% CI 34%–100%) | 2/2 = 100.0% (95% CI 34%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 17 | 10/17 = 58.8% (95% CI 36%–78%) | 7/17 = 41.2% (95% CI 22%–64%) |
| mistral | 13 | 4/13 = 30.8% (95% CI 13%–58%) | 5/13 = 38.5% (95% CI 18%–64%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 30 | 14/30 = 46.7% (95% CI 30%–64%) | 12/30 = 40.0% (95% CI 25%–58%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 18 | 6/18 = 33.3% (95% CI 16%–56%) | 8/18 = 44.4% (95% CI 25%–66%) |
| proposed | 12 | 8/12 = 66.7% (95% CI 39%–86%) | 4/12 = 33.3% (95% CI 14%–61%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| False | 2 | 0/2 = 0.0% (95% CI 0%–66%) | 1/2 = 50.0% (95% CI 9%–91%) |
| True | 28 | 14/28 = 50.0% (95% CI 33%–67%) | 11/28 = 39.3% (95% CI 24%–58%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields |
|---|---|---|---|---|
| CL-007 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | lands, other_beyond_design |
| CL-010 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | pressure_kpa, limit_kpa, other_beyond_design |
| CL-012 | clear-cut | reportable T24 clear-cut | precautionary T3 clear-cut | discovered_at, volume_m3, rupture |
| CL-018 | clear-cut | precautionary T3 clear-cut | reportable T24 clear-cut | discovered_at, volume_m3, lands, other_beyond_design |
| CL-020 | clear-cut | reportable T24 clear-cut | precautionary T3 clear-cut | env_effect, fire_linked_to_pipeline, release |
| CL-023 | clear-cut | reportable T24 clear-cut | precautionary T3 clear-cut | env_effect, release, rupture, other_beyond_design |
| CL-030 | clear-cut | precautionary T3 clear-cut | not reportable None clear-cut | release, volume_m3 |
| CL-034 | clear-cut | precautionary T24 clear-cut | not reportable None clear-cut | volume_m3, rupture |
| CL-039 | clear-cut | precautionary T3 clear-cut | not reportable None clear-cut | discovered_at, release, volume_m3, volume_estimated |
| CL-051 | clear-cut | reportable T3 clear-cut | precautionary T3 clear-cut | env_effect, lands, other_beyond_design |
| CL-055 | clear-cut | reportable T24 clear-cut | precautionary T3 clear-cut | release |
| CL-057 | clear-cut | reportable T24 clear-cut | precautionary T3 clear-cut | discovered_at, volume_m3, volume_estimated, lands, rupture |
| JU-097 | judgment | precautionary T24 judgment | precautionary T3 judgment | discovered_at, rupture |
| JU-100 | judgment | precautionary T3 judgment | precautionary T3 clear-cut | env_effect, release, rupture, pressure_kpa, limit_kpa, other_beyond_design, point:serious_injury, point:lands |
| JU-110 | judgment | precautionary T24 judgment | precautionary T3 clear-cut | substance, volume_estimated |
| JU-111 | judgment | precautionary T24 judgment | reportable T3 clear-cut | substance, volume_estimated, rupture, other_beyond_design |
| JU-114 | judgment | precautionary T24 judgment | precautionary T3 clear-cut | substance |
| JU-124 | judgment | precautionary T24 judgment | precautionary T3 clear-cut | substance, rupture |
| JU-126 | judgment | precautionary T24 judgment | not reportable None clear-cut | discovered_at |
| JU-127 | judgment | precautionary T24 judgment | not reportable None clear-cut |  |
| JU-143 | judgment | precautionary T3 judgment | precautionary T3 clear-cut | env_effect, through_pipe_body_or_weld, rupture, toxic_plume, point:substance |
| JU-147 | judgment | precautionary T3 judgment | reportable T24 clear-cut | discovered_at, other_beyond_design, point:substance |
