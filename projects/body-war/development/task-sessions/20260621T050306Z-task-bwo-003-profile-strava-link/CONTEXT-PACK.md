# Context Pack - TASK-BWO-003 Online Profile And Strava Link

Task: `TASK-BWO-003`
SWUs: `SWU-BWO-007`, `SWU-BWO-008`, `SWU-BWO-009`
Mode: `standard`
Strict coverage: `pass`
Session evidence: `projects/body-war/development/task-sessions/20260621T050306Z-task-bwo-003-profile-strava-link/`

## Objective

Make the user-visible online identity loop real in the Body War TypeScript app:
add `/api/profile`, show `/profile` UI state with Strava connection and safe
profile link, and pass deployed-mode cookie/origin security config into the
browser session guard.

## Obligations

| Obligation | Status | Evidence |
| --- | --- | --- |
| Add `/api/profile` and minimal `RunnerProfile` read model. | covered | `S09-INVOKE-PLAN.md`, app server route structure |
| Add `/profile` UI with identity, Strava connection state, privacy state, and safe Strava profile link. | covered | `ONLINE-AUTH-PROFILE-INFRA.md`, static UI files |
| Enforce production cookie, origin, and CSRF behavior through config. | covered | `browser-session.ts`, app env handling |
| Do not expose provider tokens, OAuth codes, or private payloads. | covered | Strava/auth use cases and adoption guide |
| Keep track/game mechanics deferred. | covered | online slice capability boundary |

## Selected Sources

| Source | Selector | Obligation |
| --- | --- | --- |
| `projects/body-war/development/refinement-runs/20260621T043947Z-online-auth-profile-vps-refine/stages/S09-INVOKE-PLAN.md` | `TASK-BWO-003`, SWUs 007-009 | task contract |
| `projects/body-war/docs/features/troqar-product-architecture/ONLINE-AUTH-PROFILE-INFRA.md` | Page Boundary, Security Invariants, Validation Surface | product/security |
| `projects/body-war/app/server.ts` | authComponents, status, Strava callback, activities, routing | server shape |
| `projects/body-war/app/static/index.html` | current panels and controls | UI shell |
| `projects/body-war/app/static/app.js` | status/activity boot flow | UI behavior |
| `projects/body-war/app/static/styles.css` | existing design system | UI consistency |
| `projects/auth-user-management/src/modules/auth/interface/browser-session.ts` | `secureCookies`, allowed origins, CSRF enforcement | security config |
| `projects/body-war/app/tests/auth-consumer.test.ts` | app test style | validation |

## Controlling Constraints

- TypeScript server code only.
- Static browser UI may remain vanilla JS/CSS.
- Do not add real Strava calls beyond existing provider flow.
- Do not expose tokens in profile/status payloads.
- Do not claim route geometry from imported activities.
- Keep design consistent with the existing operational dashboard, not a landing
  page.

## Decisions

| Decision | Selection | Classification |
| --- | --- | --- |
| Profile routing | Use SPA fallback for `/profile`, plus `/api/profile` for data. | assumption |
| Strava profile link | Build only from numeric `providerUserId`. | security assumption |
| Deployed cookie config | `BODY_WAR_SECURE_COOKIES` or HTTPS/production default enables Secure cookies. | assumption |
| Allowed origins | `BODY_WAR_ALLOWED_ORIGINS` overrides default; local origin stays dev-only. | assumption |

No blocker-level decision is required before implementation.

## Write Scope

- `projects/body-war/app/server.ts`
- `projects/body-war/app/static/index.html`
- `projects/body-war/app/static/app.js`
- `projects/body-war/app/static/styles.css`
- `projects/body-war/app/.env.example`
- `projects/body-war/infra/.env.example`
- `projects/body-war/infra/SECRET-INVENTORY.md`
- `projects/body-war/app/tests/auth-consumer.test.ts`
- `projects/body-war/development/task-sessions/20260621T050306Z-task-bwo-003-profile-strava-link/`

## Validation Surface

- `npm --prefix projects/body-war/app run check`
- `bash tools/check-runtime-language-policy.sh`
- `python3 -m json.tool context-index.json`
- ASCII scan over touched files
- trailing whitespace scan over touched files
- targeted token/secret scan over profile payload code and examples

## Handoff

Proceed locally. Stop before friend activity evidence or VPS deployment.
