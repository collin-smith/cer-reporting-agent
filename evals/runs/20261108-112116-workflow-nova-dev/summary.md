# Eval run 20261108-112116-workflow-nova-dev

Arm `workflow-nova`, splits ['dev'], 4 cases × 3 passes = 12 results. Cost $0.0024 ($0.00020/case); latency p50 0.8 s, p95 1.1 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 0 | ≤ 0 | yes | 3/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct | 1.000 | ≥ 0.95 | yes | 3/3 |
| over_notify | 0.000 | ≤ 0.3 | yes | 3/3 |
| missing_recall | n/a | ≥ 0.9 | **no** | 0/3 |
| extraction_accuracy | 0.948 | ≥ 0.95 | **no** | 0/3 |
| latency_p95_s | 1.063 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.750 | 0.750 | 0.750 | 0.750 | 0.750 |
| deadline_correct | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| route | 0.750 | 0.750 | 0.750 | 0.750 | 0.750 |
| missed_reports | 0 | 0 | 0 | 0 | 0 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| missing_recall | n/a | n/a | n/a | n/a | n/a |
| extraction_accuracy | 0.948 | 0.948 | 0.948 | 0.948 | 0.948 |

## Unstable cases (0): the answer changed between passes

None.

## Metrics

- **status**: 9/12 = 75.0% (95% CI 47%–91%)
- **missed_reports**: 0/6 = 0.0% (95% CI 0%–39%)
- **late_deadlines**: n/a
- **deadline_correct**: 12/12 = 100.0% (95% CI 76%–100%)
- **over_notify**: 0/6 = 0.0% (95% CI 0%–39%)
- **route**: 9/12 = 75.0% (95% CI 47%–91%)
- **incident_types**: 9/12 = 75.0% (95% CI 47%–91%)
- **missing_recall**: n/a
- **extraction_accuracy**: 165/174 = 94.8% (95% CI 90%–97%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 12/12 = 100.0% (95% CI 76%–100%) |
| discovered_at | 12/12 = 100.0% (95% CI 76%–100%) |
| env_effect | 9/9 = 100.0% (95% CI 70%–100%) |
| fire_or_explosion | 12/12 = 100.0% (95% CI 76%–100%) |
| lands | 3/6 = 50.0% (95% CI 19%–81%) |
| limit_kpa | 12/12 = 100.0% (95% CI 76%–100%) |
| other_beyond_design | 9/12 = 75.0% (95% CI 47%–91%) |
| planned_venting | 6/6 = 100.0% (95% CI 61%–100%) |
| point:env_effect | 3/3 = 100.0% (95% CI 44%–100%) |
| pressure_kpa | 12/12 = 100.0% (95% CI 76%–100%) |
| rate_kg_s | 6/6 = 100.0% (95% CI 61%–100%) |
| release | 12/12 = 100.0% (95% CI 76%–100%) |
| rupture | 12/12 = 100.0% (95% CI 76%–100%) |
| serious_injury | 12/12 = 100.0% (95% CI 76%–100%) |
| substance | 6/6 = 100.0% (95% CI 61%–100%) |
| through_pipe_body_or_weld | 3/6 = 50.0% (95% CI 19%–81%) |
| toxic_plume | 12/12 = 100.0% (95% CI 76%–100%) |
| volume_estimated | 6/6 = 100.0% (95% CI 61%–100%) |
| volume_m3 | 6/6 = 100.0% (95% CI 61%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| judgment | 6 | 3/6 = 50.0% (95% CI 19%–81%) | 6/6 = 100.0% (95% CI 61%–100%) |
| not-reportable | 6 | 6/6 = 100.0% (95% CI 61%–100%) | 6/6 = 100.0% (95% CI 61%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 3 | 3/3 = 100.0% (95% CI 44%–100%) | 3/3 = 100.0% (95% CI 44%–100%) |
| mistral | 9 | 6/9 = 66.7% (95% CI 35%–88%) | 9/9 = 100.0% (95% CI 70%–100%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| heldout | 3 | 3/3 = 100.0% (95% CI 44%–100%) | 3/3 = 100.0% (95% CI 44%–100%) |
| test | 9 | 6/9 = 66.7% (95% CI 35%–88%) | 9/9 = 100.0% (95% CI 70%–100%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| reviewed | 12 | 9/12 = 75.0% (95% CI 47%–91%) | 12/12 = 100.0% (95% CI 76%–100%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 12 | 9/12 = 75.0% (95% CI 47%–91%) | 12/12 = 100.0% (95% CI 76%–100%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 12 | 9/12 = 75.0% (95% CI 47%–91%) | 12/12 = 100.0% (95% CI 76%–100%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| JU-092 | judgment | precautionary T24 judgment | reportable T24 clear-cut | lands, other_beyond_design | 3/3 |
