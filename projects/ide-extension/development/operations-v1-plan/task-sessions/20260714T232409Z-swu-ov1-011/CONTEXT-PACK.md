# Context Pack: SWU-OV1-011

- Task: `SWU-OV1-011` - Diagnostics, Grace, Preview, And Manual Prune
- Mode: standard
- Handoff: none; local Task Session execution
- Strict coverage: pass
- Gate verdict: pass
- Runtime: local plus real Chromium
- Dependency receipt: `../20260714T230133Z-swu-ov1-010/TASK-SESSION-RESULT.md`

## Obligation Matrix

| ID | Obligation | Status |
| --- | --- | --- |
| O1 | Keep fixed production defaults at 1 GiB soft, 2 GiB hard, seven-day grace, and reclaim below soft; tests may inject smaller values. | covered |
| O2 | Derive diagnostics only after successful full replay and blob-reference validation. | covered |
| O3 | Report total, unique referenced, orphan, and largest-blob bytes plus thresholds, state, deadline, eligible count, and blocked reason. | covered |
| O4 | Crossing soft creates exactly one durable `canvas.pruning_requested` grace request; below soft creates no event. | covered |
| O5 | Preview uses the strict existing request schema and binds command identity to deterministic normalized input. | covered |
| O6 | Protect every current Operations revision, every already-pruned revision, and any displayed Operations revision. | covered |
| O7 | Sort eligible history by committed time then revision id and account for shared content-addressed blob references. | covered |
| O8 | Hash event cursor, fixed policy, active request, and selected revision ids into a stable candidate digest. | covered |
| O9 | Manual commit runs under the server mutation queue, recomputes candidates, and rejects stale digest or command conflicts. | covered |
| O10 | Append one durable `canvas.revision_pruned` tombstone before each body deletion. | covered |
| O11 | Delete a body only when no remaining unpruned revision references its digest. | covered |
| O12 | Stop on append failure; retain committed tombstones and all un-tombstoned bodies. | covered |
| O13 | A delete failure retains the tombstone and exposes explicit residue for recovery instead of restoring false availability. | covered |
| O14 | Pruned content returns stable `410 revision_pruned` metadata. | covered |
| O15 | Exact retry of a pruned operation returns original metadata plus `operation_result_pruned` and never reruns. | covered |
| O16 | Workbench shows storage/grace state and provides preview plus explicit manual prune controls without automatic confirmation. | covered |
| O17 | Existing V0, Operations mutation, navigation, replay, browser, and approval/bridge behavior remains compatible. | covered |
| O18 | Focused tests cover diagnostics, grace idempotency, deterministic/stale preview, shared/current/display protection, partial failure, 410, retry, restart, and UI notice/control. | covered |

## Implementation Shape

- Add one retention coordinator beside the existing blob, persistence, and
  Operations services. It receives policy and clock dependencies for tests but
  keeps production defaults fixed.
- Extend the blob store with exact-digest deletion and preserve its injected
  filesystem boundary for failure tests.
- Keep candidate derivation pure over a successful reconciliation snapshot.
- Let `GET /api/canvas/storage` evaluate and durably open grace when needed;
  preview and commit remain explicit POST commands.
- Broadcast a typed storage notice when grace opens or manual pruning changes
  state; browser notices always refetch authoritative diagnostics.
- Reuse the V4 pruning event shapes already enforced by the projector.

## Write Scope

- `src/kernel/canvas-retention.mjs` and focused tests.
- Minimal blob-store delete, Operations retry, server route/service wiring, and
  workbench storage controls.
- Existing pruning request schemas only if a proven contract defect appears;
  otherwise preserve them exactly.
- Package scripts plus Task Session and synchronized plan/Craft evidence.

## Excluded

- Automatic orphan deletion, stale temporary cleanup, startup or post-commit
  evaluation hooks, deadline timers, hard-threshold reclamation, environment
  policy overrides, configurable production defaults, queues, browser
  identities, regions, and hostile HTML containment claims. These are either
  SWU-012 work or outside Operations V1.

## Context Builder Result

- Obligation coverage: 18/18, 100 percent
- Strict coverage: pass
- Blockers: 0
- Fallback search: none
- Noise: bounded to retention policy, durable pruning, storage diagnostics, and
  workbench controls
