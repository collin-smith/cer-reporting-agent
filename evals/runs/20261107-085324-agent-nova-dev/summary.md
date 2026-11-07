# Eval run 20261107-085324-agent-nova-dev

Arm `agent-nova`, splits ['dev'], 2 cases. Cost $0.0015 ($0.00074/case); latency p50 16.9 s, p95 18.3 s.

## Targets

| Target | Value | Limit | Met |
|---|---|---|---|
| missed_reports | 0 | ≤ 0 | yes |
| late_deadlines | 0 | ≤ 0 | yes |
| deadline_correct | 1.000 | ≥ 0.95 | yes |
| over_notify | n/a | ≤ 0.3 | **no** |
| missing_recall | n/a | ≥ 0.9 | **no** |
| extraction_accuracy | 1.000 | ≥ 0.95 | yes |
| latency_p95_s | 18.300 | ≤ 300 | yes |

## Metrics

- **status**: 2/2 = 100.0% (95% CI 34%–100%)
- **missed_reports**: 0/2 = 0.0% (95% CI 0%–66%)
- **late_deadlines**: 0/1 = 0.0% (95% CI 0%–79%)
- **deadline_correct**: 2/2 = 100.0% (95% CI 34%–100%)
- **over_notify**: n/a
- **route**: 2/2 = 100.0% (95% CI 34%–100%)
- **incident_types**: 2/2 = 100.0% (95% CI 34%–100%)
- **missing_recall**: n/a
- **extraction_accuracy**: 29/29 = 100.0% (95% CI 88%–100%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 2/2 = 100.0% (95% CI 34%–100%) |
| discovered_at | 2/2 = 100.0% (95% CI 34%–100%) |
| env_effect | 2/2 = 100.0% (95% CI 34%–100%) |
| fire_or_explosion | 2/2 = 100.0% (95% CI 34%–100%) |
| lands | 1/1 = 100.0% (95% CI 21%–100%) |
| limit_kpa | 2/2 = 100.0% (95% CI 34%–100%) |
| other_beyond_design | 2/2 = 100.0% (95% CI 34%–100%) |
| planned_venting | 1/1 = 100.0% (95% CI 21%–100%) |
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
| mistral | 2 | 2/2 = 100.0% (95% CI 34%–100%) | 2/2 = 100.0% (95% CI 34%–100%) |

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

## Stability under formatting

Each report also run as `noblank`, `wrap72` (same words, different layout); a flip is a different status, deadline or route from the same case in the same pass. 1 variants identical after normalising were not run. Cost including variants $0.0032.

| Variant | Flips | Right → wrong | Wrong → right | Missed | Late | Status |
|---|---|---|---|---|---|---|
| all | 0/3 = 0.0% (95% CI 0%–56%) | 0 | 0 | 0 | 0 | 3/3 = 100.0% (95% CI 44%–100%) |
| noblank | 0/1 = 0.0% (95% CI 0%–79%) | 0 | 0 | 0 | 0 | 1/1 = 100.0% (95% CI 21%–100%) |
| wrap72 | 0/2 = 0.0% (95% CI 0%–66%) | 0 | 0 | 0 | 0 | 2/2 = 100.0% (95% CI 34%–100%) |

Cases that flipped at least once: none.
