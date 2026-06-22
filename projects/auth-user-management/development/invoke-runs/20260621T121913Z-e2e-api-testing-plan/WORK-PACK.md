# Work Pack - Auth User Management E2E API Testing

## Objective

Make `@domainspec/auth-user-management` testable end to end with a real PostgreSQL container and a TypeScript E2E program that exercises every exported auth capability through Drizzle-backed persistence.

## Scope

Write scope:

- `projects/auth-user-management/docker-compose.e2e.yml`
- `projects/auth-user-management/scripts/e2e.sh`
- `projects/auth-user-management/e2e/**`
- `projects/auth-user-management/tsconfig.e2e.json`
- `projects/auth-user-management/package.json`
- `projects/auth-user-management/package-lock.json`
- `projects/auth-user-management/docs/ADOPTION.md`

Read-only scope:

- `projects/auth-user-management/src/**`
- `projects/auth-user-management/tests/**`
- `validation/poker-team/**`
- `implementation/domainspec/**`
- `arcanum/**`

Source mutation is allowed only if the E2E task discovers a real exported API defect that prevents package use. In that case, stop and record the defect before widening scope.

## Constraints

- Use shell for orchestration and TypeScript for program logic.
- Use Drizzle with PostgreSQL for SQL persistence.
- Do not introduce an HTTP server in this work-pack.
- Do not commit generated JavaScript E2E source.
- Do not log secrets, bearer tokens, password hashes, or full database URLs.
- Docker state must be cleaned on success and on failure.

## SWU-AUME2E-001 - Docker Compose PostgreSQL

Task:

Add the E2E PostgreSQL container and shell orchestration skeleton.

Implementation notes:

- `docker-compose.e2e.yml` service name: `auth-user-management-postgres`.
- Image: `postgres:16-alpine`.
- Environment:
  - `POSTGRES_DB=auth_user_management_e2e`
  - `POSTGRES_USER=auth_e2e`
  - `POSTGRES_PASSWORD=auth_e2e_password`
- Host port: `${AUTH_E2E_POSTGRES_PORT:-55432}:5432`.
- Health check: `pg_isready -U auth_e2e -d auth_user_management_e2e`.
- `scripts/e2e.sh` should support `up`, `down`, `run`, and `all`.

Acceptance:

- `docker compose -f projects/auth-user-management/docker-compose.e2e.yml up -d --wait` succeeds on a machine with Docker.
- `docker compose -f projects/auth-user-management/docker-compose.e2e.yml down -v` removes volumes.
- `bash projects/auth-user-management/scripts/e2e.sh up` reports a healthy database or fails with actionable Docker guidance.

## SWU-AUME2E-002 - Drizzle PostgreSQL E2E Harness

Task:

Add TypeScript setup helpers that connect Drizzle to the container and prepare the auth schema.

Implementation notes:

- Add `postgres` as a runtime dependency or dev dependency based on package policy.
- Use `drizzle-orm/postgres-js`.
- Add `e2e/postgres-schema.ts` with:
  - `createE2eSqlClient(databaseUrl: string)`
  - `resetAuthSchema(sql)`
  - `createAuthDatabase(sql)`
  - `closeE2eSqlClient(sql)`
- Use raw SQL only for deterministic schema creation and cleanup.
- The runtime API under test must use `createDrizzleAuthRepositories(db)`.

Acceptance:

- Schema setup creates all enum types and tables required by `authAccessControlSchema`.
- A smoke step can insert and read one principal through the Drizzle repository factory.
- Cleanup can be run repeatedly without manual intervention.

## SWU-AUME2E-003 - Full API E2E Program

Task:

Add `e2e/auth-api.e2e.ts`, a TypeScript program that executes the full scenario matrix.

Implementation notes:

- Implement a tiny scenario runner:
  - `scenario(name, fn)`
  - `assertAuthError(code, fn)`
  - `assertNoSecretLeak(logs, secrets)`
- Use deterministic IDs where needed with UUID-shaped values.
- Use `fixedClock` for stable timestamp assertions.
- Collect events in memory and assert ordering.
- Reset database between major scenario groups or isolate identifiers per group.

Acceptance:

- Covers all scenarios in `API-E2E-SCENARIO-MATRIX.md`.
- Invokes every exported auth use case at least once.
- Exits nonzero on failure.
- Prints a compact success summary with scenario count.

## SWU-AUME2E-004 - Package Scripts And Docs

Task:

Make the E2E harness easy to run from the package and document it for future consumers.

Implementation notes:

- Add scripts:
  - `e2e:db:up`
  - `e2e:db:down`
  - `e2e`
  - `e2e:all`
- Add `tsconfig.e2e.json`.
- Update `docs/ADOPTION.md` with:
  - prerequisites
  - command sequence
  - database URL override
  - package API versus HTTP adapter boundary

Acceptance:

- `npm --prefix projects/auth-user-management run e2e:db:up`
- `npm --prefix projects/auth-user-management run e2e`
- `npm --prefix projects/auth-user-management run e2e:db:down`
- `bash projects/auth-user-management/scripts/e2e.sh all`

## SWU-AUME2E-005 - Readiness Validation

Task:

Run the full validation surface and record the result.

Commands:

```sh
docker compose -f projects/auth-user-management/docker-compose.e2e.yml up -d --wait
npm --prefix projects/auth-user-management run e2e
docker compose -f projects/auth-user-management/docker-compose.e2e.yml down -v
npm --prefix projects/auth-user-management run check
npm --prefix projects/auth-user-management run validate
bash tools/check-runtime-language-policy.sh
git diff --check -- projects/auth-user-management
```

Acceptance:

- All commands pass, or any failure is recorded with exact blocker, failing command, and next action.
- Docker cleanup runs even when E2E fails.
- No unrelated files are changed.

## Completion Criteria

The work-pack is complete when:

- A fresh checkout with Docker can run one command to execute all auth E2E scenarios.
- The E2E program proves the public package API through real Drizzle/PostgreSQL persistence.
- Package checks and language policy still pass.
- Docs explain the local run path and the future HTTP adapter boundary.
