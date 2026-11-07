# Eval run 20261107-150949-supervisor-nova-dev

Arm `supervisor-nova`, splits ['dev'], 2 cases. Cost $0.0041 ($0.00204/case); latency p50 18.2 s, p95 19.9 s.

## Targets

| Target | Value | Limit | Met |
|---|---|---|---|
| missed_reports | 0 | ≤ 0 | yes |
| late_deadlines | 0 | ≤ 0 | yes |
| deadline_correct | 1.000 | ≥ 0.95 | yes |
| over_notify | n/a | ≤ 0.3 | **no** |
| missing_recall | n/a | ≥ 0.9 | **no** |
| extraction_accuracy | 0.906 | ≥ 0.95 | **no** |
| latency_p95_s | 19.943 | ≤ 300 | yes |

## Metrics

- **status**: 2/2 = 100.0% (95% CI 34%–100%)
- **missed_reports**: 0/2 = 0.0% (95% CI 0%–66%)
- **late_deadlines**: 0/2 = 0.0% (95% CI 0%–66%)
- **deadline_correct**: 2/2 = 100.0% (95% CI 34%–100%)
- **over_notify**: n/a
- **route**: 2/2 = 100.0% (95% CI 34%–100%)
- **incident_types**: 0/2 = 0.0% (95% CI 0%–66%)
- **missing_recall**: n/a
- **extraction_accuracy**: 29/32 = 90.6% (95% CI 76%–97%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 2/2 = 100.0% (95% CI 34%–100%) |
| discovered_at | 2/2 = 100.0% (95% CI 34%–100%) |
| env_effect | 1/2 = 50.0% (95% CI 9%–91%) |
| fire_linked_to_pipeline | 1/1 = 100.0% (95% CI 21%–100%) |
| fire_or_explosion | 2/2 = 100.0% (95% CI 34%–100%) |
| lands | 1/1 = 100.0% (95% CI 21%–100%) |
| limit_kpa | 2/2 = 100.0% (95% CI 34%–100%) |
| other_beyond_design | 2/2 = 100.0% (95% CI 34%–100%) |
| planned_venting | 1/1 = 100.0% (95% CI 21%–100%) |
| point:env_effect | 0/1 = 0.0% (95% CI 0%–79%) |
| point:serious_injury | 0/1 = 0.0% (95% CI 0%–79%) |
| point:substance | 1/1 = 100.0% (95% CI 21%–100%) |
| pressure_kpa | 2/2 = 100.0% (95% CI 34%–100%) |
| rate_kg_s | 1/1 = 100.0% (95% CI 21%–100%) |
| release | 2/2 = 100.0% (95% CI 34%–100%) |
| rupture | 2/2 = 100.0% (95% CI 34%–100%) |
| serious_injury | 2/2 = 100.0% (95% CI 34%–100%) |
| through_pipe_body_or_weld | 1/1 = 100.0% (95% CI 21%–100%) |
| toxic_plume | 2/2 = 100.0% (95% CI 34%–100%) |
| volume_estimated | 1/1 = 100.0% (95% CI 21%–100%) |
| volume_m3 | 1/1 = 100.0% (95% CI 21%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 1 | 1/1 = 100.0% (95% CI 21%–100%) | 1/1 = 100.0% (95% CI 21%–100%) |
| judgment | 1 | 1/1 = 100.0% (95% CI 21%–100%) | 1/1 = 100.0% (95% CI 21%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 1 | 1/1 = 100.0% (95% CI 21%–100%) | 1/1 = 100.0% (95% CI 21%–100%) |
| mistral | 1 | 1/1 = 100.0% (95% CI 21%–100%) | 1/1 = 100.0% (95% CI 21%–100%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 2 | 2/2 = 100.0% (95% CI 34%–100%) | 2/2 = 100.0% (95% CI 34%–100%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 1 | 1/1 = 100.0% (95% CI 21%–100%) | 1/1 = 100.0% (95% CI 21%–100%) |
| reviewed | 1 | 1/1 = 100.0% (95% CI 21%–100%) | 1/1 = 100.0% (95% CI 21%–100%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 2 | 2/2 = 100.0% (95% CI 34%–100%) | 2/2 = 100.0% (95% CI 34%–100%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 2 | 2/2 = 100.0% (95% CI 34%–100%) | 2/2 = 100.0% (95% CI 34%–100%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields |
|---|---|---|---|---|
