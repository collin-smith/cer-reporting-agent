# Eval run 20261111-165445-agent-nova-agentcore-dev

Arm `agent-nova-agentcore`, splits ['dev'], 1 cases. Cost $0.0005 ($0.00049/case); latency p50 8.0 s, p95 8.0 s.

## Targets

| Target | Value | Limit | Met |
|---|---|---|---|
| missed_reports | 0 | ≤ 0 | yes |
| late_deadlines | 0 | ≤ 0 | yes |
| deadline_correct | 1.000 | ≥ 0.95 | yes |
| over_notify | n/a | ≤ 0.3 | **no** |
| missing_recall | n/a | ≥ 0.9 | **no** |
| extraction_accuracy | 1.000 | ≥ 0.95 | yes |
| latency_p95_s | 7.960 | ≤ 300 | yes |

## Metrics

- **status**: 1/1 = 100.0% (95% CI 21%–100%)
- **missed_reports**: 0/1 = 0.0% (95% CI 0%–79%)
- **late_deadlines**: n/a
- **deadline_correct**: 1/1 = 100.0% (95% CI 21%–100%)
- **over_notify**: n/a
- **route**: 1/1 = 100.0% (95% CI 21%–100%)
- **incident_types**: 1/1 = 100.0% (95% CI 21%–100%)
- **missing_recall**: n/a
- **extraction_accuracy**: 11/11 = 100.0% (95% CI 74%–100%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 1/1 = 100.0% (95% CI 21%–100%) |
| discovered_at | 1/1 = 100.0% (95% CI 21%–100%) |
| env_effect | 1/1 = 100.0% (95% CI 21%–100%) |
| fire_or_explosion | 1/1 = 100.0% (95% CI 21%–100%) |
| limit_kpa | 1/1 = 100.0% (95% CI 21%–100%) |
| other_beyond_design | 1/1 = 100.0% (95% CI 21%–100%) |
| pressure_kpa | 1/1 = 100.0% (95% CI 21%–100%) |
| release | 1/1 = 100.0% (95% CI 21%–100%) |
| rupture | 1/1 = 100.0% (95% CI 21%–100%) |
| serious_injury | 1/1 = 100.0% (95% CI 21%–100%) |
| toxic_plume | 1/1 = 100.0% (95% CI 21%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 1 | 1/1 = 100.0% (95% CI 21%–100%) | 1/1 = 100.0% (95% CI 21%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 1 | 1/1 = 100.0% (95% CI 21%–100%) | 1/1 = 100.0% (95% CI 21%–100%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| test | 1 | 1/1 = 100.0% (95% CI 21%–100%) | 1/1 = 100.0% (95% CI 21%–100%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 1 | 1/1 = 100.0% (95% CI 21%–100%) | 1/1 = 100.0% (95% CI 21%–100%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 1 | 1/1 = 100.0% (95% CI 21%–100%) | 1/1 = 100.0% (95% CI 21%–100%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 1 | 1/1 = 100.0% (95% CI 21%–100%) | 1/1 = 100.0% (95% CI 21%–100%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields |
|---|---|---|---|---|
