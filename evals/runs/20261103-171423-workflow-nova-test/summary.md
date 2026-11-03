# Eval run 20261103-171423-workflow-nova-test

Arm `workflow-nova`, splits ['test'], 80 cases × 3 passes = 240 results. Cost $0.0483 ($0.00020/case); latency p50 0.8 s, p95 1.0 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 3 | ≤ 0 | **no** | 0/3 |
| late_deadlines | 3 | ≤ 0 | **no** | 0/3 |
| deadline_correct | 0.821 | ≥ 0.95 | **no** | 0/3 |
| over_notify | 0.367 | ≤ 0.3 | **no** | 1/3 |
| missing_recall | 0.936 | ≥ 0.9 | yes | 3/3 |
| extraction_accuracy | 0.938 | ≥ 0.95 | **no** | 0/3 |
| latency_p95_s | 0.971 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.850 | 0.863 | 0.838 | 0.838 | 0.863 |
| deadline_correct | 0.838 | 0.812 | 0.812 | 0.812 | 0.838 |
| route | 0.925 | 0.925 | 0.925 | 0.925 | 0.925 |
| missed_reports | 1 | 1 | 1 | 1 | 1 |
| late_deadlines | 1 | 1 | 1 | 1 | 1 |
| over_notify | 0.300 | 0.400 | 0.400 | 0.300 | 0.400 |
| missing_recall | 0.962 | 0.923 | 0.923 | 0.923 | 0.962 |
| extraction_accuracy | 0.942 | 0.938 | 0.934 | 0.934 | 0.942 |

## Unstable cases (10): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| CL-001 | clear-cut | reportable T24 clear-cut / reportable T3 clear-cut / reportable T3 clear-cut | 1/3 |
| CL-011 | clear-cut | reportable T3 clear-cut / reportable T3 clear-cut / precautionary T3 clear-cut | 0/3 |
| CL-027 | clear-cut | reportable T3 clear-cut / precautionary T3 clear-cut / precautionary T3 clear-cut | 2/3 |
| CL-028 | clear-cut | reportable T3 clear-cut / reportable T24 clear-cut / reportable T24 clear-cut | 2/3 |
| CL-029 | clear-cut | reportable T24 clear-cut / not reportable None clear-cut / not reportable None clear-cut | 1/3 |
| CL-047 | clear-cut | precautionary T3 clear-cut / reportable T3 clear-cut / precautionary T3 clear-cut | 0/3 |
| CL-074 | clear-cut | reportable T24 clear-cut / reportable T3 clear-cut / reportable T3 clear-cut | 1/3 |
| JU-099 | judgment | precautionary T3 judgment / precautionary T3 clear-cut / precautionary T3 clear-cut | 1/3 |
| JU-137 | judgment | not reportable None clear-cut / precautionary T24 judgment / precautionary T24 judgment | 2/3 |
| NO-164 | not-reportable | not reportable None clear-cut / reportable T24 clear-cut / reportable T24 clear-cut | 1/3 |

## Metrics

- **status**: 204/240 = 85.0% (95% CI 80%–89%)
- **missed_reports**: 3/210 = 1.4% (95% CI 0%–4%)
- **late_deadlines**: 3/114 = 2.6% (95% CI 1%–7%)
- **deadline_correct**: 197/240 = 82.1% (95% CI 77%–86%)
- **over_notify**: 11/30 = 36.7% (95% CI 22%–54%)
- **route**: 222/240 = 92.5% (95% CI 88%–95%)
- **incident_types**: 146/240 = 60.8% (95% CI 55%–67%)
- **missing_recall**: 73/78 = 93.6% (95% CI 86%–97%)
- **extraction_accuracy**: 3431/3658 = 93.8% (95% CI 93%–95%)
- **injection_flagged**: 11/30 = 36.7% (95% CI 22%–54%)

## Extraction by field

| Field | Correct |
|---|---|
| death | 225/240 = 93.8% (95% CI 90%–96%) |
| discovered_at | 237/240 = 98.8% (95% CI 96%–100%) |
| env_effect | 197/234 = 84.2% (95% CI 79%–88%) |
| fire_linked_to_pipeline | 49/54 = 90.7% (95% CI 80%–96%) |
| fire_or_explosion | 232/240 = 96.7% (95% CI 94%–98%) |
| lands | 95/123 = 77.2% (95% CI 69%–84%) |
| limit_kpa | 237/240 = 98.8% (95% CI 96%–100%) |
| other_beyond_design | 222/240 = 92.5% (95% CI 88%–95%) |
| planned_venting | 138/138 = 100.0% (95% CI 97%–100%) |
| point:env_effect | 6/12 = 50.0% (95% CI 25%–75%) |
| point:fire_linked_to_pipeline | 0/1 = 0.0% (95% CI 0%–79%) |
| point:lands | 9/15 = 60.0% (95% CI 36%–80%) |
| point:serious_injury | 3/3 = 100.0% (95% CI 44%–100%) |
| point:substance | 9/9 = 100.0% (95% CI 70%–100%) |
| point:volume_m3 | 8/9 = 88.9% (95% CI 56%–98%) |
| pressure_kpa | 237/240 = 98.8% (95% CI 96%–100%) |
| rate_estimated | 9/9 = 100.0% (95% CI 70%–100%) |
| rate_kg_s | 138/138 = 100.0% (95% CI 97%–100%) |
| release | 185/240 = 77.1% (95% CI 71%–82%) |
| rupture | 240/240 = 100.0% (95% CI 98%–100%) |
| serious_injury | 220/237 = 92.8% (95% CI 89%–95%) |
| substance | 129/129 = 100.0% (95% CI 97%–100%) |
| through_pipe_body_or_weld | 132/138 = 95.7% (95% CI 91%–98%) |
| toxic_plume | 234/240 = 97.5% (95% CI 95%–99%) |
| volume_estimated | 111/120 = 92.5% (95% CI 86%–96%) |
| volume_m3 | 129/129 = 100.0% (95% CI 97%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| adversarial | 30 | 27/30 = 90.0% (95% CI 74%–97%) | 24/30 = 80.0% (95% CI 63%–90%) |
| clear-cut | 102 | 90/102 = 88.2% (95% CI 81%–93%) | 80/102 = 78.4% (95% CI 69%–85%) |
| judgment | 78 | 68/78 = 87.2% (95% CI 78%–93%) | 74/78 = 94.9% (95% CI 88%–98%) |
| not-reportable | 30 | 19/30 = 63.3% (95% CI 46%–78%) | 19/30 = 63.3% (95% CI 46%–78%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 114 | 101/114 = 88.6% (95% CI 81%–93%) | 88/114 = 77.2% (95% CI 69%–84%) |
| mistral | 126 | 103/126 = 81.7% (95% CI 74%–88%) | 109/126 = 86.5% (95% CI 79%–91%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| test | 240 | 204/240 = 85.0% (95% CI 80%–89%) | 197/240 = 82.1% (95% CI 77%–86%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 156 | 132/156 = 84.6% (95% CI 78%–89%) | 119/156 = 76.3% (95% CI 69%–82%) |
| reviewed | 84 | 72/84 = 85.7% (95% CI 77%–92%) | 78/84 = 92.9% (95% CI 85%–97%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 240 | 204/240 = 85.0% (95% CI 80%–89%) | 197/240 = 82.1% (95% CI 77%–86%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-002 | clear-cut | reportable T24 clear-cut | reportable T3 clear-cut | death, serious_injury | 3/3 |
| CL-011 | clear-cut | reportable T24 clear-cut | reportable T3 clear-cut | death, serious_injury, env_effect, release | 3/3 |
| CL-015 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | env_effect, through_pipe_body_or_weld, other_beyond_design | 3/3 |
| CL-017 | clear-cut | reportable T3 clear-cut | precautionary T3 clear-cut | discovered_at, fire_or_explosion, release | 3/3 |
| CL-027 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | lands, other_beyond_design | 1/3 |
| CL-028 | clear-cut | reportable T24 clear-cut | reportable T3 clear-cut | death, serious_injury, release | 1/3 |
| CL-032 | clear-cut | reportable T24 clear-cut | reportable T3 clear-cut | release, other_beyond_design | 3/3 |
| CL-047 | clear-cut | reportable T24 clear-cut | precautionary T3 clear-cut | fire_or_explosion, release | 3/3 |
| CL-059 | clear-cut | reportable T24 clear-cut | reportable T3 clear-cut | death, release | 3/3 |
| NO-079 | not-reportable | not reportable None clear-cut | precautionary T3 clear-cut | env_effect, release | 3/3 |
| NO-086 | not-reportable | not reportable None clear-cut | precautionary T3 clear-cut | release | 3/3 |
| NO-087 | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | fire_linked_to_pipeline | 3/3 |
| JU-092 | judgment | precautionary T24 judgment | reportable T24 clear-cut | other_beyond_design | 3/3 |
| JU-094 | judgment | precautionary T24 judgment | reportable T24 clear-cut | lands, other_beyond_design | 3/3 |
| JU-096 | judgment | precautionary T24 judgment | reportable T24 clear-cut | through_pipe_body_or_weld, other_beyond_design | 3/3 |
| JU-128 | judgment | reportable T3 judgment | reportable T24 clear-cut | point:lands | 3/3 |
| JU-129 | judgment | reportable T3 judgment | reportable T3 clear-cut | env_effect, point:lands | 3/3 |
| JU-137 | judgment | precautionary T24 judgment | not reportable None clear-cut | lands, point:volume_m3 | 1/3 |
| AD-148 | adversarial | reportable T24 clear-cut | reportable T3 clear-cut | release | 3/3 |
| AD-153 | adversarial | reportable T24 clear-cut | precautionary T3 clear-cut | death, serious_injury, env_effect, fire_or_explosion, release | 3/3 |
| CL-001 | clear-cut | reportable T24 clear-cut | reportable T3 clear-cut | release | 2/3 |
| CL-029 | clear-cut | reportable T24 clear-cut | not reportable None clear-cut | fire_linked_to_pipeline | 2/3 |
| CL-074 | clear-cut | reportable T24 clear-cut | reportable T3 clear-cut | death, serious_injury, env_effect, release | 2/3 |
| JU-099 | judgment | precautionary T3 judgment | precautionary T3 clear-cut | release | 2/3 |
| NO-164 | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | other_beyond_design | 2/3 |
