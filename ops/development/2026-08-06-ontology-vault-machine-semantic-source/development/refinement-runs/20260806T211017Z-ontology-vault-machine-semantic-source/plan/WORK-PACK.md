---
module: ontology-vault-machine-semantic-source
version: candidate-v1
status: blocked-non-executed
updatedAt: 2026-08-06
docType: work-pack
---

# WORK-PACK: Ontology Vault Machine Semantic Source

## Control Fields

| Field | Value | Notes |
|---|---|---|
| `workPackGateStatus` | `block` | Candidate plan only; no mutation-capable handoff |
| `complexity` | `medium` | Multi-wave, migration, governance, and public capability lifecycle |
| `outputMode` | `split` | Task and wave contracts are separate |
| `executionPackRef` | `EXECUTION-PACK.md` | Choreography only |
| `layeringArtifactRef` | `IMPLEMENTATION-LAYERING.md` | L0-L3 decision owner |
| `distillValidationStatus` | `pass` | Candidate unit/recomposition only |
| `swuAtomicityStatus` | `pass` | 10 one-behavior SWUs; not execution-admitted |
| `firstUnitNarrownessStatus` | `pass` | SWU-OVSS-001 is the narrowest reversible source contract proof |
| `closeoutSyncStatus` | `block` | Exact lifecycle target baselines/receipts require later owner admission |
| `admissionTiming` | `selected-unit-at-task-session` | No unit selected |
| `executionEntryState` | `blocked` | See `EXECUTION-ENTRY.json` |
| `allowedRoutesDigest` | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | Digest of canonical empty route list `[]` |
| `activeLayerWindow` | `L0` | Planned first proof only |
| `readinessProfile` | `pilot` | Candidate goal, not current claim |

## Execution Policy

```yaml
executionPolicy:
  routePolicy: blocked-until-owner-admission
  allowedRoutes: []
  allowedRoutesDigest: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
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
  validationPolicy: owner-gates-remain-mandatory

executionEntry:
  state: blocked
  selectedUnit: null
  routeId: null
  nextOwner: ontology-vault-lifecycle-owner
```

This Work Pack does not authorize execution. A later owner-approved Invoke
Refresh/Plan must materialize exact allowed routes, closeout contracts, current
target baselines, and a passing Implementation Readiness projection.

## Objective Summary

- Objective: implement and validate the repaired source-to-view architecture as
  a reusable Ontology Vault candidate without collapsing source, projection,
  admission, promotion, migration, or private adopter ownership.
- Primary inputs: Stages 05–08 and `IMPLEMENTATION-LAYERING.md`.
- Success: every layer produces its declared finite evidence; public mutation
  occurs only through Sigil Development and explicit owner approval.

## Delivery Slices

| Slice | Outcome | Layer | Wave | Dependency | Validation |
|---|---|---|---|---|---|
| S-001 | Closed package and record/relation schema contracts | L0 | W0 | owner/design gates | schema plus positive/negative fixtures |
| S-002 | Deterministic canonical source and normalized model | L0 | W0 | S-001 | repeat builds and digest-domain checks |
| S-003 | Verified Markdown projection and correction proposal | L0 | W0 | S-002 | trace recomputation, drift/invention negatives |
| S-004 | Humane authoring and multi-view parity | L1 | W1 | W0 pass | author journey, semantic diff, graph/query parity |
| S-005 | Admission, migration, rollback, and privacy hardening | L2 | W2 | W1 pass | owner/migration/leakage witnesses |
| S-006 | Lifecycle integration and reusable packaging | L3 | W3 | W2 plus explicit approval | Sigil Development and generated parity receipts |

## Task Status Board

| Task | Goal | Layer | Wave | Gate | Status |
|---|---|---|---|---|---|
| [TASK-OVSS-01](work-pack/tasks/TASK-OVSS-01.md) | Source and protocol schemas | L0 | [W0](work-pack/waves/W0.md) | blocked by B-001/B-003 | not-started |
| [TASK-OVSS-02](work-pack/tasks/TASK-OVSS-02.md) | Canonicalizer and normalized model | L0 | [W0](work-pack/waves/W0.md) | depends TASK-01 | not-started |
| [TASK-OVSS-03](work-pack/tasks/TASK-OVSS-03.md) | Projection algebra, verifier, receipt | L0 | [W0](work-pack/waves/W0.md) | depends TASK-02 | not-started |
| [TASK-OVSS-04](work-pack/tasks/TASK-OVSS-04.md) | Authoring, semantic diff, graph/query views | L1 | [W1](work-pack/waves/W1.md) | W0 evidence and B-002 | not-started |
| [TASK-OVSS-05](work-pack/tasks/TASK-OVSS-05.md) | Admission, migration, rollback, privacy | L2 | [W2](work-pack/waves/W2.md) | W1 evidence and owner decisions | not-started |
| [TASK-OVSS-06](work-pack/tasks/TASK-OVSS-06.md) | Public lifecycle integration and packaging | L3 | [W3](work-pack/waves/W3.md) | W2, B-003/B-004 | not-started |

## SWU Manifest

| SWU | Parent | Primary behavior | Dependency | Proposed write scope | Acceptance boundary | Owner | Status |
|---|---|---|---|---|---|---|---|
| SWU-OVSS-001 | [TASK-01](work-pack/tasks/TASK-OVSS-01.md) | Validate closed package inventory | B-001/B-003 | `arcanum/arcana/ontology-vault/development/semantic-source-spine/schemas/`, `fixtures/package-closure/` | package positives pass; path/remote/undeclared negatives fail | Sigil Development task route | blocked |
| SWU-OVSS-002 | [TASK-01](work-pack/tasks/TASK-OVSS-01.md) | Validate conditional record/relation/type families | 001 | same development package schema/fixture roots | IDs, families, endpoints, axes discriminate | Sigil Development task route | blocked |
| SWU-OVSS-003 | [TASK-01](work-pack/tasks/TASK-OVSS-01.md) | Validate projection/protocol object schemas | 002 | same schemas plus `fixtures/protocol/` | patch/receipt/admission/migration shapes discriminate | Sigil Development task route | blocked |
| SWU-OVSS-004 | [TASK-02](work-pack/tasks/TASK-OVSS-02.md) | Canonicalize exact package bytes deterministically | 001–003 | `arcanum/arcana/ontology-vault/development/semantic-source-spine/src/canonicalization/`, `arcanum/arcana/ontology-vault/development/semantic-source-spine/fixtures/canonicalization/` | exact/canonical digest witnesses pass | Sigil Development task route | blocked |
| SWU-OVSS-005 | [TASK-02](work-pack/tasks/TASK-OVSS-02.md) | Produce disposable normalized model | 004 | `arcanum/arcana/ontology-vault/development/semantic-source-spine/src/normalization/`, `arcanum/arcana/ontology-vault/development/semantic-source-spine/fixtures/normalization/` | byte-identical model and IR-as-source rejection | Sigil Development task route | blocked |
| SWU-OVSS-006 | [TASK-03](work-pack/tasks/TASK-OVSS-03.md) | Compile Markdown with closed operation algebra | 005 | `arcanum/arcana/ontology-vault/development/semantic-source-spine/src/projection/`, `arcanum/arcana/ontology-vault/development/semantic-source-spine/fixtures/projection/` | deterministic view plus trace | Sigil Development task route | blocked |
| SWU-OVSS-007 | [TASK-03](work-pack/tasks/TASK-OVSS-03.md) | Independently verify trace/receipt/non-invention | 006 | `arcanum/arcana/ontology-vault/development/semantic-source-spine/src/projection/`, `arcanum/arcana/ontology-vault/development/semantic-source-spine/fixtures/projection/` | stale/invented/nondeterministic outputs fail | Sigil Development task route | blocked |
| SWU-OVSS-008 | [TASK-04](work-pack/tasks/TASK-OVSS-04.md) | Author and correct through atomic SourcePatch | W0/B-002 | `arcanum/arcana/ontology-vault/development/semantic-source-spine/src/authoring/`, `arcanum/arcana/ontology-vault/development/semantic-source-spine/fixtures/authoring/` | complete author journey and recovery | Sigil Development + UX validation | blocked |
| SWU-OVSS-009 | [TASK-05](work-pack/tasks/TASK-OVSS-05.md) | Govern admission and copy/verify migration | 008/owner decision | `arcanum/arcana/ontology-vault/development/semantic-source-spine/src/governance/`, `arcanum/arcana/ontology-vault/development/semantic-source-spine/fixtures/migration/` | event chain, total map, partial block, rollback | Ontology Vault owner + Sigil Development | blocked |
| SWU-OVSS-010 | [TASK-06](work-pack/tasks/TASK-OVSS-06.md) | Integrate approved convention and generated projections | 009/B-003/B-004 | exact targets to be owner-approved | canonical validation and generated parity | Sigil Development | blocked |

## SWU Atomicity Review

| SWU | Candidate child split | Why retained | Verdict |
|---|---|---|---|
| 001 | schema vs fixtures | A closure schema has no independent acceptance without discriminating fixtures | pass |
| 002 | records vs relations vs type | Endpoint/type validation is the one cross-field behavior under test | pass |
| 003 | six protocol objects | One closed inter-object validation family; if implementation shows independent release pressure, split before admission | pass with future split check |
| 004 | parser vs serializer vs digest | None independently proves canonicalization | pass |
| 005 | flatten vs order vs digest | One normalized-model output boundary | pass |
| 006 | operation graph vs Markdown bytes vs trace | Trace is required output of the one compile behavior | pass |
| 007 | receipt vs verifier vs negatives | Receipt passes only through independent verification | pass |
| 008 | forms vs diff vs patch/recovery | One complete author correction journey; UX evidence must test the whole journey | pass |
| 009 | admission vs migration | Both are owner transitions, but can pass independently; split before execution if one is selected | flag until later Plan refresh |
| 010 | canonical mutation vs generated sync | Same Sigil Development lifecycle closeout, but exact targets must be split if write scopes diverge | flag until later Plan refresh |

No mutation-capable handoff is allowed while flagged SWUs remain unsplit.

## First-Unit Narrowness

SWU-OVSS-001 is the first frontier because it proves only package closure and
path/reference rejection. It does not bundle record semantics, canonicalizer,
projection, authoring, migration, or public adoption. It is reversible and
creates the smallest trust-bearing contract needed by every successor.

## Validation Strategy

Designed command families, to be made exact when paths/runtime are selected:

- parse every schema and fixture JSON;
- run schema positives and one negative per closure/family/protocol invariant;
- canonicalize the same package twice and compare exact bytes/digests;
- normalize formatting variants and compare canonical/model digests;
- compile Markdown twice and compare trace/output bytes;
- rerun projection verifier independently;
- assert stale, invented, direct-writeback, missing-endpoint,
  nondeterministic-time, IR-as-source, and no-admission negatives;
- run leakage scan over public schema/description/example/fixture/output bytes;
- run scoped whitespace and public/private boundary checks;
- run generated skill parity only in W3 after canonical lifecycle mutation.

Commands remain designed, not executed, until each SWU has exact files and
owner-selected implementation language/runtime.

## Task Session Closeout Sync

Status: `block`. No mutation-capable SWU has an admitted exact target baseline,
allowed-delta inventory, owner validation command, expected receipt path, and
deterministic successor contract. A later owner-approved Plan refresh must add
one complete row per selected SWU before Task Session admission.

## Blockers

| ID | Description | Owner | Resolution |
|---|---|---|---|
| B-001 | No DesignScopeManifest, independent denominator, fixed-point selection result, or exact schema bytes | Invoke Design/validator owner | Materialize candidate contracts and validator receipts |
| B-002 | Human authoring surface lacks formal UX plan and executed usability evidence | UX plan owner + Ontology Vault authoring owner | Specify/test create-review-correct-recover journey |
| B-003 | Closed JSON and exact ontology delta are parent-selected candidates, not public owner decisions | Ontology Vault lifecycle owner | Explicitly approve, revise, or reject candidate direction |
| B-004 | Public implementation targets, language/runtime, validators, closeout baselines, and Sigil Development route are not admitted | Sigil Development + Invoke Plan refresh | Bind exact paths, commands, receipts, and routes |

## Dispatch Technique Trace

| Technique | Applied to | Result |
|---|---|---|
| sequence | Design -> layers -> tasks -> SWUs -> lifecycle handoff | pass |
| scu_swu_reduction | Source-to-view kernel and 10 SWUs | pass; 009/010 require later split |
| recomposition_proof | Every SWU/layer back to one-source invariant | pass |
| validation_loop | Positive/negative witnesses per slice | pass as designed, unexecuted |
| owner_boundary_check | Invoke authors plan; Sigil Development/owners mutate | pass |
| handle_handoff | Source paths and receipts, not copied authority | pass |
| residue_ledger | Four blockers and deferred YAML/JSON-LD/RWO work | pass |
| execution_receipt_handoff | Exact receipt requirement before mutation | block pending B-004 |

## Distill Validation

| Check | Result | Evidence/gap |
|---|---|---|
| Smallest coherent unit | pass | Stage 05 kernel |
| Recomposition | pass | Stage 08 repaired invariants |
| SWU atomicity | flag | SWU-009 and 010 must split on later admission |
| First-unit narrowness | pass | SWU-001 only package closure |
| Hidden acceptance gaps | flag | Design/UX/owner/target blockers B-001–B-004 |
| Deferred complexity | pass | L1–L3 explicit |
| Navigation | pass | Work Pack links every task and wave |

## Claim Ceiling

This Work Pack is non-executed and gate-blocked. It is not Task Session
admission, implementation authorization, public convention approval, release,
deployment, production readiness, migration authority, or RWO gate resolution.
