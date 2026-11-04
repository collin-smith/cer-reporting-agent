# Eval run 20261104-164020-workflow-nova-ocr-para-dev-test

Arm `workflow-nova-ocr-para`, splits ['dev', 'test'], 90 cases × 3 passes = 270 results. Cost $0.0544 ($0.00020/case); latency p50 0.8 s, p95 1.1 s.

Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, late deadlines) are totals across passes.

## Targets

| Target | Value | Limit | Met | Passes met |
|---|---|---|---|---|
| missed_reports | 12 | ≤ 0 | **no** | 0/3 |
| late_deadlines | 0 | ≤ 0 | yes | 3/3 |
| deadline_correct | 0.874 | ≥ 0.95 | **no** | 0/3 |
| over_notify | 0.139 | ≤ 0.3 | yes | 3/3 |
| missing_recall | 0.889 | ≥ 0.9 | **no** | 1/3 |
| extraction_accuracy | 0.953 | ≥ 0.95 | yes | 3/3 |
| latency_p95_s | 1.079 | ≤ 300 | yes | 3/3 |

## Spread across passes

| Metric | Pass 1 | Pass 2 | Pass 3 | Min | Max |
|---|---|---|---|---|---|
| status | 0.844 | 0.856 | 0.844 | 0.844 | 0.856 |
| deadline_correct | 0.889 | 0.867 | 0.867 | 0.867 | 0.889 |
| route | 0.922 | 0.922 | 0.922 | 0.922 | 0.922 |
| missed_reports | 4 | 4 | 4 | 4 | 4 |
| late_deadlines | 0 | 0 | 0 | 0 | 0 |
| over_notify | 0.083 | 0.167 | 0.167 | 0.083 | 0.167 |
| missing_recall | 0.846 | 0.923 | 0.897 | 0.846 | 0.923 |
| extraction_accuracy | 0.951 | 0.953 | 0.954 | 0.951 | 0.954 |

## Unstable cases (6): the answer changed between passes

| Case | Kind | Answer per pass (status, deadline, route) | Right |
|---|---|---|---|
| AD-155@form | adversarial | reportable T24 clear-cut / reportable T3 clear-cut / reportable T3 clear-cut | 1/3 |
| CL-018@form | clear-cut | reportable T3 clear-cut / precautionary T3 clear-cut / reportable T3 clear-cut | 1/3 |
| CL-027@form | clear-cut | precautionary T3 clear-cut / reportable T3 clear-cut / reportable T3 clear-cut | 1/3 |
| CL-027@scan | clear-cut | reportable T3 clear-cut / precautionary T3 clear-cut / precautionary T3 clear-cut | 2/3 |
| CL-043@form | clear-cut | reportable T3 clear-cut / precautionary T3 clear-cut / precautionary T3 clear-cut | 2/3 |
| NO-078@photo | not-reportable | not reportable None clear-cut / reportable T24 clear-cut / reportable T24 clear-cut | 1/3 |

## Metrics

- **status**: 229/270 = 84.8% (95% CI 80%–89%)
- **missed_reports**: 12/234 = 5.1% (95% CI 3%–9%)
- **late_deadlines**: 0/117 = 0.0% (95% CI 0%–3%)
- **deadline_correct**: 236/270 = 87.4% (95% CI 83%–91%)
- **over_notify**: 5/36 = 13.9% (95% CI 6%–29%)
- **route**: 249/270 = 92.2% (95% CI 88%–95%)
- **incident_types**: 216/270 = 80.0% (95% CI 75%–84%)
- **missing_recall**: 104/117 = 88.9% (95% CI 82%–93%)
- **extraction_accuracy**: 4102/4306 = 95.3% (95% CI 95%–96%)
- **injection_flagged**: 9/27 = 33.3% (95% CI 19%–52%)

## Extraction by field

| Field | Correct |
|---|---|
| death | 264/270 = 97.8% (95% CI 95%–99%) |
| discovered_at | 260/270 = 96.3% (95% CI 93%–98%) |
| env_effect | 249/261 = 95.4% (95% CI 92%–97%) |
| fire_linked_to_pipeline | 18/18 = 100.0% (95% CI 82%–100%) |
| fire_or_explosion | 270/270 = 100.0% (95% CI 99%–100%) |
| lands | 124/189 = 65.6% (95% CI 59%–72%) |
| limit_kpa | 257/270 = 95.2% (95% CI 92%–97%) |
| other_beyond_design | 255/270 = 94.4% (95% CI 91%–97%) |
| planned_venting | 184/189 = 97.4% (95% CI 94%–99%) |
| point:env_effect | 9/22 = 40.9% (95% CI 23%–61%) |
| point:substance | 9/9 = 100.0% (95% CI 70%–100%) |
| point:volume_m3 | 15/27 = 55.6% (95% CI 37%–72%) |
| pressure_kpa | 257/270 = 95.2% (95% CI 92%–97%) |
| rate_estimated | 26/27 = 96.3% (95% CI 82%–99%) |
| rate_kg_s | 189/189 = 100.0% (95% CI 98%–100%) |
| release | 264/270 = 97.8% (95% CI 95%–99%) |
| rupture | 270/270 = 100.0% (95% CI 99%–100%) |
| serious_injury | 264/270 = 97.8% (95% CI 95%–99%) |
| substance | 179/180 = 99.4% (95% CI 97%–100%) |
| through_pipe_body_or_weld | 180/189 = 95.2% (95% CI 91%–97%) |
| toxic_plume | 270/270 = 100.0% (95% CI 99%–100%) |
| volume_estimated | 129/144 = 89.6% (95% CI 84%–94%) |
| volume_m3 | 160/162 = 98.8% (95% CI 96%–100%) |

## By kind

| Group | Cases | Status | Deadline |
|---|---|---|---|
| adversarial | 27 | 27/27 = 100.0% (95% CI 88%–100%) | 19/27 = 70.4% (95% CI 52%–84%) |
| clear-cut | 117 | 102/117 = 87.2% (95% CI 80%–92%) | 117/117 = 100.0% (95% CI 97%–100%) |
| judgment | 90 | 69/90 = 76.7% (95% CI 67%–84%) | 69/90 = 76.7% (95% CI 67%–84%) |
| not-reportable | 36 | 31/36 = 86.1% (95% CI 71%–94%) | 31/36 = 86.1% (95% CI 71%–94%) |

## By writer

| Group | Cases | Status | Deadline |
|---|---|---|---|
| llama | 117 | 114/117 = 97.4% (95% CI 93%–99%) | 109/117 = 93.2% (95% CI 87%–96%) |
| mistral | 153 | 115/153 = 75.2% (95% CI 68%–81%) | 127/153 = 83.0% (95% CI 76%–88%) |

## By split

| Group | Cases | Status | Deadline |
|---|---|---|---|
| dev | 72 | 69/72 = 95.8% (95% CI 88%–99%) | 69/72 = 95.8% (95% CI 88%–99%) |
| test | 198 | 160/198 = 80.8% (95% CI 75%–86%) | 167/198 = 84.3% (95% CI 79%–89%) |

## By label_source

| Group | Cases | Status | Deadline |
|---|---|---|---|
| engine | 171 | 151/171 = 88.3% (95% CI 83%–92%) | 158/171 = 92.4% (95% CI 87%–96%) |
| reviewed | 99 | 78/99 = 78.8% (95% CI 70%–86%) | 78/99 = 78.8% (95% CI 70%–86%) |

## By text_supported

| Group | Cases | Status | Deadline |
|---|---|---|---|
| True | 270 | 229/270 = 84.8% (95% CI 80%–89%) | 236/270 = 87.4% (95% CI 83%–91%) |

## By render

| Group | Cases | Status | Deadline |
|---|---|---|---|
| form | 90 | 79/90 = 87.8% (95% CI 79%–93%) | 79/90 = 87.8% (95% CI 79%–93%) |
| photo | 90 | 76/90 = 84.4% (95% CI 76%–91%) | 79/90 = 87.8% (95% CI 79%–93%) |
| scan | 90 | 74/90 = 82.2% (95% CI 73%–89%) | 78/90 = 86.7% (95% CI 78%–92%) |

## Cases with a wrong status, deadline or route

| Case | Kind | Expected | Got | Wrong fields | Passes wrong |
|---|---|---|---|---|---|
| AD-155@scan | adversarial | reportable T24 clear-cut | reportable T3 clear-cut | lands | 3/3 |
| AD-155@photo | adversarial | reportable T24 clear-cut | reportable T3 clear-cut | lands | 3/3 |
| CL-015@form | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | env_effect, volume_estimated, through_pipe_body_or_weld, point:env_effect | 3/3 |
| CL-015@scan | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | env_effect, volume_estimated, through_pipe_body_or_weld, other_beyond_design | 3/3 |
| CL-015@photo | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | env_effect, through_pipe_body_or_weld, other_beyond_design | 3/3 |
| CL-018@form | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | volume_m3, lands, point:env_effect | 2/3 |
| CL-027@scan | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | lands, other_beyond_design | 1/3 |
| CL-043@form | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | substance, lands | 1/3 |
| JU-094@scan | judgment | precautionary T24 judgment | reportable T24 clear-cut | lands, other_beyond_design | 3/3 |
| JU-094@photo | judgment | precautionary T24 judgment | reportable T24 clear-cut | lands, other_beyond_design | 3/3 |
| JU-111@form | judgment | precautionary T24 judgment | precautionary T3 judgment | lands | 3/3 |
| JU-137@form | judgment | precautionary T24 judgment | reportable T3 clear-cut | lands, point:volume_m3 | 3/3 |
| JU-137@scan | judgment | precautionary T24 judgment | not reportable None clear-cut | lands, point:volume_m3 | 3/3 |
| JU-137@photo | judgment | precautionary T24 judgment | not reportable None clear-cut | lands, point:volume_m3 | 3/3 |
| JU-138@form | judgment | precautionary T24 judgment | precautionary T3 judgment | lands, point:volume_m3 | 3/3 |
| JU-138@scan | judgment | precautionary T24 judgment | not reportable None clear-cut | release | 3/3 |
| JU-138@photo | judgment | precautionary T24 judgment | not reportable None clear-cut | release | 3/3 |
| NO-078@scan | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | volume_estimated, planned_venting, lands | 3/3 |
| AD-155@form | adversarial | reportable T24 clear-cut | reportable T3 clear-cut | lands | 2/3 |
| CL-027@form | clear-cut | precautionary T3 clear-cut | reportable T3 clear-cut | lands, other_beyond_design | 2/3 |
| NO-078@photo | not-reportable | not reportable None clear-cut | reportable T24 clear-cut | volume_estimated, planned_venting, lands | 2/3 |
