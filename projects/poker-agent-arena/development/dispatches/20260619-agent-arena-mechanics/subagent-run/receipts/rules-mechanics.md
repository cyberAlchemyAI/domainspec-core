# Rules/Mechanics Receipt

- dispatch_id: 2026-06-19-poker-agent-arena-mechanics
- role_id: rules-mechanics
- spawn_status: spawned
- join_status: completed
- close_status: closed
- status: flag
- step_id: s2-fanout-lanes
- capability_ref: task-session

## Proposed mechanics

Baseline game: no-limit Texas Hold'em cash-hand semantics, initially 2-6 seats, with deterministic table configuration: seat count, button seat, small blind, big blind, ante if any, starting stack per seat, timeout policy, and hand seed held only by the engine. MVP should start with heads-up and 6-max fixtures before tournament movement or multi-table play.

Hand lifecycle:

1. Initialize active seats with nonzero stacks; assign button by configured rotation.
2. Post forced bets. Heads-up: button posts small blind and acts first preflop; big blind acts first after the flop. Multiway: first live seat left of big blind acts preflop; first live seat left of button acts postflop.
3. Deal private hole cards only to each owning player.
4. Run betting rounds: preflop, flop, turn, river. Burn/deal behavior may be delegated to the local engine, but observations must expose only public board cards after they are dealt.
5. End a round when every non-folded, non-all-in player has either matched the current bet or has no legal response pending.
6. If only one non-folded player remains, award all pots that player can win and end immediately.
7. If at least two players remain after river betting, reveal only showdown-eligible hands, rank by standard Hold'em best five of seven, and award main and side pots.

Legal actions per decision:

- `fold`: legal only facing a bet or raise. If checking is free, timeout fallback should prefer check, not fold.
- `check`: legal only when call amount is zero.
- `call`: legal when call amount is positive; if stack is less than call amount, it is an all-in call for the remaining stack.
- `bet`: legal when no bet exists in the round; amount must be at least big blind or remaining stack if smaller, and no more than stack.
- `raise`: legal facing a bet; total commitment must be at least previous bet plus the last full raise increment unless the player is all-in for less. Short all-in raises do not reopen action for players who have already acted unless they meet the full-raise threshold.

All-in and pot contract:

- A player may never commit more chips than their stack.
- All-in players stay eligible only for pots capped by their contributed amount.
- Side pots are layered by contribution thresholds among players who have not folded for each pot.
- Folded players forfeit eligibility for every pot, but their committed chips remain in the pot.
- Uncalled excess bet chips are returned to the bettor before pot distribution.
- Odd chips require a deterministic rule; MVP should choose one explicit rule, preferably first eligible seat left of the button for that pot.

Hidden-information boundary:

- Public observation: button, blinds, stacks, committed chips, current street, public board, pot summaries, action history with public amounts, legal action list, acting seat, and deadline.
- Private observation: only the acting agent's own hole cards and its own previous private messages/state if the protocol supports memory.
- Forbidden observation: undealt deck, random seed, future board cards, other live players' hole cards before legal showdown exposure, folded mucked cards unless explicitly shown, engine internals that imply hidden card order, and other agents' private reasoning.

Timeout and invalid-action fallback:

- Timeout, malformed output, illegal action, or amount outside legal bounds must resolve to a deterministic legal fallback.
- Recommended fallback order: check if legal; otherwise call if legal and configured as non-punitive; otherwise fold. For strict competition mode, illegal output may add a scoring penalty while the game action still follows the legal fallback.
- The fallback must be computed from the engine legal-action set at the moment of decision, not from agent-supplied intent.

Engine compatibility:

- The arena should treat PokerKit or any local engine as an authority for state transition and hand ranking, while the arena owns the observation filter, action schema, timeout policy, reproducible configuration, and scoring hooks.
- Do not fork game truth between custom arena logic and engine state. If the engine cannot express a proposed rule, downgrade that rule to residue or add a toy fixture before adopting it.

## Toy-game checks needed

- Heads-up preflop blind/action-order fixture: button posts small blind, acts first preflop, and acts last postflop.
- Multiway action-order fixture: first live seat left of big blind preflop, first live seat left of button postflop, skipping folded/all-in seats.
- Legal-action matrix fixture for check, bet, call, fold, min-raise, all-in short call, all-in short raise, and full raise reopening action.
- Side-pot fixture with three players and uneven stacks, including a folded contributor and uncalled bet return.
- Showdown fixture with tied best hands and odd-chip distribution.
- Hidden-information fixture proving each agent sees only its hole cards, public board, public action, legal actions, and no deck/seed/future-card data.
- Timeout fixture proving the fallback is legal on free-check, facing-bet, and all-in-short-stack states.
- Engine parity fixture comparing arena observations and pot results against the selected local engine on a small deterministic hand corpus.

## Risks/blockers/residue

- Risk: no-limit min-raise and short all-in reopen rules are easy to implement incorrectly. Carry as mandatory fixture coverage.
- Risk: side-pot accounting can silently diverge from engine truth. The arena should not hand-roll pot settlement unless engine parity tests exist.
- Risk: hidden information can leak through action history, logs, debug state, random seeds, or serialized engine objects. Observation serialization needs an allowlist, not a denylist.
- Risk: timeout fallback can become a strategy exploit if penalties and time banks are scoring-only afterthoughts. Scoring/economy should own penalties; rules/mechanics should only guarantee a legal game action.
- Residue: tournament eliminations, table balancing, antes, straddles, run-it-twice, bomb pots, and novelty mechanics are out of MVP baseline.
- Residue: exact odd-chip convention and muck/show rules must be chosen before executable fixtures are frozen.

## Handoff_note

This lane proposes a conservative, engine-compatible no-limit Hold'em contract. It should be safe for parent synthesis as a baseline, but it is flagged until toy-game fixtures prove action ordering, min-raise/reopen behavior, side pots, hidden-information filtering, and timeout fallback legality.
