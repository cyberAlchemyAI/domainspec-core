# Poker Agent Arena MVP Path

Status: MVP runtime proof pass
Selected route: `local-arena-cli-v0` (`Local Arena CLI v0`)
Purpose: keep the executable MVP line and its verification evidence visible.

## Definition Of MVP

The MVP is a local CLI arena that can run a Kuhn hidden-information fixture end to end against agent processes, produce private transcript material, export a redacted public replay, replay the match deterministically, and report raw performance plus protocol diagnostics.

MVP is not a complete poker platform. It is the first runnable proof that the arena contract is strict, fair, debuggable, and hard to game through invalid output or timing behavior.

## The One Line

1. Repair the handoff: make the route, gaps, defaults, and output tree explicit.
2. Freeze the contract: write versioned `spec/l0/` files for runtime, protocol, transcript, fixtures, diagnostics, deadline, and fallback.
3. Implement the local runner: spawn agents, send decision envelopes, parse action envelopes, enforce deadlines, and run the Kuhn referee.
4. Prove replay and diagnostics: reproduce payouts and events, redact public replay, and report clean EV beside invalid/timeout/fallback metrics.
5. Prove author usability: ship sample agents, failing fixtures, JSON examples, diagnostics examples, and quickstart commands.

That is the MVP stream. Leduc, Hold'em engine parity, adjusted scoring, and novelty mechanics are staged after this line passes.

## Execution Status

`SWU-PAA-001R` through `SWU-PAA-004` have passed for the local MVP proof slice.
The runtime now includes:

- versioned `spec/l0/` contracts,
- `src/poker_agent_arena/` Python runtime,
- `paa doctor`, `paa run`, `paa eval`, and `paa replay` through `python -m`,
- Kuhn hidden-information fixture orbit,
- private transcript JSONL,
- deterministic replay,
- redacted public replay export,
- diagnostics for clean EV, fallback-inclusive EV, invalid rate, timeout rate,
  fallback count, replay determinism, canary, and redaction checks,
- friendly and adversarial sample agents,
- unittest coverage and smoke verification.

Durable verification: `development/verification/local-arena-cli-v0/VERIFICATION.md`.

## Recommended Decisions

These defaults are accepted for Local Arena CLI v0.

| Decision | Recommendation |
| --- | --- |
| Runtime language/root | Python package under `src/poker_agent_arena/` |
| CLI namespace | `paa` |
| CLI commands | `paa doctor`, `paa run`, `paa eval`, `paa replay` |
| First fixture gate | Kuhn hidden information |
| Decision timeout | `5000ms` |
| Process cleanup timeout | `10000ms`; cleanup only, not accepted action time |
| Clock | Monotonic clock |
| Deadline start | After arena flushes the decision envelope to agent stdin |
| Deadline stop | First complete stdout JSON object |
| Late output | Timeout event; ignore for gameplay; clean up process at cleanup timeout |
| Fallback | Passive deterministic legal action order: `check`, `fold`, `call`, then minimum legal wager action |
| MVP scoring | Clean EV, fallback-inclusive EV, invalid rate, timeout rate, fallback count, replay determinism |

## Hard MVP Acceptance

The route is MVP-complete only when all of these are true:

- A fresh checkout can run the author quickstart without hidden local assumptions.
- `paa doctor` reports the local environment and fixture availability.
- `paa eval` can run bundled sample agents through the Kuhn fixture.
- Agent-visible observations never include opponent card, raw seed, deck order, future card, referee trace, or reversible hidden-state hash.
- Invalid output, timeout, crash, and EOF cases produce named diagnostics and deterministic fallback.
- `paa replay` reproduces accepted actions, fallback events, diagnostics, and payouts from private transcript material.
- Public replay export is redacted according to `spec/l0/transcript/redaction-policy.md`.
- Diagnostics report clean EV and fallback-inclusive EV separately.
- Abuse fixture agents cannot improve displayed rank through timeout or invalid-output behavior.

## Closed MVP Gaps

| Gap | Status | Closing Artifact |
| --- | --- | --- |
| Runtime root | closed | `src/poker_agent_arena/`, `pyproject.toml` |
| CLI commands | closed | `spec/l0/runtime/cli.md`, `src/poker_agent_arena/cli.py` |
| Match config schema | closed | `spec/l0/runtime/match-config.md` |
| Process lifecycle | closed | `spec/l0/runtime/process-lifecycle.md`, `runner/agent_process.py` |
| Decision/action examples | closed | `spec/l0/protocol/*.md`, `docs/AGENT-AUTHOR-GUIDE.md` |
| Fallback selector | closed | `spec/l0/protocol/fallback-policy.md`, runtime fallback tests |
| Timing defaults | closed | `spec/l0/protocol/deadline-policy.md`, timeout fixture smoke |
| Invalid-output matrix | closed | `fixtures/l0/invalid_output_matrix/cases.json`, invalid/crash/EOF smokes |
| Kuhn fixture oracle | closed | `fixtures/l0/kuhn_hidden_info/`, replay determinism check |
| Private/public transcript split | closed | `spec/l0/transcript/`, `replay/public-replay.json` smoke |
| Diagnostics schema | closed | `spec/l0/diagnostics/`, diagnostics report smoke |
| Sample agents | closed | `examples/agents/` |

## Post-MVP Decision Points

The remaining decisions no longer block Local Arena CLI v0:

- Leduc board reveal as the first post-MVP expansion.
- Hold'em engine choice for M1.
- Calibrated leaderboard scoring and confidence-bound ranking.
- Time-credit or other novelty mechanics outside primary ranking.
