# Strict Refresh Context

## Target

Update the active Co-Op Engine L0 plan with one unselected HTML-prototype SWU
without invalidating the already selected `SWU-COOP-001` goal handoff.

## Obligation Matrix

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| R-01 | direct-user approval and exact scope | `REFRESH-INTENT.md` | covered |
| R-02 | current selected SWU remains singular | `SWU-MANIFEST.json`; `WORK-PACK.md` | covered |
| R-03 | page and presentation remain one artifact | `SPEC.md#what-this-product-owns`; `UX-PLAN.md#shared-content-spine` | covered |
| R-04 | all fourteen projects use bounded labels and ceilings | `SPEC.md#project-catalog-boundary`; research `findings.md#project-truth-product-and-whisper-intake-cards` | covered |
| R-05 | prototype is separate from final copy and product behavior | `DESIGN-ACCEPTANCE-REVIEW.md`; `UX-PLAN.md` | covered |
| R-06 | new SWU is atomic and recomposes into L1 | `REFRESH-DISTILL-VALIDATION.md` | covered |
| R-07 | browser acceptance is black-box and evidence-bounded | `UX-EVIDENCE-ACCEPTANCE.md`; installed Playwright CLI contract | covered |
| R-08 | stale strict pack for selected SWU is repaired | existing context-pack index and exact changed-source digests | covered |
| R-09 | apply mutation is material-package gated | Invoke `refresh.md` and material-package schemas | covered |
| R-10 | public/private and lifecycle owners stay separated | `SPEC.md#define-owner-assignment`; Invoke refresh contract | covered |

Strict coverage: `pass` — 10/10 obligations covered, zero assumptions, zero
unresolved refresh-authoring blockers.

## Selected Sources

| Source | Selectors | Obligations |
| --- | --- | --- |
| `REFRESH-INTENT.md` | exact scope, exclusions, approval | R-01, R-09 |
| `../../WORK-PACK.md` | selected SWU, deferred page scope | R-02, R-08 |
| `../../SPEC.md` | one-artifact contract, catalog, copy boundaries | R-03, R-04, R-10 |
| `../../UX-PLAN.md` | shared spine, meta-narration rule, audit contract | R-03, R-05, R-07 |
| `../../../2026-07-25-co-op-engine-portfolio-research/findings.md` | fourteen accepted project cards and claim ceilings | R-04, R-05 |
| `../../DESIGN-ACCEPTANCE-REVIEW.md` | evidence ceiling and prohibited shortcuts | R-05, R-07 |
| `../../UX-EVIDENCE-ACCEPTANCE.md` | browser hard gates versus human residue | R-07 |
| `../../session-evidence/20260726T044915Z-swu-coop-001/CONTEXT-PACK.index.json` | selected-source bindings to repair | R-08 |

## Authority and Conflict Resolution

1. The new direct user signal may change planning scope but cannot establish
   implementation evidence.
2. Approved `SPEC.md` and Design artifacts control product truth and claim
   boundaries.
3. Accepted research supplies prototype copy substrate, not public-ready copy.
4. The active work-pack and SWU manifest control selection; exactly one SWU
   remains selected.
5. Persisted context packs are execution evidence and must be re-bound when
   selected source bytes change.

## Excluded Context

- individual project roots: accepted research already closes the prototype
  card substrate;
- public Arcanum sources beyond named runtime contracts: no reusable public
  artifact is being changed;
- implementation and hosting folders: target work is not executed;
- full prior transcript: obligation-linked artifacts are sufficient.
