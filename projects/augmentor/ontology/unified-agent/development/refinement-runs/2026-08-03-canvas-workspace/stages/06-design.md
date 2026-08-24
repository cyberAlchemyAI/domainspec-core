# Stage 06 — Canvas workspace design

- Capability: `invoke`
- Phase: `design`
- Status: `authored-complete`
- Selected model: docked support panels on desktop, one bottom sheet on mobile
- Authority effect: none
- Product implementation: not started

## 1. Context view

The generated HTML is currently a long, vertically composed explainer with a
graph card and adjacent inspector. The target is one bounded workspace whose
persistent graph is the spatial foundation. Controls, explanations, details,
and evidence become named in-canvas surfaces rather than independent document
sections.

The shell operates on already-generated content. It neither changes the
ontology bundle nor introduces session, memory, routing, reasoning, or work
execution behavior.

## 2. High-level view

```text
+ CanvasWorkspace ---------------------------------------------------------+
| TrustBoundaryBar                                           panel toggles |
| + CanvasToolbar -------------------------------------------------------+ |
| | view | search | state filter | zoom -/reset/+ | Focus canvas         | |
| +---------------------------------------------------------------------+ |
| + ExplanationDock +---- GraphViewport (persistent) ----+ DetailsDock + |
| | lens + lanes       |                                  | selection    | |
| | collapsible        | lanes · nodes · relations        | collapsible  | |
| +--------------------+----------------------------------+--------------+ |
| + EvidenceTray: flows | legend | gaps | text view --------------------+ |
| | collapsible; does not imply hidden gaps are resolved                 | |
| +---------------------------------------------------------------------+ |
+------------------------------------------------------------------------+
```

The graph is persistent in the DOM and owns the remaining center area. Opening
a dock changes the available viewport; it does not remount, reset, or replace
the graph. On mobile, the graph fills the workspace and support regions are
rendered through a single bottom-sheet host.

## 3. Component-state map

| Component | Owns | Reads | Must not own |
| --- | --- | --- | --- |
| `CanvasWorkspaceShell` | region placement, breakpoint policy, presentation reducer, focus return | presentation state, viewport class | semantic selection, ontology data, persistence |
| `TrustBoundaryBar` | always-visible candidate/design-only message | visualization contract | authority or approval |
| `CanvasToolbar` | presentation triggers plus existing semantic control placement | both state namespaces | route execution, query persistence |
| `GraphViewport` | contained graph pan/scroll/zoom transform | generated graph, semantic state | dock visibility, browser zoom |
| `GraphNodeCard` | card geometry and accessible naming | one existing node and explanation record | implementation truth beyond existing posture field |
| `ExplanationDock` | explanation/lane content presentation | explanation lens, selected lane if any | semantic lens ownership or memory |
| `DetailsDock` | inspector content presentation | selected and selectedKind | clearing selection on minimize |
| `EvidenceTray` | flows, legend, gaps, and synchronized text content presentation | sequence, visible graph, residue | audit authority, gap resolution |
| `MobileSheetHost` | exactly one active support surface, backdrop, focus containment | activeMobileSheet | duplicated content or multiple simultaneous sheets |

### Semantic state (existing)

```js
{
  view, query, posture,
  selected, selectedKind,
  sequence, explanationLens
}
```

### Presentation state (new, ephemeral)

```js
{
  explanationOpen: true,
  detailsOpen: true,
  evidenceOpen: false,
  activeMobileSheet: null, // null | "explanation" | "details" | "evidence"
  canvasFocus: false,
  returnFocusId: null
}
```

The two objects may be stored beside one another in the first implementation,
but transition functions and tests treat them as separate namespaces.

## 4. Low-level view

### Workspace sizing

- `CanvasWorkspace` has a minimum usable block size of `calc(100dvh - topbar)`
  and may grow only when fallback content requires it.
- Desktop grid columns are
  `minmax(0, explanationWidth) minmax(480px, 1fr) minmax(0, detailsWidth)`.
- Default dock widths: explanation `clamp(240px, 20vw, 320px)`; details
  `clamp(280px, 24vw, 380px)`.
- Closed docks occupy only their labelled edge trigger, not an invisible column.
- The tray opens to `min(42dvh, 420px)` and its body scrolls internally.
- The graph viewport keeps intentional two-dimensional overflow inside itself.

### Card geometry and type

- Shared constants: card width `216`, card height `88`, horizontal gap `44`,
  line height `18`, and edge-anchor offsets derived from width/height.
- Canonical label: `15px`, weight `750–800`, line height `18px`, at most two
  `<tspan>` rows. Prefer boundaries before capital letters; fall back to a
  measured character boundary. Never append an ellipsis to a canonical label.
- A two-line label begins at `y=23`; a one-line label remains vertically aligned
  to the same content band.
- Role and posture appear as separate bottom-row badges with `12px` text and no
  all-caps letter spacing below `0.02em`.
- Role mark remains redundant decoration. State is available as text and in the
  accessible name; color is not the only carrier.
- Every card's accessible name and SVG `<title>` contain the unmodified
  canonical label, friendly name, state, and plain meaning.
- Lane width, start position, node centers, edge paths, labels, and sequence
  markers use the same geometry object; no legacy `78`, `33`, `76`, or `84`
  center/edge offsets remain hard-coded independently.

### Panel controls

Each region has a persistent trigger:

```html
<button aria-expanded="true|false"
        aria-controls="explanation-dock|details-dock|evidence-tray">
  Explanations | Details | Evidence
</button>
```

The visible label stays textual at 200% zoom. An icon may supplement it but may
not replace it. Closing a panel sets `hidden` only after the close transition;
reduced-motion makes that transition effectively immediate.

### Focus and keyboard contract

- A panel trigger opens the panel and moves focus only when the user explicitly
  asked to enter it (for example, mobile sheet open). Desktop pointer opening
  does not unexpectedly move focus.
- `Focus canvas` records its own trigger, sets `canvasFocus=true`, and collapses
  desktop panels or closes the active mobile sheet. It does not clear any
  semantic state.
- Leaving focus mode restores the previous open/closed desktop configuration;
  if that snapshot is unavailable, explanation/details open and evidence closed.
- Escape priority: active mobile sheet → transient tray/dock focus context →
  focus mode. If nothing temporary is open, Escape is a no-op. Clear selection
  remains a labelled action and is no longer overloaded onto Escape.
- Closing a temporary surface restores focus to the exact trigger that opened
  it, falling back to the corresponding persistent toolbar trigger.
- When a selected node opens Details on mobile, the sheet heading receives
  programmatic focus; the selected graph node remains the semantic selection.

### Mobile contract (`max-width: 720px`)

- Docks and tray do not occupy grid columns.
- `activeMobileSheet` is the only visibility authority. Opening one support
  region atomically closes the previous one.
- The sheet is bottom anchored, max height `min(78dvh, 640px)`, scrolls its body,
  has a labelled close button, traps focus while open, and makes the canvas
  behind it inert for keyboard/pointer interaction.
- A non-color state cue in the toolbar names the open sheet.
- The page remains 320px wide without outer horizontal overflow; graph overflow
  stays in the graph viewport.

### Intermediate desktop contract (`721–1180px`)

- Only one dock is open by default. Selecting a graph item prefers Details;
  requesting an explanation swaps to Explanation. Evidence remains a tray.
- The user may close every support surface and retain the graph state.
- No dock may reduce the graph column below 480 CSS pixels; if it would, use
  the one-dock policy rather than squeezing the graph.

## 5. Workflow view

### Inspect and recover

1. User selects `ConversationThread` in `GraphViewport`.
2. Semantic reducer sets `selected` and `selectedKind`.
3. Desktop opens/updates Details; mobile sets `activeMobileSheet="details"`.
4. User minimizes Details.
5. Presentation reducer hides the region; selection and graph dimming remain.
6. User invokes Details again.
7. Details reads the unchanged selection and shows the same record.

### Focus the canvas

1. User has a view, query, sequence, lens, selection, and any panel layout.
2. User activates Focus canvas.
3. Shell snapshots presentation visibility and hides support surfaces.
4. Graph receives the available workspace area without semantic rerender/reset.
5. User exits focus mode.
6. Shell restores the visibility snapshot and returns focus to the focus trigger.

### Switch support context on mobile

1. Details sheet is open for a selected node.
2. User activates Explanations in the persistent sheet switcher.
3. `activeMobileSheet` changes atomically from `details` to `explanation`.
4. Selection remains visible in the graph after the sheet closes.
5. Reopening Details recovers the selected-node content.

## 6. Decision flow

```text
support trigger
  ├─ mobile? ─ yes ─> set activeMobileSheet to requested region
  │                    └─ same region already open? close it
  └─ no
       ├─ focus mode? ─> exit focus mode, then toggle requested region
       └─ toggle only that desktop region

Focus canvas
  ├─ entering ─> snapshot visibility → close supports → preserve semantics
  └─ leaving  ─> restore snapshot → preserve semantics → return focus

Escape
  ├─ mobile sheet open ─> close sheet → trigger focus
  ├─ temporary region context open ─> close context → trigger focus
  ├─ focus mode ─> exit focus mode → focus trigger
  └─ none ─> no-op
```

## 7. Dependency-interface view

| Interface | Input | Output | Failure behavior |
| --- | --- | --- | --- |
| Template → generator | canonical template plus embedded ontology bundle | self-contained root HTML | generation/currentness test fails closed |
| Semantic reducer → graph/contents | semantic exploration state | visible nodes/relations and selected content | empty or invalid refs remain detectable by existing tests |
| Presentation reducer → shell | presentation action plus viewport class | region visibility and focus target | illegal mobile multi-open state rejected/normalized to one sheet |
| Geometry → SVG renderer | measured card constants and positions | cards, anchors, relation paths, labels | bounds assertions fail; do not silently truncate canonical labels |
| Shell → browser accessibility tree | labelled regions, toggles, expanded state, hidden/inert status | perceivable/operable panel model | browser acceptance fails on missing names, focus escape, or stale expansion state |
| Visible graph → text view | the same computed visible node/relation set | synchronized non-graph alternative | count/content mismatch fails deterministic/browser checks |

No interface grants authority. The trust-boundary bar remains visible and the
generated visualization continues to describe a design only.

## Selected panel model

Selected: docked edge panels on wide desktop, single-host bottom sheets on
mobile, and one-dock adaptation at intermediate widths.

Rejected:

- Floating cards: higher collision, z-order, focus-order, persistence, and
  mobile complexity without a demonstrated user need for free placement.
- Modal-only drawers: safer on mobile but prevents desktop comparison of lane
  explanation and selected-node details.

This choice is reversible at the shell boundary because support content and
semantic state do not depend on a panel's presentation mode.

## Acceptance evidence required after implementation

- Node label/client bounds are contained within every node card at 100% and
  200% browser zoom, including the longest canonical label.
- Full canonical names remain in accessible names and SVG titles.
- Exact semantic-state snapshot before/after minimize, focus mode, and mobile
  sheet switching is equal.
- At 1440×1000, both docks can open and the graph remains at least 480px wide.
- At an intermediate width, opening one dock cannot squeeze below 480px.
- At 320×800, only one support sheet is exposed, the outer document has no
  horizontal overflow, and focus cannot escape behind the sheet.
- `aria-expanded`, `aria-controls`, focus restoration, Escape priority,
  reduced-motion, no console/page errors, and no external requests pass.
- Existing generation currency, ontology totals, view membership, explanation
  coverage, and synchronized text-view tests remain green.

## Evidence and handoff ceiling

This artifact is authored-complete and ready for the approved independent UX
review. It has not passed a product Design Validator, and no implementation
evidence exists. The later plan may organize candidate work, but Task Session
admission must require a fresh baseline and the validation contract named here.

