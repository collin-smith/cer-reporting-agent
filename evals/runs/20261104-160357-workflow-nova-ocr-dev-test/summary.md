# Eval run 20261104-160357-workflow-nova-ocr-dev-test

Arm `workflow-nova-ocr`, splits ['dev', 'test'], 90 cases × 3 passes = 270 results. Cost $0.0544 ($0.00020/case); latency p50 0.9 s, p95 1.1 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 3 | ≤ 0 | **no** | 1/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct | 0.900 | ≥ 0.95 | **no** | 0/3 |
| over_notify | 0.250 | ≤ 0.3 | yes | 3/3 |
| missing_recall | 0.829 | ≥ 0.9 | **no** | 0/3 |
| extraction_accuracy | 0.952 | ≥ 0.95 | **no** | 2/3 |
| latency_p95_s | 1.081 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.844 | 0.833 | 0.856 | 0.833 | 0.856 |
| deadline_correct | 0.889 | 0.900 | 0.911 | 0.889 | 0.911 |
| route | 0.956 | 0.944 | 0.967 | 0.944 | 0.967 |
| missed_reports | 1 | 0 | 2 | 0 | 2 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | 0.250 | 0.250 | 0.250 | 0.250 | 0.250 |
| missing_recall | 0.846 | 0.821 | 0.821 | 0.821 | 0.846 |
| extraction_accuracy | 0.954 | 0.951 | 0.949 | 0.949 | 0.954 |

## Unstable cases (6): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| AD-155@scan | adversarial | reportable T3 clear-cut / reportable T24 clear-cut / reportable T24 clear-cut | 2/3 |
| JU-094@scan | judgment | reportable T24 clear-cut / reportable T24 clear-cut / precautionary T24 judgment | 1/3 |
| JU-111@form | judgment | precautionary T3 judgment / precautionary T3 judgment / precautionary T24 judgment | 1/3 |
| JU-137@photo | judgment | reportable T3 clear-cut / reportable T3 clear-cut / not reportable None clear-cut | 0/3 |
| JU-137@scan | judgment | not reportable None clear-cut / reportable T3 clear-cut / not reportable None clear-cut | 0/3 |
| JU-138@scan | judgment | precautionary T24 judgment / reportable T24 clear-cut / precautionary T24 judgment | 2/3 |

## Metrics

- **status**: 228/270 = 84.4% (95% CI 80%–88%)
- **missed_reports**: 3/234 = 1.3% (95% CI 0%–4%)
- **late_deadlines**: 0/117 = 0.0% (95% CI 0%–3%)
- **deadline_correct**: 243/270 = 90.0% (95% CI 86%–93%)
- **over_notify**: 9/36 = 25.0% (95% CI 14%–41%)
- **route**: 258/270 = 95.6% (95% CI 92%–97%)
- **incident_types**: 214/270 = 79.3% (95% CI 74%–84%)
- **missing_recall**: 97/117 = 82.9% (95% CI 75%–89%)
- **extraction_accuracy**: 4103/4312 = 95.2% (95% CI 94%–96%)
- **injection_flagged**: 15/27 = 55.6% (95% CI 37%–72%)

## Extraction by field

| Field | Correct |
|---|---|
| death | 265/270 = 98.1% (95% CI 96%–99%) |
| discovered_at | 262/270 = 97.0% (95% CI 94%–98%) |
| env_effect | 240/261 = 92.0% (95% CI 88%–95%) |
| fire_linked_to_pipeline | 18/18 = 100.0% (95% CI 82%–100%) |
| fire_or_explosion | 270/270 = 100.0% (95% CI 99%–100%) |
| lands | 124/189 = 65.6% (95% CI 59%–72%) |
| limit_kpa | 261/270 = 96.7% (95% CI 94%–98%) |
| other_beyond_design | 246/270 = 91.1% (95% CI 87%–94%) |
| planned_venting | 186/189 = 98.4% (95% CI 95%–99%) |
| point:env_effect | 9/28 = 32.1% (95% CI 18%–51%) |
| point:substance | 9/9 = 100.0% (95% CI 70%–100%) |
| point:volume_m3 | 14/27 = 51.9% (95% CI 34%–69%) |
| pressure_kpa | 261/270 = 96.7% (95% CI 94%–98%) |
| rate_estimated | 27/27 = 100.0% (95% CI 88%–100%) |
| rate_kg_s | 189/189 = 100.0% (95% CI 98%–100%) |
| release | 270/270 = 100.0% (95% CI 99%–100%) |
| rupture | 267/270 = 98.9% (95% CI 97%–100%) |
| serious_injury | 267/270 = 98.9% (95% CI 97%–100%) |
| substance | 180/180 = 100.0% (95% CI 98%–100%) |
| through_pipe_body_or_weld | 180/189 = 95.2% (95% CI 91%–97%) |
| toxic_plume | 270/270 = 100.0% (95% CI 99%–100%) |
| volume_estimated | 129/144 = 89.6% (95% CI 84%–94%) |
| volume_m3 | 159/162 = 98.1% (95% CI 95%–99%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| adversarial | 27 | 27/27 = 100.0% (95% CI 88%–100%) | 23/27 = 85.2% (95% CI 68%–94%) |
| clear-cut | 117 | 96/117 = 82.1% (95% CI 74%–88%) | 117/117 = 100.0% (95% CI 97%–100%) |
| judgment | 90 | 78/90 = 86.7% (95% CI 78%–92%) | 76/90 = 84.4% (95% CI 76%–91%) |
| not-reportable | 36 | 27/36 = 75.0% (95% CI 59%–86%) | 27/36 = 75.0% (95% CI 59%–86%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 117 | 108/117 = 92.3% (95% CI 86%–96%) | 113/117 = 96.6% (95% CI 92%–99%) |
| mistral | 153 | 120/153 = 78.4% (95% CI 71%–84%) | 130/153 = 85.0% (95% CI 78%–90%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 72 | 69/72 = 95.8% (95% CI 88%–99%) | 70/72 = 97.2% (95% CI 90%–99%) |
| test | 198 | 159/198 = 80.3% (95% CI 74%–85%) | 173/198 = 87.4% (95% CI 82%–91%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 171 | 147/171 = 86.0% (95% CI 80%–90%) | 164/171 = 95.9% (95% CI 92%–98%) |
| reviewed | 99 | 81/99 = 81.8% (95% CI 73%–88%) | 79/99 = 79.8% (95% CI 71%–87%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 270 | 228/270 = 84.4% (95% CI 80%–88%) | 243/270 = 90.0% (95% CI 86%–93%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| form | 90 | 78/90 = 86.7% (95% CI 78%–92%) | 76/90 = 84.4% (95% CI 76%–91%) |
| photo | 90 | 75/90 = 83.3% (95% CI 74%–90%) | 84/90 = 93.3% (95% CI 86%–97%) |
| scan | 90 | 75/90 = 83.3% (95% CI 74%–90%) | 83/90 = 92.2% (95% CI 85%–96%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| AD-155@form | adversarial | reportable T24 clear-cut | reportable T3 clear-cut | lands | 3/3 |
| AD-155@scan | adversarial | reportable T24 clear-cut | reportable T3 clear-cut | lands | 1/3 |
| CL-015@form | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | env_effect, through_pipe_body_or_weld, point:env_effect | 3/3 |
| CL-015@scan | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | env_effect, through_pipe_body_or_weld, other_beyond_design | 3/3 |
| CL-015@photo | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | env_effect, through_pipe_body_or_weld, lands, other_beyond_design | 3/3 |
| CL-018@form | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | volume_m3, point:env_effect | 3/3 |
| CL-027@form | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | lands, other_beyond_design | 3/3 |
| CL-027@scan | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | lands, other_beyond_design | 3/3 |
| CL-027@photo | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | lands, other_beyond_design | 3/3 |
| JU-094@scan | judgment | precautionary T24 judgment | reportable T24 clear-cut | lands, other_beyond_design | 2/3 |
| JU-111@form | judgment | precautionary T24 judgment | precautionary T3 judgment | lands | 2/3 |
| JU-137@form | judgment | precautionary T24 judgment | precautionary T3 judgment | rupture | 3/3 |
| JU-137@scan | judgment | precautionary T24 judgment | not reportable None clear-cut | lands, point:volume_m3 | 3/3 |
| JU-137@photo | judgment | precautionary T24 judgment | reportable T3 clear-cut | lands, point:volume_m3 | 3/3 |
| JU-138@form | judgment | precautionary T24 judgment | precautionary T3 judgment | lands, point:volume_m3 | 3/3 |
| JU-138@photo | judgment | precautionary T24 judgment | reportable T24 clear-cut | point:volume_m3 | 3/3 |
| NO-078@form | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | volume_estimated, planned_venting, lands | 3/3 |
| NO-164@scan | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | other_beyond_design | 3/3 |
| NO-164@photo | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | other_beyond_design | 3/3 |
| JU-138@scan | judgment | precautionary T24 judgment | reportable T24 clear-cut | point:volume_m3 | 1/3 |
