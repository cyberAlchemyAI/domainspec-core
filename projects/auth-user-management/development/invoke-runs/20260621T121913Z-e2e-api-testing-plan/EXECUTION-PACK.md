# Execution Pack

## Recommended Route

Run `task-session` on the full work-pack, starting at `SWU-AUME2E-001` and continuing through `SWU-AUME2E-005` unless a real blocker appears.

The work is small enough for one implementation session, but each SWU has a clean rollback and validation boundary.

## First Command Set

```sh
docker info >/dev/null
npm --prefix projects/auth-user-management run check
```

If Docker is unavailable, stop before file mutation and record the environment blocker. The plan can still be implemented, but E2E validation would remain blocked.

## Implementation Order

1. Add Compose file and shell script.
2. Add `postgres` dependency and E2E TypeScript compile config.
3. Add schema setup helpers and Drizzle connection.
4. Add full scenario program.
5. Add package scripts and docs.
6. Run E2E and package validation.

## Suggested Package Scripts

```json
{
  "e2e:db:up": "docker compose -f docker-compose.e2e.yml up -d --wait",
  "e2e:db:down": "docker compose -f docker-compose.e2e.yml down -v",
  "build:e2e": "tsc -p tsconfig.e2e.json",
  "e2e": "npm run build:e2e && node dist-e2e/e2e/auth-api.e2e.js",
  "e2e:all": "bash scripts/e2e.sh all"
}
```

Use the package directory as the working directory for these scripts so `docker-compose.e2e.yml` resolves cleanly.

## Environment Defaults

```sh
AUTH_E2E_POSTGRES_PORT=55432
AUTH_E2E_DATABASE_URL=postgres://auth_e2e:auth_e2e_password@127.0.0.1:55432/auth_user_management_e2e
AUTH_E2E_TOKEN_SECRET=auth-e2e-token-secret
```

The E2E program should allow overrides through environment variables while keeping these deterministic local defaults.

## Failure Handling

- If Docker startup fails, print `docker compose ps` and the service logs.
- If schema setup fails, drop and recreate all auth objects before retrying.
- If an auth scenario fails, include the scenario name and assertion message only; avoid dumping token bodies or credentials.
- Always run `docker compose ... down -v` from `scripts/e2e.sh all` after the program exits.

## Handoff To Implementation

Selected next unit: `SWU-AUME2E-001`.

Recommended command:

```sh
/task-session projects/auth-user-management/development/invoke-runs/20260621T121913Z-e2e-api-testing-plan/WORK-PACK.md until next blocker
```
