# Implementation Layering

## Objective

Create an end-to-end test harness for `@domainspec/auth-user-management` that starts a real PostgreSQL container, wires Drizzle to that database, and runs a TypeScript program against every exported auth capability.

## Layer 0 - Container And Connection Proof

Goal: make PostgreSQL reproducible from the package directory.

Required changes:

- Add `docker-compose.e2e.yml` with one `postgres:16-alpine` service.
- Use a package-scoped project name and non-default host port, for example `${AUTH_E2E_POSTGRES_PORT:-55432}:5432`.
- Include a PostgreSQL health check with `pg_isready`.
- Add `scripts/e2e.sh` as the shell entrypoint for preflight, up, run, and cleanup.

Acceptance:

- `docker compose -f projects/auth-user-management/docker-compose.e2e.yml up -d --wait` reaches healthy.
- `docker compose -f projects/auth-user-management/docker-compose.e2e.yml down -v` removes state.
- Script exits with a clear message if Docker is unavailable.

## Layer 1 - Real Drizzle/PostgreSQL Harness

Goal: prove the repository adapter against actual PostgreSQL behavior.

Required changes:

- Add a PostgreSQL client dependency, preferably `postgres`, and use `drizzle-orm/postgres-js`.
- Add `e2e/postgres-schema.ts` to create and drop the exact auth schema needed by `authAccessControlSchema`.
- Keep schema setup deterministic: drop auth tables and enum types in dependency order, then recreate them before each run.
- Create repositories with `createDrizzleAuthRepositories(db)`.

Acceptance:

- The E2E program can create principals, permission grants, sessions, and tokens through Drizzle repositories.
- JSONB arrays, enum values, UUID primary keys, unique grants, foreign keys, timestamp persistence, token revocation, and session status updates are all exercised against PostgreSQL.

## Layer 2 - Full Public API Scenario Program

Goal: cover every public auth capability through one TypeScript E2E executable.

Required changes:

- Add `e2e/auth-api.e2e.ts` as a TypeScript program with named scenario steps.
- Use production-adjacent ports: `createPbkdf2PasswordService`, `createHmacTokenCodec`, Drizzle repositories, fixed clock, deterministic UUID IDs where required, and an in-memory event collector.
- Run through the scenario matrix in `API-E2E-SCENARIO-MATRIX.md`.
- Fail fast with precise assertion messages and print a compact pass summary only after all scenarios pass.

Acceptance:

- The program exits nonzero on the first failed scenario.
- The program does not log secrets, token bodies, credential hashes, or database URLs containing passwords.
- Every exported use case is invoked at least once.
- Every auth error code has at least one E2E assertion where reachable through the public API.

## Layer 3 - Package Integration And Readiness

Goal: make the E2E harness easy to run locally and safe to wire into CI later.

Required changes:

- Add scripts:
  - `e2e:db:up`
  - `e2e:db:down`
  - `e2e`
  - optionally `e2e:all` for up, run, cleanup.
- Add `tsconfig.e2e.json` so E2E TypeScript compiles independently of source and unit tests.
- Update `docs/ADOPTION.md` with how to run the E2E harness and how consumers can adapt the package.
- Keep `npm run validate` unchanged unless the team intentionally wants Docker-backed E2E in default validation.

Acceptance:

- `npm --prefix projects/auth-user-management run e2e` runs the TypeScript program against an already healthy database.
- `projects/auth-user-management/scripts/e2e.sh` runs up, compile, E2E, and cleanup safely.
- `npm --prefix projects/auth-user-management run check` still passes.
- `bash tools/check-runtime-language-policy.sh` still passes.
