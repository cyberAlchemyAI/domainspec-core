---
module: domainspec-v2-foundation-execution
version: current
status: planned
updatedAt: 2026-07-14
docType: work-pack
---

# WORK-PACK: DomainSpec v2 Foundation Execution

## Purpose

Executable planning source for restoring the DomainSpec v2 retired-orchestration guard and completing the bounded `FPR-01 -> FPR-04` foundation chain.

## Control Fields

| Field | Value | Notes |
|---|---|---|
| workPackGateStatus | pass | Pass applies only to preparing the selected census `SWU-FPR01-001`; execution still requires a later Task Session. |
| complexity | high | Cross-authority, cross-capability, multiple owner decisions. |
| outputMode | split | Task and wave contracts are separate files. |
| executionPackRef | [EXECUTION-PACK.md](EXECUTION-PACK.md) | Wave scheduler. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0-L3 decision boundaries. |
| dispatchTechniqueTrace | [DISPATCH.json](DISPATCH.json) | Governed sequence and boundary evidence. |
| distillValidationStatus | pass | [DISTILL-VALIDATION.md](DISTILL-VALIDATION.md). |
| activeLayerWindow | L1 | Authority census only; profile and semantic work remain blocked. |
| selectedSWU | `SWU-FPR01-001` | Build a deterministic census without selecting an authoritative winner. |
| lastUpdatedAt | 2026-07-14 | Invoke planning receipt date. |
| readinessProfile | pilot | Bounded first profile, not production. |

## Objective Summary

- Objective: establish a trustworthy guard, ratified authority baseline, exact supported profile, governed business-to-Spec mapping, and smallest independently verified Spec graph projection.
- Primary inputs: accepted product decision, approved roadmap/findings, live Craft state, engine-gap findings, and historical SGRM contracts/receipts.
- Success condition: all five waves have named receipts, predecessor digests agree, FPR-04 has exactly one source/two nodes/one edge with a separate comparator, and no artifact claims release authorization.

## Delivery Slices

| Slice | Outcome | Layer | Wave | Dependency | Validation |
|---|---|---|---|---|---|
| S-000 | Restored current zero-active reference proof | L0 | [W0](work-pack/waves/W0-GUARD-REPAIR.md) | historical SGRM receipt + live four-violation state | clean audit + seeded active failure + digest-drift failure |
| S-001 | Ratified non-contradictory authority baseline | L1 | [W1](work-pack/waves/W1-AUTHORITY-BASELINE.md) | S-000 receipt | baseline validator + count/path/status/direction mutants |
| S-002 | Frozen supported profile and digest | L1 | [W2](work-pack/waves/W2-SUPPORTED-PROFILE.md) | S-001 receipt | all-artifact validator + typed negative matrix |
| S-003 | Governed B plane and total B-to-Spec map | L2 | [W3](work-pack/waves/W3-BUSINESS-SPEC.md) | S-002 receipt + direction decision | total-map validator + deletion/endpoint/orphan/collapse mutants |
| S-004 | Tiny authoritative Sg and bounded retraction | L3 | [W4](work-pack/waves/W4-SPEC-PROJECTION.md) | S-003 receipt | source/graph/quotient verifier + independent comparator mutants |

## Task Status Board

| Task | Goal | Layer | Wave | Gate | Status |
|---|---|---|---|---|---|
| [TASK-SGRM-GUARD-REOPEN](work-pack/tasks/TASK-SGRM-GUARD-REOPEN.md) | Reopen SGRM-006/007 against live drift | L0 | W0 | 006 and 007 retry receipts accepted | completed |
| [TASK-FPR-01-AUTHORITY-BASELINE](work-pack/tasks/TASK-FPR-01-AUTHORITY-BASELINE.md) | Ratify one source/count/status baseline | L1 | W1 | W0 accepted; FPR01-001 selected | ready |
| [TASK-FPR-02-SUPPORTED-PROFILE](work-pack/tasks/TASK-FPR-02-SUPPORTED-PROFILE.md) | Freeze exact admitted/exercised profile | L1 | W2 | blocked by FPR-01 | not-started |
| [TASK-FPR-03-BUSINESS-SPEC](work-pack/tasks/TASK-FPR-03-BUSINESS-SPEC.md) | Resolve direction and emit total B-to-Spec map | L2 | W3 | blocked by FPR-02 and frontier | not-started |
| [TASK-FPR-04-SPEC-PROJECTION](work-pack/tasks/TASK-FPR-04-SPEC-PROJECTION.md) | Compile and independently retract tiny Sg | L3 | W4 | blocked by FPR-03 | not-started |

## SWU Execution Handoff

Every row below is an execution handle under an existing SGRM or FPR owner, not a new lifecycle or gap identity.

| SWU | Parent | Source anchors | Dependencies | Write scope | Done/evidence | Validation | Owner | Handoff |
|---|---|---|---|---|---|---|---|---|
| `SWU-SGRM-006-R1` | SGRM guard | live audit; SGRM-006/007 contracts; four files | none | existing SGRM package `runs/SWU-SGRM-006/RETRY-001/` only | line-level disposition JSON + receipt | JSON parse; reviewer confirms every match covered | local Task Session + SGRM plan-owner review | completed |
| `SWU-SGRM-007-R1` | SGRM guard | approved disposition; guard/allowlist/tests | SGRM-006-R1 | exact guard allowlist/tests/package script + `runs/SWU-SGRM-007/RETRY-001/` | zero violations, seeded active and digest drift killed | `npm ... audit:retired-orchestration`; focused tests; typecheck | local Task Session | completed |
| `SWU-FPR01-001` | FPR-01 | meta-types, relationships, definitions, homing decision, EGI-001/002/020 | SGRM-007-R1 | FPR evidence draft/census only | deterministic census with source provenance and disagreements | schema/parse + repeat-run equality | definitions/validation local fallback | selected |
| `SWU-FPR01-002` | FPR-01 | census + `DEC-DSV2-SPEC-HOMING` + active direction sources | FPR01-001 | FPR decision/disposition packet only | every source has owner/disposition; ambiguity routed | Decision Gate review | definitions/layering owners | blocked |
| `SWU-FPR01-003` | FPR-01 | approved dispositions | FPR01-002 | baseline, schema, deterministic validator | non-contradictory baseline validates | positive + stale count/path/status/direction fixtures | validation owner | blocked |
| `SWU-FPR01-004` | FPR-01 | baseline + validator results | FPR01-003 | owner-ratification evidence only | owner receipt binds baseline and input digests | independent receipt verification | definitions/validation/layering owners | blocked |
| `SWU-FPR02-001` | FPR-02 | FPR-01 receipt; GAP-SH-UI11-MIGRATE; product decision | FPR01-004 | FPR-02 decision packet only | exact admitted/excluded profile and origin/redaction decisions | Decision Gate review | claim/semantic owners | blocked |
| `SWU-FPR02-002` | FPR-02 | approved decision packet | FPR02-001 | product/profile schemas and artifacts, pilot matrices, validator | stable digest consumes every artifact | two-run digest equality + schema validation | profile/validation owner | blocked |
| `SWU-FPR02-003` | FPR-02 | profile validator | FPR02-002 | FPR-02 fixtures/evidence only | empty, unknown, absent, placeholder, missing obligation, unresolved origin, empty redaction all fail distinctly | negative matrix command | independent validation owner | blocked |
| `SWU-FPR03-001` | FPR-03 | FR-FPR-ONTOLOGY-DIRECTION; prior ontology findings | FPR02-003 | `decisions/ontology-spec-direction.md` only | direction, supersession, provenance, contradiction policy accepted | Decision Gate + definitions review | semantic/definitions owners | blocked |
| `SWU-FPR03-002` | FPR-03 | direction decision + profile | FPR03-001 | BO/BK/B graphs and schemas | CT-1 and EC-3/EC-4 exist with stable IDs/provenance | schema validation + digest | ontology/business owners | blocked |
| `SWU-FPR03-003` | FPR-03 | BO/BK/B + authoritative Spec disposition | FPR03-002 | B-to-Spec map, validator, evidence | total map; typed deletion/endpoint/orphan/collapse failures | map verifier + mutants | semantic/validation owners | blocked |
| `SWU-FPR04-001` | FPR-04 | FPR-03 receipt + FPR-02 profile | FPR03-003 | required-doc registry, exact source manifest, schemas | one required source resolves; missing/empty/deferred inputs fail | source-manifest verifier | semantic/validation owners | blocked |
| `SWU-FPR04-002` | FPR-04 | exact source manifest + schemas | FPR04-001 | Sg graph + semantic manifest + compiler module/tests | exactly two nodes/one admitted edge; total profile mapping | compiler tests + graph schema | engine owner | blocked |
| `SWU-FPR04-003` | FPR-04 | Sg + authority edge registry | FPR04-002 | quotient registry + local G/compiler IR | every rename/loss is enumerated; unapproved quotient fails | quotient validator + direction mutant | semantic/engine owners | blocked |
| `SWU-FPR04-004` | FPR-04 | Sg, G, quotient registry | FPR04-003 | independent verifier + evidence only | separate Sg-to-G-to-Sg-canonical comparator; node/field/edge/quotient mutants fail | `verify-spec-projection.cjs` + independence review | independent validation owner | blocked |

## Blockers and closed prerequisites

These are plan-local labels, not new Craft gap identities.

| Blocker | Status | Scope | Description | Existing owner | Resolution |
|---|---|---|---|---|---|
| `PLAN-B1-GUARD-RED` | resolved | W0 | The accepted 007 retry receipt proves the current guard and its negative controls. | SGRM-006/007 | proof refresh recorded; W1 opened |
| `PLAN-B2-BASELINE` | active | W1 | Counts, statuses, source homes, and projections disagree. | FPR-01 + `DEC-DSV2-SPEC-HOMING` | census, dispositions, owner receipt |
| `PLAN-B3-PROFILE` | active | W2 | Exact backend/UI admission, origin, redaction, owners, and obligation kinds are unresolved. | FPR-02 + `GAP-SH-UI11-MIGRATE` | Decision Gate before schema promotion |
| `PLAN-B4-DIRECTION` | active | W3 | Precedence/supersession/provenance/contradiction are open. | `FR-FPR-ONTOLOGY-DIRECTION` | Decision Gate and definitions review |
| `PLAN-B5-QUOTIENT` | active | W4 | Permitted Sg-to-G mappings are not yet named. | FPR-04 | enumerate only after authoritative Sg exists |

## Dispatch Technique Trace

| Technique | Applied to | Expectation | Status |
|---|---|---|---|
| sequence | W0 -> W4 | no successor starts without predecessor receipt | pass |
| scu_swu_reduction | first execution boundary | disposition is separated from guard mutation | pass |
| recomposition_proof | SWUs -> FPR route | every unit contributes to one named FPR/SGRM owner | pass |
| state_namespace_boundary | Craft, authority, generated graphs | projections never become authority | pass |
| owner_boundary_check | Invoke -> Task Session/Decision Gate/owners | plan does not claim execution or promotion | pass |
| validation_loop | each wave | positive proof and deliberate red control are paired | pass |
| residue_ledger | blockers and deferred scope | unresolved choices remain visible | pass |

## Gate Checks

1. The current pass selects `SWU-FPR01-001` for a later Task Session; this refresh does not execute it or grant a blanket FPR pass.
2. A Task Session runtime pack must be built from the selected SWU before work begins.
3. One and only one SWU may be selected at a time until a wave receipt closes.
4. Decision-bearing SWUs stop at Decision Gate; implementers cannot choose an authority or product boundary.
5. Any mismatch between Craft and this package defers to Craft and triggers plan refresh.
6. No output may set or imply `production_authorized: true`.

## Change Log

| Date | Change | Author |
|---|---|---|
| 2026-07-14 | Initial Invoke plan from accepted roadmap and live guard evidence | Codex / Invoke |
| 2026-07-14 | Apply-approved refresh consumed the accepted 006 receipt and selected `SWU-SGRM-007-R1` under Decision Gate Option 1 | Codex / Invoke refresh |
| 2026-07-14 | Proof refresh consumed the accepted 007 retry receipt, closed W0, and selected but did not execute `SWU-FPR01-001` | Codex / Invoke refresh |
