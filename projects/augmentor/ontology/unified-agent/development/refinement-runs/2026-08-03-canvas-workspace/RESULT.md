# Refine Result

- Target: `projects/augmentor/ontology/unified-agent/ontology-visualization.html`
- Status: `flag`
- Preset: `standard`
- Research: `no-research`
- Run manifest: `RUN-MANIFEST.md`
- Evidence index: `evidence-index.json`
- Seed proposal: `REFINE-SEED-PROPOSAL.md`
- Dispatch route: `REFINE-DISPATCH.json`
- Runtime handoff: `RUNTIME-HANDOFF.md`
- Product implementation: not started and not authorized by this run

## Dispatch strategy

The validated route used the canonical ten-stage sequence with the
`baseline_sequence`, `xray_for_hidden_structure`,
`route_menu_for_ambiguity`, and `toy_game_for_low_cost_falsification`
overlays. The operator selected docked support panels and approved one read-only
`canvas-evidence-reviewer`; the final helper joined with a terminal `flag`
receipt and no writes. Parent synthesis waited for that receipt.

## Stage evidence

- Context Builder evidence baseline: `pass`
- Invoke Define: `pass`
- Interrogation refine-review: `flag` (bounded design risks, no blocker)
- Research decision: `pass` (`no-research`)
- Distill: `pass`
- Invoke Redefine / Design: `pass` (authored, non-executed)
- Interrogation refine-design-review: `flag`
- Distill Repair: `pass`
- Invoke Plan: `pass` (non-executed)
- Final Interrogation and Synthesis: `pass-with-residue`

## Final synthesis

The coherent architecture is a bounded `CanvasWorkspaceShell` with a persistent
`GraphViewport`, in-canvas toolbar, Explanation and Details edge regions, and an
Evidence tray. Wide desktops can show both docks; narrower containers admit a
dock only while the graph retains 480px; mobile and height-constrained content
use exactly one labelled modal sheet. Minimize, focus mode, resize normalization,
and sheet switching change presentation state only. Selection, filters, view,
sequence, explanation lens, and graph transform remain semantic exploration
state.

Node cards target 216×88 geometry, a 15px/18px two-line untruncated canonical
label, 12px role/state metadata, full accessible names/titles, and one shared
geometry contract for cards, anchors, edges, labels, and sequence markers.

The independent UX review exposed five hard-gate risks. The repaired design now
uses measured layout feasibility, a deterministic focus-return stack and Escape
order, explicit SVG focus, a space-consuming non-overlay tray with a 320px graph
height floor, and one properly labelled/inert/focus-contained mobile dialog.

Implementation is split into seven SWUs. `SWU-CANVAS-001` is the first reversible
card-legibility proof; complete feature evidence requires `SWU-CANVAS-007` and a
fresh hash-bound UX evidence bundle. The current UI has not changed in this run.

## Residue

- Beginner comprehension, perceived balance/trust, navigation efficiency, and
  low-vision adequacy require human evidence.
- The proposed behavior has no browser evidence until it is implemented.
- Current untracked/dirty target bytes require exact baseline binding; they must
  not be silently attributed or overwritten.
- Candidate-local, interpretive-read-model, and `authority_effect:none` ceilings
  remain unchanged; this does not prove routing, memory, reasoning, work, or
  authority capability.

## Recommended next route

Explicitly admit `task-session` for
`WP-AUG-CANVAS-001 / SWU-CANVAS-001`. Do not start later SWUs until the preceding
receipt passes. Task Session, commits, publication, deployment, and promotion
are outside this completed Refine run.

