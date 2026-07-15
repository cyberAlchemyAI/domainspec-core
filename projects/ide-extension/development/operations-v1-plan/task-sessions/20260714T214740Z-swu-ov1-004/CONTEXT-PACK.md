# Context Pack: SWU-OV1-004

- Task: `SWU-OV1-004` - Additive Event V4 And Reference Reconciliation
- Mode: standard
- Handoff: none; local Task Session execution
- Strict coverage: block
- Gate verdict: block
- Runtime: local

This file is session evidence. It is not a canonical planning or contract
source.

## Objective

Extend replay with additive Operations V1 event version 4 and reconcile every
unpruned committed body reference against the content-addressed blob store,
while leaving V1/V2/V3 projections exact and adding no routes, CLI, or browser
behavior.

## Obligation Matrix

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| O1 | Admit event version 4 without changing V1/V2/V3 reducers or legacy projections. | Task contract; existing projector compatibility tests. | covered |
| O2 | Add strict reducers for derivation, committed operation, display target, pruning request, and prune tombstone events. | Task contract event vocabulary and projected state. | covered |
| O3 | Admit the Operations V1 interaction event required by SWU-004/SWU-010 under the frozen V4 vocabulary. | TASK-BLOB-REPLAY; TASK-REBUILD-NAVIGATION; SWU-OV1-001 constants. | block: vocabulary contradiction |
| O4 | Enforce exact keys, id/digest bindings, unique derivation keys and operation ids, ordered lineage, current revision, and tombstone consistency. | Task replay algorithm; existing projector style. | covered |
| O5 | Keep Operations V1 state nested under Canvas while preserving V0 surfaces, revisions, current id, and interactions. | Task projected state; shared V0 contract. | covered |
| O6 | After pure reduction, verify every unpruned Operations revision through the blob store. | Task replay algorithm; architecture dependency contract. | covered |
| O7 | Fail closed on missing/corrupt references; report unreferenced blobs as safe residue rather than rejecting replay. | Task edge cases; SWU-OV1-003 diagnostics. | covered |
| O8 | Preserve blob-before-event ordering and reconciliation-required semantics after projection write failure. | Architecture; existing storage contract. | covered |
| O9 | Cover exact V1/V2/V3, mixed V3/V4, unknown V4, duplicate/binding errors, missing/corrupt body, orphan body, restart repair, and projection failure. | Task edge-case matrix. | covered |
| O10 | Keep HTTP, CLI, browser, and event-producing routes read-only. | Exact write scope. | covered |
| O11 | Run focused replay plus existing Canvas, bridge, and persistence suites. | Task validation. | covered |
| O12 | Synchronize a PASS receipt before SWU-OV1-005. | Work-pack gate 2. | blocked by O3 |

## Selected Context

1. `development/operations-v1-plan/WORK-PACK.md`
   - Selectors: SWU-004 row, gate checks, blockers/gaps, next route.
   - Covers: O10-O12.
2. `development/operations-v1-plan/work-pack/tasks/TASK-BLOB-REPLAY.md`
   - Selector: `SWU-OV1-004` event vocabulary and replay algorithm.
   - Covers: O1-O12.
3. `development/operations-v1-plan/work-pack/waves/W1.md`
   - Selectors: exit, promotion, stop.
   - Covers: O6-O9, O11, O12.
4. `development/operations-v1-plan/task-sessions/20260714T214040Z-swu-ov1-003/TASK-SESSION-RESULT.md`
   - Selectors: PASS result, blob API, reroute.
   - Covers: O6-O9, O12.
5. `src/kernel/projector.mjs`
   - Selectors: version header, lazy Canvas state, strict V3 reducers, checksum.
   - Covers: O1, O4, O5, O9.
6. `src/kernel/storage.mjs`
   - Selectors: `reconcile`, `commitEvent`, projection failure semantics.
   - Covers: O6-O9.
7. `src/kernel/audit.mjs`
   - Selectors: append/read history integrity.
   - Covers: O8, O9.
8. `src/kernel/canvas-blobs.mjs`
   - Selectors: verified read and deterministic diagnostics.
   - Covers: O6, O7, O9.
9. `src/kernel/operations-contracts.mjs`
   - Selector: frozen five-name `OPERATIONS_V1_EVENT_TYPES` array.
   - Covers: O2, exposes O3 contradiction.
10. `tests/session-content-workbench-replay.test.mjs` and V3 event fixture
    - Selectors: exact legacy projection, mixed replay, hostile event tests.
    - Covers: O1, O5, O9, O11.
11. `development/operations-v1-plan/work-pack/tasks/TASK-DERIVE-REPLACE.md`
    - Selectors: derivation/operation event producers and retry bindings.
    - Covers: O2, O4, O8.
12. `development/operations-v1-plan/work-pack/tasks/TASK-REBUILD-NAVIGATION.md`
    - Selectors: durable display event and required V4 interaction record.
    - Covers: O2-O5.
13. `development/operations-v1-plan/work-pack/tasks/TASK-RETENTION.md`
    - Selectors: pruning request and tombstone semantics.
    - Covers: O2, O4, O6-O9.
14. `development/operations-v1-design/ARCHITECTURE-BUNDLE.md`
    - Selectors: operation record, storage namespaces, event-before-blob order.
    - Covers: O2, O4-O9.

## Blocking Contradiction

SWU-OV1-001 froze event version 4 with exactly five names:

1. `canvas.operations_surface_derived`
2. `canvas.content_operation_committed`
3. `canvas.display_target_selected`
4. `canvas.pruning_requested`
5. `canvas.revision_pruned`

The SWU-OV1-004 contract additionally requires an Operations V1 interaction
event, and SWU-OV1-010 explicitly requires that operations-surface
interactions use a V4 interaction record while V0 interactions remain V3.
Silently adding or omitting that event would invalidate one accepted contract.

## Non-Blocking Implementation Assumptions

- V4 state will be a nested `canvas.operations_v1` namespace so exact V3 Canvas
  fields remain compatible.
- Derivation and operation events will carry strict normalized record objects,
  complete revision metadata, and surface lineage; they will never carry HTML.
- Storage reconciliation will accept an injected Canvas blob store and verify
  only unpruned Operations V1 revisions after pure reduction.
- Unreferenced blobs remain diagnostics residue; missing/corrupt referenced
  blobs disable usable reconciliation.

## Write Scope After Gate Pass

- `src/kernel/projector.mjs`
- `src/kernel/storage.mjs`
- Focused V4 event fixtures and replay/recovery tests
- `package.json` only for `test:operations-replay`
- Task Session evidence and status synchronization

## Context Builder Result

- Files selected: 14 grouped entries
- Obligation coverage: 11/12 resolved; O3 blocked
- Strict coverage: block
- Blockers: 1
- Fallback search: no unresolved evidence search; contradiction is explicit
- Noise: bounded to projector/storage and downstream event owners
