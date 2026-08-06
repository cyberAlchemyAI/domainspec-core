# Stage 09 — Plan Distill validation

- Capability: `distill`
- Mode: `validate`
- Status: `pass`

## Proposal track

The initial plan grouped adaptive layout, SVG focus, Escape behavior, tray
geometry, and mobile dialog behavior into one responsive-accessibility task.

## Balancer challenge

That bundle is task-shaped: layout feasibility, keyboard/focus ownership, and
modal behavior have different failure modes and can be validated independently.
Combining them would let a passing reflow result obscure a focus or dialog
failure.

## Reconciliation

Split the bundle into:

- `SWU-CANVAS-004` measured layout and tray geometry;
- `SWU-CANVAS-005` SVG keyboard/focus and Escape stack;
- `SWU-CANVAS-006` one mobile dialog host;
- `SWU-CANVAS-007` evidence-only closure with no product repair rights.

Keep node typography, static composition, and desktop panel state as separate
predecessors. The resulting seven SWUs each have one dominant state transition
or observable output and recompose in a dependency DAG. Plan validation passes.

