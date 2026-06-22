# Refine Seed Proposal - Online Auth/Profile VPS Slice

Status: `strategy-prepared`
Target: `projects/body-war/docs/features/troqar-product-architecture/ONLINE-AUTH-PROFILE-INFRA.md`
Preset: `standard`
Research mode: `no-research`

## Operator Intent

The operator has a friend with a Parque Taquaral run in Strava and a VPS that
can host the app. The priority is to make TROQAR online with login, a minimal
user profile, Strava connection, and a link to the connected Strava profile
page. The run must extract infra definitions from:

- `implementation/domainspec/`
- `validation/poker-team/`
- `ops/development/infra-spec-research-strategy.md`

## Refined Objective

Prepare a non-executed refine route that turns the online auth/profile/VPS
priority into an implementation-ready plan after confirmation, while preserving
DomainSpec infra discipline, poker-team deployment evidence, and Body War auth
security boundaries.

## Write Scope

Allowed before confirmation:

- `projects/body-war/docs/features/troqar-product-architecture/ONLINE-AUTH-PROFILE-INFRA.md`
- `projects/body-war/development/refinement-runs/20260621T043947Z-online-auth-profile-vps-refine/`

Blocked before confirmation:

- app runtime mutation,
- VPS access or deployment,
- GitHub Actions/secret mutation,
- external research,
- canonical DomainSpec mutation,
- poker-team mutation,
- public/private consent artifact creation for the friend's Strava data.

## Evidence Baseline

| Evidence | Role |
| --- | --- |
| `ONLINE-AUTH-PROFILE-INFRA.md` | Body War local definition of the new online priority. |
| `INFRA-DEFINITION-EXTRACTION.md` | Local extraction of infrastructure concepts and gaps. |
| `implementation/domainspec/templates/infra-architecture.md` | DomainSpec infra constitution template. |
| `implementation/domainspec/copilot/skills/domainspec-infra-deploy/SKILL.md` | Infra deploy synchronization and validation contract. |
| `ops/development/infra-spec-research-strategy.md` | Infra-spec concept axes and research constraints. |
| `validation/poker-team/docs/INFRA-ARCHITECTURE.md` | Concrete single-VPS reference. |
| `validation/poker-team/infra/` | Compose, Caddy, cloud-init, Pulumi evidence. |
| `validation/poker-team/docs/features/auth-access-control/` | Reusable auth access-control domain and interface contracts. |
| `projects/auth-user-management/` | Current TypeScript auth/session/Strava provider package consumed by Body War. |
| `projects/body-war/app/` | Current TypeScript pilot app. |

## Done Criteria For A Confirmed Run

A confirmed Refine run should produce:

1. an online-slice define artifact,
2. an infra design artifact,
3. a non-executed implementation plan/work-pack,
4. a validation matrix for VPS health, login, profile, Strava connect, profile link, activity import, cookie flags, CSRF, and secret scan,
5. refined gap/blocker status for Strava activity evidence, Taquaral geometry, domain/DNS, Postgres auth store, deployment receipt, friend consent, and observability scope.

## Candidate Next Routes After Refine

- `invoke plan` for an online-auth-profile work-pack.
- `task-session` for a bounded L0 implementation if the plan closes the missing decisions.
- `decision-gate` for domain/deployment method/Postgres adapter if still ambiguous.
