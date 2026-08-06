---
module: craft-consultation-api
version: current
status: blocked-before-mutation
updatedAt: 2026-08-05
docType: work-pack
---

# WORK-PACK: Craft Consultation API

## Control fields

| Field | Value |
| --- | --- |
| workPackGateStatus | block |
| complexity | medium |
| outputMode | split |
| executionPackRef | `EXECUTION-PACK.md` |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` |
| dispatchTechniqueTrace | sequence, authority_split_gate, scu_swu_reduction, recomposition_proof, validation_loop, owner_boundary_check, residue_ledger |
| distillValidationStatus | flag |
| swuAtomicityStatus | pass |
| firstUnitNarrownessStatus | pass |
| closeoutSyncStatus | pass |
| admissionTiming | selected-unit-at-task-session |
| executionEntryState | blocked |
| allowedRoutesDigest | `ccf1d1860af5298a377c80b78b0668e61c103de85b7626c1433f0bafc698718c` |
| activeLayerWindow | L0 |
| lastUpdatedAt | 2026-08-05T19:49:40Z |
| readinessProfile | pilot |

## Work-Pack execution policy

```yaml
executionPolicy:
  routePolicy: automatic-in-scope
  allowedRoutes: []
  allowedRoutesDigest: ccf1d1860af5298a377c80b78b0668e61c103de85b7626c1433f0bafc698718c
  automaticDecisions: []
  stopDecisions:
    - product-or-semantic-choice
    - scope-expansion
    - destructive-or-irreversible-effect
    - credentials-or-secret-access
    - external-message-or-network-effect
    - cost-policy-or-risk-acceptance
    - authority-promotion-publication-deployment
    - failed-acceptance-critical-validation
  scopeSource: exact-work-pack-and-captured-frontier
  validationPolicy: owner-gates-remain-mandatory
executionEntry:
  state: blocked
  selectedUnit: null
  routeId: null
  nextOwner: decision-gate
preExecutionOwnerPrerequisite: null
```

The digest is SHA-256 of canonical UTF-8 `{"allowedRoutes":[]}`. This Refine run
does not authorize implementation or experiments, so the executable projection
is intentionally empty. A later owner decision and direct execution request must
refresh this Work Pack before Task Session mutation.

## Objective and success

Deliver a private read-only API whose L0 returns authorization-filtered status,
space metadata, and exact raw bytes from one fully verified derived snapshot.
L1 adds only a fixture-validated 0.3.0 row adapter. Success requires executable
contract, privacy, integrity, limit, and fresh-process evidence while preserving
Craft source authority and zero request-path writes.

## Delivery slices and task board

| Slice | Outcome | Layer | Wave | Task |
| --- | --- | --- | --- | --- |
| S-RUNTIME | Fresh-process witness, verifier, invalidation | L0 | W1-W2 | [TASK-RUNTIME](work-pack/tasks/TASK-RUNTIME.md) |
| S-CONTRACT | Schemas, fixtures, opaque IDs, cursors | L0 | W2 | [TASK-CONTRACT](work-pack/tasks/TASK-CONTRACT.md) |
| S-HTTP | Authorized status/catalog/raw slice | L0 | W3 | [TASK-HTTP](work-pack/tasks/TASK-HTTP.md) |
| S-ROWS | One validated 0.3.0 row projection | L1 | W4 | [TASK-ROWS](work-pack/tasks/TASK-ROWS.md) |
| S-VERIFY | Independent closure | L2 | W5 | [TASK-VERIFY](work-pack/tasks/TASK-VERIFY.md) |

All tasks are `not-started`. TASK-RUNTIME SWU-001 is the narrowest candidate,
but no SWU is selected or admitted while this gate is blocked.

## SWU execution handoff

| SWU | Parent | Dependencies | Exact write scope | Independent evidence | Status |
| --- | --- | --- | --- | --- | --- |
| SWU-CAPI-001 | TASK-RUNTIME | pinned inputs | `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import/execution/wcli-fresh-reader-01/` | child-process 55-record receipt + unchanged inputs/store | blocked |
| SWU-CAPI-002 | TASK-RUNTIME | 001, root approval | `implementation/domainspec/tools/craft-consultation-api/src/snapshot/`, `implementation/domainspec/tools/craft-consultation-api/test/snapshot/` | fixture closure/limit suite | blocked |
| SWU-CAPI-003 | TASK-RUNTIME | 002 | `implementation/domainspec/tools/craft-consultation-api/src/snapshot/`, `implementation/domainspec/tools/craft-consultation-api/test/snapshot/`, sequential only | runtime invalidation state tests | blocked |
| SWU-CAPI-004 | TASK-CONTRACT | root approval | `implementation/domainspec/tools/craft-consultation-api/contracts/`, `implementation/domainspec/tools/craft-consultation-api/test/fixtures/` | schema/fixture validation receipt | blocked |
| SWU-CAPI-005 | TASK-CONTRACT | 004, secret-provider port | `implementation/domainspec/tools/craft-consultation-api/src/security/`, `implementation/domainspec/tools/craft-consultation-api/test/security/` | HMAC/cursor vectors and negatives | blocked |
| SWU-CAPI-006 | TASK-HTTP | 004, auth port approval | `implementation/domainspec/tools/craft-consultation-api/src/auth/`, `implementation/domainspec/tools/craft-consultation-api/test/auth/` | policy/concealment matrix | blocked |
| SWU-CAPI-007 | TASK-HTTP | 002,003,005,006 | `implementation/domainspec/tools/craft-consultation-api/src/http/`, `implementation/domainspec/tools/craft-consultation-api/test/http/` | complete L0 HTTP contract suite | blocked |
| SWU-CAPI-008 | TASK-ROWS | 002,004 | `implementation/domainspec/tools/craft-consultation-api/src/adapters/v0_3/`, `implementation/domainspec/tools/craft-consultation-api/test/adapters/v0_3/` | adapter fixture receipt | blocked |
| SWU-CAPI-009 | TASK-ROWS | 005,006,007,008 | `implementation/domainspec/tools/craft-consultation-api/src/http/rows/`, `implementation/domainspec/tools/craft-consultation-api/test/http/rows/` | row contract/negative suite | blocked |

Exact source selectors, done criteria, validation, split rationale, and execution
owner recommendations live in the linked task files.

## SWU atomicity and first-unit review

All nine SWUs own one independently reviewable behavior; task-shaped bundles
were split. SWU-CAPI-001 passes the narrow-first-unit test because it changes no
product code, creates only isolated experiment evidence, and directly tests the
largest unsupported runtime assumption. It cannot be executed from this run's
empty route projection.

## Task Session closeout sync contract

Common rule for every row: before mutation, Task Session records a sorted
SHA-256/size inventory of every declared target (`ABSENT` for missing paths),
the scoped Git status, and input receipt digests. Allowed deltas are only
`evidence_added`, `blocker_opened`, `blocker_resolved`, `status_changed`, and
`route_changed`. Owner route is `invoke:refresh:apply-approved`; terminal input
must be `task-session.receipt.v1`; the accepted owner receipt is
`work-pack/execution-receipts/<SWU>.refresh.json`. Failure has no successor.

| SWU | Declared target inventory | Owner validation | Successor |
| --- | --- | --- | --- |
| 001 | `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import/execution/wcli-fresh-reader-01/` | commands and digests in TASK-RUNTIME | 002 and 004 become dependency-ready, not auto-started |
| 002 | `implementation/domainspec/tools/craft-consultation-api/src/snapshot/`; `implementation/domainspec/tools/craft-consultation-api/test/snapshot/` | TASK-RUNTIME verifier suite | 003 |
| 003 | same exact snapshot source/test paths | TASK-RUNTIME invalidation suite | 007 only after other deps |
| 004 | `implementation/domainspec/tools/craft-consultation-api/contracts/`; `implementation/domainspec/tools/craft-consultation-api/test/fixtures/` | TASK-CONTRACT schema suite | 005 and 006 |
| 005 | `implementation/domainspec/tools/craft-consultation-api/src/security/`; `implementation/domainspec/tools/craft-consultation-api/test/security/` | TASK-CONTRACT vector suite | 007 only after other deps |
| 006 | `implementation/domainspec/tools/craft-consultation-api/src/auth/`; `implementation/domainspec/tools/craft-consultation-api/test/auth/` | TASK-HTTP policy matrix | 007 only after other deps |
| 007 | `implementation/domainspec/tools/craft-consultation-api/src/http/`; `implementation/domainspec/tools/craft-consultation-api/test/http/` | TASK-HTTP L0 suite | 008/verification decision, not auto-started |
| 008 | `implementation/domainspec/tools/craft-consultation-api/src/adapters/v0_3/`; `implementation/domainspec/tools/craft-consultation-api/test/adapters/v0_3/` | TASK-ROWS adapter suite | 009 |
| 009 | `implementation/domainspec/tools/craft-consultation-api/src/http/rows/`; `implementation/domainspec/tools/craft-consultation-api/test/http/rows/` | TASK-ROWS row suite | TASK-VERIFY |

Refresh may update only this run's work-pack state, blocker board, and exact
receipt file. It cannot admit the successor, implementation outside declared
targets, publication, deployment, authority changes, or unrelated cleanup.

## Blockers

| ID | Scope | Blocker | Owner route |
| --- | --- | --- | --- |
| CAPI-B001 | all implementation SWUs | Candidate private root is proposed but not owner-approved. | `decision-gate` |
| CAPI-B002 | security/auth/HTTP | Authentication principal/session and secret-provider port owners are unselected. | `decision-gate` |
| CAPI-B003 | runtime admission | Separately launched reader evidence does not exist. | later SWU-CAPI-001 Task Session |
| CAPI-B004 | deployment | Locking, OS sealing, replacement, recovery, and environment matrix are unproven. | L2/L3 owner work, outside current Work Pack execution window |

## Distill and gate verdict

- Smallest coherent API unit: pass (L0 status/catalog/raw).
- SWU atomicity: pass; nine non-task-shaped units.
- First-unit narrowness: pass (SWU-CAPI-001).
- Recomposition: pass; 001-007 recompose L0, 008-009 add conditional L1.
- Hidden gaps: flag; authentication/placement are explicit owner decisions.
- Deferred complexity: pass; replacement/recovery/search/legacy adapters remain
  separate.
- Navigation: pass; every SWU has one task contract and source anchors.

`workPackGateStatus` remains `block` because CAPI-B001/B002 affect acceptance and
the confirmed run did not authorize mutation. No Task Session may infer a route
from this plan.
