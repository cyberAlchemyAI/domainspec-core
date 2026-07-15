# Context Pack: SWU-OV1-014

- Task: `SWU-OV1-014` - Integrated Audit And Plan Synchronization
- Mode: standard closure-only VERIFY unit
- Runtime: local Node, schema validator, Playwright Chromium, dispatch validator
- Dependency receipt: `../20260715T010547Z-swu-ov1-013-resume/TASK-SESSION-RESULT.md`
- Gate verdict: pass

## Obligation Matrix

| ID | Obligation | Status |
| --- | --- | --- |
| A1 | Confirm SWU-OV1-013 machine evidence and human Option 1 review passed. | covered |
| A2 | Run all focused Operations V1 Node suites. | covered |
| A3 | Run inherited V0 canvas, bridge, persistence, runtime-schema, schema, and workbench suites. | covered |
| A4 | Run all Playwright desktop/mobile journeys. | covered |
| A5 | Validate schemas and the Operations V1 dispatch with deterministic tools. | covered |
| A6 | Validate retained JSON/JSONL evidence and fixture parseability. | covered |
| A7 | Map every OV1-D1-D9 and OVG-001-004 obligation to retained evidence. | covered |
| A8 | Prove V0 compatibility and absence of protected-effect/region expansion. | covered |
| A9 | Classify all remaining gaps without inflating the closure claim. | covered |
| A10 | Review the scoped diff while preserving unrelated worktree changes. | covered |
| A11 | Synchronize work-pack, wave, task, traceability, Task Session, and Craft evidence only after pass. | covered |

## Command Matrix

- Focused Operations Node: all `tests/operations-v1-*.test.mjs` with serial
  execution.
- Inherited Node: V0 canvas, manual bridge, persistence, runtime-schema,
  schema-validation, artifact/adversarial, and workbench suites.
- Browser: `npm run test:e2e` for every configured desktop/mobile journey.
- Schema: `npm run validate:schemas` and `npm run test:schemas`.
- Dispatch: `python3 .agents/skills/dispatch-spec/scripts/validate-dispatch.py
  projects/ide-extension/development/operations-v1-plan/operations-v1-plan.dispatch.json
  --json` from the repository root.
- Data: parse all project JSON and line-by-line JSONL fixtures/evidence selected
  by the audit; verify Craft ledger/index hash separately.
- Scope: `git diff --check -- projects/ide-extension` plus scoped status review.

## Write Scope

- tests only for a regression proven by the audit
- `development/operations-v1-plan/work-pack/shared/traceability.md`
- Operations V1 work-pack, W6, and task status/evidence
- this Task Session's integrated report and PASS/BLOCK receipt
- Craft canonical ledger, generated index, and human view

Product/design authority and unrelated dirty worktree changes are read-only.

## Context Builder Result

- Obligation coverage: 11/11
- Strict coverage: pass
- Blocking decisions: 0
- Dependency: pass
- Fallback search: none
- Residue entering audit: `GAP-OV1-006`, the inherited V0 matrix assertion that
  treats the intentional `/api/craft/frontier` route as forbidden

