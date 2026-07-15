# Context Pack: SWU-OV1-005

- Task: `SWU-OV1-005` - Derive Exact V0 Revision
- Mode: standard
- Handoff: none; local Task Session execution
- Strict coverage: pass
- Gate verdict: pass
- Runtime: local
- Dependency receipt: `../20260714T215322Z-swu-ov1-004-resume/TASK-SESSION-RESULT.md`

## Obligation Matrix

| ID | Obligation | Source | Status |
| --- | --- | --- | --- |
| O1 | Admit only the strict derivation request and enforce the 5 MiB HTTP limit. | task contract, accepted schema | covered |
| O2 | Serialize reconciliation, idempotency lookup, source admission, blob write, and event append. | task contract, server mutation queue | covered |
| O3 | Normalize fixed semantic fields and bind one derivation key to one SHA-256 input digest/outcome. | task contract, architecture | covered |
| O4 | Resolve an existing named V0 surface/revision without requiring current selection. | task contract, V3 projection | covered |
| O5 | Read through canonical workspace admission and require exact revision digest plus 4 MiB source limit. | task contract, canvas reader, frozen limits | covered |
| O6 | Return `source_revision_unavailable` before blob/event on missing, drifted, oversized, or unreadable source bytes. | task contract | covered |
| O7 | Store exact bytes before appending `canvas.operations_surface_derived`. | blob/replay substrate | covered |
| O8 | Return separate Operations surface/revision identity without mutating or redirecting V0. | architecture, projector | covered |
| O9 | Same key/same digest returns the original result; same key/different digest conflicts. | task contract | covered |
| O10 | Preserve orphan residue on append failure and reconciliation-required semantics after append. | storage contract | covered |
| O11 | Expose POST derive, GET surface, and one bounded CLI derive command. | task contract | covered |
| O12 | Prove exact bytes, historical source, idempotency, conflict, drift, limits, crashes, restart, and V0 parity. | task validation | covered |

## Implementation Shape

- Add `src/kernel/operations.mjs` as a pure derivation planner/projector helper.
- The service accepts injected clock/id generation for deterministic tests but
  production uses UUID-backed Operations surface and revision ids.
- Canonical normalized input is fixed-order JSON containing
  `schema_version`, `source_v0_surface_id`, `source_revision_id`, and
  `operation_surface_idempotency_key`; its SHA-256 is the replayed
  `normalized_input_digest`.
- `src/server.mjs` wires one Canvas blob store into persistence, performs all
  derivation effects inside the existing mutation queue, and maps stable
  domain errors to HTTP outcomes.
- The POST response returns `surface`, `revision`, and `idempotent`; GET returns
  the same admitted metadata without reading mutable workspace bytes. An
  Operations content URL remains deferred to SWU-OV1-006.
- The CLI adds `derive` with source surface, source revision, and idempotency
  key options.

## Write Scope

- New `src/kernel/operations.mjs`.
- `src/server.mjs` derivation/blob-store wiring and routes.
- `scripts/session-bridge.mjs` derive command.
- Focused derivation API/CLI tests and `package.json` test command.
- Task Session and synchronized plan/Craft evidence.

## Excluded

- Replace, append, rebuild, content serving for Operations revisions,
  navigation, browser changes, retention deletion, V0 schema/route changes,
  and any implicit synchronization from later V0 publications.

## Context Builder Result

- Files selected: task contract, W2, architecture derivation contract, V0
  canvas admission, server mutation/storage boundary, CLI, schemas, replay and
  prior receipt
- Obligation coverage: 12/12, 100 percent
- Strict coverage: pass
- Blockers: 0
- Fallback search: none
- Noise: bounded to exact derivation and read metadata
