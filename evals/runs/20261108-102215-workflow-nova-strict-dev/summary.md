# Eval run 20261108-102215-workflow-nova-strict-dev

Arm `workflow-nova-strict`, splits ['dev'], 33 cases × 3 passes = 99 results. Cost $0.0550 ($0.00056/case); latency p50 0.9 s, p95 1.2 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 0 | ≤ 0 | yes | 3/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct | 0.939 | ≥ 0.95 | **no** | 0/3 |
| over_notify | 0.500 | ≤ 0.3 | **no** | 0/3 |
| missing_recall | 0.933 | ≥ 0.9 | yes | 3/3 |
| extraction_accuracy | 0.982 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s | 1.208 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.939 | 0.939 | 0.939 | 0.939 | 0.939 |
| deadline_correct | 0.939 | 0.939 | 0.939 | 0.939 | 0.939 |
| route | 0.909 | 0.909 | 0.909 | 0.909 | 0.909 |
| missed_reports | 0 | 0 | 0 | 0 | 0 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 |
| missing_recall | 0.933 | 0.933 | 0.933 | 0.933 | 0.933 |
| extraction_accuracy | 0.981 | 0.983 | 0.981 | 0.981 | 0.983 |

## Unstable cases (0): the answer changed between passes

None.

## Metrics

- **status**: 93/99 = 93.9% (95% CI 87%–97%)
- **missed_reports**: 0/93 = 0.0% (95% CI 0%–4%)
- **late_deadlines**: 0/36 = 0.0% (95% CI 0%–10%)
- **deadline_correct**: 93/99 = 93.9% (95% CI 87%–97%)
- **over_notify**: 3/6 = 50.0% (95% CI 19%–81%)
- **route**: 90/99 = 90.9% (95% CI 84%–95%)
- **incident_types**: 89/99 = 89.9% (95% CI 82%–94%)
- **missing_recall**: 42/45 = 93.3% (95% CI 82%–98%)
- **extraction_accuracy**: 1555/1584 = 98.2% (95% CI 97%–99%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 99/99 = 100.0% (95% CI 96%–100%) |
| discovered_at | 99/99 = 100.0% (95% CI 96%–100%) |
| env_effect | 96/99 = 97.0% (95% CI 91%–99%) |
| fire_linked_to_pipeline | 6/6 = 100.0% (95% CI 61%–100%) |
| fire_or_explosion | 99/99 = 100.0% (95% CI 96%–100%) |
| lands | 61/69 = 88.4% (95% CI 79%–94%) |
| limit_kpa | 99/99 = 100.0% (95% CI 96%–100%) |
| other_beyond_design | 99/99 = 100.0% (95% CI 96%–100%) |
| planned_venting | 69/69 = 100.0% (95% CI 95%–100%) |
| point:env_effect | 0/6 = 0.0% (95% CI 0%–39%) |
| point:serious_injury | 3/3 = 100.0% (95% CI 44%–100%) |
| point:substance | 9/9 = 100.0% (95% CI 70%–100%) |
| point:volume_m3 | 3/3 = 100.0% (95% CI 44%–100%) |
| pressure_kpa | 99/99 = 100.0% (95% CI 96%–100%) |
| rate_estimated | 7/12 = 58.3% (95% CI 32%–81%) |
| rate_kg_s | 69/69 = 100.0% (95% CI 95%–100%) |
| release | 99/99 = 100.0% (95% CI 96%–100%) |
| rupture | 99/99 = 100.0% (95% CI 96%–100%) |
| serious_injury | 96/96 = 100.0% (95% CI 96%–100%) |
| substance | 57/60 = 95.0% (95% CI 86%–98%) |
| through_pipe_body_or_weld | 68/69 = 98.6% (95% CI 92%–100%) |
| toxic_plume | 99/99 = 100.0% (95% CI 96%–100%) |
| volume_estimated | 57/57 = 100.0% (95% CI 94%–100%) |
| volume_m3 | 63/66 = 95.5% (95% CI 87%–98%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 57 | 57/57 = 100.0% (95% CI 94%–100%) | 54/57 = 94.7% (95% CI 86%–98%) |
| judgment | 36 | 33/36 = 91.7% (95% CI 78%–97%) | 36/36 = 100.0% (95% CI 90%–100%) |
| not-reportable | 6 | 3/6 = 50.0% (95% CI 19%–81%) | 3/6 = 50.0% (95% CI 19%–81%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 57 | 54/57 = 94.7% (95% CI 86%–98%) | 54/57 = 94.7% (95% CI 86%–98%) |
| mistral | 42 | 39/42 = 92.9% (95% CI 81%–98%) | 39/42 = 92.9% (95% CI 81%–98%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 99 | 93/99 = 93.9% (95% CI 87%–97%) | 93/99 = 93.9% (95% CI 87%–97%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 63 | 60/63 = 95.2% (95% CI 87%–98%) | 57/63 = 90.5% (95% CI 81%–96%) |
| reviewed | 36 | 33/36 = 91.7% (95% CI 78%–97%) | 36/36 = 100.0% (95% CI 90%–100%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 99 | 93/99 = 93.9% (95% CI 87%–97%) | 93/99 = 93.9% (95% CI 87%–97%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 99 | 93/99 = 93.9% (95% CI 87%–97%) | 93/99 = 93.9% (95% CI 87%–97%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-034 | clear-cut | precautionary T24 clear-cut | precautionary T3 judgment | volume_m3, lands | 3/3 |
| NO-090 | not-reportable | not reportable None clear-cut | precautionary T24 judgment | substance | 3/3 |
| JU-124 | judgment | precautionary T24 judgment | reportable T24 clear-cut | rate_estimated | 3/3 |
