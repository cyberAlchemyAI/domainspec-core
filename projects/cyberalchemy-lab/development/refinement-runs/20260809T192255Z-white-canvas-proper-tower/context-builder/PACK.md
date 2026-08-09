# Runtime context pack — white canvas proper tower

Session evidence only. This pack is not a product specification, authority record, or implementation permission.

## Identity

- Task: `REFINE-WHITE-CANVAS-PROPER-TOWER`
- Run: `20260809T192255Z-white-canvas-proper-tower`
- Source request: remove the background, create a white canvas, and have a proper tower.
- Mode: `standard --strict --emit both --handoff runtime`.

## Obligation matrix

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Replace the dark photographic primary background with a white/warm-white canvas. | current page `:root`, `body`, `#lab-canvas`, `.scene-stack`, `.veil` | covered |
| O2 | Make one proper vertical tower the primary navigation object. | current `.core`/`.source-orbit` composition; manifest `towers[0].scenes` | covered |
| O3 | Map exactly three evidence floors without collapsing them into Tower System layers. | `EVIDENCE_SCENE_IDS`, `SYSTEM_LAYER_IDS`, prior Refine result, `SYSTEM-VIEW.md` layer stack | covered |
| O4 | Preserve state, source refs, claim ceiling, and explicit unavailable/refusal behavior. | manifest validation and browser assertions | covered |
| O5 | Preserve native keyboard/focus, mobile, and reduced-motion behavior. | current HTML controls and Playwright test | covered |
| O6 | Produce a non-executed plan only; no product, external, authority, or promotion effect. | operator strategy, foundation findings, Refine contract | covered |

## Selected evidence

1. `projects/ide-extension/public/demo/research-tower.html`
   - Selectors: CSS roots `:root`, `body`, `#lab-canvas`, `.scene-stack`, `.core`, `.source-orbit`, `.scene-nav`, `.tower-scene`; DOM root and navigation; `renderSceneControls`.
   - Covers: O1, O2, O5.
   - Evidence: the current UI is dark, uses three rotating photographic scenes and a veil, centers a circular core/source orbit, and already uses native scene/system buttons.
2. `projects/ide-extension/src/research-tower/l0-witness.mjs`
   - Selectors: `EVIDENCE_SCENE_IDS`, `SYSTEM_LAYER_IDS`, `validateTowerSceneManifest`, `buildTowerSceneManifest`.
   - Covers: O2, O3, O4.
   - Evidence: exactly one synthetic tower, three evidence scenes, and five separately namespaced system descriptors with unavailable reasons.
3. `projects/ide-extension/tests/research-tower-explorer.test.mjs`
   - Selectors: manifest negative test; server page/API contract.
   - Covers: O3, O4.
4. `projects/ide-extension/tests/e2e/research-tower-explorer.spec.mjs`
   - Selectors: scene selection/refusal/source inspection test; reduced-motion test.
   - Covers: O4, O5.
5. `research/tower-system-taxonomy/SYSTEM-VIEW.md`
   - Selectors: layer stack, core flow, reuse map, evidence tiers.
   - Covers: O3, O6.
6. `projects/cyberalchemy-lab/development/refinement-runs/20260809T182018Z-tower-scene-canvas/RESULT.md`
   - Selectors: Decision, Design that survived review, Complete residue/blockers.
   - Covers: O3, O4, O6.
7. `projects/cyberalchemy-lab/development/research/2026-08-07-foundation/findings.md`
   - Selectors: Crosswalk, Current versus required IDE interface, Risks and open residue.
   - Covers: O3, O4, O6.

## Architecture guidance

- Use a DOM/CSS tower shell with one vertical spine and three native floor buttons.
- Keep source inspection and evidence details as an anchored secondary surface.
- Keep Tower System architecture outside the tower's selectable floor stack.
- Treat background photography, robots, and source orbit as removable decoration, not semantic dependencies.

## Constraints and non-goals

- No new scene-manifest meaning.
- No real tower selection.
- No pan/zoom requirement, game engine, dependency, or image generation.
- No product file mutation during Refine.
- No authority, promotion, publication, deployment, release, or production claim.

## Gaps and resolutions

- Gap: “proper tower” has no existing accepted geometry. Resolution: the approved visual reviewer proposes and attacks one geometry; the semantic reviewer independently constrains it.
- Gap: usability is not proven. Resolution: the plan specifies browser acceptance; Refine does not claim usability.

## Strict coverage

All six obligations are covered. No contradiction blocks the planning handoff.
