---
node_type: result
is_session: false
status: candidate
boundary: INTERNAL — body-war private consumer; this slice is the shipped-demo wedge
created: 2026-06-29
owner: refine
verdict: flag
---

# REFINE RESULT — TROQAR Zone-Control / Score-Authority Rule

## Status: FLAG (refinement ran clean; design sound with one required repair + open decision-gate items)

## One-line synthesis
The refine loop turned `GAP-TROQAR-SCORE-AUTHORITY-001` from "needs a rule" into a **typed,
falsified, repaired, plan-ready** zone-control invariant — and in doing so **demonstrated the wedge on
a live slice**: the toy_game caught our *own* converged design making a false "replayable certificate"
claim (a late in-window arrival mutates the past), the consistency guard collapsed verdict-invariant
(the dcb-saga A3 pattern, reproduced), and we wrote it down and repaired it (the **seal invariant**)
*before any code*. Claim ≤ proof, self-caught — exactly the differentiator the slice exists to show.

## What was decided / produced
- **Rule (candidate, → decision-gate):** R2 cumulative-presence at window-close, `argmax Σ duration·surge_k`
  over a **sealed** window; tie → `ContestedUnresolved`; fixed-point `surge_k`.
- **The load-bearing fix:** the **seal invariant** `arrival(a) > emit_time(cert_W) ⟹ a ∉ validActivitiesIn(z,W)`
  — the genuine TOCTOU/concurrency discrimination (build target #1 from the correctness sweep), now
  concrete on a real slice.
- **Enforcement:** the auto-verdict gate (#2) emits `✓ CHECK PASSED (decidable)` + a replayable
  certificate — honest register, NOT "provably correct". The slice is its **first fixture**.

## Stage evidence
| stage | verdict | artifact |
|---|---|---|
| s1 Context Builder | pass | stages/s1-context-builder/context-pack.md |
| s2 Invoke Define | pass | stages/s2-invoke-define/DEFINE.md |
| s3 Interrogation (refine-review) | pass (2 flags carried) | stages/s3-interrogation-review/REVIEW.md |
| s4 Research decision | pass (no external) | stages/s4-research-decision/RESEARCH-DECISION.md |
| s5 Distill | pass | stages/s5-distill/DISTILL.md |
| s6 Invoke Design | pass (route open) | stages/s6-invoke-design/DESIGN.md |
| s7 Interrogation (dialectic) | pass (CONVERGED) | stages/s7-interrogation-design-review/REVIEW.md |
| s8 Distill Repair (toy_game) | **flag — needs-concurrency-semantics, repaired** | stages/s8-distill-repair/{TOY-GAME,REPAIR}.md |
| s9 Invoke Plan | pass (non-executed) | stages/s9-invoke-plan/PLAN.md |
| s10 Final synthesis | flag | this file |

## Subagents (registered: 2026-06-29-troqar-score-authority)
3 across 2 groups — dialectic (rule-advocate-A real-time, rule-advocate-B verifiability; converged) +
contention-falsifier (toy_game; verdict needs-concurrency-semantics). anti-bias axis: rule-philosophy.

## Residue (carried — NOT resolved in refine)
- **R-validation:** the sealed rule must re-pass the toy_game (`needs-concurrency-semantics` → `well-defined`)
  + reject a tampered/late-arrival fixture. Open until L0 validation.
- **R-decision-gate:** metric (R2 vs R1-at-close); seal policy (reject vs successor vs amended window);
  feel tradeoff (window-close binding vs live control).
- **R-feel (product):** does window-close binding make a worse game? `Provisional` advisory signal mitigates.

## Recommended next routes (post-refine)
1. `decision-gate` — ratify the 3 open items.
2. `sigil-development` / `task-session` — implement L0 kernel + the auto-verdict-gate fixture.
3. Update body-war Craft ledger `GAP-TROQAR-SCORE-AUTHORITY-001` after ratification (separate act).

## Certificate layer = Attestation L1 (reuse — do NOT reinvent)
The slice's "re-verifiable certificate" (and the **seal** the toy_game forced) IS an **attestation**:
`attest(resolution) → cert(zone,window,sealedClaimHashes,resolution)`; `verify(cert, claimed) → valid|tampered`.
Two-arm specimen: `verify(attest(r), r)=valid` AND `verify(attest(r), r+late-arrival)=tampered` — the
late-arriving in-window activity IS the negative control. Build-from-owned on the cav2
**attestation-capability** (`cyberAlchemy-v2/development/attestation-capability/`; L1 = attest+verify+specimen).
That sigil is scoped to cav2 acts, so body-war reuses the *pattern* (content-hash + `decidePolicy_sound`
template), not the literal sigil. **Sequence:** the certificate/verify layer waits on / reuses attestation L1
— do NOT hand-roll a second verifier (the toy_game already caught a vacuous guard here).

**"body-war as cross-domain witness" status: INTENDED, NOT BUILT** (claim ≤ proof). When the L0 kernel + the
reused verify ship, body-war becomes a *runnable* witness that the discriminating-verify pattern generalizes
beyond cav2. Until then it is a planned witness. It witnesses **verify-pattern generality** — a DIFFERENT
claim from the Mint N=3 foundry-H; it is NOT a 4th mint domain.
