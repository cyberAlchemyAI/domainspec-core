# Implementation Layering — Canvas workspace

- Status: candidate plan; not executed
- Complexity: high (seven independently verifiable SWUs across rendering,
  composition, presentation state, responsive layout, focus, modal behavior,
  and evidence closure)
- Canonical UI source: `visualization/template.html`
- Generated mirror: `ontology-visualization.html`
- First useful proof: `SWU-CANVAS-001`
- Complete feature evidence: all layers through L5

| Layer | Question | SWUs | Promotion evidence |
| --- | --- | --- | --- |
| L0 Legibility | Can every canonical node label and both metadata fields fit at a readable size without changing ontology data? | `SWU-CANVAS-001` | shared geometry, two-line wrap, bounds checks, screenshot review, generation/currentness pass |
| L1 Composition | Can the current guide, controls, graph, details, flows, legend, gaps, and text alternative recompose into one canvas shell without losing content? | `SWU-CANVAS-002` | DOM/accessible-region inventory parity and existing interactions pass |
| L2 Desktop state | Can non-modal docks/tray minimize and focus mode restore without changing semantic state? | `SWU-CANVAS-003` | state snapshots equal, toggles accurate, stable Escape contract, graph persists |
| L3 Adaptive/accessibility | Can layout feasibility and keyboard behavior remain deterministic across sizes? | `SWU-CANVAS-004`, `SWU-CANVAS-005` | measured 480px/320px floors, no occlusion, SVG focus, focus-return stack, 100%/200% checks |
| L4 Mobile sheet | Can exactly one labelled modal support sheet operate at 320px while preserving state and focus? | `SWU-CANVAS-006` | one visual/a11y dialog, inert background, trapped/restored focus, atomic switching, outer reflow pass |
| L5 Evidence closure | Does the complete implemented target satisfy deterministic, browser, source/generated, and UX-evidence gates? | `SWU-CANVAS-007` | all declared commands pass and a fresh hash-bound evidence bundle is retained |

## Promotion rules

- A layer may start only after all dependencies have terminal passing receipts.
- A passing lower layer proves only its question; it does not prove the complete
  canvas experience.
- Generated HTML is refreshed by the existing builder and is never edited as
  authority.
- Any ontology, source, view, relation, residue, authority, routing, memory, or
  reasoning change is out of scope and must stop the session.
- Human comprehension, navigation efficiency, trust, and visual preference do
  not promote from browser evidence.

## Rollback boundaries

Each SWU is limited to template/test/generated-output deltas named in the work
pack. Because the current package contains untracked/dirty user bytes, rollback
must be patch-local and receipt-backed; no Git reset, checkout, or blanket file
replacement is permitted.

