# Context Pack - TASK-BWO-004 Strava Activity Validation Path

Task: `TASK-BWO-004`
SWUs: `SWU-BWO-010`, `SWU-BWO-011`, `SWU-BWO-012`
Mode: `standard`
Strict coverage: `pass`
Session evidence: `projects/body-war/development/task-sessions/20260621T050630Z-task-bwo-004-activity-validation/`

## Objective

Add the safe activity-validation layer for TROQAR L0: a redacted activity import
receipt shape, a friend consent receipt template, and UI/backend caveats that
imported Strava activity does not validate Taquaral route geometry or scoring.

## Obligations

| Obligation | Status | Evidence |
| --- | --- | --- |
| Add activity summary import receipt shape with redaction rules. | covered | refined work-pack, Strava summary adapter, app activities route |
| Add friend consent template before using Taquaral run as validation evidence. | covered | online infra security invariants and protected context rule |
| Add UI/backend caveat that imported Strava activity does not validate route geometry or scoring. | covered | online slice L0 boundary and gap review |
| Do not store real friend activity evidence or raw Strava payloads. | covered | protected context rule |

## Selected Sources

| Source | Selector | Obligation |
| --- | --- | --- |
| `projects/body-war/development/refinement-runs/20260621T043947Z-online-auth-profile-vps-refine/stages/S09-INVOKE-PLAN.md` | `TASK-BWO-004`, SWUs 010-012 | task contract |
| `projects/body-war/docs/features/troqar-product-architecture/ONLINE-AUTH-PROFILE-INFRA.md` | Friend activity fixture, security invariants, validation surface | consent/security |
| `projects/body-war/app/server.ts` | `handleActivities`, redacted Strava summaries | backend receipt |
| `projects/body-war/app/static/app.js` | activity rendering | UI caveat |
| `projects/auth-user-management/src/modules/providers/strava/application/strava.use-cases.ts` | redacted summary behavior | provider boundary |
| `projects/body-war/docs/features/troqar-product-architecture/GAP-BLOCKER-REVIEW.md` | geometry and activity blockers | caveat |

## Controlling Constraints

- Do not create a real consent receipt for the friend.
- Do not include Strava activity IDs, athlete IDs, tokens, private URLs, raw
  maps, notes, or payloads in tracked artifacts.
- Keep receipt fields public-safe and redacted.
- Keep route geometry and scoring explicitly deferred.

## Decisions

| Decision | Selection | Classification |
| --- | --- | --- |
| Real friend activity evidence | Do not create. Template only. | blocker avoidance |
| Activity receipt storage | Return a public-safe receipt with activity list response; persistence can come later. | assumption |
| Consent artifact | Track a blank template; filled receipt should be private if sensitive. | assumption |

No blocker-level decision is required for templates/caveats. Real friend
validation remains blocked until consent exists.

## Write Scope

- `projects/body-war/docs/validation/ACTIVITY-IMPORT-RECEIPT.md`
- `projects/body-war/docs/validation/FRIEND-ACTIVITY-CONSENT-TEMPLATE.md`
- `projects/body-war/app/server.ts`
- `projects/body-war/app/static/index.html`
- `projects/body-war/app/static/app.js`
- `projects/body-war/app/tests/auth-consumer.test.ts`
- `projects/body-war/development/task-sessions/20260621T050630Z-task-bwo-004-activity-validation/`

## Validation Surface

- `npm --prefix projects/body-war/app run check`
- `bash tools/check-runtime-language-policy.sh`
- JSON validation for `context-index.json`
- ASCII and whitespace scans
- targeted scan for tracked token/secret/private-payload terms

## Handoff

Proceed with safe scaffolding. Stop before real friend evidence.
