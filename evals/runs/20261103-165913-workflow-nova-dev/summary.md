# Eval run 20261103-165913-workflow-nova-dev

Arm `workflow-nova`, splits ['dev'], 30 cases × 3 passes = 90 results. Cost $0.0175 ($0.00019/case); latency p50 0.8 s, p95 1.0 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 3 | ≤ 0 | **no** | 0/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct [proposed] | 0.811 | ≥ 0.95 | **no** | 0/3 |
| over_notify [proposed] | 0.000 | ≤ 0.3 | yes | 3/3 |
| missing_recall [proposed] | 0.978 | ≥ 0.9 | yes | 3/3 |
| extraction_accuracy [proposed] | 0.947 | ≥ 0.95 | **no** | 0/3 |
| latency_p95_s [proposed] | 1.042 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.967 | 0.933 | 0.967 | 0.933 | 0.967 |
| deadline_correct | 0.833 | 0.800 | 0.800 | 0.800 | 0.833 |
| route | 0.833 | 0.833 | 0.833 | 0.833 | 0.833 |
| missed_reports | 1 | 1 | 1 | 1 | 1 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| missing_recall | 0.933 | 1.000 | 1.000 | 0.933 | 1.000 |
| extraction_accuracy | 0.947 | 0.945 | 0.947 | 0.945 | 0.947 |

## Unstable cases (5): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| CL-007 | clear-cut | reportable T3 clear-cut / precautionary T3 clear-cut / reportable T3 clear-cut | 2/3 |
| CL-034 | clear-cut | precautionary T24 clear-cut / precautionary T3 clear-cut / precautionary T3 clear-cut | 1/3 |
| JU-126 | judgment | precautionary T24 judgment / precautionary T3 clear-cut / precautionary T3 clear-cut | 1/3 |
| JU-139 | judgment | precautionary T3 judgment / precautionary T24 judgment / precautionary T24 judgment | 2/3 |
| JU-143 | judgment | reportable T3 clear-cut / reportable T3 judgment / reportable T3 judgment | 2/3 |

## Metrics

- **status**: 86/90 = 95.6% (95% CI 89%–98%)
- **missed_reports**: 3/84 = 3.6% (95% CI 1%–10%)
- **late_deadlines**: 0/36 = 0.0% (95% CI 0%–10%)
- **deadline_correct**: 73/90 = 81.1% (95% CI 72%–88%)
- **over_notify**: 0/6 = 0.0% (95% CI 0%–39%)
- **route**: 75/90 = 83.3% (95% CI 74%–90%)
- **incident_types**: 67/90 = 74.4% (95% CI 65%–82%)
- **missing_recall**: 44/45 = 97.8% (95% CI 88%–100%)
- **extraction_accuracy**: 1406/1485 = 94.7% (95% CI 93%–96%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 90/90 = 100.0% (95% CI 96%–100%) |
| discovered_at | 90/90 = 100.0% (95% CI 96%–100%) |
| env_effect | 82/90 = 91.1% (95% CI 83%–95%) |
| fire_linked_to_pipeline | 6/6 = 100.0% (95% CI 61%–100%) |
| fire_or_explosion | 90/90 = 100.0% (95% CI 96%–100%) |
| lands | 56/69 = 81.2% (95% CI 70%–89%) |
| limit_kpa | 90/90 = 100.0% (95% CI 96%–100%) |
| other_beyond_design | 85/90 = 94.4% (95% CI 88%–98%) |
| planned_venting | 69/69 = 100.0% (95% CI 95%–100%) |
| point:env_effect | 0/6 = 0.0% (95% CI 0%–39%) |
| point:serious_injury | 3/3 = 100.0% (95% CI 44%–100%) |
| point:substance | 9/9 = 100.0% (95% CI 70%–100%) |
| point:volume_m3 | 3/3 = 100.0% (95% CI 44%–100%) |
| pressure_kpa | 90/90 = 100.0% (95% CI 96%–100%) |
| rate_estimated | 9/12 = 75.0% (95% CI 47%–91%) |
| rate_kg_s | 64/69 = 92.8% (95% CI 84%–97%) |
| release | 84/90 = 93.3% (95% CI 86%–97%) |
| rupture | 90/90 = 100.0% (95% CI 96%–100%) |
| serious_injury | 81/87 = 93.1% (95% CI 86%–97%) |
| substance | 60/60 = 100.0% (95% CI 94%–100%) |
| through_pipe_body_or_weld | 69/69 = 100.0% (95% CI 95%–100%) |
| toxic_plume | 90/90 = 100.0% (95% CI 96%–100%) |
| volume_estimated | 48/57 = 84.2% (95% CI 73%–91%) |
| volume_m3 | 48/66 = 72.7% (95% CI 61%–82%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 48 | 44/48 = 91.7% (95% CI 80%–97%) | 40/48 = 83.3% (95% CI 70%–91%) |
| judgment | 36 | 36/36 = 100.0% (95% CI 90%–100%) | 27/36 = 75.0% (95% CI 59%–86%) |
| not-reportable | 6 | 6/6 = 100.0% (95% CI 61%–100%) | 6/6 = 100.0% (95% CI 61%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 51 | 51/51 = 100.0% (95% CI 93%–100%) | 42/51 = 82.4% (95% CI 70%–90%) |
| mistral | 39 | 35/39 = 89.7% (95% CI 76%–96%) | 31/39 = 79.5% (95% CI 64%–89%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 90 | 86/90 = 95.6% (95% CI 89%–98%) | 73/90 = 81.1% (95% CI 72%–88%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 54 | 50/54 = 92.6% (95% CI 82%–97%) | 46/54 = 85.2% (95% CI 73%–92%) |
| reviewed | 36 | 36/36 = 100.0% (95% CI 90%–100%) | 27/36 = 75.0% (95% CI 59%–86%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 90 | 86/90 = 95.6% (95% CI 89%–98%) | 73/90 = 81.1% (95% CI 72%–88%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-023 | clear-cut | reportable T24 clear-cut | reportable T3 clear-cut | release | 3/3 |
| CL-046 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | other_beyond_design | 3/3 |
| JU-110 | judgment | precautionary T24 judgment | precautionary T3 clear-cut | serious_injury, env_effect | 3/3 |
| JU-124 | judgment | precautionary T24 judgment | precautionary T3 clear-cut | volume_m3, volume_estimated, rate_kg_s, rate_estimated | 3/3 |
| JU-139 | judgment | precautionary T24 judgment | precautionary T3 judgment | lands | 1/3 |
| JU-142 | judgment | reportable T3 judgment | reportable T3 clear-cut | volume_m3, lands | 3/3 |
| JU-143 | judgment | reportable T3 judgment | reportable T3 clear-cut | volume_m3 | 1/3 |
| JU-147 | judgment | reportable T3 judgment | reportable T3 clear-cut | serious_injury | 3/3 |
| CL-007 | clear-cut | reportable T3 clear-cut | precautionary T3 clear-cut | volume_m3 | 1/3 |
| CL-034 | clear-cut | precautionary T24 clear-cut | precautionary T3 clear-cut | lands | 2/3 |
| JU-126 | judgment | precautionary T24 judgment | precautionary T3 clear-cut | volume_m3, rate_kg_s | 2/3 |
