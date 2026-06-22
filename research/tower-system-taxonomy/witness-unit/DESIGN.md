---
module: tower-witness-unit
version: current
status: draft
updatedAt: 2026-06-18
docType: design
invoke_mode: design
profile: architecture (six-view)
upstream: research/tower-system-taxonomy/witness-unit/SPEC.md
---

# DESIGN: Tower System — Witness Unit (six-view)

Non-mutating design over the approved define outputs (SPEC.md, GLOSSARY.md). Upstream corrections are recorded as gaps, not silent edits.

## 1. Context view

```
                  ┌─────────────────────────── Tower Witness Spell ───────────────────────────┐
   author/human ─►│  build tower fixture → instantiate personas → run debate → score → verdict │─► graded verdict
        (gate) ◄──│                                   (human gate inside debate, robot-talks)   │
                  └────────────┬───────────────┬───────────────┬───────────────┬───────────────┘
                     research-tower      persona+graph      robot-talks     scoring substrate
                     (source content)    (net-new)          (reuse)         (net-new D3)
```
Actors: the human (seeds fixture, sits the debate gate, reads the verdict). External owners reused: research-tower, robot-talks, the subagents constitution's verdict schema. The unit is a **spell** composing these; net-new pieces become candidate sub-sigils.

## 2. High-level structure view

Five components, one linear pipeline (the assembly; integration pattern = blackboard, findings R1):

| Component | Kind | Source |
|---|---|---|
| C1 Tower-graph | net-new object over reuse | research-tower content + queryable graph object |
| C2 Persona-builder | net-new sub-sigil (D1+D2) | new |
| C3 Debate-runner | reuse | robot-talks |
| C4 Scorer | net-new sub-sigil (D3) | new (ELO + oracle-consensus) |
| C5 Verdict-emitter | reuse | research verdict schema |

## 3. Low-level components view

- **C1 Tower-graph.** `Node{id,label,type,def}`, `Edge{from,to,type}`. Query surface: `nodes(type?)`, `neighbors(id, edge_type?)`. Fixture: 3 nodes + 2 edges (DDD).
- **C2 Persona-builder.** Implements D1 schema `Persona{anchor, stance, criteria, voice?, provenance[]}` and D2 rule `stance(node, proposition) → position`. Emits a tensioned pair `(P_A, P_B)` given a proposition + two related nodes.
- **C3 Debate-runner.** Adapter over robot-talks: input `(P_A, P_B, proposition)`, output `{position_A, position_B, disagreement_axis}` + human gate.
- **C4 Scorer.** `RatingStore{rating[persona], K}`; `oracle_consensus(votes[], ratings) → {outcome, confidence, layer_resolved}` via ladder L1 unanimous(≥0.9)→L2 supermajority(≥0.66)→L3 ELO-weighted→L4 human-flag(<0.45). Updates ratings after resolution.
- **C5 Verdict-emitter.** `Verdict{proposition, outcome, confidence, route}` from C4 output; confidence = graded score.

## 4. Workflow process view

`seed fixture → build (P_A,P_B) [C2] → run debate [C3, human gate] → collect ≥3 judge votes → oracle_consensus [C4] → emit verdict [C5]`. One pass; no recursion in the witness unit.

## 5. Decision flow view

| Decision point | Branch | Resolution |
|---|---|---|
| Is the persona pair genuinely opposable? | yes → debate; no → re-pick nodes/proposition | D2 rule + reviewer check (A3) |
| Consensus layer reached? | L1/L2 → resolve; L3 → ELO-weighted; L4 → human-flag | thresholds in C4 |
| Confidence graded? | yes → verdict; no (degenerated to majority) → fail A4 | D3 must execute layers 2–3 |

## 6. Dependency interface view

```
C1 ──(nodes/edges)──► C2 ──(P_A,P_B)──► C3 ──(positions)──► C4 ──(outcome,confidence)──► C5
                       ▲ D2 rule          │ robot-talks      │ ELO store (D3)
                       │ D1 schema         human gate         threshold (D3)
research-tower ────────┘                                     anti-bias principle (tension only)
```
Hard dependencies: C2→C1 (needs nodes), C4→C3 (needs positions/votes), C5→C4. C3 reuses robot-talks as-is. No cross-repo dependency (all in the new spell + reused sigils).

## Glossary consistency report

| Term | SPEC/GLOSSARY status | Consistency | Note |
|---|---|---|---|
| Persona | candidate | pass | design uses graph-anchor + stance, matches D1; not "saved angle" |
| Opposable-stance rule | candidate | pass | C2 implements D2 as named |
| Oracle-consensus | candidate | pass | C4 ladder matches glossary; thresholds now concretized (0.9/0.66/0.45) — **flag**: thresholds are design proposals, confirm in plan |
| ELO substrate | candidate | pass | C4 RatingStore matches D3 |
| Dispatch / application | linked / dropped-label | pass | design avoids "application", uses the debate dispatch |
| MOGT | dropped | pass | absent from design (correct) |

Consistency: **pass with one flag** (threshold values are design-proposed, not yet confirmed).

## Design decisions

- DD-1: pipeline is linear and single-pass for the witness unit (recursion deferred).
- DD-2: C2 and C4 are the net-new sub-sigils; C1/C3/C5 are reuse/thin-adapters. This isolates D1/D2 (C2) and D3 (C4) as the only real build risk.
- DD-3: oracle-consensus thresholds proposed at L1≥0.9 / L2≥0.66 / L4<0.45 (proposal; confirm in plan).
- DD-4: MOGT (owned, `arcanum/research/mogt-agentic-conversation/`) is a **deferred** decision/action-selection layer — *not* part of the witness pipeline (which scores via oracle-consensus, not MOGT). It is sequenced **before** the tower build for its evidence (SPEC Sequencing, DEC-6). Debate (C3) and tower content (C1) are **OWN-PRIOR-WORK** reuse (executed in-repo), not external — per [../PRECEDENT-RECHECK.md](../PRECEDENT-RECHECK.md).

## Risks

- R-1 (high): D2 (node→opposable-stance) is the hardest unproven piece — if adjacency can't be turned into genuine tension, the debate is vacuous (findings R2). Mitigate: design the rule around the *contested proposition*, not node adjacency alone.
- R-2 (med): ELO substrate with only ~3 judges per query is statistically thin — acceptable for a witness, not for production.
- R-3 (med): the MOGT layer the tower will later reuse is owned but **unproven** (0 live runs). Mitigated by DEC-6: run MOGT's E1–E4 for evidence *before* the tower commits to reusing it.

## Next route

`invoke plan` → implementation-layering + work-pack with SWUs for C1–C5, D1/D2/D3 as the core specs.
