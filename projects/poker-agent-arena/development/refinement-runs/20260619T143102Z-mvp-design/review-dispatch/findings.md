# Review Findings

Dispatch id: `2026-06-19-poker-agent-arena-mvp-review`
Final approver: `parent`
Verdict: `FIX`
Exit reason: `resolved`

The review produced no blockers to continuing the design path, but it did produce blockers to claiming MVP acceptance. The naming observer refined the recommendation: use `local-arena-cli-v0` as the canonical route id, treat Kuhn as the first fixture gate inside that route, and stage Leduc as the next validation expansion.

## `REFINE-DISPATCH.json`

| # | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- |
| 1 | Selected route was `local-kuhn-cli-mvp`, while existing M0 docs still required Kuhn plus Leduc. | major | Rename the canonical route to `local-arena-cli-v0`; make Kuhn the first fixture gate and stage Leduc as the first board-reveal expansion. |
| 2 | The dispatch itself says the project still needs module boundaries, interfaces, artifact ownership, and CLI command shape. | major | Add an explicit runtime architecture packet to the next invoke/refine result: runtime root, module tree, CLI commands, process lifecycle, transcript/replay ownership, diagnostics ownership, and sample-agent ownership. |

Verdict: `FIX`

## Root Project Docs

| # | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- |
| 3 | `SPEC.md`, `DESIGN.md`, `README.md`, `AGENT-RULES.md`, and `IMPLEMENTATION-LAYERING.md` describe M0/L0 as Kuhn plus Leduc. | major | Split route and fixture language: `Local Arena CLI v0` is the durable route, Kuhn is the first fixture gate, and Leduc is the board-reveal expansion. |
| 4 | `WORK-PACK.md` routes raw scoring diagnostics after both Kuhn and Leduc tasks, which blocks the first route from reporting EV. | major | Split diagnostics into Kuhn gate diagnostics for `Local Arena CLI v0` and Leduc diagnostics for the next validation expansion. |
| 5 | `IMPLEMENTATION-LAYERING.md` says "Start with L0" while the active route is `SWU-PAA-001R`. | medium | Reword the recommendation to start with L0R contract repair, then execute `Local Arena CLI v0`. |
| 6 | Public and author docs are polished but conceptual; there is no first runnable path. | major | Add a quickstart contract: run bundled Kuhn match, validate a custom agent, replay transcript, inspect diagnostics. |

Verdict: `FIX`

## Runtime Architecture

| # | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- |
| 7 | The output tree names docs, specs, and fixtures, but not a concrete runtime root. | major | Add a selected runtime root and package boundary, for example `src/poker_agent_arena/`, with CLI, runner, protocol, games/kuhn, referee, transcript, replay, and diagnostics modules. |
| 8 | CLI command shape is not frozen. | major | Add `spec/l0/runtime/cli.md` with `run`, `eval`, `replay`, and `doctor` commands plus match config and output directory contracts. |
| 9 | Runner lifecycle policy is incomplete. | major | Add process lifecycle rules for stdout buffering, stderr capture/redaction, env allowlist, crash, EOF, kill, retry, retirement, and timeout handling. |
| 10 | Sample agents are named in the seed but not owned in the output tree. | major | Add friendly samples under `examples/agents/` and abuse fixtures under `fixtures/l0/agents/`, with separate roles for onboarding and validation. |

Verdict: `FIX`

## Fixture And Safety Gates

| # | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- |
| 11 | Fallback is deterministic in prose but has no selection rule. | block-for-acceptance | Freeze fallback as a deterministic function of legal-action state; record `fallback_action`, `fallback_reason`, and source event in transcript diagnostics. |
| 12 | Invalid stdout/stderr edge cases are not enumerated. | major | Add `spec/l0/protocol/invalid-events.md` with event codes and golden cases for prose before JSON, partial JSON, stderr JSON, duplicate objects, invalid UTF-8, oversized stdout, mismatched ids, unknown actions, and illegal amounts. |
| 13 | Hidden-information canary scope is broad but not operationalized. | block-for-acceptance | Define canary injection and scanning across seed, deck order, opponent card, future board, referee trace, env/log fields, private transcript, public replay, reversible hashes, stdout/stderr, and retained inputs. |
| 14 | Timing defaults are open while deadline behavior is normative. | major | Freeze Local Arena CLI v0 defaults for monotonic clock, write-flush start, first complete stdout JSON stop, soft/hard deadline, grace policy, timeout class, late-output behavior, and elapsed/deadline transcript fields. |
| 15 | Raw EV could hide fallback abuse if reported alone. | block-for-acceptance | Report clean EV, fallback-inclusive EV, timeout rate, invalid rate, fallback count, and replay determinism separately; block any ranking display where abuse agents beat clean baselines. |

Verdict: `FIX`

## Author Experience

| # | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- |
| 16 | `docs/AGENT-AUTHOR-GUIDE.md` lists required fields but has no canonical JSON examples. | major | Add minimal Kuhn decision and action JSON examples, plus invalid-output examples and expected diagnostics. |
| 17 | Diagnostics are named but not shown. | major | Add diagnostics examples: event code, cause, stdout/stderr snippet, fallback action, transcript path, and suggested fix. |
| 18 | Submission shape is not specified. | minor | Define one submission contract: command string or manifest, argv/env allowlist, working directory, exit/EOF behavior, and sample invocation. |

Verdict: `FIX`

## Accepted Change Requests

1. Use `local-arena-cli-v0` as the canonical route id; keep Kuhn and Leduc as fixture-gate names.
2. Add a runtime architecture packet before implementation task-session.
3. Freeze the CLI command contract and match config surface.
4. Freeze timing and fallback rules before claiming first-run usability.
5. Add transcript/private replay and public replay schemas with redaction policy.
6. Add invalid-event codes and fixture cases for stdout/stderr/protocol drift.
7. Operationalize hidden-information canary scanning.
8. Split clean EV, fallback-inclusive EV, and diagnostics; keep composite scoring blocked.
9. Add sample agents and abuse fixture agents as owned Local Arena CLI v0 outputs.
10. Add author-facing quickstart, JSON examples, diagnostics examples, and troubleshooting.

## Parent Synthesis Decision

The parent accepts the review and closes the dispatch as resolved with `FIX` verdicts. The next refine/invoke refresh should produce a `Local Arena CLI v0` design and plan, not runtime code, and should preserve Leduc as a staged validation extension.
