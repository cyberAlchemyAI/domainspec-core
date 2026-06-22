# Work Pack - BodyWar Auth Integration

Status: `invoke-plan-pass`
Next owner: `task-session`
Recommended first SWU: `SWU-BWAUTH-001`

## Objective

Repair and implement the BodyWar/TROQAR auth integration against the current
`@domainspec/auth-user-management` package so local TypeScript checks and
PostgreSQL-backed auth/profile E2E pass before any real VPS or Strava
production deployment.

## Current Problem

`projects/body-war/app` imports auth package helpers that are not exported by
the current package. The app does not compile. The integration also still uses a
JSON local auth store shape in docs/config, while the online runtime requires
PostgreSQL with Drizzle Kit generated migrations.

## Write Scope

Primary implementation scope:

- `projects/auth-user-management/src/application/auth-access-control/**`
- `projects/auth-user-management/src/domain/auth-access-control/**`
- `projects/auth-user-management/src/infrastructure/drizzle-postgres/**`
- `projects/auth-user-management/tests/**`
- `projects/auth-user-management/docs/ADOPTION.md`
- `projects/body-war/app/server.ts`
- `projects/body-war/app/src/**`
- `projects/body-war/app/tests/**`
- `projects/body-war/app/package.json`
- `projects/body-war/app/package-lock.json`
- `projects/body-war/app/tsconfig.json`
- `projects/body-war/app/tsconfig.test.json`
- `projects/body-war/app/drizzle.config.ts`
- `projects/body-war/app/drizzle/**`
- `projects/body-war/app/scripts/**`
- `projects/body-war/app/docker-compose.e2e.yml`
- `projects/body-war/app/.env.example`
- `projects/body-war/infra/**`
- `projects/body-war/docs/features/troqar-product-architecture/**`
- `projects/body-war/docs/INFRA-ARCHITECTURE.md`
- `projects/body-war/development/invoke-runs/20260621T131933Z-auth-user-management-integration/**`

Read-only context:

- `projects/auth-user-management/drizzle/**`
- `projects/auth-user-management/README.md`
- `projects/auth-user-management/docs/auth-access-control/**`
- `projects/body-war/development/task-sessions/20260621T04*/**`
- `implementation/domainspec/architecture/pattern-library/SQL-PERSISTENCE.md`

## Constraints

- Runtime code is TypeScript.
- Shell is orchestration only.
- SQL/PostgreSQL uses Drizzle ORM and Drizzle Kit generated migrations.
- Do not add Strava/browser/session/product UI logic to the reusable auth
  package.
- Do not deploy, configure real DNS, configure real Strava callback settings,
  or handle real friend activity evidence in this work-pack.
- Do not commit or print real secrets, tokens, OAuth codes, or raw private
  provider payloads.

## SWU Manifest

| SWU | Parent Task | Goal | Dependencies | Verification |
| --- | --- | --- | --- | --- |
| `SWU-BWAUTH-001` | `TASK-BWAUTH-001` | Add generic trusted-session support to the auth package. | none | `npm --prefix projects/auth-user-management run check` |
| `SWU-BWAUTH-002` | `TASK-BWAUTH-002` | Add BodyWar Drizzle/Postgres schema and migration runner. | SWU-BWAUTH-001 optional | `npm --prefix projects/body-war/app run db:generate` and migration probe |
| `SWU-BWAUTH-003` | `TASK-BWAUTH-003` | Replace broken auth imports with BodyWar-owned browser session adapter. | SWU-BWAUTH-001, SWU-BWAUTH-002 | `npm --prefix projects/body-war/app run check` |
| `SWU-BWAUTH-004` | `TASK-BWAUTH-004` | Implement BodyWar-owned Strava OAuth/provider adapter with stub gateway tests. | SWU-BWAUTH-002, SWU-BWAUTH-003 | BodyWar tests pass with simulated callback |
| `SWU-BWAUTH-005` | `TASK-BWAUTH-005` | Wire profile/activity/logout routes through the new adapters. | SWU-BWAUTH-003, SWU-BWAUTH-004 | Route tests prove profile link, redaction, logout, CSRF |
| `SWU-BWAUTH-006` | `TASK-BWAUTH-006` | Add Docker-backed BodyWar auth E2E and validation scripts. | SWU-BWAUTH-005 | `bash projects/body-war/app/scripts/e2e.sh all` |
| `SWU-BWAUTH-007` | `TASK-BWAUTH-007` | Synchronize docs and deployment-readiness notes without real deploy. | SWU-BWAUTH-006 | doc probes, compose config, secret scan |

## Task Contracts

### TASK-BWAUTH-001 - Auth Package Trusted Session Use Case

Objective:

Create a reusable package use case that lets a consumer create an auth
session/token after an external identity proof, without putting OAuth logic in
the shared package.

Implementation detail:

- Add `createTrustedSessionUseCase` under
  `src/application/auth-access-control/`.
- Reuse session/token creation rules from `loginUseCase` where practical.
- Resolve effective permissions from principal roles, direct permissions, and
  permission grants.
- Export the use case and types from package indexes.
- Add tests for active principal success, missing principal, disabled
  principal, permission resolution, token issuance, and event/telemetry shape.

Smallest Working Unit:

- `SWU-BWAUTH-001`

Acceptance evidence:

- `npm --prefix projects/auth-user-management run check`
- `npm --prefix projects/auth-user-management run validate`
- `git diff --check -- projects/auth-user-management`

### TASK-BWAUTH-002 - BodyWar Postgres Schema And Migration Runner

Objective:

Add BodyWar-owned SQL persistence for provider/profile state and make generated
migrations the executable schema source.

Implementation detail:

- Add `drizzle-orm`, `drizzle-kit`, and `postgres` to BodyWar app if absent.
- Add `projects/body-war/app/drizzle.config.ts`.
- Add BodyWar schema for:
  - `body_war_runner_profiles`
  - `body_war_oauth_states`
  - `body_war_provider_accounts`
  - `body_war_provider_tokens`
- Add scripts:
  - `db:generate`
  - `db:push` or `db:migrate`
- Add a TypeScript migration runner that applies:
  1. `projects/auth-user-management/drizzle/*.sql`
  2. `projects/body-war/app/drizzle/*.sql`
- Keep raw SQL only for operational setup/cleanup, not duplicate schema
  creation.

Smallest Working Unit:

- `SWU-BWAUTH-002`

Acceptance evidence:

- `npm --prefix projects/body-war/app run db:generate`
- `rg -n "body_war_runner_profiles|body_war_oauth_states|body_war_provider_accounts|body_war_provider_tokens" projects/body-war/app/drizzle`
- Duplicate-schema SQL probe over BodyWar E2E helpers returns no matches.

### TASK-BWAUTH-003 - Browser Session Adapter

Objective:

Replace imports of non-existent browser/session package helpers with a
BodyWar-owned adapter around package bearer token authentication.

Implementation detail:

- Implement cookie parsing and cookie headers locally in BodyWar.
- Store package access token in an HttpOnly `bw_session` cookie or store an
  opaque id that resolves server-side to the package token.
- Implement CSRF cookie/header binding for unsafe methods.
- Call `authenticateRequestUseCase` for session authentication.
- Call `authorizeRequestUseCase` or package permission helpers for route
  permission checks.
- Map package `AuthValidationError` codes to BodyWar HTTP errors.

Smallest Working Unit:

- `SWU-BWAUTH-003`

Acceptance evidence:

- `npm --prefix projects/body-war/app run check`
- tests prove missing session, valid session, CSRF rejection, and origin
  rejection.

### TASK-BWAUTH-004 - Strava OAuth Provider Adapter

Objective:

Keep Strava OAuth/provider logic in BodyWar while using the auth package for the
resulting principal/session.

Implementation detail:

- Add `StravaOAuthGateway` port with real HTTP and test fake adapters.
- Implement OAuth state create/consume with expiry.
- Exchange code server-side and store provider tokens encrypted/protected.
- Upsert provider account and runner profile.
- Upsert auth principal with identifier `strava:<athlete-id>` and BodyWar
  runner role.
- Create auth session through `createTrustedSessionUseCase`.

Smallest Working Unit:

- `SWU-BWAUTH-004`

Acceptance evidence:

- tests simulate OAuth callback without real Strava credentials.
- response bodies and logs contain no `access_token`, `refresh_token`, or OAuth
  code values.

### TASK-BWAUTH-005 - Profile, Activities, Logout Route Wiring

Objective:

Route the existing BodyWar API and UI through the new adapters.

Implementation detail:

- `GET /api/status`: configuration, authenticated, connected, safe athlete
  summary.
- `GET /api/profile`: profile projection with safe Strava URL.
- `GET /api/activities`: redacted activity summaries and no-geometry receipt.
- `POST /api/auth/logout`: package logout plus cookie clears.
- `POST /api/submissions`: session plus CSRF plus permission guard.
- Preserve UI copy that route geometry and scoring are not claimed.

Smallest Working Unit:

- `SWU-BWAUTH-005`

Acceptance evidence:

- `npm --prefix projects/body-war/app run check`
- tests cover profile URL, token redaction, logout, activities receipt, and
  submission CSRF.

### TASK-BWAUTH-006 - Docker E2E And Validation Script

Objective:

Create repeatable local proof with PostgreSQL and fake Strava.

Implementation detail:

- Add `docker-compose.e2e.yml` for BodyWar app Postgres.
- Add TypeScript E2E program or node:test integration suite.
- Add `scripts/e2e.sh`.
- Add `scripts/validate.sh` that runs build, tests, E2E where available,
  language policy, secret scans, and migration probes.

Smallest Working Unit:

- `SWU-BWAUTH-006`

Acceptance evidence:

- `bash projects/body-war/app/scripts/e2e.sh all`
- `npm --prefix projects/body-war/app run validate`
- `bash tools/check-runtime-language-policy.sh`

### TASK-BWAUTH-007 - Docs And Deployment Readiness Sync

Objective:

Synchronize documentation with the corrected package/BodyWar ownership boundary
without claiming live deployment.

Implementation detail:

- Patch `interfaces.md`, `ARCHITECTURE.md`, `app/README.md`, and infra docs to
  state:
  - auth package owns core auth domain/use cases/repositories/migrations;
  - BodyWar owns cookies, CSRF, Strava OAuth, provider tokens, profile, and
    activity UI/API.
- Preserve `vps-deployment-readiness.md` blockers.
- Add or update deployment receipt template only with placeholders.

Smallest Working Unit:

- `SWU-BWAUTH-007`

Acceptance evidence:

- `rg -n "BodyWar owns|auth package owns|generated migrations|Strava OAuth" projects/body-war/docs projects/body-war/app/README.md`
- Compose config check with `.env.example`.
- Secret scan over touched docs and infra artifacts.

## Validation Strategy

Required before marking this work-pack complete:

- `npm --prefix projects/auth-user-management run check`
- `npm --prefix projects/auth-user-management run validate`
- `npm --prefix projects/body-war/app run check`
- `npm --prefix projects/body-war/app run validate`
- `bash projects/body-war/app/scripts/e2e.sh all`
- `bash tools/check-runtime-language-policy.sh`
- Drizzle migration generation idempotence for auth and BodyWar app.
- Secret/token scan over touched BodyWar/auth files.
- `git diff --check -- projects/auth-user-management projects/body-war`

## Distill Validation

Verdict: `pass`.

Smallest coherent unit: `SWU-BWAUTH-001` plus the local BodyWar adapter SWUs.
The unit is small enough to execute without VPS or real Strava credentials and
large enough to repair the broken auth import boundary. It recomposes into the
online preview through L1 local E2E, L2 deploy readiness, and L3 operator-gated
online proof.

## Current Blockers

Not blockers for L0-L1 local integration:

- Real public domain.
- VPS access.
- Real Strava credentials.
- Friend activity consent.

Blockers for L3 online proof:

- public origin decision,
- private VPS access path,
- real Strava callback/secret provisioning,
- friend consent receipt if using friend activity evidence.

## Next Route

Run:

```text
[$task-session] projects/body-war/development/invoke-runs/20260621T131933Z-auth-user-management-integration/WORK-PACK.md --swu SWU-BWAUTH-001
```
