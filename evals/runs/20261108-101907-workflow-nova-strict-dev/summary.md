# Eval run 20261108-101907-workflow-nova-strict-dev

Arm `workflow-nova-strict`, splits ['dev'], 6 cases × 3 passes = 18 results. Cost $0.0103 ($0.00057/case); latency p50 0.9 s, p95 1.7 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 9 | ≤ 0 | **no** | 0/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct | 0.500 | ≥ 0.95 | **no** | 0/3 |
| over_notify | n/a | ≤ 0.3 | **no** | 0/3 |
| missing_recall | n/a | ≥ 0.9 | **no** | 0/3 |
| extraction_accuracy | 0.939 | ≥ 0.95 | **no** | 0/3 |
| latency_p95_s | 1.694 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.167 | 0.167 | 0.333 | 0.167 | 0.333 |
| deadline_correct | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 |
| route | 0.667 | 0.667 | 0.833 | 0.667 | 0.833 |
| missed_reports | 3 | 3 | 3 | 3 | 3 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | n/a | n/a | n/a | n/a | n/a |
| missing_recall | n/a | n/a | n/a | n/a | n/a |
| extraction_accuracy | 0.939 | 0.939 | 0.939 | 0.939 | 0.939 |

## Unstable cases (1): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| CL-171 | clear-cut | precautionary T24 judgment / precautionary T24 judgment / reportable T24 clear-cut | 1/3 |

## Metrics

- **status**: 4/18 = 22.2% (95% CI 9%–45%)
- **missed_reports**: 9/18 = 50.0% (95% CI 29%–71%)
- **late_deadlines**: n/a
- **deadline_correct**: 9/18 = 50.0% (95% CI 29%–71%)
- **over_notify**: n/a
- **route**: 13/18 = 72.2% (95% CI 49%–88%)
- **incident_types**: 9/18 = 50.0% (95% CI 29%–71%)
- **missing_recall**: n/a
- **extraction_accuracy**: 186/198 = 93.9% (95% CI 90%–96%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 18/18 = 100.0% (95% CI 82%–100%) |
| discovered_at | 15/18 = 83.3% (95% CI 61%–94%) |
| env_effect | 18/18 = 100.0% (95% CI 82%–100%) |
| fire_or_explosion | 18/18 = 100.0% (95% CI 82%–100%) |
| limit_kpa | 18/18 = 100.0% (95% CI 82%–100%) |
| other_beyond_design | 9/18 = 50.0% (95% CI 29%–71%) |
| pressure_kpa | 18/18 = 100.0% (95% CI 82%–100%) |
| release | 18/18 = 100.0% (95% CI 82%–100%) |
| rupture | 18/18 = 100.0% (95% CI 82%–100%) |
| serious_injury | 18/18 = 100.0% (95% CI 82%–100%) |
| toxic_plume | 18/18 = 100.0% (95% CI 82%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 18 | 4/18 = 22.2% (95% CI 9%–45%) | 9/18 = 50.0% (95% CI 29%–71%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 9 | 1/9 = 11.1% (95% CI 2%–44%) | 6/9 = 66.7% (95% CI 35%–88%) |
| mistral | 9 | 3/9 = 33.3% (95% CI 12%–65%) | 3/9 = 33.3% (95% CI 12%–65%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 9 | 3/9 = 33.3% (95% CI 12%–65%) | 6/9 = 66.7% (95% CI 35%–88%) |
| test | 9 | 1/9 = 11.1% (95% CI 2%–44%) | 3/9 = 33.3% (95% CI 12%–65%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 18 | 4/18 = 22.2% (95% CI 9%–45%) | 9/18 = 50.0% (95% CI 29%–71%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 18 | 4/18 = 22.2% (95% CI 9%–45%) | 9/18 = 50.0% (95% CI 29%–71%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 18 | 4/18 = 22.2% (95% CI 9%–45%) | 9/18 = 50.0% (95% CI 29%–71%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-167 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | other_beyond_design | 3/3 |
| CL-168 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | other_beyond_design | 3/3 |
| CL-171 | clear-cut | reportable T24 clear-cut | precautionary T24 judgment | discovered_at | 2/3 |
| CL-173 | clear-cut | reportable T24 clear-cut | precautionary T24 judgment |  | 3/3 |
| CL-174 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | other_beyond_design | 3/3 |
