---
id: context-pack-traefik-secret-blind-deploy
task: SWU-BW-DEPLOY-TRAEFIK-001..004
mode: standard
strictCoverage: pass
createdAt: 2026-06-22T14:02:08Z
---

# Context Pack: TROQAR Traefik Secret-Blind Deploy Harness

## Task

Implement the local deployment harness needed before the first online TROQAR
test:

1. Add a production image build path for the Body War app.
2. Add a Traefik Compose stack with Docker-provided Postgres.
3. Add restricted, secret-blind deploy scripts.
4. Add a manual so the operator can configure the Hostinger VPS, domain,
   Traefik labels, Strava callback, and private `.env`.

## Controlling Evidence

| Source | Selectors | Obligation |
| --- | --- | --- |
| `projects/body-war/development/refinement-runs/20260622T133331Z-agent-safe-traefik-deploy/RESULT.md` | Final synthesis, Traefik Compose shape, secret-blind deploy contract, minimal SWUs | Use Traefik, Docker Postgres, restricted deploy command, image-tag deploy, redacted receipts. |
| `projects/body-war/app/package.json` | `build`, `db:migrate`, `start`, file dependency on `../../auth-user-management` | Docker build must include sibling auth package and app migrations. |
| `projects/body-war/app/src/infrastructure/postgres/migrations.ts` | `AUTH_MIGRATIONS_DIR`, `BODY_WAR_MIGRATIONS_DIR` | Image must contain both auth and body-war Drizzle migration folders at expected paths. |
| `projects/body-war/docs/INFRA-ARCHITECTURE.md` | Single VPS existing host, secrets, validation gates | Update stale Caddy references to Traefik for Hostinger path. |
| `projects/body-war/docs/decisions/vps-deployment-readiness.md` | blocker decisions | Actual online deploy still blocks on operator configuration. |
| `projects/body-war/infra/SECRET-INVENTORY.md` | secret names and tracking rules | Keep real values untracked and agent-invisible. |

## Hard Constraints

- Do not request, read, print, or validate real production secret values.
- Do not deploy to the VPS in this task session.
- Postgres is provided by Docker Compose on the VPS, private internal network,
  persistent Docker volume.
- Traefik is the existing VPS ingress; Caddy is not part of the Hostinger path.
- Agents should deploy by image tag through a restricted command, not by a
  normal Docker-capable shell.
- Production auth must set `BODY_WAR_AUTH_BACKEND=postgres`.

## Write Scope

- `projects/body-war/app/Dockerfile`
- `projects/body-war/app/.dockerignore`
- `projects/body-war/infra/docker-compose.traefik.yml`
- `projects/body-war/infra/.env.traefik.example`
- `projects/body-war/infra/scripts/*.sh`
- `projects/body-war/infra/deployment-receipts/TEMPLATE.md`
- `projects/body-war/docs/ONLINE-DEPLOY-MANUAL.md`
- scoped updates to `INFRA-ARCHITECTURE.md`, `SECRET-INVENTORY.md`,
  `vps-deployment-readiness.md`
- task-session result artifacts

## Done Criteria

- Compose config validates with placeholder env.
- Shell scripts pass `bash -n`.
- App build/check still passes locally.
- Dockerfile is present and documents repo-root build context.
- Manual gives the operator concrete configuration steps without leaking
  secrets.

## Known Blocker After This Session

Online testing cannot start until the operator configures the VPS/domain/Strava
values privately and either grants an appropriate restricted deploy command or
runs the manual deploy steps.
