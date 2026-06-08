# Evidence And KPI Appendix

## Evidence Discipline

GoldenQuill should separate grant status, final outcome, validation state, graph
authority, and source truth.

| Evidence State | Meaning |
| --- | --- |
| Application stage | Where the application appears to be in the lifecycle, such as submitted, under review, awarded, declined, reporting, or closed out. |
| Outcome event | A source-backed notice or event, such as award, decline, withdrawal, report acceptance, or closeout. |
| Validation state | Whether a claim, feedback item, compliance pass, metric denominator, or source interpretation has been checked. |
| Graph authority | Whether the run history is traceable and reviewable before it becomes structured reusable knowledge. |
| Source truth | The source that proves a grant fact, such as a portal export, agency notice, award letter, decline notice, email archive, report, or approved operator record. |

## Boundary Rules

```text
application status != outcome truth
review feedback != funding validation
award notification != post-award performance
proposal claim != source fact
dashboard KPI != promotion authority
```

## Outcome Examples

### Submitted But Not Reviewed

Use this to measure operational completion and portal success. Do not infer
proposal quality.

### Declined After Review

Use this to create a private learning candidate from reviewer feedback and
strategy signals. Do not reuse feedback outside the client context unless it is
generalized and approved.

### Awarded For Less Than Requested

Use this to learn about budget framing, funder preference, scope fit, or award
negotiation. Do not treat the award as proof that every proposal claim was
strong.

### Blocked Before Draft

Use this to track evidence gaps, eligibility issues, missing partner materials,
or review gates that prevented work from moving forward.

### Successful Closeout

Use this to learn from stewardship, reporting quality, funder relationship, and
repeat-support signals.

## KPI Families

### Lifecycle Depth

| KPI | Signal |
| --- | --- |
| `stage_depth` | Deepest verified application stage reached. |
| `stage_depth_score` | Numeric comparison of progress across opportunities. |
| `submission_validated_rate` | Validated submissions divided by submitted applications. |
| `agency_retrieved_rate` | Agency-retrieved applications divided by validated submissions. |
| `review_reached_rate` | Applications with review signal divided by submitted applications. |
| `final_decision_rate` | Awarded plus declined applications divided by submitted applications. |
| `closeout_completed_rate` | Closed awards divided by awarded grants. |

### Outcome Evidence

| KPI | Signal |
| --- | --- |
| `win_rate_by_count` | Awards divided by final decisions. |
| `win_rate_by_dollars` | Awarded dollars divided by requested dollars for final decisions. |
| `decline_rate` | Declines divided by final decisions. |
| `pending_rate` | Pending applications divided by submitted applications. |
| `award_amount_realization` | Awarded amount divided by requested amount. |
| `partial_award_rate` | Partial awards divided by awards. |
| `resubmission_success_rate` | Awarded resubmissions divided by final-decision resubmissions. |
| `repeat_funder_win_rate` | Repeat-funder awards divided by repeat-funder final decisions. |
| `new_funder_conversion_rate` | New-funder awards divided by new-funder final decisions. |

### Quality And Review Movement

| KPI | Signal |
| --- | --- |
| `compliance_pass_rate` | Pre-submit gates passed divided by attempted gates. |
| `rubric_coverage_score` | Covered rubric criteria divided by total criteria. |
| `reviewer_objection_resolution_rate` | Resolved objections divided by total objections. |
| `evidence_gap_resolution_rate` | Resolved evidence gaps divided by identified gaps. |
| `section_revision_delta` | Score or risk improvement across draft iterations. |
| `review_feedback_quality` | Specificity and actionability of feedback. |
| `resubmission_delta` | Score or review movement from prior submission to next submission. |

### Strategy Fit

| KPI | Signal |
| --- | --- |
| `go_no_go_selectivity` | Pursued opportunities divided by researched opportunities. |
| `high_match_pursuit_rate` | High-fit pursued opportunities divided by high-fit identified opportunities. |
| `low_fit_avoidance_rate` | Low-fit avoided opportunities divided by low-fit identified opportunities. |
| `relationship_present_rate` | Submissions with existing funder relationship divided by submissions. |
| `prior_award_alignment` | Fit against funder prior-award patterns. |
| `program_drift_rate` | Changed funder or opportunity requirements after discovery. |

### Effort And ROI

| KPI | Signal |
| --- | --- |
| `hours_per_submission` | Staff hours divided by submitted applications. |
| `cost_per_submitted_application` | Labor plus tools divided by submitted applications. |
| `cost_per_award` | Labor plus tools divided by awards. |
| `dollars_requested_per_hour` | Requested dollars divided by grant-work hours. |
| `dollars_awarded_per_hour` | Awarded dollars divided by grant-work hours. |
| `cycle_time_discovery_to_submit` | Submission date minus discovery date. |
| `cycle_time_submit_to_decision` | Decision date minus submission date. |
| `reporting_burden_hours` | Post-award reporting hours divided by award count. |

### Capacity And Relationship

| KPI | Signal |
| --- | --- |
| `stakeholder_contacts` | Grant-seeking contacts per period. |
| `new_stakeholder_engagement_rate` | New stakeholders engaged divided by stakeholders engaged. |
| `collaboration_artifacts_count` | MOUs, MOAs, support letters, partner commitments. |
| `staff_consultations` | Staff consultations for proposal or program development. |
| `internal_training_hours` | Hours improving internal grant capability. |
| `funder_touchpoints` | Contacts with new and existing funders. |
| `grant_retention_rate` | Repeat support year over year. |
