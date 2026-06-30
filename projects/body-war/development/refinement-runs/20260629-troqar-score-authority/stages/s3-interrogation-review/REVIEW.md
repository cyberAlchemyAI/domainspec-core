# s3 — Interrogation (refine-review of the Define)

Owner: interrogation · mode: refine-review · verdict: pass (with 2 carried flags)

## Findings
- **PASS:** the Define correctly makes the rule geometry-agnostic (over Activities-in-Zone), which
  dodges the deferred geometry blocker — the slice can proceed without sourced polygons.
- **PASS:** O2 (determinism/verifiability) + the scope fence (O-scope) are exactly the wedge; the
  define resists "provably correct" inflation. Good.
- **FLAG F1 (carried to s6/s7):** O3 contention is under-specified — "fastest-lap" makes `controller`
  a **running max over an open set of activities**; that is the Σ/TOCTOU hard case, not a per-activity
  check. The Define names it but does not resolve it. This is the dialectic + toy_game's job.
- **FLAG F2 (carried to s6):** O5 powerup is a placeholder; the design must pick ONE concrete powerup
  and show it modifies the invariant without breaking O1/O2.
- **No BLOCK.** The define is sound enough to design from.
