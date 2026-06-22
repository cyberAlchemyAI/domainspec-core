# Stage 10 - Final Implementation Stream Synthesis

Status: `flag`
Reason: one executable MVP stream is now selected, but runtime remains blocked until contract files and operator-sensitive defaults are accepted or overridden.

## Inputs

- `review-dispatch/findings.md`
- `review-dispatch/attacks.md`
- `naming-observer-receipt.md`
- `../../../NAMING.md`
- `../../../WORK-PACK.md`
- `../../../MVP-PATH.md`

## Result

Parent refine synthesis selects one implementation stream:

```text
SWU-PAA-001R -> SWU-PAA-001 -> SWU-PAA-002 -> SWU-PAA-003 -> SWU-PAA-004
```

The route is `Local Arena CLI v0`. Kuhn is the first fixture gate. Leduc is staged after MVP acceptance.

## Surfaced Decisions

- Runtime root: recommend `src/poker_agent_arena/`.
- CLI namespace: recommend `paa`.
- Commands: recommend `doctor`, `run`, `eval`, and `replay`.
- Timing: recommend 5s decision timeout and 10s process cleanup timeout.
- Fallback: recommend passive deterministic legal-action order.
- Scoring: keep clean EV separate from fallback-inclusive EV and diagnostics.

## Blockers

- No runtime code should begin until `SWU-PAA-001R` and `SWU-PAA-001` pass.
- MVP acceptance is blocked until Kuhn runs end to end with replay, redaction, diagnostics, canary scans, sample agents, and author quickstart.
- Hold'em engine and composite leaderboard work remain blocked until Local Arena CLI v0 acceptance.

## Artifacts Produced

- `../../../MVP-PATH.md`
- `../../../WORK-PACK.md`
- `IMPLEMENTATION-STREAM.md`
- `stages/10-final-implementation-stream.md`
