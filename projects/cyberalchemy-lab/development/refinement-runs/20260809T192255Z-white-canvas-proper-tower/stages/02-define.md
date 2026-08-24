# Stage 02 — Invoke Define

- Capability: `invoke`.
- Mode: `define`.
- Handle: native `invoke:define` authoring pass.
- Runtime surface: parent-native.
- Target artifact: white-canvas proper-tower UX/design definition.
- Template selection: local `ux-plan` companion semantics within this run-local stage artifact; no template promotion.
- Questions asked: 0. The operator already chose white canvas, proper tower, no background, and approved the reviewer strategy; no blocker ambiguity remains.
- Verdict: `pass`.

## Defined terms

**White Canvas** — the primary viewport is a warm-white or white surface with quiet structural guides. It contains no rotating photographic scene layer or dark veil. White does not mean empty: hierarchy comes from typography, borders, spacing, floor depth, and restrained CyberAlchemy blue/amber accents.

**Proper Tower** — one vertically organized, visibly architectural DOM structure composed of a shell, a spine, and exactly three selectable evidence floors. It is the primary orientation and navigation object. It is not a runtime graph, persona habitat, simulation, or authority artifact.

**Evidence Floor** — a native button and associated content region bound to exactly one existing scene descriptor, including its `level_id`, evidence state, source references, implementation status, claim ceiling, and unavailable reason where applicable.

**Tower Spine** — a decorative/structural connector showing order between floors. It may animate subtly, but it cannot encode evidence or status without equivalent text.

**Evidence Detail Surface** — the anchored region that explains the selected floor and retains source inspection, relation filtering, residue, and claim-ceiling information.

**System Atlas** — a visibly separate compact list of Tower System architectural descriptors. Unproven descriptors remain unavailable/refusal controls. They are not floors in the evidence tower.

## Desired behavior

1. The initial view immediately exposes one selected tower and its three stacked floors.
2. A floor can be activated with pointer, Enter, or Space and has one visible `aria-pressed` state.
3. Selection updates the bound evidence detail without moving focus unexpectedly.
4. Reset returns to `evidence-l0-corpus` and focuses its floor control.
5. System Atlas selection renders the existing explicit refusal state and never lights a tower floor as functioning.
6. On narrow viewports, the tower becomes a compact vertical stack followed by the detail surface; semantic order remains unchanged.
7. Reduced motion removes decorative transitions without changing selection, reading order, state, or detail content.

## Non-goals

- no pan/zoom, free camera, RPG movement, game engine, Anime.js dependency, or image generation;
- no multi-tower selector beyond the existing one synthetic tower;
- no change to the scene-manifest schema or API semantics;
- no real source/tower selection, workflow execution, agent operation, scoring, adjudication, authority, or promotion;
- no product mutation during this Refine run.

## Success definition

The design is defined when a first-time user can answer from the initial viewport: “What is the tower?”, “Which floor am I on?”, “What evidence state does it have?”, and “Why are the System layers separate or unavailable?” without interpreting the decorative background.

## Dispatch technique trace

- `frame_handoff`: consumes the strict Context Builder pack.
- `owner_boundary_check`: defines a UX object while preserving the manifest, source, and future execution owners.
- `component_descriptor`: names shell, spine, floors, detail, and atlas as separate responsibilities.
- Full dispatch: `REFINE-DISPATCH.json`, validation `pass`.
- Distill in Define: not required here because Stage 05 owns the already-approved bounded reduction; Define does not claim plan readiness.

## Output boundary

This artifact defines design intent only. It changes no product, source, schema, authority, promotion, publication, deployment, release, or runtime state.
