# s4 — Research Decision

Owner: refine · mode: research-if-gap-appears · verdict: pass

## Decision: NO external research triggered (local-first holds)
The two carried flags (F1 contention, F2 powerup) are resolvable from **owned** precedent:
- F1 (Σ/TOCTOU contention) → reuse `dcb-saga-correctness` (the witness + the content-hash freshness
  guard + the named-open concurrency obligation) and `alloy-tla-modeling` (TLA+ for the temporal
  contention model; Alloy for adjacency). No external source needed.
- F2 (powerup) → product-local design choice; no external precedent required.

No named **external**-context gap appeared (the contention math is owned, not novel-to-the-field).
**Re-open condition:** if the toy_game (s8) finds the chosen rule `needs-concurrency-semantics`
beyond what TLA+ owned-precedent covers, escalate to bounded-research with operator confirm.
