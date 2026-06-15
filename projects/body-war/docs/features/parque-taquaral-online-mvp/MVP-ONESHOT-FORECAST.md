---
node_type: readiness-forecast
status: active
topic: Body War / TROQAR Parque Taquaral online MVP one-shot forecast
last_updated: 2026-06-14
created_by: codex
---

# MVP One-Shot Forecast - Parque Taquaral Online MVP

## Verdict

Status: `flag`

A one-shot implementation is plausible only if the target is a showable online
MVP, not a proven physical pilot. The architecture/import boundary is closed,
but the build still needs explicit decisions around implementation posture,
demo-versus-live Strava evidence, track geometry claims, operator review, local
storage, and validation gates.

Recommended default:

> Build a Body War-owned TypeScript online MVP that preserves the current Python
> app as prototype evidence, supports fixture/demo activity states, supports the
> live Strava path when credentials and a real activity are available, and does
> not claim pilot readiness until one real Strava run imports and submits.

## Source Evidence

| Source | Role |
| --- | --- |
| `projects/body-war/.craft/ledger.yml` | Current blockers, gaps, decisions, and next move. |
| `projects/body-war/CRAFT.md` | Human Craft view. |
| `projects/body-war/docs/features/parque-taquaral-online-mvp/DISCOVERY.md` | Current product and build framing. |
| `projects/body-war/docs/features/parque-taquaral-online-mvp/ARCHITECTURE-AUDIT.md` | Closed TypeScript architecture/import boundary. |
| `projects/body-war/docs/features/strava-linked-pilot/WORK-PACK.md` | Strava prototype test status and active blocker. |
| `projects/body-war/docs/PROJECT-DECISIONS.md` | Selected and open project decisions. |
| `projects/body-war/app/` | Current Python/static prototype evidence. |

## Decisions To Make Before One-Shot Implementation

| ID | Decision | Blocking | Recommended one-shot default | Consequence if not decided |
| --- | --- | --- | --- | --- |
| D-OS-001 | Implementation posture: TypeScript target app, Python prototype hardening, or hybrid migration. | Yes | Create a new Body War-owned TypeScript app/workspace and keep `projects/body-war/app/` as prototype evidence. | Work may continue in the wrong architecture after the TypeScript boundary was selected. |
| D-OS-002 | App location and package shape. | Yes | Use a clear new target such as `projects/body-war/app-ts/` unless the operator explicitly wants to replace `projects/body-war/app/`. | The build may overwrite or confuse the existing prototype. |
| D-OS-003 | Demo states versus real Strava-only display. | Yes | Allow fixture/demo activities for UI and automated validation, but label them clearly. Require real Strava evidence before pilot-ready claims. | A zero-activity Strava account can block all visible progress. |
| D-OS-004 | Track geometry claim level. | Yes for runner-facing claims | Use Parque Taquaral as context only; use textual placeholder track cards until a sourced boundary/lap artifact exists. | The app may imply GPS validation or official route geometry that is not sourced. |
| D-OS-005 | Evidence acceptance and review status model. | Yes | Model `submitted`, `verified`, `rejected`, and `needs_review`; fastest verified time controls public state. | Submissions cannot safely become controller state. |
| D-OS-006 | Persistence and token handling. | Yes if hosted, flag if local | For local one-shot, use a local dev store and keep tokens ignored. For hosted demo, require secure secret and token storage before launch. | Secrets or runner data may leak, or the MVP may be non-repeatable. |
| D-OS-007 | Runner/operator UI boundary. | Flag | Use one compact web UI with runner connection/submission and operator evidence review sections. | The app may prove Strava import but not the actual review/control loop. |
| D-OS-008 | Validation proof level. | Yes | Require typecheck, lint/import-boundary check, API contract tests, fixture UI smoke, and optional live Strava evidence. | A showable app may exist without proof that the loop works. |
| D-OS-009 | Deployment surface. | Yes if external users see it | Local-first by default. Decide hosted domain/callback/HTTPS only if the one-shot includes external runner access. | Strava callback and secret handling can fail late. |
| D-OS-010 | Monetization and economy scope. | No if explicitly deferred | Keep monetization, RunCoins, sponsors, paid progression, clans, seasons, and XP economy out of this MVP. | Economy work can swamp the validation loop. |
| D-OS-011 | Anti-cheat and GPS automation scope. | No if explicitly deferred | Manual plausibility review only; preserve metadata for later anti-cheat. No automated polygon validation. | The build can balloon into a full validation engine. |
| D-OS-012 | MVP success definition. | Yes | Split `showable-online-mvp` from `pilot-ready`: showable passes with fixtures plus architecture checks; pilot-ready requires real Strava import/submission. | The team may overclaim readiness after a demo-only pass. |

## Missing Specs

| Spec | Status | Minimum contents |
| --- | --- | --- |
| `WORK-PACK.md` for Parque Taquaral online MVP | Missing, blocking next route | Target package, tasks, acceptance criteria, tests, explicit deferrals, and closure evidence. |
| TypeScript app/package spec | Missing, blocking implementation | App path, package manager, scripts, `tsconfig` aliases, DomainSpec reference path, and import-boundary checks. |
| Domain model spec | Missing, blocking clean code shape | `Runner`, `Track`, `StravaActivity`, `EvidenceSubmission`, `ControlClaim`, `ReviewStatus`, and `ControllerMetric`. |
| API contract spec | Missing, blocking backend/frontend split | Status, auth start/callback, activities, tracks, submissions, review, and fixture/demo endpoints if allowed. |
| Persistence schema | Missing, blocking repeatability | Local store shape, token record boundary, submission record, review log, and privacy notes. |
| UI state spec | Missing, flag | Disconnected, connected, zero-activity, fixture/demo, submitted, verified, rejected, and error states. |
| Track card / geometry artifact | Missing, flag | Track name, description, safe route note, source status, and explicit "not GPS-validated yet" boundary. |
| Operator review policy | Missing, blocking controller state | Who can verify, what fields are checked, tie handling, rejection reasons, and audit log fields. |
| Validation matrix | Missing, blocking readiness claim | Typecheck, architecture boundary, API tests, fixture smoke, no-secret checks, live Strava optional/required split. |
| Deployment/security note | Missing if hosted | Callback domain, env vars, HTTPS requirement, token storage, data retention, and redaction rules. |

## Recommended One-Shot Build Contract

Build only:

- Body War-owned TypeScript online MVP surface.
- Strava connection/status flow.
- Activities list with fixture fallback and live path.
- Parque Taquaral track-control page with explicit placeholder geometry status.
- Evidence submission and operator review state.
- Current controller computed from fastest verified time.
- Local development persistence suitable for review.
- Tests and checks for API contracts, UI fixture flow, import direction, and secret/data safety.

Do not build:

- Full mobile app.
- City-wide hexes.
- Automated GPS polygon validation.
- Full anti-cheat or sensor fusion.
- Clans, seasons, XP economy, RunCoins, sponsors, premium features, or payments.
- Public pilot launch without real Strava activity submission evidence.

## Suggested Work Order

1. Write `projects/body-war/docs/features/parque-taquaral-online-mvp/WORK-PACK.md`.
2. Decide D-OS-001 through D-OS-008 inside the work-pack before code mutation.
3. Scaffold the TypeScript app/package boundary and `tsconfig` aliases.
4. Add domain/API/persistence contracts before UI polish.
5. Build fixture-backed UI and API first.
6. Add live Strava adapter compatibility after the fixture path passes.
7. Run validation matrix and record whether the result is `showable-online-mvp`, `pilot-ready`, or `blocked`.

## Readiness Split

`showable-online-mvp` requires:

- TypeScript app starts locally.
- Fixture/demo flow shows connect, activity, submit, review, and controller states.
- API contract tests pass.
- Architecture/import-boundary checks pass.
- No committed secrets or token data.

`pilot-ready` additionally requires:

- One real Strava athlete connects.
- At least one real run imports.
- One real run submits as track evidence.
- Operator review can verify or reject the submission.
- Controller state updates from verified evidence without exposing tokens.

## Craft Residue

Still open:

- `BLK-STRAVA-ACTIVITY-001`: real Strava activity import/submission evidence.
- `GAP-TAQUARAL-GEOMETRY-001`: sourced Parque Taquaral track boundary/lap artifact.

New forecast residue:

- `WORK-PACK.md` is still the next required planning artifact.
- The implementation posture decision should be closed before code mutation.
