---
task: SWU-RDL-006
mode: lean-strict
status: block
createdAt: 2026-07-14T22:46:09Z
session_evidence: true
source_count: 7
obligation_coverage: 100%
---

# Context Pack: SWU-RDL-006 Focused IDE Route And Canvas Witness

This is Task Session evidence, not a reusable source-of-truth document.

## Objective

Give the generated Roadmap Lab a focused IDE route/mode that reuses the existing
Canvas publication/current/content/event path, hides unrelated IDE context, and
proves a real publish/display/event/poll round trip.

## Obligation Matrix

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| I1 | Reuse the existing Canvas kernel and parent `postMessage` event adapter; do not duplicate a standalone interaction kernel. | `TASK-RDL-GUIDED-SURFACE.md#SWU-RDL-006`, `l0.html:1390-1432` | covered |
| I2 | Provide a focused `/demo/roadmap-lab` or equivalent stable route/mode that hides unrelated Craft/operations context. | task rules and UX dedicated layout | covered |
| I3 | Publish/display the current generated `roadmap.html`, then submit restatement/source/proposal events and poll them back. | SWU-RDL-005 evidence and existing `/api/canvas/*` contracts | covered |
| I4 | Preserve refresh/reconnect/error boundary and existing Canvas regressions. | `l0.html`, `server.mjs`, package scripts/tests | covered |
| I5 | Stop before mutation when current dirty IDE files overlap the required route/kernel changes. | work-pack dirty-scope gate and live `git diff` | covered |

## Selected Sources

| Source selector | Why included | Obligations |
| --- | --- | --- |
| `WORK-PACK.md` SWU-RDL-006 row and blockers | exact status/write scope/gate | I1-I5 |
| `TASK-RDL-GUIDED-SURFACE.md#SWU-RDL-006` | rules, done criteria, validation | I1-I5 |
| `ARCHITECTURE-BUNDLE.md#RDL-O02`, `#View 6` | Canvas interface and route boundary | I1-I4 |
| `UX-PLAN.md#Dedicated Layout`, `#Interaction States` | focused mode and hidden-context requirement | I2-I4 |
| `l0.html:1390-1432` plus current dirty hunks | exact event adapter and overlapping UI surface | I1-I5 |
| `server.mjs` current dirty hunks | route/API overlap and current in-flight operations work | I2-I5 |
| `SWU-RDL-005/TASK-SESSION-RESULT.md` | generated page is ready; parent route remains | I3 |

Selected excerpt budget: 122 lines across 7 files.

## Gate Result

Strict coverage for understanding the task passes, but the dirty-scope gate
blocks mutation:

- `l0.html` has a 230-line uncommitted change adding Craft Frontier UI, layout
  changes, startup refresh, and action wiring in the exact page that SWU-RDL-006
  would need to turn into a focused Roadmap Lab mode.
- `server.mjs` has a 257-line uncommitted change adding Craft frontier reading,
  Canvas blob store integration, and Operations v1 routes in the same server
  dispatch/runtime initialization surface where the Roadmap Lab route and
  publication witness would be added.
- `package.json`, `package-lock.json`, and many IDE tests are dirty for
  Operations v1 and parse5-related work; SWU-RDL-006 validation would need to
  compose with those scripts/tests.

This is not a missing-file blocker; it is an ownership/overlap blocker. Mutating
through it would risk corrupting unrelated in-flight IDE work or silently
changing the intended Operations/Craft route.

## Decision Builder

Decision Gate is required before mutation. The options are recorded in
`DECISION-GATE.md`.

## Context Builder Result

- Mode: lean, strict.
- Files selected: 7.
- Obligations: 5/5 covered.
- Noise ratio: low.
- Handoff pack: none; mutation blocked.
- Strict coverage: pass for context; block for dirty ownership gate.
- Blockers: 1.
