---
dispatch_id: body-war-pilot-domainspec-subagent-strategy-20260614
role_id: pilot-feature-spec-cartographer
agent_id: 019ec50d-7df0-7532-85cd-f22106441075
spawn_status: spawned
join_status: completed
close_status: closed
validation_result: pass
status: complete
last_updated: 2026-06-14
---

# Receipt: Pilot Feature Spec Cartographer

## Scope

Map the hosted friend preview into feature lanes and identify missing DomainSpec
artifacts before `WORK-PACK.md` and implementation.

## Key Findings

- The target folder has discovery/audit/forecast docs, but no `SPEC.md`,
  `WORK-PACK.md`, `domain.md`, `interfaces.md`, `operations.md`, `queries.md`,
  `states.md`, `mappings.md`, or persistence/security spec.
- Success is `hosted-friend-preview-succeeds`: hosted TypeScript app, friend
  Strava login, activity appears, submission works, and preview controller
  updates.
- The feature lanes are TypeScript app boundary, friend Strava auth/activity,
  Parque track/geometry target, evidence submission/controller update, hosted
  persistence/security, and preview validation.
- Existing Strava prototype docs are stale for the hosted preview because they
  assume Python, `.env`, and local ignored token/submission JSON.

## Missing Specs

| Artifact | Why Needed | Priority |
| --- | --- | --- |
| `SPEC.md` | Top-level hosted-preview feature contract, lanes, non-goals, selected decisions, aspect links. | P0 |
| `domain.md` | `Runner`, friend Strava session, `StravaActivity`, `PilotTrack`, geometry status, `EvidenceSubmission`, `ControllerState`. | P0 |
| `states.md` | Preserve `preview-accepted` as separate from `verified`; model auth/activity/submission/error/geometry states. | P0 |
| `interfaces.md` | Hosted API/OAuth contracts for status, auth, activities, tracks, submissions, controller. | P0 |
| `operations.md` | Connect/callback, submit evidence, auto-accept preview submission, compute controller, store redacted evidence. | P0 |
| `queries.md` | Connection status, activity list, track view, submissions, current controller read models. | P0 |
| `mappings.md` | Strava payload to domain/read models, redacted activity summaries, token refs not token values. | P0 |
| `WORK-PACK.md` | W0 spec baseline, mutation gates, validation, deferrals, and implementation task board. | P0 |

## Tensions

- `MVP-ONESHOT-FORECAST.md` is superseded by later decisions in several places:
  it recommends fixture/local/default paths while the decision record selects a
  canonical TypeScript app, real friend Strava data, hosted preview, managed
  storage, and Parque geometry as the pilot target.
- The decision gate has no remaining product-choice blockers, but real Strava
  activity submission and track geometry remain evidence/spec gaps. They should
  be framed as implementation readiness gaps, not reopened product blockers.
- `preview-accepted` must not be named `verified`; otherwise the MVP would
  overclaim pilot-ready validation.

## Backlog Contribution

1. Create `SPEC.md` with the lane inventory and selected decision baseline.
2. Create `domain.md` and `states.md` first because they anchor every other doc.
3. Create `interfaces.md`, `operations.md`, `queries.md`, and `mappings.md` as a
   coherent API/domain contract set.
4. Create `WORK-PACK.md` with W0 spec baseline and no app mutation until P0
   contracts exist.

