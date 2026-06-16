---
node_type: domainspec-backlog
status: active
topic: Body War / Parque Taquaral hosted friend preview missing spec backlog
last_updated: 2026-06-14
created_by: codex
dispatch_id: body-war-pilot-domainspec-subagent-strategy-20260614
---

# Pilot DomainSpec Backlog - Parque Taquaral Online MVP

## Verdict

Do not start TypeScript app mutation yet. Start with a W0 spec baseline and keep
the Python prototype as reference-only until the work-pack explicitly schedules
replacement.

## P0 Spec Order

| Order | Artifact | Owner Lane | Completion Meaning |
| --- | --- | --- | --- |
| 1 | `SPEC.md` | parent feature spec | Defines module ownership, selected decisions, lanes, non-goals, aspect links, and stale forecast supersession. |
| 2 | `domain.md` | feature/domain | Defines `Runner`, `StravaSession`, `StravaActivity`, `PilotTrack`, `TrackGeometry`, `EvidenceSubmission`, `PreviewControllerState`, token references. |
| 3 | `states.md` | feature/domain | Defines auth, activity, submission, controller, error, geometry, and `preview-accepted` states. |
| 4 | `TRACK-GEOMETRY.md` | geometry | Defines full Parque Taquaral track identity, source, route metadata, geometry format, and validation caveats. |
| 5 | Static geometry artifact | geometry | Stores the chosen sourced geometry in an implementation-readable format. |
| 6 | `DEPLOYMENT-SECURITY.md` | hosted/security | Selects runtime/provider, managed storage, secret store, env inventory, privacy, retention, redaction, access control. |
| 7 | `interfaces.md` | API/interface | Defines hosted routes: status, auth start/callback, activities, tracks, submissions, controller. |
| 8 | `operations.md` | application | Defines connect/callback, import/list activities, submit evidence, auto-accept preview claim, compute controller. |
| 9 | `queries.md` | application | Defines status, activity list, track, submissions, current controller read models. |
| 10 | `mappings.md` | application/infrastructure | Maps Strava payloads to redacted domain/read models and token references. |
| 11 | `ui-spec.md` | UI | Defines route table, component inventory, data flow, form contracts, state-to-UI, a11y. |
| 12 | `TEST-SPEC.md` | validation | Defines hosted preview proof matrix and no-secret checks. |
| 13 | `WORK-PACK.md` | planning | Turns the above into W0/W1 tasks, mutation gates, validation, and deferrals. |

## Immediate Decisions Or Defaults Needed

These are not reopening the earlier product decision gate. They are implementation
contract choices that must be written before code can safely begin.

| ID | Choice | Why It Matters | Recommended Handling |
| --- | --- | --- | --- |
| D-IMPL-001 | Hosted runtime/provider | Strava callback, env vars, logs, and deployment commands depend on it. | Select in `DEPLOYMENT-SECURITY.md` before TS scaffold. |
| D-IMPL-002 | Managed storage provider/schema | Token, submission, controller, and audit storage cannot be abstract forever. | Select in `DEPLOYMENT-SECURITY.md`; no local JSON authority for hosted preview. |
| D-IMPL-003 | Preview access control | Public, unlisted, password-gated, or friend/operator restricted changes privacy risk. | Choose lowest-friction safe preview mode in security spec. |
| D-IMPL-004 | Strava scopes | `activity:read` may be insufficient for private/Only Me activities. | Default `read,activity:read`; permit `activity:read_all` only if the consenting friend needs it. |
| D-IMPL-005 | Geometry source | The app cannot claim full track geometry from placeholder metadata. | Name OSM/GPX/KML/manual trace/source authority before route rendering. |
| D-IMPL-006 | Controller update proof | Tests need a concrete UI/read-model assertion after submission. | Define current holder, fastest time, and latest accepted submission as preview controller fields. |

## P0 Test Bar

| Test ID | Required Preview Proof |
| --- | --- |
| PTV-001 | Hosted HTTPS preview URL loads the app shell. |
| PTV-002 | Strava OAuth starts and returns to the hosted callback. |
| PTV-003 | Friend connected state appears without tokens or secrets. |
| PTV-004 | At least one real friend run appears, or the run absence is recorded as blocker. |
| PTV-005 | Friend submits one activity to the Parque Taquaral pilot track. |
| PTV-006 | Preview controller state changes after auto-accepted submission. |
| PTV-007 | UI/API/log/evidence artifacts contain no tokens, secrets, raw private payloads, or unredacted friend data. |

## Explicit Deferrals

- Pilot-ready GPS proof.
- Full anti-cheat or sensor fusion.
- Operator verification console beyond preview acceptance.
- Native mobile app.
- City-wide territory/hex model.
- Economy, RunCoins, sponsors, clans, seasons, and monetization.
- Engineering-ready suite beyond the preview smoke checks, unless a later gate
  raises the validation bar.

## Work-Pack Entry Gate

`WORK-PACK.md` may be created next, but it should mark `plannerGateStatus` as
`block` for mutation until the P0 spec baseline exists or is assigned to W0 with
clear completion evidence.

Recommended W0:

1. Write `SPEC.md`, `domain.md`, and `states.md`.
2. Select hosted runtime and managed storage in `DEPLOYMENT-SECURITY.md`.
3. Write `TRACK-GEOMETRY.md` and add or link the static geometry artifact.
4. Write `interfaces.md`, `operations.md`, `queries.md`, and `mappings.md`.
5. Write `ui-spec.md` and `TEST-SPEC.md`.
6. Re-evaluate mutation gate for replacing `projects/body-war/app/`.

