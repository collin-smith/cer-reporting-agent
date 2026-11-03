# Eval run 20261103-173853-workflow-nova-test

Arm `workflow-nova`, splits ['test'], 80 cases × 3 passes = 240 results. Cost $0.0480 ($0.00020/case); latency p50 0.8 s, p95 0.9 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 2 | ≤ 0 | **no** | 1/3 |
| late_deadlines | 6 | ≤ 0 | **no** | 0/3 |
| deadline_correct | 0.958 | ≥ 0.95 | yes | 3/3 |
| over_notify | 0.067 | ≤ 0.3 | yes | 3/3 |
| missing_recall | 0.923 | ≥ 0.9 | yes | 3/3 |
| extraction_accuracy | 0.965 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s | 0.946 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.925 | 0.938 | 0.925 | 0.925 | 0.938 |
| deadline_correct | 0.963 | 0.963 | 0.950 | 0.950 | 0.963 |
| route | 0.938 | 0.950 | 0.938 | 0.938 | 0.950 |
| missed_reports | 1 | 0 | 1 | 0 | 1 |
| late_deadlines | 2 | 2 | 2 | 2 | 2 |
| over_notify | 0.000 | 0.100 | 0.100 | 0.000 | 0.100 |
| missing_recall | 0.923 | 0.923 | 0.923 | 0.923 | 0.923 |
| extraction_accuracy | 0.962 | 0.967 | 0.966 | 0.962 | 0.967 |

## Unstable cases (3): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| CL-027 | clear-cut | reportable T3 clear-cut / precautionary T3 clear-cut / precautionary T3 clear-cut | 2/3 |
| JU-137 | judgment | not reportable None clear-cut / precautionary T24 judgment / not reportable None clear-cut | 1/3 |
| NO-087 | not-reportable | not reportable None clear-cut / reportable T24 clear-cut / reportable T24 clear-cut | 1/3 |

## Metrics

- **status**: 223/240 = 92.9% (95% CI 89%–96%)
- **missed_reports**: 2/210 = 1.0% (95% CI 0%–3%)
- **late_deadlines**: 6/114 = 5.3% (95% CI 2%–11%)
- **deadline_correct**: 230/240 = 95.8% (95% CI 93%–98%)
- **over_notify**: 2/30 = 6.7% (95% CI 2%–21%)
- **route**: 226/240 = 94.2% (95% CI 90%–96%)
- **incident_types**: 206/240 = 85.8% (95% CI 81%–90%)
- **missing_recall**: 72/78 = 92.3% (95% CI 84%–96%)
- **extraction_accuracy**: 3546/3676 = 96.5% (95% CI 96%–97%)
- **injection_flagged**: 9/30 = 30.0% (95% CI 17%–48%)

## Extraction by field

| Field | Correct |
|---|---|
| death | 237/240 = 98.8% (95% CI 96%–100%) |
| discovered_at | 228/240 = 95.0% (95% CI 91%–97%) |
| env_effect | 217/234 = 92.7% (95% CI 89%–95%) |
| fire_linked_to_pipeline | 51/54 = 94.4% (95% CI 85%–98%) |
| fire_or_explosion | 239/240 = 99.6% (95% CI 98%–100%) |
| lands | 93/126 = 73.8% (95% CI 66%–81%) |
| limit_kpa | 234/240 = 97.5% (95% CI 95%–99%) |
| other_beyond_design | 224/240 = 93.3% (95% CI 89%–96%) |
| planned_venting | 141/141 = 100.0% (95% CI 97%–100%) |
| point:env_effect | 6/10 = 60.0% (95% CI 31%–83%) |
| point:lands | 12/15 = 80.0% (95% CI 55%–93%) |
| point:serious_injury | 3/3 = 100.0% (95% CI 44%–100%) |
| point:substance | 9/9 = 100.0% (95% CI 70%–100%) |
| point:volume_m3 | 7/9 = 77.8% (95% CI 45%–94%) |
| pressure_kpa | 234/240 = 97.5% (95% CI 95%–99%) |
| rate_estimated | 9/9 = 100.0% (95% CI 70%–100%) |
| rate_kg_s | 141/141 = 100.0% (95% CI 97%–100%) |
| release | 240/240 = 100.0% (95% CI 98%–100%) |
| rupture | 240/240 = 100.0% (95% CI 98%–100%) |
| serious_injury | 234/237 = 98.7% (95% CI 96%–100%) |
| substance | 132/132 = 100.0% (95% CI 97%–100%) |
| through_pipe_body_or_weld | 135/141 = 95.7% (95% CI 91%–98%) |
| toxic_plume | 234/240 = 97.5% (95% CI 95%–99%) |
| volume_estimated | 114/123 = 92.7% (95% CI 87%–96%) |
| volume_m3 | 132/132 = 100.0% (95% CI 97%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| adversarial | 30 | 30/30 = 100.0% (95% CI 89%–100%) | 27/30 = 90.0% (95% CI 74%–97%) |
| clear-cut | 102 | 98/102 = 96.1% (95% CI 90%–98%) | 99/102 = 97.1% (95% CI 92%–99%) |
| judgment | 78 | 67/78 = 85.9% (95% CI 76%–92%) | 76/78 = 97.4% (95% CI 91%–99%) |
| not-reportable | 30 | 28/30 = 93.3% (95% CI 79%–98%) | 28/30 = 93.3% (95% CI 79%–98%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 114 | 113/114 = 99.1% (95% CI 95%–100%) | 114/114 = 100.0% (95% CI 97%–100%) |
| mistral | 126 | 110/126 = 87.3% (95% CI 80%–92%) | 116/126 = 92.1% (95% CI 86%–96%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| test | 240 | 223/240 = 92.9% (95% CI 89%–96%) | 230/240 = 95.8% (95% CI 93%–98%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 156 | 150/156 = 96.2% (95% CI 92%–98%) | 148/156 = 94.9% (95% CI 90%–97%) |
| reviewed | 84 | 73/84 = 86.9% (95% CI 78%–93%) | 82/84 = 97.6% (95% CI 92%–99%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 240 | 223/240 = 92.9% (95% CI 89%–96%) | 230/240 = 95.8% (95% CI 93%–98%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| CL-008 | clear-cut | reportable T3 clear-cut | reportable T24 clear-cut | toxic_plume | 3/3 |
| CL-015 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | env_effect, through_pipe_body_or_weld, lands, other_beyond_design | 3/3 |
| CL-027 | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | lands, other_beyond_design | 1/3 |
| JU-092 | judgment | precautionary T24 judgment | reportable T24 clear-cut | other_beyond_design | 3/3 |
| JU-094 | judgment | precautionary T24 judgment | reportable T24 clear-cut | lands, other_beyond_design | 3/3 |
| JU-096 | judgment | precautionary T24 judgment | reportable T24 clear-cut | through_pipe_body_or_weld, other_beyond_design | 3/3 |
| JU-129 | judgment | reportable T3 judgment | reportable T3 clear-cut | env_effect, point:lands | 3/3 |
| JU-137 | judgment | precautionary T24 judgment | not reportable None clear-cut | lands, point:volume_m3 | 2/3 |
| AD-151 | adversarial | reportable T3 clear-cut | reportable T24 clear-cut | toxic_plume | 3/3 |
| NO-087 | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | fire_linked_to_pipeline | 2/3 |
