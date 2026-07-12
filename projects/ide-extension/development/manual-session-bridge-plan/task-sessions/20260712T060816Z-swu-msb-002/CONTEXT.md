# Context Pack: SWU-MSB-002

## Selection

- Work-pack: `projects/ide-extension/development/manual-session-bridge-plan/WORK-PACK.md`
- Task: `TASK-CONTRACT-MIGRATION`
- SWU: `SWU-MSB-002`
- Dependency receipt: `task-sessions/20260712T055820Z-swu-msb-001/TASK-SESSION-RESULT.md`
- Runtime: local Codex / Task Session
- Strict runtime handoff: not requested

## Controlling Sources

1. SWU-002 task contract: version dispatch, immutable v1 result, complete legal
   v2 transitions, singleton target, authorization lifetime, attempt history,
   restart stability.
2. SWU-001 schemas: v2 envelope, approval, authorization/execution receipts,
   and bridge request bindings.
3. Approved architecture event contracts and decision-gate recovery policy.
4. Current projector/storage/audit modules and persistence/lifecycle tests.

## Brownfield Baseline

- `EVENT_VERSION` is 1 and the projector accepts three event types.
- Pure v1 projections are consumed by existing server, restart, artifact, and UI tests.
- Storage already derives projection from the append-only event log before append
  and on reconcile; audit already preserves mixed JSON objects without rewriting.
- Full Node baseline after SWU-001: 58/58 pass.

## Execution Decision

- Preserve `EVENT_VERSION = 1` for current server emission and add
  `BRIDGE_EVENT_VERSION = 2` for later bridge writers.
- Dispatch v1 and v2 reducers explicitly; never infer version from event shape.
- Keep pure-v1 `createInitialWorkbench()` output field-for-field unchanged.
- Add `bridge` projection state only when the first v2 event is reduced.
- Represent attempts as immutable claim IDs in `claim_order` plus a claim map;
  release updates that claim and a later attempt receives a new ID.
- Keep result and execution receipt in one `bridge.result_recorded` event so a
  projected terminal state cannot exist without its receipt.

## Gates

- Dependency 001: pass.
- Approved decisions: pass; no unresolved choice.
- Storage/audit compatibility: existing append/reconcile path is sufficient;
  no file rewrite or migration required.
- Write scope: projector, focused replay fixtures/tests, package script, and
  task evidence only.
- Gate verdict: PASS.

## Done Evidence Required

- Checked-in v1 event fixture reduces to checked-in expected projection exactly.
- Mixed v1/v2 replay succeeds without mutating source events.
- Legal prepare -> authorize -> ready -> claim -> terminal and interrupted ->
  release -> ready -> new claim paths pass.
- Duplicate target/event/claim/result, stale unready/release, unknown version,
  and wrong binding fail closed.
- Storage reconcile produces identical checksum/state after restart.
