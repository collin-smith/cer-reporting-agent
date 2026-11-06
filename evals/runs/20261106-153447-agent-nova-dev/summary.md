# Eval run 20261106-153447-agent-nova-dev

Arm `agent-nova`, splits ['dev'], 30 cases × 3 passes = 90 results. Cost $0.0958 ($0.00106/case); latency p50 12.5 s, p95 15.6 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 5 | ≤ 0 | **no** | 0/3 |
| late_deadlines | 2 | ≤ 0 | **no** | 1/3 |
| deadline_correct | 0.922 | ≥ 0.95 | **no** | 0/3 |
| over_notify | 0.000 | ≤ 0.3 | yes | 3/3 |
| missing_recall | 0.844 | ≥ 0.9 | **no** | 1/3 |
| extraction_accuracy | 0.972 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s | 15.627 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.867 | 0.900 | 0.867 | 0.867 | 0.900 |
| deadline_correct | 0.933 | 0.933 | 0.900 | 0.900 | 0.933 |
| route | 0.933 | 0.900 | 0.933 | 0.900 | 0.933 |
| missed_reports | 2 | 1 | 2 | 1 | 2 |
| late_deadlines | 1 | 0 | 1 | 0 | 1 |
| over_notify | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| missing_recall | 0.800 | 0.933 | 0.800 | 0.800 | 0.933 |
| extraction_accuracy | 0.974 | 0.966 | 0.976 | 0.966 | 0.976 |

## Unstable cases (5): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| CL-030 | clear-cut | not reportable None clear-cut / precautionary T3 clear-cut / not reportable None clear-cut | 1/3 |
| CL-046 | clear-cut | reportable T24 clear-cut / reportable T24 clear-cut / reportable T3 clear-cut | 2/3 |
| JU-110 | judgment | precautionary T24 judgment / precautionary T3 clear-cut / precautionary T24 judgment | 2/3 |
| JU-127 | judgment | not reportable None clear-cut / not reportable None clear-cut / precautionary T24 judgment | 1/3 |
| JU-139 | judgment | precautionary T24 judgment / precautionary T24 judgment / not reportable None clear-cut | 2/3 |

## Metrics

- **status**: 79/90 = 87.8% (95% CI 79%–93%)
- **missed_reports**: 5/84 = 6.0% (95% CI 3%–13%)
- **late_deadlines**: 2/36 = 5.6% (95% CI 2%–18%)
- **deadline_correct**: 83/90 = 92.2% (95% CI 85%–96%)
- **over_notify**: 0/6 = 0.0% (95% CI 0%–39%)
- **route**: 83/90 = 92.2% (95% CI 85%–96%)
- **incident_types**: 81/90 = 90.0% (95% CI 82%–95%)
- **missing_recall**: 38/45 = 84.4% (95% CI 71%–92%)
- **extraction_accuracy**: 1441/1483 = 97.2% (95% CI 96%–98%)
- **injection_flagged**: n/a

## Extraction by field

| Field | Correct |
|---|---|
| death | 89/90 = 98.9% (95% CI 94%–100%) |
| discovered_at | 79/90 = 87.8% (95% CI 79%–93%) |
| env_effect | 86/90 = 95.6% (95% CI 89%–98%) |
| fire_linked_to_pipeline | 6/6 = 100.0% (95% CI 61%–100%) |
| fire_or_explosion | 90/90 = 100.0% (95% CI 96%–100%) |
| lands | 67/69 = 97.1% (95% CI 90%–99%) |
| limit_kpa | 90/90 = 100.0% (95% CI 96%–100%) |
| other_beyond_design | 90/90 = 100.0% (95% CI 96%–100%) |
| planned_venting | 69/69 = 100.0% (95% CI 95%–100%) |
| point:env_effect | 0/1 = 0.0% (95% CI 0%–79%) |
| point:lands | 0/3 = 0.0% (95% CI 0%–56%) |
| point:serious_injury | 3/3 = 100.0% (95% CI 44%–100%) |
| point:substance | 9/9 = 100.0% (95% CI 70%–100%) |
| point:volume_m3 | 2/3 = 66.7% (95% CI 21%–94%) |
| pressure_kpa | 86/90 = 95.6% (95% CI 89%–98%) |
| rate_estimated | 7/12 = 58.3% (95% CI 32%–81%) |
| rate_kg_s | 69/69 = 100.0% (95% CI 95%–100%) |
| release | 88/90 = 97.8% (95% CI 92%–99%) |
| rupture | 90/90 = 100.0% (95% CI 96%–100%) |
| serious_injury | 85/87 = 97.7% (95% CI 92%–99%) |
| substance | 59/60 = 98.3% (95% CI 91%–100%) |
| through_pipe_body_or_weld | 69/69 = 100.0% (95% CI 95%–100%) |
| toxic_plume | 90/90 = 100.0% (95% CI 96%–100%) |
| volume_estimated | 57/57 = 100.0% (95% CI 94%–100%) |
| volume_m3 | 61/66 = 92.4% (95% CI 83%–97%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| clear-cut | 48 | 43/48 = 89.6% (95% CI 78%–95%) | 45/48 = 93.8% (95% CI 83%–98%) |
| judgment | 36 | 30/36 = 83.3% (95% CI 68%–92%) | 32/36 = 88.9% (95% CI 75%–96%) |
| not-reportable | 6 | 6/6 = 100.0% (95% CI 61%–100%) | 6/6 = 100.0% (95% CI 61%–100%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 51 | 48/51 = 94.1% (95% CI 84%–98%) | 47/51 = 92.2% (95% CI 81%–97%) |
| mistral | 39 | 31/39 = 79.5% (95% CI 64%–89%) | 36/39 = 92.3% (95% CI 80%–97%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 90 | 79/90 = 87.8% (95% CI 79%–93%) | 83/90 = 92.2% (95% CI 85%–96%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 54 | 49/54 = 90.7% (95% CI 80%–96%) | 51/54 = 94.4% (95% CI 85%–98%) |
| reviewed | 36 | 30/36 = 83.3% (95% CI 68%–92%) | 32/36 = 88.9% (95% CI 75%–96%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 90 | 79/90 = 87.8% (95% CI 79%–93%) | 83/90 = 92.2% (95% CI 85%–96%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 90 | 79/90 = 87.8% (95% CI 79%–93%) | 83/90 = 92.2% (95% CI 85%–96%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-030 | clear-cut | precautionary T3 clear-cut | not reportable None clear-cut | discovered_at, release, volume_m3 | 2/3 |
| CL-034 | clear-cut | precautionary T24 clear-cut | reportable T24 clear-cut | volume_m3 | 3/3 |
| JU-124 | judgment | precautionary T24 judgment | reportable T24 clear-cut | rate_estimated | 3/3 |
| JU-127 | judgment | precautionary T24 judgment | not reportable None clear-cut | rate_estimated | 2/3 |
| JU-110 | judgment | precautionary T24 judgment | precautionary T3 clear-cut | serious_injury, env_effect, pressure_kpa | 1/3 |
| CL-046 | clear-cut | reportable T24 clear-cut | reportable T3 clear-cut | discovered_at, death | 1/3 |
| JU-139 | judgment | precautionary T24 judgment | not reportable None clear-cut | point:volume_m3 | 1/3 |

## Stability under formatting

Each report also run as `noblank`, `wrap72` (same words, different layout); a flip is a different status, deadline or route from the same case in the same pass. 9 variants identical after normalising were not run. Cost including variants $0.2594.

| Variant | Flips | Right → wrong | Wrong → right | Missed | Late | Status |
|---|---|---|---|---|---|---|
| all | 20/153 = 13.1% (95% CI 9%–19%) | 5 | 12 | 8 | 1 | 137/153 = 89.5% (95% CI 84%–93%) |
| noblank | 9/63 = 14.3% (95% CI 8%–25%) | 3 | 4 | 4 | 1 | 54/63 = 85.7% (95% CI 75%–92%) |
| wrap72 | 11/90 = 12.2% (95% CI 7%–21%) | 2 | 8 | 4 | 0 | 83/90 = 92.2% (95% CI 85%–96%) |

Cases that flipped at least once: CL-030, CL-034, CL-046, JU-110, JU-124, JU-127, JU-139, JU-143.
