# Stage 09 — Invoke Plan (non-executed) + Emit

Capability: `invoke` · Mode: `plan` · Status: **pass**

This stage emits the refined artifacts and records the non-executed plan for what happens next. It does **not** execute the strategy's research fan-out.

## Emitted / mutated artifacts (this refinement's product)

| Artifact | Action | Verification |
| --- | --- | --- |
| `ops/development/infra-spec-research-strategy.dispatch.json` | **promoted** repaired version (receipt-field completeness + 4 capability handles labeled `local-extension`) | `validate-dispatch.py` on canonical path → **VALIDATION=pass** (T5 ✓) |
| `ops/development/infra-spec-research-strategy.md` | self-test command repaired to in-checkout validator; "Scope Boundary" section added | command path exists; section present |
| `…/stages/infra-spec-research-strategy.dispatch.repaired.json` | retained as the run-folder evidence copy | identical to promoted file |

## Non-executed plan: what to run next (the strategy itself is now executable)

1. **Now executable**: the strategy's `validate-research-coverage` gate and its documented self-test command both pass. The strategy can proceed to its own "Next Route" (read-only fan-out execution) when the operator chooses.
2. **Recommended MVP-first first pass (B-opt, unforced)**: before the full 7-lane fan-out, run read-only **L1 Repository Zone Cartographer + L2 Lean Infra Translator + L7 Skeptical Gap Hunter** to produce the cheapest high-signal evidence, then decide whether L3–L6 are warranted. This is a recommendation; the route was **not** rewritten to impose it.
3. **Local gap to clear before deep Lean linkage**: `git submodule update --init arcanum` so `domainspec-lean-formalization-*` and `formulae/dispatch-spec` sources are present.
4. **Do not** create `formulae/infra-spec`, schemas, or registry entries from this refinement — that remains gated behind the strategy's own owner-review + validated-candidate-schema non-negotiables.

## Owner-boundary check

All writes confined to `ops/development/infra-spec-*` (parent-owned) — consistent with the target strategy's own write non-negotiable and confirmed by the owner-boundary reviewer. No child-owned surface touched.

## Verdict

`pass` — refined artifacts emitted and verified; next routes recommended, not executed.
