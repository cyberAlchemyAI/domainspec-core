# s9 — Invoke Plan (NON-EXECUTED)

Owner: invoke · mode: plan · verdict: pass · **No code written — this is the plan.**

Target: the TROQAR zone-control authority slice as the shipped-demo wedge, with the **sealed** R2 rule
(s8 repair). Layered by value/cost; each layer emits ONE externally-runnable, honest-labelled artifact.

## L0 — MVP kernel (the wedge made visible)
- **Typed invariant** `ZoneControlSound` over a SEALED window: `resolve(z,w)=argmax_runner Σ duration·surge_k`
  on frozen membership; exact tie → `ContestedUnresolved`; `surge_k` fixed-point.
- **Seal invariant** `arrival(a) > emit_time(cert_W) ⟹ a ∉ validActivitiesIn(z,W)` — the load-bearing
  concurrency clause (build-from-owned: the dcb-saga named-open obligation made real).
- **Auto-verdict gate fixture (#2):** register label = `decidable-check` over sealed facts; evidence =
  the replayable `resolve` trace; emits `✓ CHECK PASSED (decidable) — controller=X over W` + certificate
  `(zone, window, sealedClaimHashes, resolution)`. NOT "provably correct".
- **Validation gate:** re-run the s8 toy_game on the sealed rule — MUST flip `needs-concurrency-semantics`
  → `well-defined`, AND a tampered/late-arrival fixture MUST be rejected `out-of-order-sealed`.
- Artifact: a runnable checker + a specimen certificate a stranger re-verifies.

## L1 — consistency boundary + audit
- Freshness threshold + quiescence AS the seal trigger; late-arrival → successor/amended-window per the
  decision-gate policy. Immutable audit log of `(emit_time, sealedClaimHashes, resolution)`.

## L2 — powerup + advisory feel
- `Surge` powerup: recorded multiplier `surge_k∈[1,2]` folded into the hash preimage (replay-stable).
- `Provisional(runner, confidence)` live signal during the open window — explicitly **advisory, never a
  certificate** (the dialectic's feel-vs-verifiability mitigation).

## Decision-gate items (owner ratification — NOT decided in refine)
1. **Metric:** R2 (Σ-presence) vs R1-at-close (argmin lap). R2 = falsified+repaired primary; R1 = fallback.
2. **Seal policy:** reject-late vs successor-window vs amended-window.
3. **Feel tradeoff:** window-close binding vs live-control feel (the R-feel residue).

## Recommended next routes (post-refine, NOT executed here)
1. `decision-gate` — ratify metric + seal policy + feel tradeoff (3 items above).
2. `sigil-development` / `task-session` — implement L0 kernel + the auto-verdict-gate fixture.
3. Wire as the **first fixture of the auto-verdict gate (#2)** — the wedge build and the shipped demo meet.

## Owner-boundary
Non-executed. No mutation of body-war specs/app/Craft ledger. body-war's `GAP-TROQAR-SCORE-AUTHORITY-001`
is advanced from "needs a rule" to "rule designed, falsified, repaired, plan ready" — the Craft ledger
update is a separate, post-ratification act.
