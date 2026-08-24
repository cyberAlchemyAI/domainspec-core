# Context Pack — Augmentor canvas chain preflight

- Task: `WP-AUG-CANVAS-001 / SWU-CANVAS-001`
- Chain: `20260803T175006Z-augmentor-canvas`
- Mode: `standard-strict`
- Handoff: chain preflight evidence, not a runtime implementation handoff
- Status: `BLOCK`
- Product mutation: none

## Objective

Bind the seven-SWU Augmentor canvas frontier and decide whether the first fresh
Task Session can be admitted without weakening Task Session closeout or routed-
mutation controls.

## Obligation matrix

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Bind one exact work pack and live identity. | E1 | covered |
| O2 | Capture a finite, ordered, dependency-aware frontier. | E1, E2 | covered |
| O3 | Prove every unit has bounded write scope and acceptance-critical validation. | E1 | covered |
| O4 | Prove the first selector is unique and dependency-ready. | E1, E2 | covered |
| O5 | Bind a complete Task Session closeout contract: exact sync inventory, baselines, admitted closeout delta classes, owner validation, expected Invoke owner receipt, and unique successor. | E1, E5 | block |
| O6 | Bind a schema-valid routed-mutation request to an Invoke-owned material package, material receipt, and producer receipt schema. | E1, E3, E5 | block |
| O7 | Preserve candidate-local and authority-none boundaries. | E1, E2, E3 | covered |
| O8 | Set the maximum session count no higher than the captured frontier. | E4 | covered: 7 |

## Included context

| ID | Path and selector | Why included | Obligations |
| --- | --- | --- | --- |
| E1 | `projects/augmentor/ontology/unified-agent/development/refinement-runs/2026-08-03-canvas-workspace/WORK-PACK.md`: Shared invariants, SWU index, SWU-001, validation, closeout | Owns the exact candidate frontier and declared execution contract. | O1–O7 |
| E2 | `.../IMPLEMENTATION-LAYERING.md`: layers and promotion rules | Confirms order, dependencies, and evidence ceilings. | O2, O4, O7 |
| E3 | `.../stages/08-distill-repair.md`: repaired contracts | Controls geometry, focus, responsive, dialog, and non-authority behavior. | O6, O7 |
| E4 | `.agents/skills/task-session-until-blocker/SKILL.md`: Preconditions and Phases 1–2 | Requires a finite frontier, closeout contract, unique first selector, and budget ≤ frontier. | O1–O8 |
| E5 | `.agents/skills/task-session/SKILL.md`: Steps 4/4A/5A/8 | Requires pre-mutation closeout inputs and a material-bound mutation-admission receipt. | O5, O6 |
| E6 | `.agents/skills/continuation-router/SKILL.md`: route catalog and one-hop boundary | Owns the probable next owner route without owner mutation. | O5, O6 |
| E7 | `visualization/template.html`: `.node-*`, `nodeWidth`, `drawNodes`, `edgePath` | Live material target for the first SWU. | O3, O6 |
| E8 | `tests/visualization.test.mjs`, `tests/visualization.browser.mjs`, `scripts/build-visualization.mjs` | Live validation and generated-output boundary. | O3, O6 |

## Bound frontier

1. `SWU-CANVAS-001`
2. `SWU-CANVAS-002` after 001
3. `SWU-CANVAS-003` after 002
4. `SWU-CANVAS-004` after 003
5. `SWU-CANVAS-005` after 003
6. `SWU-CANVAS-006` after 004 and 005
7. `SWU-CANVAS-007` after 001–006

The declared order is deterministic even where 004 and 005 are both ready
after 003: the captured frontier fixes 004 before 005. The unique initial
selector is `SWU-CANVAS-001`. Session budget is 7.

## Live baseline identities

| Artifact | SHA-256 |
| --- | --- |
| Work Pack | `0ffb516e8070fa53f3df2af0c0a8c1154b4b9d1b924a2138d14179eb74dee07d` |
| Implementation Layering | `7d235195f4b20b46110791daa5652f645aea73a6d836cc7b161d59def41a9d71` |
| Stage 06 Design | `2f9ef1d9b864b6ab6fbec5aa4412439fcdfeb42974e4164a85edc3ff3e05f25e` |
| Stage 08 repair | `0a1addea12da33fb47cbfcdc6797011bf02a40ad5d7368ac164b3c44f61b5f5e` |
| Template | `8b7018cda724136a583b1dd790143c9e0833dd98738adb82bdabd15fb16ddf82` |
| Generated HTML | `79397e106f4f5d5894262c63b6e96d704c7bd025fa7331f1b97750b975256b9f` |
| Deterministic visualization test | `7a0bc64bfd81c59afcd423105fc02171483f0027efa11099306ca3135832eda4` |
| Browser visualization test | `14caa9888f4e562fed310a59c3c676ee0b0277cfafed1136d6314cfb2806554c` |

The target package contains pre-existing modified and untracked bytes. These
hashes bind the live baseline but do not attribute those bytes to this chain.

## Blocking gaps

### B1 — closeout synchronization contract

The Work Pack describes what a Task Session report should contain, but it does
not declare:

- the exact planning/status artifacts Invoke Refresh may synchronize;
- their bound pre-session baselines;
- closeout delta classes from the allowed vocabulary;
- owner validation commands after synchronization;
- the expected separate Invoke owner receipt schema/path.

Because completing SWU-001 would change task/work-pack status and successor
readiness, a receipt-backed `NO_OP` cannot be claimed in advance.

### B2 — routed material admission

`SWU-CANVAS-001` has material writes. No Invoke-owned material package,
material receipt, or producer receipt schema exists for this selector. A routed
mutation request that omits these artifacts cannot satisfy Task Session
mutation-admission schema 1.2.0.

## Strict coverage verdict

Six obligations are covered; O5 and O6 are blocked by exact absent owner
artifacts. Strict coverage is `BLOCK`. The chain may persist evidence and a
Continuation Router receipt, but it must not start Task Session or change
product files.

## Smallest unblock action

Run `invoke:refresh:proposal-only` for `WP-AUG-CANVAS-001 / SWU-CANVAS-001` to
author the exact material package/receipt/schema binding and complete closeout-
sync inventory. If that owner finds no consequential design choice, a later
explicitly admitted apply route can synchronize the plan; then rerun this spell
from a fresh baseline.

