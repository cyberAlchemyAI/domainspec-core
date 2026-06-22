# Context Pack - Drizzle Kit Migration Obligation

Session evidence for
`projects/auth-user-management/development/invoke-runs/20260621T130134Z-drizzle-kit-obligation-plan/WORK-PACK.md`.

## Scope

Execute all work-pack SWUs as one bounded Task Session because the SWUs form one
cohesive migration authority change:

- `SWU-AUMDK-001`: add Drizzle Kit config, dependency, and package scripts.
- `SWU-AUMDK-002`: generate and commit the initial auth migration artifacts.
- `SWU-AUMDK-003`: make E2E reset apply generated migrations instead of
  duplicating schema SQL.
- `SWU-AUMDK-004`: document and validate the migration obligation.

## Controlling Constraints

- Runtime and E2E program logic remain TypeScript.
- Shell remains orchestration only.
- PostgreSQL persistence uses Drizzle ORM schema plus Drizzle Kit generated
  migrations.
- Hand-written raw SQL may remain only for cleanup, fixture data, assertions, or
  documented operational exceptions.
- No HTTP, Troqar, Strava, or deployment changes are in scope.
- The repository has unrelated dirty files; this session only mutates the
  work-pack write scope.

## Selected Evidence

- `WORK-PACK.md`: source of objective, constraints, SWU list, acceptance
  evidence, write scope, and completion criteria.
- `src/infrastructure/drizzle-postgres/schema.ts`: TypeScript Drizzle schema
  that must become the source for generated migration SQL.
- `e2e/postgres-schema.ts`: current hand-written duplicate schema creation to
  replace with migration loading.
- `docs/ADOPTION.md`: consumer-facing adoption and E2E documentation to update.
- `implementation/domainspec/architecture/pattern-library/SQL-PERSISTENCE.md`:
  architecture obligation requiring Drizzle ORM plus Drizzle Kit generated
  migrations for PostgreSQL persistence.
- `implementation/domainspec/architecture/ARCHITECTURE.md` and
  `implementation/domainspec/architecture/pattern-library/README.md`: indexes
  that expose the obligation.

## Gate Check

- Baseline package check: `npm --prefix projects/auth-user-management run check`
  passed before mutation.
- Docker availability: `docker info --format '{{.ServerVersion}}'` returned
  `28.0.1`.
- Architecture obligation link check already finds `SQL-PERSISTENCE.md` from the
  architecture index and pattern-library README.
- Blockers: none.

## Implementation Obligations

1. Add `drizzle-kit`, `drizzle.config.ts`, `db:generate`, and `db:push`.
2. Run `npm --prefix projects/auth-user-management run db:generate` and keep
   generated `drizzle/*.sql` plus `drizzle/meta/*`.
3. Remove duplicate raw table/type/index creation from the E2E helper and apply
   generated migration files by splitting Drizzle Kit statement breakpoints.
4. Document that generated migrations are the executable schema source for E2E
   and consumer deployment/adoption flows.
5. Validate with the work-pack commands and record the result in this session
   directory.

## Decisions

- Decision: execute the four SWUs together.
  Rationale: each SWU depends on the same migration authority boundary; stopping
  after config or generation would leave E2E in the drift-prone state the
  work-pack is meant to remove.
- Decision: allow a narrow raw SQL operational pre-step for
  `create extension if not exists pgcrypto`.
  Rationale: the Drizzle schema uses generated UUID defaults, while the
  work-pack only forbids duplicate table, enum, relation, constraint, and index
  schema SQL outside generated migrations.
