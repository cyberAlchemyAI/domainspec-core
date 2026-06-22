---
dispatch_id: 2026-06-19-poker-agent-arena-mechanics
role_id: novelty-lane
agent_id: feyerabend-paul-explorer
spawn_status: spawned
join_status: completed
close_status: closed
status: pass
step_id: s5-novelty-tournament
capability_ref: distill
observer_status: receipt-only-design
artifacts:
  - projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/subagent-run/receipts/novelty-lane.md
validation: "Novelty proposal only. No engine run, tournament run, or exploitability proof is claimed."
blockers: []
reroute: none
---

# Novelty Lane Receipt

## Lane Frame

Proposed lane: **agent-native resource and adaptation mechanics**. Keep the poker hand fair and orthodox, but wrap it in measurable constraints that agents uniquely care about: compute time, observation bandwidth, memory across rounds, compact explanations, and transfer across small imperfect-information games. Hidden cards, deck order, seeds, future board cards, and opponent private reasoning remain referee-only.

## Ranked Ideas

| Rank | Idea | Novelty | Implementability | Testability | Cleverness Signal | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | **Time-bank market** | 5 | 4 | 5 | 5 | Each agent starts with match-level clock credits. Before a hand or street, agents may spend credits for longer deadlines or sell unused reserve for score. Bids are public, deterministic, and cannot depend on hidden engine state. Signal: knowing when a spot is worth deeper search. |
| 2 | **Observation bandwidth draft** | 5 | 3 | 4 | 5 | Instead of always receiving the full safe observation, an agent allocates fixed bandwidth among public-history detail, stack/pot detail, opponent timing summaries, and own-card/action affordances. All categories are filtered safe fields. Signal: strategic state abstraction under pressure. |
| 3 | **Memory/adaptation ladder** | 4 | 4 | 5 | 5 | Run seed-paired blocks with cold-start, retained-memory, and opponent-policy-shift phases. Score the delta between static competence and adaptation from public history only. Signal: learning without privileged labels. |
| 4 | **Mixed toy-game ladder** | 4 | 5 | 5 | 4 | Same protocol, agents, clocks, and scoring across Kuhn, Leduc, single-street hold'em, short-stack all-in hold'em, then full hold'em. Signal: robust imperfect-information reasoning rather than overfit one game. |
| 5 | **Explanation tax** | 4 | 3 | 3 | 4 | For selected high-impact actions, require an optional compact rationale field that costs tokens/time/score but is logged for audit. MVP should not use semantic judging for score; it should measure cost discipline and enable later review. |
| 6 | **Counterfactual mirror seats** | 3 | 4 | 4 | 3 | Replay strategically equivalent public states with seat swaps, stack mirrors, or scripted opponent variants. Compare action distributions and EV. Signal: consistency and exploit selection, not just lucky outcomes. |
| 7 | **Adversarial observation compression challenge** | 5 | 2 | 3 | 5 | A separate challenge where agents submit a deterministic compressor for their own observations, then play using only the compressed view. Powerful, but riskier than the bandwidth draft because bad compressors can make failures hard to interpret. |

## Recommended Wild-Card

Adopt the **time-bank market** as the safest first novelty mechanic. It is agent-native, cheap to fixture, reproducible, and does not alter poker legality. Keep credits outside chip stacks: chip EV remains poker score, while arena score adds a small time-efficiency component. Tie-break credit auctions deterministically by seat order or hand id hash, never by wall-clock race.

## Toy-Game Checks Needed

- Kuhn clock-credit fixture: both agents receive identical starting credits, bid for extra time before each decision, and replay yields identical deadlines and credit balances.
- Leduc bandwidth fixture: each bandwidth category serializes only allowlisted public fields plus own private card; canary hidden fields never enter compressed observations.
- Adaptation ladder fixture: scripted opponent changes public policy after a fixed hand count, but no phase label is sent; evidence reports rolling EV and adaptation latency.
- Mixed-game protocol fixture: the same agent process handles Kuhn, Leduc, and short-stack hold'em envelopes without schema drift.
- Explanation-tax fixture: rationale text is accepted, capped, timestamped, and ignored by game state; malformed rationale cannot invalidate an otherwise legal action unless stdout JSON is malformed.
- Mirror-seat fixture: seed-paired states swap seats and blinds; scoring separates chance correction from strategic action differences.

## Risks/Blockers/Residue

- Risk: time-bank markets can become an optimization contest over scheduler jitter. Use monotonic engine timestamps, deterministic deadlines, and generous IO grace.
- Risk: observation bandwidth can accidentally penalize simple agents by hiding legally necessary fields. Legal actions must always remain authoritative and complete.
- Risk: memory ladders can reward contamination if agents retain hidden referee traces. Persist only agent-owned state and public transcripts; never expose full referee logs to agents.
- Risk: explanation tax becomes subjective if natural-language quality affects score. Keep semantic explanation review audit-only until a deterministic rubric exists.
- Risk: mixed toy-game ladders may over-reward generality before baseline hold'em competence is stable. Use as a side leaderboard first.
- Residue: exact credit pricing, per-hand credit reset policy, bandwidth categories, and adaptation scoring windows need the scoring/economy lane.
- Residue: exploitability skeptic should attack credit hoarding, intentional timeouts, compressor-induced blind spots, and explanation spam.

## Handoff_note

Parent synthesis can safely carry **time-bank market** as the first candidate wild-card mechanic, with bandwidth draft and memory/adaptation ladder as next-tier experiments. Claim only design readiness: every accepted novelty must map to a toy fixture and must preserve public-plus-own-private observation boundaries before entering the main rules package.
