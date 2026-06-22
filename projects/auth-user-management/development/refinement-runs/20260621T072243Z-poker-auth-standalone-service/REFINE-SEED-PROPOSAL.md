# Refine Seed Proposal: Poker Auth Standalone Service

## Target

`projects/auth-user-management`

## Operator Intent

Copy the already-implemented auth-access-control capability from
`validation/poker-team/backend/src/domain/auth-access-control` and make it a
standalone TypeScript service that any other project can import. The service
must have its extracted docs, spec, and application layer ready with tests.

## Source Context

Primary implementation evidence:

- `validation/poker-team/backend/src/domain/auth-access-control/`
- `validation/poker-team/backend/src/use-cases/auth-access-control/`
- `validation/poker-team/backend/src/infrastructure/repositories/drizzle-auth.repository.ts`
- `validation/poker-team/backend/src/infrastructure/database/schema.ts`
- `validation/poker-team/backend/src/infrastructure/http/auth/auth-access-control.test.ts`
- `validation/poker-team/docs/features/auth-access-control/`
- `validation/poker-team/docs/index/feature-map.md`
- `validation/poker-team/docs/slos.md`
- `validation/poker-team/infra/alerts/auth-access-control.rules.yml`

Existing target context:

- `projects/auth-user-management/`
- `projects/body-war/`
- `implementation/domainspec/architecture/`

## Refinement Objective

Produce a confirmed plan for replacing the earlier auth foundation direction
with a Poker Team port:

1. preserve the proven auth-access-control domain semantics,
2. lift application use cases into a reusable package,
3. remove Poker Team infrastructure coupling from the application layer,
4. keep SQL persistence on Drizzle with PostgreSQL,
5. expose a clean import surface for Body War/TROQAR and later projects,
6. extract and normalize the source auth-access-control docs,
7. validate the package with TypeScript tests before any consumer handoff.

## Write Scope After Confirmation

Allowed:

- `projects/auth-user-management/src/**`
- `projects/auth-user-management/tests/**`
- `projects/auth-user-management/docs/**`
- `projects/auth-user-management/package.json`
- `projects/auth-user-management/package-lock.json`
- target-local development evidence under this run folder
- Body War/TROQAR docs or imports only when needed to point to the standalone package

Protected:

- Do not mutate Poker Team source except if a later explicit follow-up asks for upstream sync.
- Do not copy Poker Team product roles, player-management permissions, bootstrap users, secrets, or HTTP route bindings into reusable defaults.
- Do not put private implementation details into the public `arcanum` submodule.

## Done Criteria

- Standalone package exports domain, application use cases, ports, and adapters.
- Domain source is copied from Poker Team with only portability edits.
- Application use cases are copied from Poker Team and normalized to injectable ports for token signing/verifying, password checking, ids, clock, and telemetry.
- Drizzle/PostgreSQL schema and repositories are the default SQL persistence surface.
- Poker Team auth-access-control docs are extracted into package-local docs and
  normalized for reusable service authority.
- Tests cover domain lifecycle, permission resolution, login, authentication, authorization, logout, token introspection, permission catalog, and Drizzle repository mapping with fakes or query-level fixtures.
- `npm --prefix projects/auth-user-management run check` passes.
- `bash tools/check-runtime-language-policy.sh` passes.

## Preset And Research

- Preset: `standard`
- Research: `no-research`
- Rationale: the user identified the authoritative local implementation, and the repo already contains the source, use cases, Drizzle adapter, and tests.

## Planned Stage Configuration

The canonical Refine loop remains available after confirmation. The selected
strategy is local-first, no subagents, and implementation-ready after the
approved Task Session handoff.
