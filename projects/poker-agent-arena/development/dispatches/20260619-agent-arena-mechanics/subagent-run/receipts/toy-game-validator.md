---
dispatch_id: 2026-06-19-poker-agent-arena-mechanics
role_id: toy-game-validator
agent_id: simon-herbert-explorer
spawn_status: spawned
join_status: completed
close_status: closed
status: pass
step_id: s3-toy-game-fixtures
capability_ref: task-session
observer_status: receipt-only-design
artifacts:
  - projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/subagent-run/receipts/toy-game-validator.md
validation: "Fixture design only. No engine execution or scoring run is claimed."
blockers: []
reroute: none
---

# Toy-Game Validator Receipt

## Scope

Design small deterministic fixtures that can validate arena mechanics before a full no-limit Hold'em engine exists. The fixtures below avoid full hand evaluation where possible: they use Kuhn, Leduc, fixed showdown ranks, scripted agents, and frozen seeds. Each fixture should emit enough evidence to diagnose legal-action handling, hidden-information boundaries, clock behavior, invalid output behavior, pot accounting, score variance, adaptation, and exploitability.

## Fixture List

1. **Kuhn Hidden-Info Smoke**
   - Game: two-player Kuhn poker, J/Q/K deck, one private card each, ante 1, one betting round.
   - Tests: private observations, legal actions, fold/call/showdown flow, deterministic chance seed.
   - Evidence: per-seat observation JSON without opponent card or undealt card; legal-action mask each turn; full state trace available only to referee; final payoff and showdown reveal timing.

2. **Leduc Two-Street State Boundary**
   - Game: two-player fixed-limit Leduc with paired J/Q/K deck, one private card, one public board card, fixed bet sizes.
   - Tests: transition from private-only to public-card state, round reset, legal raises, public/private namespace.
   - Evidence: before/after observation diffs at board reveal; round index; pot and contribution ledger; state hash proving hidden cards did not enter agent observations.

3. **Invalid Action Matrix**
   - Game: minimal single-street betting state with scripted faulty agents.
   - Tests: malformed JSON, unknown action, out-of-turn action, impossible bet size, action after terminal state, hidden-field echo attempts.
   - Evidence: error code per invalid output; fallback action selected by rules; penalty applied; unchanged canonical state hash after rejected actions; transcript proving no hidden echo is rewarded.

4. **Clock And Time-Bank Fixture**
   - Game: deterministic betting loop with one fast scripted agent and one slow/late scripted agent.
   - Tests: per-turn deadline, reserve time-bank debit, timeout fallback, match-level exhaustion.
   - Evidence: monotonic receive/send timestamps; deadline_ms supplied to agent; timeout decision; remaining time-bank after each turn; latency stats and terminal reason.

5. **Three-Seat All-In Pot Accounting**
   - Game: toy three-player hand with fixed ranks and stack sizes that force main pot plus side pot.
   - Tests: all-in legality, contribution caps, side-pot eligibility, folded player exclusion, chip conservation.
   - Evidence: contribution table by street; pot-layer table with eligible seats; refund rows; payout rows; invariant check `sum(starting_stacks) == sum(ending_stacks)`.

6. **Seat-Swapped Variance Scoring**
   - Game: repeated Kuhn/Leduc seeds where each agent plays both seats for every seed.
   - Tests: chance variance control, score aggregation, tie-breakers, separation between chip result and arena score.
   - Evidence: seed-pair result table; seat-normalized EV; ROI/window score; variance estimate; deterministic tie-break result when aggregate score matches.

7. **Adaptation Ladder**
   - Game: fixed-limit toy opponent changes policy after a known hand count: passive phase, aggressive phase, trap phase.
   - Tests: whether an agent adapts from public history only, and whether scoring can recognize adaptation without leaking the policy switch.
   - Evidence: phase-tagged action frequencies; rolling EV; adaptation latency after switch; observation transcript showing no private phase label was sent.

8. **Exploitability Oracle**
   - Game: tiny Kuhn policy evaluator with enumerable best response, plus optional Leduc-lite extension later.
   - Tests: exploitability metric, degenerate always-bet/always-fold strategies, baseline policy regression.
   - Evidence: submitted policy/action table; best-response value; exploitability score; comparison to frozen baseline policies; seed-independent reproducibility log.

9. **Information-Leak Canary**
   - Game: any above fixture with referee-only canary fields attached to hidden state.
   - Tests: serialization boundary and logging discipline.
   - Evidence: agent observation snapshots do not contain canary keys or values; public logs redact referee-only state; failure fixture proves the detector catches an injected leak.

## Risks, Blockers, Residue

- **Risk:** A toy all-in fixture can validate pot layers and chip conservation, but not full no-limit betting complexity. Carry this as residue for the Hold'em engine.
- **Risk:** Adaptation evidence can show behavior changes after public history changes; it cannot prove strategic understanding.
- **Risk:** Exploitability is tractable for Kuhn and maybe small Leduc, not for full no-limit Hold'em. Keep the oracle scoped to tiny games.
- **Risk:** Timing fixtures depend on stable local scheduler behavior. Evidence should tolerate small timing jitter while still hard-failing missed deadlines.
- **Blockers:** none for fixture design. Implementation should block if the protocol cannot emit legal-action masks, deadline metadata, state hashes, and referee-only traces.
- **Residue:** map every accepted arena mechanic to at least one fixture above before calling the mechanics package implementation-ready.

## Handoff Note

Build these as a deterministic fixture harness before the poker engine. Freeze a minimal transcript schema with `seed`, `hand_id`, `seat`, `observation`, `legal_actions`, `deadline_ms`, `action`, `error_code`, `state_hash`, `pot_layers`, and `payouts`. Treat fixture success as evidence that the arena contract is coherent, not evidence that full no-limit Hold'em is implemented or balanced.
