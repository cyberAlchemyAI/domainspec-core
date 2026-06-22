# WORK-PACK: Auth User Management TypeScript Correction

## Purpose

Canonical executable plan for correcting the auth/user-management foundation to TypeScript, preserving shell-first validation, and preparing Body War Strava login without continuing the Python auth path.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | One-shot Task Session approved by operator and executed. |
| complexity | medium | Split work-pack required. |
| outputMode | split | Waves and task contracts included. |
| executionPackRef | `EXECUTION-PACK.md` | Wave choreography. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | L0-L3 boundary decisions. |
| dispatchTechniqueTrace | `REFINE-DISPATCH.json`, `stages/S09-INVOKE-PLAN.md` | Validated. |
| distillValidationStatus | pass | See `stages/S08-DISTILL-REPAIR.md`. |
| activeLayerWindow | L0-L3 | Full auth work-pack executed as one shot. |
| readinessProfile | pilot-to-production | L0/L1 local proof, L2/L3 production hardening. |

## Objective Summary

- Objective: replace the Python auth foundation with a TypeScript package that follows DomainSpec layering and can support login, server sessions, authorization, and Strava linking.
- Primary inputs: DomainSpec architecture, poker-team auth access-control, Savvy browser-session guard, current Python drift.
- Success condition: TypeScript package validates, Python auth runtime is retired, Body War consumes a TypeScript auth boundary, and shell policy checks block new Python auth/runtime drift.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | TypeScript package baseline replaces Python auth foundation | L0 | W0 | none | `projects/auth-user-management/scripts/validate.sh` |
| S-002 | Auth behavior implemented in DomainSpec layers | L1 | W1 | S-001 | TypeScript tests for sessions, tokens, permissions, CSRF, Strava state |
| S-003 | Repo invariant and Body War consumer boundary enforced | L2 | W2 | S-001, S-002 | shell policy check, Body War auth contract/smoke tests |
| S-004 | Production readiness hardening captured | L3 | W3 | S-001 to S-003 | readiness report and secret-gated smoke plan |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [TASK-AUTH-TYPESCRIPT-SPINE](work-pack/tasks/TASK-AUTH-TYPESCRIPT-SPINE.md) | Build TypeScript package and auth behavior | L0/L1 | medium | [W0](work-pack/waves/W0.md), [W1](work-pack/waves/W1.md) | DomainSpec, poker-team, Savvy | pass | completed |
| [TASK-REPO-LANGUAGE-INVARIANT](work-pack/tasks/TASK-REPO-LANGUAGE-INVARIANT.md) | Add shell-enforced runtime language policy | L2 | medium | [W2](work-pack/waves/W2.md) | user invariant, repo drift scan | pass | completed |
| [TASK-BODY-WAR-AUTH-CONSUMER](work-pack/tasks/TASK-BODY-WAR-AUTH-CONSUMER.md) | Replace Body War Python auth dependency | L2 | medium | [W2](work-pack/waves/W2.md) | Body War app and static client | pass | completed |
| [TASK-AUTH-PRODUCTION-READINESS](work-pack/tasks/TASK-AUTH-PRODUCTION-READINESS.md) | Harden production storage, secrets, and smoke proof | L3 | medium | [W3](work-pack/waves/W3.md) | auth package + Body War | pass | completed-with-live-smoke-deferred |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-AUTH-001 | [TASK-AUTH-TYPESCRIPT-SPINE](work-pack/tasks/TASK-AUTH-TYPESCRIPT-SPINE.md) | previous Python package, `implementation/domainspec/architecture/pattern-library/LAYERING-REFERENCE.md` | DomainSpec TS package conventions | none | `projects/auth-user-management/` | TS package skeleton exists; Python auth runtime removed; shell validate exists | TS check passes; no Python auth package selected | `bash projects/auth-user-management/scripts/validate.sh` | local-fallback | completed |
| SWU-AUTH-002 | [TASK-AUTH-TYPESCRIPT-SPINE](work-pack/tasks/TASK-AUTH-TYPESCRIPT-SPINE.md) | poker-team domain auth files | Domain layer rules | SWU-AUTH-001 | `projects/auth-user-management/src/modules/auth/domain/` | principal/session/token/permission rules implemented | domain tests pass | package test command | local-fallback | completed |
| SWU-AUTH-003 | [TASK-AUTH-TYPESCRIPT-SPINE](work-pack/tasks/TASK-AUTH-TYPESCRIPT-SPINE.md) | poker-team authenticate/authorize use-cases | Application layer | SWU-AUTH-002 | `src/modules/auth/application/` | auth/authorization/logout use-cases implemented | app tests pass | package test command | local-fallback | completed |
| SWU-AUTH-004 | [TASK-AUTH-TYPESCRIPT-SPINE](work-pack/tasks/TASK-AUTH-TYPESCRIPT-SPINE.md) | Savvy `savvy-auth.ts` and tests | Browser session and CSRF | SWU-AUTH-003 | `src/modules/auth/interface/`, `src/modules/auth/infrastructure/` | cookie/CSRF guard and local stores implemented | denial matrix passes | package test command | local-fallback | completed |
| SWU-AUTH-005 | [TASK-AUTH-TYPESCRIPT-SPINE](work-pack/tasks/TASK-AUTH-TYPESCRIPT-SPINE.md) | Body War Strava routes, prior Strava provider | Strava provider module | SWU-AUTH-003 | `src/modules/providers/strava/` | OAuth start/callback/refresh/activity summary contracts implemented | mocked Strava tests pass | package test command | local-fallback | completed |
| SWU-INV-001 | [TASK-REPO-LANGUAGE-INVARIANT](work-pack/tasks/TASK-REPO-LANGUAGE-INVARIANT.md) | `REFINE-SEED-PROPOSAL.md`, repo Python drift list | Private parent policy | SWU-AUTH-001 | `development/invariants/`, `tools/` | shell checker and policy doc added | checker flags Python auth/runtime drift outside allowlist | `bash tools/check-runtime-language-policy.sh` | local-fallback | completed |
| SWU-BW-001 | [TASK-BODY-WAR-AUTH-CONSUMER](work-pack/tasks/TASK-BODY-WAR-AUTH-CONSUMER.md) | previous `server.py`, new `server.ts`, `static/app.js` | Body War auth-only scope | SWU-AUTH-004, SWU-AUTH-005 | `projects/body-war/` | Body War no longer imports Python auth package; consumes TS auth boundary | auth/status/Strava mocked flow passes | Body War auth smoke/contract test | local-fallback | completed |
| SWU-AUTH-008 | [TASK-AUTH-PRODUCTION-READINESS](work-pack/tasks/TASK-AUTH-PRODUCTION-READINESS.md) | Savvy decisions, auth package adapters | Production hardening | SWU-BW-001, SWU-INV-001 | `projects/auth-user-management/docs/`, `.env.example`, readiness docs | production store/secrets/runbook decisions recorded | readiness report passes review | reviewable checklist + secret-gated smoke plan | manual | completed-with-live-smoke-deferred |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target Date |
| --- | --- | --- | --- | --- | --- |
| B-AUTH-001 | production | Exact durable session/token store and encryption backend not selected | future L2/L3 | decide during production readiness SWU | deferred |
| B-AUTH-002 | live Strava | Real credential smoke requires secrets | operator | run only when credentials are available | deferred |

## Gate Checks

1. `SWU-AUTH-001` must execute first.
2. No auth package runtime acceptance while Python auth package remains the selected source.
3. TypeScript domain layer must not import infrastructure/interface libraries.
4. Browser protected routes must reject forged client auth state.
5. Strava tokens must remain server-side and untracked.
6. Body War auth acceptance requires no Python auth import.
7. Runtime language policy must be shell-checkable before it counts as invariant.

## Next Route

One-shot Task Session executed at `task-session/20260621T-auth-workpack-oneshot/`.
