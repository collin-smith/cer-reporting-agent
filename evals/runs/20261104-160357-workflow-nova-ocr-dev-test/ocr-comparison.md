# OCR vs. text: 20261104-160357-workflow-nova-ocr-dev-test

30 cases from dev and test, each rendered as a form PDF, a scan and a photo (D24); text rows from 20261103-174404-workflow-nova-test, 20261103-173717-workflow-nova-dev on the same cases. Extractor versions: 4968c49f. Every pass pooled.

| Format | Results | Status | Deadline | Missed | Late | Extraction | Report words lost | Confidence |
|---|---|---|---|---|---|---|---|---|
| text | 90 | 93.3% | 98.9% | 0 | 0 | 96.9% | n/a | n/a |
| form | 90 | 86.7% | 84.4% | 0 | 0 | 94.5% | 0.0% | 99.7 |
| scan | 90 | 83.3% | 92.2% | 2 | 0 | 95.5% | 0.0% | 99.4 |
| photo | 90 | 83.3% | 93.3% | 1 | 0 | 95.4% | 0.0% | 99.3 |

## Fields that moved by 3 points or more against text

| Field | Text | form | scan | photo |
|---|---|---|---|---|
| env_effect | 96.6% | 90.8% | 92.0% | 93.1% |
| lands | 84.1% | 50.8% | 74.6% | 71.4% |
| other_beyond_design | 93.3% | 95.6% | 87.8% | 90.0% |
| planned_venting | 100.0% | 95.2% | 100.0% | 100.0% |
| point:env_effect | 50.0% | 27.3% | 37.5% | 33.3% |
| point:volume_m3 | 100.0% | 66.7% | 55.6% | 33.3% |
| rupture | 100.0% | 96.7% | 100.0% | 100.0% |
| volume_estimated | 87.5% | 91.7% | 89.6% | 87.5% |
| volume_m3 | 100.0% | 94.4% | 100.0% | 100.0% |

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

## OCR results with a wrong status or deadline (54)

| Row | Pass | Expected | Got | Wrong fields |
|---|---|---|---|---|
| AD-155@form | 1 | reportable T24 | reportable T3 | lands |
| AD-155@form | 2 | reportable T24 | reportable T3 | lands |
| AD-155@form | 3 | reportable T24 | reportable T3 | lands |
| AD-155@scan | 1 | reportable T24 | reportable T3 | lands |
| CL-015@form | 1 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld, point:env_effect |
| CL-015@form | 2 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld, point:env_effect |
| CL-015@form | 3 | precautionary T3 | reportable T3 | env_effect, volume_estimated, through_pipe_body_or_weld, other_beyond_design |
| CL-015@photo | 1 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld, lands, other_beyond_design |
| CL-015@photo | 2 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld, lands, other_beyond_design |
| CL-015@photo | 3 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld, lands, other_beyond_design |
| CL-015@scan | 1 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld, other_beyond_design |
| CL-015@scan | 2 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld, lands, other_beyond_design |
| CL-015@scan | 3 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld, lands, other_beyond_design |
| CL-018@form | 1 | precautionary T3 | reportable T3 | volume_m3, point:env_effect |
| CL-018@form | 2 | precautionary T3 | reportable T3 | volume_m3, lands, point:env_effect |
| CL-018@form | 3 | precautionary T3 | reportable T3 | volume_m3, lands, point:env_effect |
| CL-027@form | 1 | precautionary T3 | reportable T3 | lands, other_beyond_design |
| CL-027@form | 2 | precautionary T3 | reportable T3 | lands, other_beyond_design |
| CL-027@form | 3 | precautionary T3 | reportable T3 | lands, other_beyond_design |
| CL-027@photo | 1 | precautionary T3 | reportable T3 | lands, other_beyond_design |
| CL-027@photo | 2 | precautionary T3 | reportable T3 | lands, other_beyond_design |
| CL-027@photo | 3 | precautionary T3 | reportable T3 | lands, other_beyond_design |
| CL-027@scan | 1 | precautionary T3 | reportable T3 | lands, other_beyond_design |
| CL-027@scan | 2 | precautionary T3 | reportable T3 | lands, other_beyond_design |
| CL-027@scan | 3 | precautionary T3 | reportable T3 | lands, other_beyond_design |
| JU-094@scan | 1 | precautionary T24 | reportable T24 | lands, other_beyond_design |
| JU-094@scan | 2 | precautionary T24 | reportable T24 | lands, other_beyond_design |
| JU-111@form | 1 | precautionary T24 | precautionary T3 | lands |
| JU-111@form | 2 | precautionary T24 | precautionary T3 | lands |
| JU-137@form | 1 | precautionary T24 | precautionary T3 | rupture |
| JU-137@form | 2 | precautionary T24 | precautionary T3 | rupture |
| JU-137@form | 3 | precautionary T24 | precautionary T3 | rupture |
| JU-137@photo | 1 | precautionary T24 | reportable T3 | lands, point:volume_m3 |
| JU-137@photo | 2 | precautionary T24 | reportable T3 | lands, point:volume_m3 |
| JU-137@photo | 3 | precautionary T24 | not reportable None | lands, point:volume_m3 |
| JU-137@scan | 1 | precautionary T24 | not reportable None | lands, point:volume_m3 |
| JU-137@scan | 2 | precautionary T24 | reportable T3 | lands, point:volume_m3 |
| JU-137@scan | 3 | precautionary T24 | not reportable None | lands, point:volume_m3 |
| JU-138@form | 1 | precautionary T24 | precautionary T3 | lands, point:volume_m3 |
| JU-138@form | 2 | precautionary T24 | precautionary T3 | lands, point:volume_m3 |
| JU-138@form | 3 | precautionary T24 | precautionary T3 | lands, point:volume_m3 |
| JU-138@photo | 1 | precautionary T24 | reportable T24 | point:volume_m3 |
| JU-138@photo | 2 | precautionary T24 | reportable T24 | point:volume_m3 |
| JU-138@photo | 3 | precautionary T24 | reportable T24 | point:volume_m3 |
| JU-138@scan | 2 | precautionary T24 | reportable T24 | point:volume_m3 |
| NO-078@form | 1 | not reportable None | reportable T24 | volume_estimated, planned_venting, lands |
| NO-078@form | 2 | not reportable None | reportable T24 | volume_estimated, planned_venting, lands |
| NO-078@form | 3 | not reportable None | reportable T24 | volume_estimated, planned_venting, lands |
| NO-164@photo | 1 | not reportable None | reportable T24 | other_beyond_design |
| NO-164@photo | 2 | not reportable None | reportable T24 | other_beyond_design |
| NO-164@photo | 3 | not reportable None | reportable T24 | other_beyond_design |
| NO-164@scan | 1 | not reportable None | reportable T24 | other_beyond_design |
| NO-164@scan | 2 | not reportable None | reportable T24 | other_beyond_design |
| NO-164@scan | 3 | not reportable None | reportable T24 | other_beyond_design |
