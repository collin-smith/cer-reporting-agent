# Eval run 20261108-101832-workflow-nova-dev

Arm `workflow-nova`, splits ['dev'], 6 cases × 3 passes = 18 results. Cost $0.0036 ($0.00020/case); latency p50 0.8 s, p95 1.2 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 10 | ≤ 0 | **no** | 0/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct | 0.444 | ≥ 0.95 | **no** | 0/3 |
| over_notify | n/a | ≤ 0.3 | **no** | 0/3 |
| missing_recall | n/a | ≥ 0.9 | **no** | 0/3 |
| extraction_accuracy | 0.924 | ≥ 0.95 | **no** | 0/3 |
| latency_p95_s | 1.238 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.333 | 0.500 | 0.500 | 0.333 | 0.500 |
| deadline_correct | 0.333 | 0.500 | 0.500 | 0.333 | 0.500 |
| route | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| missed_reports | 4 | 3 | 3 | 3 | 4 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | n/a | n/a | n/a | n/a | n/a |
| missing_recall | n/a | n/a | n/a | n/a | n/a |
| extraction_accuracy | 0.894 | 0.939 | 0.939 | 0.894 | 0.939 |

## Unstable cases (1): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| CL-173 | clear-cut | not reportable None clear-cut / reportable T24 clear-cut / reportable T24 clear-cut | 2/3 |

## Metrics

- **status**: 8/18 = 44.4% (95% CI 25%–66%)
- **missed_reports**: 10/18 = 55.6% (95% CI 34%–75%)
- **late_deadlines**: n/a
- **deadline_correct**: 8/18 = 44.4% (95% CI 25%–66%)
- **over_notify**: n/a
- **route**: 18/18 = 100.0% (95% CI 82%–100%)
- **incident_types**: 8/18 = 44.4% (95% CI 25%–66%)
- **missing_recall**: n/a
- **extraction_accuracy**: 183/198 = 92.4% (95% CI 88%–95%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 18/18 = 100.0% (95% CI 82%–100%) |
| discovered_at | 15/18 = 83.3% (95% CI 61%–94%) |
| env_effect | 18/18 = 100.0% (95% CI 82%–100%) |
| fire_or_explosion | 18/18 = 100.0% (95% CI 82%–100%) |
| limit_kpa | 17/18 = 94.4% (95% CI 74%–99%) |
| other_beyond_design | 8/18 = 44.4% (95% CI 25%–66%) |
| pressure_kpa | 17/18 = 94.4% (95% CI 74%–99%) |
| release | 18/18 = 100.0% (95% CI 82%–100%) |
| rupture | 18/18 = 100.0% (95% CI 82%–100%) |
| serious_injury | 18/18 = 100.0% (95% CI 82%–100%) |
| toxic_plume | 18/18 = 100.0% (95% CI 82%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 18 | 8/18 = 44.4% (95% CI 25%–66%) | 8/18 = 44.4% (95% CI 25%–66%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 9 | 5/9 = 55.6% (95% CI 27%–81%) | 5/9 = 55.6% (95% CI 27%–81%) |
| mistral | 9 | 3/9 = 33.3% (95% CI 12%–65%) | 3/9 = 33.3% (95% CI 12%–65%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 9 | 5/9 = 55.6% (95% CI 27%–81%) | 5/9 = 55.6% (95% CI 27%–81%) |
| test | 9 | 3/9 = 33.3% (95% CI 12%–65%) | 3/9 = 33.3% (95% CI 12%–65%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 18 | 8/18 = 44.4% (95% CI 25%–66%) | 8/18 = 44.4% (95% CI 25%–66%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 18 | 8/18 = 44.4% (95% CI 25%–66%) | 8/18 = 44.4% (95% CI 25%–66%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 18 | 8/18 = 44.4% (95% CI 25%–66%) | 8/18 = 44.4% (95% CI 25%–66%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-167 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | other_beyond_design | 3/3 |
| CL-168 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | other_beyond_design | 3/3 |
| CL-173 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | pressure_kpa, limit_kpa, other_beyond_design | 1/3 |
| CL-174 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | other_beyond_design | 3/3 |
