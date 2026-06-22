# Work Pack - Drizzle Kit Migration Obligation

## Objective

Make Drizzle Kit generated migrations the executable SQL source for
`@domainspec/auth-user-management`, and ensure the new PostgreSQL persistence
obligation is represented in the DomainSpec architecture pattern library.

## Current Problem

The auth package has a valid Drizzle schema and real PostgreSQL E2E coverage,
but the E2E setup currently duplicates schema creation with hand-written SQL in
`e2e/postgres-schema.ts`. That bypasses Drizzle Kit and can drift from
`src/infrastructure/drizzle-postgres/schema.ts`.

## Write Scope

- `implementation/domainspec/architecture/ARCHITECTURE.md`
- `implementation/domainspec/architecture/pattern-library/README.md`
- `implementation/domainspec/architecture/pattern-library/SQL-PERSISTENCE.md`
- `projects/auth-user-management/drizzle.config.ts`
- `projects/auth-user-management/drizzle/**`
- `projects/auth-user-management/e2e/postgres-schema.ts`
- `projects/auth-user-management/package.json`
- `projects/auth-user-management/package-lock.json`
- `projects/auth-user-management/docs/ADOPTION.md`
- `projects/auth-user-management/development/invoke-runs/20260621T130134Z-drizzle-kit-obligation-plan/**`

Read-only context:

- `projects/auth-user-management/src/infrastructure/drizzle-postgres/schema.ts`
- `projects/auth-user-management/e2e/auth-api.e2e.ts`
- `validation/poker-team/backend/drizzle.config.ts`
- `validation/poker-team/backend/package.json`
- `validation/poker-team/backend/drizzle/**`

## Constraints

- Runtime and E2E program logic remain TypeScript.
- Shell remains orchestration only.
- PostgreSQL persistence uses Drizzle ORM schema plus Drizzle Kit generated migrations.
- Hand-written raw SQL may remain only for cleanup, fixture data, assertions, or documented exceptions.
- Do not introduce HTTP, Troqar, Strava, or deployment changes.

## SWU-AUMDK-001 - Install Drizzle Kit Config And Scripts

Goal:

Add the package-local Drizzle Kit generator surface.

Implementation detail:

- Add `drizzle-kit` as a dev dependency.
- Add `drizzle.config.ts` with:
  - `schema: "./src/infrastructure/drizzle-postgres/schema.ts"`
  - `out: "./drizzle"`
  - `dialect: "postgresql"`
  - `dbCredentials.url` from `AUTH_E2E_DATABASE_URL`, `DATABASE_URL`, or the local E2E default.
- Add scripts:
  - `db:generate`: `drizzle-kit generate`
  - `db:push`: `drizzle-kit push`

Acceptance evidence:

- `npm --prefix projects/auth-user-management run db:generate` creates migration output.
- `git diff --check -- projects/auth-user-management/drizzle.config.ts projects/auth-user-management/package.json projects/auth-user-management/package-lock.json`

## SWU-AUMDK-002 - Generate Initial Auth Migration

Goal:

Commit generated migration artifacts as the executable schema source.

Implementation detail:

- Run the generator from the package.
- Commit the generated `drizzle/*.sql` and `drizzle/meta/*` files.
- Review generated SQL for:
  - `auth_principals`
  - `auth_sessions`
  - `auth_access_tokens`
  - `auth_permission_grants`
  - principal/session/grant enums
  - unique grant index or constraint
  - foreign keys

Acceptance evidence:

- `rg -n "auth_principals|auth_sessions|auth_access_tokens|auth_permission_grants" projects/auth-user-management/drizzle`
- `rg -n "principal_subject_type|principal_status|session_status|permission_effect|grantee_type" projects/auth-user-management/drizzle`

## SWU-AUMDK-003 - Make E2E Consume Generated Migrations

Goal:

Remove duplicate raw schema creation from the E2E helper.

Implementation detail:

- Replace the `CREATE_AUTH_SCHEMA_SQL` table/enum creation array with migration loading from `drizzle/*.sql`.
- Preserve deterministic reset by dropping package-owned objects before applying migrations.
- Split Drizzle Kit `--> statement-breakpoint` migration files into executable statements.
- Keep raw SQL only for object drops and assertions.
- Keep `createAuthDatabase(sql)` using `authAccessControlSchema`.

Acceptance evidence:

- `rg -n "create table auth_|create type principal_|create type session_|create type permission_|create type grantee_" projects/auth-user-management/e2e/postgres-schema.ts` returns no matches.
- `bash projects/auth-user-management/scripts/e2e.sh all` passes.

## SWU-AUMDK-004 - Document And Validate The Obligation

Goal:

Make the generator requirement visible to future maintainers and validators.

Implementation detail:

- Ensure `implementation/domainspec/architecture/pattern-library/SQL-PERSISTENCE.md` is linked from the architecture index and pattern-library README.
- Update `docs/ADOPTION.md` with the migration generation flow and the rule that E2E/deployment consumes generated migrations.
- Record the final task-session result under this invoke run.

Acceptance evidence:

- `rg -n "Drizzle Kit|generated migration|SQL persistence obligation" implementation/domainspec/architecture projects/auth-user-management/docs/ADOPTION.md`
- `npm --prefix projects/auth-user-management run check`
- `npm --prefix projects/auth-user-management run validate`
- `bash tools/check-runtime-language-policy.sh`
- `git diff --check -- implementation/domainspec/architecture projects/auth-user-management`

## Completion Criteria

The work-pack is complete when:

- The architecture pattern library carries the SQL persistence obligation.
- The auth package has Drizzle Kit config and generated migrations.
- The E2E harness applies generated migrations instead of maintaining duplicate schema SQL.
- Existing auth E2E behavior still passes.
- Package checks and repo language policy pass.
