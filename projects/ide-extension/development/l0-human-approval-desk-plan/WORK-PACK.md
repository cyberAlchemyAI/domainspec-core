---
module: ide-extension-l0-human-approval-desk
version: current
status: ready-for-approval
updatedAt: 2026-07-11
docType: work-pack
---

# WORK-PACK: L0 Human Approval Desk

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Planning gates pass; execution still requires explicit Task Session selection. |
| complexity | medium | Coupled policy, lifecycle, persistence, evidence, and browser behavior. |
| outputMode | split | Task and wave contracts are independently executable. |
| executionPackRef | [EXECUTION-PACK.md](EXECUTION-PACK.md) | Cross-task choreography. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0-L3 boundary authority. |
| dispatchTechniqueTrace | [dispatch.json](dispatch.json) | Validated cross-capability route. |
| distillValidationStatus | pass | See [PLAN-TRANSPORT.md](PLAN-TRANSPORT.md). |
| activeLayerWindow | L0 | L1-L3 are deferred. |
| lastUpdatedAt | 2026-07-11 | Initial plan. |
| readinessProfile | pilot | Local no-op human workflow only. |

## Objective Summary

- Objective: repair the current L0 witness into a local Approval Desk a person can use to inspect, approve, reject, and audit multiple no-op proposals.
- Primary inputs: [SPEC.md](../../SPEC.md), [ARCHITECTURE.md](../../ARCHITECTURE.md), and the accepted [architecture review](../architecture-review-2026-07-10/findings.md).
- Success condition: every present-L0 review finding is closed with hostile evidence, the complete browser workflow passes, and no deferred authority enters the implementation.
- Current proof: `npm run validate:schemas` and `npm run smoke` pass, but they cover only schema parsing/manifests and the cooperative happy path.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | Deterministic regressions reproduce every accepted present-L0 defect. | L0 | [W0](work-pack/waves/W0.md) | none | `npm run test:adversarial` fails against the unrepaired baseline for the named reasons, then becomes the repair oracle. |
| S-002 | Approval and contract boundaries are ID-addressed, exact-once, honest, grant-closed, and schema-enforced. | L0 | [W1](work-pack/waves/W1.md) | S-001 | Focused approval and schema tests pass, including sequential/concurrent replay and malformed input. |
| S-003 | Event, projection, artifact, and receipt persistence is serialized, recoverable, and reference-complete. | L0 | [W2](work-pack/waves/W2.md) | S-002 | Race/restart tests pass and every committed receipt reference resolves. |
| S-004 | A person can inspect and resolve proposals through the HTML workbench, with browser evidence and closure audit. | L0 | [W3](work-pack/waves/W3.md) | S-003 | Smoke, hostile, recovery, schema, and Playwright suites pass; closure matrix maps every finding to evidence. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Wave | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- |
| [TASK-REGRESSION-HARNESS](work-pack/tasks/TASK-REGRESSION-HARNESS.md) | Capture accepted failures as deterministic tests. | L0 | medium | W0 | ready | not-started |
| [TASK-TRUSTED-KERNEL](work-pack/tasks/TASK-TRUSTED-KERNEL.md) | Repair lifecycle, grants, attribution, and runtime contracts. | L0 | high | W1 | ready-after-W0 | not-started |
| [TASK-PERSISTENCE-EVIDENCE](work-pack/tasks/TASK-PERSISTENCE-EVIDENCE.md) | Make persistence recoverable and receipt evidence resolvable. | L0 | high | W2 | ready-after-W1 | not-started |
| [TASK-HUMAN-WORKBENCH](work-pack/tasks/TASK-HUMAN-WORKBENCH.md) | Deliver the usable HTML workflow and browser proof. | L0 | medium | W3 | ready-after-W2 | not-started |
| [TASK-VERIFY-READINESS](work-pack/tasks/TASK-VERIFY-READINESS.md) | Audit closure and prepare evidence-backed synchronization. | L0 | medium | W3 | ready-after-implementation | not-started |

## SWU Execution Handoff

| SWU ID | Parent Task | Dependencies | Write Scope | Done Criteria | Validation Surface | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-IDEAD-001 | [TASK-REGRESSION-HARNESS](work-pack/tasks/TASK-REGRESSION-HARNESS.md) | none | `tests/l0-adversarial.test.mjs`, test scripts only | Eight accepted present-L0 failures are deterministic and individually named. | `npm run test:adversarial` | local-fallback | ready |
| SWU-IDEAD-002 | [TASK-TRUSTED-KERNEL](work-pack/tasks/TASK-TRUSTED-KERNEL.md) | 001 | envelope/server state model and focused tests | Multiple proposals remain reachable; approval is exact-once under sequential and concurrent calls. | focused Node tests | local-fallback | ready-after-001 |
| SWU-IDEAD-003 | [TASK-TRUSTED-KERNEL](work-pack/tasks/TASK-TRUSTED-KERNEL.md) | 002 | grants, approval records, routes, focused tests | Unknown grants reject; approve/reject are terminal; records describe an unattested local operator action without identity claims. | focused Node tests | local-fallback | ready-after-002 |
| SWU-IDEAD-004 | [TASK-TRUSTED-KERNEL](work-pack/tasks/TASK-TRUSTED-KERNEL.md) | 001 | dependency lock, schema adapter, schema fixtures/tests | One Draft 2020-12 validator compiles all schemas and returns stable validation errors. | schema unit tests | local-fallback | ready-after-001 |
| SWU-IDEAD-005 | [TASK-TRUSTED-KERNEL](work-pack/tasks/TASK-TRUSTED-KERNEL.md) | 003, 004 | registry, prepare/resolve routes, schemas, validation script | Manifests, requests, envelopes, approvals, and receipts reject before authoritative writes when invalid. | `npm run validate:schemas`; hostile tests | local-fallback | ready-after-003-004 |
| SWU-IDEAD-006 | [TASK-PERSISTENCE-EVIDENCE](work-pack/tasks/TASK-PERSISTENCE-EVIDENCE.md) | 005 | audit/projector/storage modules and tests | Mutations serialize; event replay rebuilds projection; races cannot diverge receipts and events. | race and restart tests | local-fallback | ready-after-005 |
| SWU-IDEAD-007 | [TASK-PERSISTENCE-EVIDENCE](work-pack/tasks/TASK-PERSISTENCE-EVIDENCE.md) | 006 | artifact writer, receipt construction/schema, tests | Before/after/receipt artifacts are exclusive, resolvable, and validated before commit. | artifact/reference tests | local-fallback | ready-after-006 |
| SWU-IDEAD-008 | [TASK-HUMAN-WORKBENCH](work-pack/tasks/TASK-HUMAN-WORKBENCH.md) | 007 | local API and `public/demo/l0.html` | Queue selection, details, grants, approve, reject, history, evidence, and error states work without identity overclaim. | smoke and DOM-level checks | local-fallback | ready-after-007 |
| SWU-IDEAD-009 | [TASK-HUMAN-WORKBENCH](work-pack/tasks/TASK-HUMAN-WORKBENCH.md) | 008 | Playwright config/test and test scripts | Real browser proves multiple proposal resolution, reload persistence, evidence navigation, and replay rejection. | `npm run test:e2e` | local-fallback | ready-after-008 |

Every row above is expanded in its parent task contract with source anchors, edge cases, expected evidence, and result shape.

## Blockers And Gaps

| ID | Type | Description | Owner | Treatment |
| --- | --- | --- | --- | --- |
| GAP-IDEAD-001 | deliberate boundary | L0 cannot attest that the browser operator is a specific human. | architecture owner | Record an unattested local operator action; keep attested principal/session separation as an L1 promotion blocker. |
| GAP-IDEAD-002 | dependency | Runtime validation adds Ajv and a lockfile change. | SWU-IDEAD-004 owner | Use the Draft 2020-12 export behind `schema-validation.mjs`; pin through the package lock and verify licenses at execution. |
| GAP-IDEAD-003 | synchronization | `SPEC.md`, `ARCHITECTURE.md`, `README.md`, and Craft frontier predate the completed repair. | TASK-VERIFY-READINESS | Prepare evidence-backed deltas after implementation; mutate Craft only through an approved Craft operation. |
| GAP-IDEAD-004 | environment | Playwright browser installation may be absent. | SWU-IDEAD-009 owner | Detect before the SWU; install only the required browser through the approved project tooling or return BLOCK with the exact command. |

No gap blocks `SWU-IDEAD-001`. Effectful L1+ work remains blocked by the promotion conditions in the accepted review.

## Dispatch Technique Trace

| Technique ID | Applied To | Validation Expectation | Status |
| --- | --- | --- | --- |
| `sequence` | W0 through W3 | Each wave consumes prior evidence. | pass |
| `scu_swu_reduction` | SWU manifest | Every SWU has one executable responsibility and one parent. | pass |
| `recomposition_proof` | SWUs to L0 product | Nine SWUs recompose into one human Approval Desk without importing L1 scope. | pass |
| `validation_loop` | Every SWU and slice | Each mutation has a command or reviewable acceptance check. | pass |
| `owner_boundary_check` | Invoke to Task Session and Craft | Invoke authors; Task Session executes; Craft alone promotes ledger deltas. | pass |
| `handle_handoff` | Plan artifacts to execution | Task Session consumes paths and selectors, not copied ambient context. | pass |
| `residue_ledger` | gaps and deferred layers | Every unresolved item has an owner and treatment. | pass |
| `execution_receipt_handoff` | Task Session result | Every SWU returns files, validation, blockers, residue, and reroute. | pass |
| `authority_split_gate` | kernel, UI, adapters, Craft | Lifecycle, execution, evidence, and promotion owners remain distinct. | pass |
| `concrete_path_evidence` | closure audit | Every closed finding cites a test, artifact, or concrete path. | pass |

## Distill Validation

| Check | Result | Evidence Or Gap |
| --- | --- | --- |
| Smallest coherent unit | pass | `SWU-IDEAD-001` creates the finite repair oracle without changing product behavior. |
| Recomposition proof | pass | W0 captures failures; W1 repairs authority/contracts; W2 repairs durable evidence; W3 exposes and proves the human workflow. |
| Hidden acceptance-critical gaps | pass | Identity assurance is explicitly bounded; browser availability has a fail-closed route. |
| Deferred complexity | pass | MCP, providers, MV3, IDE chrome, external witnesses, and Nimbalyst are excluded. |
| Navigation to first executable unit | pass | Start at `task-session ... --swu SWU-IDEAD-001`. |

## Gate Checks

1. Execute one SWU per Task Session unless a later approved handoff explicitly composes read-only verification.
2. Do not start W1 until W0 records all accepted failures as deterministic evidence.
3. Do not start W2 until approval and schema hostile tests pass.
4. Do not start W3 until restart/reconciliation and receipt-reference tests pass.
5. Do not claim L0 complete until `TASK-VERIFY-READINESS` maps AR-CAND-001 through AR-CAND-008 to concrete passing evidence.
6. Do not mutate the canonical Craft ledger from an implementation SWU.
7. Do not admit L1+ authority under this work-pack.

## Expected SWU Result

```yaml
swu_id: SWU-IDEAD-NNN
result: pass | flag | block | interrupted
capability_ref: task-session
receipt_kind: native-stage | local-fallback | blocked
receipt_artifact: path-or-none
files_touched: []
validation: []
blockers: []
residue: []
reroute: next-swu-or-none
handoff_note: concise continuation state
```

## Next Route

After explicit user approval:

```text
task-session to projects/ide-extension/development/l0-human-approval-desk-plan/WORK-PACK.md --swu SWU-IDEAD-001
```
