# Context Pack: SWU-OV1-004 Resume

- Task: `SWU-OV1-004` - Additive Event V4 And Reference Reconciliation
- Mode: standard
- Handoff: none; local Task Session execution
- Strict coverage: pass
- Gate verdict: pass
- Runtime: local
- Prior blocked run: `../20260714T214740Z-swu-ov1-004/TASK-SESSION-RESULT.md`

This file is resumed session evidence. It is not a canonical planning or
contract source.

## Gate Resolution

The human selected Decision Gate Option 1 on 2026-07-14:

- V4 reuses `canvas.interaction_recorded`.
- `event_version` distinguishes the existing V0/V3 interaction binding from
  the Operations V1/V4 binding.
- The Operations V1 event vocabulary migrates from five to six names before
  projector/storage implementation.

## Obligation Matrix

| ID | Obligation | Status |
| --- | --- | --- |
| O1 | Admit event version 4 without changing V1/V2/V3 reducers or legacy projections. | covered |
| O2 | Add strict reducers for derivation, operation, display, pruning request, prune tombstone, and V4 interaction events. | covered |
| O3 | Reuse `canvas.interaction_recorded` in V4 under an explicit SWU-001 contract migration. | resolved by human Option 1 |
| O4 | Enforce exact keys, id/digest bindings, unique keys/operations, ordered lineage, current revision, and tombstone consistency. | covered |
| O5 | Keep Operations V1 state nested under Canvas while preserving V0 fields. | covered |
| O6 | Verify every unpruned Operations revision through the blob store after pure reduction. | covered |
| O7 | Fail closed on missing/corrupt references and report unreferenced blobs as residue. | covered |
| O8 | Preserve blob-before-event ordering and reconciliation-required projection failure semantics. | covered |
| O9 | Cover legacy, mixed, hostile, restart, orphan, missing/corrupt, and projection-failure cases. | covered |
| O10 | Keep HTTP, CLI, browser, and event-producing routes read-only. | covered |
| O11 | Run focused replay plus Canvas, bridge, and persistence suites. | covered |
| O12 | Synchronize a PASS receipt before SWU-OV1-005. | covered |

## Event And Projection Decisions

- `canvas.operations_v1` owns derivation keys, operation surfaces, immutable
  revisions, operation records, redirect commands/display target, pruning
  state, tombstones, and Operations interaction cursor/history.
- V4 derivation and operation events carry strict metadata records, surface
  snapshots, and revision records. HTML never enters the event log.
- Operations revisions use immutable `content_sha256`, `blob_ref`,
  `byte_length`, and `committed_at` fields.
- Content operations bind normalized request digest, source/result revisions,
  mode, whole-document target, input digest, optional rebuild lineage, result
  digest/ref, and commit time.
- Display, pruning, and V4 interaction shapes are frozen now so later routes
  emit against replay authority rather than redefining it.
- Storage requires a Canvas blob store whenever V4 contains unpruned revisions;
  pure `reduceEvents()` remains synchronous and filesystem-free.

## Controlling Sources

The 14 grouped sources and selectors in the prior blocked
`CONTEXT-PACK.md` remain controlling. The selected Decision Gate and
`EVENT-V4-MIGRATION.md` resolve its only uncovered obligation.

## Write Scope

- `src/kernel/operations-contracts.mjs` and its focused test for the approved
  six-name vocabulary migration.
- `src/kernel/projector.mjs`.
- `src/kernel/storage.mjs`.
- V4 event fixtures and focused replay/recovery tests.
- `package.json` only for `test:operations-replay`.
- Task Session and synchronized planning/Craft evidence.

## Excluded

- Routes, CLI, browser/UI, event producers, retention deletion, and operation
  services.

## Context Builder Result

- Files selected: 14 grouped sources plus 2 gate/migration artifacts
- Obligation coverage: 12/12, 100 percent
- Strict coverage: pass
- Blockers: 0
- Fallback search: none
- Noise: bounded to replay, storage reconciliation, and migration evidence
