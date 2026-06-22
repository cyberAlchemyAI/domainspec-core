# Refine Result - Poker Agent Arena Local Arena CLI v0 MVP Path

Status: `parent-synthesis-complete-with-open-decisions`

This result consumes the completed subagent review and turns the review residue into one executable MVP path. It is not runtime implementation proof. It is a decision-ready handoff for `task-session`.

## Selected Route

Use `local-arena-cli-v0` as the canonical route id and `Local Arena CLI v0` as the human label. Kuhn is the first fixture gate inside the route. Leduc is the first post-MVP validation expansion.

## Parent Synthesis

The implementation stream is:

```text
SWU-PAA-001R -> SWU-PAA-001 -> SWU-PAA-002 -> SWU-PAA-003 -> SWU-PAA-004
```

Meaning:

1. Repair the handoff and surface decisions.
2. Freeze the Local Arena CLI v0 contract.
3. Implement the local runner and Kuhn fixture gate.
4. Add replay, redaction, and diagnostics acceptance.
5. Add author proof with sample agents and quickstart.

## Produced Artifacts

- `../../../MVP-PATH.md`
- `../../../WORK-PACK.md`
- `IMPLEMENTATION-STREAM.md`
- `stages/10-final-implementation-stream.md`

## Recommended Defaults

- Runtime root: `src/poker_agent_arena/`
- CLI namespace: `paa`
- CLI commands: `paa doctor`, `paa run`, `paa eval`, `paa replay`
- Decision timeout: `5000ms`
- Process cleanup timeout: `10000ms`; late output remains timeout, not accepted action
- Clock: monotonic
- Fallback selector: passive deterministic order, `check`, `fold`, `call`, then minimum legal wager action
- Scoring surface: clean EV, fallback-inclusive EV, invalid rate, timeout rate, fallback count, replay determinism

## Blockers

- Runtime code remains blocked until `SWU-PAA-001R` and `SWU-PAA-001` pass.
- MVP acceptance remains blocked until Kuhn runs end to end with replay, redaction, diagnostics, canary scans, sample agents, and author quickstart.
- Leduc, Hold'em engine parity, adjusted leaderboard scoring, and novelty mechanics remain deferred unless the operator explicitly widens the route.

## Gaps Now Surfaced

- Runtime root and package boundary.
- CLI command contract and match config schema.
- Process lifecycle policy for stdout, stderr, env, crash, EOF, kill, timeout, and cleanup.
- Decision/action examples and invalid-event codes.
- Formal fallback and deadline policies.
- Kuhn golden transcript and payout oracle.
- Private referee transcript, public replay, and redaction schemas.
- Diagnostics schema separating clean EV from fallback-inclusive EV.
- Friendly sample agents and adversarial fixture agents.
- Author quickstart with runnable commands and expected diagnostics.

## Validation Meaning

`REFINE-DISPATCH.json` should continue to validate as `VALIDATION=flag`, not `pass`, because the completed subagent lifecycle and parent synthesis intentionally carry fix residue and open decisions. That flag is useful: it tells the next task-session what must be closed before runtime claims.

## Next Action

Run `task-session` on `SWU-PAA-001R`. If the operator accepts the recommended defaults, `SWU-PAA-001R` can move directly to freezing the output tree and handing off `SWU-PAA-001`.
