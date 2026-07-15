# Context Pack: SWU-OV1-008

- Task: `SWU-OV1-008` - Exact Workspace Rebuild
- Mode: standard
- Handoff: none; local Task Session execution
- Strict coverage: pass
- Gate verdict: pass
- Runtime: local
- Dependency receipt: `../20260714T223240Z-swu-ov1-007/TASK-SESSION-RESULT.md`

## Obligation Matrix

| ID | Obligation | Status |
| --- | --- |
| O1 | Reuse operation normalization/id lookup and CAS before workspace admission. | covered |
| O2 | Admit only schema-valid relative HTML path and expected SHA-256 input. | covered |
| O3 | Read through existing canonical workspace helper and reject missing, directory, or external-link targets. | covered |
| O4 | Require read-byte digest to equal caller expected digest. | covered |
| O5 | Enforce 4 MiB source and 8 MiB serialized-result limits. | covered |
| O6 | Require lossless UTF-8 and parse/serialize one complete document with parse5 8.0.1. | covered |
| O7 | Store exact result blob before the normal V4 content event. | covered |
| O8 | Record source lineage kind, normalized path, and expected digest. | covered |
| O9 | Preserve Operations surface id and append one ordered revision. | covered |
| O10 | Same-id retry survives later source changes; conflict/stale input commits nothing. | covered |
| O11 | Later V0 publication never invokes rebuild or changes Operations identity/content. | covered |
| O12 | Prove path/hash/limit/lineage/retry/crash matrix plus inherited L0/L1 and V0 suites. | covered |

## Implementation Shape

- Extend the generic operation service `rebuild` branch; routes and CLI remain
  unchanged.
- Normalize workspace input as kind, path, and expected digest; use the
  expected digest as `input_digest` and event lineage binding.
- Map canonical read failures to `rebuild_source_unavailable`, digest mismatch
  to `rebuild_source_changed`, invalid UTF-8 to the existing 422 source error,
  and byte limits to existing stable limit responses.

## Write Scope

- `src/kernel/operations.mjs` rebuild branch.
- `src/server.mjs` stable rebuild error mapping.
- Focused rebuild tests and package command.
- Task Session and synchronized plan/Craft evidence.

## Excluded

- Navigation/display routes, browser frame changes, refresh/ack, retention,
  regions, implicit sync, and any V0 mutation.

## Context Builder Result

- Obligation coverage: 12/12, 100 percent
- Strict coverage: pass
- Blockers: 0
- Fallback search: none
- Noise: bounded to exact rebuild and inherited evidence
