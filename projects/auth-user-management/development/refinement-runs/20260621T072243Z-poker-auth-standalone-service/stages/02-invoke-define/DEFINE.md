# Define: Standalone Auth User Management Service

## Mode Result

- Mode: invoke define
- Phase status: pass
- Template selection: DomainSpec-style reusable service spec
- Discovery waiver: user supplied concrete implementation source
- Dispatch techniques: sequence, frame_handoff, owner_boundary_check,
  artifact_contract_bridge, concrete_path_evidence
- Distill validation: not required at define stage; full distill is stage 5
- Next route: invoke design

## Problem

The workspace needs a reusable auth/user-management service that can be imported
by Body War/TROQAR and later projects. The implementation should not be rebuilt
from scratch: Poker Team already contains an implemented auth-access-control
domain, application use cases, Drizzle/Postgres repository, DomainSpec docs,
and test scaffold.

## Definition

`projects/auth-user-management` is a standalone private TypeScript package that
owns reusable authentication and authorization behavior:

- principal identity and credential verification,
- sessions,
- access tokens,
- permission grants and deny-overrides authorization,
- login risk policy,
- request authentication,
- logout and revocation,
- token introspection,
- permission catalog,
- bootstrap seeding hooks,
- Drizzle/PostgreSQL persistence,
- extracted DomainSpec documentation and capability specs.

Consumers import the package and provide adapters/configuration for HTTP
transport, token secrets, password hashing, persistence, clock, ids, telemetry,
and product-specific roles.

## Domain Terms

| Term | Definition |
| --- | --- |
| Principal | An actor subject, such as user, service, or automation, with status, roles, and direct permissions. |
| Session | A server-owned login continuity record with effective permissions and expiry. |
| Access token | A bearer credential bound to a session id and token id, with expiry and revocation evidence. |
| Permission grant | An allow or deny rule attached to a role or principal. |
| Auth context | The request-time identity, session, token, permission, and expiry view used by consumers. |
| Token codec | An injected signer/verifier for bearer tokens. |
| Password service | An injected verifier/hasher for credentials. |
| Auth repository set | Principal, session, token, and grant ports, with memory and Drizzle/Postgres implementations. |

## Functional Requirements

1. Login rejects missing credentials, disabled principals, invalid credentials,
   and risk-policy denial.
2. Login creates an active session with effective permissions and issues an
   access token.
3. Effective permissions include direct permissions and role/principal allow
   grants, with deduplication.
4. Authenticate rejects missing, malformed, expired, revoked, or sessionless
   bearer tokens.
5. Authenticate resolves a valid token into an auth context.
6. Authorize validates canonical permission keys and applies deny override.
7. Logout terminates a session and revokes one token or all session tokens.
8. Introspection reports active or inactive token state with stable inactive
   reason precedence.
9. Permission catalog returns deduplicated permission keys by namespace.
10. Bootstrap can create an admin principal and sync role grants when configured.
11. Drizzle/Postgres repositories implement the repository ports.
12. Source docs are extracted into the package docs and normalized for reusable
    service authority.

## Non-Goals

- No Poker Team player, coach, finance, onboarding, or settlement permissions as
  reusable defaults.
- No HTTP framework binding in the core package.
- No Strava provider logic in this core service slice.
- No raw SQL query-client adapter as the production SQL default.

## Invariants

- TypeScript is the implementation language for runtime code.
- Shell is acceptable for scripts.
- PostgreSQL SQL persistence uses Drizzle by default.
- Extracted docs must not preserve stale Poker Team source paths as reusable
  package links.
- Domain and application layers do not import Drizzle, HTTP frameworks, process
  environment, or concrete telemetry.
- Application use cases receive dependencies through ports/configuration.
- Provider secrets, access tokens, refresh tokens, and generated credentials are
  not written to tracked files.

## Import Surface

The package should export:

- `domain/*`: entities, errors, validation, policies, events.
- `application/*`: login, issue token, authenticate, authorize, logout,
  introspect, permission catalog, bootstrap.
- `ports/*`: token codec, password service, clock, ids, telemetry, repository
  set.
- `infrastructure/memory/*`: in-memory test repositories.
- `infrastructure/drizzle-postgres/*`: Drizzle schema and repository factories.
- `docs/*`: normalized feature spec, DomainSpec aspect docs, capability docs,
  test spec, decisions, stories, and adoption notes.

## Validation Criteria

- Standalone package builds.
- Tests cover the copied behavior before Body War/TROQAR imports it.
- Drizzle schema exports compile without requiring a concrete database at test
  time.
- Docs include the extracted auth-access-control spec/capability docs and mark
  Poker Team roles/routes as examples or deferred consumer adapters.
- Existing Poker Team source remains read-only.

## Verdict

pass
