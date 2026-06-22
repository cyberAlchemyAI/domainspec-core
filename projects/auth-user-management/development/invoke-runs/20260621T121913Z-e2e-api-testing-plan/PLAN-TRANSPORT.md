# Plan Transport

## Distill Validation

Smallest useful unit:

- A package-local E2E harness for the auth user management library.

Why not smaller:

- A Compose file without the TypeScript program proves only infrastructure.
- A TypeScript program without PostgreSQL proves only unit-level behavior already covered by memory repositories.
- An HTTP adapter would be larger than the current need and would introduce transport decisions not required to prove the reusable service.

Recomposition proof:

- Docker Compose supplies PostgreSQL.
- Schema setup creates the persistence contract.
- Drizzle repositories bind the existing service to real SQL.
- The E2E program exercises every exported use case.
- Package scripts and docs make the result reusable by Troqar and future projects.

## Boundary Check

Inside scope:

- Auth package E2E infrastructure.
- Drizzle/PostgreSQL adapter validation.
- TypeScript E2E scenario program.
- Shell wrapper and package scripts.
- Adoption docs.

Outside scope:

- Troqar application pages.
- Strava OAuth.
- Browser cookie session.
- VPS deployment.
- HTTP API transport.

## Risk Register

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Docker daemon unavailable | E2E cannot be executed locally | Preflight with `docker info`; plan and code can be produced, but validation records blocker |
| Drizzle schema has no migrations | Setup could drift from `schema.ts` | Keep E2E setup SQL adjacent to schema and assert table behavior through repositories |
| Port conflict on 55432 | Compose startup fails | Allow `AUTH_E2E_POSTGRES_PORT` override |
| Secret leakage in failure logs | Security regression | Redact database URL password and avoid printing tokens/credential hashes |
| API defect discovered | Work-pack scope widens | Stop, record defect, then decide whether to patch source in a follow-up SWU |

## Validation Plan

```sh
bash projects/auth-user-management/scripts/e2e.sh all
npm --prefix projects/auth-user-management run check
npm --prefix projects/auth-user-management run validate
bash tools/check-runtime-language-policy.sh
git diff --check -- projects/auth-user-management
```

## Invoke Result

This plan is executable and has no current design blocker. The only expected runtime blocker is local Docker availability, which the next task session can detect before implementation.
