# s6 — Invoke Design (zone-control authority rule)

Owner: invoke · mode: design · verdict: pass (route open → s7 dialectic → decision-gate)

## The typed invariant (rule-shape, independent of which rule wins)
```
controller(zone, window) : Resolution :=
  let claims = validActivitiesIn(zone, window)        // each: {runner, clan, metric, activityId, ts, factHash}
  in  resolve(claims)                                  // -> Controlled(runner|clan) | ContestedUnresolved
// enforced invariant the auto-verdict gate checks, honestly labelled:
//   ZoneControlSound : ∀ z w. resolve(validActivitiesIn(z,w)) is total ∧ deterministic ∧ replayable
```
- **Register label:** `decidable-check` over recorded facts (NOT "provably correct"). The audit record
  binds `(zone, window, claims[].activityId+factHash, resolution)` → re-verifiable by re-running `resolve`.
- **Scope label:** proves *resolution satisfies the rule over these facts* — not *"rightful champion"*.

## Route menu — which `resolve` (the open decision → s7 dialectic → decision-gate)
| id | rule | resolve(claims) | feel | verifiability | contention behaviour |
|---|---|---|---|---|---|
| **R1** | fastest-lap | argmin metric=lap-time | high | TOCTOU-risk | running-max over open set → Σ class |
| **R2** | cumulative-presence | argmax Σ(time-in-zone) over window | low | deterministic + consistency-boundary | aggregate; window-closed = unique |
| **R3** | king-of-hill | last valid claim | high | TOCTOU-risk | last-writer; clock-dependent |
| **R4** | season total-time | argmin Σ(time) ranking | med | deterministic | aggregate ranking |

## The contention question (F1 — load-bearing, geometry-agnostic)
Two runners' activities for the same zone+window arrive ~simultaneously. The rule must either resolve
**uniquely + replayably** or emit `ContestedUnresolved` (never last-writer-by-clock). R1/R3 are
clock/order-sensitive (TOCTOU); R2/R4 are window-closed aggregates (deterministic once the window
closes, but need a stated **consistency boundary** = when the window is "closed enough" to score —
reuse the DCB freshness guard + the named-open concurrency obligation).

## Powerup pick (F2) — ONE concrete, invariant-preserving
`Surge` powerup: within an active window, multiplies the holder's metric contribution by k (bounded,
k∈[1,2]), expires at window close. It MODIFIES `resolve`'s input weighting but preserves O1 (totality)
and O2 (determinism/replayability) — the multiplier is a recorded, re-checkable fact.

## Enforcement + audit (the wedge made visible)
On each scoring, the **auto-verdict gate (#2)** computes `Pass|Flag|Block` from the rule's declared
register (`decidable-check`) vs the produced evidence (the replayable `resolve` trace), and emits
`✓ CHECK PASSED (decidable) — controller=X over window W` + a certificate
`(zone,window,claimHashes,resolution)` a stranger re-runs. NOT "provably correct."

## Carried to s7 (dialectic) and s8 (toy_game)
- s7: **excitement (R1/R3) vs verifiability (R2/R4)** — the genuine tension; convergence criterion =
  a rule that satisfies O1–O2 *and* is demonstrable as a re-verifiable wedge.
- s8: toy_game falsifies the s7-selected rule under simultaneity → verdict
  {well-defined | underspecified | collapses-to-decidable | needs-concurrency-semantics}.
