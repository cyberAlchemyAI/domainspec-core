---
module: inventory-runtime-faceted-layout
version: candidate
status: owner-integration-required
updatedAt: 2026-07-24
docType: work-pack
---

# WORK-PACK: Inventory Runtime And Faceted Layout

## Control Fields

| Field | Value | Notes |
|---|---|---|
| workPackGateStatus | block | Authored plan is complete, but Sigil Development has not accepted/reconciled it with the existing canonical Inventory work-pack. |
| complexity | medium | Public runtime, schema, generated package, and isolated consumer proof. |
| outputMode | split | Task and wave contracts are separate. |
| executionPackRef | [EXECUTION-PACK.md](EXECUTION-PACK.md) | Required medium-complexity choreography. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0-L3 decisions. |
| dispatchTechniqueTrace | [DISPATCH-TECHNIQUE-TRACE.md](DISPATCH-TECHNIQUE-TRACE.md) | Validated route techniques. |
| distillValidationStatus | pass | [DISTILL-VALIDATION.md](DISTILL-VALIDATION.md) |
| swuAtomicityStatus | pass | Seven mutation SWUs, zero task-shaped SWUs. |
| firstUnitNarrownessStatus | pass | `SWU-IFR-001` is pure, reversible, and mutation-free. |
| closeoutSyncStatus | pass | Every mutation SWU has a complete closeout row below. |
| activeLayerWindow | L0 | Receipt kernel only after owner acceptance. |
| lastUpdatedAt | 2026-07-24T17:51:03Z | Invoke authoring timestamp. |
| readinessProfile | pilot | Generic deterministic proof, not release. |

## Objective

Deliver Candidate B as a deterministic installed Inventory append runtime, then
admit and project new faceted entries without moving legacy state.

Success means the twelve research validation gates plus faceted path/projection
compatibility are witnessed by durable receipts. Authored artifacts alone do
not establish success.

## Delivery Boundary

Included:

- receipt kernel;
- package-local dry-run;
- explicit sequential apply observation;
- faceted new-entry metadata and physical path admission;
- derived namespace/class/concept maps;
- runtime manifest and sync;
- isolated installed-consumer proof.

Excluded:

- current live Inventory migration;
- replace/update/delete;
- legacy tag cleanup;
- lock/journal/recovery and atomicity;
- currentness verification;
- UI/search/database/vector storage;
- publication or release.

## Delivery Slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
|---|---|---|---|---|---|
| S-01 | Canonical receipt kernel. | L0 | W1 | owner acceptance | schema and byte-repeat tests |
| S-02 | Full no-write append transition. | L1 | W2 | S-01 | unrelated-CWD and zero-mutation receipts |
| S-03 | Sequential apply is attributable. | L2 | W3 | S-02 | success/failure/postwrite fixtures |
| S-04 | New faceted records are admitted safely. | L2 | W3 | S-02 | path/metadata/legacy fixtures |
| S-05 | Facet maps and human projections conform. | L2 | W3 | S-04 | exact derived-map and human-view validation |
| S-06 | Runtime distribution is bounded. | L3 | W4 | S-03, S-05 | manifest drift and consumer-state negative fixture |
| S-07 | Installed consumer proof closes the design. | L3 | W4 | S-06 | acceptance receipts and boundary scan |

## Task Board

| Task | Goal | Layer | Wave | Gate | Status |
|---|---|---|---|---|---|
| [TASK-IFR-001](work-pack/tasks/TASK-IFR-001-RECEIPT-KERNEL.md) | Canonical receipt kernel. | L0 | [W1](work-pack/waves/W1-L0-RECEIPT.md) | ready-after-owner-acceptance | not-started |
| [TASK-IFR-002](work-pack/tasks/TASK-IFR-002-DRY-RUN.md) | No-write append transition. | L1 | [W2](work-pack/waves/W2-L1-DRY-RUN.md) | blocked-by-001 | not-started |
| [TASK-IFR-003](work-pack/tasks/TASK-IFR-003-APPLY-OBSERVATION.md) | Sequential apply observation. | L2 | [W3](work-pack/waves/W3-L2-APPLY-FACETS.md) | blocked-by-002 | not-started |
| [TASK-IFR-004](work-pack/tasks/TASK-IFR-004-FACET-ADMISSION.md) | Faceted record/path admission. | L2 | [W3](work-pack/waves/W3-L2-APPLY-FACETS.md) | blocked-by-002 | not-started |
| [TASK-IFR-005](work-pack/tasks/TASK-IFR-005-FACET-PROJECTIONS.md) | Exact facet projections. | L2 | [W3](work-pack/waves/W3-L2-APPLY-FACETS.md) | blocked-by-004 | not-started |
| [TASK-IFR-006](work-pack/tasks/TASK-IFR-006-RUNTIME-SYNC.md) | Manifest-bound runtime sync. | L3 | [W4](work-pack/waves/W4-L3-PACKAGE-PROOF.md) | blocked-by-003,005 | not-started |
| [TASK-IFR-007](work-pack/tasks/TASK-IFR-007-CONSUMER-PROOF.md) | Isolated installed-consumer proof. | L3 | [W4](work-pack/waves/W4-L3-PACKAGE-PROOF.md) | blocked-by-006 | not-started |
| [TASK-IFR-VERIFY](work-pack/tasks/TASK-IFR-VERIFY.md) | Recompose, audit, and close. | L3 | [W4](work-pack/waves/W4-L3-PACKAGE-PROOF.md) | blocked-by-007 | not-started |

## Shared SWU Manifest

| SWU | Parent | Primary behavior | Dependencies | Write scope | Verification | Owner |
|---|---|---|---|---|---|---|
| SWU-IFR-001 | TASK-IFR-001 | Serialize and digest one canonical operation receipt. | owner acceptance | `arcanum/arcana/inventory/{schemas,lib,test}/` named files | `node --test arcanum/arcana/inventory/test/operation-receipt.test.cjs` | sigil-development |
| SWU-IFR-002 | TASK-IFR-002 | Compute one complete no-write append transition. | 001 | `bin/inventory`, `lib/inventory-update.cjs`, dry-run tests | `node --test .../append-dry-run.test.cjs` | sigil-development |
| SWU-IFR-003 | TASK-IFR-003 | Observe sequential apply and partial failures. | 002 | append runtime and apply tests | `node --test .../append-apply.test.cjs` | sigil-development |
| SWU-IFR-004 | TASK-IFR-004 | Admit one new faceted record/path while preserving legacy. | 002 | entry/index schemas, updater, facet tests | `node --test .../facet-admission.test.cjs` | sigil-development |
| SWU-IFR-005 | TASK-IFR-005 | Derive exact namespace/class/concept projections. | 004 | updater, validator, projection tests/templates | full projection conformance fixture | sigil-development |
| SWU-IFR-006 | TASK-IFR-006 | Check/apply generated runtime members only. | 003,005 | manifest, sync script, SKILL/README, sync tests | sync check/apply fixture | sigil-development |
| SWU-IFR-007 | TASK-IFR-007 | Reproduce acceptance in an isolated installed consumer. | 006 | generic consumer fixture and session evidence only | installed-consumer harness | sigil-development |

## SWU Atomicity Review

| SWU | Candidate child units | Why retained | Verdict |
|---|---|---|---|
| 001 | schema; serializer; digest tests | None proves a usable canonical receipt without the other two. | pass |
| 002 | root resolution; validation; warning delta; dry-run CLI | Their joined output is the single no-write transition receipt; individual helpers are not independently accepted behavior. | pass |
| 003 | successful apply; failure injection; postwrite mismatch | All are outcomes of one sequential-write observation contract. | pass |
| 004 | metadata validation; path validation; legacy bypass | One admission decision requires all three precedence rules. | pass |
| 005 | three maps; human index grouping | Each map is independently testable but the acceptance boundary is exact projection conformance for the admitted facet model. | pass |
| 006 | manifest; check; apply; docs | One distribution contract is incomplete without managed-set enforcement and operator surface. | pass |
| 007 | unrelated-CWD; warning delta; repeat; zero mutation | These are separate cases in one installed-consumer acceptance harness, with no source implementation change. | pass |

## First Unit

`SWU-IFR-001` is selected after owner acceptance. It changes only new public
schema/library/test files, performs no consumer mutation, and can be reverted
without affecting the current updater or validator. Starting with CLI, facets,
sync, or current consumer state would be broader and less reversible.

## Task Session Closeout Sync Contract

Common terminal receipt:

```text
ops/development/2026-07-24-inventory-runtime-faceted-layout/
work-pack/session-evidence/<SWU-ID>/receipt.json
```

Common baseline: Task Session captures the canonical Arcanum git SHA plus
SHA-256 of this work-pack and the selected task file before mutation.

Common allowed planning deltas:
`evidence_added`, `blocker_opened`, `blocker_resolved`, `status_changed`,
`route_changed`. Closeout may not admit unrelated implementation or authority
changes.

| SWU | Lifecycle route | Declared target inventory | Owner validation | Expected owner receipt | Successor |
|---|---|---|---|---|---|
| 001 | `sigil-development inventory --update` | this work-pack, task 001, traceability, session evidence 001 | receipt unit test | `inventory.operation-receipt-kernel-result.v1` | 002 if pass |
| 002 | same | work-pack, task 002, traceability, evidence 002 | dry-run test plus validator pair | `inventory.append-dry-run-result.v1` | 003 and 004 become dependency-ready |
| 003 | same | work-pack, task 003, traceability, evidence 003 | apply/failure test | `inventory.append-apply-result.v1` | 006 after 005 |
| 004 | same | work-pack, task 004, traceability, evidence 004 | facet admission test | `inventory.facet-admission-result.v1` | 005 |
| 005 | same | work-pack, task 005, traceability, evidence 005 | projection conformance | `inventory.facet-projection-result.v1` | 006 after 003 |
| 006 | same | work-pack, task 006, traceability, evidence 006 | sync harness and boundary test | `inventory.runtime-sync-result.v1` | 007 |
| 007 | same | work-pack, task 007, traceability, evidence 007 | installed-consumer harness | `inventory.installed-consumer-proof.v1` | VERIFY |

Successor policy is deterministic: a passing receipt unlocks only the named
successor; flag/block unlocks none and routes to the same lifecycle owner.

## Blockers And Gaps

| ID | Class | Description | Owner | Resolution |
|---|---|---|---|---|
| B-OWNER-INTEGRATION | handoff blocker | Existing canonical Inventory work-pack selects `SWU-INT-001`; this delta is not yet admitted. | sigil-development | Accept, sequence, or supersede explicitly before SWU-IFR-001. |
| G-CURRENTNESS | deferred gap | Currentness verifier owner remains unresolved. | future decision-gate | Make no currentness claims. |
| G-ATOMICITY | deferred gap | Lock/journal/recovery is outside MVP. | later transaction-safety owner | Preserve partial-mutation evidence. |
| G-LEGACY-MIGRATION | deferred gap | 111 flat entry files remain. | future migration plan | New entries only in this work-pack. |
| G-GENERATED-COMPANIONS | tooling gap | Several `.agents` companion packages are absent. | Arcanum bootstrap owner | Use canonical contracts; do not block subject plan. |

## Validation Strategy

| Check | Scope | Evidence |
|---|---|---|
| Receipt schema and canonical bytes | L0 | repeated unit fixtures |
| No-write state coverage | L1 | unrelated-CWD, warning delta, no-op/conflict, missing helper |
| Full baseline/candidate conformance | L1-L3 | canonical validator pair |
| Apply failure observation | L2 | injected write failure and postwrite alteration |
| Facet admission and legacy compatibility | L2 | new faceted and legacy fixtures |
| Exact derived maps and human view | L2 | projection conformance |
| Runtime managed-set safety | L3 | sync negative fixture |
| Public/private boundary | L3 | private path/evidence scan |
| Recomposition | closure | AC-01 through AC-10 traceability |

## Gate Result

- Invoke Plan artifact: `flag` only because target lifecycle acceptance is
  pending.
- Distill: pass.
- Work-pack/Task Session: block until `B-OWNER-INTEGRATION` closes.
- Next route: `sigil-development inventory --update`.

