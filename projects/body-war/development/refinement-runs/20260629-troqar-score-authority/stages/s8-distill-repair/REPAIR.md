# s8 — Distill Repair

Owner: distill · mode: validate (repair) · verdict: **FLAG — repair required, design salvageable**

## What the toy_game falsified
The s7-converged R2 rule's certificate is **not actually replayable** under late in-window arrivals
(see TOY-GAME.md). The consistency guard collapses (verdict-invariant) — the genuine cross-record /
concurrency content the slice must demonstrate is exactly what the converged rule was missing.

## The repair (build-from-owned)
1. **Seal invariant** (the real concurrency edge — the named-open obligation from `dcb-saga-correctness`,
   now made load-bearing): `arrival(a) > emit_time(cert_W) ⟹ a ∉ validActivitiesIn(z,W)`. Window
   membership freezes at certificate emission; late in-window activities route to a successor/amended
   window or are rejected `out-of-order-sealed`. **This** is the clause that makes the certificate
   genuinely replayable — and it is precisely the TOCTOU discrimination the correctness-ownership
   sweep flagged as net-new (build target #1).
2. **Pin `surge_k`** to fixed-point/rational so the exact-tie → ContestedUnresolved branch is reachable.

## Why this is the RIGHT outcome (not a failure)
The toy_game caught our *own* converged design making a false "replayable" claim — and we wrote it
down. That self-caught-overclaim is the wedge thesis demonstrated on a live slice: claim ≤ proof,
honestly, before any code. The repaired rule reaches **well-defined** only after the seal — re-run the
toy_game on the sealed rule in validation (must flip `needs-concurrency-semantics` → `well-defined`).

## Carried to s9 (plan) and decision-gate
- Seal policy is a **decision-gate** item: reject-late vs successor-window vs amended-window.
- The seal invariant is the kernel that the auto-verdict-gate fixture (#2) must enforce + certify.
