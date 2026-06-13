---
tags: [goldenquill-promotion-governance, spec, test]
node_type: spec
is_session: false
layer: application
nature: procedural, technical
status: draft
version: 0.1.0
last_updated: 2026-06-08
---

# Test Spec: GoldenQuill Promotion Governance

This test specification defines the fixture-only L0 validator contract for
GoldenQuill Promotion Governance. Tests should use synthetic/demo data only and
must not write production org memory, signed cards, dashboard state, org-vault
data, or canonical Ontology Vault artifacts.

## Fixture Corpus

The first fixture corpus must include:

- an event envelope fixture corpus;
- fake adapter producer fixtures for at least one seat, one outcome source, and one legacy backfill producer;
- a projection receipt fixture corpus;
- replay/idempotency fixtures;
- a pass path from `run_context` to `delivery_envelope`;
- a blocked path where `kgie_preflight` is blocked by `logician_gate_result`;
- a submitted-but-not-reviewed outcome;
- a declined-after-review outcome;
- an awarded-for-less-than-requested outcome;
- a successful post-award report or closeout outcome;
- positive candidate, governance projection, redaction/generalization, and owner
  decision cases;
- negative cases for missing source, missing denominator, premature approved
  uses, missing contradiction path, unsafe feedback reuse, missing projection
  evidence, and KPI-only promotion.
- approved reuse and future-context hydration fixtures.

## Test Matrix

| ID | Test | Validates |
| --- | --- | --- |
| T-OP-AcceptGrantWorkEvent-01 | Valid adapter event projects to expected DAG node and edge. | [AcceptGrantWorkEvent](operations.md#acceptgrantworkevent), [ProjectEventToDag](operations.md#projecteventtodag) |
| T-OP-AcceptGrantWorkEvent-02 | Source-backed adapter event without source fails. | [AcceptGrantWorkEvent R2](operations.md#acceptgrantworkevent) |
| T-OP-AcceptGrantWorkEvent-03 | Duplicate idempotency key with identical content is no-op replay. | [AcceptGrantWorkEvent R5](operations.md#acceptgrantworkevent) |
| T-OP-AcceptGrantWorkEvent-04 | Duplicate idempotency key with changed content blocks as contradiction/residue. | [AcceptGrantWorkEvent R6](operations.md#acceptgrantworkevent) |
| T-OP-AcceptGrantWorkEvent-05 | Adapter event attempting to set approved uses fails. | [AcceptGrantWorkEvent R7](operations.md#acceptgrantworkevent) |
| T-OP-RecordGrantRunEvent-01 | Valid run DAG captures pass path from `run_context` to `delivery_envelope`. | [SPEC execution DAG](SPEC.md#execution-dag-contract), [RecordGrantRunEvent R1-R4](operations.md#recordgrantrunevent) |
| T-ST-GrantRunTraversalState-01 | `kgie_preflight blocked_by_gate logician_gate_result` prevents downstream draft and delivery. | [GrantRunTraversalState GRT-I1](states.md#grantruntraversalstate) |
| T-OP-RecordOutcomeEvent-01 | Outcome event without source fails. | [RecordOutcomeEvent R1](operations.md#recordoutcomeevent) |
| T-PO-EvidenceStatePolicy-01 | Portal validation advances stage but cannot prove final award/decline. | [EvidenceStatePolicy](workflows.md#evidencestatepolicy) |
| T-OP-ComputeKpiObservation-01 | Rate or ratio KPI without denominator definition fails. | [ComputeKpiObservation R1](operations.md#computekpiobservation) |
| T-PO-PromotionAuthorityPolicy-01 | KPI threshold alone cannot create approved reuse. | [PromotionAuthorityPolicy](workflows.md#promotionauthoritypolicy) |
| T-OP-CreatePromotionCandidate-01 | Candidate with `approved_allowed_uses` fails. | [CreatePromotionCandidate R2](operations.md#createpromotioncandidate) |
| T-OP-CreatePromotionCandidate-02 | Candidate without contradiction path fails. | [CreatePromotionCandidate R3](operations.md#createpromotioncandidate) |
| T-OP-ValidatePromotionGovernance-01 | Governance projection missing evidence, review gate, or contradiction path fails. | [ValidatePromotionGovernance R1-R3](operations.md#validatepromotiongovernance) |
| T-MAP-OntologyVaultProjection-01 | Ontology Vault projection remains audit-only in L0. | [OntologyVaultProjection validation](mappings.md#ontologyvaultprojection) |
| T-OP-RedactionGeneralizationGate-01 | Org-scoped feedback cannot become workspace-safe without redaction/generalization and owner approval. | [RedactionGeneralizationGate R1-R3](operations.md#redactiongeneralizationgate) |
| T-ST-PromotionCandidateState-01 | Redacted/generalized org-scoped feedback candidate can proceed to owner decision. | [PromotionCandidateState PCS-I3](states.md#promotioncandidatestate) |
| T-OP-RecordOwnerDecision-01 | Approved owner decision with approved uses passes. | [RecordOwnerDecision R1](operations.md#recordownerdecision) |
| T-OP-RecordOwnerDecision-02 | Rejected, retired, or contradicted decision with approved uses fails. | [RecordOwnerDecision R2](operations.md#recordownerdecision) |
| T-ST-ApplicationLifecycleState-01 | Stage-depth can use global baseline and name a future profile override. | [ApplicationLifecycleState ALS-I3](states.md#applicationlifecyclestate) |
| T-OP-RecordOutcomeEvent-02 | Submitted/portal-validated fixture tracks operational completion only. | [Outcome Examples](SPEC.md#submitted-but-not-reviewed) |
| T-OP-RecordOutcomeEvent-03 | Declined-after-review fixture creates org-scoped candidate only. | [Outcome Examples](SPEC.md#declined-after-review) |
| T-OP-RecordOutcomeEvent-04 | Partial award creates budget-framing candidate without validating all claims. | [Outcome Examples](SPEC.md#awarded-for-less-than-requested) |
| T-OP-RecordOutcomeEvent-05 | Report accepted and closeout feed retention/stewardship candidate with privacy guard. | [Outcome Examples](SPEC.md#successful-closeout) |
| T-OP-PublishApprovedReusePacket-01 | Approved owner decision publishes an approved reuse packet. | [PublishApprovedReusePacket](operations.md#publishapprovedreusepacket) |
| T-OP-HydrateFutureGrantContext-01 | Future context hydration consumes only approved allowed uses. | [HydrateFutureGrantContext](operations.md#hydratefuturegrantcontext) |
| T-DOM-EventProjectionReceipt-01 | Projection without an event projection receipt fails. | [EventProjectionReceipt](domain.md#eventprojectionreceipt) |
| T-OP-ProjectGrantActionFacts-01 | Accepted event and DAG evidence project to a valid action fact. | [ProjectGrantActionFacts](operations.md#projectgrantactionfacts) |
| T-OP-BuildKpiResponseWindow-01 | Action after KPI response is rejected as leakage. | [BuildKpiResponseWindow](operations.md#buildkpiresponsewindow) |
| T-OP-BuildKpiResponseWindow-02 | Pending outcome is censored, not counted as loss. | [analytics-methods.md](analytics-methods.md#time-to-event) |
| T-AM-StatisticalMethodSpec-01 | Method with too few observations emits residue or blocks. | [StatisticalMethodSpec](analytics-methods.md#statisticalmethodspec) |
| T-OP-EvaluateActionKpiAssociation-01 | Naive-positive Red Team association is downgraded by confounding guard. | [analytics-methods.md L0 fixture](analytics-methods.md#l0-required-fixture) |
| T-OP-EvaluateActionKpiAssociation-02 | Quasi-causal method blocks without comparison group. | [analytics-methods.md](analytics-methods.md#difference-in-differences) |
| T-OP-CreateBIInsightCandidate-01 | BI insight candidate cannot carry approved allowed uses. | [CreateBIInsightCandidate](operations.md#createbiinsightcandidate) |
| T-AM-BIInsightCandidate-01 | Small/private aggregate cannot hydrate future context as BI guidance. | [BIInsightCandidate](analytics-methods.md#biinsightcandidate-profile) |
| T-EV-GrantWorkEventAccepted-01 | Operation emits [GrantWorkEventAccepted](events.md#grantworkeventaccepted) with the declared payload on success. | [GrantWorkEventAccepted](events.md#grantworkeventaccepted) |
| T-EV-GrantWorkEventAccepted-02 | Declared consumer of [GrantWorkEventAccepted](events.md#grantworkeventaccepted) handles the event without granting approved reuse. | [GrantWorkEventAccepted](events.md#grantworkeventaccepted) |
| T-EV-GrantWorkEventRejected-01 | Operation emits [GrantWorkEventRejected](events.md#grantworkeventrejected) with the declared payload on success. | [GrantWorkEventRejected](events.md#grantworkeventrejected) |
| T-EV-GrantWorkEventRejected-02 | Declared consumer of [GrantWorkEventRejected](events.md#grantworkeventrejected) handles the event without granting approved reuse. | [GrantWorkEventRejected](events.md#grantworkeventrejected) |
| T-EV-DagProjectionUpdated-01 | Operation emits [DagProjectionUpdated](events.md#dagprojectionupdated) with the declared payload on success. | [DagProjectionUpdated](events.md#dagprojectionupdated) |
| T-EV-DagProjectionUpdated-02 | Declared consumer of [DagProjectionUpdated](events.md#dagprojectionupdated) handles the event without granting approved reuse. | [DagProjectionUpdated](events.md#dagprojectionupdated) |
| T-EV-GrantRunNodeRecorded-01 | Operation emits [GrantRunNodeRecorded](events.md#grantrunnoderecorded) with the declared payload on success. | [GrantRunNodeRecorded](events.md#grantrunnoderecorded) |
| T-EV-GrantRunNodeRecorded-02 | Declared consumer of [GrantRunNodeRecorded](events.md#grantrunnoderecorded) handles the event without granting approved reuse. | [GrantRunNodeRecorded](events.md#grantrunnoderecorded) |
| T-EV-GrantOutcomeEventRecorded-01 | Operation emits [GrantOutcomeEventRecorded](events.md#grantoutcomeeventrecorded) with the declared payload on success. | [GrantOutcomeEventRecorded](events.md#grantoutcomeeventrecorded) |
| T-EV-GrantOutcomeEventRecorded-02 | Declared consumer of [GrantOutcomeEventRecorded](events.md#grantoutcomeeventrecorded) handles the event without granting approved reuse. | [GrantOutcomeEventRecorded](events.md#grantoutcomeeventrecorded) |
| T-EV-KpiObservationComputed-01 | Operation emits [KpiObservationComputed](events.md#kpiobservationcomputed) with the declared payload on success. | [KpiObservationComputed](events.md#kpiobservationcomputed) |
| T-EV-KpiObservationComputed-02 | Declared consumer of [KpiObservationComputed](events.md#kpiobservationcomputed) handles the event without granting approved reuse. | [KpiObservationComputed](events.md#kpiobservationcomputed) |
| T-EV-KpiProjectionUpdated-01 | Operation emits [KpiProjectionUpdated](events.md#kpiprojectionupdated) with the declared payload on success. | [KpiProjectionUpdated](events.md#kpiprojectionupdated) |
| T-EV-KpiProjectionUpdated-02 | Declared consumer of [KpiProjectionUpdated](events.md#kpiprojectionupdated) handles the event without granting approved reuse. | [KpiProjectionUpdated](events.md#kpiprojectionupdated) |
| T-EV-PromotionCandidateCreated-01 | Operation emits [PromotionCandidateCreated](events.md#promotioncandidatecreated) with the declared payload on success. | [PromotionCandidateCreated](events.md#promotioncandidatecreated) |
| T-EV-PromotionCandidateCreated-02 | Declared consumer of [PromotionCandidateCreated](events.md#promotioncandidatecreated) handles the event without granting approved reuse. | [PromotionCandidateCreated](events.md#promotioncandidatecreated) |
| T-EV-PromotionCandidateProjected-01 | Operation emits [PromotionCandidateProjected](events.md#promotioncandidateprojected) with the declared payload on success. | [PromotionCandidateProjected](events.md#promotioncandidateprojected) |
| T-EV-PromotionCandidateProjected-02 | Declared consumer of [PromotionCandidateProjected](events.md#promotioncandidateprojected) handles the event without granting approved reuse. | [PromotionCandidateProjected](events.md#promotioncandidateprojected) |
| T-EV-GovernanceProjectionValidated-01 | Operation emits [GovernanceProjectionValidated](events.md#governanceprojectionvalidated) with the declared payload on success. | [GovernanceProjectionValidated](events.md#governanceprojectionvalidated) |
| T-EV-GovernanceProjectionValidated-02 | Declared consumer of [GovernanceProjectionValidated](events.md#governanceprojectionvalidated) handles the event without granting approved reuse. | [GovernanceProjectionValidated](events.md#governanceprojectionvalidated) |
| T-EV-OwnerDecisionRecorded-01 | Operation emits [OwnerDecisionRecorded](events.md#ownerdecisionrecorded) with the declared payload on success. | [OwnerDecisionRecorded](events.md#ownerdecisionrecorded) |
| T-EV-OwnerDecisionRecorded-02 | Declared consumer of [OwnerDecisionRecorded](events.md#ownerdecisionrecorded) handles the event without granting approved reuse. | [OwnerDecisionRecorded](events.md#ownerdecisionrecorded) |
| T-EV-ApprovedReusePacketPublished-01 | Operation emits [ApprovedReusePacketPublished](events.md#approvedreusepacketpublished) with the declared payload on success. | [ApprovedReusePacketPublished](events.md#approvedreusepacketpublished) |
| T-EV-ApprovedReusePacketPublished-02 | Declared consumer of [ApprovedReusePacketPublished](events.md#approvedreusepacketpublished) handles the event without granting approved reuse. | [ApprovedReusePacketPublished](events.md#approvedreusepacketpublished) |
| T-EV-FutureGrantContextHydrated-01 | Operation emits [FutureGrantContextHydrated](events.md#futuregrantcontexthydrated) with the declared payload on success. | [FutureGrantContextHydrated](events.md#futuregrantcontexthydrated) |
| T-EV-FutureGrantContextHydrated-02 | Declared consumer of [FutureGrantContextHydrated](events.md#futuregrantcontexthydrated) handles the event without granting approved reuse. | [FutureGrantContextHydrated](events.md#futuregrantcontexthydrated) |
| T-MAP-GrantWorkEventToDagNode-01 | [GrantWorkEventToDagNode](mappings.md#grantworkeventtodagnode) transforms source to target shape; required-field validation fails closed. | [GrantWorkEventToDagNode](mappings.md#grantworkeventtodagnode) |
| T-MAP-GrantWorkEventToDagEdge-01 | [GrantWorkEventToDagEdge](mappings.md#grantworkeventtodagedge) transforms source to target shape; required-field validation fails closed. | [GrantWorkEventToDagEdge](mappings.md#grantworkeventtodagedge) |
| T-MAP-GrantWorkEventToOutcomeEvent-01 | [GrantWorkEventToOutcomeEvent](mappings.md#grantworkeventtooutcomeevent) transforms source to target shape; required-field validation fails closed. | [GrantWorkEventToOutcomeEvent](mappings.md#grantworkeventtooutcomeevent) |
| T-MAP-OutcomeEventToLifecycleState-01 | [OutcomeEventToLifecycleState](mappings.md#outcomeeventtolifecyclestate) transforms source to target shape; required-field validation fails closed. | [OutcomeEventToLifecycleState](mappings.md#outcomeeventtolifecyclestate) |
| T-MAP-KpiObservationToPromotionCandidate-01 | [KpiObservationToPromotionCandidate](mappings.md#kpiobservationtopromotioncandidate) transforms source to target shape; required-field validation fails closed. | [KpiObservationToPromotionCandidate](mappings.md#kpiobservationtopromotioncandidate) |
| T-MAP-ActionKpiAssociationToBIInsightCandidate-01 | [ActionKpiAssociationToBIInsightCandidate](mappings.md#actionkpiassociationtobiinsightcandidate) transforms source to target shape; required-field validation fails closed. | [ActionKpiAssociationToBIInsightCandidate](mappings.md#actionkpiassociationtobiinsightcandidate) |
| T-MAP-ActionKpiAssociationToOptimizationChainDefinition-01 | [ActionKpiAssociationToOptimizationChainDefinition](mappings.md#actionkpiassociationtooptimizationchaindefinition) transforms source to target shape; required-field validation fails closed. | [ActionKpiAssociationToOptimizationChainDefinition](mappings.md#actionkpiassociationtooptimizationchaindefinition) |
| T-MAP-OwnerDecisionToApprovedReusePacket-01 | [OwnerDecisionToApprovedReusePacket](mappings.md#ownerdecisiontoapprovedreusepacket) transforms source to target shape; required-field validation fails closed. | [OwnerDecisionToApprovedReusePacket](mappings.md#ownerdecisiontoapprovedreusepacket) |
| T-MAP-ApprovedReusePacketToFutureGrantContext-01 | [ApprovedReusePacketToFutureGrantContext](mappings.md#approvedreusepackettofuturegrantcontext) transforms source to target shape; required-field validation fails closed. | [ApprovedReusePacketToFutureGrantContext](mappings.md#approvedreusepackettofuturegrantcontext) |
| T-WF-GrantRunCaptureLoop-01 | [GrantRunCaptureLoop](workflows.md#grantruncaptureloop) happy path orchestrates its operations in order. | [GrantRunCaptureLoop](workflows.md#grantruncaptureloop) |
| T-WF-GrantRunCaptureLoop-02 | [GrantRunCaptureLoop](workflows.md#grantruncaptureloop) fail-closed path preserves residue without promoting. | [GrantRunCaptureLoop](workflows.md#grantruncaptureloop) |
| T-WF-OutcomeMeasurementLoop-01 | [OutcomeMeasurementLoop](workflows.md#outcomemeasurementloop) happy path orchestrates its operations in order. | [OutcomeMeasurementLoop](workflows.md#outcomemeasurementloop) |
| T-WF-OutcomeMeasurementLoop-02 | [OutcomeMeasurementLoop](workflows.md#outcomemeasurementloop) fail-closed path preserves residue without promoting. | [OutcomeMeasurementLoop](workflows.md#outcomemeasurementloop) |
| T-WF-KnowledgeFeedbackLoop-01 | [KnowledgeFeedbackLoop](workflows.md#knowledgefeedbackloop) happy path orchestrates its operations in order. | [KnowledgeFeedbackLoop](workflows.md#knowledgefeedbackloop) |
| T-WF-KnowledgeFeedbackLoop-02 | [KnowledgeFeedbackLoop](workflows.md#knowledgefeedbackloop) fail-closed path preserves residue without promoting. | [KnowledgeFeedbackLoop](workflows.md#knowledgefeedbackloop) |
| T-WF-GrantPromotionGovernanceWorkflow-01 | [GrantPromotionGovernanceWorkflow](workflows.md#grantpromotiongovernanceworkflow) coordinates the three sub-loops with cross-loop compensation. | [GrantPromotionGovernanceWorkflow](workflows.md#grantpromotiongovernanceworkflow) |
| T-OP-ProjectEventToDag-01 | [ProjectEventToDag](operations.md#projecteventtodag) idempotent replay yields a no-op receipt, not a duplicate node/edge. | [ProjectEventToDag R5](operations.md#projecteventtodag) |
| T-OP-ProjectEventToLifecycleAndKpi-01 | [ProjectEventToLifecycleAndKpi](operations.md#projecteventtolifecycleandkpi) projects accepted events into lifecycle and KPI read models with a receipt. | [ProjectEventToLifecycleAndKpi](operations.md#projecteventtolifecycleandkpi) |
| T-OC-OptimizationChainDefinition-01 | [OptimizationChainDefinition](optimization-chains.md#core-definition) requires all expression forms and a governance route before reuse. | [OptimizationChainDefinition](optimization-chains.md#required-contract-fields) |

## Test Details

### T-OP-AcceptGrantWorkEvent-01 — Valid Adapter Event Projects To DAG

Create a fake [AdapterProducer](domain.md#adapterproducer), a valid
[GrantWorkEventEnvelope](domain.md#grantworkeventenvelope), and a
`run_node_recorded` event. Assert [AcceptGrantWorkEvent](operations.md#acceptgrantworkevent)
passes and [ProjectEventToDag](operations.md#projecteventtodag) creates expected
[GrantRunNode](domain.md#grantrunnode), [GrantRunEdge](domain.md#grantrunedge),
and [EventProjectionReceipt](domain.md#eventprojectionreceipt) records.

### T-OP-AcceptGrantWorkEvent-02 — Adapter Event Without Source Fails

Create a source-backed `outcome_event_recorded` adapter event without
`source_ref`. Assert the event is rejected before outcome, KPI, DAG, candidate,
or memory projection.

### T-OP-AcceptGrantWorkEvent-03 — Idempotent Replay Is No-op

Replay an identical event with the same `idempotency_key` and content hash.
Assert the second acceptance records no duplicate projection and emits a no-op
projection receipt or audit record.

### T-OP-AcceptGrantWorkEvent-04 — Idempotent Conflict Blocks

Replay an event with the same `idempotency_key` but changed content. Assert the
event blocks as contradiction or residue and produces no DAG, KPI, candidate, or
approved reuse projection.

### T-OP-AcceptGrantWorkEvent-05 — Adapter Cannot Set Approved Uses

Create an adapter event payload containing `approved_allowed_uses`. Assert
[AcceptGrantWorkEvent](operations.md#acceptgrantworkevent) rejects it.

### T-OP-RecordGrantRunEvent-01 — Valid Run DAG Pass Path

Fixture includes all minimum execution nodes and edges:

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
logician_gate_result
operator_signoff
delivery_envelope
```

Assert the graph can answer what happened, in what order, and which gate allowed
the next step.

### T-ST-GrantRunTraversalState-01 — Blocked Preflight Stops Traversal

Fixture uses:

```text
kgie_preflight
  blocked_by_gate logician_gate_result
logician_gate_result(emits=evidence_gap)
```

Assert no [scribe_section_draft](domain.md#grantrunnodekind) or
[delivery_envelope](domain.md#grantrunnodekind) exists downstream unless reopen
evidence exists.

### T-OP-ComputeKpiObservation-01 — KPI Requires Denominator Definition

For every rate or ratio [GrantKpiKind](domain.md#grantkpikind), omit
`denominator_definition` and assert the validator rejects the observation.

### T-OP-RedactionGeneralizationGate-01 — Org-Scoped Feedback Blocks Workspace Reuse

Create a declined-after-review candidate with `privacy_scope=single_org`,
feedback refs, and proposed `workspace_reuse`. Assert the candidate remains
blocked until `redaction_status=generalized` and owner approval evidence exists.

### T-OP-RecordOutcomeEvent-01 — Outcome Event Requires Source

Omit [GrantOutcomeEvent](domain.md#grantoutcomeevent).`source_ref` and assert
[RecordOutcomeEvent](operations.md#recordoutcomeevent) rejects the event.

### T-PO-EvidenceStatePolicy-01 — Portal Status Is Not Final Outcome

Use a `portal_validated` event and assert it advances
[ApplicationLifecycleState](states.md#applicationlifecyclestate) only to
`portal_validated`, not `awarded` or `declined`.

### T-PO-PromotionAuthorityPolicy-01 — KPI Cannot Promote Directly

Create a high or low KPI value and assert it can create a
[PromotionCandidate](domain.md#promotioncandidate) only after validation. It
must not create [OwnerDecision](domain.md#ownerdecision) or approved reuse.

### T-OP-CreatePromotionCandidate-01 — Candidate Forbids Approved Uses

Create a candidate with `approved_allowed_uses` and assert
[CreatePromotionCandidate](operations.md#createpromotioncandidate) rejects it.

### T-OP-CreatePromotionCandidate-02 — Candidate Requires Contradiction Path

Create a candidate without `contradiction_path` and assert validation fails
closed.

### T-OP-ValidatePromotionGovernance-01 — Governance Projection Requires Evidence Gate And Contradiction

Omit evidence refs, review gate, and contradiction path in separate fixtures and
assert each one blocks [ValidatePromotionGovernance](operations.md#validatepromotiongovernance).

### T-MAP-OntologyVaultProjection-01 — Projection Does Not Mutate Target Artifacts

Assert [OntologyVaultProjection](mappings.md#ontologyvaultprojection) produces
audit output only in L0 and cannot write to Ontology Vault, cards, org memory,
or production state.

### T-ST-PromotionCandidateState-01 — Valid Redacted Learning Candidate Passes

Create org-scoped feedback with `redaction_status=generalized`, owner approval
evidence, and bounded approved uses. Assert the candidate reaches
`decision_pending`.

### T-OP-RecordOwnerDecision-01 — Owner Decision Owns Approved Uses

Create an approved [OwnerDecision](domain.md#ownerdecision) with
`approved_allowed_uses` and decision source evidence. Assert it passes.

### T-OP-RecordOwnerDecision-02 — Non-Approved Decision Cannot Grant Uses

Create rejected, retired, and contradicted owner decisions with
`approved_allowed_uses`. Assert each fails.

### T-ST-ApplicationLifecycleState-01 — Stage Depth Supports Profile Override

Use the global stage baseline, then add a named funder-family
[StageProfile](domain.md#stageprofile) override with source evidence. Assert the
override is accepted only when the profile is named and sourced.

### T-OP-RecordOutcomeEvent-02 — Submitted But Not Reviewed Does Not Imply Quality

Use the submitted-but-not-reviewed fixture and assert it creates operational
completion metrics only, not proposal-quality validation.

### T-OP-RecordOutcomeEvent-03 — Declined After Review Creates Private Learning

Use a feedback-plus-decline fixture and assert candidate privacy remains
`single_org` unless redaction/generalization and owner approval pass.

### T-OP-RecordOutcomeEvent-04 — Awarded For Less Than Requested Candidate Is Bounded

Use an award event where awarded amount is lower than requested. Assert it feeds
`award_amount_realization` and possible budget-framing learning without
validating every proposal claim.

### T-OP-RecordOutcomeEvent-05 — Successful Closeout Feeds Stewardship Learning

Use `report_accepted` and `closed_out` outcome events and assert the candidate
feeds stewardship and retention learning while keeping org facts private unless
generalized.

### T-OP-PublishApprovedReusePacket-01 — Owner Decision Publishes Approved Reuse Packet

Create an approved [OwnerDecision](domain.md#ownerdecision) with approved allowed
uses and decision source evidence. Assert
[PublishApprovedReusePacket](operations.md#publishapprovedreusepacket) produces
an [ApprovedReusePacket](domain.md#approvedreusepacket) with source refs,
conditions, scope, and contradiction path.

### T-OP-HydrateFutureGrantContext-01 — Future Context Consumes Only Approved Uses

Hydrate future Scout, Scribe, Judge, Logician, Funding Goal, or memory-query
context from an [ApprovedReusePacket](domain.md#approvedreusepacket). Assert
requested use must be present in `approved_allowed_uses`, consumer scope must
fit packet scope, and retired/contradicted packets cannot hydrate context.

### T-DOM-EventProjectionReceipt-01 — Projection Receipt Required

Run event-to-DAG and event-to-KPI projection without an
[EventProjectionReceipt](domain.md#eventprojectionreceipt). Assert projection
fails closed.

### T-OP-ProjectGrantActionFacts-01 — Valid Action Fact Projection

Create an accepted grant-work event with source refs, projection receipt, and
DAG node refs. Assert [ProjectGrantActionFacts](operations.md#projectgrantactionfacts)
emits a [GrantActionFact](analytics-methods.md#grantactionfact) with event,
receipt, DAG, scope, and source lineage.

### T-OP-BuildKpiResponseWindow-01 — Response Window Blocks Temporal Leakage

Create an anchor action whose `occurred_at` is after the KPI response
measurement. Assert [BuildKpiResponseWindow](operations.md#buildkpiresponsewindow)
rejects the window and emits a temporal leakage block.

### T-OP-BuildKpiResponseWindow-02 — Pending Outcome Is Censored

Create a submit-to-decision response window with no final decision yet. Assert
the window status is `censored`, not `declined`, `lost`, or zero-value success.

### T-AM-StatisticalMethodSpec-01 — Sample Gate Blocks Method

Run an [EvaluateActionKpiAssociation](operations.md#evaluateactionkpiassociation)
request with fewer observations than
[StatisticalMethodSpec](analytics-methods.md#statisticalmethodspec).`minimum_observations`.
Assert the method emits `blocked_or_residue` or rejects evaluation.

### T-OP-EvaluateActionKpiAssociation-01 — Naive Red Team Association Is Downgraded

Use the [L0 fixture](analytics-methods.md#l0-required-fixture): 12 grant runs,
Red Team review before final signoff, reviewer objection resolution rate, and a
high-risk confounder. Assert the naive positive association is downgraded to
`correlation_candidate` or `blocked_or_residue`, not promoted.

### T-OP-EvaluateActionKpiAssociation-02 — Quasi-Causal Method Requires Comparison Design

Run a difference-in-differences or propensity matching method without a valid
comparison group. Assert the method blocks and cannot emit
`quasi_causal_candidate`.

### T-OP-CreateBIInsightCandidate-01 — BI Insight Candidate Cannot Approve Reuse

Create a valid [ActionKpiAssociation](analytics-methods.md#actionkpiassociation)
and convert it to a [BIInsightCandidate](analytics-methods.md#biinsightcandidate-profile).
Assert it is a [PromotionCandidate](domain.md#promotioncandidate) profile with
`proposed_allowed_uses` only and no `approved_allowed_uses`.

### T-AM-BIInsightCandidate-01 — Aggregate Privacy Threshold Blocks BI Reuse

Create a BI insight from an aggregate below the minimum group threshold or with
private org-scoped feedback. Assert workspace-safe reuse and future-context
hydration are blocked until privacy and owner-decision rules pass.

## Source Completeness Gate

The generated validator is incomplete if any of these source-of-truth items are
missing from fixtures:

- all mandatory execution node kinds;
- all mandatory execution edge kinds;
- at least one accepted grant-work event;
- at least one rejected grant-work event;
- at least one event projection receipt;
- one idempotent replay no-op;
- one duplicate idempotency conflict;
- at least one source-backed outcome event;
- at least one denominator-safe KPI observation;
- one candidate with `proposed_allowed_uses`;
- one owner decision with `approved_allowed_uses`;
- one governance projection;
- one redaction/generalization case;
- one negative KPI-only promotion attempt.
- one approved reuse packet;
- one future-context hydration case.
- one valid grant action fact;
- one KPI response window;
- one method sample-gate failure;
- one temporal leakage block;
- one censored pending outcome;
- one BI insight candidate without approved uses;
- one aggregate privacy threshold block.

## Out of Scope

- Live grant portal integration.
- Dashboard UI.
- Production org-vault mutation.
- Signed-card mutation.
- Canonical Ontology Vault mutation.
- Real client or org data.

## Connections

| Document | Type | Description |
| --- | --- | --- |
| [SPEC.md](SPEC.md) | `derives-from` | Feature source of truth. |
| [operations.md](operations.md) | `validates` | Operation rules and error states. |
| [states.md](states.md) | `validates` | State transitions and invariants. |
| [mappings.md](mappings.md) | `validates` | Ontology Vault projection and KPI/candidate mappings. |
| [events.md](events.md) | `validates` | Event-spine, projection, approved reuse, and future-context events. |
| [observability.md](observability.md) | `observes` | Event acceptance, projection, replay, conflict, governance, and hydration metrics. |
| [analytics-methods.md](analytics-methods.md) | `defines` | Analytics method implementation registry, facts, response windows, method specs, association outputs, and BI insight candidate profile. |
