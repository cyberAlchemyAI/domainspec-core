# Context Pack - TASK-BWO-001 Infra Definition And Runtime Shape

Task: `TASK-BWO-001`
SWUs: `SWU-BWO-001`, `SWU-BWO-002`, `SWU-BWO-003`
Mode: `standard`
Strict coverage: `pass`
Session evidence: `projects/body-war/development/task-sessions/20260621T045622Z-task-bwo-001-infra-shape/`

## Objective

Create Body War specific infrastructure authority and first deployable runtime
shape from the refined TROQAR online auth/profile/VPS plan.

## Obligations

| Obligation | Status | Evidence |
| --- | --- | --- |
| Author `projects/body-war/docs/INFRA-ARCHITECTURE.md` from the Single VPS existing-host preset. | covered | `S09-INVOKE-PLAN.md`, `ONLINE-AUTH-PROFILE-INFRA.md`, DomainSpec infra template |
| Add Body War `infra/docker-compose.prod.yml` and `infra/Caddyfile` for app, postgres, and caddy. | covered | poker-team compose/Caddy reference, Body War app server route/port |
| Add env example and secret inventory without committing real secrets. | covered | auth-user-management adoption guide, Body War app `.env.example`, refined security invariants |
| Preserve TypeScript/shell runtime policy. | covered | `tools/check-runtime-language-policy.sh`, Body War `package.json` |
| Do not touch app code, VPS, external services, or friend Strava evidence in this task. | covered | Refine runtime handoff and task scope |

## Selected Sources

| Source | Selector | Obligation |
| --- | --- | --- |
| `projects/body-war/development/refinement-runs/20260621T043947Z-online-auth-profile-vps-refine/stages/S09-INVOKE-PLAN.md` | `TASK-BWO-001`, SWUs 001-003, validation matrix | task contract |
| `projects/body-war/docs/features/troqar-product-architecture/ONLINE-AUTH-PROFILE-INFRA.md` | infrastructure definitions, security invariants, validation surface | infra authority |
| `projects/body-war/development/refinement-runs/20260621T043947Z-online-auth-profile-vps-refine/INFRA-DEFINITION-EXTRACTION.md` | L0 infra candidate, production-readiness gaps | gap/residue |
| `implementation/domainspec/templates/infra-architecture.md` | Single VPS preset, layout, networking, secrets, conventions | template authority |
| `validation/poker-team/docs/INFRA-ARCHITECTURE.md` | concrete single-VPS reference | reference evidence |
| `validation/poker-team/infra/docker-compose.prod.yml` | compose services and health checks | runtime pattern |
| `validation/poker-team/infra/Caddyfile` | Caddy reverse proxy pattern | reverse proxy pattern |
| `projects/body-war/app/server.ts` | app port, host, routes, `/api/status` | Body War runtime truth |
| `projects/body-war/app/package.json` | build/start commands and TypeScript package boundary | app runtime |
| `projects/auth-user-management/docs/ADOPTION.md` | required env vars, storage warning, token custody | auth/security |
| `tools/check-runtime-language-policy.sh` | TypeScript/shell invariant | validation |

## Controlling Constraints

- Use TypeScript app/auth/store code and shell for deployment/check scripts.
- Do not create Python runtime surfaces.
- Do not copy poker-team product names, domains, secrets, or roles.
- Do not expose PostgreSQL on the public network.
- Do not commit real `.env` values, Strava tokens, OAuth codes, client secrets,
  raw private athlete data, or friend activity evidence.
- The current app still uses a JSON auth store; online production readiness
  remains blocked until the Postgres adapter SWU is complete.
- `/api/status` is the current health endpoint.

## Decisions

| Decision | Selection | Classification |
| --- | --- | --- |
| Provisioning path | Existing VPS plus manual compose first; Pulumi/CI later. | assumption |
| Public origin | Single canonical app origin, same-origin `/api/*`. | assumption |
| Monitoring | App/Caddy/Postgres health first; Prometheus/Grafana L1. | assumption |
| App image | Compose references a configurable image tag; image build/publish is later deploy work. | deferrable |
| Postgres usage | Include Postgres service and `DATABASE_URL`; production token custody remains a later implementation gate. | flag |

No blocker-level decision is required before writing the infra artifacts.

## Write Scope

- `projects/body-war/docs/INFRA-ARCHITECTURE.md`
- `projects/body-war/infra/docker-compose.prod.yml`
- `projects/body-war/infra/Caddyfile`
- `projects/body-war/infra/.env.example`
- `projects/body-war/infra/.gitignore`
- `projects/body-war/infra/SECRET-INVENTORY.md`
- `projects/body-war/development/task-sessions/20260621T045622Z-task-bwo-001-infra-shape/`

## Validation Surface

- `docker compose --env-file projects/body-war/infra/.env.example -f projects/body-war/infra/docker-compose.prod.yml config`
- `bash tools/check-runtime-language-policy.sh`
- JSON validation for the context index.
- ASCII scan over changed Body War infra/task-session docs.
- Trailing whitespace scan over changed Body War infra/task-session docs.
- Secret-placeholder scan over Body War infra examples.

## Handoff

Proceed with local execution. Stop before deployment, real secret handling, or
production Strava callback changes.
