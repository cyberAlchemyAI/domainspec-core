# s8 — Toy Game (contention falsification evidence)

Owner: contention-falsifier (subagent, registered) · overlay: toy_game · verdict: **needs-concurrency-semantics**

## Fixture (hand-traceable)
Zone `summit`, window `W=[100,200)`, `DCB_freshness_threshold=50`, `T_quiesce=30`. Score = Σ duration·surge_k.

| act | runner | ts | duration | surge_k | arrival |
|---|---|---|---|---|---|
| a1 | Ana | 120 | 10 | 1.0 | 130 |
| a2 | Ana | 150 | 5 | 1.6 | 155 |
| a3 | Bo | 110 | 8 | 1.0 | 118 |
| a4 | Bo | 180 | 4→5 | 2.0 | 182 |
| a5 | Bo | 160 | 12 | 1.0 | **265 (sync lag)** |

## The decisive trace — mutable past (Stressor 2, the killer)
1. `now=250`: close-eligible (250−200≥50 ✓; last arrival a4@182, 250−182=68≥30 ✓ quiescent). **Certificate C1 emitted: winner=Ana (18 vs 16)**, claimHashes={a1,a2,a3,a4}.
2. `now=265`: a5 arrives — `ts=160 ∈ W`, valid by event time. `validActivitiesIn` filters on event time, "NOT arrival time" → a5 is licensed into W.
3. Replay including a5: Bo=28 > Ana=18. **The replay disagrees with C1.** The "replayable by a third party" guarantee is FALSE.

The quiescence guard is evaluated at close (t=250) and cannot observe the t=265 arrival → it does **not** seal the past.

## Collapse-test (Stressor 4) — the dcb-saga A3 pattern, reproduced
Strip the guard (R2' = filter-by-ts-then-argmax, tie→Contested). On every stressor (tie / surge / late-arrival), **R2' and R2 produce identical resolutions** — flipping the consistency guard on/off is **verdict-invariant**. The guard only changes *when* a cert may fire, never *what* it resolves to, and it does not seal against a5. The "DCB freshness/quiescence boundary" is decoration over `filter-by-ts-then-argmax` — exactly `[[kodamai-smithe-correctness-layer-synthesis]]`'s A3 finding (dcb→hash verdict-invariant), caught again in our own fresh design.

## Secondary: underspecification
The "exact Σ tie → ContestedUnresolved" branch is **dead code under IEEE-754 floats** (`5·1.6` ≠ exact 8). Tie fires only if `surge_k` is pinned to fixed-point/rational. Locally repairable.

## What is SOUND (claim ≤ proof)
The resolution math (`argmax Σ duration·surge_k`, tie→Contested) is sound; surge replay is clean *given a frozen activity set*. The defect is scoped precisely to **write-ordering at the window seal**.

## Minimal repair → s8 REPAIR
Add a **seal invariant**: `arrival(a) > emit_time(cert_W) ⟹ a ∉ validActivitiesIn(z,W)`. On cert emission, W membership freezes; late in-window arrivals route to a successor/amended window or are rejected `out-of-order, sealed`. Pin `surge_k` to fixed-point.
