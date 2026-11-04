# Eval run 20261104-163507-workflow-nova-test

Arm `workflow-nova`, splits ['test'], 80 cases × 3 passes = 240 results. Cost $0.0479 ($0.00020/case); latency p50 0.8 s, p95 1.0 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 4 | ≤ 0 | **no** | 0/3 |
| late_deadlines | 1 | ≤ 0 | **no** | 2/3 |
| deadline_correct | 0.975 | ≥ 0.95 | yes | 3/3 |
| over_notify | 0.067 | ≤ 0.3 | yes | 3/3 |
| missing_recall | 0.936 | ≥ 0.9 | yes | 3/3 |
| extraction_accuracy | 0.966 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s | 0.955 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.912 | 0.925 | 0.912 | 0.912 | 0.925 |
| deadline_correct | 0.975 | 0.975 | 0.975 | 0.975 | 0.975 |
| route | 0.938 | 0.938 | 0.925 | 0.925 | 0.938 |
| missed_reports | 1 | 1 | 2 | 1 | 2 |
| late_deadlines | 0 | 0 | 1 | 0 | 1 |
| over_notify | 0.100 | 0.100 | 0.000 | 0.000 | 0.100 |
| missing_recall | 0.923 | 0.962 | 0.923 | 0.923 | 0.962 |
| extraction_accuracy | 0.967 | 0.964 | 0.967 | 0.964 | 0.967 |

## Unstable cases (4): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| CL-027 | clear-cut | reportable T3 clear-cut / precautionary T3 clear-cut / reportable T3 clear-cut | 1/3 |
| JU-099 | judgment | precautionary T3 judgment / precautionary T3 judgment / not reportable None clear-cut | 2/3 |
| NO-078 | not-reportable | not reportable None clear-cut / reportable T24 clear-cut / not reportable None clear-cut | 2/3 |
| NO-087 | not-reportable | reportable T24 clear-cut / not reportable None clear-cut / not reportable None clear-cut | 2/3 |

## Metrics

- **status**: 220/240 = 91.7% (95% CI 87%–95%)
- **missed_reports**: 4/210 = 1.9% (95% CI 1%–5%)
- **late_deadlines**: 1/114 = 0.9% (95% CI 0%–5%)
- **deadline_correct**: 234/240 = 97.5% (95% CI 95%–99%)
- **over_notify**: 2/30 = 6.7% (95% CI 2%–21%)
- **route**: 224/240 = 93.3% (95% CI 89%–96%)
- **incident_types**: 205/240 = 85.4% (95% CI 80%–89%)
- **missing_recall**: 73/78 = 93.6% (95% CI 86%–97%)
- **extraction_accuracy**: 3552/3677 = 96.6% (95% CI 96%–97%)
- **injection_flagged**: 9/30 = 30.0% (95% CI 17%–48%)

## Extraction by field

| Field | Correct |
|---|---|
| death | 239/240 = 99.6% (95% CI 98%–100%) |
| discovered_at | 228/240 = 95.0% (95% CI 91%–97%) |
| env_effect | 217/234 = 92.7% (95% CI 89%–95%) |
| fire_linked_to_pipeline | 51/54 = 94.4% (95% CI 85%–98%) |
| fire_or_explosion | 238/240 = 99.2% (95% CI 97%–100%) |
| lands | 96/126 = 76.2% (95% CI 68%–83%) |
| limit_kpa | 233/240 = 97.1% (95% CI 94%–99%) |
| other_beyond_design | 223/240 = 92.9% (95% CI 89%–96%) |
| planned_venting | 140/141 = 99.3% (95% CI 96%–100%) |
| point:env_effect | 6/11 = 54.5% (95% CI 28%–79%) |
| point:lands | 12/15 = 80.0% (95% CI 55%–93%) |
| point:serious_injury | 2/3 = 66.7% (95% CI 21%–94%) |
| point:substance | 9/9 = 100.0% (95% CI 70%–100%) |
| point:volume_m3 | 9/9 = 100.0% (95% CI 70%–100%) |
| pressure_kpa | 233/240 = 97.1% (95% CI 94%–99%) |
| rate_estimated | 9/9 = 100.0% (95% CI 70%–100%) |
| rate_kg_s | 141/141 = 100.0% (95% CI 97%–100%) |
| release | 237/240 = 98.8% (95% CI 96%–100%) |
| rupture | 240/240 = 100.0% (95% CI 98%–100%) |
| serious_injury | 236/237 = 99.6% (95% CI 98%–100%) |
| substance | 132/132 = 100.0% (95% CI 97%–100%) |
| through_pipe_body_or_weld | 135/141 = 95.7% (95% CI 91%–98%) |
| toxic_plume | 240/240 = 100.0% (95% CI 98%–100%) |
| volume_estimated | 114/123 = 92.7% (95% CI 87%–96%) |
| volume_m3 | 132/132 = 100.0% (95% CI 97%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| adversarial | 30 | 30/30 = 100.0% (95% CI 89%–100%) | 30/30 = 100.0% (95% CI 89%–100%) |
| clear-cut | 102 | 97/102 = 95.1% (95% CI 89%–98%) | 102/102 = 100.0% (95% CI 96%–100%) |
| judgment | 78 | 65/78 = 83.3% (95% CI 74%–90%) | 74/78 = 94.9% (95% CI 88%–98%) |
| not-reportable | 30 | 28/30 = 93.3% (95% CI 79%–98%) | 28/30 = 93.3% (95% CI 79%–98%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 114 | 111/114 = 97.4% (95% CI 93%–99%) | 113/114 = 99.1% (95% CI 95%–100%) |
| mistral | 126 | 109/126 = 86.5% (95% CI 79%–91%) | 121/126 = 96.0% (95% CI 91%–98%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| test | 240 | 220/240 = 91.7% (95% CI 87%–95%) | 234/240 = 97.5% (95% CI 95%–99%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 156 | 149/156 = 95.5% (95% CI 91%–98%) | 154/156 = 98.7% (95% CI 95%–100%) |
| reviewed | 84 | 71/84 = 84.5% (95% CI 75%–91%) | 80/84 = 95.2% (95% CI 88%–98%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 240 | 220/240 = 91.7% (95% CI 87%–95%) | 234/240 = 97.5% (95% CI 95%–99%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| text | 240 | 220/240 = 91.7% (95% CI 87%–95%) | 234/240 = 97.5% (95% CI 95%–99%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-015 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | env_effect, through_pipe_body_or_weld, lands, other_beyond_design | 3/3 |
| CL-027 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | lands, other_beyond_design | 2/3 |
| NO-087 | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | fire_linked_to_pipeline | 1/3 |
| JU-092 | judgment | precautionary T24 judgment | reportable T24 clear-cut | other_beyond_design | 3/3 |
| JU-094 | judgment | precautionary T24 judgment | reportable T24 clear-cut | lands, other_beyond_design | 3/3 |
| JU-096 | judgment | precautionary T24 judgment | reportable T24 clear-cut | through_pipe_body_or_weld, other_beyond_design | 3/3 |
| JU-129 | judgment | reportable T3 judgment | reportable T3 clear-cut | env_effect, point:lands | 3/3 |
| JU-138 | judgment | precautionary T24 judgment | not reportable None clear-cut | release | 3/3 |
| NO-078 | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | volume_estimated, planned_venting, lands | 1/3 |
| JU-099 | judgment | precautionary T3 judgment | not reportable None clear-cut | point:serious_injury | 1/3 |

## Stability under formatting

Each report also run as `noblank`, `wrap72` (same words, different layout); a flip is a different status, deadline or route from the same case in the same pass. 18 variants identical after normalising were not run. Cost including variants $0.1331.

| Variant | Flips | Right → wrong | Wrong → right | Missed | Late | Status |
|---|---|---|---|---|---|---|
| all | 28/426 = 6.6% (95% CI 5%–9%) | 17 | 8 | 9 | 7 | 384/426 = 90.1% (95% CI 87%–93%) |
| noblank | 13/186 = 7.0% (95% CI 4%–12%) | 9 | 4 | 6 | 0 | 164/186 = 88.2% (95% CI 83%–92%) |
| wrap72 | 15/240 = 6.2% (95% CI 4%–10%) | 8 | 4 | 3 | 7 | 220/240 = 91.7% (95% CI 87%–95%) |

Cases that flipped at least once: AD-148, CL-016, CL-027, CL-029, CL-070, JU-094, JU-099, JU-137, JU-138, NO-078, NO-087, NO-164.
