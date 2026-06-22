# Context Pack: Poker Auth Standalone Service

## Identity

- Task: refine confirmed route for standalone auth-user-management service
- Run id: `20260621T072243Z-poker-auth-standalone-service`
- Dispatch id: `refine-20260621T072243Z-poker-auth-standalone-service`
- Mode: standard
- Strict coverage: pass

## Obligations

| ID | Obligation | Status | Evidence |
| --- | --- | --- | --- |
| O1 | Copy the implemented Poker Team auth-access-control capability. | covered | `validation/poker-team/backend/src/domain/auth-access-control/` |
| O2 | Include application use cases, not only domain types. | covered | `validation/poker-team/backend/src/use-cases/auth-access-control/` |
| O3 | Make the service importable by other services. | covered | target package `projects/auth-user-management` |
| O4 | Keep SQL persistence on Drizzle with PostgreSQL. | covered | `drizzle-auth.repository.ts`, `schema.ts` auth tables |
| O5 | Produce spec and application-ready plan with tests. | covered | `auth-access-control.test.ts`, `seed-system-bootstrap.test.ts`, plan stage |
| O6 | Do not carry Poker Team product defaults into reusable authority. | covered | `role-definitions.ts` contains Poker-specific permissions to replace |
| O7 | Extract the Poker Team auth-access-control docs, not only code and tests. | covered | `validation/poker-team/docs/features/auth-access-control/` |

## Selected Evidence

### Domain Boundary

`validation/poker-team/backend/src/domain/auth-access-control/`

- Entities: principal, session, access token, permission grant.
- Value objects and policies: auth context, permission key parsing,
  permission resolution, introspection reason, login risk.
- Repositories: principal, session, token, grant ports.
- Lifecycle: session and token transition functions.
- Validation: permission key, token expiry, revoked-token state, sid claim.
- Events: login, token issue/revoke, logout, access denied.

Why included: this is the user-identified source implementation and the reusable
domain core.

### Application Use Cases

`validation/poker-team/backend/src/use-cases/auth-access-control/`

- `login.ts`: login and issue-access-token workflows.
- `authenticate-request.ts`: bearer authentication from token to auth context.
- `authorize-request.ts`: deny-overrides permission check.
- `logout.ts`: session termination and token revocation.
- `introspect-token.ts`: active/inactive token introspection.
- `get-permission-catalog.ts`: grant-derived permission catalog.
- `seed-system-bootstrap.ts`: first admin and role grant bootstrap.

Why included: the target must be application-ready, not domain-only.

### Drizzle/Postgres Persistence

`validation/poker-team/backend/src/infrastructure/database/schema.ts`

- Auth tables: `auth_principals`, `auth_sessions`,
  `auth_access_tokens`, `auth_permission_grants`.
- Enum columns for principal subject type, principal status, session status,
  permission effect, and grantee type.

`validation/poker-team/backend/src/infrastructure/repositories/drizzle-auth.repository.ts`

- Drizzle repositories implement all auth ports.
- It currently imports the Poker Team global `db` and schema path; the reusable
  package must inject the database and own auth schema exports.

Why included: this satisfies the Drizzle/PostgreSQL default and gives concrete
adapter code to copy.

### Test Specification

`validation/poker-team/backend/src/infrastructure/http/auth/auth-access-control.test.ts`

- Imports domain, use cases, and repository ports.
- Covers login rules, authenticate rules, authorization, logout, token
  introspection, permission catalog, lifecycle transitions, validation,
  permission resolution, and events.
- Contains HTTP-layer assertions that should not become package authority.

`validation/poker-team/backend/src/use-cases/auth-access-control/seed-system-bootstrap.test.ts`

- Covers first-admin creation, env username/password behavior, role-grant sync,
  idempotence, and no plaintext logging when password is supplied.

Why included: these tests define the expected application behavior and the split
between reusable and route-specific coverage.

### Documentation Authority

`validation/poker-team/docs/features/auth-access-control/`

- Canonical feature specification: `SPEC.md`.
- DomainSpec aspect docs: `domain.md`, `operations.md`, `interfaces.md`,
  `queries.md`, `mappings.md`, `workflows.md`, `states.md`, `events.md`, and
  `observability.md`.
- Capability docs: login, authenticate request, authorize request, logout,
  introspect token, browse permission catalog, and system bootstrap.
- Test and delivery docs: `TEST-SPEC.md`, `STORIES.md`, `tasks.en.md`,
  `decisions.en.md`, `CHANGELOG.md`, and alignment/pipeline reports.
- Consumer-facing UI docs exist, but they describe Poker Team web routes and
  should be copied only as source examples or deferred consumer-interface notes.

Additional linked references:

- `validation/poker-team/docs/index/feature-map.md` lists the auth docs in the
  project feature map.
- `validation/poker-team/docs/slos.md` contains auth SLO expectations.
- `validation/poker-team/infra/alerts/auth-access-control.rules.yml` contains
  alert rules that can inform operational docs.

Why included: the user corrected the route to extract the docs too; the
standalone service should preserve the existing DomainSpec documentation
surface, with links and Poker-specific language normalized for reuse.

## Transfer Risks

- `login.ts`, `authenticate-request.ts`, `authorize-request.ts`, `logout.ts`,
  `introspect-token.ts`, and `get-permission-catalog.ts` import Poker Team
  telemetry instruments. The standalone package should use an optional telemetry
  port or no-op observer.
- `login.ts` and `introspect-token.ts` use `jsonwebtoken` and `process.env`.
  The reusable service should inject a token codec/config.
- `drizzle-auth.repository.ts` imports Poker Team `db` and schema. The reusable
  package should export its own Drizzle schema and accept an injected Drizzle DB.
- `role-definitions.ts` includes Poker Team roles and permissions. Reusable
  defaults should be generic or consumer-provided.
- `seed-system-bootstrap.ts` logs a generated admin password. The reusable
  service should expose a bootstrap result/report and leave console behavior to
  the consumer.
- Source docs contain Poker Team paths, UI routes, and role examples. The
  extracted docs should rewrite local links and mark Poker-specific material as
  example or deferred consumer material.

## Write Scope

Allowed after task-session handoff:

- `projects/auth-user-management/src/**`
- `projects/auth-user-management/tests/**`
- `projects/auth-user-management/docs/**`
- `projects/auth-user-management/package.json`
- `projects/auth-user-management/package-lock.json`

Read-only:

- `validation/poker-team/**`
- `arcanum/**`

## Validation Surface

- `npm --prefix projects/auth-user-management run check`
- focused auth tests after copy
- docs extraction path/link scan for stale Poker Team source references
- `bash tools/check-runtime-language-policy.sh`
- `git diff --check -- projects/auth-user-management`

## Verdict

pass
