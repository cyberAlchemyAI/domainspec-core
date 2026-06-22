# S09 Invoke Plan - Online Auth/Profile VPS Work-Pack

Status: `flag`
Capability: `invoke plan`
Input: `stages/S08-DISTILL-REPAIR.md`

## Plan Summary

Implement Body War/TROQAR L0 as an Online Identity Loop before track/game work:
HTTPS app, secure browser session, Strava connect, minimal profile, Strava
profile link, redacted activity summaries, and deployment receipt on the
available VPS.

The plan is ready for Task Session execution, but production launch remains
flagged until domain/DNS, VPS access, Strava redirect URI, and friend consent
are supplied or confirmed.

## Implementation Layering

| Layer | Scope | Exit Criteria |
| --- | --- | --- |
| L0A Production-shape local | Auth/profile/store/API/UI implemented locally with TypeScript and Postgres-compatible storage. | TypeScript checks pass; session/CSRF/profile/activity tests or smoke scripts pass; secret scan clean. |
| L0B VPS online | Compose/Caddy/Postgres/app deployed to the available VPS with production env. | HTTPS health, login, Strava connect, profile link, activity import, redaction, and deployment receipt pass. |
| L1 Operational hardening | CI deploy, backups, monitoring, alerts, runbooks. | Restore drill, monitoring route protection, and deploy rollback documented. |
| L2 TROQAR validation | Friend consent, Taquaral activity import, route-geometry handoff. | Consent and redacted activity receipt exist; geometry remains explicitly unresolved until track work. |
| L3 Game surfaces | scoring, challenges, rankings, social, economy. | Out of scope for this work-pack. |

## Work-Pack

Work-pack id: `WP-BWO-ONLINE-AUTH-PROFILE-VPS`
Primary target: `projects/body-war/`
Reference target: `projects/auth-user-management/`
Runtime languages: TypeScript for app/auth/store code; shell for scripts and
deployment checks.

### TASK-BWO-001 - Infra Definition And Runtime Shape

Goal: Create Body War specific infra authority from DomainSpec and poker-team
patterns.

SWUs:

- `SWU-BWO-001`: Author `projects/body-war/docs/INFRA-ARCHITECTURE.md` using
  the Single VPS existing-host preset.
- `SWU-BWO-002`: Add `projects/body-war/infra/docker-compose.prod.yml` and
  Caddy config for app, postgres, and caddy.
- `SWU-BWO-003`: Add `.env.example` and secret inventory for production deploy
  without committing secrets.

Validation:

- `docker compose -f projects/body-war/infra/docker-compose.prod.yml config`
- Caddy config names Body War/TROQAR domains, not poker-team domains.
- No secret values appear in docs, env examples, or receipts.

### TASK-BWO-002 - Durable Auth/Profile Store

Goal: Replace local-pilot storage for online auth/provider state.

SWUs:

- `SWU-BWO-004`: Implement a Postgres store adapter for
  `projects/auth-user-management` session, OAuth state, user, provider account,
  provider token, and audit/import records.
- `SWU-BWO-005`: Add migration or schema definition for Body War online auth and
  profile state.
- `SWU-BWO-006`: Add store-level tests for token custody, state expiry, session
  revocation, and no-token public reads.

Validation:

- `npm --prefix projects/auth-user-management run check`
- store tests pass,
- profile/public reads contain no provider tokens.

### TASK-BWO-003 - Online Profile And Strava Link

Goal: Make the user-visible online loop real.

SWUs:

- `SWU-BWO-007`: Add `/api/profile` and minimal `RunnerProfile` read model in
  the Body War TypeScript app.
- `SWU-BWO-008`: Add `/profile` UI with identity, Strava connection state,
  privacy state, and safe outbound Strava profile link.
- `SWU-BWO-009`: Enforce production cookie, origin, and CSRF behavior through
  config for deployed mode.

Validation:

- `npm --prefix projects/body-war/app run check`
- local smoke: status, session, logout, profile without tokens,
- CSRF rejection for unsafe requests without matching token/header.

### TASK-BWO-004 - Strava Activity Validation Path

Goal: Allow token-safe activity summary import without claiming route authority.

SWUs:

- `SWU-BWO-010`: Add activity summary import receipt shape with redaction rules.
- `SWU-BWO-011`: Add friend consent receipt template before using the Taquaral
  run as validation evidence.
- `SWU-BWO-012`: Add UI/backend caveat that imported Strava activity does not
  validate Taquaral route geometry or scoring.

Validation:

- imported summaries include only redacted fields,
- consent receipt exists before real friend activity is referenced,
- no route geometry or score claim is emitted.

### TASK-BWO-005 - VPS Deployment Receipt

Goal: Prove online readiness on the available VPS.

SWUs:

- `SWU-BWO-013`: Configure canonical domain, Caddy TLS, and Strava redirect URI.
- `SWU-BWO-014`: Deploy app/postgres/caddy to VPS using shell scripts or CI.
- `SWU-BWO-015`: Produce deployment receipt with health, login, Strava connect,
  profile link, activity import, CSRF, and secret-redaction results.

Validation:

- HTTPS app root works,
- `/api/status` works,
- login/session/logout smoke passes,
- Strava callback smoke passes,
- `/profile` shows safe link and no tokens,
- activity import is redacted,
- logs/artifacts pass a secret scan.

## First Executable Task Session

Recommended first bounded Task Session:

`SWU-BWO-001`: author `projects/body-war/docs/INFRA-ARCHITECTURE.md` from the
existing `ONLINE-AUTH-PROFILE-INFRA.md`, DomainSpec infra template, poker-team
infra reference, and infra-spec strategy.

Reason: it creates the project-local authority needed before compose, Caddy,
and deployment scripts are copied or adapted.

Fastest visible app route after that:

`SWU-BWO-007` and `SWU-BWO-008` for `/api/profile` and `/profile`, but these
should not be called production-ready until `SWU-BWO-004` durable store work is
complete.

## Validation Matrix

| Check | Owner Stage |
| --- | --- |
| `npm --prefix projects/auth-user-management run check` | durable auth store |
| `npm --prefix projects/body-war/app run check` | app/profile UI |
| `bash tools/check-runtime-language-policy.sh` | TypeScript/shell invariant |
| `docker compose -f projects/body-war/infra/docker-compose.prod.yml config` | infra runtime shape |
| secret scan over logs, receipts, docs, and generated env examples | deployment receipt |
| HTTPS health/login/connect/profile/activity smoke | VPS deployment |

## Open Flags

- canonical domain and app origin,
- VPS access/deploy user,
- Strava redirect URI,
- Postgres adapter implementation,
- friend activity consent,
- monitoring depth.

## Handoff

Proceed to final interrogation and synthesis. The refined route should be
marked executable with flags, not blocked.
