# s5 — Distill (coherent-unit selection)

Owner: distill · mode: standard · verdict: pass

## Selected coherent unit (the smallest thing that demonstrates the wedge)
**One Zone, one scoring window: the `controller(zone, window)` invariant + its contention resolution
+ a re-verifiable audit record.** Geometry-agnostic (over validated Activities-in-Zone). Plus ONE
powerup that modifies it.

## Rejected alternatives (and why)
- ✗ Full territory-scoring system (all zones, leagues, seasons) — too large; not needed to demonstrate
  the wedge; would drag in deferred geometry + backend-provider gaps.
- ✗ The whole `game-rules` feature — same; the wedge needs one rule, end-to-end, not a rules engine.
- ✗ Real-time live control feed — couples to deploy/ops plumbing (the current next-move trap); the
  demonstration is the *rule + proof + audit*, not the live UX.

## Why this unit recomposes upward
The single-zone controller invariant is the cell the full territory map is tiled from; proving it
honestly (O1–O5) is the reusable kernel. It is also the **first fixture of the auto-verdict gate (#2)**
— so this unit simultaneously advances the wedge build and the shipped demo. One unit, two fronts.
