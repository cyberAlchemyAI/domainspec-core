# Stage 04 — Research Decision

Owner: `refine` · Mode: `research-if-gap-appears` · Status: **pass (no external research)**

## Decision

**No external/web research.** Local repository evidence is sufficient and authoritative for B1–B3. The validator, schema, the target artifacts, and the installed skill set are all local and decisive.

## Named gap (recorded, not triggering external research)

- The orchestration/Lean context referenced by the strategy (`arcanum/formulae/dispatch-spec/...`, `domainspec-lean-formalization-*`) partly lives in the **uninitialized `arcanum/` submodule**. This is a *local* gap, resolved by `git submodule update --init arcanum`, **not** by web research.
- Impact on this refinement: **none for B1–B3.** The repair operates on the dispatch JSON + `.md`, which are fully present. The gap only matters if a future pass wants to deep-link Lean lessons; recorded as residue with owner = whoever runs the fan-out execution.

## Confirmation status

External research not selected, not triggered, not run. Local-first honored. No operator confirmation required.
