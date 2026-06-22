# Poker Agent Arena Design

Status: refreshed Invoke artifact
Source evidence:

- `development/dispatches/20260619-agent-arena-mechanics/`
- `development/refinement-runs/20260619T022414Z-current-spec-architecture-plan/RESULT.md`

## 1. Context

The arena sits between submitted agents and an authoritative referee. Agents see only filtered observations and legal actions. The referee owns truth. Scoring consumes transcripts after hand resolution.

```text
agent executable <-> CLI protocol <-> arena/referee <-> game authority
                                      |
                                      v
                              transcript + diagnostics
```

`Local Arena CLI v0` uses toy game authority with a Kuhn fixture gate first. Leduc board reveal is staged as the next validation expansion. M1 replaces or wraps the game authority with a selected Hold'em engine while keeping the same outer protocol and observation rules.

## 2. High-Level Structure

| Component | Responsibility | Local Arena CLI v0 Status |
| --- | --- | --- |
| Agent runner | Spawn process, pass env allowlist, wire stdin/stdout/stderr | Required |
| Protocol adapter | Serialize decision envelopes and parse one action envelope | Required |
| Referee | Own true game state, legal actions, payouts, fallbacks | Required for toy games |
| Observation filter | Project referee state into agent-visible allowlist | Required |
| Transcript writer | Record decisions, actions, errors, fallbacks, timings, payouts | Required |
| Replay verifier | Re-read transcript and reproduce diagnostics | Required |
| Scoring diagnostics | Raw EV, timeout rate, invalid rate, replay determinism | Required |
| Hold'em engine adapter | Delegate legal transitions and settlement to engine | M1 |
| Leaderboard scorer | Compute adjusted score after calibration | M2 |
| Novelty appendix | Time-bank and other agent-native mechanics | M2 |

## 3. Rule View Architecture

| View | File | Audience | Owns | Must Not Own |
| --- | --- | --- | --- | --- |
| Human/product | `RULES.md` | Competitors, reviewers, product readers | Plain-language competition rules, fairness promises, Local Arena CLI v0 ranking explanation, non-goals | Exact JSON schemas or hidden-state authority |
| Engineer/agent | `AGENT-RULES.md` | Agent authors, referee implementers, validators, task-session agents | Protocol-facing obligations, invalid-output rules, deadline/fallback rules, transcript/replay obligations, fixture obligations | Product positioning or final versioned schema details |
| Versioned L0 specs | `spec/l0/` | Implementers and validators | Exact field contracts, fixture formats, validation checks | Broad product explanation |

The two rule files are a deliberate split. `RULES.md` should make the arena understandable to humans without requiring protocol literacy. `AGENT-RULES.md` should be strict enough that a coding agent can implement or validate against it without importing product language into machine-facing contracts.

## 4. L0 Component Map

| Component | Input | Output | Owns | Must Not Own |
| --- | --- | --- | --- | --- |
| Agent runner | Agent package, argv/env allowlist, decision envelope | stdout/stderr events, lifecycle status | Process lifecycle and monotonic timing window | Game truth or scoring truth |
| Protocol adapter | Referee decision request | JSON decision envelope and parsed action envelope | Schema versioning, id matching, parse errors | Hidden state |
| Toy referee | Ruleset id, seed material, accepted action | Legal actions, state transition, payout | True toy-game state; Kuhn first, Leduc expansion next | Public redaction policy |
| Observation filter | Referee truth | Agent observation | Allowlist projection | Deck order, future cards, opponent private cards |
| Transcript writer | Decisions, actions, fallbacks, timings, payouts | Referee transcript and public replay material | Replay fields and redaction split | Score coefficients |
| Replay verifier | Transcript | Reproduced events and payouts | Determinism check | Live game control |
| Scoring diagnostics | Transcript and replay results | Raw EV, invalid rate, timeout rate, fallback count | Local Arena CLI v0 diagnostics | Adjusted leaderboard score |

## 5. State Namespace Matrix

| Namespace | Visibility | Examples | Transition Rule |
| --- | --- | --- | --- |
| `referee.truth` | Referee-only | Raw seed, deck order, private cards, full toy state | May project only through observation filter or redacted transcript. |
| `agent.observation` | Acting agent | Public state, own private card, legal actions, deadline | Must be allowlisted and non-predictive. |
| `protocol.action` | Arena/referee | Parsed action envelope, decision id, action, amount | Must match current legal-action set or become invalid event. |
| `transcript.private` | Referee/replay verifier | Raw seed or deterministic replay material, state hashes | Must not be exported to live agents. |
| `transcript.public` | Post-match/public if enabled | Seed commitment, opaque ids, accepted actions, public state, payouts | Redaction policy controls release timing. |
| `score.diagnostics` | Evaluator/report | Raw EV, invalid rate, timeout rate, replay determinism | Derived from transcript, not live referee internals. |

## 6. Low-Level Components

### Decision Envelope

Required fields:

- `protocol_version`
- `type`
- `match_id`
- `hand_id`
- `decision_id`
- `seat_id`
- `deadline_ms`
- `observation`
- `legal_actions`

The envelope must not include seed material that predicts future cards, referee-only traces, opponent private cards, phase labels, or engine internals.

### Action Envelope

Required fields:

- `protocol_version`
- `decision_id`
- `action`
- Optional opaque metadata ignored by gameplay.

Only the first complete stdout JSON object is eligible for validation. Prose before JSON, malformed JSON, extra decision objects, mismatched ids, unknown actions, and illegal amounts become invalid events.

### Fallback Event

Fallback records:

- Error type.
- Original output classification.
- Deterministic legal continuation.
- Elapsed time.
- Decision id.
- Seat id.
- Whether strike or retirement policy applies.

Fallback action changes the hand state; fallback event changes diagnostics and later penalties.

### Transcript Record

Transcript material is split by namespace:

- Referee transcript may include raw seed material, deterministic replay material, state hashes, referee-only traces, decision envelopes, accepted actions, fallback events, elapsed time, and payouts.
- Public replay may include only redacted public state, opaque ids, seed handles or post-match commitments, accepted actions, fallbacks, elapsed time, and payouts.

Raw seed material, future cards, live opponent private cards, hidden traces, and reversible hidden-state hashes must never appear in live decision envelopes or public replay.

### Timing Policy

Local Arena CLI v0 must freeze:

- monotonic clock source,
- deadline start at arena write flush,
- deadline stop at first complete stdout JSON object,
- grace policy,
- timeout classification,
- recorded elapsed/deadline fields,
- replay behavior for timeout diagnostics.

## 7. Workflow Process

```text
configure match
spawn agent processes
for each hand:
  referee creates true state
  for each decision:
    compute legal actions
    filter observation
    send decision envelope
    read first stdout JSON or timeout
    validate decision id and action
    accept action or apply fallback
    append transcript event
  settle payout
  append hand result
after match:
  replay transcript
  compute raw EV and diagnostics
```

Local Arena CLI v0 blocks if the replay verifier cannot reproduce payouts and invalid/timeout/fallback diagnostics from recorded material.

## 8. Decision Flow

```text
stdout object received?
  no -> timeout event -> deterministic fallback
  yes
    valid JSON object?
      no -> invalid event -> deterministic fallback
      yes
        decision_id matches?
          no -> invalid event -> deterministic fallback
          yes
            action in legal_actions?
              no -> invalid event -> deterministic fallback
              yes -> accept action
```

This flow intentionally separates legal continuation from competitive forgiveness. Fallback keeps the match alive, but it is always visible in diagnostics and later scoring.

## 9. L0 Output Tree

`SWU-PAA-001R` should authorize this docs/schema/fixture surface before runtime code:

```text
projects/poker-agent-arena/
  RULES.md
  AGENT-RULES.md
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

## 10. Dependency Interface

Local Arena CLI v0 dependencies are intentionally small:

- Local process spawning and monotonic timing.
- JSON line transport.
- Toy Kuhn rules for the first fixture gate; Leduc rules for the next fixture expansion.
- Deterministic seeding for replay.
- Markdown/fixture evidence for review.

M1 adds one selected local poker engine. The arena interface to that engine must be narrow:

- Request legal actions.
- Advance state by validated action.
- Project public state.
- Resolve payout and pot layers.
- Provide versioned replay identifiers.

The arena must not depend on engine object serialization for agent-visible observations. Observation projection stays allowlist-based.
