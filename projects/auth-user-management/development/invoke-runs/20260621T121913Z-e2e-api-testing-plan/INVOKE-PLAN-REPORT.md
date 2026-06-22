# Auth User Management E2E API Testing Invoke Plan

## Invocation

- Run id: `20260621T121913Z-e2e-api-testing-plan`
- Mode: `/invoke plan`
- Target: `projects/auth-user-management`
- Request: plan end-to-end testing for the auth API, starting with Docker Compose, then container startup, then a full program that tests every API feature.
- Status: ready for `task-session`.

## Decision Summary

The first E2E target is the public TypeScript package API exported by `src/index.ts`, wired through the real Drizzle PostgreSQL adapter. This keeps the service reusable for Troqar, Savvy, and future projects without introducing an HTTP transport before that adapter is specified.

If an HTTP API is later required, it should be a separate adapter work-pack that consumes this package and reuses the same E2E scenario matrix.

## Current Evidence

- Package API export surface: `projects/auth-user-management/src/index.ts`.
- Use cases: `loginUseCase`, `issueAccessTokenUseCase`, `authenticateRequestUseCase`, `authorizeRequestUseCase`, `logoutUseCase`, `introspectTokenUseCase`, `getPermissionCatalogUseCase`, `seedSystemBootstrap`.
- PostgreSQL adapter: `createDrizzleAuthRepositories` and `authAccessControlSchema` under `src/infrastructure/drizzle-postgres`.
- Existing unit coverage: `tests/auth-access-control.test.ts` covers memory-backed behavior and fake Drizzle injection, but does not prove real PostgreSQL schema, inserts, updates, JSONB, enum handling, or token/session persistence.
- Architecture invariant carried forward: SQL persistence uses Drizzle with PostgreSQL; implementation code is shell where possible and TypeScript where program logic is needed.

## Planned Outputs

Implementation should add:

- `projects/auth-user-management/docker-compose.e2e.yml`
- `projects/auth-user-management/scripts/e2e.sh`
- `projects/auth-user-management/e2e/auth-api.e2e.ts`
- `projects/auth-user-management/e2e/postgres-schema.ts`
- `projects/auth-user-management/e2e/assertions.ts`
- `projects/auth-user-management/tsconfig.e2e.json`
- `projects/auth-user-management/package.json` script updates
- `projects/auth-user-management/package-lock.json` dependency updates
- `projects/auth-user-management/docs/ADOPTION.md` E2E usage note

Planning artifacts from this invoke pass:

- `IMPLEMENTATION-LAYERING.md`
- `API-E2E-SCENARIO-MATRIX.md`
- `WORK-PACK.md`
- `EXECUTION-PACK.md`
- `PLAN-TRANSPORT.md`

## Non-Goals

- No HTTP server, browser cookie session, OAuth, Strava, Troqar UI, or deployment mutation in this E2E pass.
- No mutation outside `projects/auth-user-management`, except optional parent-level status checks.
- No generated JavaScript source committed. Build outputs remain disposable unless the package already intentionally commits them.

## Readiness

The plan is ready for a single bounded `task-session` because it has:

- Clear write scope.
- Deterministic container boundary.
- A complete API feature matrix.
- Acceptance criteria for every scenario.
- Cleanup and failure behavior.
- Validation commands that prove both package behavior and repo language policy.
