---
title: GoldenQuill Promotion Governance Architecture Design
date: 2026-06-01
status: design-ready
observed_capability: invoke
invoke_mode: design
target_owner: GoldenQuill local model with Ontology Vault governance layer
decision_record: ../decisions/goldenquill-promotion-mechanism-open-gaps.md
proposal: goldenquill_promotion_governance_proposal_2026-06-01.md
---

# GoldenQuill Promotion Governance Architecture Design

## Executive Summary

GoldenQuill needs a local promotion-governance architecture that can learn from
grant work without turning drafts, metrics, reviewer comments, or retrieved
evidence into reusable authority too early.

The selected architecture is:

```text
GoldenQuill local grant model
  -> evidence and outcome capture
  -> candidate generation
  -> Ontology Vault governance layer
  -> owner decision
  -> approved reuse, rejection, retirement, or private residue
```

GoldenQuill owns grant-specific runtime shape: applications, opportunities,
outcomes, KPIs, feedback, stage depth, and grant-cycle events. The Ontology Vault
layer owns promotion governance: target owner routing, evidence sufficiency,
contradiction paths, approved uses, and non-promotion guardrails.

## Source Decisions

| Decision | Selected Direction |
| --- | --- |
| Promotion unit home | GoldenQuill local model with Ontology Vault as explicit governance layer. |
| First implementation location | GoldenQuill local `grant_dag` package with an Ontology Vault layer or adapter. |
| Allowed uses | Split `proposed_allowed_uses` and `approved_allowed_uses`. |
| KPI authority | Selected KPIs can create candidates, but cannot promote directly. |
| Feedback generalization | Org-scoped by default; reusable only through redaction/generalization gate plus owner approval. |
| Stage-depth scoring | Global stage baseline plus optional funder-family profile override. |

## Design Goals

1. Track real-world grant progress from prospect through award, decline,
   reporting, and closeout.
2. Convert wins, rejections, reviewer comments, and KPI signals into candidate
   learning without automatic promotion.
3. Keep private applicant feedback private until redacted and approved.
4. Give GoldenQuill a local validator surface for grant-specific semantics.
5. Keep the Ontology Vault layer responsible for promotion authority.
6. Make every candidate auditable through source evidence, owner decision,
   approved uses, and contradiction path.

## Non-Goals

- No production org-vault mutation in the first slice.
- No dashboard implementation in the first slice.
- No automatic promotion from KPI thresholds.
- No signed-card mutation.
- No canonical Ontology Vault template mutation.
- No private funder feedback becoming workspace-global without a redaction gate.

## Six Design Views

### 1. Context View

GoldenQuill already has a grant workflow with discovery, drafting, editing,
scoring, gate checks, and operator decisions. The missing layer is a governed
learning path:

- what happened in the world;
- what evidence supports that event;
- what the event suggests;
- what may be reused;
- who is allowed to approve reuse;
- what must stay private or rejected.

This architecture sits after and around the existing workflow. It does not
replace Scout, Scribe, Editor, Judge, Logician, card governance, or org-vault
memory.

The first thing it must preserve is the execution DAG of a grant run. That DAG
answers three operational questions:

- what happened in this grant run;
- in what order it happened;
- which gate allowed or blocked the next step.

Minimum execution nodes:

| Node | Purpose |
| --- | --- |
| `run_context` | One bounded grant run, including org scope, opportunity, operator, and run id. |
| `project_context_reference` | Source pointer to the applicant/project context used for the run. |
| `rfa_reference` | Source pointer to the RFA/NOFO/funder instruction source. |
| `scout_discovery_record` | Record that the opportunity was found. |
| `scout_verification_record` | Record that the opportunity was verified as usable or rejected. |
| `operator_review_decision` | Human go/no-go or review decision after discovery. |
| `rfa_dissection` | Extracted requirements, deadlines, forms, criteria, and constraints. |
| `kgie_preflight` | Pre-draft fit, evidence, eligibility, and gap check. |
| `scribe_section_draft` | Drafted proposal section or section version. |
| `editor_suggestion_report` | Clarity, structure, and reviewer-fit suggestions. |
| `judge_score_report` | Rubric scoring and risk assessment. |
| `responsiveness_map` | Map from RFA/rubric requirements to draft responses. |
| `red_team_review` | Conditional adversarial or risk review. |
| `logician_gate_result` | Deterministic pass/fail/warn gate result. |
| `operator_signoff` | Human approval to deliver, revise, pause, or stop. |
| `delivery_envelope` | Final package delivered, submitted, or handed off. |

Minimum execution edges:

| Edge | Meaning |
| --- | --- |
| `precedes` | One run event happened before another. |
| `consumes` | A step used a source, artifact, or decision. |
| `emits` | A step produced an artifact or event. |
| `blocked_by_gate` | A gate prevented traversal to the next step. |
| `revised_by` | A draft or artifact was changed by a later review/revision. |
| `approved_by` | A human or owner approval allowed the next transition. |
| `delivered_as` | A delivery envelope was emitted as a submission or handoff. |

Example pass path:

```text
run_context
  precedes scout_discovery_record
  precedes scout_verification_record
  approved_by operator_review_decision
  emits rfa_dissection
  emits kgie_preflight
  precedes scribe_section_draft
  revised_by editor_suggestion_report
  tested_by judge_score_report
  traced_to responsiveness_map
  approved_by logician_gate_result
  approved_by operator_signoff
  delivered_as delivery_envelope
```

Example blocked path:

```text
kgie_preflight
  blocked_by_gate logician_gate_result
  emits evidence_gap
  prevents scribe_section_draft
```

The promotion-governance layer consumes this execution DAG. It does not replace
it.

### 2. High-Level Structure View

```text
projects/goldenquill/pipeline/grant_dag/
  __init__.py
  models.py
  validate.py
  execution/
    __init__.py
    run_nodes.py
    run_edges.py
    traversal.py
  promotion/
    __init__.py
    candidates.py
    decisions.py
    allowed_uses.py
  ontology_vault/
    __init__.py
    adapter.py
    promotion_record_projection.py
    governance_checks.py
  metrics/
    __init__.py
    outcome_events.py
    lifecycle.py
    kpi_observations.py
    stage_profiles.py
  privacy/
    __init__.py
    redaction.py
    generalization.py
  fixtures/
    README.md

projects/goldenquill/tests/grant_dag/
  test_promotion_governance.py
  test_outcome_metrics.py
  test_feedback_generalization.py
  fixtures/
```

Layer responsibilities:

| Layer | Responsibility |
| --- | --- |
| `grant_dag.models` | Shared node, edge, source, scope, and graph structures. |
| `execution` | Grant-run DAG nodes, edges, ordering, and gate traversal. |
| `promotion` | Candidate state, proposed uses, approved uses, owner decision references. |
| `ontology_vault` | Governance checks and projection to PromotionRecord-compatible shape. |
| `metrics` | Outcome events, stage-depth projection, KPI observations, denominator checks. |
| `privacy` | Redaction/generalization gates for reusable feedback. |
| tests/fixtures | Positive and negative cases using synthetic/demo data only. |

### 3. Low-Level Components View

#### `GrantRunNode`

Represents one event or artifact in a grant run execution DAG.

Fields:

- `node_id`
- `node_kind`
- `run_id`
- `org_scope`
- `source_ref`
- `created_utc`
- `state`
- `artifact_ref`
- `gate_ref`

Allowed `node_kind` values for the first slice:

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

#### `GrantRunEdge`

Represents ordering, consumption, emission, revision, approval, blocking, or
delivery between run nodes.

Fields:

- `edge_id`
- `edge_kind`
- `from_node`
- `to_node`
- `run_id`
- `evidence_ref`
- `created_by`
- `validation_state`

Allowed `edge_kind` values for the first slice:

```text
precedes
consumes
emits
blocked_by_gate
revised_by
approved_by
delivered_as
```

Rule: no draft, delivery, KPI, or learning candidate can skip the run DAG. The
validator must be able to explain which prior node and gate allowed it.

#### `MemoryEvidencePacketRef`

References an existing evidence packet or source-backed equivalent.

Fields:

- `packet_id`
- `source_path`
- `locator`
- `authority_class`
- `org_scope`
- `retrieval_surface`
- `freshness_signal`

Rule: evidence references do not approve reuse.

#### `GrantOutcomeEvent`

Captures source-backed real-world grant movement.

Fields:

- `event_id`
- `application_id`
- `event_kind`
- `event_date`
- `source_ref`
- `portal_status`
- `agency_status`
- `amount_requested`
- `amount_awarded`
- `feedback_refs`
- `post_award_obligations`
- `org_scope`

Rule: outcome events can create learning candidates, but cannot approve them.

Concrete outcome examples:

| Example | Event Kind | How GoldenQuill Uses It |
| --- | --- | --- |
| Portal accepted the package. | `portal_validated` | Advances stage depth; does not mean agency review started. |
| Agency assigned a tracking number. | `agency_tracking_assigned` | Confirms agency receipt; can feed cycle-time metrics. |
| Review comments arrived after decline. | `feedback_received` plus `declined` | Creates org-scoped learning candidate; requires redaction for shared reuse. |
| Award notice arrived for less than requested. | `awarded` | Feeds dollar realization KPI and possible budget-framing candidate. |
| Application was withdrawn before review. | `withdrawn` | Blocks win/loss interpretation; can create process lesson. |
| Post-award report accepted. | `report_accepted` | Feeds stewardship and retention metrics; does not validate every proposal claim. |
| Award closed out successfully. | `closed_out` | Feeds retention/readiness learning and future funder relationship metrics. |

#### `ApplicationLifecycleState`

Projects the deepest verified application stage.

Fields:

- `application_id`
- `current_stage`
- `stage_depth_score`
- `stage_profile`
- `profile_override`
- `source_event_id`
- `last_verified_utc`

Rule: stage depth is not a win/loss outcome.

#### `GrantKpiObservation`

Stores a metric read model.

Fields:

- `metric_id`
- `metric_kind`
- `numerator`
- `denominator`
- `denominator_definition`
- `value`
- `segment`
- `source_events`
- `interpretation_limits`

Rule: selected KPIs may create candidates after validation; they cannot promote.

#### `PromotionCandidate`

The local grant-learning proposal object.

Fields:

- `candidate_id`
- `candidate_kind`
- `created_utc`
- `created_by`
- `source_packets`
- `source_events`
- `source_kpis`
- `target_owner`
- `target_artifact`
- `proposed_relation`
- `proposed_allowed_uses`
- `current_state`
- `review_gate`
- `promotion_blockers`
- `contradiction_path`
- `privacy_scope`
- `redaction_status`
- `owner_decision_ref`
- `residue`

Rule: candidates are not approved reuse.

#### `OwnerDecision`

The approved, rejected, retired, or contradicted decision record.

Fields:

- `decision_id`
- `candidate_id`
- `owner`
- `decision`
- `approved_allowed_uses`
- `decision_date`
- `decision_source`
- `conditions`
- `contradiction_path`

Rule: approved uses live here, not on raw evidence.

#### `OntologyVaultProjection`

Maps the local candidate and decision shape into the governance layer.

Fields:

- `projection_id`
- `candidate_id`
- `record_kind`
- `target_relation`
- `evidence_refs`
- `review_gate`
- `contradiction_path`
- `governance_state`
- `validation_result`

Rule: the projection enforces governance compatibility; it does not mutate the
target artifact.

### 4. Workflow Process View

```text
1. Create run_context.
2. Attach project_context_reference and rfa_reference.
3. Record scout_discovery_record.
4. Record scout_verification_record.
5. Ask operator_review_decision.
6. Emit rfa_dissection.
7. Run kgie_preflight.
8. If blocked, emit logician_gate_result and stop traversal.
9. If allowed, emit scribe_section_draft.
10. Emit editor_suggestion_report.
11. Emit judge_score_report and responsiveness_map.
12. Optionally emit red_team_review.
13. Emit logician_gate_result.
14. Ask operator_signoff.
15. Emit delivery_envelope.
16. Record real-world outcome events after delivery/submission.
17. Project application lifecycle state.
18. Compute KPI observations with denominator definitions.
19. Generate PromotionCandidate records from selected signals.
20. Run local validation.
21. Run Ontology Vault governance checks.
22. If feedback is private, run redaction/generalization gate.
23. Ask owner decision.
24. Record approved uses, rejection, retirement, or contradiction.
25. Append audit projection.
26. Hand off approved changes to the owning lifecycle route.
```

## Outcome Examples

These examples should appear as fixtures in the first validation slice.

### Example 1: Submitted But Not Reviewed

```text
delivery_envelope
  delivered_as grant_submission
grant_outcome_event(event_kind=portal_validated)
application_lifecycle_state(current_stage=portal_validated)
grant_kpi_observation(metric_kind=submission_validated_rate)
```

Use: track operational completion. Do not infer proposal quality.

### Example 2: Declined After Review

```text
grant_outcome_event(event_kind=feedback_received)
grant_outcome_event(event_kind=declined)
grant_kpi_observation(metric_kind=review_reached_rate)
promotion_candidate(candidate_kind=lesson, privacy_scope=org_scoped)
```

Use: create a private learning candidate. Workspace reuse requires
redaction/generalization and owner approval.

### Example 3: Awarded For Less Than Requested

```text
grant_outcome_event(event_kind=awarded, amount_requested=500000, amount_awarded=300000)
grant_kpi_observation(metric_kind=award_amount_realization)
promotion_candidate(candidate_kind=budget_framing_lesson)
```

Use: learn from budget framing or funder preference. Do not treat the win as
evidence that all claims were strong.

### Example 4: Blocked Before Draft

```text
kgie_preflight
  blocked_by_gate logician_gate_result
logician_gate_result(emits=evidence_gap)
```

Use: no Scribe draft should exist downstream unless a later operator decision or
evidence fix reopens traversal.

### Example 5: Successful Closeout

```text
grant_outcome_event(event_kind=report_accepted)
grant_outcome_event(event_kind=closed_out)
grant_kpi_observation(metric_kind=grant_retention_rate)
promotion_candidate(candidate_kind=stewardship_lesson)
```

Use: feed stewardship and funder relationship learning. Keep org facts private
unless generalized.

### 5. Decision Flow View

```text
Does the event have a source?
  no -> reject candidate generation
  yes -> continue

Is the signal a KPI?
  yes -> require denominator definition and interpretation limits
  no -> continue

Does it contain org-scoped feedback?
  yes -> require redaction/generalization before workspace reuse
  no -> continue

Is there a contradiction path?
  no -> block promotion
  yes -> continue

Does Ontology Vault governance pass?
  no -> candidate remains blocked or rejected
  yes -> owner may decide

Owner approves?
  yes -> record approved_allowed_uses
  no -> record rejected, retired, or contradicted
```

## Grant DAG Translation

GoldenQuill should adapt the research-DAG idea into grant-writing terms. The
unit is not "the proposal" as a static document. The unit is a traceable graph
of funder-fit claims, source evidence, compliance checks, reviewer objections,
draft surfaces, rubric scores, and reuse decisions.

| Research DAG Primitive | GoldenQuill Primitive |
| --- | --- |
| Hypothesis | Funder-fit hypothesis, eligibility claim, budget assumption, reviewer-risk claim. |
| Experiment | Draft section, evidence search, rubric scoring pass, compliance check, outreach test. |
| Replication | Second source, second reviewer seat, cross-family review, prior-award precedent, repeated scoring pass. |
| Objection | Red Team/Judge challenge, admin-risk warning, missing evidence, rule conflict. |
| Extension | Proposal variant, adjacent opportunity, reusable evidence packet, next funder strategy. |
| Consensus | Signed/operator-approved state after evidence and gate checks, not model agreement. |

This means GoldenQuill can learn from each grant run without pretending the
grant document itself is the source of truth.

## KPI Catalog

The first architecture should include KPI families beyond win/loss.

### Quality And Review Movement

Track whether GoldenQuill improves proposal quality before funding.

| KPI | Signal |
| --- | --- |
| `compliance_pass_rate` | Logician pre-submit gates passed / attempted |
| `rubric_coverage_score` | covered rubric criteria / total criteria |
| `reviewer_objection_resolution_rate` | resolved objections / total objections |
| `evidence_gap_resolution_rate` | resolved evidence gaps / identified gaps |
| `section_revision_delta` | score or risk improvement across draft iterations |
| `review_feedback_quality` | coded feedback specificity and actionability |
| `resubmission_delta` | score/review movement from prior submission to next |

### Strategy Fit

Track whether the team applies to the right opportunities.

| KPI | Signal |
| --- | --- |
| `go_no_go_selectivity` | pursued opportunities / researched opportunities |
| `high_match_pursuit_rate` | high-fit pursued / high-fit identified |
| `low_fit_avoidance_rate` | low-fit not pursued / low-fit identified |
| `relationship_present_rate` | submissions with existing funder relationship / submissions |
| `prior_award_alignment` | proposal fit against funder prior-award corpus |
| `program_drift_rate` | funder/RFA requirements that changed after discovery |

### Effort And ROI

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

### Capacity And Relationship

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

| State | Grant Meaning |
| --- | --- |
| application stage | Artifact or application stage, such as submitted, under review, awarded, declined. |
| outcome event | Final source-backed notification, award, decline, withdrawal, report acceptance, or closeout. |
| validation state | Verified claim, compliance pass, source-resolved evidence, reviewer-confirmed feedback. |
| graph authority | Visible authored trace first; structured edges only after validator parity. |
| source truth | No grant truth from proposal prose, dashboard label, or staff memory. |

Evidence-state rules:

```text
application status != outcome truth
review feedback != funding validation
award notification != post-award performance
proposal claim != source fact
dashboard KPI != promotion authority
```

### 6. Dependency Interface View

| Dependency | Interface | Boundary |
| --- | --- | --- |
| Existing evidence packets | `MemoryEvidencePacketRef` | Source reference only; no promotion authority. |
| Outcome sources | `GrantOutcomeEvent` | Portal, agency, email, report, or operator-uploaded source. |
| KPI projection | `GrantKpiObservation` | Read model with denominator semantics. |
| Ontology Vault layer | `OntologyVaultProjection` and `governance_checks` | Promotion governance only; no direct production mutation. |
| Org-vault memory | owner handoff only | Private by default. |
| Card governance | owner handoff only | No signed-card mutation in first slice. |
| Logician gates | validation inputs | Gate failures can create candidates, not promotion. |
| Reflection Packet | later learning handoff | Deferred until learning-loop activation. |

## Data Contracts

### Candidate State Values

```text
captured
candidate
validated
decision_pending
approved
rejected
retired
contradicted
```

### Allowed Use Values

```text
orient
draft_support
decision_input
dashboard
learning_candidate
workspace_reuse
org_private_reuse
citation_candidate
do_not_use
```

### Stage Baseline

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

Each stage has a global score. A funder-family profile may override display
label, score, or stage ordering when the grant family has different workflow
semantics.

## Validation Strategy

Positive fixtures:

- valid source-backed outcome event;
- valid KPI with denominator definition;
- valid candidate with proposed allowed uses;
- valid governance projection;
- valid redacted feedback candidate;
- valid owner decision with approved allowed uses.

Negative fixtures:

- outcome event without source;
- KPI without denominator definition;
- stage-depth treated as award;
- candidate without contradiction path;
- candidate with approved uses before owner decision;
- workspace-global reuse from org-scoped feedback without redaction;
- governance projection missing evidence;
- promotion from KPI threshold alone.

## Implementation Layers

### L0: Fixture-Only Governance Shape

Goal: prove the model can represent the selected decisions.

Deliverables:

- JSON fixtures;
- lightweight validator;
- no runtime integration.

### L1: Local Python Models And Validator

Goal: provide importable GoldenQuill structures and tests.

Deliverables:

- `grant_dag` package;
- dataclasses or typed dictionaries;
- pytest coverage for positive and negative fixtures.

### L2: Workflow Integration Hooks

Goal: connect Scout, Logician, metrics, and operator decisions through explicit
handoffs.

Deliverables:

- event intake hooks;
- KPI projection hooks;
- owner-decision handoff.

### L3: Dashboard And Learning Loop

Goal: expose metrics and candidate learning safely.

Deliverables:

- dashboard read model;
- candidate review queue;
- redaction/generalization workflow;
- owner decision records.

## Risks

| Risk | Mitigation |
| --- | --- |
| KPI optimization distorts behavior. | KPIs create candidates only; owner approval remains required. |
| Private feedback leaks into shared learning. | Org-scoped by default; redaction/generalization gate required. |
| Local model drifts from governance layer. | Projection and governance checks are mandatory validator steps. |
| Evidence packets become promotion authority. | Evidence references stay read-only. |
| Stage scoring overfits federal grants. | Global baseline plus funder-family profile override. |
| Dashboard appears more authoritative than source evidence. | Dashboard observations include interpretation limits and source event refs. |

## Plan-Ready Handoff

Recommended next route: `task-session` for L0 fixture-only governance shape.

First task:

```text
Create GoldenQuill grant_dag promotion-governance fixtures and validator for
outcome events, KPI observations, PromotionCandidate, Ontology Vault projection,
redaction/generalization, and owner decisions.
```

Done criteria:

- positive fixtures pass;
- negative fixtures fail closed;
- no production org memory, signed cards, dashboard, or owner artifacts mutate;
- validator output is deterministic;
- vocabulary stays GoldenQuill-native.
