# Implementation Layering - Drizzle Kit Migration Obligation

## Objective

Replace the auth package E2E raw schema recreation with Drizzle Kit generated
migrations, while making the Drizzle Kit generator requirement a reusable
architecture obligation for PostgreSQL persistence.

## L0 - Obligation And Config

Question: can the architecture rule and package config express the new source of
truth without changing runtime behavior?

Scope:

- Add the SQL persistence obligation to DomainSpec architecture patterns.
- Add `drizzle-kit` to `projects/auth-user-management`.
- Add package-local `drizzle.config.ts`.
- Add package scripts for migration generation and application.

Evidence:

- `drizzle.config.ts` points at `src/infrastructure/drizzle-postgres/schema.ts`.
- `npm --prefix projects/auth-user-management run db:generate` can produce migration artifacts.

## L1 - Generated Migration Ownership

Question: can generated migrations become the executable schema source?

Scope:

- Generate and commit the initial auth migration under `projects/auth-user-management/drizzle/`.
- Keep the generated metadata files with the migration.
- Review the generated SQL for auth principals, sessions, access tokens, permission grants, enums, unique constraint, and foreign keys.

Evidence:

- `projects/auth-user-management/drizzle/*.sql` exists.
- Migration SQL includes every table and enum from `authAccessControlSchema`.

## L2 - E2E Migration Runner

Question: does E2E consume generated migrations instead of duplicate raw schema SQL?

Scope:

- Replace hand-written schema creation in `e2e/postgres-schema.ts` with a migration applier.
- Keep raw SQL only for test cleanup, migration bookkeeping if needed, and data assertions.
- Keep the existing 8 E2E scenario groups as the behavioral proof.

Evidence:

- `e2e/postgres-schema.ts` reads/applies generated migration SQL.
- `bash projects/auth-user-management/scripts/e2e.sh all` passes.
- No duplicate `create table auth_*` definitions remain outside generated migrations.

## L3 - Validation And Documentation

Question: does the package make migration drift visible to future tasks?

Scope:

- Update adoption docs to explain Drizzle Kit migration generation.
- Add validation guidance that schema changes require generated migration updates.
- Record the task-session result.

Evidence:

- Docs name `db:generate` and migration ownership.
- `npm --prefix projects/auth-user-management run check` passes.
- `npm --prefix projects/auth-user-management run validate` passes.
- `bash tools/check-runtime-language-policy.sh` passes.
