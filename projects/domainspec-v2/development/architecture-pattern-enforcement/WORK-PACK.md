---
module: architecture-pattern-enforcement
feature_code: APE
version: current
status: draft
updatedAt: 2026-07-02
docType: work-pack
---

# WORK-PACK: architecture-pattern-enforcement

Canonical executable plan for the APE program. The coordinator control panel: objective, slices,
tasks, SWUs, gates, blockers. Split-capable; single-file for now (task files created at execution
time by `task-session`).

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass (L0 node plane) / flag (edge plane) | W0 done; W1 executable; W2 edge tasks unblocked by R3A but still depend on L1 repeatability; W3 formalism remains blocked. |
| complexity | high | |
| outputMode | single-file | split into `work-pack/tasks/*` at execution time. |
| executionPackRef | execution-pack.md | |
| layeringArtifactRef | implementation-layering.md | |
| dispatchTechniqueTrace | sequence, scu_swu_reduction, recomposition_proof, validation_loop, owner_boundary_check, residue_ledger | see trace below. |
| distillValidationStatus | pass | G-001 resolved (DEC-DSV2-APE-L0-DOMAIN → reuse financial-settlement, 2026-07-02); recorded in `.craft` ledger. |
| activeLayerWindow | L1 | |
| lastUpdatedAt | 2026-07-02 | |
| readinessProfile | pilot | |

## Objective Summary

- Objective: stand up a **witnessed, CI-gated node plane** (uniformity) on ≥2 real feature packs with
  the v1 pattern-library triaged in as the authoring/card layer — then sequence the edge plane
  (composability, layering), authority promotion, and cross-project inheritance behind their named
  dependencies.
- Primary inputs: [SPEC.md](SPEC.md), [architecture-bundle.md](architecture-bundle.md),
  [implementation-layering.md](implementation-layering.md), and the
  [research findings](../../research/2026-07-02-architecture-patterns-enforcement/findings.md).
- Success condition: the owned validator stack, now witnessed on one real domain, catches violations
  across repeated packs and blocks CI on them — and a second (minted) project inherits the same discipline.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | node validators witnessed on one real feature pack (green + deliberate red) | L0 | W0 | ✓ done | **DONE 2026-07-02** — validate:content 7 concepts PASS · engine:lint CLEAN · instances 14 PASS · red exit 1 |
| S-002 | v1 pattern-library triaged into v2 card layer + Evidence links | L1 | W1 | S-001 | IMPORT-MANIFEST rows; cards resolve |
| S-003 | node gates in CI over ≥2 packs; 2 defects cleared | L1 | W1 | S-001 | seeded violation blocks CI |
| S-004 | composability (edge-law) green on a real pack | L2 | W2 | **R3A done**, S-003 | endpoint-signature check passes |
| S-005 | ≥1 node handle promoted candidate→binding | L2 | W2 | S-003 | cav2 promotion recorded |
| S-006 | a minted 2nd repo validates its own nodes with the inherited substrate | L3 | W3 | S-004/S-005 | minted repo green |
| S-007 | forbidden edge unbuildable (C6) + drift baseline series (C7) | L3 | W3 | **formalism**, S-004 | unbuildable proof; drift trend |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TASK-POC | first real feature pack; node validators green + deliberate red | L0 | medium | W0 | findings A/UNIFORMITY | ready | **completed ✓ 2026-07-02** |
| TASK-CARDS | triage v1 pattern-library into v2 card layer + manifest rows | L1 | medium | W1 | findings E2; ARCHITECTURE-PATTERN-LIBRARY.md | ready | not-started |
| TASK-CI | node gates in CI + clean 2 defects | L1 | medium | W1 | findings G1/G2 | ready | not-started |
| TASK-EDGE | composability after R3A; dynamic DS-D8 edge-law refactor | L2 | high | W2 | findings C-B/W2 | ready-after-S-003 | not-started |
| TASK-PROMOTE | promote node handles candidate→binding | L2 | high | W2 | cav2 lifecycle | ready-after-L1 | not-started |
| TASK-MINT | mint a 2nd repo inheriting the substrate | L3 | high | W3 | mint skill; findings C-F | ready-after-L2 | not-started |
| TASK-UNCONSTRUCT | C6 typed-catalog unconstructibility | L3 | high | W3 | findings W1 | block-until-formalism | not-started |
| TASK-DRIFT | C7 drift baseline + trend | L3 | medium | W3 | findings W3 | ready-after-L2 | not-started |

## SWU Execution Handoff

Executable-now SWUs (W0/W1) are specified in full. Later-wave SWUs are named at manifest level and
expanded by `task-session` when their gate opens.

| SWU ID | Parent Task | Source Anchors | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-APE-001 | TASK-POC | `impl/test-derivation-engine/__fixtures__/financial-settlement/`, toy `research/spec-ontology-unification/toy/graph.md` (23 nodes), SPEC.md Concept Registry, TAXONOMY.md | none (G-001 resolved → financial-settlement) | `impl/spec/features/financial-settlement/` (SPEC + aspect docs) | promote the financial-settlement fixture into a v2 feature pack; its concepts typed to the 14 backend meta-type schemas | pack files exist; concepts resolve to `.schema.yml` types | `validate-content` parses it | subagent / local | **done ✓** (spec/features/financial-settlement/SPEC.md, 7 concepts) |
| SWU-APE-002 | TASK-POC | `impl/tools/validate-content.ts`, `instances.ts`, `impl/test-derivation-engine/src/cli.ts` (runLint) | SWU-APE-001 | none (run only) | `validate:content`, `instances:validate`, `engine:lint <path>` all exit 0 | green transcripts committed | the three commands | local | **done ✓** (all exit 0; aggregate `validate` + `tools:test` 20/20 also green) |
| SWU-APE-003 | TASK-POC | the pack from SWU-APE-001 | SWU-APE-002 | `spec/features/financial-settlement/__redcheck__/entity-missing-identity.md` | break one concept (drop its identity field); confirm `validate:content` exits non-zero on it | red transcript committed; error names the failing criterion | `validate:content` | local | **done ✓** (exit 1; `criterion 'identity': no field flagged`) |
| SWU-APE-004 | TASK-CI | `impl/governance/tags/code-tag-waivers.yaml` | none | that file | reset to `waivers: []` (removes the 4 stale v1 AEO entries) | diff shows empty waiver list | `tags:validate` no longer suppresses CT-004/006 | local | ready |
| SWU-APE-005 | TASK-CI | `validate-code-tags.ts:~749` (normalizeSpecPath), `validate-doc-links.ts:~228`, `compare-code-tag-drift.ts` default | none | those three files | retarget the `docs/features` anchors to `spec/features` | diff at 3 sites; anchor matches v2 layout | the affected validators on a v2 pack | local | ready |
| SWU-APE-006 | TASK-CARDS | v1 `architecture/pattern-library/concepts/backend/*.md` (14), `ARCHITECTURE-PATTERN-LIBRARY.md` | SWU-APE-001 | `impl/spec/meta-types/**/` (card companion) or a v2 `architecture/` tree; IMPORT-MANIFEST.md | import the 14 backend concept cards into v2 + add IMPORT-MANIFEST rows | cards present; manifest rows added | `validate-doc-links` resolves the new links | subagent / local | ready-after-001 |
| SWU-APE-007 | TASK-CARDS | v1 `ARCHITECTURE-PATTERN-LIBRARY.md` relationship cards (29) | SWU-APE-006 | v2 card layer, **labeled R3-dependent** | park the 29 relationship cards with an explicit `blocked-by: R3` note | cards present + R3 label | n/a (parked) | local | blocked (R3) |
| SWU-APE-008 | TASK-CI | CI config; SWU-APE-002 commands | SWU-APE-002, SWU-APE-004/005 | CI workflow file | wire `validate:content` + `instances:validate` + `engine:lint` as blocking CI on ≥2 packs | CI run blocks a seeded violation | the CI job | local | ready-after-002 |
| SWU-APE-009 | TASK-CARDS | SWU-APE-006 cards; CANDIDATES.md Tier 1a; `definitions/DEFINITIONS.md` | SWU-APE-006 | meta-type definition Evidence links | link each backend concept card as Evidence for its DS-D1.x promotion | Evidence rows reference the card + `.schema.yml` + TAXONOMY | definitions-governance review | manual (owner) | ready-after-006 |
| SWU-APE-EDGE-* | TASK-EDGE | RELATIONSHIPS.md (post-R3), `check-code-tag-composability.ts:27-109` | **R3** | edge validators | expand at execution time once R3 lands | — | — | subagent | blocked (R3) |
| SWU-APE-MINT-* | TASK-MINT | `mint` skill; SPEC.md APE.Substrate | S-004/S-005 | new repo (out of tree) | expand at execution time | — | — | manual (owner) | blocked (L2) |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target Date |
| --- | --- | --- | --- | --- | --- |
| B-001 | TASK-EDGE, SWU-APE-007/EDGE-* | edge verbs + endpoint signatures not final until **R3** reformulated RELATIONSHIPS.md | R3 / definitions-governance | land R3 (CANDIDATES.md Tier 1c) | — |
| B-002 | TASK-UNCONSTRUCT | C6 unconstructibility needs a typed catalog layer; **meta-type formalism still moving** | meta-type-formalization | settle the formalism variant | — |
| B-003 (=G-001) | TASK-POC / SWU-APE-001 | **RESOLVED 2026-07-02** (decision-gate) → reuse financial-settlement (DEC-DSV2-APE-L0-DOMAIN) | owner | task-session: promote the fixture into `impl/spec/features/financial-settlement/` | done |

## Dispatch Technique Trace

| Technique ID | Applied To | Validation Expectation | Status |
| --- | --- | --- | --- |
| sequence | SPEC → design → layering → work-pack → SWUs | each artifact consumes explicit prior inputs | pass |
| scu_swu_reduction | L0 POC → SWU-APE-001/002/003 | the SWUs are individually executable and meaningful | pass |
| recomposition_proof | L0→L1→L2→L3 → SPEC capabilities C-A..C-G | the layered units recompose into the full program | pass |
| validation_loop | every slice S-001..S-007 has a Validation column | every delivery slice carries evidence | pass |
| owner_boundary_check | APE handles → cav2 / definitions-governance / R3 | plan claims no execution or promotion authority — routes it | pass |
| residue_ledger | blockers B-001/002/003 + parked SWUs | deferred scope stays explicit, never silently pulled forward | pass |

No full dispatch JSON required: the route stays inside one capability's development package and
delegates via named owner routes rather than a cross-capability protected-context dispatch.

## Distill Validation

| Check | Result | Evidence Or Gap |
| --- | --- | --- |
| Smallest coherent unit / SWU boundary | pass | L0 POC = one feature pack + green/red; SWU-APE-001..003 executable. |
| Recomposition proof | pass | L0→L3 recomposes into SPEC capabilities C-A..C-G. |
| Hidden acceptance-critical gaps | pass | G-001 RESOLVED (DEC-DSV2-APE-L0-DOMAIN → reuse financial-settlement, 2026-07-02). |
| Deferred complexity | pass | edge plane / promotion / mint deferred with named blockers B-001/002. |
| Navigation to first executable unit | pass | first units = SWU-APE-004/005 (defect cleanup, no dependency) and SWU-APE-001 (promote financial-settlement, now ready). |

**Verdict: pass.** G-001 resolved (reuse financial-settlement); SWU-APE-001 is now ready alongside the
zero-dependency defect-cleanup SWUs (004/005).

## Gate Checks

1. `workPackGateStatus` pass for node-plane waves (W0/W1); block for edge-plane tasks until R3/formalism.
2. High complexity → `executionPackRef` set + baseline wave W0 present. ✓
3. Layer mappings consistent with `implementation-layering.md` deferred scope. ✓
4. Blocker B-003/G-001 **RESOLVED** (reuse financial-settlement) → SWU-APE-001 ready.
5. Dispatch technique trace present; no unused citations. ✓
6. Distill = **pass** (G-001 resolved) → SWU-APE-001 + 004/005 routable. ✓
7. Every non-exempt SWU (004/005/001/002/003) carries deps, write scope, done criteria, evidence, validation, owner. ✓
8. No runtime-goal SWU is missing Context Builder anchors. ✓
9. TASK-POC has multiple SWUs → SWU-APE-001 is the selected first (after G-001). ✓
10. Parallel SWUs (004, 005) have disjoint write scopes. ✓

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-07-02 | Initial work-pack created (invoke plan) | invoke / Claude |
| 2026-07-02 | DEC-DSV2-APE-L0-DOMAIN resolved (decision-gate) → reuse financial-settlement; B-003/G-001 closed; SWU-APE-001 ready; distill → pass | decision-gate / owner |
| 2026-07-02 | **TASK-POC executed (task-session): L0 POC DONE.** Authored `impl/spec/features/financial-settlement/SPEC.md` (7 backend meta-types); `validate:content` PASS (7 concepts, was 0/vacuous), `instances:validate` 14 PASS, `engine:lint` CLEAN; red-check exit 1 on a dropped identity flag; aggregate `validate` + `tools:test` 20/20 green (no regression). SWU-APE-001/002/003 done; slice S-001 done; `GAP-DSV2-APE-VACUOUS` resolved. | task-session |
