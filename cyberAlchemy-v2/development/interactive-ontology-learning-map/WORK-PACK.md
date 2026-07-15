---
module: interactive-ontology-learning-map
version: 0.1.0-candidate
status: blocked
updatedAt: 2026-07-14
docType: work-pack
---

# WORK-PACK: Interactive Ontology Learning Map

## Control fields

| Field | Value |
|---|---|
| workPackGateStatus | `block` |
| complexity | `high` |
| outputMode | `split` |
| executionPackRef | [EXECUTION-PACK.md](./EXECUTION-PACK.md) |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](./IMPLEMENTATION-LAYERING.md) |
| dispatchTechniqueTrace | [DISPATCH.json](./DISPATCH.json) |
| distillValidationStatus | `pass` — [DISTILL-VALIDATION.md](./DISTILL-VALIDATION.md) |
| activeLayerWindow | `pre-L0` |
| readinessProfile | `pilot` |
| nextRoute | `deferred` — resolve G-DSV2-SG through the existing DomainSpec owner route; G-OWNER is recorded |

## Objective

Deliver a private, deterministic, source-preserving ontology learning-map witness that makes semantic, epistemic, governance, operational, and pedagogical connections inspectable without collapsing their types or authority.

The planning package is structurally complete and G-OWNER has passed. Prototype mutation remains blocked because DomainSpec has not yet supplied the exact owner-generated `Sg` plus its prerequisite FPR receipts.

## Delivery slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
|---|---|---|---|---|---|
| S-000 | Projection owner and schema approval route named | L0 | [W0](work-pack/waves/W0.md) | none | signed/recorded decision with scope and downstream owner |
| S-000B | Exact DomainSpec `Sg` readiness handle verified without changing upstream state | pre-L0 | [W0](work-pack/waves/W0.md) | live guard plus existing FPR-01/02/03/04 owner receipts | schema-valid graph/quotient/retraction receipt and bound handle |
| S-001 | Read-only import/projection contract, source manifest, and failure fixtures locked | L0 | [W1](work-pack/waves/W1.md) | S-000, S-000B | schema validator positive/negative suite |
| S-002 | Deterministic immutable snapshot compiler | L1 | [W2](work-pack/waves/W2.md) | S-001 | repeated clean-build equality and identity-change tests |
| S-003 | AEO/Financial/Craft witnesses compile honestly | L1 | [W2](work-pack/waves/W2.md) | S-001, S-002 | admitted/rejected relation and claim-ladder fixtures |
| S-004 | Bounded GET-only read surface | L1 | [W2](work-pack/waves/W2.md) | S-002 | route inventory, query fixtures, path-boundary tests |
| S-005 | Equivalent learning interface | L2 | [W3](work-pack/waves/W3.md) | S-003, S-004 | graph/hierarchy/table parity and two journeys |
| S-006 | Evidence-backed private pilot decision | L3 | [W4](work-pack/waves/W4.md) | S-005 | determinism, a11y, performance, comprehension receipts |

## Task status board

| Task | Goal | Layer | Complexity | Wave | Gate | Status |
|---|---|---|---|---|---|---|
| [TASK-IOLM-000](work-pack/tasks/TASK-IOLM-000-OWNER.md) | resolve projection owner | L0 | medium | W0 | pass | completed |
| [TASK-IOLM-000B](work-pack/tasks/TASK-IOLM-000B-DOMAINSPEC-SG-READINESS.md) | verify exact upstream `Sg` readiness handle | pre-L0 | medium | W0 | blocked by existing FPR owners | not-started |
| [TASK-IOLM-001](work-pack/tasks/TASK-IOLM-001-CONTRACT.md) | lock read-only import/projection contract and fixtures | L0 | high | W1 | blocked by G-DSV2-SG | not-started |
| [TASK-IOLM-002](work-pack/tasks/TASK-IOLM-002-COMPILER.md) | build deterministic compiler | L1 | high | W2 | dependency | not-started |
| [TASK-IOLM-003](work-pack/tasks/TASK-IOLM-003-WITNESSES.md) | compile ontology/Craft witnesses | L1 | high | W2 | dependency | not-started |
| [TASK-IOLM-004](work-pack/tasks/TASK-IOLM-004-READ-API.md) | serve immutable GET queries | L1 | medium | W2 | dependency | not-started |
| [TASK-IOLM-005](work-pack/tasks/TASK-IOLM-005-LEARNING-UI.md) | deliver equivalent UI surfaces | L2 | high | W3 | dependency | not-started |
| [TASK-IOLM-006](work-pack/tasks/TASK-IOLM-006-EVIDENCE-PILOT.md) | verify and pilot private witness | L2/L3 | high | W4 | dependency | not-started |

## SWU execution handoff

| SWU | Parent | Dependencies | Write scope | Acceptance evidence | Validation | Owner | Handoff |
|---|---|---|---|---|---|---|---|
| SWU-IOLM-000-A | TASK-IOLM-000 | none | `work-pack/shared/G-OWNER-DECISION.md` | named schema owner, posture, vocabulary route | decision-gate receipt review: pass | manual/decision-gate | completed; G-OWNER handle recorded |
| SWU-IOLM-000B-A | TASK-IOLM-000B | live guard; FPR-01/02/03/04 owner receipts | `work-pack/session-evidence/SWU-IOLM-000B-A/` only | exact schema-valid `Sg`, quotient, retraction, identities, and readiness handle | read-only receipt/schema verification | task-session verify | blocked |
| SWU-IOLM-001-A | TASK-IOLM-001 | G-OWNER and G-DSV2-SG | `prototype/contracts/`, `prototype/fixtures/non-collapse/` | read-only import/projection schemas plus one fixture per law | schema test command chosen with host | task-session | blocked |
| SWU-IOLM-001-B | TASK-IOLM-001 | 001-A | `prototype/manifests/`, `prototype/fixtures/sources/` | default-deny pinned manifest | manifest validator | task-session | blocked |
| SWU-IOLM-002-A | TASK-IOLM-002 | 001-A/B and G-DSV2-SG | `prototype/src/compiler/`, `prototype/tests/compiler/` | read-only `Sg` import and source-preserving projection build | unit/schema tests | task-session | blocked |
| SWU-IOLM-002-B | TASK-IOLM-002 | 002-A | `prototype/src/layout/`, `prototype/src/search/` | deterministic layout/search artifacts | double-build comparison | task-session | blocked |
| SWU-IOLM-003-A | TASK-IOLM-003 | 002-A and G-DSV2-SG | `prototype/fixtures/aeo/`, `prototype/tests/witnesses/` | unchanged imported edge plus EGI-008/010/011 negative receipts | witness tests | task-session | blocked |
| SWU-IOLM-003-B | TASK-IOLM-003 | 003-A | `prototype/fixtures/financial-settlement/`, `prototype/fixtures/craft/` | positive fixture and five-class journey | fixture tests | task-session | blocked |
| SWU-IOLM-004-A | TASK-IOLM-004 | 002-A/B | `prototype/src/api/`, `prototype/tests/api/` | GET-only route family | API tests and route scan | task-session | blocked |
| SWU-IOLM-005-A | TASK-IOLM-005 | 003-B, 004-A | `prototype/src/ui/read-model/`, `prototype/tests/parity/` | shared typed read model and parity oracle | parity tests | task-session | blocked |
| SWU-IOLM-005-B | TASK-IOLM-005 | 005-A | `prototype/src/ui/`, `prototype/tests/ui/` | graph, hierarchy, table, journeys | browser journey tests | task-session | blocked |
| SWU-IOLM-006-A | TASK-IOLM-006 | 005-B | `prototype/tests/evidence/`, `prototype/runs/` | gate receipts for determinism/a11y/perf | full evidence command | task-session | blocked |
| SWU-IOLM-006-B | TASK-IOLM-006 | 006-A | `prototype/pilot/`, `prototype/runs/pilot/` | protocol, raw data, bounded verdict | human review + rubric | manual + task-session evidence | blocked |

Task files carry full source anchors, done criteria, related context, synchronization, and recomposition notes.

## Blockers and deferred residue

| ID | Disposition | Scope | Owner | Resolution |
|---|---|---|---|---|
| G-OWNER | resolved gate | none; handle required downstream | [G-OWNER decision](work-pack/shared/G-OWNER-DECISION.md) | `private-learning-map-product-owner` selected with projection-bounded authority |
| B-VOCAB | resolved for private projection scope | none at candidate stage | projection owner plus definitions/source-owner handback | local enums governed; authority-relevant terms remain candidates upstream |
| SGRM-006 | upstream blocker projection | DomainSpec guard/FPR route | existing DomainSpec owner | owner receipt showing legacy oracle retirement is complete |
| SGRM-007 | upstream blocker projection | DomainSpec guard/FPR route | existing DomainSpec owner | owner receipt showing no executable retired-reference guard remains |
| FPR-01 | upstream prerequisite | G-DSV2-SG | existing FPR-01 owner | authority-baseline receipt |
| FPR-02 | upstream prerequisite | G-DSV2-SG | existing FPR-02 owner | supported-profile receipt |
| FPR-03 | upstream prerequisite | G-DSV2-SG | existing FPR-03 owner | precedence/direction receipt |
| FPR-04 | upstream prerequisite | G-DSV2-SG | existing FPR-04 owner | bounded `Sg`, quotient, and independent retraction receipt |
| G-DSV2-SG | local consumer gate | all prototype mutation | TASK-IOLM-000B read-only verifier | exact FPR receipts and bound read-only `Sg` handle |
| D-WEBSITE | deferred | production integration | website product/architecture owner | select host after private witness evidence |
| D-EDITOR | deferred | maintained journeys | learning-content owner | approve editorial lifecycle after pilot |
| D-PUBLIC | deferred | Arcanum-only derivative | separate projection/publication owners | new Invoke and exact-manifest public proof |
| D-SCALE | deferred | alternate renderer | performance/accessibility review | open only after measured trigger |
| B-SWU-TERM | learner-copy blocker | expanded acronym | Craft definitions owner | resolve definition drift |

## Gate checks

1. `workPackGateStatus` remains `block` while G-DSV2-SG is unresolved.
2. G-OWNER is persisted and G-DSV2-SG must close before any task writes under `prototype/`; neither gate's evidence may waive the other.
3. Each multi-SWU task executes one selected SWU at a time through Task Session.
4. No two SWUs may write the same path concurrently.
5. Every layer promotion cites its exact evidence receipt.
6. Distill validation passes structural coherence but cannot waive authority.
7. Production website and public derivative remain outside the active execution pack.

## Technique trace

| Technique | Concrete effect | Status |
|---|---|---|
| `sequence` | owner decision + upstream `Sg` verification -> import contract -> compiler/witness/API -> UI -> evidence | pass |
| `scu_swu_reduction` | thirteen bounded SWUs with one write scope and evidence surface | pass |
| `recomposition_proof` | every SWU maps to slice, layer decision, SPEC criterion | pass |
| `artifact_contract_bridge` | define/design contracts become task acceptance evidence | pass |
| `state_namespace_boundary` | projection/source/claim/Craft/publication statuses remain separate | pass |
| `owner_boundary_check` | Decision Gate owns local owner selection; existing FPR owners retain DomainSpec authority; Task Session verifies or mutates only its declared scope | pass |
| `validation_loop` | every slice has positive and negative evidence | pass |
| `execution_receipt_handoff` | each SWU returns artifact, validation, residue, next route | pass |
| `residue_ledger` | blockers and deferred scope are named, owned, and routed | pass |

## Next handoff

G-OWNER is complete through [TASK-IOLM-000](work-pack/tasks/TASK-IOLM-000-OWNER.md). Run the existing DomainSpec guard/FPR route to produce the exact FPR-01/02/03/04 receipts, then verify them through [TASK-IOLM-000B](work-pack/tasks/TASK-IOLM-000B-DOMAINSPEC-SG-READINESS.md). When G-DSV2-SG passes, Context Builder may prepare `SWU-IOLM-001-A` for Task Session using both handles.
