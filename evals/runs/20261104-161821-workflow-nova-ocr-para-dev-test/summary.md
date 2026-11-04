# Eval run 20261104-161821-workflow-nova-ocr-para-dev-test

Arm `workflow-nova-ocr-para`, splits ['dev', 'test'], 90 cases × 3 passes = 270 results. Cost $0.0542 ($0.00020/case); latency p50 0.8 s, p95 1.0 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 6 | ≤ 0 | **no** | 0/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct | 0.915 | ≥ 0.95 | **no** | 0/3 |
| over_notify | 0.250 | ≤ 0.3 | **no** | 2/3 |
| missing_recall | 0.880 | ≥ 0.9 | **no** | 0/3 |
| extraction_accuracy | 0.956 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s | 1.008 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.889 | 0.889 | 0.878 | 0.878 | 0.889 |
| deadline_correct | 0.933 | 0.911 | 0.900 | 0.900 | 0.933 |
| route | 0.956 | 0.956 | 0.956 | 0.956 | 0.956 |
| missed_reports | 2 | 2 | 2 | 2 | 2 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | 0.167 | 0.250 | 0.333 | 0.167 | 0.333 |
| missing_recall | 0.897 | 0.872 | 0.872 | 0.872 | 0.897 |
| extraction_accuracy | 0.958 | 0.956 | 0.955 | 0.955 | 0.958 |

## Unstable cases (6): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| CL-027@scan | clear-cut | reportable T3 clear-cut / precautionary T3 clear-cut / precautionary T3 clear-cut | 2/3 |
| JU-110@form | judgment | precautionary T24 judgment / precautionary T3 judgment / precautionary T3 judgment | 1/3 |
| NO-078@form | not-reportable | reportable T24 clear-cut / not reportable None clear-cut / not reportable None clear-cut | 2/3 |
| NO-078@scan | not-reportable | not reportable None clear-cut / not reportable None clear-cut / reportable T24 clear-cut | 2/3 |
| NO-164@photo | not-reportable | not reportable None clear-cut / reportable T24 clear-cut / reportable T24 clear-cut | 1/3 |
| NO-164@scan | not-reportable | not reportable None clear-cut / reportable T24 clear-cut / reportable T24 clear-cut | 1/3 |

## Metrics

- **status**: 239/270 = 88.5% (95% CI 84%–92%)
- **missed_reports**: 6/234 = 2.6% (95% CI 1%–5%)
- **late_deadlines**: 0/117 = 0.0% (95% CI 0%–3%)
- **deadline_correct**: 247/270 = 91.5% (95% CI 88%–94%)
- **over_notify**: 9/36 = 25.0% (95% CI 14%–41%)
- **route**: 258/270 = 95.6% (95% CI 92%–97%)
- **incident_types**: 216/270 = 80.0% (95% CI 75%–84%)
- **missing_recall**: 103/117 = 88.0% (95% CI 81%–93%)
- **extraction_accuracy**: 4121/4310 = 95.6% (95% CI 95%–96%)
- **injection_flagged**: 15/27 = 55.6% (95% CI 37%–72%)

## Extraction by field

| Field | Correct |
|---|---|
| death | 265/270 = 98.1% (95% CI 96%–99%) |
| discovered_at | 263/270 = 97.4% (95% CI 95%–99%) |
| env_effect | 240/261 = 92.0% (95% CI 88%–95%) |
| fire_linked_to_pipeline | 18/18 = 100.0% (95% CI 82%–100%) |
| fire_or_explosion | 270/270 = 100.0% (95% CI 99%–100%) |
| lands | 125/189 = 66.1% (95% CI 59%–73%) |
| limit_kpa | 261/270 = 96.7% (95% CI 94%–98%) |
| other_beyond_design | 253/270 = 93.7% (95% CI 90%–96%) |
| planned_venting | 184/189 = 97.4% (95% CI 94%–99%) |
| point:env_effect | 9/26 = 34.6% (95% CI 19%–54%) |
| point:substance | 9/9 = 100.0% (95% CI 70%–100%) |
| point:volume_m3 | 21/27 = 77.8% (95% CI 59%–89%) |
| pressure_kpa | 261/270 = 96.7% (95% CI 94%–98%) |
| rate_estimated | 27/27 = 100.0% (95% CI 88%–100%) |
| rate_kg_s | 189/189 = 100.0% (95% CI 98%–100%) |
| release | 270/270 = 100.0% (95% CI 99%–100%) |
| rupture | 270/270 = 100.0% (95% CI 99%–100%) |
| serious_injury | 265/270 = 98.1% (95% CI 96%–99%) |
| substance | 180/180 = 100.0% (95% CI 98%–100%) |
| through_pipe_body_or_weld | 180/189 = 95.2% (95% CI 91%–97%) |
| toxic_plume | 270/270 = 100.0% (95% CI 99%–100%) |
| volume_estimated | 129/144 = 89.6% (95% CI 84%–94%) |
| volume_m3 | 162/162 = 100.0% (95% CI 98%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| adversarial | 27 | 27/27 = 100.0% (95% CI 88%–100%) | 24/27 = 88.9% (95% CI 72%–96%) |
| clear-cut | 117 | 107/117 = 91.5% (95% CI 85%–95%) | 117/117 = 100.0% (95% CI 97%–100%) |
| judgment | 90 | 78/90 = 86.7% (95% CI 78%–92%) | 79/90 = 87.8% (95% CI 79%–93%) |
| not-reportable | 36 | 27/36 = 75.0% (95% CI 59%–86%) | 27/36 = 75.0% (95% CI 59%–86%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 117 | 116/117 = 99.1% (95% CI 95%–100%) | 112/117 = 95.7% (95% CI 90%–98%) |
| mistral | 153 | 123/153 = 80.4% (95% CI 73%–86%) | 135/153 = 88.2% (95% CI 82%–92%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 72 | 72/72 = 100.0% (95% CI 95%–100%) | 70/72 = 97.2% (95% CI 90%–99%) |
| test | 198 | 167/198 = 84.3% (95% CI 79%–89%) | 177/198 = 89.4% (95% CI 84%–93%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 171 | 156/171 = 91.2% (95% CI 86%–95%) | 163/171 = 95.3% (95% CI 91%–98%) |
| reviewed | 99 | 83/99 = 83.8% (95% CI 75%–90%) | 84/99 = 84.8% (95% CI 76%–91%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 270 | 239/270 = 88.5% (95% CI 84%–92%) | 247/270 = 91.5% (95% CI 88%–94%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| form | 90 | 86/90 = 95.6% (95% CI 89%–98%) | 81/90 = 90.0% (95% CI 82%–95%) |
| photo | 90 | 76/90 = 84.4% (95% CI 76%–91%) | 82/90 = 91.1% (95% CI 83%–95%) |
| scan | 90 | 77/90 = 85.6% (95% CI 77%–91%) | 84/90 = 93.3% (95% CI 86%–97%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| AD-155@form | adversarial | reportable T24 clear-cut | reportable T3 clear-cut | lands | 3/3 |
| CL-015@form | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | env_effect, volume_estimated, through_pipe_body_or_weld | 3/3 |
| CL-015@scan | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | env_effect, through_pipe_body_or_weld, other_beyond_design | 3/3 |
| CL-015@photo | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | env_effect, through_pipe_body_or_weld, lands, other_beyond_design | 3/3 |
| CL-027@scan | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | lands, other_beyond_design | 1/3 |
| JU-094@scan | judgment | precautionary T24 judgment | reportable T24 clear-cut | lands, other_beyond_design | 3/3 |
| JU-094@photo | judgment | precautionary T24 judgment | reportable T24 clear-cut | lands, other_beyond_design | 3/3 |
| JU-137@scan | judgment | precautionary T24 judgment | not reportable None clear-cut | lands, point:volume_m3 | 3/3 |
| JU-137@photo | judgment | precautionary T24 judgment | not reportable None clear-cut | lands, point:volume_m3 | 3/3 |
| JU-138@form | judgment | precautionary T24 judgment | precautionary T3 judgment | lands | 3/3 |
| NO-078@form | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | volume_estimated, planned_venting, lands | 1/3 |
| NO-078@photo | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | volume_estimated, planned_venting, lands | 3/3 |
| JU-110@form | judgment | precautionary T24 judgment | precautionary T3 judgment | lands | 2/3 |
| NO-164@scan | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | other_beyond_design | 2/3 |
| NO-164@photo | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | other_beyond_design | 2/3 |
| NO-078@scan | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | volume_estimated, planned_venting, lands | 1/3 |
