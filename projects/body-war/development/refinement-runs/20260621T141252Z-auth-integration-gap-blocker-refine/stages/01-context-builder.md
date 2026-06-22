# Context Pack Summary

Stage: `s01-context-builder`
Owner: `context-builder`
Status: `pass`
Mode: `standard`
Handoff pack: `runtime`
Strict coverage: `pass`

## Task

Build a local evidence baseline for the BodyWar auth integration gap/blocker
review before `task-session` execution.

## Obligation Coverage

| Obligation | Status | Evidence |
| --- | --- | --- |
| Identify whether `SWU-BWAUTH-001` is blocked. | covered | `WORK-PACK.md`, `INVOKE-AUTH-INTEGRATION-REPORT.md` |
| Identify whether the current BodyWar app is blocked. | covered | `projects/body-war/app/server.ts`, fresh `npm --prefix projects/body-war/app run check` receipt |
| Identify package/app ownership split. | covered | `AUTH-INTEGRATION-SPEC.md`, `AUTH-INTEGRATION-DESIGN.md`, `projects/auth-user-management/src/index.ts` |
| Identify local integration blockers. | covered | `WORK-PACK.md`, `AUTH-INTEGRATION-SPEC.md`, `AUTH-INTEGRATION-DESIGN.md` |
| Identify online proof blockers. | covered | `projects/body-war/docs/decisions/vps-deployment-readiness.md` |
| Identify project-level residue. | covered | `projects/body-war/.craft/ledger.yml` |
| Avoid protected state. | covered | Only local docs/source and safe command output were used; no secrets, tokens, OAuth codes, or raw private activity payloads were requested. |

## Included Context

- `projects/body-war/development/invoke-runs/20260621T131933Z-auth-user-management-integration/WORK-PACK.md` - SWU manifest, constraints, validation strategy, blockers, next route.
- `projects/body-war/development/invoke-runs/20260621T131933Z-auth-user-management-integration/AUTH-INTEGRATION-SPEC.md` - package versus BodyWar capability boundary, security invariants, acceptance criteria.
- `projects/body-war/development/invoke-runs/20260621T131933Z-auth-user-management-integration/AUTH-INTEGRATION-DESIGN.md` - six-view design, workflow, dependency interfaces, risks, recomposition path.
- `projects/body-war/development/invoke-runs/20260621T131933Z-auth-user-management-integration/INVOKE-AUTH-INTEGRATION-REPORT.md` - existing invoke verdict, current compile failure, selected first SWU.
- `projects/body-war/app/server.ts` - current imports from `@domainspec/auth-user-management` that do not match the current package boundary.
- `projects/body-war/app/tests/auth-consumer.test.ts` - current tests depend on non-exported browser guard and JSON store helpers.
- `projects/auth-user-management/src/index.ts` - actual package root exports.
- `projects/body-war/.craft/ledger.yml` - active BodyWar blockers and gaps.
- `projects/body-war/docs/decisions/vps-deployment-readiness.md` - operator-gated VPS, origin, Strava, and activity decisions.

## Fresh Validation Receipt

Command:

```sh
npm --prefix projects/body-war/app run check
```

Result: `block-current-app`

Observed TypeScript failures include missing exports from
`@domainspec/auth-user-management` for `DEFAULT_STRAVA_SCOPE`, `allow`,
`createBrowserSessionGuard`, `createJsonAuthStore`, `createPrincipal`,
`createStravaProviderAdapter`, `parseCookieHeader`, `AppError`, `AuthStore`,
`CookieMap`, and `ProviderAccount`, plus `Principal.displayName`.

## Receipt

```yaml
run_id: 20260621T141252Z-auth-integration-gap-blocker-refine
session_id: session-20260621T141252Z
capability_ref: context-builder
receipt_kind: native-stage
artifact: stages/01-context-builder.md
status: pass
validation_result: strict coverage pass; fresh BodyWar app check captured as current-state blocker
blockers:
  - current BodyWar app compile is blocked by auth package export mismatch
handoff_note: Use this context to review define/design/plan artifacts without requesting protected runtime state.
```
