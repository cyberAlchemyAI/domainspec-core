# Stage 02 — Define the canvas workspace

- Capability: `invoke`
- Phase: `define`
- Status: `authored-complete`
- Discovery: waived because the operator named an existing artifact, supplied a
  screenshot, selected the docked-panel route, and confirmed the dispatch
- Promotion: none; these are run-local terms

## Problem statement

The current interface makes the graph one card in a long document. Its fixed
156×66 node cards truncate canonical names to one 13px line, which can collide
visually at the current scale. Explanations, controls, details, gaps, and the
text view compete vertically with the graph rather than behaving as tools of a
single exploration space.

## Defined target

`CanvasWorkspace` is the full interactive product surface. The graph occupies
its persistent background. Supporting controls and reading surfaces are
contained regions of the same workspace and can be collapsed independently.
Collapsing a region changes presentation only; it does not erase or rewrite the
current semantic exploration state.

## Run-local glossary

| Term | Definition | Does not mean |
| --- | --- | --- |
| `CanvasWorkspace` | The bounded viewport containing the graph, toolbar, docks, and tray. | An infinite document, ontology store, or operating-system desktop. |
| `GraphViewport` | The pan/scroll/zoom region in which the four lanes, nodes, and relations render. | The full page or a separate authority surface. |
| `CanvasToolbar` | A compact in-canvas surface for view, query, posture, zoom, reset, and focus-canvas actions. | A route executor or persistence layer. |
| `ExplanationDock` | A left edge panel for explanation mode, lane explanations, and the current lens. | The selected-node record. |
| `DetailsDock` | A right edge panel for the selected lane, node, or relation. | Selection itself; minimizing it does not clear selection. |
| `EvidenceTray` | A bottom panel for example flows, legend, known gaps, and synchronized text view. | An audit authority or source of truth. |
| `PanelState` | Ephemeral UI state describing visibility, active mobile sheet, focus mode, and focus-return target. | Conversation, session, memory, work, ontology, or routing state. |
| `CanvasFocusMode` | A reversible presentation mode that collapses support regions while preserving semantic exploration state. | Fullscreen permission, loss of context, or a semantic reset. |
| `GraphNodeCard` | A selectable SVG group with a readable canonical label and separate role/state metadata. | A runtime capability or proof of implementation. |

## State namespace boundary

Semantic exploration state remains:
`view`, `query`, `posture`, `selected`, `selectedKind`, `sequence`, and
`explanationLens`.

Presentation state is added separately:
`explanationOpen`, `detailsOpen`, `evidenceOpen`, `activeMobileSheet`,
`canvasFocus`, and `returnFocusId`.

No presentation transition may modify semantic state unless the user invokes an
existing semantic control such as Clear selection or Clear filters.

## Acceptance definition

- Canonical node labels render at 15px or larger with 1.2 or greater line
  height and at most two visible lines; the full label remains in accessible
  naming and `<title>`.
- Role and implementation state are visually distinct metadata at 12px or
  larger, not merged with the canonical label.
- The graph remains present while desktop support regions open and close.
- Focus canvas minimizes every support region and preserves semantic state.
- Desktop can show explanation and details concurrently; mobile exposes no more
  than one support bottom sheet at a time.
- Panel toggles are buttons with correct `aria-expanded` and `aria-controls`.
- Escape closes the topmost temporary support surface and restores focus to its
  trigger; it does not silently clear selection.
- The outer document has no horizontal overflow at 320 CSS pixels; intentional
  graph panning/scrolling remains contained in `GraphViewport`.
- Reduced-motion and synchronized text-view behavior remain supported.

## Non-goals

- Changing ontology nodes, relations, sources, views, or authority semantics.
- Implementing routing, sessions, memory, reasoning, work execution, or approval.
- Persisting panel state across sessions in the first implementation slice.
- Movable/free-floating windows, resizable docks, or multi-canvas tabs.
- Claiming beginner comprehension, aesthetic preference, or full WCAG conformance.

## Boundary result

The terms are mutually distinguishable and do not collapse presentation state
into ontology or runtime state. Define is ready for adversarial review.

