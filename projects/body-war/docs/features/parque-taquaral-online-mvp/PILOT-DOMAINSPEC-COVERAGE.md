---
node_type: domainspec-coverage-synthesis
status: active
topic: Body War / Parque Taquaral hosted friend preview missing spec coverage
last_updated: 2026-06-14
created_by: codex
dispatch_id: body-war-pilot-domainspec-subagent-strategy-20260614
---

# Pilot DomainSpec Coverage - Parque Taquaral Online MVP

## Result

Status: `pass-for-strategy`, `block-for-implementation-mutation`

The subagent fanout completed and confirmed the missing spec surface. The
product decision gate is passed, but implementation should not start until the
P0 DomainSpec contracts below are written or explicitly seeded as W0 tasks in
`WORK-PACK.md`.

## Source Inputs

| Source | Role |
| --- | --- |
| `docs/decisions/parque-taquaral-online-mvp-oneshot.md` | Selected one-shot MVP decisions. |
| `docs/features/parque-taquaral-online-mvp/DISCOVERY.md` | Earlier product/build framing and open gaps. |
| `docs/features/parque-taquaral-online-mvp/ARCHITECTURE-AUDIT.md` | TypeScript app and DomainSpec boundary. |
| `docs/features/parque-taquaral-online-mvp/MVP-ONESHOT-FORECAST.md` | Pre-decision forecast, now partly superseded. |
| `docs/features/strava-linked-pilot/SPEC.md` | Python/local Strava prototype contract, now reference-only. |
| `docs/features/strava-linked-pilot/WORK-PACK.md` | Prior local validation evidence and stale local-token assumptions. |
| `app/data/tracks.json` | Safe static prototype track metadata; contains placeholder `park-track-alpha`. |
| `domainspec/templates/SPEC.md` | Expected feature spec shape. |
| `domainspec/templates/TEST-SPEC.md` | Expected test spec shape. |
| `domainspec/templates/ui-spec.md` | Expected UI spec shape. |
| `domainspec/templates/work-pack.md` | Expected work-pack shape. |

## Selected MVP Baseline

| Decision | Selected Baseline |
| --- | --- |
| Implementation posture | New TypeScript MVP app. |
| App path | Canonical `projects/body-war/app/`, replacing Python prototype during implementation. |
| Runner data | Real consenting friend Strava data in runner-facing preview. |
| Access | Hosted public preview URL. |
| Storage | Hosted managed storage with sealed secrets; provider/schema still missing. |
| Track | Existing Parque Taquaral track as pilot geometry target; full artifact still missing. |
| Evidence acceptance | Auto-accept matching Strava activity for preview controller only. |
| Validation | Preview validation only. |
| Success label | Hosted friend preview succeeds. |

## Feature Lanes

| Lane | MVP Responsibility | Current Coverage | Gap |
| --- | --- | --- | --- |
| TypeScript app boundary | Body War-owned TS app with DomainSpec path/source references. | `ARCHITECTURE-AUDIT.md` selects boundary. | `SPEC.md`, `WORK-PACK.md`, and task directives missing. |
| Friend Strava login/activity | Friend opens hosted page, connects Strava, sees real activities. | Old Python prototype and local test evidence. | Hosted OAuth, scopes, state/session, redaction, and activity mapping specs missing. |
| Parque track geometry | Show full Parque Taquaral pilot track without GPS-validation overclaim. | Placeholder `park-track-alpha`; decision selects real track target. | `TRACK-GEOMETRY.md` and static geometry artifact missing. |
| Evidence submission/controller | Friend submits activity; preview controller updates immediately. | Old prototype stores `submitted` records. | `preview-accepted` state, controller read model, operation/query/interface contract missing. |
| Hosted persistence/security | Store tokens/evidence/controller state in managed storage with sealed secrets. | Decision selects category. | Provider, schema, env inventory, retention, redaction, access-control specs missing. |
| Preview validation | Prove hosted URL, OAuth, activity, submission, controller update, no secret leaks. | Local Python smoke/OAuth evidence only. | Feature-local `TEST-SPEC.md` missing. |

## Artifact Coverage Matrix

| Artifact | Status | Required Before Mutation | Notes |
| --- | --- | --- | --- |
| `SPEC.md` | missing | yes | Feature contract and lane index. |
| `domain.md` | missing | yes | Domain vocabulary and invariants. |
| `states.md` | missing | yes | Must keep `preview-accepted` separate from `verified`. |
| `interfaces.md` | missing | yes | Hosted HTTP/OAuth/API contracts. |
| `operations.md` | missing | yes | Connect, callback, submit, auto-accept, compute controller. |
| `queries.md` | missing | yes | Status, activities, track, submissions, controller read models. |
| `mappings.md` | missing | yes | Strava payload to redacted domain/read models. |
| `ui-spec.md` | missing | yes | Route/component/data-flow/state-to-UI/a11y contract. |
| `TEST-SPEC.md` | missing | yes | Hosted preview proof matrix. |
| `DEPLOYMENT-SECURITY.md` | missing | yes | Provider, env, token, storage, privacy, retention. |
| `TRACK-GEOMETRY.md` | missing | yes for track claim | Source-backed full Parque Taquaral geometry contract. |
| Static track geometry file | missing/not identified | yes for map/route rendering | Existing `tracks.json` is placeholder metadata only. |
| `WORK-PACK.md` | missing | yes | May seed W0 spec baseline, but app mutation waits for P0 contracts. |

## Synthesis Tensions

| Tension | Resolution For Next Plan |
| --- | --- |
| Forecast says fixture/local/defaults; decisions now say real friend data, hosted preview, TS replacement, managed storage. | Treat forecast as pre-decision evidence. `SPEC.md` should explicitly supersede stale defaults. |
| Decision gate says blockers remaining 0, but provider/schema/geometry specs are missing. | Product-choice blockers are closed; implementation-spec blockers remain. |
| Discovery says fastest verified time; decision permits auto-accept preview update. | Introduce `preview-accepted` and avoid calling it `verified`. |
| Parque track is selected, but no source-backed full geometry artifact exists. | Create geometry contract before map/route claims. |
| Hosted storage is selected only by category. | Choose provider/schema/env contract before TypeScript implementation. |

## Parent Synthesis Decisions

| Question | Parent Synthesis |
| --- | --- |
| One feature pack or split sub-lane specs? | One feature pack under `parque-taquaral-online-mvp/` with aspect docs is the cleanest MVP route. |
| May fixtures exist? | Yes for tests/mocks only. Hosted runner-facing preview must show real consenting Strava data. |
| What controller evidence counts? | A read model or UI region must change after submission; appending a `submitted` card alone is insufficient. |
| What is the next blocker? | Hosted provider/storage/schema and source-backed geometry artifact are the highest-risk P0 spec gaps. |

## Handoff

Use `PILOT-DOMAINSPEC-BACKLOG.md` as the ordered input to `WORK-PACK.md`.

