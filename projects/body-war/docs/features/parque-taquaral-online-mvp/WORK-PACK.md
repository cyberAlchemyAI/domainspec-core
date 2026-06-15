---
node_type: work-pack
status: active
topic: Parque Taquaral online MVP design and implementation plan
last_updated: 2026-06-14
created_by: codex
invoke_mode: plan
---

# WORK-PACK: Parque Taquaral Online MVP

## Purpose

Plan the governed path from current decisions and audit evidence to a hosted
TypeScript friend preview. This work-pack is execution-ready for W0 spec
authoring and blocked for app mutation until W0 closes.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | block-for-app-mutation | W0 docs may execute; TypeScript app mutation waits for W0 evidence. |
| complexity | medium | Hosted OAuth, managed storage, geometry, UI, tests, app replacement. |
| outputMode | split | Uses task, wave, and shared files under `work-pack/`. |
| executionPackRef | `EXECUTION-PACK.md` | Required for medium complexity. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | L0-L3 decision boundary. |
| activeLayerWindow | L0 | Spec baseline first. |
| lastUpdatedAt | 2026-06-14T00:00:00Z | Date-only source session. |
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

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [TASK-W0-SPEC-BASELINE](work-pack/tasks/TASK-W0-SPEC-BASELINE.md) | Write P0 specs and contracts. | L0 | medium | [W0](work-pack/waves/W0.md) | `PILOT-DOMAINSPEC-BACKLOG.md` | ready | not-started |
| [TASK-W1-TYPESCRIPT-SCAFFOLD](work-pack/tasks/TASK-W1-TYPESCRIPT-SCAFFOLD.md) | Replace Python app path with TS scaffold and boundary. | L1 | medium | [W1](work-pack/waves/W1.md) | `ARCHITECTURE-AUDIT.md`, W0 specs | blocked-until-W0 | not-started |
| [TASK-W1-FRIEND-FLOW](work-pack/tasks/TASK-W1-FRIEND-FLOW.md) | Implement Strava friend flow, submission, and preview controller. | L1 | medium | [W1](work-pack/waves/W1.md) | W0 API/UI/test specs | blocked-until-W0 | not-started |
| [TASK-W2-HOSTED-PREVIEW](work-pack/tasks/TASK-W2-HOSTED-PREVIEW.md) | Deploy hosted preview with sealed secrets and managed storage. | L2 | medium | [W2](work-pack/waves/W2.md) | `DEPLOYMENT-SECURITY.md`, W1 app | blocked-until-W1 | not-started |
| [TASK-W3-VERIFY-AND-AUDIT](work-pack/tasks/TASK-W3-VERIFY-AND-AUDIT.md) | Run preview validation and close alignment/layering checks. | L2 | medium | [W3](work-pack/waves/W3.md) | `TEST-SPEC.md`, hosted preview | ready-after-implementation | not-started |

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

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action |
| --- | --- | --- | --- | --- |
| B-W0-PROVIDER | W0 | Hosted runtime/storage provider not selected. | TASK-W0-SPEC-BASELINE | Complete SWU-BWPT-004. |
| B-W0-GEOMETRY | W0 | Source-backed Parque Taquaral geometry artifact missing. | TASK-W0-SPEC-BASELINE | Complete SWU-BWPT-003. |
| B-MUTATION-GATE | W1+ | TypeScript app mutation would require guessing W0 contracts. | parent work-pack | Finish W0 specs and reopen gate. |

## Gate Checks

1. W0 docs may start immediately.
2. No deletion/replacement of Python app files before all W0 SWUs pass.
3. Any SWU touching friend data must keep secrets/tokens/raw private activity
   out of repo artifacts.
4. A runtime worker should execute one SWU at a time unless write scopes are
   disjoint and explicitly coordinated.

## Next Route

Route to `task-session` for `SWU-BWPT-001` or another W0 SWU. Do not route to
app implementation until W0 is complete.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-06-14 | Initial invoke design/plan work-pack created. | codex |

