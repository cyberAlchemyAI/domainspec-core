# Stage 03 — Interrogation (refine-review)

Capability: `interrogation` · Mode: `refine-review` · Runtime: native · Status: **flag → routed**
Overlays: `dialectic_for_tension` · Roles: proposer, critic, synthesizer · Inputs: Define (s02), subagent receipts

Critique of the Define's claim that the refinement target is "make the existing strategy valid, runnable, unambiguous."

## Proposer

The Define is correct and well-scoped: the headline defect (dispatch blocks validation) is objective, reproducible, and violates the strategy's own non-negotiable. Repairing it is unambiguously "better."

## Critic (skeptical + owner-boundary lenses)

1. **Is passing the validator actually "better," or just box-ticking?** — A route that blocks cannot be executed by the very `validate-research-coverage` gate it defines. So validity is a precondition for the strategy to function at all, not cosmetics. Holds.
2. **Risk of over-editing.** — "Make it better" could tempt a rewrite of the 7 lanes. That would be scope creep and would destroy reviewed design. The refinement must stay surgical (B4). Accepted as a hard constraint.
3. **Is the `local-extension` capability label honest?** — `x-ray`, `decision-gate`, `robot-talks`, `implementation-readiness` are real installed skills (present under `.claude/skills/`). Labeling them `local-extension` with provenance is truthful, not a workaround to silence the validator. Verified against the skills list. Holds.
4. **Scope-boundary note — necessary or padding?** — A careful operator (and this very run) conflated infra-spec with runtime-surface convergence. The convergence-tension subagent drifted for the same reason. The conflation is demonstrated, not hypothetical. The note earns its place.
5. **Owner boundary.** — All proposed writes are under `ops/development/infra-spec-*`, which the owner-boundary reviewer confirmed is parent-owned and matches the strategy's own write non-negotiable. No child surface touched. Holds.

## Unsupported-assumption separation

- Assumption that the `.md` validate command is broken: **verified** (submodule empty). Not an assumption.
- Assumption that MVP-first ordering is wanted: **not verified** — demote to a recommendation/residue, do not impose. (Routed to Distill as optional.)

## Synthesizer (residue ledger)

- Stable, supported: B1 (validity), B2 (runnable self-test), B3 (scope note) are real improvements with surgical edits.
- Demoted to residue/recommendation: B-opt (MVP-first lane ordering) — valuable but a design opinion the operator should accept explicitly; keep as a recommendation, not a forced edit.
- No stable disagreement remains that blocks design.

## Verdict

`flag` (one item demoted to residue) → proceed. Refinement scope locked to surgical B1–B3 + B4 no-regression, with B-opt carried as a recommendation.
