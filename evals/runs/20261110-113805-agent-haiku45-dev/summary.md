# Eval run 20261110-113805-agent-haiku45-dev

Arm `agent-haiku45`, splits ['dev'], 3 cases. Cost $0.0354 ($0.01180/case); latency p50 7.2 s, p95 14.8 s.

## Targets

| Target | Value | Limit | Met |
|---|---|---|---|
| missed_reports | 0 | ≤ 0 | yes |
| late_deadlines | 0 | ≤ 0 | yes |
| deadline_correct | 1.000 | ≥ 0.95 | yes |
| over_notify | 0.000 | ≤ 0.3 | yes |
| missing_recall | n/a | ≥ 0.9 | **no** |
| extraction_accuracy | 0.976 | ≥ 0.95 | yes |
| latency_p95_s | 14.765 | ≤ 300 | yes |

## Metrics

- **status**: 2/3 = 66.7% (95% CI 21%–94%)
- **missed_reports**: 0/2 = 0.0% (95% CI 0%–66%)
- **late_deadlines**: n/a
- **deadline_correct**: 3/3 = 100.0% (95% CI 44%–100%)
- **over_notify**: 0/1 = 0.0% (95% CI 0%–79%)
- **route**: 2/3 = 66.7% (95% CI 21%–94%)
- **incident_types**: 2/3 = 66.7% (95% CI 21%–94%)
- **missing_recall**: n/a
- **extraction_accuracy**: 40/41 = 97.6% (95% CI 87%–100%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 3/3 = 100.0% (95% CI 44%–100%) |
| discovered_at | 3/3 = 100.0% (95% CI 44%–100%) |
| env_effect | 2/2 = 100.0% (95% CI 34%–100%) |
| fire_linked_to_pipeline | 1/1 = 100.0% (95% CI 21%–100%) |
| fire_or_explosion | 3/3 = 100.0% (95% CI 44%–100%) |
| lands | 1/1 = 100.0% (95% CI 21%–100%) |
| limit_kpa | 3/3 = 100.0% (95% CI 44%–100%) |
| other_beyond_design | 2/3 = 66.7% (95% CI 21%–94%) |
| planned_venting | 1/1 = 100.0% (95% CI 21%–100%) |
| point:env_effect | 1/1 = 100.0% (95% CI 21%–100%) |
| pressure_kpa | 3/3 = 100.0% (95% CI 44%–100%) |
| rate_kg_s | 1/1 = 100.0% (95% CI 21%–100%) |
| release | 3/3 = 100.0% (95% CI 44%–100%) |
| rupture | 3/3 = 100.0% (95% CI 44%–100%) |
| serious_injury | 3/3 = 100.0% (95% CI 44%–100%) |
| substance | 1/1 = 100.0% (95% CI 21%–100%) |
| through_pipe_body_or_weld | 1/1 = 100.0% (95% CI 21%–100%) |
| toxic_plume | 3/3 = 100.0% (95% CI 44%–100%) |
| volume_estimated | 1/1 = 100.0% (95% CI 21%–100%) |
| volume_m3 | 1/1 = 100.0% (95% CI 21%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 1 | 1/1 = 100.0% (95% CI 21%–100%) | 1/1 = 100.0% (95% CI 21%–100%) |
| judgment | 1 | 0/1 = 0.0% (95% CI 0%–79%) | 1/1 = 100.0% (95% CI 21%–100%) |
| not-reportable | 1 | 1/1 = 100.0% (95% CI 21%–100%) | 1/1 = 100.0% (95% CI 21%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| mistral | 3 | 2/3 = 66.7% (95% CI 21%–94%) | 3/3 = 100.0% (95% CI 44%–100%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| heldout | 2 | 2/2 = 100.0% (95% CI 34%–100%) | 2/2 = 100.0% (95% CI 34%–100%) |
| test | 1 | 0/1 = 0.0% (95% CI 0%–79%) | 1/1 = 100.0% (95% CI 21%–100%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 2 | 2/2 = 100.0% (95% CI 34%–100%) | 2/2 = 100.0% (95% CI 34%–100%) |
| reviewed | 1 | 0/1 = 0.0% (95% CI 0%–79%) | 1/1 = 100.0% (95% CI 21%–100%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 3 | 2/3 = 66.7% (95% CI 21%–94%) | 3/3 = 100.0% (95% CI 44%–100%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 3 | 2/3 = 66.7% (95% CI 21%–94%) | 3/3 = 100.0% (95% CI 44%–100%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields |
|---|---|---|---|---|
| JU-092 | judgment | precautionary T24 judgment | reportable T24 clear-cut | other_beyond_design |
