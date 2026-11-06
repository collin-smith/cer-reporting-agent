# Eval run 20261106-160529-oracle-dev-test-heldout

Arm `oracle`, splits ['dev', 'test', 'heldout'], 166 cases. Cost $0.0000 ($0.00000/case); latency p50 0.0 s, p95 0.0 s.

## Targets

| Target | Value | Limit | Met |
|---|---|---|---|
| missed_reports | 0 | ≤ 0 | yes |
| late_deadlines | 0 | ≤ 0 | yes |
| deadline_correct | 1.000 | ≥ 0.95 | yes |
| over_notify | 0.000 | ≤ 0.3 | yes |
| missing_recall | 1.000 | ≥ 0.9 | yes |
| extraction_accuracy | 1.000 | ≥ 0.95 | yes |
| latency_p95_s | 0.000 | ≤ 300 | yes |

## Metrics

- **status**: 166/166 = 100.0% (95% CI 98%–100%)
- **missed_reports**: 0/147 = 0.0% (95% CI 0%–3%)
- **late_deadlines**: 0/71 = 0.0% (95% CI 0%–5%)
- **deadline_correct**: 166/166 = 100.0% (95% CI 98%–100%)
- **over_notify**: 0/19 = 0.0% (95% CI 0%–17%)
- **route**: 166/166 = 100.0% (95% CI 98%–100%)
- **incident_types**: 166/166 = 100.0% (95% CI 98%–100%)
- **missing_recall**: 57/57 = 100.0% (95% CI 94%–100%)
- **extraction_accuracy**: 2569/2569 = 100.0% (95% CI 100%–100%)
- **injection_flagged**: 0/15 = 0.0% (95% CI 0%–20%)

## Extraction by field

| Field | Correct |
|---|---|
| death | 166/166 = 100.0% (95% CI 98%–100%) |
| discovered_at | 166/166 = 100.0% (95% CI 98%–100%) |
| env_effect | 162/162 = 100.0% (95% CI 98%–100%) |
| fire_linked_to_pipeline | 27/27 = 100.0% (95% CI 88%–100%) |
| fire_or_explosion | 166/166 = 100.0% (95% CI 98%–100%) |
| lands | 94/94 = 100.0% (95% CI 96%–100%) |
| limit_kpa | 166/166 = 100.0% (95% CI 98%–100%) |
| other_beyond_design | 166/166 = 100.0% (95% CI 98%–100%) |
| planned_venting | 102/102 = 100.0% (95% CI 96%–100%) |
| point:env_effect | 4/4 = 100.0% (95% CI 51%–100%) |
| point:fire_linked_to_pipeline | 3/3 = 100.0% (95% CI 44%–100%) |
| point:lands | 8/8 = 100.0% (95% CI 68%–100%) |
| point:serious_injury | 4/4 = 100.0% (95% CI 51%–100%) |
| point:substance | 6/6 = 100.0% (95% CI 61%–100%) |
| point:volume_m3 | 6/6 = 100.0% (95% CI 61%–100%) |
| pressure_kpa | 166/166 = 100.0% (95% CI 98%–100%) |
| rate_estimated | 12/12 = 100.0% (95% CI 76%–100%) |
| rate_kg_s | 102/102 = 100.0% (95% CI 96%–100%) |
| release | 166/166 = 100.0% (95% CI 98%–100%) |
| rupture | 166/166 = 100.0% (95% CI 98%–100%) |
| serious_injury | 162/162 = 100.0% (95% CI 98%–100%) |
| substance | 96/96 = 100.0% (95% CI 96%–100%) |
| through_pipe_body_or_weld | 102/102 = 100.0% (95% CI 96%–100%) |
| toxic_plume | 166/166 = 100.0% (95% CI 98%–100%) |
| volume_estimated | 89/89 = 100.0% (95% CI 96%–100%) |
| volume_m3 | 96/96 = 100.0% (95% CI 96%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| adversarial | 15 | 15/15 = 100.0% (95% CI 80%–100%) | 15/15 = 100.0% (95% CI 80%–100%) |
| clear-cut | 75 | 75/75 = 100.0% (95% CI 95%–100%) | 75/75 = 100.0% (95% CI 95%–100%) |
| judgment | 57 | 57/57 = 100.0% (95% CI 94%–100%) | 57/57 = 100.0% (95% CI 94%–100%) |
| not-reportable | 19 | 19/19 = 100.0% (95% CI 83%–100%) | 19/19 = 100.0% (95% CI 83%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 85 | 85/85 = 100.0% (95% CI 96%–100%) | 85/85 = 100.0% (95% CI 96%–100%) |
| mistral | 81 | 81/81 = 100.0% (95% CI 95%–100%) | 81/81 = 100.0% (95% CI 95%–100%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 30 | 30/30 = 100.0% (95% CI 89%–100%) | 30/30 = 100.0% (95% CI 89%–100%) |
| heldout | 56 | 56/56 = 100.0% (95% CI 94%–100%) | 56/56 = 100.0% (95% CI 94%–100%) |
| test | 80 | 80/80 = 100.0% (95% CI 95%–100%) | 80/80 = 100.0% (95% CI 95%–100%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 105 | 105/105 = 100.0% (95% CI 96%–100%) | 105/105 = 100.0% (95% CI 96%–100%) |
| reviewed | 61 | 61/61 = 100.0% (95% CI 94%–100%) | 61/61 = 100.0% (95% CI 94%–100%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 166 | 166/166 = 100.0% (95% CI 98%–100%) | 166/166 = 100.0% (95% CI 98%–100%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 166 | 166/166 = 100.0% (95% CI 98%–100%) | 166/166 = 100.0% (95% CI 98%–100%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields |
|---|---|---|---|---|
