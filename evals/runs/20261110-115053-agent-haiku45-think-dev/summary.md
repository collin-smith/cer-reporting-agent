# Eval run 20261110-115053-agent-haiku45-think-dev

Arm `agent-haiku45-think`, splits ['dev'], 30 cases. Cost $0.5898 ($0.01966/case); latency p50 13.2 s, p95 23.7 s.

## Targets

| Target | Value | Limit | Met |
|---|---|---|---|
| missed_reports | 0 | ≤ 0 | yes |
| late_deadlines | 0 | ≤ 0 | yes |
| deadline_correct | 0.900 | ≥ 0.95 | **no** |
| over_notify | 0.333 | ≤ 0.3 | **no** |
| missing_recall | 0.833 | ≥ 0.9 | **no** |
| extraction_accuracy | 0.932 | ≥ 0.95 | **no** |
| latency_p95_s | 23.658 | ≤ 300 | yes |

## Metrics

- **status**: 24/30 = 80.0% (95% CI 63%–90%)
- **missed_reports**: 0/24 = 0.0% (95% CI 0%–14%)
- **late_deadlines**: 0/9 = 0.0% (95% CI 0%–30%)
- **deadline_correct**: 27/30 = 90.0% (95% CI 74%–97%)
- **over_notify**: 2/6 = 33.3% (95% CI 10%–70%)
- **route**: 26/30 = 86.7% (95% CI 70%–95%)
- **incident_types**: 18/30 = 60.0% (95% CI 42%–75%)
- **missing_recall**: 10/12 = 83.3% (95% CI 55%–95%)
- **extraction_accuracy**: 424/455 = 93.2% (95% CI 90%–95%)
- **injection_flagged**: 1/1 = 100.0% (95% CI 21%–100%)

## Extraction by field

| Field | Correct |
|---|---|
| death | 30/30 = 100.0% (95% CI 89%–100%) |
| discovered_at | 28/30 = 93.3% (95% CI 79%–98%) |
| env_effect | 19/28 = 67.9% (95% CI 49%–82%) |
| fire_linked_to_pipeline | 2/2 = 100.0% (95% CI 34%–100%) |
| fire_or_explosion | 28/30 = 93.3% (95% CI 79%–98%) |
| lands | 12/16 = 75.0% (95% CI 51%–90%) |
| limit_kpa | 30/30 = 100.0% (95% CI 89%–100%) |
| other_beyond_design | 24/30 = 80.0% (95% CI 63%–90%) |
| planned_venting | 17/17 = 100.0% (95% CI 82%–100%) |
| point:env_effect | 2/3 = 66.7% (95% CI 21%–94%) |
| point:fire_linked_to_pipeline | 2/2 = 100.0% (95% CI 34%–100%) |
| point:lands | 0/1 = 0.0% (95% CI 0%–79%) |
| point:serious_injury | 1/1 = 100.0% (95% CI 21%–100%) |
| pressure_kpa | 30/30 = 100.0% (95% CI 89%–100%) |
| rate_estimated | 4/4 = 100.0% (95% CI 51%–100%) |
| rate_kg_s | 17/17 = 100.0% (95% CI 82%–100%) |
| release | 30/30 = 100.0% (95% CI 89%–100%) |
| rupture | 29/30 = 96.7% (95% CI 83%–99%) |
| serious_injury | 27/29 = 93.1% (95% CI 78%–98%) |
| substance | 17/17 = 100.0% (95% CI 82%–100%) |
| through_pipe_body_or_weld | 14/17 = 82.4% (95% CI 59%–94%) |
| toxic_plume | 30/30 = 100.0% (95% CI 89%–100%) |
| volume_estimated | 14/14 = 100.0% (95% CI 78%–100%) |
| volume_m3 | 17/17 = 100.0% (95% CI 82%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| adversarial | 1 | 1/1 = 100.0% (95% CI 21%–100%) | 0/1 = 0.0% (95% CI 0%–79%) |
| clear-cut | 13 | 11/13 = 84.6% (95% CI 58%–96%) | 13/13 = 100.0% (95% CI 77%–100%) |
| judgment | 10 | 8/10 = 80.0% (95% CI 49%–94%) | 10/10 = 100.0% (95% CI 72%–100%) |
| not-reportable | 6 | 4/6 = 66.7% (95% CI 30%–90%) | 4/6 = 66.7% (95% CI 30%–90%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 8 | 7/8 = 87.5% (95% CI 53%–98%) | 7/8 = 87.5% (95% CI 53%–98%) |
| mistral | 22 | 17/22 = 77.3% (95% CI 57%–90%) | 20/22 = 90.9% (95% CI 72%–97%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 6 | 5/6 = 83.3% (95% CI 44%–97%) | 6/6 = 100.0% (95% CI 61%–100%) |
| heldout | 11 | 10/11 = 90.9% (95% CI 62%–98%) | 9/11 = 81.8% (95% CI 52%–95%) |
| test | 13 | 9/13 = 69.2% (95% CI 42%–87%) | 12/13 = 92.3% (95% CI 67%–99%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 18 | 16/18 = 88.9% (95% CI 67%–97%) | 17/18 = 94.4% (95% CI 74%–99%) |
| reviewed | 12 | 8/12 = 66.7% (95% CI 39%–86%) | 10/12 = 83.3% (95% CI 55%–95%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 30 | 24/30 = 80.0% (95% CI 63%–90%) | 27/30 = 90.0% (95% CI 74%–97%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 30 | 24/30 = 80.0% (95% CI 63%–90%) | 27/30 = 90.0% (95% CI 74%–97%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields |
|---|---|---|---|---|
| CL-015 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | env_effect, through_pipe_body_or_weld, lands, other_beyond_design |
| CL-018 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | env_effect |
| CL-034 | clear-cut | precautionary T24 clear-cut | precautionary T24 judgment | through_pipe_body_or_weld |
| JU-092 | judgment | precautionary T24 judgment | reportable T24 clear-cut | other_beyond_design |
| JU-096 | judgment | precautionary T24 judgment | reportable T24 clear-cut | through_pipe_body_or_weld, other_beyond_design |
| JU-127 | judgment | precautionary T24 judgment | precautionary T24 clear-cut | fire_or_explosion |
| AD-161 | adversarial | reportable T24 clear-cut | reportable T3 clear-cut | env_effect, rupture |
| NO-163 | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | other_beyond_design |
| NO-164 | not-reportable | not reportable None clear-cut | reportable T3 clear-cut | serious_injury, other_beyond_design |
