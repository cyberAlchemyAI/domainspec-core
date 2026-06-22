# Implementation Layering - BodyWar Auth Integration

Status: `invoke-plan-pass`
Target: BodyWar/TROQAR auth integration with `@domainspec/auth-user-management`

## Layer Summary

| Layer | Decision Question | Minimum Working Unit | Exit Evidence |
| --- | --- | --- | --- |
| L0 | After this layer, do we know BodyWar can compile and run locally against the current reusable auth package boundary? | Package trusted-session use case, BodyWar browser-session adapter, local Strava stub, generated migrations, and local tests. | `npm --prefix projects/body-war/app run check` passes; local E2E uses Postgres and simulated Strava callback. |
| L1 | After this layer, do we know the integration is repeatable and migration-owned? | Docker Postgres E2E, migration runner applying auth plus BodyWar migrations, secret/token redaction tests. | `bash projects/body-war/app/scripts/e2e.sh all` passes; migration idempotence check passes. |
| L2 | After this layer, do we know the online preview can be operated safely before public proof claims? | Production compose wiring, health/status, deployment receipt template, manual secret handling checklist. | Compose config passes; deploy receipt can be completed without secrets in tracked files. |
| L3 | After this layer, do we know the integration can be promoted beyond friend preview? | CI/CD, managed VPS/IaC, observability, real Strava callback receipt, friend consent receipt, activity import receipt. | Deployment receipt with login/connect/profile/activity checks and no secret leakage. |

## L0 - Local Contract Repair

Decision question: after L0, we know whether BodyWar can consume the current
auth package through a stable TypeScript contract.

Included:

- Add generic `createTrustedSessionUseCase` to auth package.
- Refactor BodyWar imports away from non-existent auth package helpers.
- Implement BodyWar-owned browser cookie/CSRF adapter.
- Implement BodyWar-owned Strava OAuth adapter with fake gateway support for
  tests.
- Add BodyWar Drizzle schema/config/migrations for provider/profile state.
- Add migration runner for auth package migrations plus BodyWar migrations.
- Update tests to prove no token leaks and current app check passes.

Deferred:

- Real Strava credentials.
- VPS deployment.
- Friend activity validation.
- Full operator console.

Promotion evidence:

- BodyWar `check` passes.
- Auth package `check` passes.
- Drizzle generation is idempotent.
- No duplicate schema SQL outside generated migrations.

## L1 - Repeatable E2E

Decision question: after L1, we know whether the auth integration is repeatable
against PostgreSQL and fails closed under browser security checks.

Included:

- Docker Compose local Postgres for BodyWar auth integration.
- E2E program for status, Strava start/callback with stub provider, profile,
  activities, logout, CSRF failure, and no-token responses.
- Secret/redaction scan over E2E output.
- Migration application receipt.

Deferred:

- Public DNS and Caddy TLS.
- Real Strava app callback.

Promotion evidence:

- `bash projects/body-war/app/scripts/e2e.sh all` passes.
- `npm --prefix projects/body-war/app run validate` passes.

## L2 - Deployment Readiness Without Secret Mutation

Decision question: after L2, we know whether the app is deployable once the
operator supplies private deployment inputs.

Included:

- Update production compose to use `DATABASE_URL` and migration command.
- Add deployment receipt template and smoke script placeholders.
- Update docs to correct auth/package/BodyWar ownership.

Deferred:

- Real deploy.
- DNS update.
- Real Strava credentials.

Promotion evidence:

- `docker compose --env-file projects/body-war/infra/.env.example -f projects/body-war/infra/docker-compose.prod.yml config --quiet` passes.
- Secret inventory has all required values with placeholders only.

## L3 - Online Proof

Decision question: after L3, we know whether the friend-preview auth loop works
online without leaking private data or overclaiming game readiness.

Included:

- Run deploy after operator choices are supplied.
- Configure Strava callback on chosen origin.
- Produce deployment receipt: health, login, profile, Strava link, activity
  import, no secrets, geometry caveat.
- Record friend consent receipt privately before using friend activity.

Deferred:

- Track geometry validation.
- Scoring, territory ownership, clans, seasons, economy.

Promotion evidence:

- Public origin health/login/connect/profile receipt.
- Redacted activity import receipt.
- No secret scan findings.

## Recommended Next Layer

Start with L0. The current BodyWar app does not compile against the current auth
package, so deployment-layer work would amplify a broken boundary.
