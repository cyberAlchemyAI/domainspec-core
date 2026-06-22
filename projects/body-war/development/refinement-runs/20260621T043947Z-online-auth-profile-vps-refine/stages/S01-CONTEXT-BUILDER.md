# S01 Context Builder - Online Auth/Profile VPS

Status: `pass`
Mode: `standard`
Run id: `20260621T043947Z-online-auth-profile-vps-refine`

## Frame

The operator confirmed that the immediate TROQAR priority is an online app with
login, a minimal profile, Strava connection, a link to the connected Strava
profile page, and use of an available VPS. Track/game surfaces remain deferred.

This frame is implementation-ready but non-mutating: it prepares the work-pack
and validation surface without touching app code, secrets, infrastructure, or
external systems.

## Obligations

| Obligation | Coverage | Evidence |
| --- | --- | --- |
| Preserve the new L0 priority: online auth, profile, Strava connection, Strava profile link, and VPS hosting. | covered | `ONLINE-AUTH-PROFILE-INFRA.md`, `REFINE-SEED-PROPOSAL.md` |
| Extract infra definitions from DomainSpec, poker-team, and the infra-spec research strategy. | covered | `INFRA-DEFINITION-EXTRACTION.md`, DomainSpec infra template, poker-team infra files, infra strategy doc |
| Treat the friend's Taquaral Strava activity as protected validation evidence, not assumed consented data. | covered | `ONLINE-AUTH-PROFILE-INFRA.md`, protected context overlay in `REFINE-DISPATCH.json` |
| Keep runtime mutation out of Refine. | covered | `REFINE-SEED-PROPOSAL.md`, `RUNTIME-HANDOFF.md` |
| Produce a plan that can move into Task Session execution. | covered | this stage sequence and `S09-INVOKE-PLAN.md` |

## Selected Evidence

| Path | Role |
| --- | --- |
| `projects/body-war/docs/features/troqar-product-architecture/ONLINE-AUTH-PROFILE-INFRA.md` | Body War online slice definition and security invariants. |
| `projects/body-war/development/refinement-runs/20260621T043947Z-online-auth-profile-vps-refine/INFRA-DEFINITION-EXTRACTION.md` | Local extraction of infra concepts and open production decisions. |
| `implementation/domainspec/templates/infra-architecture.md` | DomainSpec infra constitution and presets. |
| `implementation/domainspec/copilot/skills/domainspec-infra-deploy/SKILL.md` | Infra deploy artifact and validation discipline. |
| `ops/development/infra-spec-research-strategy.md` | Infra evidence axes, residue, ownership, and proof-status vocabulary. |
| `validation/poker-team/docs/INFRA-ARCHITECTURE.md` | Concrete Single VPS deployment reference. |
| `validation/poker-team/infra/docker-compose.prod.yml` | Reference service topology for app, web, postgres, Caddy, Prometheus, and Grafana. |
| `validation/poker-team/infra/Caddyfile` | Reference TLS reverse-proxy and protected observability routes. |
| `validation/poker-team/infra/index.ts` | Reference Pulumi TypeScript infra code. |
| `validation/poker-team/docs/features/auth-access-control/` | Auth domain concepts, operations, state, and interfaces. |
| `projects/auth-user-management/` | Reusable TypeScript auth/session/Strava package already oriented toward Body War. |
| `projects/body-war/app/` | Current TypeScript pilot app and local routes. |
| `projects/body-war/docs/features/troqar-product-architecture/backend.md` | Backend security and observability requirements. |
| `projects/body-war/docs/features/troqar-product-architecture/ui-spec.md` | Required online pages, including connect and profile surfaces. |

## Context Claims

- The correct infrastructure baseline is a Single VPS style deployment, adapted
  to an already available VPS rather than starting with provider provisioning.
- poker-team is evidence, not authority for product behavior. Its topology and
  auth patterns can be copied structurally, but secrets, names, ports, and poker
  domain concepts must not bleed into Body War.
- `projects/auth-user-management/` is the reusable TypeScript auth foundation.
  It should be treated as the auth/user-management project that future projects
  can adopt.
- Body War production auth needs a server-side durable store before real online
  provider-token custody is acceptable. JSON/local stores remain local-pilot
  only.
- The friend's Strava activity can validate import mechanics only after consent
  and token-safe receipts exist.

## Residue

| Residue | Severity | Owner Path |
| --- | --- | --- |
| Public domain name and production Strava redirect URI are not selected. | flag | decision gate before VPS deploy |
| Production Postgres adapter for auth/profile/provider state must be implemented or confirmed. | flag | first implementation work-pack |
| Friend consent artifact is missing. | flag | validation precondition |
| Deployment receipt does not exist yet. | flag | Task Session deploy validation |
| Monitoring scope should begin with health/logs; Prometheus/Grafana can be L1. | flag | infra plan |

## Handoff

Proceed to Invoke Define with a bounded feature definition: the Online Identity
Loop for Body War/TROQAR L0.
