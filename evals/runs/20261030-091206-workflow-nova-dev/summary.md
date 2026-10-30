# Eval run 20261030-091206-workflow-nova-dev

Arm `workflow-nova`, splits ['dev'], 30 cases. Cost $0.0054 ($0.00018/case); latency p50 0.8 s, p95 1.2 s.

## Targets

| Target | Value | Limit | Met |
|---|---|---|---|
| missed_reports | 1 | ≤ 0 | **no** |
| late_deadlines | 1 | ≤ 0 | **no** |
| deadline_correct [proposed] | 0.800 | ≥ 0.95 | **no** |
| over_notify [proposed] | 0.000 | ≤ 0.3 | yes |
| missing_recall [proposed] | 1.000 | ≥ 0.9 | yes |
| extraction_accuracy [proposed] | 0.917 | ≥ 0.95 | **no** |
| latency_p95_s [proposed] | 1.162 | ≤ 300 | yes |

## Metrics

- **status**: 25/30 = 83.3% (95% CI 66%–93%)
- **missed_reports**: 1/28 = 3.6% (95% CI 1%–18%)
- **late_deadlines**: 1/12 = 8.3% (95% CI 1%–35%)
- **deadline_correct**: 24/30 = 80.0% (95% CI 63%–90%)
- **over_notify**: 0/2 = 0.0% (95% CI 0%–66%)
- **route**: 25/30 = 83.3% (95% CI 66%–93%)
- **incident_types**: 21/30 = 70.0% (95% CI 52%–83%)
- **missing_recall**: 15/15 = 100.0% (95% CI 80%–100%)
- **extraction_accuracy**: 452/493 = 91.7% (95% CI 89%–94%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 30/30 = 100.0% (95% CI 89%–100%) |
| discovered_at | 24/30 = 80.0% (95% CI 63%–90%) |
| env_effect | 26/30 = 86.7% (95% CI 70%–95%) |
| fire_linked_to_pipeline | 2/2 = 100.0% (95% CI 34%–100%) |
| fire_or_explosion | 30/30 = 100.0% (95% CI 89%–100%) |
| lands | 18/23 = 78.3% (95% CI 58%–90%) |
| limit_kpa | 30/30 = 100.0% (95% CI 89%–100%) |
| other_beyond_design | 27/30 = 90.0% (95% CI 74%–97%) |
| planned_venting | 23/23 = 100.0% (95% CI 86%–100%) |
| point:serious_injury | 0/1 = 0.0% (95% CI 0%–79%) |
| point:substance | 0/3 = 0.0% (95% CI 0%–56%) |
| point:volume_m3 | 1/1 = 100.0% (95% CI 21%–100%) |
| pressure_kpa | 30/30 = 100.0% (95% CI 89%–100%) |
| rate_estimated | 3/4 = 75.0% (95% CI 30%–95%) |
| rate_kg_s | 21/23 = 91.3% (95% CI 73%–98%) |
| release | 27/30 = 90.0% (95% CI 74%–97%) |
| rupture | 26/30 = 86.7% (95% CI 70%–95%) |
| serious_injury | 28/29 = 96.6% (95% CI 83%–99%) |
| substance | 20/20 = 100.0% (95% CI 84%–100%) |
| through_pipe_body_or_weld | 23/23 = 100.0% (95% CI 86%–100%) |
| toxic_plume | 30/30 = 100.0% (95% CI 89%–100%) |
| volume_estimated | 16/19 = 84.2% (95% CI 62%–94%) |
| volume_m3 | 17/22 = 77.3% (95% CI 57%–90%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 16 | 14/16 = 87.5% (95% CI 64%–97%) | 13/16 = 81.2% (95% CI 57%–93%) |
| judgment | 12 | 9/12 = 75.0% (95% CI 47%–91%) | 9/12 = 75.0% (95% CI 47%–91%) |
| not-reportable | 2 | 2/2 = 100.0% (95% CI 34%–100%) | 2/2 = 100.0% (95% CI 34%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 17 | 15/17 = 88.2% (95% CI 66%–97%) | 14/17 = 82.4% (95% CI 59%–94%) |
| mistral | 13 | 10/13 = 76.9% (95% CI 50%–92%) | 10/13 = 76.9% (95% CI 50%–92%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 30 | 25/30 = 83.3% (95% CI 66%–93%) | 24/30 = 80.0% (95% CI 63%–90%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 18 | 16/18 = 88.9% (95% CI 67%–97%) | 15/18 = 83.3% (95% CI 61%–94%) |
| proposed | 12 | 9/12 = 75.0% (95% CI 47%–91%) | 9/12 = 75.0% (95% CI 47%–91%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 30 | 25/30 = 83.3% (95% CI 66%–93%) | 24/30 = 80.0% (95% CI 63%–90%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields |
|---|---|---|---|---|
| CL-012 | clear-cut | precautionary T24 clear-cut | precautionary T3 clear-cut | discovered_at, rupture |
| CL-023 | clear-cut | reportable T24 clear-cut | precautionary T3 clear-cut | release |
| CL-046 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | other_beyond_design |
| JU-100 | judgment | precautionary T3 judgment | precautionary T3 clear-cut | release, other_beyond_design, point:serious_injury |
| JU-111 | judgment | precautionary T24 judgment | reportable T3 clear-cut | rupture, other_beyond_design |
| JU-124 | judgment | precautionary T24 judgment | reportable T3 clear-cut | volume_estimated, rate_estimated, rupture |
| JU-142 | judgment | precautionary T3 judgment | precautionary T3 clear-cut | volume_m3, lands, point:substance |
| JU-147 | judgment | precautionary T3 judgment | reportable T24 clear-cut | lands, point:substance |
