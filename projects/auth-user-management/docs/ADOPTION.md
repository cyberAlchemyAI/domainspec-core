# Adoption

`@domainspec/auth-user-management` is a reusable TypeScript auth package. A
consumer wires HTTP transport, cookies or bearer headers, token secrets,
password hashing, role definitions, telemetry, and a Drizzle database.

Core package responsibilities:

- principal/session/access-token/permission-grant domain behavior;
- login, issue token, authenticate, authorize, logout, token introspection,
  permission catalog, and bootstrap use cases;
- memory repositories for tests and local smoke checks;
- Drizzle/Postgres schema and repository factories for SQL persistence.

Consumer responsibilities:

- provide role definitions and permission keys;
- choose HTTP framework, cookie/session transport, CSRF policy, and UI flows;
- provide a `TokenCodec`, `PasswordService`, `Clock`, `IdGenerator`, and
  database connection;
- keep Strava or other OAuth providers in a separate consumer module.

Minimal wiring:

```ts
import {
  createDrizzleAuthRepositories,
  createHmacTokenCodec,
  createPbkdf2PasswordService,
  loginUseCase,
  authenticateRequestUseCase,
  authorizeRequestUseCase,
} from "@domainspec/auth-user-management";

const repos = createDrizzleAuthRepositories(db);
const tokenCodec = createHmacTokenCodec(process.env.AUTH_TOKEN_SECRET);
const passwordService = createPbkdf2PasswordService();

const login = loginUseCase({ ...repos, tokenCodec, passwordService });
const authenticate = authenticateRequestUseCase({ ...repos, tokenCodec });
const authorize = authorizeRequestUseCase({ grantRepo: repos.grantRepo });
```

SQL persistence uses Drizzle with PostgreSQL by default. In-memory repositories
are for tests and local smoke checks, not the production persistence default.

## Drizzle Schema And Migrations

The package SQL schema lives in
`src/infrastructure/drizzle-postgres/schema.ts`. Drizzle Kit writes generated
migration SQL to `drizzle/`, and those generated migration artifacts are the
executable schema source for E2E, CI, and consumer deployment setup.

Generate migrations after changing the Drizzle schema:

```sh
npm run db:generate
```

The generated `drizzle/*.sql` and `drizzle/meta/*` artifacts must be committed
with the schema change. Hand-written raw SQL must not duplicate table, enum,
foreign-key, constraint, or index creation already represented by generated
migrations. Raw SQL is reserved for cleanup, fixture data, assertions, or a
documented operational exception.

## E2E API Harness

The package includes a Docker-backed E2E harness for the public TypeScript API.
It starts PostgreSQL, applies generated Drizzle migrations, wires Drizzle
repositories, and executes bootstrap, login, token issue, authenticate,
authorize, logout, introspection, catalog, and export-smoke scenarios.

Prerequisites:

- Docker with Compose support;
- package dependencies installed with `npm install`.

Run the complete E2E flow from the repository root:

```sh
bash projects/auth-user-management/scripts/e2e.sh all
```

Or run the steps manually from `projects/auth-user-management`:

```sh
npm run e2e:db:up
npm run e2e
npm run e2e:db:down
```

Defaults:

- `AUTH_E2E_POSTGRES_PORT=55432`
- `AUTH_E2E_DATABASE_URL=postgres://auth_e2e:<password>@127.0.0.1:55432/auth_user_management_e2e`
- `AUTH_E2E_TOKEN_SECRET=auth-e2e-token-secret`

Override the port or database URL when another local PostgreSQL service is
already using the default port.

This harness validates the reusable package API. HTTP routes, browser cookies,
CSRF, OAuth, Strava linking, and Troqar profile pages remain consumer adapter
responsibilities.
