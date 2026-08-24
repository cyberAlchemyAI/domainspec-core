---
module: craft-consultation-api
version: current
status: blocked-after-validation
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
| lastUpdatedAt | 2026-08-06T03:12:32Z |
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

The digest is SHA-256 of canonical UTF-8 `{"allowedRoutes":[]}`. Direct user
decision `CAPI-SCOPE-INCLUDE-28` remains the exact source-scope decision, but
the authorized SWU-CAPI-000 `-02` route was consumed and stopped on failed
acceptance-critical validation. A new owner authorization and refreshed
immutable attempt are required before Task Session mutation. SWU-CAPI-001, API
implementation, canonical Craft source mutation, publication, deployment, and
rewrites of either failed attempt remain unauthorized.

## Objective and success

Deliver a private read-only API whose L0 returns authorization-filtered status,
space metadata, and exact raw bytes from one fully verified derived snapshot.
L1 adds only a fixture-validated 0.3.0 row adapter. Success requires executable
contract, privacy, integrity, limit, and fresh-process evidence while preserving
Craft source authority and zero request-path writes.

The admitted runtime order is now explicit: create a new immutable Craft
snapshot with the exact verified npm `@vijayee/wavedb@0.15.9` artifact, verify
that snapshot from a separately launched process, bind the same artifact in the
owner-approved API dependency surface, and only then construct the read-only L0
API. This refresh records the order; it does not execute or admit any step.

## Delivery slices and task board

| Slice | Outcome | Layer | Wave | Task |
| --- | --- | --- | --- | --- |
| S-RUNTIME | 0.15.9 snapshot, fresh-process witness, verifier, invalidation | L0 | W1-W2 | [TASK-RUNTIME](work-pack/tasks/TASK-RUNTIME.md) |
| S-CONTRACT | Schemas, fixtures, opaque IDs, cursors | L0 | W2 | [TASK-CONTRACT](work-pack/tasks/TASK-CONTRACT.md) |
| S-HTTP | Authorized status/catalog/raw slice | L0 | W3 | [TASK-HTTP](work-pack/tasks/TASK-HTTP.md) |
| S-ROWS | One validated 0.3.0 row projection | L1 | W4 | [TASK-ROWS](work-pack/tasks/TASK-ROWS.md) |
| S-VERIFY | Independent closure | L2 | W5 | [TASK-VERIFY](work-pack/tasks/TASK-VERIFY.md) |

All product tasks are `not-started`. TASK-RUNTIME SWU-000 remains the
narrowest reversible predecessor, but its `-02` attempt is closed as blocked
and no SWU is currently selected or admitted.

## SWU execution handoff

| SWU | Parent | Dependencies | Exact write scope | Independent evidence | Status |
| --- | --- | --- | --- | --- | --- |
| SWU-CAPI-000 | TASK-RUNTIME | exact 0.15.9 diagnostic receipts, preserved 0.15.8 scope baseline, `-01` inventory-drift stop, direct option-2 scope decision | `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import/.work/wcli-20260805-node26-0.15.9-02/`, `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import/execution/wcli-20260805-node26-0.15.9-02/` | blocked `-02` receipt: generated `staged/` duplicate was not excluded; no store created; exact 28-ledger/57-record scope unchanged | blocked after acceptance-critical validation; fresh immutable attempt required |
| SWU-CAPI-001 | TASK-RUNTIME | accepted 000 receipt and its closed 0.15.9 snapshot | `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import/execution/wcli-fresh-reader-0.15.9-01/` | child-process 57-record receipt + unchanged inputs/store | blocked |
| SWU-CAPI-002 | TASK-RUNTIME | 001, root approval, exact 0.15.9 dependency pin | `implementation/domainspec/tools/craft-consultation-api/package.json`, `implementation/domainspec/tools/craft-consultation-api/package-lock.json`, `implementation/domainspec/tools/craft-consultation-api/src/snapshot/`, `implementation/domainspec/tools/craft-consultation-api/test/snapshot/` | exact dependency lock + fixture closure/limit suite | blocked |
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

All ten SWUs own one independently reviewable behavior; task-shaped bundles
were split. SWU-CAPI-000 passes the narrow-first-unit test because it changes no
product code or Craft source and creates only isolated derived snapshot
evidence. Its consumed `-02` route cannot be reused. A later refresh must bind
the intended `staged/`-directory exclusion and a fresh immutable attempt
before Task Session can execute again.

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
| 000 | `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import/.work/wcli-20260805-node26-0.15.9-02/`; `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import/execution/wcli-20260805-node26-0.15.9-02/` | TASK-RUNTIME package, exact 28-ledger source manifest, 57-record byte-readback, and immutability checks | 001 becomes dependency-ready, not auto-started |
| 001 | `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import/execution/wcli-fresh-reader-0.15.9-01/` | commands and digests in TASK-RUNTIME | 002 and 004 become dependency-ready, not auto-started |
| 002 | `implementation/domainspec/tools/craft-consultation-api/package.json`; `implementation/domainspec/tools/craft-consultation-api/package-lock.json`; `implementation/domainspec/tools/craft-consultation-api/src/snapshot/`; `implementation/domainspec/tools/craft-consultation-api/test/snapshot/` | TASK-RUNTIME dependency and verifier suite | 003 |
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

## Runtime promotion order

1. **Regenerate derived data:** SWU-CAPI-000 must create a new immutable
   0.15.9 snapshot from the exact manifest-bound 28-ledger/57-record scope:
   the preserved 27-ledger baseline plus the selected nested ledger at SHA-256
   `0effd055c9f25ea3e46de7e5280585f987e9734411ae1639d9c53171b8ed6b84`.
   The `-02` attempt blocked before store creation because the discovery filter
   omitted the literal `staged` directory component from its exclusion set.
   Preserve that receipt; repair only through a fresh immutable attempt.
2. **Prove process independence:** SWU-CAPI-001 must open only the accepted
   closed 0.15.9 snapshot from a separately launched Node process and verify all
   manifest-bound bytes without changing source or store trees.
3. **Pin the API runtime:** before SWU-CAPI-002 writes product code, the
   owner-approved dependency surface must bind Node `v26.6.0`, npm package
   `@vijayee/wavedb@0.15.9`, tarball SHA-256
   `e8156c107117c8bc7f3394ceb16dff439c87c0cb4f8991033dad960b13ae396f`,
   SRI
   `sha512-qoRqZUti9Rjs9UT4rj8cQKNv2Gdr8bJ25p6miU4dKojLeBMfzkgQqp+D/fd2PsaItXyhgMLrlx/wQUmyj/W8hA==`,
   and native-addon SHA-256
   `4846a91117cfeaee42011e401e65448216d85c0ebd04fc860585e3a32e17bb3b`.
4. **Construct read-only behavior:** SWU-CAPI-002 through 007 build L0 from the
   tested core read surface only; SWU-CAPI-008 and 009 remain conditional L1.
   The compiler-warning-bearing, untested WaveDB Subtree API is excluded.

## Blockers

| ID | Scope | Blocker | Owner route |
| --- | --- | --- | --- |
| CAPI-B001 | all implementation SWUs | Candidate private root is proposed but not owner-approved. | `decision-gate` |
| CAPI-B002 | security/auth/HTTP | Authentication principal/session and secret-provider port owners are unselected. | `decision-gate` |
| CAPI-B003 | runtime admission | A 0.15.9 Craft snapshot and separately launched reader evidence do not exist. | later SWU-CAPI-000 then SWU-CAPI-001 Task Sessions |
| CAPI-B004 | deployment | Locking, OS sealing, replacement, recovery, and environment matrix are unproven. | L2/L3 owner work, outside current Work Pack execution window |
| CAPI-B005 | runtime admission | The SWU-CAPI-000 importer does not exclude literal `staged/` directory components, so generated evidence is misclassified as a source ledger. | fresh authorized Invoke Refresh and immutable Task Session attempt |

## Distill and gate verdict

- Smallest coherent API unit: pass (L0 status/catalog/raw).
- SWU atomicity: pass; ten non-task-shaped units.
- First-unit narrowness: pass (SWU-CAPI-000).
- Recomposition: pass; 000-007 recompose L0, 008-009 add conditional L1.
- Hidden gaps: flag; authentication/placement are explicit owner decisions.
- Deferred complexity: pass; replacement/recovery/search/legacy adapters remain
  separate.
- Navigation: pass; every SWU has one task contract and source anchors.

`workPackGateStatus` is `block`: CAPI-B005 stopped the consumed `-02`
attempt before database creation, CAPI-B003 remains open, and CAPI-B001/B002
still block later product units. There are no allowed routes. No retry or
successor may infer authority from the blocked receipt.
