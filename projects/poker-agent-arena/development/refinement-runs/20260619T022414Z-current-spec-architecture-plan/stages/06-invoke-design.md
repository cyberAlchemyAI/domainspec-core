# Invoke Redefine / Design: L0 Contract Repair Packet

Status: flag
Owner: `invoke` via parent Refine coordinator
Mode: `design`

## Design Target

Repair the current spec, architecture, and plan just enough to make `SWU-PAA-001` executable as a contract-freeze task.

## Required L0 Output Tree

The next root-artifact repair should add or authorize a tree like:

```text
projects/poker-agent-arena/
  spec/l0/protocol/
    decision-envelope.md
    action-envelope.md
    legal-actions.md
    invalid-events.md
    deadline-policy.md
  spec/l0/transcript/
    referee-transcript.md
    public-replay.md
    redaction-policy.md
  spec/l0/state-namespaces.md
  fixtures/l0/
    kuhn_hidden_info/
    leduc_board_reveal/
    invalid_output_matrix/
    timeout_fallback/
    fallback_abuse/
    leak_canary/
```

This tree can begin as Markdown/schema examples. Runtime implementation remains a later task.

## L0 Component Map

| Component | Input | Output | Owns | Must Not Own |
| --- | --- | --- | --- | --- |
| Agent runner | Agent package, argv/env allowlist, decision envelope | stdout/stderr events, lifecycle status | process lifecycle, monotonic timing window | game truth, scoring truth |
| Protocol adapter | Referee decision request | JSON decision envelope and parsed action envelope | schema versioning, id matching, parse errors | hidden state |
| Toy referee | ruleset id, seed material, accepted action | legal actions, state transition, payout | true toy-game state | public redaction policy |
| Observation filter | referee truth | agent observation | allowlist projection | deck order, future cards, opponent private cards |
| Transcript writer | decisions, actions, fallbacks, timings, payouts | referee transcript and public replay material | replay fields, redaction split | score coefficients |
| Replay verifier | transcript | reproduced events and payouts | determinism check | live game control |
| Scoring diagnostics | transcript and replay results | raw EV, invalid rate, timeout rate | M0 diagnostics | adjusted leaderboard score |

## State Namespace Matrix

| Namespace | Visibility | Examples | Transition Rule |
| --- | --- | --- | --- |
| `referee.truth` | referee-only | raw seed, deck order, private cards, full toy state | May project only through observation filter or redacted transcript. |
| `agent.observation` | acting agent | public state, own private card, legal actions, deadline | Must be allowlisted and non-predictive. |
| `protocol.action` | arena/referee | parsed action envelope, decision id, action, amount | Must match current legal-action set or become invalid event. |
| `transcript.private` | referee/replay verifier | raw seed or deterministic replay material, state hashes | Must not be exported to live agents. |
| `transcript.public` | post-match/public if enabled | seed commitment, opaque ids, accepted actions, public state, payouts | Redaction policy controls release timing. |
| `score.diagnostics` | evaluator/report | raw EV, invalid rate, timeout rate, replay determinism | Derived from transcript, not live referee internals. |

## Repair Gates

- Public replay cannot expose raw seed material.
- Agent-visible ids must be opaque and non-predictive.
- Fallback actions are flagged separately from agent-chosen legal actions.
- Hidden-information canaries cover observations, legal actions, logs, replay exports, state hashes, retained memory inputs, and environment/log redaction.
- Timing semantics define clock source, start/stop points, grace policy, timeout classification, and recorded elapsed/deadline fields.
