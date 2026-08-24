# Stage 08 — Distill repair

- Capability: `distill`
- Mode: `validate`
- Status: `pass`
- Input: Stage 07 `pass-with-required-repairs`

## Repaired coherent unit

`CanvasWorkspaceShell` remains the selected SCU. The reviewer did not show that
it is too large or unable to recompose; it showed that five shell contracts were
underspecified. The repair changes those contracts without absorbing graph data,
content ownership, persistence, or runtime behavior.

## Repaired contracts

### 1. Measured region mode

The shell observes its own available inline size. It enables a requested dock
only when:

`availableInline >= 480 + requestedDockWidth + visibleOtherDockWidths + gaps`.

If the inequality fails, closed labelled edge triggers remain and the requested
support region uses the single-sheet host. The named 720/1180 CSS ranges are
styling hints, not the feasibility authority. A `ResizeObserver` or equivalent
container measurement normalizes open regions without changing semantic state.

### 2. Deterministic focus and Escape

Presentation state replaces `returnFocusId` with:

```js
focusReturnStack: [{ surface, triggerId }]
```

- Wide desktop docks and the space-consuming tray are stable non-modal regions;
  Escape does not minimize them.
- A mobile sheet is modal and closes first on Escape, popping its trigger.
- Focus mode is next and exits on Escape, restoring its visibility snapshot and
  trigger.
- With neither modal sheet nor focus mode active, Escape is a no-op. Selection
  is cleared only by the explicit Clear selection action.
- Selecting a graph object updates Details content but never reopens a panel the
  user minimized.

### 3. SVG focus

Lanes, nodes, and relations receive explicit non-color-only focus treatments
with at least a 2px visible outline/stroke against the canvas. Browser tests
exercise Tab focus plus Enter/Space activation for every interactive SVG class.

### 4. Tray behavior

The desktop tray consumes workspace grid rows; it never overlays the graph or
toolbar. Its open height is `min(38dvh, 360px)` and the graph retains at least
`320px` block size. If both cannot fit, the tray content uses the sheet host.
Persistent region triggers remain outside its scrolling body.

### 5. Mobile sheet semantics

The sheet host exposes exactly one `role="dialog"`, `aria-modal="true"`, and a
programmatically associated visible heading. The graph/shell background is
inert while open. Focus starts at the heading/close control, remains contained,
and returns to the exact trigger on close or Escape.

### 6. Readable graph navigation

Default graph scale is 1. `Fit` may not reduce rendered canonical labels below
15 CSS pixels; if the graph cannot fit at that readability floor, it keeps
contained two-dimensional navigation and exposes a visible pan/scroll cue plus
Reset view. Browser zoom remains independent.

## Recomposition proof

Each repair is owned by the shell, presentation reducer, geometry contract, or
browser acceptance layer. None changes the generated ontology data or the
semantic reducer. The unit still recomposes through the existing template and
generator. The repair is ready for the toy scenario and non-executed plan.

