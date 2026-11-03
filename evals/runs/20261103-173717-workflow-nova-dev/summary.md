# Eval run 20261103-173717-workflow-nova-dev

Arm `workflow-nova`, splits ['dev'], 30 cases × 3 passes = 90 results. Cost $0.0181 ($0.00020/case); latency p50 0.9 s, p95 1.0 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 0 | ≤ 0 | yes | 3/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct | 0.978 | ≥ 0.95 | **no** | 2/3 |
| over_notify | 0.167 | ≤ 0.3 | **no** | 2/3 |
| missing_recall | 0.933 | ≥ 0.9 | yes | 3/3 |
| extraction_accuracy | 0.988 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s | 1.025 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.933 | 0.967 | 0.967 | 0.933 | 0.967 |
| deadline_correct | 0.933 | 1.000 | 1.000 | 0.933 | 1.000 |
| route | 0.933 | 0.933 | 0.933 | 0.933 | 0.933 |
| missed_reports | 0 | 0 | 0 | 0 | 0 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | 0.500 | 0.000 | 0.000 | 0.000 | 0.500 |
| missing_recall | 0.933 | 0.933 | 0.933 | 0.933 | 0.933 |
| extraction_accuracy | 0.984 | 0.990 | 0.990 | 0.984 | 0.990 |

## Unstable cases (2): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| JU-111 | judgment | precautionary T3 judgment / precautionary T24 judgment / precautionary T24 judgment | 2/3 |
| NO-090 | not-reportable | precautionary T24 clear-cut / not reportable None clear-cut / not reportable None clear-cut | 2/3 |

## Metrics

- **status**: 86/90 = 95.6% (95% CI 89%–98%)
- **missed_reports**: 0/84 = 0.0% (95% CI 0%–4%)
- **late_deadlines**: 0/36 = 0.0% (95% CI 0%–10%)
- **deadline_correct**: 88/90 = 97.8% (95% CI 92%–99%)
- **over_notify**: 1/6 = 16.7% (95% CI 3%–56%)
- **route**: 84/90 = 93.3% (95% CI 86%–97%)
- **incident_types**: 86/90 = 95.6% (95% CI 89%–98%)
- **missing_recall**: 42/45 = 93.3% (95% CI 82%–98%)
- **extraction_accuracy**: 1464/1482 = 98.8% (95% CI 98%–99%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 90/90 = 100.0% (95% CI 96%–100%) |
| discovered_at | 89/90 = 98.9% (95% CI 94%–100%) |
| env_effect | 90/90 = 100.0% (95% CI 96%–100%) |
| fire_linked_to_pipeline | 6/6 = 100.0% (95% CI 61%–100%) |
| fire_or_explosion | 90/90 = 100.0% (95% CI 96%–100%) |
| lands | 62/69 = 89.9% (95% CI 81%–95%) |
| limit_kpa | 90/90 = 100.0% (95% CI 96%–100%) |
| other_beyond_design | 90/90 = 100.0% (95% CI 96%–100%) |
| planned_venting | 69/69 = 100.0% (95% CI 95%–100%) |
| point:env_effect | 0/3 = 0.0% (95% CI 0%–56%) |
| point:serious_injury | 3/3 = 100.0% (95% CI 44%–100%) |
| point:substance | 9/9 = 100.0% (95% CI 70%–100%) |
| point:volume_m3 | 3/3 = 100.0% (95% CI 44%–100%) |
| pressure_kpa | 90/90 = 100.0% (95% CI 96%–100%) |
| rate_estimated | 9/12 = 75.0% (95% CI 47%–91%) |
| rate_kg_s | 69/69 = 100.0% (95% CI 95%–100%) |
| release | 90/90 = 100.0% (95% CI 96%–100%) |
| rupture | 90/90 = 100.0% (95% CI 96%–100%) |
| serious_injury | 87/87 = 100.0% (95% CI 96%–100%) |
| substance | 59/60 = 98.3% (95% CI 91%–100%) |
| through_pipe_body_or_weld | 69/69 = 100.0% (95% CI 95%–100%) |
| toxic_plume | 90/90 = 100.0% (95% CI 96%–100%) |
| volume_estimated | 57/57 = 100.0% (95% CI 94%–100%) |
| volume_m3 | 63/66 = 95.5% (95% CI 87%–98%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 48 | 48/48 = 100.0% (95% CI 93%–100%) | 48/48 = 100.0% (95% CI 93%–100%) |
| judgment | 36 | 33/36 = 91.7% (95% CI 78%–97%) | 35/36 = 97.2% (95% CI 86%–100%) |
| not-reportable | 6 | 5/6 = 83.3% (95% CI 44%–97%) | 5/6 = 83.3% (95% CI 44%–97%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 51 | 50/51 = 98.0% (95% CI 90%–100%) | 50/51 = 98.0% (95% CI 90%–100%) |
| mistral | 39 | 36/39 = 92.3% (95% CI 80%–97%) | 38/39 = 97.4% (95% CI 87%–100%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 90 | 86/90 = 95.6% (95% CI 89%–98%) | 88/90 = 97.8% (95% CI 92%–99%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 54 | 53/54 = 98.1% (95% CI 90%–100%) | 53/54 = 98.1% (95% CI 90%–100%) |
| reviewed | 36 | 33/36 = 91.7% (95% CI 78%–97%) | 35/36 = 97.2% (95% CI 86%–100%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 90 | 86/90 = 95.6% (95% CI 89%–98%) | 88/90 = 97.8% (95% CI 92%–99%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-034 | clear-cut | precautionary T24 clear-cut | precautionary T24 judgment | volume_m3 | 3/3 |
| NO-090 | not-reportable | not reportable None clear-cut | precautionary T24 clear-cut | discovered_at, substance | 1/3 |
| JU-111 | judgment | precautionary T24 judgment | precautionary T3 judgment | lands | 1/3 |
| JU-124 | judgment | precautionary T24 judgment | reportable T24 clear-cut | rate_estimated | 3/3 |
