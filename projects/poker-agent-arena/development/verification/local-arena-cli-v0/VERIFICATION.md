# Local Arena CLI v0 Verification

Date: 2026-06-20
Status: pass

## Scope

This verification covers the selected one-shot stream `SWU-PAA-001R` through
`SWU-PAA-004` for `Local Arena CLI v0` inside `projects/poker-agent-arena/`.

## Defaults Accepted

- Runtime root: `src/poker_agent_arena/`
- CLI namespace: `paa`
- Commands: `doctor`, `run`, `eval`, `replay`
- First fixture: `kuhn_hidden_info`
- Default decision timeout: `5000ms`
- Process cleanup timeout: `10000ms`
- Clock policy: monotonic timer after decision-envelope flush
- Fallback selector: `check`, `fold`, `call`, then minimum legal wager
- Public replay: seed handles only, no raw seed material
- MVP scoring: clean EV, fallback-inclusive EV, invalid rate, timeout rate,
  fallback count, replay determinism, canary and redaction results

## Commands Run

```sh
env PYTHONPATH=projects/poker-agent-arena/src python3 -m unittest discover -s projects/poker-agent-arena/tests
env PYTHONPATH=projects/poker-agent-arena/src python3 -m poker_agent_arena.cli doctor
env PYTHONPATH=projects/poker-agent-arena/src python3 -m poker_agent_arena.cli run --fixture kuhn_hidden_info --agent-a projects/poker-agent-arena/examples/agents/check_call.py --agent-b projects/poker-agent-arena/examples/agents/legal_random.py --seed-handle kuhn-smoke-000 --out projects/poker-agent-arena/.tmp/run-smoke
env PYTHONPATH=projects/poker-agent-arena/src python3 -m poker_agent_arena.cli eval --fixture kuhn_hidden_info --agent-a projects/poker-agent-arena/examples/agents/check_call.py --agent-b projects/poker-agent-arena/examples/agents/legal_random.py --out projects/poker-agent-arena/.tmp/smoke
env PYTHONPATH=projects/poker-agent-arena/src python3 -m poker_agent_arena.cli replay projects/poker-agent-arena/.tmp/smoke/private-transcript.jsonl --out projects/poker-agent-arena/.tmp/smoke/replay
env PYTHONPATH=projects/poker-agent-arena/src python3 -m poker_agent_arena.cli eval --fixture kuhn_hidden_info --agent-a projects/poker-agent-arena/examples/agents/invalid_json.py --agent-b projects/poker-agent-arena/examples/agents/check_call.py --decision-timeout-ms 200 --process-kill-after-ms 500 --max-hands 4 --out projects/poker-agent-arena/.tmp/invalid-smoke
env PYTHONPATH=projects/poker-agent-arena/src python3 -m poker_agent_arena.cli eval --fixture kuhn_hidden_info --agent-a projects/poker-agent-arena/examples/agents/timeout.py --agent-b projects/poker-agent-arena/examples/agents/check_call.py --decision-timeout-ms 100 --process-kill-after-ms 300 --max-hands 4 --out projects/poker-agent-arena/.tmp/timeout-smoke
env PYTHONPATH=projects/poker-agent-arena/src python3 -m poker_agent_arena.cli eval --fixture kuhn_hidden_info --agent-a projects/poker-agent-arena/examples/agents/crash.py --agent-b projects/poker-agent-arena/examples/agents/eof.py --decision-timeout-ms 200 --process-kill-after-ms 500 --max-hands 2 --out projects/poker-agent-arena/.tmp/crash-eof-smoke
```

## Outcomes

- Unit tests: pass, 4 tests.
- `doctor`: pass; required contracts, fixtures, and sample agents present.
- `run`: pass; single Kuhn match wrote transcript and diagnostics.
- `eval`: pass; 12-hand seat-rotated smoke orbit wrote private transcript and
  diagnostics.
- `replay`: pass; private transcript replayed with no payout mismatches and
  exported redacted public replay.
- Hidden-information canary: pass; generated decision envelopes contained no
  forbidden live fields.
- Public replay redaction: pass; no `raw_seed`, `deck_order`, `opponent_card`,
  `future_state`, `referee_trace`, or `hidden_state_hash` appeared in public
  replay or public diagnostics.
- Invalid JSON fixture: pass; produced `prose_before_json` fallback diagnostics.
- Timeout fixture: pass; produced `timeout` fallback diagnostics.
- Crash and EOF fixture: pass; produced named `crash` and `eof` fallback
  diagnostics.
- Fallback abuse check: pass for bundled smoke fixtures.

## Artifacts Created

- `spec/l0/`
- `src/poker_agent_arena/`
- `fixtures/l0/`
- `examples/agents/`
- `tests/test_local_arena_cli.py`
- `pyproject.toml`

## Deferred Work

- Leduc board reveal remains post-MVP.
- Hold'em engine parity remains post-MVP.
- Calibrated leaderboard and novelty mechanics remain post-MVP.
