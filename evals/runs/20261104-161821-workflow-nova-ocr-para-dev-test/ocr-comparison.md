# OCR vs. text: 20261104-161821-workflow-nova-ocr-para-dev-test

30 cases from dev and test, each rendered as a form PDF, a scan and a photo (D24); text rows from 20261103-174404-workflow-nova-test, 20261103-173717-workflow-nova-dev on the same cases. Extractor versions: 4968c49f. Every pass pooled.

| Format | Results | Status | Deadline | Missed | Late | Extraction | Report words lost | Confidence |
|---|---|---|---|---|---|---|---|---|
| text | 90 | 93.3% | 98.9% | 0 | 0 | 96.9% | n/a | n/a |
| form | 90 | 95.6% | 90.0% | 0 | 0 | 95.7% | 0.0% | 99.7 |
| scan | 90 | 85.6% | 93.3% | 3 | 0 | 95.9% | 0.0% | 99.4 |
| photo | 90 | 84.4% | 91.1% | 3 | 0 | 95.3% | 0.0% | 99.3 |

## Fields that moved by 3 points or more against text

| Field | Text | form | scan | photo |
|---|---|---|---|---|
| env_effect | 96.6% | 92.0% | 90.8% | 93.1% |
| lands | 84.1% | 52.4% | 77.8% | 68.3% |
| other_beyond_design | 93.3% | 100.0% | 90.0% | 91.1% |
| planned_venting | 100.0% | 98.4% | 98.4% | 95.2% |
| point:env_effect | 50.0% | 33.3% | 37.5% | 33.3% |
| point:volume_m3 | 100.0% | 100.0% | 66.7% | 66.7% |
| volume_estimated | 87.5% | 87.5% | 93.8% | 87.5% |

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

## OCR results with a wrong status or deadline (39)

| Row | Pass | Expected | Got | Wrong fields |
|---|---|---|---|---|
| AD-155@form | 1 | reportable T24 | reportable T3 | lands |
| AD-155@form | 2 | reportable T24 | reportable T3 | lands |
| AD-155@form | 3 | reportable T24 | reportable T3 | lands |
| CL-015@form | 1 | precautionary T3 | reportable T3 | env_effect, volume_estimated, through_pipe_body_or_weld |
| CL-015@form | 2 | precautionary T3 | reportable T3 | env_effect, volume_estimated, through_pipe_body_or_weld |
| CL-015@form | 3 | precautionary T3 | reportable T3 | env_effect, volume_estimated, through_pipe_body_or_weld |
| CL-015@photo | 1 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld, lands, other_beyond_design |
| CL-015@photo | 2 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld, lands, other_beyond_design |
| CL-015@photo | 3 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld, lands, other_beyond_design |
| CL-015@scan | 1 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld, other_beyond_design |
| CL-015@scan | 2 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld, lands, other_beyond_design |
| CL-015@scan | 3 | precautionary T3 | reportable T3 | env_effect, through_pipe_body_or_weld, lands, other_beyond_design |
| CL-027@scan | 1 | precautionary T3 | reportable T3 | lands, other_beyond_design |
| JU-094@photo | 1 | precautionary T24 | reportable T24 | lands, other_beyond_design |
| JU-094@photo | 2 | precautionary T24 | reportable T24 | lands, other_beyond_design |
| JU-094@photo | 3 | precautionary T24 | reportable T24 | lands, other_beyond_design |
| JU-094@scan | 1 | precautionary T24 | reportable T24 | lands, other_beyond_design |
| JU-094@scan | 2 | precautionary T24 | reportable T24 | lands, other_beyond_design |
| JU-094@scan | 3 | precautionary T24 | reportable T24 | lands, other_beyond_design |
| JU-110@form | 2 | precautionary T24 | precautionary T3 | lands |
| JU-110@form | 3 | precautionary T24 | precautionary T3 | lands |
| JU-137@photo | 1 | precautionary T24 | not reportable None | lands, point:volume_m3 |
| JU-137@photo | 2 | precautionary T24 | not reportable None | lands, point:volume_m3 |
| JU-137@photo | 3 | precautionary T24 | not reportable None | lands, point:volume_m3 |
| JU-137@scan | 1 | precautionary T24 | not reportable None | lands, point:volume_m3 |
| JU-137@scan | 2 | precautionary T24 | not reportable None | lands, point:volume_m3 |
| JU-137@scan | 3 | precautionary T24 | not reportable None | lands, point:volume_m3 |
| JU-138@form | 1 | precautionary T24 | precautionary T3 | lands |
| JU-138@form | 2 | precautionary T24 | precautionary T3 | lands |
| JU-138@form | 3 | precautionary T24 | precautionary T3 | lands |
| NO-078@form | 1 | not reportable None | reportable T24 | volume_estimated, planned_venting, lands |
| NO-078@photo | 1 | not reportable None | reportable T24 | volume_estimated, planned_venting, lands |
| NO-078@photo | 2 | not reportable None | reportable T24 | volume_estimated, planned_venting, lands |
| NO-078@photo | 3 | not reportable None | reportable T24 | volume_estimated, planned_venting, lands |
| NO-078@scan | 3 | not reportable None | reportable T24 | volume_estimated, planned_venting, lands |
| NO-164@photo | 2 | not reportable None | reportable T24 | other_beyond_design |
| NO-164@photo | 3 | not reportable None | reportable T24 | other_beyond_design |
| NO-164@scan | 2 | not reportable None | reportable T24 | other_beyond_design |
| NO-164@scan | 3 | not reportable None | reportable T24 | other_beyond_design |
