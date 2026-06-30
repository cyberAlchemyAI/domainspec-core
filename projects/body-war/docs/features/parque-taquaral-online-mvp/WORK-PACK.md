---
node_type: work-pack
status: active
topic: Parque Taquaral online MVP design and implementation plan
last_updated: 2026-06-29
created_by: codex
invoke_mode: plan
---

# WORK-PACK: Parque Taquaral Online MVP

## Purpose

Plan the governed path from current decisions and audit evidence to a hosted
TypeScript friend preview. The original W0 gate remains authority for the full
Parque Taquaral preview, while the confirmed SuggestedTrack child route is open
for one bounded Task Session after the preflight recorded below.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | conditional-open-for-suggested-track-one-go | W0 remains for full preview work; `HND-SUGGESTED-TRACK-ONE-GO-BUILD-001` may mutate docs/app within its declared scope. |
| complexity | medium | Hosted OAuth, managed storage, geometry, UI, tests, app replacement. |
| outputMode | split | Uses task, wave, and shared files under `work-pack/`. |
| executionPackRef | `EXECUTION-PACK.md` | Required for medium complexity. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | L0-L3 decision boundary. |
| activeLayerWindow | L0 | Spec baseline first. |
| lastUpdatedAt | 2026-06-29T00:00:00Z | SuggestedTrack one-go preflight recorded. |
| readinessProfile | pilot-preview | Hosted friend preview, not pilot-ready. |

## Objective Summary

- Objective: author W0 contracts, then replace the Python prototype with a
  hosted TypeScript MVP that supports friend Strava login, activity submission,
  and preview controller update.
- Primary inputs: decision record, `DESIGN.md`, `PILOT-DOMAINSPEC-COVERAGE.md`,
  `PILOT-DOMAINSPEC-BACKLOG.md`, `ARCHITECTURE-AUDIT.md`.
- Success condition: hosted friend preview validates with redacted evidence and
  no secret leakage.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-000 | W0 spec baseline closes implementation-contract gaps. | L0 | W0 | Decision record, design, backlog. | Review all P0 specs exist and align. |
| S-001 | TypeScript app scaffold replaces Python path safely. | L1 | W1 | S-000. | TS strict/typecheck and route smoke. |
| S-002 | Friend Strava flow and preview controller work. | L1 | W1 | S-001, provider/storage ready. | OAuth/activity/submission/controller checks. |
| S-003 | Hosted preview deploys with managed storage/secrets. | L2 | W2 | S-002. | Hosted HTTPS/callback/no-secret smoke. |
| S-004 | Preview validation and audits close. | L2 | W3 | S-003. | PTV matrix, alignment/layering review. |
| S-SGT | SuggestedTrack route expansion loop ships without pilot-ready overclaim. | L1 | one-go | Refine decision-build route. | SuggestedTrack docs, schema, API, UI, tests, no-secret checks. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [TASK-W0-SPEC-BASELINE](work-pack/tasks/TASK-W0-SPEC-BASELINE.md) | Write P0 specs and contracts. | L0 | medium | [W0](work-pack/waves/W0.md) | `PILOT-DOMAINSPEC-BACKLOG.md` | ready | not-started |
| [TASK-W1-TYPESCRIPT-SCAFFOLD](work-pack/tasks/TASK-W1-TYPESCRIPT-SCAFFOLD.md) | Replace Python app path with TS scaffold and boundary. | L1 | medium | [W1](work-pack/waves/W1.md) | `ARCHITECTURE-AUDIT.md`, W0 specs | blocked-until-W0 | not-started |
| [TASK-W1-FRIEND-FLOW](work-pack/tasks/TASK-W1-FRIEND-FLOW.md) | Implement Strava friend flow, submission, and preview controller. | L1 | medium | [W1](work-pack/waves/W1.md) | W0 API/UI/test specs | blocked-until-W0 | not-started |
| [TASK-W2-HOSTED-PREVIEW](work-pack/tasks/TASK-W2-HOSTED-PREVIEW.md) | Deploy hosted preview with sealed secrets and managed storage. | L2 | medium | [W2](work-pack/waves/W2.md) | `DEPLOYMENT-SECURITY.md`, W1 app | blocked-until-W1 | not-started |
| [TASK-W3-VERIFY-AND-AUDIT](work-pack/tasks/TASK-W3-VERIFY-AND-AUDIT.md) | Run preview validation and close alignment/layering checks. | L2 | medium | [W3](work-pack/waves/W3.md) | `TEST-SPEC.md`, hosted preview | ready-after-implementation | not-started |
| TASK-SGT-ONE-GO | Build SuggestedTrack list/create/help/evidence loop. | L1 | medium | one-go | `HND-SUGGESTED-TRACK-ONE-GO-BUILD-001` | ready | in-progress |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-BWPT-001 | TASK-W0-SPEC-BASELINE | `PILOT-DOMAINSPEC-BACKLOG.md#p0-spec-order` | none | `SPEC.md` | Feature contract names lanes, decisions, non-goals, aspect docs. | Reviewable `SPEC.md`. | Markdown review. | local-fallback | ready |
| SWU-BWPT-002 | TASK-W0-SPEC-BASELINE | `DESIGN.md#component-responsibilities` | SWU-BWPT-001 | `domain.md`, `states.md` | Domain and states separate `preview-accepted` from `verified`. | Reviewable docs. | Markdown review. | local-fallback | ready |
| SWU-BWPT-003 | TASK-W0-SPEC-BASELINE | `PILOT-DOMAINSPEC-BACKLOG.md#immediate-decisions-or-defaults-needed` | SWU-BWPT-001 | `TRACK-GEOMETRY.md`, static geometry path | Geometry source, metadata, and validation caveats are defined. | Geometry contract and artifact/link. | Review source and caveats. | manual | ready |
| SWU-BWPT-004 | TASK-W0-SPEC-BASELINE | `PILOT-DOMAINSPEC-BACKLOG.md#immediate-decisions-or-defaults-needed` | SWU-BWPT-001 | `DEPLOYMENT-SECURITY.md` | Hosted runtime, storage, env, redaction, retention, access control selected. | Security/deploy contract. | Markdown review. | manual | ready |
| SWU-BWPT-005 | TASK-W0-SPEC-BASELINE | `DESIGN.md#dependency-interface-view` | SWU-BWPT-002, SWU-BWPT-004 | `interfaces.md`, `operations.md`, `queries.md`, `mappings.md` | API/domain contracts written with Strava redaction and controller semantics. | Reviewable aspect docs. | Markdown review. | local-fallback | ready |
| SWU-BWPT-006 | TASK-W0-SPEC-BASELINE | `DESIGN.md#workflow-process-view` | SWU-BWPT-005 | `ui-spec.md`, `TEST-SPEC.md` | UI and test contracts cover hosted friend preview and PTV checks. | Reviewable UI/test specs. | Markdown review. | local-fallback | ready |
| SWU-BWPT-007 | TASK-W1-TYPESCRIPT-SCAFFOLD | W0 specs | all W0 SWUs | `projects/body-war/app/` | TS app scaffold replaces Python prototype path safely. | Diff plus TS checks. | `npm`/typecheck command chosen in W0. | subagent | blocked |
| SWU-BWPT-008 | TASK-W1-FRIEND-FLOW | W0 API/UI/test specs | SWU-BWPT-007 | `projects/body-war/app/` | OAuth/status/activity/submission/controller flow works locally/pre-host. | Local smoke and redacted API samples. | App smoke checks. | subagent | blocked |
| SWU-BWPT-009 | TASK-W2-HOSTED-PREVIEW | `DEPLOYMENT-SECURITY.md` | SWU-BWPT-008 | deploy config, env docs | Hosted preview URL and callback work with sealed secrets. | Hosted smoke receipt. | PTV-001..PTV-003. | manual | blocked |
| SWU-BWPT-010 | TASK-W3-VERIFY-AND-AUDIT | `TEST-SPEC.md` | SWU-BWPT-009 | validation receipts | PTV matrix passes or records blockers. | Redacted validation receipt. | PTV-001..PTV-007. | manual | blocked |
| SWU-SGT-001..006 | TASK-SGT-ONE-GO | Refine run `20260629T050046Z-suggested-track-decision-build-route` | confirmed preflight | docs, schema, migration, seed, API, UI, tests | SuggestedTrack loop works for connected runners while geometry/source-backed status stays deferred. | Task Session result plus validation logs. | `npm --prefix projects/body-war/app run validate`; `npm --prefix projects/body-war/app test`; `npm --prefix projects/body-war/app run e2e`; `npm --prefix projects/body-war/app run test:ui` | local-codex | ready |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action |
| --- | --- | --- | --- | --- |
| B-W0-PROVIDER | W0 | Hosted runtime/storage provider not selected. | TASK-W0-SPEC-BASELINE | Complete SWU-BWPT-004. |
| B-W0-GEOMETRY | W0 | Source-backed Parque Taquaral geometry artifact missing. | TASK-W0-SPEC-BASELINE | Complete SWU-BWPT-003. |
| B-MUTATION-GATE | W1+ | TypeScript app mutation would require guessing W0 contracts for the full preview. This blocker is superseded only for the SuggestedTrack one-go child route named above. | parent work-pack | Keep unrelated preview mutations behind W0; complete this Task Session for SuggestedTrack. |

## Gate Checks

1. W0 docs may start immediately.
2. No deletion/replacement of Python app files before all W0 SWUs pass.
3. Any SWU touching friend data must keep secrets/tokens/raw private activity
   out of repo artifacts.
4. A runtime worker should execute one SWU at a time unless write scopes are
   disjoint and explicitly coordinated.
5. SuggestedTrack app mutation is allowed after this preflight, limited to
   connected-runner visibility, login-required creation, Drizzle persistence,
   idempotent Taquaral seed data, redacted evidence candidates, and tests.

## Next Route

Route to `task-session` for `HND-SUGGESTED-TRACK-ONE-GO-BUILD-001`. Do not
route unrelated full-preview app implementation until W0 is complete.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-06-29 | Opened the bounded SuggestedTrack one-go Task Session route and recorded the child-route mutation exception. | codex |
| 2026-06-14 | Initial invoke design/plan work-pack created. | codex |
