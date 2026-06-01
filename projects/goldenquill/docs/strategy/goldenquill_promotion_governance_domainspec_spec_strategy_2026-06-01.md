---
title: GoldenQuill Promotion Governance DomainSpec Strategy
date: 2026-06-01
status: strategy-ready
route: context-builder fanout to domainspec-spec-writer
target_feature: goldenquill-promotion-governance
dispatch: goldenquill_promotion_governance_domainspec_spec_strategy_2026-06-01.dispatch.json
---

# GoldenQuill Promotion Governance DomainSpec Strategy

## Objective

Create DomainSpec feature docs for GoldenQuill promotion governance from the
proposal packet already produced on 2026-06-01.

The target DomainSpec feature should be:

```text
implementation/domainspec/docs/features/goldenquill-promotion-governance/
```

Recommended initial artifact set:

- `SPEC.md`
- `architecture.md`
- `domain.md`
- `operations.md`
- `states.md`
- `events.md`
- `workflows.md`
- `mappings.md`
- `observability.md`
- `glossary.md`
- `TEST-SPEC.md`

The docs should describe the GoldenQuill feature in product/domain language. They
should not import historical external-method vocabulary into the implementation
surface.

## Why A Context-Builder Fanout

The current proposal packet is broad. A direct spec-writing pass risks mixing
architecture, KPI research, operator decisions, vocabulary cleanup, and
DomainSpec template obligations into one oversized context. The safer route is a
fanout of focused `context-builder` packs, each with selector-level evidence and
clear obligations.

The fanout should produce six context packs:

| Pack | Focus | Primary Question |
| --- | --- | --- |
| CB-01 | Proposal and architecture | What is the feature boundary and first slice? |
| CB-02 | Execution DAG | What happened in a grant run, in what order, and which gate allowed or blocked the next step? |
| CB-03 | KPI and evidence-state model | What real-world evidence, outcomes, and KPIs should be modeled? |
| CB-04 | Governance decisions | Which blocker decisions are already resolved and which constraints are locked? |
| CB-05 | DomainSpec templates | What must the spec writer produce and validate? |
| CB-06 | Vocabulary policy | Which terms are allowed in implementation-facing docs? |

The parent synthesis then turns those packs into a spec-writer handoff.

## Evidence Map

| Evidence | Selectors To Pull | Why It Matters |
| --- | --- | --- |
| `projects/goldenquill/docs/strategy/goldenquill_promotion_governance_proposal_2026-06-01.md` | Proposal, first slice, acceptance criteria, KPI families, evidence-state rules, vocabulary policy | Client-facing summary and implementation boundary |
| `projects/goldenquill/docs/strategy/goldenquill_promotion_governance_architecture_design_2026-06-01.md` | Executive summary, source decisions, execution DAG nodes/edges, low-level components, workflow, outcomes, validation strategy, implementation layers | Main source for DomainSpec concept registry, operations, workflows, states, events, and architecture |
| `projects/goldenquill/docs/decisions/goldenquill-promotion-mechanism-open-gaps.md` | Gate result, DG-001 through DG-006, assumptions safe for refine | Locked decisions and unsafe next steps |
| `projects/goldenquill/docs/decisions/goldenquill-promotion-mechanism-interrogation.md` | Interview order and decision log | Human-answer provenance for decisions |
| `projects/goldenquill/docs/strategy/goldenquill_promotion_mechanism_refresh_report_2026-06-01.md` | Online research baseline, KPI families, evidence-state discipline, promotion model refresh | Grant-writing KPI and real-world evidence model |
| `projects/goldenquill/docs/strategy/goldenquill_ontology_dag_grant_research_synthesis_2026-06-01.md` | Core finding, execution DAG, ontology DAG, Paradigma adaptation, authority model | Graph model and grant-DAG translation |
| `projects/goldenquill/docs/strategy/goldenquill_promotion_governance_vocabulary_revision_proposal_2026-06-01.md` | Keep, replace, revision scope, acceptance criteria | Prevents vocabulary drift in active docs |
| `implementation/domainspec/CHANGELOG.md` | Latest framework changes, especially architecture and glossary requirements | Required initial read for the spec writer |
| `implementation/domainspec/templates/SPEC.md` | Module ownership, capabilities, concept registry, concept graph, aspect docs | Shape of the entrypoint spec |
| `implementation/domainspec/templates/architecture.md` | Six architecture views, source contracts, gate result | Shape of the required architecture companion |
| `implementation/domainspec/.codex/agents/domainspec-spec-writer.agent.toml` | Discovery precondition, spec workflow, signal obligations | Execution contract for DomainSpec spec writing |

## Target Feature Boundary

The DomainSpec feature owns the specification for a GoldenQuill-local promotion
governance layer under `grant_dag`.

It should cover:

- grant-run execution DAG;
- source-backed outcome events;
- application lifecycle state;
- KPI observations with denominator semantics;
- promotion candidates;
- owner decisions;
- Ontology Vault projection/governance checks;
- redaction/generalization for org-scoped feedback;
- fixture-only first validator expectations.

It should explicitly exclude:

- production org-vault mutation;
- signed-card mutation;
- dashboard implementation;
- automatic promotion from KPIs;
- production importers;
- canonical Ontology Vault template mutation.

## DomainSpec Concept Seed

Recommended concept IDs for `SPEC.md`:

| Concept | ID | Type |
| --- | --- | --- |
| GrantRunNode | `goldenquill-promotion-governance.GrantRunNode` | Entity |
| GrantRunEdge | `goldenquill-promotion-governance.GrantRunEdge` | Entity |
| MemoryEvidencePacketRef | `goldenquill-promotion-governance.MemoryEvidencePacketRef` | Value Object |
| GrantOutcomeEvent | `goldenquill-promotion-governance.GrantOutcomeEvent` | Event |
| ApplicationLifecycleState | `goldenquill-promotion-governance.ApplicationLifecycleState` | State Machine |
| GrantKpiObservation | `goldenquill-promotion-governance.GrantKpiObservation` | Entity |
| PromotionCandidate | `goldenquill-promotion-governance.PromotionCandidate` | Entity |
| OwnerDecision | `goldenquill-promotion-governance.OwnerDecision` | Entity |
| OntologyVaultProjection | `goldenquill-promotion-governance.OntologyVaultProjection` | Mapping |
| RedactionGeneralizationGate | `goldenquill-promotion-governance.RedactionGeneralizationGate` | Operation |
| ValidatePromotionGovernance | `goldenquill-promotion-governance.ValidatePromotionGovernance` | Operation |
| RecordGrantRunEvent | `goldenquill-promotion-governance.RecordGrantRunEvent` | Operation |
| RecordOutcomeEvent | `goldenquill-promotion-governance.RecordOutcomeEvent` | Operation |
| ComputeKpiObservation | `goldenquill-promotion-governance.ComputeKpiObservation` | Operation |
| CreatePromotionCandidate | `goldenquill-promotion-governance.CreatePromotionCandidate` | Operation |
| RecordOwnerDecision | `goldenquill-promotion-governance.RecordOwnerDecision` | Operation |

## Feature Concept Graph Seed

Use canonical DomainSpec edge names where available. If a relationship is not in
`RELATIONSHIPS.md`, the spec writer should either choose the closest canonical
edge or record a spec gap before inventing a new one.

Candidate graph rows:

| From | Edge | To | Evidence |
| --- | --- | --- | --- |
| `goldenquill-promotion-governance.RecordGrantRunEvent` | produces | `goldenquill-promotion-governance.GrantRunNode` | `operations.md#recordgrantrunevent` |
| `goldenquill-promotion-governance.GrantRunEdge` | links | `goldenquill-promotion-governance.GrantRunNode` | `domain.md#grantrunedge` |
| `goldenquill-promotion-governance.RecordOutcomeEvent` | produces | `goldenquill-promotion-governance.GrantOutcomeEvent` | `operations.md#recordoutcomeevent` |
| `goldenquill-promotion-governance.GrantOutcomeEvent` | produces | `goldenquill-promotion-governance.ApplicationLifecycleState` | `events.md#grantoutcomeevent` |
| `goldenquill-promotion-governance.ComputeKpiObservation` | produces | `goldenquill-promotion-governance.GrantKpiObservation` | `operations.md#computekpiobservation` |
| `goldenquill-promotion-governance.GrantKpiObservation` | triggers | `goldenquill-promotion-governance.CreatePromotionCandidate` | `operations.md#createpromotioncandidate` |
| `goldenquill-promotion-governance.CreatePromotionCandidate` | produces | `goldenquill-promotion-governance.PromotionCandidate` | `operations.md#createpromotioncandidate` |
| `goldenquill-promotion-governance.PromotionCandidate` | mapped-by | `goldenquill-promotion-governance.OntologyVaultProjection` | `mappings.md#ontologyvaultprojection` |
| `goldenquill-promotion-governance.RedactionGeneralizationGate` | guards | `goldenquill-promotion-governance.PromotionCandidate` | `operations.md#redactiongeneralizationgate` |
| `goldenquill-promotion-governance.RecordOwnerDecision` | produces | `goldenquill-promotion-governance.OwnerDecision` | `operations.md#recordownerdecision` |

## Aspect Doc Intent

`SPEC.md` should be capability-led:

- capture grant run DAG;
- capture real-world outcome evidence;
- compute evidence-safe KPIs;
- create promotion candidates;
- apply Ontology Vault governance;
- record owner decisions.

`architecture.md` should follow the six-view DomainSpec template and must include
the first-slice boundary: fixture-only validator before dashboard, production
memory, org-vault, or signed-card changes.

`domain.md` should define the structural concepts, enums, and value objects:

- execution node kinds;
- execution edge kinds;
- outcome event kinds;
- lifecycle stage baseline;
- candidate states;
- allowed-use values;
- validation states;
- privacy scopes.

`operations.md` should define validation and mutation-like domain operations,
including rules for fail-closed negative cases.

`states.md` should define at least:

- `ApplicationLifecycleState`;
- `PromotionCandidate` lifecycle;
- `OwnerDecision` result states.

`events.md` should define source-backed events such as `GrantOutcomeEvent`,
`PromotionCandidateCreated`, `GovernanceProjectionValidated`, and
`OwnerDecisionRecorded`.

`workflows.md` should encode the run path from `run_context` to
`delivery_envelope`, then outcome capture through owner decision.

`mappings.md` should define the `OntologyVaultProjection` from local candidate
shape into governance-compatible fields.

`observability.md` should include KPI and validator signals, but clearly state
that dashboard observations do not create promotion authority.

`TEST-SPEC.md` should derive positive and negative fixture tests from the
proposal acceptance criteria.

## DomainSpec Writer Gate

The `domainspec-spec-writer` contract requires discovery lookup before authoring.
This route should handle that in one of two ways:

1. Preferred: persist the fanout synthesis as:

   ```text
   implementation/domainspec/docs/features/goldenquill-promotion-governance/discovery/goldenquill-promotion-governance.md
   ```

   Then run the spec writer with that discovery present.

2. Acceptable if the operator wants immediate spec authoring: pass
   `skip_discovery: true` with waiver reason:

   ```text
   GoldenQuill promotion governance already has a dated proposal packet and context-builder fanout synthesis.
   ```

The preferred route is better because it keeps the research packet visible to
future DomainSpec updates.

## Dispatch Route

Use the paired dispatch artifact:

```text
projects/goldenquill/docs/strategy/goldenquill_promotion_governance_domainspec_spec_strategy_2026-06-01.dispatch.json
```

The dispatch validates a proposal-only route:

1. context-builder fanout creates six packs;
2. synthesis joins them into a DomainSpec writer handoff;
3. human gate chooses discovery-persist or skip-discovery waiver;
4. domainspec-spec-writer creates the feature docs;
5. verification checks links, concept IDs, vocabulary, and gate coverage.

## Stop Conditions

Block the spec-writing run if:

- the execution DAG nodes or edges are omitted;
- KPI observations are written as promotion authority;
- org-scoped feedback can become workspace-safe without redaction and owner approval;
- `approved_allowed_uses` appears before `OwnerDecision`;
- the Ontology Vault layer is treated as a direct production mutation path;
- DomainSpec docs use external method vocabulary in active implementation-facing sections;
- discovery is missing and no explicit waiver is supplied.

## Recommended Next Command

Run the fanout first, then author the specs:

```text
context-builder goldenquill-promotion-governance-domainspec --mode deep --strict --emit both --handoff runtime
domainspec-spec-writer goldenquill-promotion-governance
```

If no discovery artifact is persisted before the second command, include the
explicit skip-discovery waiver described above.
