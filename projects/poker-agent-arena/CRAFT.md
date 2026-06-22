# Poker Agent Arena Craft

Source of truth: [.craft/ledger.yml](.craft/ledger.yml)

This Craft space tracks the `Local Arena CLI v0` MVP line for Poker Agent Arena.
The local proof slice has passed: contracts, runtime, fixtures, sample agents,
replay, diagnostics, tests, and verification evidence now exist.

## Quick Links

- Root context: [CTX-PAA-ROOT](#ctx-paa-root)
- Current blocker: none
- Blocking decisions: none
- Active gaps: none
- Current work pack: [WORK-PACK.md](WORK-PACK.md)
- Verification: [development/verification/local-arena-cli-v0/VERIFICATION.md](development/verification/local-arena-cli-v0/VERIFICATION.md)
- Share packet: [Poker-Agent-Arena.pdf](Poker-Agent-Arena.pdf)
- One-shot goal: [development/goals/local-arena-cli-v0-one-shot-goal.md](development/goals/local-arena-cli-v0-one-shot-goal.md)
- MVP sidecar: [development/goals/local-arena-cli-v0-mvp-sidecar.md](development/goals/local-arena-cli-v0-mvp-sidecar.md)

## Pending By Node

### Poker Agent Arena - Local Arena CLI v0

- Ledger: [.craft/ledger.yml](.craft/ledger.yml)
- Root context: `CTX-PAA-ROOT`
- Readiness: `pass`
- Active blockers: none
- Blocking decisions: none
- Other open decisions: [DEC-PAA-M1-ENGINE-001](#dec-paa-m1-engine-001), [DEC-PAA-TIME-CREDITS-001](#dec-paa-time-credits-001)
- Active gaps: none
- Completed route: `SWU-PAA-001R` through `SWU-PAA-004`
- Recomposition residue: Leduc, Hold'em engine parity, calibrated leaderboard, and novelty mechanics remain post-MVP routes.
- Current next move: Select the first post-MVP expansion route. Do not widen Local Arena CLI v0 without a new explicit route.

## Context

### CTX-PAA-ROOT

Poker Agent Arena is a local competition harness where agents play poker-like
toy games through constrained CLI decisions. The first product surface is
`Local Arena CLI v0`, with Kuhn as the first fixture gate and Leduc, Hold'em
engine parity, calibrated leaderboards, and novelty mechanics staged after the
MVP line proves protocol and replay.

## Decisions

### DEC-PAA-DEADLINE-001

Question: What exact Local Arena CLI v0 deadline policy should `SWU-PAA-001`
freeze?

Blocking: no. Closed for Local Arena CLI v0.

Default option: accept the current refine defaults: 5000ms decision timeout,
10000ms cleanup timeout, monotonic clock, start after decision-envelope flush,
and stop at the first complete stdout JSON object.

Evidence: [WORK-PACK.md](WORK-PACK.md), [development/goals/local-arena-cli-v0-one-shot-goal.md](development/goals/local-arena-cli-v0-one-shot-goal.md)

### DEC-PAA-INVALID-RETIREMENT-001

Question: What invalid-output strike and process retirement policy should v0
use?

Blocking: no. Closed for Local Arena CLI v0.

Default option: every invalid decision triggers deterministic fallback, with no
match retirement in v0.

Evidence: [SPEC.md](SPEC.md)

### DEC-PAA-PUBLIC-REPLAY-001

Question: What redaction and seed-commitment policy should public replay expose?

Blocking: no. Closed for Local Arena CLI v0.

Default option: public replay uses opaque seed handles and no raw seed material.

Evidence: [SPEC.md](SPEC.md)

### DEC-PAA-ORBIT-COUNT-001

Question: What first hand or seat-orbit count should provisional diagnostics use?

Blocking: no. Closed for Local Arena CLI v0.

Default option: use a tiny deterministic smoke orbit for fast local proof.

Evidence: [WORK-PACK.md](WORK-PACK.md)

### DEC-PAA-M1-ENGINE-001

Question: Which local Hold'em engine should M1 wrap after Local Arena CLI v0
passes?

Blocking: no. This is deferred until after MVP acceptance.

Evidence: [SPEC.md](SPEC.md)

### DEC-PAA-TIME-CREDITS-001

Question: Should appendix time credits reset per hand, match, or evaluation
block?

Blocking: no. Novelty mechanics stay outside v0 primary ranking.

Evidence: [SPEC.md](SPEC.md)

## Blockers

### BLK-PAA-RUNTIME-GATE-001

Runtime gate is closed for Local Arena CLI v0.

Closure evidence: versioned protocol, runtime, transcript, diagnostics, fixture,
deadline, fallback, state-namespace artifacts, sample agents, tests, and
verification evidence exist and are linked back into Craft.

Evidence: [WORK-PACK.md](WORK-PACK.md), [MVP-PATH.md](MVP-PATH.md), [development/verification/local-arena-cli-v0/VERIFICATION.md](development/verification/local-arena-cli-v0/VERIFICATION.md)

## Gaps

### GAP-PAA-L0-SPEC-TREE-001

The required `spec/l0/` runtime, protocol, transcript, diagnostics, fixture, and
state-namespace tree exists.

Status: closed.

### GAP-PAA-RUNTIME-ROOT-001

Runtime root is `src/poker_agent_arena/`.

Status: closed.

### GAP-PAA-PROTOCOL-EXAMPLES-001

Decision/action examples and invalid-output matrix are enumerated.

Status: closed.

### GAP-PAA-TRANSCRIPT-REPLAY-001

Referee transcript and public replay split is schema-level and runtime-backed.

Status: closed.

### GAP-PAA-KUHN-ORACLE-001

Kuhn fixture has seed corpus, legal-action table, transcript replay, and payout
verification.

Status: closed.

### GAP-PAA-DIAGNOSTICS-001

Diagnostic report schema and runtime report exist for clean EV,
fallback-inclusive EV, invalid rate, timeout rate, fallback count, and replay
determinism.

Status: closed.

## Artifacts

- [README.md](README.md): project overview.
- [SPEC.md](SPEC.md): owned boundary, milestones, contracts, gates, and open decisions.
- [DESIGN.md](DESIGN.md): architecture and design artifact.
- [WORK-PACK.md](WORK-PACK.md): `WP-PAA-001` one implementation stream and SWU manifest.
- [MVP-PATH.md](MVP-PATH.md): MVP route and blockers.
- [RULES.md](RULES.md): human/product rule view.
- [AGENT-RULES.md](AGENT-RULES.md): engineer/agent rule view.
- [pyproject.toml](pyproject.toml): package metadata and `paa` entry point.
- [spec/l0/](spec/l0/): versioned runtime, protocol, transcript, diagnostics, fixture, and state namespace contracts.
- [src/poker_agent_arena/](src/poker_agent_arena/): Local Arena CLI v0 runtime.
- [fixtures/l0/](fixtures/l0/): Kuhn, invalid, timeout, fallback-abuse, and leak-canary fixture material.
- [examples/agents/](examples/agents/): friendly and adversarial sample agents.
- [tests/](tests/): unittest coverage for core runtime invariants.
- [development/verification/local-arena-cli-v0/VERIFICATION.md](development/verification/local-arena-cli-v0/VERIFICATION.md): durable verification report.
- [Poker-Agent-Arena.pdf](Poker-Agent-Arena.pdf): public-safe product/system share packet.
- [docs/poker-agent-arena-share.html](docs/poker-agent-arena-share.html): print-oriented source for the share packet.
- [development/refinement-runs/20260619T143102Z-mvp-design/RUNTIME-HANDOFF.md](development/refinement-runs/20260619T143102Z-mvp-design/RUNTIME-HANDOFF.md): refined runtime handoff.
- [development/refinement-runs/20260619T143102Z-mvp-design/RESULT.md](development/refinement-runs/20260619T143102Z-mvp-design/RESULT.md): refine result that selected the Local Arena CLI v0 line.
- [development/goals/local-arena-cli-v0-one-shot-goal.md](development/goals/local-arena-cli-v0-one-shot-goal.md): generated one-shot Codex goal profile.
- [development/goals/local-arena-cli-v0-mvp-sidecar.md](development/goals/local-arena-cli-v0-mvp-sidecar.md): dense execution frame for the compact MVP goal.

## Next Move

Select the first post-MVP expansion route: Leduc board reveal, Hold'em engine
parity research, or calibrated leaderboard work.
