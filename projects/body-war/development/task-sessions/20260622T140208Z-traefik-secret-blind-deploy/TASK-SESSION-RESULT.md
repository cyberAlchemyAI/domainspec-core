# Task Session Result - Traefik Secret-Blind Deploy Harness

- Task: `SWU-BW-DEPLOY-TRAEFIK-001..004`
- Result: `BLOCK`
- Block reason: local deploy harness is implemented and validated; online test
  now requires operator-private VPS/domain/Strava configuration from
  `projects/body-war/docs/ONLINE-DEPLOY-MANUAL.md`.
- Context pack: `CONTEXT-PACK.md`, 6 controlling sources, strict coverage pass.
- Handoff pack: none.
- Strict coverage: pass.
- Fallback search: named gaps only.
- Runtime: local.
- Adapter: none.
- Gate verdict: local mutation allowed; real VPS deployment and secret handling
  blocked until operator configuration is complete.
- Subagent closeout: n/a.
- Experiment harness: not_applicable.

## Decisions

| Decision | Selected |
| --- | --- |
| Reverse proxy | Existing VPS Traefik, not app-owned Caddy. |
| Database | Docker Compose Postgres with persistent `postgres_data` volume. |
| Agent deploy | Restricted image-tag deploy command; no general Docker-capable shell. |
| Secret handling | `/srv/troqar/.env` is server-owned and never printed/tracked. |
| Image build context | Repo root, because Body War depends on sibling `auth-user-management`. |

## Files Updated

- `projects/body-war/app/Dockerfile`
- `projects/body-war/app/Dockerfile.dockerignore`
- `projects/body-war/app/.dockerignore`
- `projects/body-war/infra/docker-compose.traefik.yml`
- `projects/body-war/infra/.env.traefik.example`
- `projects/body-war/infra/.gitignore`
- `projects/body-war/infra/scripts/build-image.sh`
- `projects/body-war/infra/scripts/deploy-agent.sh`
- `projects/body-war/infra/scripts/smoke-online.sh`
- `projects/body-war/infra/deployment-receipts/TEMPLATE.md`
- `projects/body-war/infra/SECRET-INVENTORY.md`
- `projects/body-war/docs/ONLINE-DEPLOY-MANUAL.md`
- `projects/body-war/docs/INFRA-ARCHITECTURE.md`
- `projects/body-war/docs/decisions/vps-deployment-readiness.md`
- `projects/body-war/.craft/ledger.yml`
- `projects/body-war/CRAFT.md`
- `projects/body-war/development/task-sessions/20260622T140208Z-traefik-secret-blind-deploy/CONTEXT-PACK.md`
- `projects/body-war/development/task-sessions/20260622T140208Z-traefik-secret-blind-deploy/context-index.json`
- `projects/body-war/development/task-sessions/20260622T140208Z-traefik-secret-blind-deploy/TASK-SESSION-RESULT.md`

## Validation

| Command | Result |
| --- | --- |
| `docker compose --env-file projects/body-war/infra/.env.traefik.example -f projects/body-war/infra/docker-compose.traefik.yml config --quiet` | pass |
| `bash -n projects/body-war/infra/scripts/*.sh` | pass |
| `python3 -m json.tool projects/body-war/development/task-sessions/20260622T140208Z-traefik-secret-blind-deploy/context-index.json` | pass |
| `npm --prefix projects/body-war/app run check` | pass |
| `bash tools/check-runtime-language-policy.sh` | pass |
| `projects/body-war/infra/scripts/build-image.sh task-session-smoke-script domainspec-body-war-app` | pass |
| Docker runtime smoke on `127.0.0.1:5180` with fake Strava/memory auth | pass |
| `git diff --check -- <scoped paths>` | pass |

## Manual For Operator

Use: `projects/body-war/docs/ONLINE-DEPLOY-MANUAL.md`.

The manual covers:

1. build and push image,
2. copy Traefik Compose/env example to `/srv/troqar`,
3. configure `/srv/troqar/.env`,
4. set Strava callback URL,
5. run first manual deploy,
6. smoke test the online app,
7. optionally install the restricted deploy command.

## Remaining Blockers

| Blocker | Unblock Action |
| --- | --- |
| Public domain/subdomain | Point DNS `A` record to the Hostinger VPS. |
| Traefik names | Confirm `TRAEFIK_NETWORK`, `TRAEFIK_ENTRYPOINT`, and `TRAEFIK_CERT_RESOLVER`. |
| Server-owned secrets | Create `/srv/troqar/.env` on VPS from `.env.traefik.example`. |
| Strava production callback | Set `https://<domain>/api/auth/strava/callback` in Strava app settings. |
| App image availability | Push the image to a registry the VPS can pull, or make it locally available. |
| First activity validation identity | Choose operator account first, friend account with consent, or skip activity import for the first deploy receipt. |

## Decision Gate Result

- Target scope: first online TROQAR deployment receipt.
- Result: `BLOCK`
- Decisions resolved: 4 local implementation decisions.
- Blockers remaining: 6 operator configuration blockers.
- Decision artifact: `projects/body-war/docs/decisions/vps-deployment-readiness.md`.
- Recommendation: configure a temporary stable subdomain first, run the manual
  deploy once, then install the restricted deploy command for later agent
  image-tag deploys.
- Next step: operator performs `ONLINE-DEPLOY-MANUAL.md`, then task-session can
  run the online receipt.
