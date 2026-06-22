# Auth User Management

Reusable TypeScript auth/user-management package for DomainSpec projects.

This package is extracted from Poker Team's implemented `auth-access-control`
vertical slice and normalized for reuse:

- domain entities, policies, validation, lifecycle helpers, and events;
- application use cases for login, token issue, authenticate, authorize,
  logout, introspection, permission catalog, and bootstrap;
- injectable ports for token codec, password service, clock, IDs, telemetry,
  configuration, and repository sets;
- memory repositories for tests/local smoke checks;
- Drizzle/Postgres schema and repository factories as the SQL default;
- extracted DomainSpec docs under `docs/auth-access-control/`.

Runtime code is TypeScript. Shell is used only for scripts.

## Install

```bash
npm install
```

## Verify

```bash
npm run check
```

## Boundaries

The package does not own HTTP routes, browser cookies, CSRF policy, Strava,
Body War/TROQAR profile pages, or consumer UI. Consumers provide those adapters
around the package's stable domain/application surface.

Roles and permissions are consumer-provided. Extracted Poker Team roles are
kept only as examples in the docs; they are not exported as package defaults.

PostgreSQL persistence uses Drizzle by default:

```ts
import { createDrizzleAuthRepositories } from "@domainspec/auth-user-management";

const repos = createDrizzleAuthRepositories(db);
```
