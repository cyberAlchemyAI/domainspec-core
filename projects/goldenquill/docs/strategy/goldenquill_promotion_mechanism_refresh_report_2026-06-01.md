---
title: GoldenQuill Promotion Mechanism Invoke Refresh Report
date: 2026-06-01
status: proposal-only
observed_capability: invoke
invoke_mode: refresh
mutation_mode: proposal-only
target_artifacts:
  - docs/strategy/goldenquill_promotion_mechanism_research_2026-06-01.md
  - docs/strategy/goldenquill_promotion_mechanism_invoke_design_2026-06-01.md
  - docs/strategy/goldenquill_promotion_mechanism_refine_seed_2026-06-01.md
  - docs/strategy/goldenquill_ontology_dag_grant_research_synthesis_2026-06-01.md
  - docs/strategy/goldenquill_ontology_dag_toy_validation_2026-06-01.md
---

# GoldenQuill Promotion Mechanism Invoke Refresh Report

## Refresh Intent

Refresh the GoldenQuill ontology-DAG and promotion-mechanism artifacts with
real-world outcome evidence:

- rejections;
- wins;
- stage depth;
- review movement;
- funder response timing;
- post-award reporting outcomes;
- grant-writing KPIs;
- grant evidence-state separation for stage, outcome, and validation.

This refresh is proposal-only. It does not implement runtime tracking, mutate
org memory, promote ontology entries, or modify GoldenQuill production schema.

## Online Research Baseline

| Source | What It Contributes | Design Use |
| --- | --- | --- |
| [Grants.gov Grant Lifecycle](https://www.grants.gov/learn-grants/grants-101/the-grant-lifecycle) | Federal grant lifecycle has pre-award, award, and post-award phases; status progresses through opportunity search, registration, completion, submission, agency retrieval, review, award notification, reporting, and closeout. | Use lifecycle depth as a first-class metric, not only final outcome. |
| [Grants.gov Check Application Status](https://www.grants.gov/help/applicants/check-application-status) | Applicants can track Grants.gov status through validation, agency receipt, and agency tracking number; later status moves to the agency. | Split `portal_status` from `agency_status`; do not assume Grants.gov knows final outcome. |
| [NIH FY 2025 By The Numbers](https://grants.nih.gov/news-events/nih-extramural-nexus-news/2026/03/fiscal-year-2025-by-the-numbers-extramural-grant-investments-in-research) | NIH reports applications, awards, success rates, award sizes, and fiscal-year trend changes. FY 2025 RPG success rate was reported at 13.0%, down from 18.5% in FY 2024. | Track program/funder benchmark context beside internal win rate so low win rate is not misread as writing failure. |
| [NSF Funding Rates](https://www.nsf.gov/eng/funding-rates) | NSF defines funding rate as new competitively reviewed awards divided by competitive awards plus declines; directorates publish rates such as ENG 23% in FY 2024. | Store benchmark denominator semantics with each KPI. |
| [NSF Proposal and Award Overview](https://www.nsf.gov/funding/overview) | NSF proposals are reviewed on intellectual merit and broader impacts; the overview notes repeated submission behavior and first-attempt outcomes. | Track criterion-specific review signals and resubmission learning. |
| [Instrumentl Grant Performance Dashboard](https://help.instrumentl.com/en/articles/10543572-grant-performance-dashboard) | Common dashboard KPIs include amount awarded, won/lost, win rate, applications by status, new vs repeat funders, amount requested, and grants researched. | Adopt a practical dashboard starter set. |
| [Grant Professionals Association Strategy Paper](https://cdn.ymaws.com/grantprofessionals.org/resource/resmgr/publications/strategy_papers/strategy_papers_volume_6.2.pdf) | Grant-professional metrics include stakeholder contacts, new stakeholder engagement, proposals to new funders, grant retention, dollars secured, progress to goal, funder contacts, consultations, trainings, collaborations, and data-maintenance work. | Add relationship, stewardship, and capacity metrics beyond win rate. |

## KPI Families To Add

### 1. Lifecycle Depth

Track how far the grant went.

| KPI | Formula / Source |
| --- | --- |
| `stage_depth` | deepest reached stage in the local lifecycle enum |
| `stage_depth_score` | numeric score for comparison across opportunities |
| `submission_validated_rate` | validated submissions / submitted applications |
| `agency_retrieved_rate` | agency-retrieved applications / validated submissions |
| `review_reached_rate` | applications with agency/reviewer review signal / submitted applications |
| `final_decision_rate` | awarded plus declined / submitted applications |
| `closeout_completed_rate` | closed awards / awarded grants |

Proposed stage enum:

```text
prospect
eligible_match
go_no_go_approved
loi_submitted
invited_full
application_started
application_submitted
portal_validated
agency_retrieved
agency_tracking_assigned
under_review
review_feedback_received
award_recommended
awarded
declined
withdrawn
post_award_active
reporting_current
closed_out
```

### 2. Outcome Evidence

Track wins and rejections as source-backed events.

| KPI | Formula / Source |
| --- | --- |
| `win_rate_by_count` | awarded / final decisions |
| `win_rate_by_dollars` | awarded dollars / requested dollars for final decisions |
| `decline_rate` | declined / final decisions |
| `pending_rate` | pending / submitted applications |
| `award_amount_realization` | awarded amount / requested amount |
| `partial_award_rate` | partial awards / awards |
| `resubmission_success_rate` | awarded resubmissions / final-decision resubmissions |
| `repeat_funder_win_rate` | repeat-funder awards / repeat-funder final decisions |
| `new_funder_conversion_rate` | new-funder awards / new-funder final decisions |

Every outcome event should carry:

- source document path or URL;
- notification date;
- portal or agency status;
- amount requested;
- amount awarded;
- funder;
- program;
- applicant/org;
- outcome class;
- follow-up obligations.

### 3. Quality And Review Movement

Track whether GoldenQuill improves proposal quality even before funding.

| KPI | Signal |
| --- | --- |
| `compliance_pass_rate` | Logician pre-submit gates passed / attempted |
| `rubric_coverage_score` | covered rubric criteria / total criteria |
| `reviewer_objection_resolution_rate` | resolved objections / total objections |
| `evidence_gap_resolution_rate` | resolved evidence gaps / identified gaps |
| `section_revision_delta` | score or risk improvement across draft iterations |
| `review_feedback_quality` | coded feedback specificity and actionability |
| `resubmission_delta` | score/review movement from prior submission to next |

### 4. Strategy Fit

Track whether the team applies to the right opportunities.

| KPI | Signal |
| --- | --- |
| `go_no_go_selectivity` | pursued opportunities / researched opportunities |
| `high_match_pursuit_rate` | high-fit pursued / high-fit identified |
| `low_fit_avoidance_rate` | low-fit not pursued / low-fit identified |
| `relationship_present_rate` | submissions with existing funder relationship / submissions |
| `prior_award_alignment` | proposal fit against funder prior-award corpus |
| `program_drift_rate` | funder/RFA requirements that changed after discovery |

### 5. Effort And ROI

Track cost, cycle time, and operational leverage.

| KPI | Signal |
| --- | --- |
| `hours_per_submission` | staff hours / submitted application |
| `cost_per_submitted_application` | labor plus tools / submitted application |
| `cost_per_award` | labor plus tools / awards |
| `dollars_requested_per_hour` | requested dollars / grant-work hours |
| `dollars_awarded_per_hour` | awarded dollars / grant-work hours |
| `cycle_time_discovery_to_submit` | submission date - discovery date |
| `cycle_time_submit_to_decision` | decision date - submission date |
| `reporting_burden_hours` | post-award reporting hours / award |

### 6. Capacity And Relationship

Track grant-professional work that win rate hides.

| KPI | Signal |
| --- | --- |
| `stakeholder_contacts` | grant-seeking contacts per period |
| `new_stakeholder_engagement_rate` | new stakeholders engaged / stakeholders engaged |
| `collaboration_artifacts_count` | MOUs, MOAs, support letters, partner commitments |
| `staff_consultations` | staff consultations for proposal/program development |
| `internal_training_hours` | hours spent improving internal grant capability |
| `funder_touchpoints` | contacts with new and existing funders |
| `grant_retention_rate` | repeat support year over year |

## Grant Evidence-State Discipline

GoldenQuill should treat grant status, final outcome, and validation as separate
states.

The grant metric model should separate:

| State | Grant Meaning |
| --- | --- |
| application stage | artifact or application stage, such as submitted, under review, awarded, declined |
| outcome event | final source-backed notification, award, decline, withdrawal, report acceptance, or closeout |
| validation state | verified claim, compliance pass, source-resolved evidence, reviewer-confirmed feedback |
| graph authority | visible authored trace first; structured edges only after validator parity |
| source truth | no grant truth from proposal prose, dashboard label, or staff memory |

This gives GoldenQuill a clearer real-world evidence rule:

```text
application status != outcome truth
review feedback != funding validation
award notification != post-award performance
proposal claim != source fact
dashboard KPI != promotion authority
```

## Promotion Model Refresh

`PromotionCandidate` should gain a real-world evidence section:

```json
{
  "real_world_evidence": {
    "event_kind": "submitted | validated | retrieved_by_agency | under_review | feedback_received | awarded | declined | withdrawn | report_accepted | closed_out",
    "event_date": "YYYY-MM-DD",
    "source_ref": "path, URL, portal export, email archive, or agency notice",
    "amount_requested": null,
    "amount_awarded": null,
    "stage_depth": "under_review",
    "stage_depth_score": 10,
    "funder_feedback_refs": [],
    "post_award_obligations": []
  }
}
```

Real-world evidence can promote a learning only when:

- the event source is captured;
- the lifecycle stage is explicit;
- the denominator is known for any rate;
- the owner is named;
- counterevidence or future reversal is possible;
- the learning does not expose private org context outside its scope.

## Recommended Artifact Deltas

| Artifact | Delta |
| --- | --- |
| promotion research | Add real-world outcome evidence and KPI families. |
| invoke design | Add `GrantOutcomeEvent`, `ApplicationLifecycleState`, and KPI projection objects. |
| refine seed | Add a refine question about whether metrics are evidence, candidate relations, or promotion gates. |
| ontology DAG synthesis | Add outcome-event and metric-observation node families. |
| toy validation | Add positive and negative fixtures for won/lost/pending lifecycle events and denominator safety. |

## Open Questions

1. Should GoldenQuill track all application statuses internally, or import
   portal/agency exports only as evidence packets?
2. Should funder feedback be a reusable learning source by default, or always
   org-scoped until redacted?
3. Which metrics belong to operator dashboard only, and which can feed ontology
   promotion?
4. Should `stage_depth_score` be globally fixed or funder-family-specific?
5. Should post-award performance metrics influence future proposal strategy
   promotion?
