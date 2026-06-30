---
stage_id: s09-invoke-plan
capability_ref: invoke
mode: plan
status: pass
next_route: task-session
---

# S09 Invoke Plan

## Plan Summary

Route to one bounded `task-session` after Refine final synthesis:

```text
SuggestedTrack one-go build
```

## Complexity

`medium`: touches docs, schema/migration, seed, API, UI, tests, and protected
Strava activity evidence boundaries.

## Task Session Write Scope

- `projects/body-war/docs/features/parque-taquaral-online-mvp/SPEC.md`
- `projects/body-war/docs/features/parque-taquaral-online-mvp/domain.md`
- `projects/body-war/docs/features/parque-taquaral-online-mvp/states.md`
- `projects/body-war/docs/features/parque-taquaral-online-mvp/interfaces.md`
- `projects/body-war/docs/features/parque-taquaral-online-mvp/operations.md`
- `projects/body-war/docs/features/parque-taquaral-online-mvp/queries.md`
- `projects/body-war/docs/features/parque-taquaral-online-mvp/ui-spec.md`
- `projects/body-war/docs/features/parque-taquaral-online-mvp/TEST-SPEC.md`
- `projects/body-war/docs/features/parque-taquaral-online-mvp/WORK-PACK.md`
- `projects/body-war/app/src/infrastructure/postgres/schema.ts`
- `projects/body-war/app/src/infrastructure/postgres/migrations.ts`
- `projects/body-war/app/src/infrastructure/postgres/database.ts`
- `projects/body-war/app/drizzle/*`
- `projects/body-war/app/server.ts`
- `projects/body-war/app/static/index.html`
- `projects/body-war/app/static/app.js`
- `projects/body-war/app/static/styles.css`
- `projects/body-war/app/tests/*`
- `projects/body-war/app/e2e/*`

## Smallest Working Units

| SWU | Goal | Dependencies | Validation |
| --- | --- | --- | --- |
| SWU-SGT-001 | Preflight docs/gate update: record selected decision slate and one-go gate in feature docs/work-pack. | Refine final result. | Markdown review; no app mutation before this passes. |
| SWU-SGT-002 | Add SuggestedTrack and evidence-candidate Drizzle schema plus generated migration. | SWU-SGT-001. | `npm --prefix projects/body-war/app run db:generate`; schema review. |
| SWU-SGT-003 | Add idempotent Volta do Taquaral seed as `needs_evidence`. | SWU-SGT-002. | seed test or migration/bootstrap review. |
| SWU-SGT-004 | Add SuggestedTrack API and evidence attach contract. | SWU-SGT-002, SWU-SGT-003. | API tests for auth, validation, redaction, consent. |
| SWU-SGT-005 | Add connected-runner UI for suggestion list/create/help flow. | SWU-SGT-004. | UI smoke and copy review. |
| SWU-SGT-006 | Run full validation and update receipts. | SWU-SGT-001..005. | validation commands below. |

## Validation Commands

Run as available in `projects/body-war/app`:

```bash
npm --prefix projects/body-war/app run validate
npm --prefix projects/body-war/app test
npm --prefix projects/body-war/app run e2e
npm --prefix projects/body-war/app run test:ui
```

`test:ui` may be recorded as blocked only when browser dependencies are missing;
the Task Session must then record the exact blocker.

## Acceptance Checks

- SuggestedTrack statuses are documented and implemented without source-backed
  overclaim.
- Activity consult is live/ephemeral.
- Evidence candidate persistence stores redacted summaries and consent metadata,
  not raw provider payloads.
- Legacy JSON-file `/api/submissions` is not reused as the new evidence store.
- Taquaral seed is data, not a hardcoded one-off UI branch.
- Work-pack/Craft state is updated with the new route result and any residue.

## Next Route

`task-session` on `HND-SUGGESTED-TRACK-ONE-GO-BUILD-001`.

