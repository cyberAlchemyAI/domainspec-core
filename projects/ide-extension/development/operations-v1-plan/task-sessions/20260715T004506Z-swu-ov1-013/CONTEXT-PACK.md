# Context Pack: SWU-OV1-013

- Task: `SWU-OV1-013` - CLI And Interactive Value Witness
- Mode: standard
- Handoff: none; local Task Session execution
- Strict coverage: pass for machine work
- Gate verdict: pass for implementation; human review required after witness
- Runtime: local plus Playwright Chromium
- Dependency receipt: `../20260715T002431Z-swu-ov1-012-resume/TASK-SESSION-RESULT.md`

## Obligation Matrix

| ID | Obligation | Status |
| --- | --- | --- |
| O1 | Preserve all existing bridge and Canvas CLI commands/exit classes. | covered |
| O2 | Expose machine-readable `derive`, `operate`, `navigate`, `storage`, and `prune` commands. | covered |
| O3 | Route every command through existing HTTP schemas, limits, hashes, CAS, and path admission. | covered |
| O4 | Create complete interactive presentation HTML in a temporary project. | covered |
| O5 | Publish unchanged V0, then derive an exact Operations V1 surface. | covered |
| O6 | Commit a whole-document replace or rebuild and then one visible append with fresh ids/CAS. | covered |
| O7 | Redirect the durable workbench target to the final revision and observe exact acknowledgement. | covered |
| O8 | Interact inside the iframe and prove the generic message enters the V4 interaction projection. | covered |
| O9 | Restart server/browser connection and recover the same target and immutable content. | covered |
| O10 | Retain exact CLI JSON, event/revision/digest evidence, desktop/mobile screenshots, and report. | covered |
| O11 | Preserve V0 and kernel semantics; fix core code only for a proven CLI binding defect. | covered |
| O12 | Stop for explicit human usefulness review after machine proof; never simulate approval. | covered |

## Selected Command Contract

- `derive` and `operate` retain their existing shapes.
- `navigate --input <json|->` submits one exact navigation request.
- `storage` reads `GET /api/canvas/storage` and accepts only `--base-url`.
- `prune --action preview|commit --input <json|->` submits the exact command
  request to the matching pruning route.
- JSON remains the only stdout result. Usage/connection/unavailable/rejected
  exit classes remain unchanged.

## Write Scope

- `scripts/session-bridge.mjs`
- focused CLI/value tests and package test scripts
- one Operations V1 Playwright witness
- this Task Session's retained evidence/screenshots/report
- work-pack/Craft synchronization after machine evidence

Kernel/projector/storage/retention semantics are read-only unless the CLI
witness proves an existing binding defect.

## Context Builder Result

- Obligation coverage: 12/12
- Strict coverage: pass for machine execution
- Blockers before mutation: 0
- Deferred blocker: explicit post-witness human usefulness verdict
- Fallback search: none
- Noise: bounded to SWU-OV1-013 CLI and value evidence
