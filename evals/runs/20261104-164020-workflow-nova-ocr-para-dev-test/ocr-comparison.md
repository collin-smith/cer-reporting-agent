# OCR vs. text: 20261104-164020-workflow-nova-ocr-para-dev-test

30 cases from dev and test, each rendered as a form PDF, a scan and a photo (D24); text rows from 20261104-163507-workflow-nova-test, 20261104-163007-workflow-nova-dev on the same cases. Extractor versions: 2c42fea8. Every pass pooled.

| Format | Results | Status | Deadline | Missed | Late | Extraction | Report words lost | Confidence |
|---|---|---|---|---|---|---|---|---|
| text | 90 | 86.7% | 95.6% | 3 | 0 | 96.7% | n/a | n/a |
| form | 90 | 87.8% | 87.8% | 0 | 0 | 94.7% | 0.0% | 99.7 |
| scan | 90 | 82.2% | 86.7% | 6 | 0 | 95.5% | 0.0% | 99.4 |
| photo | 90 | 84.4% | 87.8% | 6 | 0 | 95.6% | 0.0% | 99.3 |

## Fields that moved by 3 points or more against text

| Field | Text | form | scan | photo |
|---|---|---|---|---|
| env_effect | 96.6% | 93.1% | 96.6% | 96.6% |
| lands | 84.1% | 47.6% | 73.0% | 76.2% |
| other_beyond_design | 91.1% | 97.8% | 92.2% | 93.3% |
| planned_venting | 98.4% | 100.0% | 95.2% | 96.8% |
| point:env_effect | 50.0% | 30.0% | 50.0% | 50.0% |
| point:volume_m3 | 100.0% | 33.3% | 66.7% | 66.7% |
| rate_estimated | 100.0% | 88.9% | 100.0% | 100.0% |
| release | 96.7% | 100.0% | 96.7% | 96.7% |
| volume_estimated | 87.5% | 89.6% | 91.7% | 87.5% |
| volume_m3 | 100.0% | 96.3% | 100.0% | 100.0% |

## Most report words lost

| Render | Words lost |
|---|---|
| NO-164-scan.jpg | 0.0% |
| NO-164-photo.jpg | 0.0% |
| NO-164-form.pdf | 0.0% |
| NO-080-scan.jpg | 0.0% |
| NO-080-photo.jpg | 0.0% |
| NO-080-form.pdf | 0.0% |
| NO-078-scan.jpg | 0.0% |
| NO-078-photo.jpg | 0.0% |

## OCR results with a wrong status or deadline (55)

| Row | Pass | Expected | Got | Wrong fields |
|---|---|---|---|---|
| AD-155@form | 2 | reportable T24 | reportable T3 | lands |
| AD-155@form | 3 | reportable T24 | reportable T3 | lands |
| AD-155@photo | 1 | reportable T24 | reportable T3 | lands |
| AD-155@photo | 2 | reportable T24 | reportable T3 | lands |
| AD-155@photo | 3 | reportable T24 | reportable T3 | lands |
| AD-155@scan | 1 | reportable T24 | reportable T3 | lands |
| AD-155@scan | 2 | reportable T24 | reportable T3 | lands |
| AD-155@scan | 3 | reportable T24 | reportable T3 | lands |
| CL-015@form | 1 | precautionary T3 | reportable T3 | env_effect, volume_estimated, through_pipe_body_or_weld, point:env_effect |
| CL-015@form | 2 | precautionary T3 | reportable T3 | env_effect, volume_estimated, through_pipe_body_or_weld |
| CL-015@form | 3 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld |
| CL-015@photo | 1 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld, other_beyond_design |
| CL-015@photo | 2 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld, other_beyond_design |
| CL-015@photo | 3 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld, other_beyond_design |
| CL-015@scan | 1 | precautionary T3 | reportable T3 | env_effect, volume_estimated, through_pipe_body_or_weld, other_beyond_design |
| CL-015@scan | 2 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld, other_beyond_design |
| CL-015@scan | 3 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld, other_beyond_design |
| CL-018@form | 1 | precautionary T3 | reportable T3 | volume_m3, lands, point:env_effect |
| CL-018@form | 3 | precautionary T3 | reportable T3 | volume_m3, lands, point:env_effect |
| CL-027@form | 2 | precautionary T3 | reportable T3 | lands, other_beyond_design |
| CL-027@form | 3 | precautionary T3 | reportable T3 | lands, other_beyond_design |
| CL-027@scan | 1 | precautionary T3 | reportable T3 | lands, other_beyond_design |
| CL-043@form | 1 | precautionary T3 | reportable T3 | substance, lands |
| JU-094@photo | 1 | precautionary T24 | reportable T24 | lands, other_beyond_design |
| JU-094@photo | 2 | precautionary T24 | reportable T24 | lands, other_beyond_design |
| JU-094@photo | 3 | precautionary T24 | reportable T24 | lands, other_beyond_design |
| JU-094@scan | 1 | precautionary T24 | reportable T24 | lands, other_beyond_design |
| JU-094@scan | 2 | precautionary T24 | reportable T24 | lands, other_beyond_design |
| JU-094@scan | 3 | precautionary T24 | reportable T24 | lands, other_beyond_design |
| JU-111@form | 1 | precautionary T24 | precautionary T3 | lands |
| JU-111@form | 2 | precautionary T24 | precautionary T3 | lands |
| JU-111@form | 3 | precautionary T24 | precautionary T3 | lands |
| JU-137@form | 1 | precautionary T24 | reportable T3 | lands, point:volume_m3 |
| JU-137@form | 2 | precautionary T24 | reportable T3 | lands, point:volume_m3 |
| JU-137@form | 3 | precautionary T24 | reportable T3 | lands, point:volume_m3 |
| JU-137@photo | 1 | precautionary T24 | not reportable None | lands, point:volume_m3 |
| JU-137@photo | 2 | precautionary T24 | not reportable None | lands, point:volume_m3 |
| JU-137@photo | 3 | precautionary T24 | not reportable None | lands, point:volume_m3 |
| JU-137@scan | 1 | precautionary T24 | not reportable None | lands, point:volume_m3 |
| JU-137@scan | 2 | precautionary T24 | not reportable None | lands, point:volume_m3 |
| JU-137@scan | 3 | precautionary T24 | not reportable None | lands, point:volume_m3 |
| JU-138@form | 1 | precautionary T24 | precautionary T3 | lands, point:volume_m3 |
| JU-138@form | 2 | precautionary T24 | precautionary T3 | lands, point:volume_m3 |
| JU-138@form | 3 | precautionary T24 | precautionary T3 | lands, point:volume_m3 |
| JU-138@photo | 1 | precautionary T24 | not reportable None | release |
| JU-138@photo | 2 | precautionary T24 | not reportable None | release |
| JU-138@photo | 3 | precautionary T24 | not reportable None | release |
| JU-138@scan | 1 | precautionary T24 | not reportable None | release |
| JU-138@scan | 2 | precautionary T24 | not reportable None | release |
| JU-138@scan | 3 | precautionary T24 | not reportable None | release |
| NO-078@photo | 2 | not reportable None | reportable T24 | volume_estimated, planned_venting, lands |
| NO-078@photo | 3 | not reportable None | reportable T24 | volume_estimated, planned_venting, lands |
| NO-078@scan | 1 | not reportable None | reportable T24 | volume_estimated, planned_venting, lands |
| NO-078@scan | 2 | not reportable None | reportable T24 | volume_estimated, planned_venting, lands |
| NO-078@scan | 3 | not reportable None | reportable T24 | volume_estimated, planned_venting, lands |
