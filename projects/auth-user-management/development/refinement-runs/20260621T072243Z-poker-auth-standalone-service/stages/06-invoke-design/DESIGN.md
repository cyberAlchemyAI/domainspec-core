# Design: Standalone Auth User Management Service

## Mode Result

- Mode: invoke design
- Phase status: pass
- Design views: context, high-level structure, low-level components, workflow,
  decision flow, dependency interface
- Template/profile selection: DomainSpec architecture profile
- Distill validation: pass via stage 5 and stage 8
- Work-pack: n/a in design
- Next route: invoke plan

## 1. Context View

`projects/auth-user-management` becomes the reusable auth package for private
workspace projects. Poker Team remains the source implementation. Body War/TROQAR
is the first planned consumer, but the core package does not depend on Body War,
Poker Team HTTP routes, or Strava. The Poker Team auth-access-control docs are
also source material and should become package-local docs after normalization.

## 2. High-Level Structure

```text
@domainspec/auth-user-management
  src/domain/auth-access-control/
  src/application/auth-access-control/
  src/ports/
  src/infrastructure/memory/
  src/infrastructure/drizzle-postgres/
  docs/auth-access-control/
  tests/
```

Exports:

- domain model and policies,
- application use-case factories,
- port interfaces and default no-op adapters,
- memory repositories for tests/local use,
- Drizzle/Postgres schema and repository factories,
- normalized feature, aspect, capability, test, and decision docs.

## 3. Low-Level Components

### Domain

Copy from Poker Team with portability edits only:

- `principal.entity.ts`
- `session.entity.ts`
- `access-token.entity.ts`
- `permission-grant.entity.ts`
- `auth-context.vo.ts`
- `auth-error-code.enum.ts`
- `auth.errors.ts`
- `auth.events.ts`
- `auth.repository.ts`
- `auth.validation.ts`
- `introspect-reason.policy.ts`
- `login-risk-policy.ts`
- `permission-resolution.ts`
- `session-lifecycle.ts`
- `token-lifecycle.ts`

Role definitions should become a configurable seed input or example fixture, not
package authority.

### Ports

Add:

- `Clock`: `now(): Date`
- `IdGenerator`: `id(): string`
- `TokenCodec`: `sign(payload, options)`, `verify(token, options)`
- `PasswordService`: `hash(secret)`, `verify(secret, hash)`
- `AuthTelemetry`: optional counters/records/events or no-op implementation
- `AuthConfig`: session TTL, token TTL bounds, admin permission key,
  permission namespace defaults

### Application

Copy and normalize:

- `loginUseCase`
- `issueAccessTokenUseCase`
- `authenticateRequestUseCase`
- `authorizeRequestUseCase`
- `logoutUseCase`
- `introspectTokenUseCase`
- `getPermissionCatalogUseCase`
- `seedSystemBootstrap`

Each use case receives a dependency object instead of positional concrete
repositories where practical. Token signing/verifying, password hashing, clock,
ids, and telemetry must come from ports.

### Infrastructure: Drizzle/Postgres

Own and export:

- auth enum definitions,
- `authPrincipals`,
- `authSessions`,
- `authAccessTokens`,
- `authPermissionGrants`,
- repository factories accepting an injected Drizzle database,
- optional `authAccessControlSchema` object for consumer Drizzle setup.

No raw SQL query-client adapter is part of the production SQL default.

### Infrastructure: Memory

Provide memory repositories for tests and local smoke checks. They are not the
production persistence default.

### Documentation

Extract from `validation/poker-team/docs/features/auth-access-control/` into a
package-local docs path such as `projects/auth-user-management/docs/auth-access-control/`.

Preserve and normalize:

- `SPEC.md`,
- aspect docs: domain, operations, interfaces, queries, mappings, workflows,
  states, events, and observability,
- capability docs for login, authenticate, authorize, logout, introspect,
  permission catalog, and bootstrap,
- `TEST-SPEC.md`, `STORIES.md`, `tasks.en.md`, `decisions.en.md`, and
  `CHANGELOG.md`.

Treat Poker Team UI docs, product roles, HTTP route names, and feature-map links
as examples or deferred consumer-interface material rather than package
authority.

## 4. Workflow Process View

### Login

1. Validate input credentials.
2. Resolve principal by identifier.
3. Verify credential through `PasswordService`.
4. Evaluate login risk policy.
5. Load role/principal grants.
6. Resolve effective permissions.
7. Create active session.
8. Issue access token through `TokenCodec`.
9. Persist token record.
10. Emit optional events/telemetry.

### Authenticate

1. Extract bearer token.
2. Verify token through `TokenCodec`.
3. Validate `sid`.
4. Check token record and revocation state.
5. Check session exists, active, and unexpired.
6. Return `AuthContext`.

### Authorize

1. Validate canonical permission key.
2. Convert session permissions into allow grants.
3. Load principal deny grants.
4. Apply deny-overrides decision.
5. Return allowed or throw `AuthValidationError`.

### Logout

1. Resolve active session.
2. Check caller ownership or configured admin logout permission.
3. Revoke target token or all session tokens.
4. Terminate session.
5. Emit events.

## 5. Decision Flow View

| Decision | Rule |
| --- | --- |
| Principal missing or disabled | reject with `PRINCIPAL_DISABLED` |
| Credential invalid | reject with `INVALID_CREDENTIALS` |
| Login risk blocked | reject with `FORBIDDEN` |
| Permission key invalid | reject with `FORBIDDEN` |
| Deny grant matches | deny regardless of allow grants |
| Token revoked | inactive/reject before session success |
| Session terminated or expired | inactive/reject |
| SQL persistence selected | use Drizzle/Postgres |

## 6. Dependency Interface View

Allowed dependencies:

- domain imports nothing concrete,
- application imports domain and ports,
- infrastructure imports domain, ports, Drizzle, and concrete libraries,
- package entrypoint re-exports stable public APIs.
- docs use package-local paths and distinguish reusable authority from source
  examples.

Forbidden dependencies:

- application importing Poker Team telemetry,
- application reading `process.env`,
- domain/application importing Drizzle,
- reusable package importing Poker Team HTTP app or database singleton.

## Design Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D1 | Copy full vertical slice, not domain-only. | accepted |
| D2 | Normalize JWT/bcrypt/env/telemetry into ports. | accepted |
| D3 | Drizzle/Postgres is the SQL default. | accepted |
| D4 | Keep role definitions consumer-provided. | accepted |
| D5 | Keep browser cookies and Strava outside this core slice. | accepted |
| D6 | Extract Poker Team auth docs and normalize them into package-local docs. | accepted |

## Open Gaps

- Decide whether to keep `jsonwebtoken` and `bcrypt` as optional infra helpers
  in the package or leave them entirely to consumers.
- Decide package test runner: current package uses `node:test`; source tests use
  Vitest. The execution task can either port tests to `node:test` or add Vitest.
- Decide whether Poker Team UI docs should be copied into an examples/deferred
  folder or summarized as consumer-interface guidance.

## Verdict

pass
