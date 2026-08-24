# Spatial prototype critic receipt

- Dispatch: `2026-08-09-cyberalchemy-lab-tower-scene-review`
- Role: `spatial-prototype-critic`
- Agent: `/root/spatial_prototype_critic`
- Capability: `interrogation` / `refine-review`
- Mutation: none; no browser, server, test, or network action.

## Current source-observed behavior

- Native source buttons: `[data-list="sources"] [data-source-id]`; relation select: `[data-field="relation-filter"]`; projection button: `#constellation-core`; motion control: `[data-action="toggle-lab-motion"]`.
- Source selection and relation filtering update the evidence dock; the motion control toggles `.motion-paused` and `aria-pressed`.
- At `max-width:800px`, `[data-panel="live-lab"]` and `[data-robot-role]` are hidden while source/relation/detail controls remain.
- `prefers-reduced-motion` disables animations and keeps one background scene visible.
- The loader is flat, locked synthetic L0; it has no manifest, scene projection, or selectable level identity.

## Required plan repairs

### P0 — semantic safety and operability

1. Introduce a source-bound manifest before scenes. Each scene needs `tower_id`, collision-free `level_id`, `semantic_axis`, `evidence_state`, `claim_ceiling`, `source_refs`, and `unavailable_reason`.
2. Use namespaced labels: `evidence-l0-corpus`, `evidence-l1-residue`, `evidence-l2-closure` versus `system-l1-substrate`, `system-l2-construction`, `system-l3-application`, `system-lphi-policy`, `system-l4-adjudication`. Bare `L1` is forbidden.
3. Keep tower and level selection native controls, with `aria-pressed`/`aria-current`, one deterministic selected state, and a textual DOM-order alternate list.
4. Use stable overview + explicit `[data-action="focus-tower"]` and `[data-action="reset-camera"]`; no drag-only navigation.
5. Reduced motion must preserve semantic selection/status while removing scene/camera transitions. Decorative layers must be `aria-hidden`; current `.live-lab` has a decorative label but is exposed to assistive technology.

### P1 — responsive and interaction quality

- 44 CSS-pixel touch targets and spacing for scene selection.
- A persistent semantic level strip/list on mobile; no overlap/horizontal-scroll failure.
- URL state only after contract creation: `?tower=tower:toy&scene=evidence-l0-corpus`; invalid state resolves to overview plus `[data-panel="scene-unavailable"]`.
- One restrained `[data-panel="tower-scene-status"][aria-live="polite"]` region for selection/refusal changes only.

### P2 — visual coherence

The open canvas supplies orientation and atmosphere, not the sole information layout. Generated libraries and robots remain decor; they must not become evidence, personas, or workflow claims.

## Browser-testable acceptance criteria

1. `[data-list="towers"] [data-tower-id="tower:toy"]` selects one tower with one selected state.
2. Every declared evidence scene has a `[data-level-id]` control; Enter/Space activate it and focus remains visible.
3. Evidence selection updates `[data-panel="tower-scene-status"]` with matching state, source ref, and ceiling.
4. Missing manifest data/unavailable system layers render `[data-panel="scene-unavailable"]`, never a simulated runtime.
5. Focus/reset controls restore orientation without drag input.
6. At mobile width, semantic controls remain visible, tabbable, touch-sized, and horizontally contained.
7. Reduced motion keeps semantic state readable and eliminates/pauses decorative movement.
8. Browser acceptance checks real computed behavior and page errors, not static HTML alone.

## Stop conditions / reroute

Stop if a scene lacks locked evidence, state, and ceiling; if labels collide; if the design implies real corpus/graph/personas/MOGT/adjudication/authority/promotion; if a new dependency or external research is proposed; or if browser acceptance fails. The engine decision remains deferred until a DOM/CSS implementation proves inadequate.
