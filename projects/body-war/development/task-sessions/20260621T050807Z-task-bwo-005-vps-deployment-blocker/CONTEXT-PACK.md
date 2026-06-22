# Context Pack - TASK-BWO-005 VPS Deployment Receipt

Task: `TASK-BWO-005`
SWUs: `SWU-BWO-013`, `SWU-BWO-014`, `SWU-BWO-015`
Mode: `standard`
Strict coverage: `block`
Session evidence: `projects/body-war/development/task-sessions/20260621T050807Z-task-bwo-005-vps-deployment-blocker/`

## Objective

Configure canonical domain, Caddy TLS, Strava production redirect URI, deploy
app/postgres/caddy to the VPS, and produce a deployment receipt with health,
login, Strava connect, profile link, activity import, CSRF, and
secret-redaction results.

## Obligation Coverage

| Obligation | Status | Evidence |
| --- | --- | --- |
| Domain/DNS and canonical app origin are known. | block | no domain supplied in current context |
| VPS access/deploy user is known. | block | VPS exists, but access details were not supplied |
| Strava production redirect URI can be configured. | block | depends on canonical domain and Strava app access |
| Runtime secrets can be provisioned. | block | real secrets are intentionally absent from tracked files |
| Deployment receipt can run health/login/connect/profile/activity checks. | block | requires deployed instance and Strava callback |
| Friend activity validation can run. | block | requires explicit friend consent before use |

## Selected Sources

| Source | Selector | Obligation |
| --- | --- | --- |
| `projects/body-war/development/refinement-runs/20260621T043947Z-online-auth-profile-vps-refine/stages/S09-INVOKE-PLAN.md` | `TASK-BWO-005`, SWUs 013-015 | task contract |
| `projects/body-war/docs/INFRA-ARCHITECTURE.md` | Deployment Flow, Validation Gates, Open Flags | deploy authority |
| `projects/body-war/infra/docker-compose.prod.yml` | app/postgres/caddy runtime shape | deploy input |
| `projects/body-war/infra/.env.example` | required environment variables | secrets boundary |
| `projects/body-war/docs/validation/FRIEND-ACTIVITY-CONSENT-TEMPLATE.md` | consent requirements | validation boundary |

## Blocker Summary

`TASK-BWO-005` cannot proceed to consequential deployment mutation without
operator decisions and private inputs. Proceeding would require guessing a
domain, SSH access model, Strava callback settings, and secret provisioning
boundary.

## Write Scope Before Unblock

- Decision record only.
- Task-session blocked evidence only.

## Handoff

Run Decision Gate for Body War VPS deployment readiness and return `BLOCK`.
