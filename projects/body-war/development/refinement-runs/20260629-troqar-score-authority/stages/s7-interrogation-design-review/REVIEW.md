# s7 — Interrogation (refine-design-review · DIALECTIC)

Owner: interrogation · mode: refine-design-review · overlay: dialectic · verdict: pass (CONVERGED)
Subagent receipts: rule-advocate-A (real-time), rule-advocate-B (verifiability). Both registered.

## Collapse check (P14 — initial vs final positions)
- **A:** initial = R1 fastest-lap (real-time flip) → final = **R1 bound at window-close, live leaderboard advisory-only** (conceded the open-set / mutable-past problem: mid-window flips are not replayable; a late-ingested faster lap creates a mutable past that breaks the audit certificate).
- **B:** initial = R2 cumulative-presence → final = **R2 at window-close + DCB freshness/quiescence consistency boundary + a non-binding `Provisional(runner,confidence)` live signal**.
- **Genuine convergence, not bias-collapse:** the two started from opposed philosophies and independently reached the SAME structure — *binding resolution over a closed claim set at window-close, with any live signal explicitly advisory.* Convergence criterion from the dispatch ("satisfies O1–O2 AND is demonstrable as a re-verifiable wedge") is MET.

## Selected candidate rule → s8 / decision-gate
**R2 — cumulative-presence at window-close:**
```
resolve(z,w) = argmax_runner Σ { duration(a) · surge_k(a) | a ∈ validActivitiesIn(z,w) }
  validActivitiesIn filters on ts ∈ window (NOT arrival time)
  window scores only when (now − window.end) ≥ DCB_freshness_threshold AND no in-window
    activity arrived within the last T_quiesce  (the consistency boundary; reuse DCB guard)
  exact Σ tie → ContestedUnresolved   (O3 honestly; never clock-broken)
  certificate (zone, window, claimHashes, resolution) — replayable by a stranger
```
Chosen over R1-at-close because R2's argmax-Σ is the genuine cross-record aggregate that *exercises*
the consistency boundary (the hard, build-from-owned layer) — A itself endorsed R2 as provable
"without caveats." Surge powerup = a recorded multiplier fact (O5), so replay stays stable.

## Residue ledger (carried — not resolved here)
- **R-feel (product, → decision-gate):** does window-close binding kill live-control feel and make a
  worse game? Both advocates flagged it; unresolvable from a technical position. The `Provisional`
  live signal is the proposed mitigation, but the bind-granularity is a product call.
- **R-metric (→ decision-gate):** R2 (Σ-presence) vs R1-at-close (argmin lap) — the metric choice is a
  product call; R2 is the falsification + MVP primary, R1-at-close the simpler fallback.

## To s8
Falsify R2 under simultaneity/contention: does `resolve` stay total + deterministic + replayable; does
the freshness/quiescence boundary prevent a mutable past; does it collapse to a trivial decidable check?
