---
module: body-war-suggested-track-ontology-domainspec-integration
version: current
status: complete
updatedAt: 2026-07-27
docType: work-pack
---

# WORK-PACK: SuggestedTrack Ontology and DomainSpec Proof Track

## Control Fields

| Field | Value |
| --- | --- |
| workPackGateStatus | pass |
| complexity | medium |
| outputMode | split |
| executionPackRef | `EXECUTION-PACK.md` |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` |
| dispatchTechniqueTrace | `DISPATCH-TRACE.md` |
| distillValidationStatus | pass |
| swuAtomicityStatus | pass |
| firstUnitNarrownessStatus | pass |
| closeoutSyncStatus | pass |
| activeLayerWindow | L3 |
| selectedSWU | none |
| planEvidence | verification-evidence-complete |
| readinessProfile | experimental |

## Objective

Implement and independently execute:

1. one Body War local ontology test;
2. one canonical DomainSpec CT-2 behavior test;
3. one exact-digest integration test.

Success requires all three receipts plus negative controls. It proves only the
experimental CT-2 seam.

## Delivery Slices

| Slice | Outcome | Layer | Wave | Dependency | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | local ontology contract and standalone receipt | L0 | W0 | none | ontology positive and invalid-transition tests |
| S-002 | canonical node behavior and standalone receipt | L1 | W1 | S-001 ordering only; no data dependency | deterministic build, backend comparison, mutation control |
| S-003 | digest-bound composition receipt | L2 | W2 | S-001 and S-002 receipts | positive bridge, stale digest, insufficient state |
| S-004 | reproducibility and claim-ceiling closeout | L3 | W3 | S-003 | two-run digest comparison and residue audit |

## Task Board

| Task | Goal | Layer | Wave | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-BWOI-ONTOLOGY](work-pack/tasks/TASK-BWOI-ONTOLOGY.md) | validate local CT-2 ontology | L0 | [W0](work-pack/waves/W0.md) | complete | completed |
| [TASK-BWOI-DOMAINSPEC](work-pack/tasks/TASK-BWOI-DOMAINSPEC.md) | derive and execute canonical CT-2 | L1 | [W1](work-pack/waves/W1.md) | complete | completed |
| [TASK-BWOI-INTEGRATION](work-pack/tasks/TASK-BWOI-INTEGRATION.md) | enforce digest-bound composition | L2 | [W2](work-pack/waves/W2.md) | complete | completed |
| [TASK-BWOI-VERIFY](work-pack/tasks/TASK-BWOI-VERIFY.md) | reproduce and audit all receipts | L3 | [W3](work-pack/waves/W3.md) | complete | completed |

## SWU Manifest

| SWU | Parent | Primary behavior | Independent acceptance | Dependency | Owner | Handoff |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-BWOI-001 | TASK-BWOI-ONTOLOGY | validate CT-2 ontology entry set | standalone ontology receipt passes and illegal transition rejects | none | local-fallback | completed |
| SWU-BWOI-002 | TASK-BWOI-DOMAINSPEC | prove canonical CT-2 against memory adapter | standalone DS proof passes and backend mutation rejects | SWU-BWOI-001 ordering gate | local-fallback | completed |
| SWU-BWOI-003 | TASK-BWOI-INTEGRATION | admit only exact ontology/DS binding | integration passes; stale digest and insufficient state reject | SWU-BWOI-001, SWU-BWOI-002 | local-fallback | completed |

TASK-BWOI-VERIFY is closure-only and uses the permitted `VERIFY` SWU
exemption.

## Atomicity Review

| SWU | Candidate child units | Retained-boundary rationale | Verdict |
| --- | --- | --- | --- |
| SWU-BWOI-001 | schema, entries, positive test, negative test | schema and fixtures have no useful verdict without the validator; both polarities define one semantic acceptance boundary | pass |
| SWU-BWOI-002 | node graph, DS evaluation, adapter, mutation | compilation alone proves structure, not behavior; CT-2 acceptance requires generated expectation and observed backend result | pass |
| SWU-BWOI-003 | bridge schema, digest checks, state check, execution | individual checks can unit-test internally, but the SWU owns one admission decision and one integration receipt | pass |

The first unit is narrowest because it writes only local experimental ontology
artifacts and cannot affect app runtime, DomainSpec v2, or promotion state.

## Validation Strategy

Run TypeScript proof tests through the checked-in DomainSpec v2 implementation
toolchain:

```bash
(cd projects/domainspec-v2/impl && node --import tsx --test \
  ../../body-war/proofs/suggested-track-ontology-domainspec/tests/*.test.ts)
```

Every test:

- uses input-only fixtures;
- emits a deterministic receipt under the Body War proof root;
- includes at least one negative control;
- returns non-zero on a failed claim;
- records `authority_effect: none` and `release_admission: not-granted`.

Final scoped checks:

```bash
npm --prefix projects/body-war/app test
git diff --check -- projects/body-war
```

## Task Session Closeout Sync Contract

| SWU | Lifecycle owner route | Terminal source receipt | Exact targets | Baseline | Allowed deltas | Owner validation | Expected owner receipt | Successor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-BWOI-001 | `invoke:refresh:apply-approved` | Task Session result with SWU id, files, commands, verdict, blockers and residue | `WORK-PACK.md`; `work-pack/tasks/TASK-BWOI-ONTOLOGY.md`; `.craft/ledger.yml`; `CRAFT.md` | digest each target at Task Session preflight; reject post-start drift | evidence-added, status-changed, BWOI blocker opened/resolved, route-changed | ontology test; app test; `git diff --check -- projects/body-war` | `projects/body-war/development/task-sessions/SWU-BWOI-001/closeout/INVOKE-REFRESH-RECEIPT.md` | SWU-BWOI-002 only after pass |
| SWU-BWOI-002 | `invoke:refresh:apply-approved` | same structured result contract | `WORK-PACK.md`; `work-pack/tasks/TASK-BWOI-DOMAINSPEC.md`; `.craft/ledger.yml`; `CRAFT.md` | live preflight digest rule | same BWOI-scoped deltas | DomainSpec test; app test; scoped diff check | `projects/body-war/development/task-sessions/SWU-BWOI-002/closeout/INVOKE-REFRESH-RECEIPT.md` | SWU-BWOI-003 only after pass |
| SWU-BWOI-003 | `invoke:refresh:apply-approved` | same structured result contract | `WORK-PACK.md`; `work-pack/tasks/TASK-BWOI-INTEGRATION.md`; `.craft/ledger.yml`; `CRAFT.md` | live preflight digest rule | same BWOI-scoped deltas | all proof tests; app test; scoped diff check | `projects/body-war/development/task-sessions/SWU-BWOI-003/closeout/INVOKE-REFRESH-RECEIPT.md` | TASK-BWOI-VERIFY only after pass |
| TASK-BWOI-VERIFY | `invoke:refresh:apply-approved` | Task Session result with task id, files, commands, verdict, blockers and residue | `WORK-PACK.md`; `work-pack/tasks/TASK-BWOI-VERIFY.md`; `.craft/ledger.yml`; `CRAFT.md` | live preflight digest rule; reject post-start drift | evidence-added, status-changed, BWOI blocker opened/resolved, route-changed | full proof suite twice with identical receipt digests; app test; scoped diff check; Craft ledger/index/view checks | `projects/body-war/development/task-sessions/TASK-BWOI-VERIFY/closeout/INVOKE-REFRESH-RECEIPT.md` | none; terminal experiment-close route only |

Closeout may synchronize evidence and route state only. It cannot authorize
another SWU, promote ontology, release DomainSpec, deploy, or accept product
risk.

The terminal Task Session result and the Invoke Refresh owner receipt are
separate artifacts. The owner receipt may reference the terminal result but
must not replace or rewrite it.

`TASK-BWOI-VERIFY` has no successor. A passing closeout ends this experiment;
any further promotion, release, deployment, or wider formalization requires a
new bounded plan and its own authorization.

## Dispatch Technique Trace

| Technique | Plan effect | Result |
| --- | --- | --- |
| `sequence` | W0 and W1 receipts feed W2; W2 feeds W3 | pass |
| `scu_swu_reduction` | exactly one primary behavior per SWU | pass |
| `recomposition_proof` | integration references both standalone receipts | pass |
| `validation_loop` | positive and negative evidence in every slice | pass |
| `owner_boundary_check` | Invoke authors; Task Session executes; owners retain promotion | pass |
| `handle_handoff` | paths and digests cross task boundaries | pass |
| `residue_ledger` | three named gaps remain visible | pass |
| `execution_receipt_handoff` | exact Task Session result paths and successors | pass |

## Distill Validation

| Check | Result | Evidence |
| --- | --- | --- |
| smallest coherent unit | pass | SWU-BWOI-001 validates one local ontology meaning boundary |
| SWU atomicity | pass | three SWUs, zero task-shaped units |
| first-unit narrowness | pass | ontology-only local files, no runtime or upstream mutation |
| recomposition | pass | W2 consumes W0/W1 receipts by digest |
| hidden acceptance gaps | pass | generic DS APIs exist; FS-specific runner reuse is forbidden |
| deferred complexity | pass | promoted ontology, Postgres parity, native schema field, release deferred |
| navigation | pass | selected SWU links to one task contract and W0 |

Full role trace: `DISTILL-VALIDATION.md`.

## Blockers and Gaps

No implementation blocker remains within the completed experiment.

| ID | Kind | Owner | Repair or boundary |
| --- | --- | --- | --- |
| GAP-BWOI-001 | implementation gap | DomainSpec engine owner | use generic compiler/projection/evaluator APIs; do not copy FS runner |
| GAP-BWOI-002 | authority gap | Body War ontology owner | experimental candidate lane only; formal promoted lane must reject |
| GAP-BWOI-003 | profile gap | DomainSpec profile owner | remain within Rule, Operation, Event and admitted edges |

## Recomposition Claim

```text
ontology receipt + DomainSpec receipt + exact bridge
  -> integrated CT-2 receipt
  -> reproducibility and claim-ceiling audit
```

The composition proves one rule seam. It does not prove all SuggestedTrack
behavior or either platform’s release readiness.

## Next Route

None. The current experiment is closed. Any promotion, release, deployment, or
wider formalization requires a new bounded plan and explicit authorization.
