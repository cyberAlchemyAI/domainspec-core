# Task Session Result: SWU-OV1-001

```yaml
swu_id: SWU-OV1-001
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: development/operations-v1-plan/task-sessions/20260714T211557Z-swu-ov1-001/TASK-SESSION-RESULT.md
files_touched:
  - package.json
  - src/kernel/operations-contracts.mjs
  - src/kernel/schema-validation.mjs
  - schemas/operations-surface-derive-request.schema.json
  - schemas/content-operation-request.schema.json
  - schemas/canvas-navigation-request.schema.json
  - schemas/canvas-navigation-ack-request.schema.json
  - schemas/canvas-pruning-preview-request.schema.json
  - schemas/canvas-pruning-commit-request.schema.json
  - tests/fixtures/schemas/
  - tests/l0-schema-validation.test.mjs
  - tests/operations-v1-contracts.test.mjs
validation:
  - npm run validate:schemas: pass
  - npm run test:schemas: pass
  - npm run test:operations-contracts: pass
  - npm run test:canvas-contracts: pass
  - npm run smoke: pass
  - npm run test:runtime-schemas: pass
  - npm run test:workbench: pass
  - Craft index source hash check: pass
  - Node syntax checks: pass
  - scoped git diff --check: pass
blockers: []
residue:
  - Navigation acknowledgement remains the deliberately minimal schema_version plus loaded-or-failed status contract selected in the context pack.
  - Unrelated concurrent worktree changes remain preserved outside this SWU.
reroute: SWU-OV1-002
handoff_note: Pin parse5 8.0.1 and freeze golden document and fragment serialization without adding durable state.
```

## Result

PASS. Operations V1 now has a strict, registered contract baseline without
adding routes, storage, event emission, parser behavior, or V0 API changes.

The implementation freezes:

- six request schemas for derivation, content operations, navigation,
  acknowledgement, pruning preview, and pruning commit;
- append and replace as inline whole-document operations, and rebuild as an
  exact-digest workspace HTML operation;
- 5 MiB HTTP, 4 MiB source, 512 KiB fragment, and 8 MiB result byte limits;
- 1 GiB soft, 2 GiB hard, seven-day grace, and reclaim-below-soft retention
  constants;
- event version 4 and five additive Operations V1 event names.

Twenty-two new schema fixtures bring the registered fixture corpus to 76.
Focused tests cover invalid fields, target and mode binding, digests, identifier
shapes, every byte limit at minus-one/exact/plus-one, and multibyte UTF-8 input.

## Decisions

- JSON Schema constrains request shape; runtime UTF-8 helpers remain the byte
  authority because JSON Schema string length counts characters, not bytes.
- The context-pack assumptions for acknowledgement and pruning request fields
  are frozen for V1. A later change requires an explicit contract migration.

## Validation Evidence

| Command | Result |
| --- | --- |
| `npm run validate:schemas` | PASS: 20 runtime schemas, 6 module manifests, and 76 schema fixtures. |
| `npm run test:schemas` | PASS: 6 tests. |
| `npm run test:operations-contracts` | PASS: 8 tests. |
| `npm run test:canvas-contracts` | PASS: 4 tests. |
| `npm run smoke` | PASS: 1 test. |
| `npm run test:runtime-schemas` | PASS: 6 tests. |
| `npm run test:workbench` | PASS: 6 tests, including stale-index refusal. |
| Craft index source hash check | PASS: generated index matches the canonical ledger. |
| Node syntax checks | PASS: constants and focused test modules parse. |
| Scoped `git diff --check` | PASS. |

The first schema validation run exposed fixture filenames that did not match
the repository's `.valid.` classifier; the fixtures were renamed and passed.
The first schema registry test exposed its explicit expected-name list; the six
new names and their base valid fixtures were added, then the suite passed.

## Session Metadata

- Context pack: [CONTEXT-PACK.md](CONTEXT-PACK.md)
- Strict context coverage: pass, 10/10 obligations
- Gate: pass
- Runtime: local
- Handoff: none
- Subagents: not applicable; started 0, completed 0, failed 0, blocked 0
- Experiment harness: not applicable
- Decision Gate Result: not applicable; inherited planning gate was already pass
- Next bounded unit: `SWU-OV1-002`

## Contract Migration

`OV1-EVENT-V4-M1` was human-approved on 2026-07-14 before any V4 route emitted.
It adds `canvas.interaction_recorded` as the sixth V4 event name, with event
version distinguishing the existing V3 binding from the Operations V1 binding.
See [EVENT-V4-MIGRATION.md](../20260714T215322Z-swu-ov1-004-resume/EVENT-V4-MIGRATION.md).
