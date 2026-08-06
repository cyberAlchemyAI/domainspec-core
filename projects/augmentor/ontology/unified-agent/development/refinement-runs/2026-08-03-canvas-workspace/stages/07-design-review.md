# Stage 07 — Design review with UX evidence sidecar

- Capability: `interrogation`
- Mode: `refine-design-review`
- Status: `pass-with-required-repairs`
- Human questions asked: 0; the operator already selected and confirmed the
  docked-panel direction
- Terminal helper: `/root/canvas_design_reviewer`
- Helper mutation: none

## Helper lifecycle

Two bounded attempts were interrupted after failing to return a terminal receipt:
`/root/ontology_html_review` and `/root/beginner_explanations`. Neither reported
writes. The same single read-only role was rerouted to
`/root/canvas_design_reviewer`, which returned the terminal receipt below. The
attempt history is retained rather than being described as three reviewers.

## Sidecar receipt

| Field | Value |
| --- | --- |
| agent_id | `/root/canvas_design_reviewer` |
| role_id | `canvas-evidence-reviewer` |
| dispatch_id / step_id | `2026-08-03-canvas-workspace` / `s7` |
| capability_ref | `ux-evidence-validator` |
| status | `flag` |
| validation | Read-only source, prior evidence, and design-contract review; no browser run |
| observer_status | complete |
| artifacts | seed, Stage 06 design, current template, prior findings, prior layout measurements |
| blockers | none |
| reroute | none after the successful terminal receipt |

The reviewer found the proposed 216×88 card, two-line canonical label, shared
geometry, separate semantic/presentation state, and candidate-only trust
boundary directionally sound. It correctly distinguished the existing browser
evidence from the proposed, unimplemented behavior.

## Required repairs

1. **Measured layout feasibility:** a fixed 721px breakpoint cannot fit a 240px
   dock, gap, and 480px graph. Region mode must derive from available workspace
   width and fall back to edge triggers or sheet presentation before the graph
   becomes narrower than 480px.
2. **Escape and focus ordering:** one `returnFocusId` cannot represent recent
   origins. The design must name deterministic Escape priority and a focus-return
   stack. Stable non-modal desktop docks should not be treated as temporary.
3. **SVG focus visibility:** prior focus evidence covers an HTML button, not
   graph lanes/nodes/relations. All interactive SVG classes need explicit focus
   treatment and keyboard acceptance checks.
4. **Tray geometry:** specify whether the tray overlays or consumes space, and
   retain a minimum usable graph height without covering persistent controls.
5. **Mobile dialog semantics:** the focus-trapped, inert-background sheet must be
   a single labelled modal dialog in the accessibility tree.

## Soft flags

- A lane with eight 216px cards approaches 2,100px, increasing intentional
  internal graph navigation.
- Zoom-to-fit must not shrink the 15px readability target into illegibility.
- Font variation and the longest labels need screenshot/bounds review.
- A 78dvh mobile sheet hides much of the graph by design and needs human
  orientation review.
- Typography cannot prove beginner comprehension of canonical vocabulary.

## Acceptance additions

Desktop must prove measured fallback, 480px minimum graph width, 320px minimum
graph height with the tray open, no invisible closed-dock width, contained card
content at 100% and 200% browser zoom, visible SVG focus, deterministic focus
return, semantic-state equality, and unchanged trust messaging.

Mobile must prove 320px outer reflow, one labelled sheet in the visual and
accessibility layers, `aria-modal`/inert/focus containment, exact trigger return,
atomic sheet switching, semantic and graph-transform continuity, reduced motion,
synchronized text, no external requests, and perceivable trust messaging.

## Review verdict

No blocker requires a new product-direction decision. All five hard-gate risks
have bounded design repairs, so Stage 08 may run. Task Session admission must
block if the repaired contract or its browser assertions are omitted.

