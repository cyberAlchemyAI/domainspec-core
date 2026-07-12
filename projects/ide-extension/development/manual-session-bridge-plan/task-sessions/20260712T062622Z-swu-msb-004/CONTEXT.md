# Context Pack: SWU-MSB-004

## Selection And Sources

- Task/SWU: `TASK-BRIDGE-KERNEL / SWU-MSB-004`
- Dependency: [SWU-MSB-003 result](../20260712T062325Z-swu-msb-003/TASK-SESSION-RESULT.md)
- Controls: bridge-kernel task contract, approved claim/recovery architecture,
  v2 schemas/projector, server mutation queue, artifact interface, 003 API tests
- Runtime: local Codex; no delegation or strict runtime handoff

## Execution Decision

- Claim request supplies only schema version, bound envelope, fixed agent ref,
  caller session ref, and `assurance: unattested`.
- The serialized mutation appends a claim event and attempt artifact before the
  response exposes task, skill, grants, or context.
- Duplicate/losing claims return stable conflict bodies with no execution packet.
- Claimant interruption requires exact session/claim binding and writes evidence.
- Operator release accepts a bounded reason, creates the actor descriptor in the
  kernel, preserves the authorization/attempt, and returns to `approved`; it
  never automatically readies or retries.
- No timer, lease, authentication, worker, or result admission enters this SWU.

## Gates And Evidence

- 003 dependency and authorization/target restart evidence: pass.
- Decisions/blockers: none.
- Write scope: bridge helper, artifacts, projector/server, focused tests/package.
- Required proof: one race winner, no loser disclosure, wrong-session failure,
  interrupt/release actor separation, restart in claimed/interrupted, second
  attempt only after release plus explicit ready, artifact/append failure safety.
- Gate verdict: PASS.
