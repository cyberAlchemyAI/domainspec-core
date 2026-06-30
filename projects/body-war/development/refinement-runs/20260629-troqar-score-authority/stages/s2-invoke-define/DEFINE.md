# s2 — Invoke Define

Owner: invoke · mode: define · verdict: pass

## What is being defined
The **zone-control authority rule**: given the set of valid Activities touching a Zone in a scoring
window, a deterministic function `controller(zone, window) -> Clan|Runner|none` plus the **Zone
Score**, expressed as a **typed invariant** the runtime can enforce and an auditor can re-verify.

## Obligations (the invariant must carry)
- **O1 totality:** every (zone, window) with ≥1 valid activity resolves to exactly one controller or
  an explicit `contested-unresolved` state — never silent ambiguity.
- **O2 determinism/verifiability:** `controller` is a pure function of recorded, re-checkable facts
  (activity id, timestamp, validated metric) — re-running it yields the same verdict (claim≤proof).
- **O3 contention resolution:** simultaneous/near-simultaneous claims (the Σ/TOCTOU class) resolve by
  a stated tiebreak, or surface as `contested-unresolved` pending evidence — never last-writer-by-clock.
- **O4 anti-cheat surface:** the rule names which fact it trusts (validated Strava metric) and what it
  does on a disputed/non-rerunnable fact (freshness reject — reuse DCB content-hash + a concurrency guard).
- **O5 powerup hook:** at least one powerup can MODIFY the rule within bounds (e.g. a multiplier or a
  grace window) without breaking O1–O2.

## Scope fence (claim≤proof)
The invariant proves **"this controller assignment satisfies the rule over these recorded facts"** —
NOT "the runner is the rightful champion." Adequacy of the metric (does fastest-lap model "best") is a
product decision, labeled separately. This is the constrained≠correct seam, on a game.
