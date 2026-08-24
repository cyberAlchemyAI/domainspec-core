# Work Pack — Augmentor canvas workspace

- Work Pack id: `WP-AUG-CANVAS-001`
- Status: ready for owner admission, not approved for execution by this Refine run
- Design source: `stages/08-distill-repair.md`
- Scenario source: `stages/08-toy-scenario.md`
- Execution owner: one future `task-session` per SWU
- Product authority: candidate-local UI only

## Shared invariants

1. Do not edit ontology data, sources, views, residue, schemas, validation
   receipts, routing/runtime code, memory, authority, Git, or external systems.
2. Patch `visualization/template.html` first; regenerate
   `ontology-visualization.html` only through `scripts/build-visualization.mjs`.
3. Preserve the existing 22 nodes, 28 relations, 5 views, 7 residue items,
   beginner-explanation coverage, and `authority_effect:none` contract.
4. Presentation-only transitions preserve semantic state and graph transform.
5. Use the shared Playwright installation; do not add `package.json`, a package
   root, dependencies, or external requests.
6. Stop on a failing hard gate. Do not widen the active SWU to repair a
   different layer.

## SWU index

| SWU | Purpose | Dependencies | Primary write scope | State |
| --- | --- | --- | --- | --- |
| `SWU-CANVAS-001` | Readable card geometry and wrapping | none | template, visualization tests, generated HTML | ready-first |
| `SWU-CANVAS-002` | Static canvas shell and content recomposition | 001 | template, surface tests, generated HTML | ready-after-001 |
| `SWU-CANVAS-003` | Desktop panel reducer, toggles, and Focus canvas | 002 | template, browser tests, generated HTML | ready-after-002 |
| `SWU-CANVAS-004` | Measured region mode and non-overlay tray geometry | 003 | template, browser tests, generated HTML | ready-after-003 |
| `SWU-CANVAS-005` | SVG focus, Escape priority, and focus-return stack | 003 | template, browser tests, generated HTML | ready-after-003 |
| `SWU-CANVAS-006` | Mobile single-sheet dialog behavior | 004, 005 | template, browser tests, generated HTML | ready-after-004-005 |
| `SWU-CANVAS-007` | UX evidence harness and full closure run | 001–006 | UX browser test and new evidence run only | ready-after-006 |

## SWU-CANVAS-001 — Node-card legibility

- Source anchors: Stage 06 `Card geometry and type`; current template
  `nodeWidth`, `drawNodes`, `edgePath`, and `.node-*` rules.
- Allowed writes:
  `visualization/template.html`, `tests/visualization.test.mjs`,
  `tests/visualization.browser.mjs`, generated `ontology-visualization.html`.
- Implement: one shared geometry object; 216×88 default cards; measured
  CamelCase/word-boundary wrapping into at most two canonical-label lines;
  15px/18px label; separate 12px role/state metadata; full accessible name and
  `<title>`; shared centers, anchors, relation labels, and sequence markers.
- Acceptance: no truncation/ellipsis; every visible text/marker bound fits its
  card for every node; longest labels reviewed at 100% and 200% browser zoom;
  default/fit scale never renders labels below the readability floor.
- Stop: any ontology label/data edit or independently hard-coded legacy offsets.

## SWU-CANVAS-002 — Static canvas composition

- Source anchors: Stage 06 high-level/component views.
- Allowed writes: template, deterministic/browser surface tests, generated HTML.
- Recompose existing content into `CanvasWorkspace`, `TrustBoundaryBar`,
  `CanvasToolbar`, `GraphViewport`, `ExplanationDock`, `DetailsDock`, and
  `EvidenceTray`. Do not add visibility state yet; every region remains exposed.
- Acceptance: graph is the persistent center surface; all prior content has one
  new owner region; labels and accessible landmarks are unique; existing search,
  view, posture, sequence, explanations, inspector, gaps, and text view work.
- Stop: missing content, duplicated content, or trust boundary hidden in the tray.

## SWU-CANVAS-003 — Desktop panel state

- Source anchors: Stage 08 repaired deterministic focus/Escape contract.
- Allowed writes: template, browser tests, generated HTML.
- Implement separate semantic and presentation reducers; labelled
  `aria-expanded`/`aria-controls` toggles; independent desktop explanation,
  details, and evidence state; visibility snapshot for Focus canvas; explicit
  Clear selection; selecting while Details is closed does not reopen it.
- Acceptance: before/after snapshots prove view/query/posture/selection/kind/
  sequence/lens/graph transform equality for all presentation moves; stable
  non-modal desktop regions do not close on Escape; graph DOM identity persists.
- Stop: panel state persisted into ontology/session/memory or minimize clears data.

## SWU-CANVAS-004 — Measured layout and tray

- Source anchors: Stage 08 measured-region and tray contracts.
- Allowed writes: template, browser tests, generated HTML.
- Implement container measurement/normalization. A requested dock is admitted
  only while the graph remains at least 480px wide. The desktop tray consumes a
  row, never overlays controls/graph, and retains at least 320px graph height;
  otherwise it requests sheet presentation.
- Acceptance: automated widths immediately below/at/above each derived threshold;
  closed docks retain no invisible column; no focused control is hidden during
  resize; no outer horizontal overflow.
- Stop: viewport-number-only logic that violates measured floors.

## SWU-CANVAS-005 — Keyboard and focus model

- Source anchors: Stage 08 focus-stack and SVG-focus contracts.
- Allowed writes: template, browser tests, generated HTML.
- Implement explicit visible focus for lanes, nodes, relations, and every panel
  control; Enter/Space activation; `focusReturnStack`; Escape order mobile
  sheet → focus mode → no-op; exact trigger restoration; reduced motion.
- Acceptance: tab/activation coverage for every SVG interactive class; no focus
  target becomes hidden; Escape never clears selection; focus ring remains
  visible against every posture color at tested zooms.
- Stop: focus recovery based on DOM order alone or color-only focus indication.

## SWU-CANVAS-006 — Mobile sheet

- Source anchors: Stage 08 mobile dialog contract.
- Allowed writes: template, browser tests, generated HTML.
- Implement one reusable sheet host with one visible/accessibility-tree dialog,
  visible heading, `role=dialog`, `aria-modal=true`, labelled close, inert
  background, focus containment, atomic region switching, exact return focus,
  and locally scrolling body.
- Acceptance at 320×800: outer `scrollWidth === innerWidth`; one dialog; no
  behind-canvas hit/focus; switch Details→Explanations without semantic/transform
  loss; Escape closes and restores trigger; trust boundary remains perceivable.
- Stop: duplicated dock and sheet content exposed simultaneously.

## SWU-CANVAS-007 — Evidence closure

- Source anchors: Stage 06 acceptance evidence and Stage 07 additions.
- Allowed writes: `tests/ux-evidence.browser.mjs` and a new, timestamped
  `output/playwright/ux-validator/<run-id>/` bundle. Product repair is forbidden
  in this SWU; failures reroute to the owning SWU.
- Extend evidence capture for card bounds, semantic-state equality, desktop
  dock widths, derived threshold cases, tray graph height, SVG focus, mobile
  dialog count/inert/focus, exact return focus, and 100%/200% screenshots.
- Acceptance: deterministic/package/browser/UX gates pass against the exact
  generated HTML hash; console/page errors and external requests are empty;
  residue remains explicit.

## Exact validation commands

Run from `/home/vrondelli/projects/domainspec-core`:

```bash
node projects/augmentor/ontology/unified-agent/scripts/validate.mjs
node projects/augmentor/ontology/unified-agent/scripts/build-visualization.mjs
node projects/augmentor/ontology/unified-agent/scripts/build-visualization.mjs --check
node --test projects/augmentor/ontology/unified-agent/tests/unified-agent-ontology.test.mjs projects/augmentor/ontology/unified-agent/tests/visualization.test.mjs
node projects/augmentor/ontology/unified-agent/tests/visualization.browser.mjs "$(npm root -g)/playwright"
```

For `SWU-CANVAS-007`, first use `html-preview-server` to open the exact generated
HTML and record the concrete loopback URL. If the currently retained preview is
still byte-matched, the command is:

```bash
node projects/augmentor/ontology/unified-agent/tests/ux-evidence.browser.mjs "$(npm root -g)/playwright" "http://127.0.0.1:43693/ontology-visualization.html" "/home/vrondelli/projects/domainspec-core/projects/augmentor/ontology/unified-agent/ontology-visualization.html" "output/playwright/ux-validator/<new-run-id>"
```

Replace only `<new-run-id>` with the Task Session id. If port 43693 is not the
byte-matched server, use the concrete URL returned by `html-preview-server` and
record that substitution in the receipt before running the command.

## Task Session admission and closeout contract

Every SWU must begin with:

1. `git status --short -- projects/augmentor/ontology/unified-agent
   output/playwright/ux-validator` and a named-file inventory.
2. SHA-256 binding for the current template, generated HTML, tests in its write
   scope, Design, and repaired Distill artifact. Current untracked bytes are not
   silently attributed to the executing agent.
3. Declaration of the one admitted SWU, its allowed files, and its allowed delta
   classes: canonical template, scoped tests, generated mirror, or evidence.
4. Baseline execution of the validation commands relevant to that SWU.

Every SWU must close with a repository-local receipt under
`projects/augmentor/ontology/unified-agent/development/task-sessions/` containing:

- exact pre/post hashes and changed-file list;
- implementation claim limited to the active SWU;
- validation commands, exit statuses, and observed results;
- preserved invariants and any residue;
- next SWU disposition: `ready`, `blocked`, or `reroute`.

Successor policy is fail-closed: only a terminal passing receipt opens dependent
SWUs. No Task Session may commit, push, deploy, publish, or promote this package
without a separate explicit authorization.

