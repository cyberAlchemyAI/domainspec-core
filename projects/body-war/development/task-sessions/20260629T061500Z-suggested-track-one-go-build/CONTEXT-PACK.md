# Context Pack: SuggestedTrack One-Go Build

## Context Pack Summary

- Task: `HND-SUGGESTED-TRACK-ONE-GO-BUILD-001`
- Mode: standard
- Files selected: 14
- Snippets selected: 18
- Obligation coverage: 100%
- Output index: `context-index.json`
- Strict coverage: pass
- Blockers: 0

## Obligations

| ID | Obligation | Coverage |
| --- | --- | --- |
| O1 | Preflight the stale W0/work-pack mutation gate before app mutation. | `WORK-PACK.md`, Refine handoff |
| O2 | Add SuggestedTrack docs and status/API/UI/test contracts. | New aspect docs under `docs/features/parque-taquaral-online-mvp/` |
| O3 | Add Drizzle/Postgres schema and generated migration. | `schema.ts`, `drizzle/0001_lyrical_living_mummy.sql` |
| O4 | Seed `Volta do Taquaral` as `needs_evidence` idempotent data. | Memory and Drizzle repository `ensureDefaultSuggestedTracks` |
| O5 | Add API/UI for connected-runner list/create/help/evidence attach. | `server.ts`, static UI files |
| O6 | Preserve live Strava consult, explicit consent, redacted persistence, and no source-backed/pilot-ready overclaim. | API tests, e2e, UI tests |
| O7 | Do not reuse legacy JSON-file `/api/submissions` as new evidence-candidate store. | New repository-backed `/api/suggested-tracks/*/evidence-candidates` |
| O8 | Run required validation commands. | `TASK-SESSION-RESULT.md` |

## Included Context

- `projects/body-war/development/refinement-runs/20260629T050046Z-suggested-track-decision-build-route/RUNTIME-HANDOFF.md` - confirmed route target, decision defaults, required validation commands.
- `projects/body-war/development/refinement-runs/20260629T050046Z-suggested-track-decision-build-route/stages/S09-INVOKE-PLAN.md` - write scope, SWUs, acceptance checks.
- `projects/body-war/development/refinement-runs/20260629T050046Z-suggested-track-decision-build-route/stages/S06-INVOKE-DESIGN.md` - component and workflow design.
- `projects/body-war/docs/features/parque-taquaral-online-mvp/WORK-PACK.md` - stale W0 gate and preflight target.
- `projects/body-war/app/src/infrastructure/postgres/schema.ts` - existing Drizzle schema extension point.
- `projects/body-war/app/src/auth/body-war-repository.ts` - repository contract extension point.
- `projects/body-war/app/src/auth/memory-repository.ts` - memory backend for tests.
- `projects/body-war/app/src/auth/drizzle-repository.ts` - Postgres backend for e2e/runtime.
- `projects/body-war/app/src/auth/strava-oauth.ts` - runner role permission seeding.
- `projects/body-war/app/server.ts` - HTTP route and auth/CSRF/origin boundary.
- `projects/body-war/app/static/index.html` - connected-runner UI surface.
- `projects/body-war/app/static/app.js` - browser controller.
- `projects/body-war/app/tests/auth-consumer.test.ts` - Node API/privacy tests.
- `projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts` - Playwright UI evidence.

## Gate Verdict

Pass. The work-pack mutation gate was updated first, the app mutation stayed
inside the declared write scope, and source-backed geometry/pilot-ready status
remain deferred.
