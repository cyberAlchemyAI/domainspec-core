# Context Pack - TASK-BWO-002 Durable Auth/Profile Store

Task: `TASK-BWO-002`
SWUs: `SWU-BWO-004`, `SWU-BWO-005`, `SWU-BWO-006`
Mode: `standard`
Strict coverage: `pass`
Session evidence: `projects/body-war/development/task-sessions/20260621T045959Z-task-bwo-002-durable-auth-store/`

## Objective

Add a production-oriented Postgres auth store adapter and schema definition for
`projects/auth-user-management`, with tests that prove durable auth/provider
state semantics without exposing provider tokens to public reads.

## Obligations

| Obligation | Status | Evidence |
| --- | --- | --- |
| Implement a Postgres adapter for the `AuthStore` interface. | covered | `auth.types.ts`, `json-store.ts`, `memory-store.ts` |
| Include session, OAuth state, user/principal, provider account, provider token, access token, and audit records. | covered | `AuthStore` method list and adoption guide storage list |
| Add migration/schema definition. | covered | Task plan and infra architecture require Postgres-backed online state |
| Add store-level tests for token custody, state expiry/consumption, session revocation, and no-token public reads. | covered | existing store and Strava tests |
| Preserve TypeScript runtime policy and avoid app/VPS mutation. | covered | runtime-language policy and task scope |

## Selected Sources

| Source | Selector | Obligation |
| --- | --- | --- |
| `projects/body-war/development/refinement-runs/20260621T043947Z-online-auth-profile-vps-refine/stages/S09-INVOKE-PLAN.md` | `TASK-BWO-002`, SWUs 004-006 | task contract |
| `projects/auth-user-management/src/modules/auth/domain/auth.types.ts` | `AuthStore`, records | adapter contract |
| `projects/auth-user-management/src/modules/auth/infrastructure/json-store.ts` | persistence semantics, `consumeOAuthState` behavior | local reference |
| `projects/auth-user-management/src/modules/auth/infrastructure/memory-store.ts` | clone and lookup semantics | local reference |
| `projects/auth-user-management/src/modules/auth/application/auth.use-cases.ts` | create/authenticate/revoke session behavior | session semantics |
| `projects/auth-user-management/src/modules/providers/strava/application/strava.use-cases.ts` | provider account/token custody behavior | provider semantics |
| `projects/auth-user-management/tests/json-store.test.ts` | existing store test pattern | test style |
| `projects/auth-user-management/tests/strava-provider.test.ts` | token custody assertion pattern | test style |
| `projects/auth-user-management/docs/ADOPTION.md` | production storage requirements and no-token public reads | product/security |

## Controlling Constraints

- Use TypeScript only.
- Do not add Python runtime/tests.
- Do not mutate VPS, deploy scripts, or Strava configuration.
- Avoid forcing a concrete Postgres package dependency if the adapter can safely
  depend on a small query-client interface.
- Store provider tokens server-side, but never expose them through provider
  account/public connection reads.

## Decisions

| Decision | Selection | Classification |
| --- | --- | --- |
| Postgres dependency | Adapter accepts an injected `{ query(sql, values) }` client. | assumption |
| Schema format | Export schema SQL from the adapter module. | assumption |
| Record model | Store typed records as JSONB plus lookup columns. | assumption |
| OAuth consume semantics | Atomic `UPDATE ... WHERE NOT consumed` returning original record. | assumption |

No blocker-level decision is required before implementation.

## Write Scope

- `projects/auth-user-management/src/modules/auth/infrastructure/postgres-store.ts`
- `projects/auth-user-management/src/modules/auth/infrastructure/index.ts`
- `projects/auth-user-management/tests/postgres-store.test.ts`
- `projects/auth-user-management/docs/ADOPTION.md`
- `projects/body-war/development/task-sessions/20260621T045959Z-task-bwo-002-durable-auth-store/`

## Validation Surface

- `npm --prefix projects/auth-user-management run check`
- `bash tools/check-runtime-language-policy.sh`
- JSON validation for `context-index.json`
- ASCII scan over touched files
- trailing whitespace scan over touched files
- targeted scan for accidental token/secret literals in tracked docs/source/tests

## Handoff

Proceed locally. Stop before app integration or production deployment.
