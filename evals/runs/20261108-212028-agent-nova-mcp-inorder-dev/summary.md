# Eval run 20261108-212028-agent-nova-mcp-inorder-dev

Arm `agent-nova-mcp-inorder`, splits ['dev'], 33 cases. Cost $0.0266 ($0.00081/case); latency p50 4.5 s, p95 10.8 s.

## Targets

| Target | Value | Limit | Met |
|---|---|---|---|
| missed_reports | 1 | ≤ 0 | **no** |
| late_deadlines | 0 | ≤ 0 | yes |
| deadline_correct | 0.939 | ≥ 0.95 | **no** |
| over_notify | 0.000 | ≤ 0.3 | yes |
| missing_recall | 0.933 | ≥ 0.9 | yes |
| extraction_accuracy | 0.985 | ≥ 0.95 | yes |
| latency_p95_s | 10.821 | ≤ 300 | yes |

## Metrics

- **status**: 31/33 = 93.9% (95% CI 80%–98%)
- **missed_reports**: 1/31 = 3.2% (95% CI 1%–16%)
- **late_deadlines**: 0/12 = 0.0% (95% CI 0%–24%)
- **deadline_correct**: 31/33 = 93.9% (95% CI 80%–98%)
- **over_notify**: 0/2 = 0.0% (95% CI 0%–66%)
- **route**: 29/33 = 87.9% (95% CI 73%–95%)
- **incident_types**: 30/33 = 90.9% (95% CI 76%–97%)
- **missing_recall**: 14/15 = 93.3% (95% CI 70%–99%)
- **extraction_accuracy**: 520/528 = 98.5% (95% CI 97%–99%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 33/33 = 100.0% (95% CI 90%–100%) |
| discovered_at | 33/33 = 100.0% (95% CI 90%–100%) |
| env_effect | 32/33 = 97.0% (95% CI 85%–99%) |
| fire_linked_to_pipeline | 2/2 = 100.0% (95% CI 34%–100%) |
| fire_or_explosion | 33/33 = 100.0% (95% CI 90%–100%) |
| lands | 21/23 = 91.3% (95% CI 73%–98%) |
| limit_kpa | 33/33 = 100.0% (95% CI 90%–100%) |
| other_beyond_design | 33/33 = 100.0% (95% CI 90%–100%) |
| planned_venting | 23/23 = 100.0% (95% CI 86%–100%) |
| point:env_effect | 0/2 = 0.0% (95% CI 0%–66%) |
| point:serious_injury | 1/1 = 100.0% (95% CI 21%–100%) |
| point:substance | 3/3 = 100.0% (95% CI 44%–100%) |
| point:volume_m3 | 1/1 = 100.0% (95% CI 21%–100%) |
| pressure_kpa | 33/33 = 100.0% (95% CI 90%–100%) |
| rate_estimated | 2/4 = 50.0% (95% CI 15%–85%) |
| rate_kg_s | 23/23 = 100.0% (95% CI 86%–100%) |
| release | 33/33 = 100.0% (95% CI 90%–100%) |
| rupture | 33/33 = 100.0% (95% CI 90%–100%) |
| serious_injury | 32/32 = 100.0% (95% CI 89%–100%) |
| substance | 20/20 = 100.0% (95% CI 84%–100%) |
| through_pipe_body_or_weld | 23/23 = 100.0% (95% CI 86%–100%) |
| toxic_plume | 33/33 = 100.0% (95% CI 90%–100%) |
| volume_estimated | 19/19 = 100.0% (95% CI 83%–100%) |
| volume_m3 | 21/22 = 95.5% (95% CI 78%–99%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 19 | 19/19 = 100.0% (95% CI 83%–100%) | 18/19 = 94.7% (95% CI 75%–99%) |
| judgment | 12 | 10/12 = 83.3% (95% CI 55%–95%) | 11/12 = 91.7% (95% CI 65%–99%) |
| not-reportable | 2 | 2/2 = 100.0% (95% CI 34%–100%) | 2/2 = 100.0% (95% CI 34%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 19 | 18/19 = 94.7% (95% CI 75%–99%) | 18/19 = 94.7% (95% CI 75%–99%) |
| mistral | 14 | 13/14 = 92.9% (95% CI 69%–99%) | 13/14 = 92.9% (95% CI 69%–99%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 33 | 31/33 = 93.9% (95% CI 80%–98%) | 31/33 = 93.9% (95% CI 80%–98%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 21 | 21/21 = 100.0% (95% CI 85%–100%) | 20/21 = 95.2% (95% CI 77%–99%) |
| reviewed | 12 | 10/12 = 83.3% (95% CI 55%–95%) | 11/12 = 91.7% (95% CI 65%–99%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 33 | 31/33 = 93.9% (95% CI 80%–98%) | 31/33 = 93.9% (95% CI 80%–98%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 33 | 31/33 = 93.9% (95% CI 80%–98%) | 31/33 = 93.9% (95% CI 80%–98%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields |
|---|---|---|---|---|
| CL-034 | clear-cut | precautionary T24 clear-cut | precautionary T3 judgment | volume_m3, lands |
| CL-055 | clear-cut | reportable T24 clear-cut | reportable T24 judgment |  |
| JU-124 | judgment | precautionary T24 judgment | reportable T24 clear-cut | rate_estimated |
| JU-127 | judgment | precautionary T24 judgment | not reportable None clear-cut | rate_estimated |
