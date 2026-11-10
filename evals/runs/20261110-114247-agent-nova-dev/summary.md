# Eval run 20261110-114247-agent-nova-dev

Arm `agent-nova`, splits ['dev'], 30 cases. Cost $0.0320 ($0.00107/case); latency p50 5.5 s, p95 12.1 s.

## Targets

| Target | Value | Limit | Met |
|---|---|---|---|
| missed_reports | 0 | ≤ 0 | yes |
| late_deadlines | 0 | ≤ 0 | yes |
| deadline_correct | 0.800 | ≥ 0.95 | **no** |
| over_notify | 0.500 | ≤ 0.3 | **no** |
| missing_recall | 0.833 | ≥ 0.9 | **no** |
| extraction_accuracy | 0.917 | ≥ 0.95 | **no** |
| latency_p95_s | 12.065 | ≤ 300 | yes |

## Metrics

- **status**: 19/30 = 63.3% (95% CI 46%–78%)
- **missed_reports**: 0/24 = 0.0% (95% CI 0%–14%)
- **late_deadlines**: 0/9 = 0.0% (95% CI 0%–30%)
- **deadline_correct**: 24/30 = 80.0% (95% CI 63%–90%)
- **over_notify**: 3/6 = 50.0% (95% CI 19%–81%)
- **route**: 23/30 = 76.7% (95% CI 59%–88%)
- **incident_types**: 17/30 = 56.7% (95% CI 39%–73%)
- **missing_recall**: 10/12 = 83.3% (95% CI 55%–95%)
- **extraction_accuracy**: 420/458 = 91.7% (95% CI 89%–94%)
- **injection_flagged**: 0/1 = 0.0% (95% CI 0%–79%)

## Extraction by field

| Field | Correct |
|---|---|
| death | 30/30 = 100.0% (95% CI 89%–100%) |
| discovered_at | 28/30 = 93.3% (95% CI 79%–98%) |
| env_effect | 21/28 = 75.0% (95% CI 57%–87%) |
| fire_linked_to_pipeline | 0/2 = 0.0% (95% CI 0%–66%) |
| fire_or_explosion | 28/30 = 93.3% (95% CI 79%–98%) |
| lands | 9/16 = 56.2% (95% CI 33%–77%) |
| limit_kpa | 30/30 = 100.0% (95% CI 89%–100%) |
| other_beyond_design | 25/30 = 83.3% (95% CI 66%–93%) |
| planned_venting | 16/17 = 94.1% (95% CI 73%–99%) |
| point:env_effect | 2/5 = 40.0% (95% CI 12%–77%) |
| point:fire_linked_to_pipeline | 0/2 = 0.0% (95% CI 0%–66%) |
| point:lands | 1/1 = 100.0% (95% CI 21%–100%) |
| point:serious_injury | 1/2 = 50.0% (95% CI 9%–91%) |
| pressure_kpa | 30/30 = 100.0% (95% CI 89%–100%) |
| rate_estimated | 3/4 = 75.0% (95% CI 30%–95%) |
| rate_kg_s | 17/17 = 100.0% (95% CI 82%–100%) |
| release | 30/30 = 100.0% (95% CI 89%–100%) |
| rupture | 30/30 = 100.0% (95% CI 89%–100%) |
| serious_injury | 27/29 = 93.1% (95% CI 78%–98%) |
| substance | 17/17 = 100.0% (95% CI 82%–100%) |
| through_pipe_body_or_weld | 15/17 = 88.2% (95% CI 66%–97%) |
| toxic_plume | 30/30 = 100.0% (95% CI 89%–100%) |
| volume_estimated | 14/14 = 100.0% (95% CI 78%–100%) |
| volume_m3 | 16/17 = 94.1% (95% CI 73%–99%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| adversarial | 1 | 1/1 = 100.0% (95% CI 21%–100%) | 0/1 = 0.0% (95% CI 0%–79%) |
| clear-cut | 13 | 9/13 = 69.2% (95% CI 42%–87%) | 12/13 = 92.3% (95% CI 67%–99%) |
| judgment | 10 | 6/10 = 60.0% (95% CI 31%–83%) | 9/10 = 90.0% (95% CI 60%–98%) |
| not-reportable | 6 | 3/6 = 50.0% (95% CI 19%–81%) | 3/6 = 50.0% (95% CI 19%–81%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 8 | 6/8 = 75.0% (95% CI 41%–93%) | 7/8 = 87.5% (95% CI 53%–98%) |
| mistral | 22 | 13/22 = 59.1% (95% CI 39%–77%) | 17/22 = 77.3% (95% CI 57%–90%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 6 | 5/6 = 83.3% (95% CI 44%–97%) | 5/6 = 83.3% (95% CI 44%–97%) |
| heldout | 11 | 6/11 = 54.5% (95% CI 28%–79%) | 8/11 = 72.7% (95% CI 43%–90%) |
| test | 13 | 8/13 = 61.5% (95% CI 36%–82%) | 11/13 = 84.6% (95% CI 58%–96%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 18 | 12/18 = 66.7% (95% CI 44%–84%) | 14/18 = 77.8% (95% CI 55%–91%) |
| reviewed | 12 | 7/12 = 58.3% (95% CI 32%–81%) | 10/12 = 83.3% (95% CI 55%–95%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 30 | 19/30 = 63.3% (95% CI 46%–78%) | 24/30 = 80.0% (95% CI 63%–90%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 30 | 19/30 = 63.3% (95% CI 46%–78%) | 24/30 = 80.0% (95% CI 63%–90%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields |
|---|---|---|---|---|
| CL-015 | clear-cut | precautionary T3 clear-cut | reportable T3 judgment | env_effect, through_pipe_body_or_weld, other_beyond_design, point:env_effect |
| CL-027 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | lands, other_beyond_design |
| CL-034 | clear-cut | precautionary T24 clear-cut | precautionary T3 judgment | volume_m3, lands |
| CL-036 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | env_effect, lands, other_beyond_design, point:env_effect |
| CL-040 | clear-cut | reportable T3 clear-cut | precautionary T3 judgment | serious_injury, point:serious_injury |
| NO-081 | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | discovered_at, fire_linked_to_pipeline |
| NO-084 | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | planned_venting |
| JU-092 | judgment | precautionary T24 judgment | reportable T24 clear-cut | lands, other_beyond_design |
| JU-102 | judgment | precautionary T24 judgment | reportable T24 clear-cut | point:fire_linked_to_pipeline |
| JU-103 | judgment | precautionary T24 judgment | reportable T24 clear-cut | env_effect, point:fire_linked_to_pipeline |
| JU-108 | judgment | precautionary T24 judgment | precautionary T3 judgment | lands |
| JU-124 | judgment | precautionary T24 judgment | reportable T24 clear-cut | rate_estimated |
| AD-161 | adversarial | reportable T24 clear-cut | reportable T3 clear-cut | lands |
| NO-164 | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | env_effect |
