# Stage 09 — Invoke Plan result

- Capability: `invoke`
- Phase: `plan`
- Status: `complete-non-executed`
- Complexity: high
- Product writes performed: none

## Goal

Implement a readable canvas-first Augmentor ontology workspace through seven
small, evidence-bound Task Sessions, preserving ontology and authority boundaries.

## Plan artifacts

- `../IMPLEMENTATION-LAYERING.md` — six evidence layers and promotion gates
- `../WORK-PACK.md` — seven bounded SWUs, exact scopes, acceptance, commands,
  and Task Session closeout contract
- `09-plan-distill.md` — automatic plan-shape validation and split rationale

## Decisions

- Canonical UI edits belong in `visualization/template.html`; the root HTML is
  a generated mirror.
- Card legibility is the first reversible proof.
- Shell composition precedes behavior.
- Semantic and presentation reducers remain separate.
- Layout mode derives from available workspace geometry, not a fixed viewport
  breakpoint alone.
- Stable desktop regions are non-modal; mobile uses one labelled modal host.
- Evidence closure cannot repair product code.

## Admission ceiling

This plan is complete and executable in shape, but this Refine confirmation did
not authorize product implementation. The next owner must explicitly admit a
`task-session` for `SWU-CANVAS-001`, bind the current untracked/dirty baseline,
and stop if its scoped bytes overlap unknown work. No formal product Design
Validator or post-implementation UX evidence pass is claimed here.

## Next route

`task-session` → `WP-AUG-CANVAS-001 / SWU-CANVAS-001`.

