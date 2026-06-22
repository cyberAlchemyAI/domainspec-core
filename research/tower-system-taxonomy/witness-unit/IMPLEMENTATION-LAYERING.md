---
module: tower-witness-unit
version: current
status: draft
updatedAt: 2026-06-18
docType: implementation-layering
invoke_mode: plan
---

# Implementation Layering: Tower System — Witness Unit

## Target And Scope

- Target: tower-witness-unit (a spell composing research-tower + robot-talks + net-new persona/scorer sub-sigils)
- Scope: capability (the smallest end-to-end proof of the Tower System architecture)
- Current state: greenfield (net-new C2 persona-builder, C4 scorer; C1/C3/C5 reuse)

## Layer Boundary Rule

```text
After this layer, we know whether {decision unlocked}.
```

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
|---|---|---|---|---|---|---|
| **P0 (predecessor) — MOGT evidence** (DEC-6) | After this phase, we know whether the owned MOGT decision/action-selection policy actually works (claims C1–C4 move off *insufficient evidence*). | run MOGT experiments E1→E2→E4→E3 (`arcanum/research/mogt-agentic-conversation/experiments/`). | MOGT's own experiment lifecycle (`experiment-harness`). | the tower's MOGT-backed decision layer (Phase 1). | C1–C4 evidence-status upgraded off *insufficient*. | proceed to tower L0 / revise MOGT / drop the reused decision layer. |
| **L0 (POC) — THIS UNIT** | After this layer, we know whether a graph-anchored persona can hold an opposable stance that produces a genuinely tensioned debate scored to a graded verdict (i.e. whether D1/D2/D3 are real, not vacuous). | The 5-step DDD trace: tower-graph → (P_A,P_B) → debate → oracle-consensus → graded verdict. | C1 fixture (3 nodes), C2 (D1 schema + D2 rule), C3 robot-talks adapter, C4 (D3 ELO + oracle-consensus), C5 verdict. One domain, one proposition, ≥3 judge votes. | recursion; persona library; read-through/promote construction; multi-domain; MOGT; production scoring. | the end-to-end trace + A1–A5 acceptance in WORK-PACK. | continue (build L1) / pivot (if D2 can't yield genuine tension) / stop. |
| L1 | After this layer, we know whether the unit is **repeatable** across nodes/propositions without per-case hand-tuning. | parametric persona-builder over the whole DDD graph + a small proposition set. | generalize C2/D2; persona library (store/retrieve). | other domains; scale. | ≥5 propositions auto-produce tensioned pairs + graded verdicts. | harden / narrow. |
| L2 | After this layer, we know whether **reliability/governance** holds (judge bias, ELO stability, degraded mode when consensus fails). | bias controls + ELO stability checks + human-flag path exercised. | scoring robustness; tension gate reuse. | scale/packaging. | stability + degraded-mode evidence. | scale / remediate. |
| L3 | After this layer, we know whether the unit **packages as a reusable spell** across domains (towers-in-towers, recursion). | spellcraft-packaged spell with ≥2 domains. | packaging; recursion. | future application modes (write/design/understand). | packaged spell + 2-domain demo. | pilot / package. |

## Non Regression Guardrails

- Later layers must preserve the L0 guarantee: every emitted verdict carries a **graded** confidence (not a bare majority count).
- Deferred scope stays explicit (recursion, library, MOGT-stays-dropped).
- Promotion L0→L1 must cite the A1–A5 evidence, not preference.

## Recommended Next Layer

- Next phase: **P0 — run MOGT experiments E1→E2** for evidence (DEC-6), *before* committing tower L0 build.
- Then **L0** (this unit) — build the witness pipeline.
- Key decision unlocked by P0: is the owned MOGT decision-policy layer worth reusing (evidence, not design-time reasoning)?
- Key decision unlocked by L0: are D1/D2/D3 real (architecture non-vacuous)?
- Major deferred scope: recursion, persona library, multi-domain, production scoring.
