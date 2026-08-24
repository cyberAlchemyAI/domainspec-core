# Define Context

## Objective

Turn the nearest blocked Anime.js AKV query repair into a durable Define, Design, and Plan package with exact candidate paths, validation commands, atomic SWUs, Task Session closeout contracts, and a pre-session readiness audit.

## Obligation matrix

| ID | Obligation | Selected evidence | Status |
| --- | --- | --- | --- |
| O-01 | Preserve the closed six-code abstention vocabulary. | Refine query matrix `closed_abstention_vocabulary` | covered |
| O-02 | Make QRY-003 tie handling emit `ABSTAIN_AMBIGUOUS_INTENT`. | Refine query matrix `selected_repair` and `terminal_paths[tie]` | covered |
| O-03 | Specify total primary-code precedence and subordinate gaps. | Refine query matrix `primary_precedence` and multiple-failure path | covered |
| O-04 | Make success and abstention receipt states mutually exclusive. | Refine query matrix `receipt_invariants` | covered |
| O-05 | Preserve historical receipts through an algorithm-version migration. | Refine query matrix `receipt_invariants.migration` | covered |
| O-06 | Bind eight terminal fixtures without claiming execution. | Refine query matrix `planned_fixtures` | covered |
| O-07 | Repair exact paths, commands, admission, and closeout gaps. | Blocked Task Session `RESULT.md` and `CLOSEOUT-PREFLIGHT.json` | covered |
| O-08 | Keep relation repair and ontology admission outside this slice. | Refine Stage 09 dependencies and `RESULT.md` claim ceiling | covered |

## Selected source selectors

1. `projects/animejs/development/refinement-runs/20260803T175423Z-animejs-blocking-defects/stages/08-query-contract-matrix.json`
   - selectors: `closed_abstention_vocabulary`, `primary_precedence`, `receipt_invariants`, `terminal_paths`, `planned_fixtures`
2. `projects/animejs/development/refinement-runs/20260803T175423Z-animejs-blocking-defects/stages/09-invoke-plan.md`
   - selectors: `SWU-AKV-NV-001`, first implementation slice, dependencies, rollback
3. `projects/animejs/development/refinement-runs/20260803T175423Z-animejs-blocking-defects/task-sessions/20260803T191537Z-SWU-AKV-NV-001/RESULT.md`
   - selectors: blocking evidence, next route, mutation statement
4. `projects/animejs/development/refinement-runs/20260803T175423Z-animejs-blocking-defects/task-sessions/20260803T191537Z-SWU-AKV-NV-001/CLOSEOUT-PREFLIGHT.json`
   - selectors: blockers, required delta classes, absent closeout fields

## Excluded context

- The Anime.js documentation corpus is not reloaded: this contract repair is already closed by the prior evidence chain.
- Relation witness details are excluded from implementation scope and retained only as successor context.
- No existing ontology model is copied because no Anime.js ontology has been admitted or created.

## Context Builder result

- Mode: standard strict
- Files selected: 4
- Obligations covered: 8/8
- Strict coverage: pass for Define/Design/Plan authoring
- Runtime handoff: not emitted; Task Session must create a fresh session-local pack after an eligible SWU is explicitly selected
