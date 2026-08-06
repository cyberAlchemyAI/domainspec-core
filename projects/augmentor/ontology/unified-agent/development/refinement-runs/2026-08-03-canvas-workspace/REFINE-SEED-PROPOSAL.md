# Refine Seed Proposal — Canvas-first ontology workspace

- **Run id:** `2026-08-03-canvas-workspace`
- **Target:** `projects/augmentor/ontology/unified-agent/ontology-visualization.html`
- **Preset:** standard
- **Research:** no-research
- **Current phase:** strategy awaiting operator confirmation

## Raw operator intent

Make node-card text easier to read and refine the visualization around the idea
that the whole interface is the canvas. Supporting elements should live inside
that canvas and be independently minimizable so the user can focus on the graph.

## Evidence baseline

- The supplied screenshot shows long single-line node labels colliding with the
  card boundary and adjacent labels.
- The generated graph currently uses `156 × 66` SVG node cards, a `13px`
  single-line label, a second role line, and a third posture line.
- The page currently presents the guide, filters, view controls, graph,
  inspector, gaps, and text index as a vertical document around one graph card.
- The previous UX evidence run passed its deterministic browser gates but kept
  graph vocabulary, beginner comprehension, and visual preference as residue.
- The ontology remains a candidate-local interpretive read model. A canvas
  redesign must not imply working routing, authority, or readiness.

## Proposed coherent unit

One canvas workspace with three independently collapsible support regions:

1. **Canvas toolbar** — view chooser, search, implementation-state filter, zoom
   controls, and a `Focus canvas` action.
2. **Explanation dock** — left-side panel for explanation mode and the four lane
   summaries; collapsed by default after the user's first explicit dismissal.
3. **Details dock** — right-side panel that opens when a lane, concept, or
   connection is selected and can be minimized without clearing selection.
4. **Evidence tray** — bottom drawer containing example flows, known gaps, the
   legend, and the text version of the graph.

The graph is no longer visually contained inside a conventional page card. It
is the workspace background and remains available while panels open above it.
Panel state is ephemeral UI state only; it does not create session, memory, or
ontology state.

## Card readability target

- Increase node cards toward `208–224px` wide and `82–92px` high.
- Use a minimum `15px` label with `1.2` line-height.
- Wrap canonical CamelCase labels into at most two visible lines instead of
  truncating them.
- Present role and implementation state as separate, quieter badges with at
  least `12px` text.
- Preserve the full canonical label in the accessible name and SVG `<title>`.
- Recalculate lane layout from measured card dimensions rather than fixed
  legacy coordinates.

## Interaction requirements

- Every panel toggle is a real button using `aria-expanded` and `aria-controls`.
- `Focus canvas` minimizes every support panel without changing filters,
  selection, or explanation mode.
- Reopening Details restores the current selection.
- Escape closes the topmost temporary panel and returns focus to its trigger.
- Desktop permits the explanation and details docks together; mobile uses one
  bottom sheet at a time so panels cannot obscure one another.
- Keyboard, reduced-motion, 320px reflow, and synchronized text-view behavior
  remain acceptance gates.

## Write scope after confirmation

This Refine run writes only its run folder. The later implementation route may
propose changes to:

- `visualization/template.html`
- `scripts/build-visualization.mjs`
- `tests/visualization.test.mjs`
- `tests/visualization.browser.mjs`
- `tests/ux-evidence.browser.mjs`
- generated `ontology-visualization.html`
- the UX evidence output for the new browser run

No ontology nodes, relations, views, source records, authority boundaries,
validation receipt, Git state, or external system may be changed by Refine.

## Done criteria for the Refine run

- The ten-stage route is validated before execution.
- Define and Design distinguish canvas, panels, drawers, and ontology state.
- The design includes desktop and mobile state transitions.
- A toy scenario proves that a user can focus the canvas, inspect one node,
  reopen details, and recover explanation context without losing state.
- The final plan is implementation-ready but remains non-executed.
- Human comprehension and aesthetic preference remain named residue.

## Planned stage configuration

Standard ten-stage Refine loop with `baseline_sequence`,
`xray_for_hidden_structure`, `route_menu_for_ambiguity`, and
`toy_game_for_low_cost_falsification`. One read-only UX evidence reviewer is
recommended for the design-review stage and requires operator permission.
