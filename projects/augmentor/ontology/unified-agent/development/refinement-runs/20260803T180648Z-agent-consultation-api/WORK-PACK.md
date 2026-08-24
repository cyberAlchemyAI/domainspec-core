---
module: augmentor-agent-consultation-api
version: candidate-0.1.0
status: one-go-l0-ready-pending-epoch-approval
updatedAt: 2026-08-03
docType: work-pack
---

# WORK-PACK: Agent Consultation API

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | approval-pending | Exact L0 material and runtime contracts are prepared; the frozen epoch still requires digest-bound human approval. |
| complexity | medium | Seven-unit L0 execution frontier plus separately gated later layers. |
| outputMode | split | Task and wave contracts are separate. |
| executionPackRef | `EXECUTION-PACK.md` | Scheduling only; SWU definitions remain here and in task files. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | Four evidence-gated layers. |
| dispatchTechniqueTrace | `REFINE-DISPATCH.json`; table below | Validated route plus plan trace. |
| distillValidationStatus | pass | Plan structure passes; execution authorization remains blocked separately. |
| swuAtomicityStatus | pass | L0 frontier is frozen as seven ordered units; later layers are outside the epoch. |
| firstUnitNarrownessStatus | pass | `SWU-ACAPI-000` repairs the acceptance-critical validator race before API bytes. |
| closeoutSyncStatus | pass | Every L0 unit uses exact terminal paths plus receipt-backed semantic `NO_OP` closeout. |
| activeLayerWindow | L0 | No later layer may begin without L0 evidence. |
| lastUpdatedAt | 2026-08-03T18:32:47Z | Refine planning time. |
| readinessProfile | frozen-input-contractual-readiness | Execution remains unapproved until the exact WPRA epoch is confirmed. |
| oneGoFrontier | `SWU-ACAPI-000` through `SWU-ACAPI-006` | Budget 7; serial; stop at first blocker; terminate after 006. |
| oneGoControl | `one-go/ONE-GO-HANDOFF.md` | Frozen material, admission receipts, audit outputs, and approval boundary. |

## Objective Summary

- Objective: implement and validate a read-only consultation boundary that
  returns bounded evidence to an answering agent without acquiring answer,
  reasoning, memory, routing, authority, or execution ownership.
- Primary inputs: `stages/06-design.md`, `stages/07-design-review.md`,
  `stages/08-distill-repair.md`, and `stages/08-question-scenarios.md`.
- Success condition: an executed L0 fixture proves the closed contract and the
  14 bounded scenario assertions before product integration is considered.

## Delivery Slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-000 | Deterministic existing ontology regression gate. | L0 prerequisite | W0 | none | repeated validator and ontology suite |
| S-001 | Closed contracts and fail-closed fixtures. | L0 | W0 | S-000 | schema and fixture validator |
| S-002 | Neutral projection and consultation core over fixtures. | L0 | W1 | S-001 | leakage, retrieval, status, and scenario tests |
| S-003 | Host adapter and answering-agent integration. | L1 | W2 | S-002 plus owner gates | targeted Vitest and end-to-end fixture |
| S-004 | Policy, cache, deadline, and degraded-mode hardening. | L2 | W2 | S-003 | failure-injection and measurement receipts |
| S-005 | Optional operations or transport packaging. | L3 | W3 | L2 promotion evidence | compatibility and security tests |

## Task Status Board

| Task | Goal | Layer | Wave | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-ACAPI-00](work-pack/tasks/TASK-ACAPI-00-VALIDATOR.md) | Make the existing ontology regression gate deterministic. | L0 prerequisite | W0 | epoch approval | material ready |
| [TASK-ACAPI-01](work-pack/tasks/TASK-ACAPI-01-CONTRACTS.md) | Closed query and response contracts. | L0 | W0 | 000 receipt | material ready |
| [TASK-ACAPI-02](work-pack/tasks/TASK-ACAPI-02-PROJECTION.md) | Neutral projection fixture and leakage proof. | L0 | W0-W1 | 002 receipt | material ready |
| [TASK-ACAPI-03](work-pack/tasks/TASK-ACAPI-03-SERVICE.md) | Read-only service core over fixtures. | L0 | W1 | 004 receipt | material ready |
| [TASK-ACAPI-04](work-pack/tasks/TASK-ACAPI-04-HOST.md) | Host tool and answer-policy integration. | L1 | W2 | owner gates plus L0 pass | blocked |
| [TASK-ACAPI-05](work-pack/tasks/TASK-ACAPI-05-HARDENING.md) | Cache, deadline, policy, and failure hardening. | L2 | W2 | L1 witness | blocked |
| [TASK-ACAPI-06](work-pack/tasks/TASK-ACAPI-06-PACKAGING.md) | Optional operations and HTTP packaging. | L3 | W3 | measured need plus L2 pass | deferred |
| TASK-ACAPI-VERIFY | Closeout verification. | L2-L3 | W3 | executed evidence | blocked |

## SWU Manifest

| SWU | Parent | Primary behavior | Layer | Dependencies | Owner | Handoff |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-ACAPI-000 | TASK-ACAPI-00 | Stabilize view digest construction in the existing validator. | L0 prerequisite | none | augmentor-consultation-candidate-owner | unique root |
| SWU-ACAPI-001 | TASK-ACAPI-01 | Validate model-visible query schema. | L0 | 000 | augmentor-consultation-candidate-owner | successor 002 |
| SWU-ACAPI-002 | TASK-ACAPI-01 | Validate status-tagged evidence results. | L0 | 001 | augmentor-consultation-candidate-owner | successor 003 |
| SWU-ACAPI-003 | TASK-ACAPI-02 | Validate neutral projection and manifest schema. | L0 | 002 | augmentor-consultation-candidate-owner | successor 004 |
| SWU-ACAPI-004 | TASK-ACAPI-02 | Build one-way fixture projection and reject leakage. | L0 | 003 | augmentor-consultation-candidate-owner | successor 005 |
| SWU-ACAPI-005 | TASK-ACAPI-03 | Enforce effective caps and mechanical status precedence. | L0 | 004 | augmentor-consultation-candidate-owner | successor 006 |
| SWU-ACAPI-006 | TASK-ACAPI-03 | Consult fixture projection through lookup/search/context. | L0 | 005 | augmentor-consultation-candidate-owner | terminal |
| SWU-ACAPI-007 | TASK-ACAPI-04 | Inject verified host context outside model arguments. | L1 | 006, owner gates | subagent | blocked |
| SWU-ACAPI-008 | TASK-ACAPI-04 | Apply answer/qualify/clarify/abstain policy to typed results. | L1 | 006 | subagent | blocked |
| SWU-ACAPI-009 | TASK-ACAPI-04 | Prove host question-to-answer or abstention flow. | L1 | 007-008 | subagent | blocked |
| SWU-ACAPI-010 | TASK-ACAPI-05 | Isolate cached evidence by access and contract identity. | L2 | 009 | subagent | blocked |
| SWU-ACAPI-013 | TASK-ACAPI-05 | Propagate effective deadline and cancellation through every read. | L2 | 009 | subagent | blocked |
| SWU-ACAPI-011 | TASK-ACAPI-05 | Prove denial, drift, timeout, and injection failure behavior. | L2 | 010, 013 | subagent | blocked |
| SWU-ACAPI-012 | TASK-ACAPI-06 | Add one evidence-justified typed operation or HTTP wrapper. | L3 | 011, owner decision | subagent | deferred |

## SWU Atomicity Review

| SWU | Candidate split | Why retained | Verdict |
| --- | --- | --- | --- |
| 000 | concurrency fix vs regression proof | The only change removes one nondeterministic construction; repeated validation is its acceptance boundary. | pass |
| 001 | schema vs fixtures | A schema without positive and negative fixtures has no independently reviewable closed-contract acceptance. | pass |
| 002 | union vs statement provenance | Status variants are unsafe unless each evidence-carrying variant binds the same atomic provenance contract. | pass |
| 003 | record schema vs manifest | Projection content cannot be evaluated without its compiler/source manifest. | pass |
| 004 | compiler vs leakage validator | The compiler's primary behavior is the one-way admitted projection; leakage rejection is its acceptance boundary. | pass |
| 005 | caps vs status precedence | Both are the one deterministic request-boundary decision before service reads and result formation. | pass |
| 006 | lookup vs search vs context | They share one closed read pipeline, one material package, and one end-to-end acceptance boundary. The epoch freezes this decision. | pass-frozen |
| 007 | principal vs policy injection | Both form one verified execution context; partial injection is not callable safely. | pass |
| 008 | answer modes | The primary behavior is one total mapping from result union to agent action. | pass |
| 009 | question vs tool vs answer | This is one integration witness whose acceptance requires the full path. | pass |
| 010 | cache key vs cached payload | They form one access-isolated cache behavior and acceptance boundary. | pass |
| 013 | deadline vs cancellation | Both terminate the same bounded read lifetime and share one propagation boundary. | pass |
| 011 | failure cases | One primary behavior is preserving fail-closed semantics under injected failures. | pass |
| 012 | operation vs HTTP | Exactly one may be selected after evidence; never implement both in one SWU. | pass by selection constraint |

SWU-006 retains one public `consult` behavior; lookup, search, and context are
closed query variants over the same pipeline rather than separately exposed
services. Any later split invalidates the epoch and requires a new audit and
approval.

## First-unit Narrowness

`SWU-ACAPI-000` changes only the order in which already-computed view digests
are assembled. It is the narrowest reversible prerequisite because the final
L0 acceptance command otherwise has a nondeterministic result. API material
starts only after its terminal receipt and semantic closeout pass.

## Task Session Closeout Sync Contract

The terminal contract is the current Task Session governance terminal schema,
bound through `one-go/audit/`. Each unit also has an exact material package,
producer receipt, target inventory, context contract, admission request, and
admission receipt under `one-go/generated/<SWU-ID>/`.

L0 closeout is receipt-backed semantic `NO_OP`: execution evidence and chain
state are append-only under `one-go/execution/`; the frozen work pack, task
files, and traceability do not change during the epoch. A local transition
validator must dereference and validate the Task Session terminal receipt,
Continuation Router verification, closeout contract, and before/after
inventories before `run_chain.py` may advance.

| SWU | Lifecycle owner | Exact execution receipt | Closeout proof | Successor |
| --- | --- | --- | --- | --- |
| 000 | augmentor-consultation-candidate-owner | `one-go/execution/receipts/SWU-ACAPI-000.json` | `one-go/execution/no-op/SWU-ACAPI-000.json` | 001 |
| 001 | augmentor-consultation-candidate-owner | `one-go/execution/receipts/SWU-ACAPI-001.json` | `one-go/execution/no-op/SWU-ACAPI-001.json` | 002 |
| 002 | augmentor-consultation-candidate-owner | `one-go/execution/receipts/SWU-ACAPI-002.json` | `one-go/execution/no-op/SWU-ACAPI-002.json` | 003 |
| 003 | augmentor-consultation-candidate-owner | `one-go/execution/receipts/SWU-ACAPI-003.json` | `one-go/execution/no-op/SWU-ACAPI-003.json` | 004 |
| 004 | augmentor-consultation-candidate-owner | `one-go/execution/receipts/SWU-ACAPI-004.json` | `one-go/execution/no-op/SWU-ACAPI-004.json` | 005 |
| 005 | augmentor-consultation-candidate-owner | `one-go/execution/receipts/SWU-ACAPI-005.json` | `one-go/execution/no-op/SWU-ACAPI-005.json` | 006 |
| 006 | augmentor-consultation-candidate-owner | `one-go/execution/receipts/SWU-ACAPI-006.json` | `one-go/execution/no-op/SWU-ACAPI-006.json` | terminal |

Later-layer closeout rows remain planning-only:

| SWU | Lifecycle owner | Target inventory | Baseline | Allowed deltas | Owner validation | Expected receipt | Successor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 007 | ResonantOS host owner | `WORK-PACK.md`, task 04, traceability, result 007 | consumer commit plus SHA-256 | same | targeted Vitest plus build | result 007 | 008 if pass |
| 008 | answering-agent owner | `WORK-PACK.md`, task 04, traceability, result 008 | consumer commit plus SHA-256 | same | answer-policy tests | result 008 | 009 if pass |
| 009 | ResonantOS product owner | `WORK-PACK.md`, task 04, traceability, result 009 | consumer commit plus SHA-256 | same | integration fixture and build | result 009 | 010 if promoted |
| 010 | consultation-service owner | `WORK-PACK.md`, task 05, traceability, result 010 | consumer commit plus SHA-256 | same | cache-isolation tests | result 010 | 013 if pass |
| 013 | consultation-service owner | `WORK-PACK.md`, task 05, traceability, result 013 | consumer commit plus SHA-256 | same | deadline/cancellation tests | result 013 | 011 if 010 also passes |
| 011 | service plus security owners | `WORK-PACK.md`, task 05, traceability, result 011 | consumer commit plus SHA-256 | same | failure-injection suite | result 011 | 012 only after decision |
| 012 | selected transport/operation owner | `WORK-PACK.md`, task 06, traceability, result 012 | consumer commit plus SHA-256 | same | compatibility/security tests | result 012 | none |

No closeout may admit L1, promotion, publication, deployment, or another owner
decision. The outer chain admits only the next unique member of the frozen L0
frontier, and each member still receives a fresh Task Session receipt.

## Blockers

| ID | Scope | Description | Owner | Next action |
| --- | --- | --- | --- | --- |
| B-001 | L0 execution | Exact WPRA epoch has not received digest-bound human approval. | human decision gate | approve or reject only the emitted seven-unit epoch. |
| B-002 | L1 | Principal, policy, projection, and answer-policy owners are unselected. | ResonantOS product governance | resolve owners before consumer writes. |
| B-003 | L1 | Neutral projection field allowlist is not approved. | private ontology owner plus consumer data owner | approve exact fields and leakage rules. |
| B-004 | L2 | Caps and service objectives are unmeasured. | service owner | measure L1 witness before fixing values. |
| B-005 | L3 | No evidence selects HTTP or additional operations. | product owner | choose one only after observed need. |

## Dispatch Technique Trace

| Technique | Applied to | Evidence | Status |
| --- | --- | --- | --- |
| sequence | W0 -> W1 -> W2 -> W3 | dependency table | pass |
| scu_swu_reduction | 14 planned SWUs; 7 in L0 epoch | atomicity table | pass; L0 frozen |
| recomposition_proof | SWUs -> repaired design | traceability file | pass |
| validation_loop | every SWU | task-local commands and receipt paths | pass |
| owner_boundary_check | candidate repo -> consumer repo -> later transport | blockers and task scopes | pass |
| handle_handoff | task and source refs | task files | pass |
| residue_ledger | B-001-B-005 | shared gaps | pass |
| execution_receipt_handoff | closeout table | exact result path per SWU | pass |

## Distill Validation

| Check | Result | Evidence |
| --- | --- | --- |
| Smallest coherent unit | pass | `ConsultationBoundary` from stage 5 and repaired stage 8 contract. |
| SWU atomicity | pass for plan | zero task-shaped units; SWU-006 retains one public behavior and must remain one pipeline. |
| First-unit narrowness | pass | SWU-ACAPI-000 repairs only deterministic digest assembly. |
| Recomposition | pass | `work-pack/shared/traceability.md`. |
| Hidden gaps | pass | B-001-B-005 are explicit. |
| Deferred complexity | pass | HTTP, extra operations, durable cache, UI, deployment remain outside L0. |
| Navigation | pass | start with `one-go/ONE-GO-HANDOFF.md`; after approval the unique root is SWU-ACAPI-000. |

## Gate Checks

- Planning artifacts: pass.
- Design evidence state: `design-validator-pass`.
- Distill plan validation: pass.
- Mutation-capable execution: exact materials and admission contracts are
  prepared; it remains blocked until B-001 approves the emitted epoch.
- L1-L3: blocked or deferred by their own owner and evidence gates.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-08-03 | Initial non-executed work-pack created from confirmed Refine run. | invoke plan through refine |
| 2026-08-03 | Frozen seven-unit candidate-local L0 one-go frontier, exact material/admission paths, and semantic NO_OP closeout added. | implementation-readiness |
