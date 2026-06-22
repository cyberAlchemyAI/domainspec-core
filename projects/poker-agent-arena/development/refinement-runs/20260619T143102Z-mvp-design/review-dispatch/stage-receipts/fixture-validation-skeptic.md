# Fixture Validation Skeptic Receipt

Agent id: `019ee093-8e57-73e1-a7fd-74e71fa8c9b7`
Role id: `fixture-validation-skeptic`
Agent name: `Capucci, Matteo`
Status: `flag`

## Findings

| Severity | File | Evidence | Proposed fix |
| --- | --- | --- | --- |
| block-for-acceptance | `REFINE-DISPATCH.json`, `SPEC.md` | Selected MVP is "Local Kuhn CLI MVP" with "one toy poker game," but M0 "proves the contract using Kuhn and Leduc fixtures." | Resolve scope: declare first executable Kuhn-only with Leduc as a later gate, or require Leduc board-reveal before MVP acceptance. |
| block-for-acceptance | `RUNTIME-HANDOFF.md`, `RUN-MANIFEST.md` | "No runtime-backed stage has been executed"; `RESULT.md` and `stages/` are pending. | Do not accept fixture claims as proved. Require executable or schema-backed fixture artifacts before MVP acceptance language. |
| block-for-acceptance | `DESIGN.md`, `SPEC.md` | Fallback is "deterministic legal continuation" and must never be score-improving, but fallback selection is unspecified. | Freeze fallback choice per legal-action state, record `fallback_action` and `fallback_reason`, and prove abuse agents cannot improve accepted ranking. |
| flag | `AGENT-RULES.md`, `DESIGN.md` | "First complete stdout JSON object" is the only candidate, but edge cases are not enumerated. | Add `invalid-events.md` with event codes and golden cases for stdout/stderr drift. |
| block-for-acceptance | `AGENT-RULES.md`, `SPEC.md` | Fixtures must prove logs, stdout/stderr, replay exports, state hashes, and retained memory inputs do not leak hidden info. | Define canary injection and scanning rules across seed, deck order, opponent card, referee traces, env/log fields, transcripts, replays, and reversible hashes. |
| flag | `SPEC.md`, `DESIGN.md` | Timing policy fields are required, but deadline defaults, grace, classification, and replay timing remain open decisions. | Block timeout fixture acceptance until clock source, grace, timeout class, late-output handling, and elapsed/deadline transcript fields are frozen. |
| block-for-acceptance | `WORK-PACK.md`, `RULES.md` | Raw EV is diagnostic while fallback is visible later; no rule prevents fallback-inclusive raw EV from looking good. | Report clean EV, fallback-inclusive EV, timeout/invalid/fallback counts separately; block any ranking display where abuse agents beat clean baselines. |

## Abuse Cases

- Hidden information: inject canary tokens into seed, deck order, opponent card, future board, referee trace, env, private transcript, and state hash; fail if any appears in agent stdin, stdout/stderr capture, logs, action history, public replay, or retained inputs.
- Invalid actions: stale `decision_id`, action outside `legal_actions`, illegal amount, legal-looking action from prior state, duplicate action object, unknown action, and amount-boundary fuzzing must all produce named invalid events plus deterministic fallback.
- Stdout/stderr protocol drift: prose before JSON, JSON only on stderr, partial JSON before valid JSON, two stdout JSON objects, valid JSON with trailing chatter, invalid UTF-8, oversized stdout, and metadata-dependent action interpretation.
- Timeout fallback: no output, late output after deadline, partial JSON until deadline, sleep-then-output, crash, EOF, and state-conditional timeout must produce stable event records and non-improving fallback behavior.
- Replay determinism: private transcript replay must reproduce accepted actions, fallback events, payouts, elapsed/deadline diagnostics, and invalid classifications without live process state or wall-clock dependence.
- Scoring: always-timeout, always-invalid, invalid-only-when-facing-bet, crash/EOF, and latency-staller agents must not improve any MVP acceptance metric relative to clean legal baselines.

## Minimum Golden Transcripts And Fixture Agents

Golden transcripts: clean Kuhn seat-swapped orbit; Kuhn hidden-info canary transcript; invalid-output matrix transcript; timeout/crash/EOF fallback transcript; fallback-abuse scoring transcript; public replay redaction transcript; Leduc board-reveal transcript if M0 keeps claiming Kuhn plus Leduc proof.

Fixture agents: legal-random deterministic baseline; legal check/fold baseline; always-timeout; always-invalid malformed JSON; mismatched-id/stale-action agent; invalid-only-when-facing-bet agent; stdout-chatter/stderr-speaker agent; crash/EOF agent; canary-echo agent that repeats any visible secret.

## Validation Gates That Should Block MVP Acceptance

- `spec/l0/` decision, action, legal-action, invalid-event, deadline, transcript, replay, and namespace contracts exist with examples.
- `fixtures/l0/` contains golden transcripts, expected payouts, expected diagnostics, and fixture-agent outputs.
- Hidden-information canary scan passes across observations, legal actions, stdout/stderr, logs, action history, public replay, hashes, env, and retained inputs.
- Invalid-output matrix passes with named event codes and deterministic fallback records.
- Timeout policy is frozen and timeout/fallback determinism passes.
- Private replay reproduces payouts and diagnostics; public replay redaction contains no raw seed or reversible hidden-state hash.
- Fallback-abuse agents cannot improve MVP ranking or acceptance metrics.
- Seat-rotation raw EV reproducibility passes.
- Kuhn-only versus Kuhn-plus-Leduc scope is resolved before any M0 fairness claim.
- Composite `arena_score` remains absent.

## Parent Synthesis Handoff

Keep the selected `local-kuhn-cli-mvp` only if parent synthesis explicitly separates "first executable path" from "M0 acceptance proof." Fixture abuse still lives mostly as requirements prose; parent should require a concrete L0 fixture packet with golden transcripts, canary scanning, fallback-abuse agents, and replay/scoring gates before treating the MVP as accepted.
