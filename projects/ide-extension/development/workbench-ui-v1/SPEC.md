---
id: ide-extension-workbench-ui-v1-spec
project: ide-extension
title: "Workbench UI V1"
status: planned
node_type: spec
updatedAt: 2026-07-17
invoke_mode: define
---

# Workbench UI V1 Spec

## Definition

Workbench UI V1 is the first product-oriented interface for the existing local
workbench. It makes agent tasks the primary path, keeps dry runs explicit, and
lets a user follow one request from preparation through admitted execution
evidence without understanding envelope internals.

## User Need

The current page proves many mechanisms, but exposes them as separate systems:
approval desk, bridge demo, Craft frontier, evidence rail, and Canvas. The mode
switch between a dry run and an agent task is implicit in whether Skill is
empty. A user needs one obvious path and contextual detail only when needed.

## Included

- Canvas-first responsive product shell.
- Explicit `Agent task` and `Dry run` preparation modes.
- Required skill input for agent tasks and no skill input for dry runs.
- Unified run timeline for prepared, approved, available, claimed, result, and receipt states.
- Contextual actions derived from current state.
- Craft frontier as a task-source view, not a competing product surface.
- Evidence drawer for receipts, grants, context refs, identifiers, and storage diagnostics.
- Desktop and mobile Playwright evidence plus a real human usefulness gate.

## Excluded

- Background agent wake-up or unattended worker scheduling.
- Multi-request leases or remote queue infrastructure.
- OpenRouter execution and provider-key handling.
- Browser extension control or VSCodium embedding.
- Hostile HTML containment.
- Region-level collaborative editing.
- Changes to existing kernel authority or receipt ownership.

## Success Criteria

1. A first-time user can create an agent task without accidentally creating a dry run.
2. The next available action is clear at every request state.
3. Task details remain hidden from a poller until claim.
4. Claimed is visibly different from completed.
5. The admitted result and Canvas output are reachable from the same run.
6. Existing L0, bridge, Canvas, and Operations V1 contracts remain compatible.
7. A human judges the V1 flow more useful than the current proof-oriented page.

## Decisions

| ID | Decision | Rationale |
| --- | --- | --- |
| WUI-D1 | Agent task is the default preparation mode. | It is the intended daily workflow; dry run is diagnostic. |
| WUI-D2 | Preserve the current local server and single-page implementation. | V1 needs product coherence, not a framework migration. |
| WUI-D3 | Canvas is the primary workspace; run state is the control rail. | The artifact is the user value, while governance remains inspectable. |
| WUI-D4 | Evidence is contextual and always reachable. | Receipts matter, but should not dominate every moment. |
| WUI-D5 | Same-session execution remains command-triggered. | V1 does not claim browser-to-agent wake-up. |

## Source Evidence

- `projects/ide-extension/public/demo/l0.html`
- `projects/ide-extension/SPEC.md`
- `projects/ide-extension/ARCHITECTURE.md`
- `projects/ide-extension/development/operations-v1-plan/WORK-PACK.md`
- `projects/ide-extension/development/workbench-bridge-demo-v01/evidence/DEMO-EVIDENCE.md`
- `projects/ide-extension/development/session-content-workbench-plan/work-pack/evidence/SWU-SCW-008-REPORT.md`
- `arcanum/arcana/workbench-poll/SKILL.md`

## Define Technique Trace

| Technique | Application |
| --- | --- |
| `sequence` | One visible request lifecycle. |
| `owner_boundary_check` | UI suggests actions; kernel admits state and receipts. |
| `artifact_contract_bridge` | Runs link to Canvas revisions and execution evidence. |
| `concrete_path_evidence` | Every claim cites current implementation or retained witness. |

## Distill Sanity Check

Pass. The coherent unit is one understandable agent-task journey. Provider,
browser-control, IDE wrapper, and background-worker work remain separate.
