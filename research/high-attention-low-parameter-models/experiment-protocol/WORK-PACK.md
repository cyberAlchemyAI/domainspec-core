---
module: high-attention-low-parameter-experiment-protocol
version: 0.1.0-draft
status: decision-gated
updatedAt: 2026-07-18
docType: work-pack
observedCapability: invoke
invokeMode: plan
---

# WORK-PACK: High-Attention, Low-Parameter Experiment Protocol

## Purpose

Canonical executable plan and current readiness surface for materializing and
running the experiment defined by [SPEC.md](SPEC.md). Invoke authored this plan;
it does not execute the tasks.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | block | Human decisions and runnable-witness artifacts are unresolved. |
| complexity | high | More than five tasks/two artifacts, external GPU/model dependencies, and multiple acceptance-critical gates. |
| outputMode | split | Task, wave, and shared contracts are required. |
| executionPackRef | [EXECUTION-PACK.md](EXECUTION-PACK.md) | Cross-task choreography. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0–L3 governance. |
| dispatchTechniqueTrace | [DISPATCH.json](DISPATCH.json) and [trace below](#dispatch-technique-trace) | Full cross-capability route. |
| distillValidationStatus | pass | Plan shape closes and recomposes; execution gate remains independently blocked. |
| swuAtomicityStatus | pass | Fourteen SWUs, zero task-shaped units. |
| firstUnitNarrownessStatus | pass | `SWU-HALP-001` is the narrowest reversible semantic decision. |
| activeLayerWindow | L0 | Decisions, contracts, fixtures, and offline witness only. |
| lastUpdatedAt | 2026-07-18 | Authoring date. |
| readinessProfile | pilot | Stack-specific research witness, not benchmark product. |

## Objective Summary

- Objective: materialize a falsifiable, repeatable paired experiment whose
  semantic, platform, inference, and resource claims remain separately auditable.
- Primary inputs: approved spec/design, accepted methodology findings, decision
  records, local Invoke/Experiment Harness contracts.
- Success condition: the selected layer's promotion evidence passes and every
  run/score/analysis claim resolves to immutable source artifacts and receipts.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-000 | Approved decisions and machine contracts. | L0 | [W0](work-pack/waves/W0-foundation.md) | none | Decision approvals; schema/validator fixtures. |
| S-001 | Deterministic offline fixture/render/score witness. | L0 | [W1](work-pack/waves/W1-offline-witness.md) | S-000 | Byte-identical rebuild and exact score receipts. |
| S-002 | One admitted stack and repeatable measurement smoke. | L1 | [W2](work-pack/waves/W2-measurement-smoke.md) | S-000, S-001 | Compatibility, capacity, telemetry, repeatability receipts. |
| S-003 | Paired within-family decision pilot and phase verdict. | L2 | [W3](work-pack/waves/W3-decision-pilot.md) | S-002 | Paired analysis, uncertainty, frontier, gate decision. |
| S-004 | Audited closeout and one optional extension route. | L3 | [W4](work-pack/waves/W4-closeout-extension.md) | S-003 | Alignment audit, license boundary, justified extension decision. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [TASK-HALP-DECISIONS](work-pack/tasks/TASK-HALP-DECISIONS.md) | Freeze five approval-bearing decision families. | L0 | high | [W0](work-pack/waves/W0-foundation.md) | research findings, spec readiness | blocked-human | not-started |
| [TASK-HALP-CONTRACTS](work-pack/tasks/TASK-HALP-CONTRACTS.md) | Implement schemas and validators for protocol, cells, and receipts. | L0 | medium | [W0](work-pack/waves/W0-foundation.md) | spec/domain/interfaces | blocked-by-decisions | not-started |
| [TASK-HALP-FIXTURES](work-pack/tasks/TASK-HALP-FIXTURES.md) | Implement deterministic generator, renderer, provenance, and scorer. | L0 | high | [W1](work-pack/waves/W1-offline-witness.md) | workload and mapping contracts | blocked-by-contracts | not-started |
| [TASK-HALP-ADMISSION](work-pack/tasks/TASK-HALP-ADMISSION.md) | Admit exact model/runtime/length cells. | L1 | high | [W2](work-pack/waves/W2-measurement-smoke.md) | platform decisions and interfaces | blocked-human/resource | not-started |
| [TASK-HALP-WITNESS](work-pack/tasks/TASK-HALP-WITNESS.md) | Close the offline fixture-to-score witness. | L0 | medium | [W1](work-pack/waves/W1-offline-witness.md) | contracts and fixtures | blocked-by-fixtures | not-started |
| [TASK-HALP-MEASURE](work-pack/tasks/TASK-HALP-MEASURE.md) | Run one-stack smoke, then paired decision cells. | L1/L2 | high | [W2](work-pack/waves/W2-measurement-smoke.md), [W3](work-pack/waves/W3-decision-pilot.md) | admitted matrix | blocked-by-admission | not-started |
| [TASK-HALP-ANALYZE](work-pack/tasks/TASK-HALP-ANALYZE.md) | Execute frozen paired analysis and resource/phase gate. | L2 | high | [W3](work-pack/waves/W3-decision-pilot.md) | complete eligible receipts | blocked-by-measurement | not-started |
| [TASK-HALP-VERIFY](work-pack/tasks/TASK-HALP-VERIFY.md) | Audit alignment, receipts, claims, and extension readiness. | L3 | medium | [W4](work-pack/waves/W4-closeout-extension.md) | all prior tasks | ready-after-analysis | not-started |

## Shared SWU Manifest

| SWU ID | Parent Task | Primary behavior/decision | Layer | Dependencies | Handoff |
| --- | --- | --- | --- | --- | --- |
| SWU-HALP-001 | [DECISIONS](work-pack/tasks/TASK-HALP-DECISIONS.md) | Freeze claim boundary and primary estimands. | L0 | none | selected, blocked-human |
| SWU-HALP-002 | [DECISIONS](work-pack/tasks/TASK-HALP-DECISIONS.md) | Freeze margins, uncertainty, multiplicity, N, and repetitions. | L0 | 001 | blocked-human |
| SWU-HALP-003 | [DECISIONS](work-pack/tasks/TASK-HALP-DECISIONS.md) | Freeze workload, arms, lengths, interference, and retrieval role. | L0 | 001 | blocked-human |
| SWU-HALP-004 | [DECISIONS](work-pack/tasks/TASK-HALP-DECISIONS.md) | Freeze checkpoint/runtime/backend admission policy. | L0 | 001 | blocked-human |
| SWU-HALP-005 | [DECISIONS](work-pack/tasks/TASK-HALP-DECISIONS.md) | Freeze resource, evidence-retention, license, and publication boundaries. | L0 | 001 | blocked-human |
| SWU-HALP-006 | [CONTRACTS](work-pack/tasks/TASK-HALP-CONTRACTS.md) | Materialize schemas and deterministic validators. | L0 | 001–005 | blocked |
| SWU-HALP-007 | [FIXTURES](work-pack/tasks/TASK-HALP-FIXTURES.md) | Generate deterministic semantic fixtures and provenance. | L0 | 006 | blocked |
| SWU-HALP-008 | [FIXTURES](work-pack/tasks/TASK-HALP-FIXTURES.md) | Render arms/rotations and score stored outputs deterministically. | L0 | 006, 007 | blocked |
| SWU-HALP-009 | [ADMISSION](work-pack/tasks/TASK-HALP-ADMISSION.md) | Produce exact stack compatibility and capacity witnesses. | L1 | 003–006 | blocked |
| SWU-HALP-010 | [WITNESS](work-pack/tasks/TASK-HALP-WITNESS.md) | Close one offline fixture-to-score end-to-end witness. | L0 | 007, 008 | blocked |
| SWU-HALP-011 | [MEASURE](work-pack/tasks/TASK-HALP-MEASURE.md) | Execute a tiny one-stack measurement smoke. | L1 | 009, 010 | blocked |
| SWU-HALP-012 | [MEASURE](work-pack/tasks/TASK-HALP-MEASURE.md) | Execute frozen paired 1B/3B decision-pilot cells. | L2 | 002–005, 011 | blocked |
| SWU-HALP-013 | [ANALYZE](work-pack/tasks/TASK-HALP-ANALYZE.md) | Produce frozen paired behavioral analysis. | L2 | 012 | blocked |
| SWU-HALP-014 | [ANALYZE](work-pack/tasks/TASK-HALP-ANALYZE.md) | Produce resource frontier and phase decision. | L2/L3 | 013 | blocked |

## SWU Atomicity Review

| SWU range | Candidate child units considered | Retained-boundary rationale | Verdict |
| --- | --- | --- | --- |
| 001–005 | Individual fields within each decision family | Fields jointly define one approval question and cannot independently authorize downstream behavior. Families remain separate because each can be approved/rejected independently. | pass |
| 006 | One schema per artifact | Shared identity and validation invariants must close together for any downstream fixture/run to be reviewable; separate files remain internal commits, not separately useful SWUs. | pass |
| 007 | Generator, splits, provenance | A generated fixture is inadmissible without its split and provenance receipt; the three pieces form one semantic artifact. | pass |
| 008 | Renderer and scorer | Retained together only for the arm/output grammar contract; acceptance requires stored positive/negative outputs through the same grammar. | pass |
| 009 | Compatibility smoke and capacity probe | Neither independently admits a model/length cell; admission requires both under the exact stack. | pass |
| 010 | Fixture build, render, stored output, score | Smaller pieces already pass in 007/008; this SWU owns only their end-to-end recomposition proof. | pass |
| 011 | One model, multiple smoke attempts | Attempts are repetitions of one measurement behavior and share one acceptance boundary. | pass |
| 012 | Matrix shards | Shards may execute separately, but none supports the decision-pilot acceptance boundary without complete required pairs; shard scheduling is internal. | pass |
| 013 | Individual estimands | They share one frozen inclusion/pairing/multiplicity population; independent release would permit inconsistent analysis populations. | pass |
| 014 | Frontier and phase decision | The gate cannot be reviewed without the frontier and the frontier has no lifecycle consequence without the declared gate. | pass |

Task-shaped SWU count: 0. `SWU-HALP-001` is the narrowest reversible first
unit because it records one semantic decision without creating runtime or code
commitments.

## SWU Execution Handoff

| SWU | Source anchors and related context | Write scope | Acceptance evidence | Validation surface | Owner |
| --- | --- | --- | --- | --- | --- |
| 001 | `SPEC.md#normative-experiment-boundary`; findings `#repaired-constructs-and-estimands` | `configs/decisions/claim-estimands.json` | approval-bearing decision record | schema/review check | manual |
| 002 | findings `#mandatory-closure-before-any-run`; `operations.md#analyzephase` | `configs/decisions/inference.json` | thresholds/N/power rationale | schema + independent statistical review | manual |
| 003 | findings `#smallest-coherent-specification-target`; `domain.md#promptarm` | `configs/decisions/workload-matrix.json` | frozen primary matrix | schema + matrix projection review | manual |
| 004 | findings platform requirements; `domain.md#modelstack` | `configs/decisions/platform-admission.json` | frozen admission policy | schema + platform review | manual |
| 005 | findings budget/license requirements; `domain.md#resourcefrontier` | `configs/decisions/resource-publication.json` | frozen resource/evidence/license boundary | schema + owner review | manual |
| 006 | `domain.md`; `interfaces.md#artifact-contracts`; `states.md` | `schemas/`, `src/validate/`, `fixtures/contracts/` | passing/failing validator fixtures | deterministic validation command | local-fallback |
| 007 | `mappings.md#fixturetoprompt`; research workload sections | `src/fixtures/`, `fixtures/semantic/`, `manifests/fixture-manifest.json` | byte-identical corpus and provenance | generator tests + hash comparison | subagent |
| 008 | `operations.md#rendertrialcell`; `operations.md#scoretrial` | `src/render/`, `src/score/`, `fixtures/render-score/` | exact render/scorer fixtures | parser/scorer tests | subagent |
| 009 | `operations.md#admitmodelstack`; `ARCHITECTURE-BUNDLE.md#6-dependency-and-interface-view` | `src/admission/`, `manifests/model-stacks/`, `capacity/` | compatibility + capacity receipts | smoke/capacity validator | local-fallback |
| 010 | `ARCHITECTURE-BUNDLE.md#4-workflow-process-view`; SWUs 006–008 | `fixtures/offline-witness/`, `reports/l0/` | one complete content-addressed chain | clean rebuild command | local-fallback |
| 011 | `IMPLEMENTATION-LAYERING.md` L1; `operations.md#executetrialcell` | `src/run-adapter/`, `trials/smoke/`, `runs/smoke/` | repeatable systems receipts | Experiment Harness smoke validation | local-fallback |
| 012 | frozen protocol/matrix; `WORK-PACK.md` S-003 | `trials/decision-pilot/`, `runs/decision-pilot/`, `scores/decision-pilot/` | complete paired receipt set | matrix/receipt eligibility validator | subagent |
| 013 | `mappings.md#scorestocontrasts`; inference decision | `src/analysis/`, `analysis/decision-pilot/` | frozen estimands + uncertainty | analysis fixtures/recomputation | subagent |
| 014 | `queries.md#getresourcefrontier`; `operations.md#evaluatephasegate` | `src/frontier/`, `analysis/frontier/`, `reports/phase-gate/` | frontier + signed gate decision | dominance fixtures + review | manual |

Every task contract below expands dependencies, source anchors, related context,
done criteria, validation, failure modes, and the required receipt shape.

## Blockers And Gap Ledger

| Blocker | Scope | Description | Owner | Repair route |
| --- | --- | --- | --- | --- |
| HALP-B001 | SWU 001–005 | Human experiment choices are not approved. | experiment owner | Execute decision SWUs one question/record at a time. |
| HALP-B002 | SWU 006–010 | Runnable-witness artifacts do not exist. | Task Session | Build after decision records freeze. |
| HALP-B003 | SWU 009–012 | Checkpoint access, exact runtime, single-H100 allocation, and capacity are unproven. | platform/resource owner | Admission and resource receipts. |
| HALP-B004 | SWU 013–014 | Numeric inference and resource boundaries are unfrozen. | experiment/analysis owner | SWU 002 and 005 approvals. |
| HALP-B005 | repository | Large evidence storage policy is unresolved. | repository owner | Choose tracked/ignored/external paths before run artifacts. |

Full ownership and source detail: [cross-task gaps](work-pack/shared/cross-task-gaps.md).

## Dispatch Technique Trace

| Technique | Applied To | Validation expectation | Status |
| --- | --- | --- | --- |
| `sequence` | define -> design -> plan -> Distill -> execution handoff | every stage consumes explicit artifacts | pass |
| `scu_swu_reduction` | fourteen SWUs | each owns one behavior/decision and review boundary | pass |
| `recomposition_proof` | SWUs -> tasks -> waves -> spec | traceability map covers every capability and layer | pass |
| `validation_loop` | every slice/SWU | evidence command or review check exists | pass |
| `owner_boundary_check` | Invoke/Task Session/Experiment Harness/human/Inventory | no false execution or promotion authority | pass |
| `handle_handoff` | task/SWU source links | execution consumes paths/selectors | pass |
| `residue_ledger` | blockers/gaps | every gap has owner and repair route | pass |
| `execution_receipt_handoff` | Task Session and Experiment Harness | structured result/receipt contract required | pass |
| `authority_split_gate` | authoring, execution, evidence, promotion | unresolved owner blocks | pass |
| `concrete_path_evidence` | work-pack navigation | no glob-only acceptance claims | pass |
| `artifact_contract_bridge` | schemas and receipts | artifacts validate without claiming promotion | pass |
| `observability_grouping` | route and later runs | dispatch/run identifiers group signals | pass |

Full dispatch: [DISPATCH.json](DISPATCH.json).

## Distill Validation

| Check | Result | Evidence |
| --- | --- | --- |
| Smallest coherent unit | pass | One protocol instance; first executable decision is SWU 001. |
| SWU atomicity/split analysis | pass | Fourteen reviewed SWUs; zero task-shaped units. |
| First-unit narrowness | pass | One reversible claim/estimand decision before implementation. |
| Recomposition proof | pass | [Traceability](work-pack/shared/traceability.md) maps spec -> layer -> wave -> task -> SWU. |
| Hidden acceptance-critical gaps | pass-as-exposed | Five blockers are explicit and keep the work-pack gate blocked. |
| Deferred complexity | pass | Retrieval, Phi, realistic data, 128K, portability, and product scale stay L3/deferred. |
| Navigation | pass | Work-pack links every task, wave, shared contract, and source. |

Detailed role trace: [DISTILL-VALIDATION.md](DISTILL-VALIDATION.md).

## Validation Strategy

| Slice | Validation family | Required evidence |
| --- | --- | --- |
| S-000 | schema, semantic, decision review | positive/negative fixtures and approvals |
| S-001 | determinism, metamorphic rendering, scorer correctness | byte/hash repeat and stored-output scores |
| S-002 | compatibility, capacity, telemetry, repeatability | stack/capacity/run receipts |
| S-003 | matrix completeness, pairing, uncertainty, multiplicity | eligibility and analysis receipts |
| S-004 | alignment, license, claim, evidence audit | closeout and extension decision |

No validation command may substitute a missing human approval, capacity witness,
or resource authorization.

## Required Links

- [Execution pack](EXECUTION-PACK.md)
- [Plan transport](PLAN-TRANSPORT.md)
- [Shared context](work-pack/shared/context.md)
- [Cross-task decisions](work-pack/shared/cross-task-decisions.md)
- [Cross-task gaps](work-pack/shared/cross-task-gaps.md)
- [Traceability](work-pack/shared/traceability.md)
- [W0 foundation](work-pack/waves/W0-foundation.md)
- [W1 offline witness](work-pack/waves/W1-offline-witness.md)
- [W2 measurement smoke](work-pack/waves/W2-measurement-smoke.md)
- [W3 decision pilot](work-pack/waves/W3-decision-pilot.md)
- [W4 closeout/extension](work-pack/waves/W4-closeout-extension.md)

## Gate Checks

1. The work-pack gate remains block until HALP-B001 through B005 are closed for
   the selected layer.
2. Only `SWU-HALP-001` is selected; no multi-SWU mutation handoff is authorized.
3. Context Builder must create strict Markdown + JSON/index session evidence at
   execution time; Invoke does not pre-generate it.
4. Task Session implements one selected SWU; Experiment Harness owns model runs.
5. Every spawned subagent must return and close with the task-local receipt.
6. Layer promotion requires the prior layer's exit evidence.
7. Inventory/definition promotion requires its own owner and explicit route.

## Recommended Next Route

Decision gate/interrogation for `SWU-HALP-001`. After its approval receipt,
`task-session` may execute that one SWU. No experiment run is authorized.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-07-18 | Initial Invoke define/design/plan package. | Codex |
