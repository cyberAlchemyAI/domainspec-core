# Stage 8 — Distill Repair (validate)

Repair check on the distilled unit:
- **multitaper × critical-band roughness compatible?** YES — both intentionally discard fine partial
  structure; multitaper lowers variance, band-roughness reads fluctuation. No double-counting; they act on
  different axes (estimator vs representation). Validated.
- **Does the fix actually beat EPS?** UNPROVEN until v2 is built and O8 re-run — the design names this as
  the gating test (RESULT plan step 3), not an assumed pass. Honest.
- **Owner-boundary intact:** no `studio_core/` source mutated; recommendation feeds `invoke design`.
- Verdict: repaired + bounded; one explicit empirical obligation carried forward (re-run O8 on v2).
