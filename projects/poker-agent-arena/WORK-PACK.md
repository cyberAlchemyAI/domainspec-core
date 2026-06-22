# Poker Agent Arena Work Pack

Status: MVP runtime proof pass
Source evidence:

- `development/refinement-runs/20260619T143102Z-mvp-design/review-dispatch/findings.md`
- `development/refinement-runs/20260619T143102Z-mvp-design/IMPLEMENTATION-STREAM.md`
- `NAMING.md`
- `MVP-PATH.md`

## Control Fields

- `workPackId`: `WP-PAA-001`
- `workPackName`: `Local Arena CLI v0 Work Pack`
- `workPackGateStatus`: `local-arena-cli-v0-mvp-proof-pass`
- `complexity`: `medium`
- `outputMode`: `one-implementation-stream`
- `activeLayerWindow`: `L0R -> L4 complete for local proof`
- `nextRoute`: `post-mvp expansion planning`
- `nextSWU`: `none`

## Objective

Turn the Poker Agent Arena planning packet into one executable MVP path: `Local Arena CLI v0`, a local command-line arena that can run a Kuhn hidden-information fixture end to end with strict protocol, deadlines, deterministic fallback, transcript replay, diagnostics, sample agents, and author-facing first-run proof.

The route is not "Kuhn as the product." Kuhn is the first fixture gate inside the durable local arena surface. Leduc, Hold'em engine parity, calibrated leaderboard scoring, and novelty mechanics are follow-on work after this line proves itself.

## Non-Goals

- Do not implement full no-limit Hold'em before Local Arena CLI v0 passes.
- Do not require Leduc for the first MVP acceptance gate.
- Do not expose hosted public matchmaking, real-money play, deposits, or withdrawals.
- Do not enable composite `arena_score` or adjusted leaderboard ranking before calibration fixtures.
- Do not let novelty mechanics affect primary Local Arena CLI v0 ranking.
- Do not treat documentation-only completion as runtime MVP acceptance.

## One Implementation Stream

No parallel implementation streams are active. Every next task should advance this line or explicitly unblock it.

| Step | Unit | Scope | Exit Evidence |
| --- | --- | --- | --- |
| 0 | `SWU-PAA-001R` | Repair the handoff and freeze the one-stream MVP path. | Root artifacts point to `Local Arena CLI v0`; gaps, blockers, runtime root, CLI shape, timing recommendation, fallback recommendation, and fixture ownership are visible. |
| 1 | `SWU-PAA-001` | Freeze the versioned Local Arena CLI v0 contract. | `spec/l0/` protocol, runtime, transcript, state namespace, fixture, invalid-event, deadline, fallback, and diagnostics files exist with examples. |
| 2 | `SWU-PAA-002` | Implement the local CLI runner and Kuhn fixture gate. | `paa doctor`, `paa run`, and `paa eval` can execute sample agents on the Kuhn fixture and write a private transcript. |
| 3 | `SWU-PAA-003` | Add replay, redaction, and diagnostics acceptance. | `paa replay` reproduces payouts, fallback events, invalid/timeout diagnostics, and redacted public replay output. |
| 4 | `SWU-PAA-004` | Add author proof and fixture agents. | A new agent author can run the quickstart, see canonical JSON examples, and debug invalid/timeout output with sample diagnostics. |

MVP acceptance for the local proof slice is reached. Leduc board reveal becomes the first post-MVP expansion, not a hidden prerequisite.

## Execution Result

`SWU-PAA-001R` through `SWU-PAA-004` passed on 2026-06-20. Durable evidence is
recorded in `development/verification/local-arena-cli-v0/VERIFICATION.md`.

The runtime now provides:

- `spec/l0/` contracts and fixture descriptions,
- `src/poker_agent_arena/` Python runtime,
- `paa doctor`, `paa run`, `paa eval`, and `paa replay` through the module CLI,
- Kuhn hidden-information smoke orbit,
- private transcript JSONL and deterministic replay,
- redacted public replay export,
- diagnostics for clean EV, fallback-inclusive EV, invalid rate, timeout rate,
  fallback count, replay determinism, hidden-information canary, and public
  replay redaction,
- friendly and adversarial sample agents,
- unittest and smoke verification.

## Refine Recommendations To Accept Or Override

| Decision | Recommendation | Why It Matters |
| --- | --- | --- |
| Runtime root | `src/poker_agent_arena/` | Gives task-session a concrete package boundary instead of inventing one during implementation. |
| CLI command namespace | `paa doctor`, `paa run`, `paa eval`, `paa replay` | Covers environment checks, one match, fixture evaluation, and deterministic replay without overbuilding a service. |
| Default decision timeout | `decision_timeout_ms=5000` | Makes deadline discipline meaningful while still realistic for local agent processes. |
| Process cleanup timeout | `process_kill_after_ms=10000` | A late process can be cleaned up without accepting a late action. Any action after 5s is already a timeout. |
| Clock policy | monotonic clock; start after arena write flush; stop at first complete stdout JSON object | Keeps timeout behavior replayable and inspectable. |
| Fallback selector | Passive deterministic order: `check`, then `fold`, then `call`, then minimum legal wager action by rule-defined order | Keeps a hand alive while making fallback a poor competitive strategy. |
| Scoring surface | clean EV, fallback-inclusive EV, invalid rate, timeout rate, fallback count, replay determinism | Prevents raw EV from hiding protocol abuse. |

These recommendations are accepted runtime defaults for Local Arena CLI v0.

## Required Output Tree Before MVP Acceptance

```text
projects/poker-agent-arena/
  spec/l0/runtime/
    cli.md
    match-config.md
    process-lifecycle.md
    output-layout.md
  spec/l0/protocol/
    decision-envelope.md
    action-envelope.md
    legal-actions.md
    invalid-events.md
    deadline-policy.md
    fallback-policy.md
  spec/l0/transcript/
    referee-transcript.md
    public-replay.md
    redaction-policy.md
  spec/l0/diagnostics/
    report-schema.md
    scoring-surface.md
  spec/l0/fixtures/
    kuhn-hidden-info.md
    invalid-output-matrix.md
    timeout-fallback.md
    fallback-abuse.md
    leak-canary.md
  spec/l0/state-namespaces.md
  src/poker_agent_arena/
    cli.py
    runner/
    protocol/
    games/kuhn.py
    referee/
    transcript/
    replay/
    diagnostics/
  examples/agents/
    check_call.py
    legal_random.py
    timeout.py
    invalid_json.py
  fixtures/l0/
    kuhn_hidden_info/
    invalid_output_matrix/
    timeout_fallback/
    fallback_abuse/
    leak_canary/
```

`examples/agents/` is friendly onboarding material. `fixtures/l0/` owns adversarial validation material. Do not collapse those roles.

## Gap And Blocker Ledger

| Gap | Status | Closing Artifact |
| --- | --- | --- |
| Runtime root | closed | `src/poker_agent_arena/`, `pyproject.toml` |
| CLI command contract | closed | `spec/l0/runtime/cli.md`, `src/poker_agent_arena/cli.py` |
| Match config schema | closed | `spec/l0/runtime/match-config.md` |
| Decision/action examples | closed | `spec/l0/protocol/*.md`, `docs/AGENT-AUTHOR-GUIDE.md` |
| Fallback selector | closed | `spec/l0/protocol/fallback-policy.md`, runtime fallback selector |
| Timing defaults | closed | `spec/l0/protocol/deadline-policy.md`, timeout smoke |
| Invalid-output matrix | closed | `fixtures/l0/invalid_output_matrix/cases.json`, invalid/crash/EOF smokes |
| Kuhn fixture oracle | closed | `fixtures/l0/kuhn_hidden_info/`, replay determinism smoke |
| Replay/private/public split | closed | `spec/l0/transcript/`, replay redaction smoke |
| Diagnostics schema | closed | `spec/l0/diagnostics/`, diagnostics report smoke |
| Sample agents | closed | `examples/agents/` |

## Task Status Board

| Task | Status | Notes |
| --- | --- | --- |
| `TASK-PAA-V0-HANDOFF-REPAIR` | Pass | One stream selected and defaults reconciled. |
| `TASK-PAA-V0-CONTRACT` | Pass | Versioned `spec/l0/` tree exists. |
| `TASK-PAA-V0-RUNNER-KUHN` | Pass | `doctor`, `run`, and `eval` execute Kuhn sample agents. |
| `TASK-PAA-V0-REPLAY-DIAGNOSTICS` | Pass | `replay` reproduces payouts and exports redacted public replay. |
| `TASK-PAA-V0-AUTHOR-PROOF` | Pass | Sample agents, quickstart docs, tests, and failure diagnostics exist. |
| `TASK-PAA-L0-LEDUC-EXPANSION` | Deferred | First post-MVP validation expansion. |
| `TASK-PAA-M1-HOLDEM-PARITY` | Deferred | Needs Local Arena CLI v0 acceptance and engine choice. |
| `TASK-PAA-M2-LEADERBOARD-NOVELTY` | Deferred | Needs calibrated reference and abuse fixtures. |

## SWU Manifest

### SWU-PAA-001R: Repair Local Arena CLI v0 Handoff

Intent: refresh the root spec/design/work-pack artifacts so `SWU-PAA-001` has one executable stream, visible gaps, and recommended defaults.

Write boundary:

- Root documentation and planning artifacts only.
- No runtime implementation.
- No Hold'em engine selection.
- No leaderboard coefficient implementation.

Acceptance:

- `MVP-PATH.md` names one implementation stream.
- `WORK-PACK.md` routes next to `SWU-PAA-001R`, then `SWU-PAA-001`.
- `RULES.md` remains the human/product rule view and `AGENT-RULES.md` remains the engineer/agent rule view.
- `NAMING.md` keeps `local-arena-cli-v0` as the durable route id.
- Leduc, Hold'em, leaderboard, and novelty work are explicitly deferred.
- Timing, fallback, CLI, runtime root, transcript, diagnostics, sample-agent, and canary gaps are surfaced for operator decision.

### SWU-PAA-001: Freeze Local Arena CLI v0 Contract

Intent: define the versioned file contracts before runtime code starts.

Depends on: `SWU-PAA-001R`

Write boundary:

- Documentation, schema/spec files, and fixture descriptions.
- No game-engine integration.
- No leaderboard coefficient implementation.

Acceptance:

- `spec/l0/runtime/cli.md` defines `paa doctor`, `paa run`, `paa eval`, and `paa replay`.
- `spec/l0/runtime/match-config.md` defines match config and output directory contracts.
- Decision envelope and action envelope examples exist.
- Referee-only fields are explicitly denied.
- Deadline policy freezes clock source, start/stop points, timeout classification, cleanup timeout, and transcript fields.
- Fallback policy freezes a deterministic legal selector.
- Referee transcript and public replay schemas are separate.
- Diagnostics schema separates clean EV, fallback-inclusive EV, invalid rate, timeout rate, fallback count, and replay determinism.

### SWU-PAA-002: Implement Local CLI Runner And Kuhn Fixture Gate

Intent: implement the smallest local runtime that can run the Kuhn hidden-information fixture with sample agents.

Depends on: `SWU-PAA-001`

Acceptance:

- Runtime root exists under `src/poker_agent_arena/`.
- `paa doctor` validates local prerequisites.
- `paa run` can run a single Kuhn match from match config.
- `paa eval` can run a seat-rotated Kuhn fixture orbit.
- Agent-visible observation never includes opponent card, deck order, raw seed, future state, or referee trace.
- Legal-action masks match the Kuhn referee state.
- Invalid output and timeout produce fallback events and transcript diagnostics.

### SWU-PAA-003: Add Replay, Redaction, And Diagnostics Gate

Intent: make the first runtime proof reproducible and honest.

Depends on: `SWU-PAA-002`

Acceptance:

- `paa replay` reproduces accepted actions, fallback events, payouts, and diagnostics from private transcript material.
- Public replay export respects redaction policy.
- Hidden-information canary scan covers observation payloads, legal actions, action history, stdout/stderr capture, logs, replay exports, state hashes, env/log fields, and retained inputs.
- Report output includes clean EV, fallback-inclusive EV, invalid rate, timeout rate, fallback count, and replay determinism.
- Abuse agents cannot improve displayed ranking by timing out or producing invalid output.

### SWU-PAA-004: Add Author Proof And Sample Agents

Intent: prove that a new agent author can run, fail, debug, and improve an agent without reading every internal artifact.

Depends on: `SWU-PAA-003`

Acceptance:

- `examples/agents/check_call.py` and `examples/agents/legal_random.py` pass the Kuhn fixture.
- `examples/agents/timeout.py` and `examples/agents/invalid_json.py` trigger expected diagnostics.
- Author guide includes canonical decision/action JSON examples, invalid-output examples, expected diagnostics, and troubleshooting.
- Quickstart commands produce a transcript, public replay, and diagnostics report in a predictable output directory.

## Deferred Work

| Work | First Eligible Point | Reason Deferred |
| --- | --- | --- |
| Leduc board reveal | After `SWU-PAA-004` | Validates public board reveal and two-street transitions after the first route runs. |
| Hold'em engine adapter | After Leduc or explicit operator override | Requires engine research and parity fixtures. |
| Calibrated leaderboard | After engine parity and reference/adversarial bots | Prevents penalty and variance mechanics from becoming rank exploits. |
| Time-bank and novelty appendix | After stable clocks, replay, and diagnostics | Keeps side mechanics from contaminating primary ranking. |

## Verification Surface

- Schema/examples lint for decision and action envelopes.
- Kuhn fixture transcript replay.
- Hidden-information canary scan.
- Invalid-output matrix.
- Timeout/fallback determinism check.
- Fallback-abuse matrix for timeout, invalid, invalid-facing-bet, crash, and EOF agents.
- Seat-rotation raw EV reproducibility.
- Public replay redaction check.
- Author quickstart smoke test.

## Handoff

Local Arena CLI v0 is complete for the MVP proof slice. Next eligible work is
post-MVP expansion planning: Leduc board reveal first, then Hold'em engine parity
or calibrated leaderboard work only after an explicit new route is selected.
