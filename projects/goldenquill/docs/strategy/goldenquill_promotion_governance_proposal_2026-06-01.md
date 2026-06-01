---
title: GoldenQuill Promotion Governance Proposal
date: 2026-06-01
status: proposed
observed_capability: invoke
invoke_mode: design
architecture: goldenquill_promotion_governance_architecture_design_2026-06-01.md
decision_record: ../decisions/goldenquill-promotion-mechanism-open-gaps.md
---

# GoldenQuill Promotion Governance Proposal

## Proposal

Build a GoldenQuill-local promotion governance layer under `grant_dag` that
tracks grant outcomes, KPI observations, feedback, candidate learning, and owner
decisions while using Ontology Vault as the embedded governance layer for
promotion safety.

The first implementation should be a fixture-only validator. It should prove the
architecture before any dashboard, production memory, org-vault, or signed-card
work begins.

The proposal must preserve the grant-run execution DAG. That DAG answers:

- what happened in the grant run;
- in what order it happened;
- what gate allowed or blocked the next step.

Minimum run nodes:

```text
run_context
project_context_reference
rfa_reference
scout_discovery_record
scout_verification_record
operator_review_decision
rfa_dissection
kgie_preflight
scribe_section_draft
editor_suggestion_report
judge_score_report
responsiveness_map
red_team_review
logician_gate_result
operator_signoff
delivery_envelope
```

Minimum run edges:

```text
precedes
consumes
emits
blocked_by_gate
revised_by
approved_by
delivered_as
```

## Why This Matters

Grant writing improves through real-world feedback:

- a grant was submitted but never reviewed;
- an agency retrieved the application;
- reviewer feedback arrived;
- the grant was declined;
- the grant won but for less money than requested;
- a report was accepted;
- a funder relationship improved;
- a repeated rejection revealed a strategy gap.

Without a governance layer, these signals can become messy memory. With this
proposal, they become source-backed candidates that can be reviewed, redacted,
approved, rejected, or retired.

The grant should be modeled as a traceable graph, not just as a final document.
The graph tracks funder-fit claims, source evidence, compliance checks,
reviewer objections, draft surfaces, rubric scores, and reuse decisions.

| Research-Style Primitive | GoldenQuill Primitive |
| --- | --- |
| Hypothesis | Funder-fit hypothesis, eligibility claim, budget assumption, reviewer-risk claim. |
| Experiment | Draft section, evidence search, rubric scoring pass, compliance check, outreach test. |
| Replication | Second source, second reviewer seat, cross-family review, prior-award precedent, repeated scoring pass. |
| Objection | Red Team/Judge challenge, admin-risk warning, missing evidence, rule conflict. |
| Extension | Proposal variant, adjacent opportunity, reusable evidence packet, next funder strategy. |
| Consensus | Signed/operator-approved state after evidence and gate checks. |

## Selected Decisions

1. GoldenQuill owns the local model.
2. Ontology Vault is an explicit governance layer inside that model.
3. First implementation lives in GoldenQuill `grant_dag`.
4. Use `proposed_allowed_uses` on candidates and `approved_allowed_uses` on
   owner decisions.
5. Selected KPIs can create candidates, but cannot promote directly.
6. Feedback is private by default; reusable only after redaction/generalization
   and owner approval.
7. Stage-depth scoring uses a global baseline plus funder-family overrides.

## Proposed Package Shape

```text
projects/goldenquill/pipeline/grant_dag/
  models.py
  validate.py
  promotion/
  ontology_vault/
  metrics/
  privacy/

projects/goldenquill/tests/grant_dag/
  test_promotion_governance.py
  fixtures/
```

## First Slice

Build only:

- fixture schema;
- validator;
- positive fixture;
- negative fixtures;
- deterministic pytest command.

The first slice should include fixtures for:

- a pass path from `run_context` to `delivery_envelope`;
- a blocked path where `kgie_preflight` is blocked by `logician_gate_result`;
- a declined-after-review outcome;
- an awarded-for-less-than-requested outcome;
- a submitted-but-not-reviewed outcome;
- a successful post-award report or closeout outcome.

Do not build:

- UI;
- dashboard;
- real data importer;
- production memory writes;
- signed-card mutation;
- org-vault mutation;
- automatic promotion.

## Acceptance Criteria

The first slice is successful when:

- an outcome event without a source fails;
- a KPI without denominator definition fails;
- a candidate with approved uses before owner decision fails;
- org-scoped feedback cannot become workspace-global without redaction;
- a valid redacted learning candidate passes;
- a valid owner decision with approved uses passes;
- the governance projection requires evidence, review gate, and contradiction
  path;
- stage-depth can use the global baseline and can name a future profile
  override.
- a run DAG can explain which gate allowed or blocked the next step;
- outcome examples can create candidates without promoting them directly.

## KPI Families

The architecture should track more than win/loss.

| Family | KPIs |
| --- | --- |
| Quality and review movement | `compliance_pass_rate`, `rubric_coverage_score`, `reviewer_objection_resolution_rate`, `evidence_gap_resolution_rate`, `section_revision_delta`, `review_feedback_quality`, `resubmission_delta` |
| Strategy fit | `go_no_go_selectivity`, `high_match_pursuit_rate`, `low_fit_avoidance_rate`, `relationship_present_rate`, `prior_award_alignment`, `program_drift_rate` |
| Effort and ROI | `hours_per_submission`, `cost_per_submitted_application`, `cost_per_award`, `dollars_requested_per_hour`, `dollars_awarded_per_hour`, `cycle_time_discovery_to_submit`, `cycle_time_submit_to_decision`, `reporting_burden_hours` |
| Capacity and relationship | `stakeholder_contacts`, `new_stakeholder_engagement_rate`, `collaboration_artifacts_count`, `staff_consultations`, `internal_training_hours`, `funder_touchpoints`, `grant_retention_rate` |

These KPIs can create candidates only after source, denominator, org-scope, and
interpretation checks. They cannot promote directly.

## Evidence-State Rules

GoldenQuill should keep these states separate:

| State | Meaning |
| --- | --- |
| application stage | Where the grant is in the process. |
| outcome event | Source-backed award, decline, withdrawal, report acceptance, or closeout. |
| validation state | Whether a claim, denominator, feedback interpretation, or compliance result was checked. |
| source truth | What the source actually says, independent of proposal prose or dashboard labels. |

Rules:

```text
application status != outcome truth
review feedback != funding validation
award notification != post-award performance
proposal claim != source fact
dashboard KPI != promotion authority
```

## Vocabulary Policy

Use GoldenQuill-native terms only in implementation-facing artifacts:

- application stage;
- final outcome;
- validation state;
- evidence packet;
- outcome event;
- KPI observation;
- promotion candidate;
- owner decision;
- governance layer;
- redaction/generalization gate.

Avoid importing external research-program vocabulary into the implementation
surface. Older research ledgers may preserve historical source notes, but
design, proposal, validator, fixture, and task-session artifacts should use the
terms above.

## Recommended Next Route

Use `task-session` for the L0 fixture-only validator.

Suggested task title:

```text
TASK-GDAG-PROMO-001: Implement fixture-only promotion governance validator
```

Suggested verification:

```bash
cd projects/goldenquill
.venv/bin/python3 -m pytest tests/grant_dag/test_promotion_governance.py -v
```

If the virtual environment is unavailable, record the environment blocker
instead of switching to an unapproved validation surface.
