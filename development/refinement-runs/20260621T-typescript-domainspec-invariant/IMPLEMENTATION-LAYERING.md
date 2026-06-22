# Implementation Layering: Auth User Management TypeScript Correction

## Purpose

Define the decision-first implementation layers for replacing the wrong Python auth foundation with a DomainSpec-aligned TypeScript auth/user-management package and shell-first validation invariant.

## Target And Scope

- Target: `projects/auth-user-management` plus Body War auth consumer boundary.
- Scope: capability + workflow + repo policy.
- Current state: partially implemented in the wrong language.

## Layer Boundary Rule

After this layer, we know whether the selected boundary is true before promoting to the next layer.

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (POC) | After this layer, we know whether auth work can be corrected into a TypeScript package boundary without Python runtime inheritance. | `SWU-AUTH-001` | package metadata, TS config, layer folders, public exports, shell validation, Python auth retirement marker/removal | full auth behavior, Body War consumer, durable storage | `scripts/validate.sh`, TS check, no Python auth runtime files selected as package source | continue to L1 if package compiles and invariant check has a foothold |
| L1 | After this layer, we know whether the reusable auth behavior is credible in TypeScript. | `SWU-AUTH-002` to `SWU-AUTH-005` | domain/session/token/permission rules, browser session guard, bearer guard, Strava provider, tests | production DB/secret store, live Strava smoke | domain/app/interface tests and denial matrix | harden to L2 if deny-by-default and Strava mocked flow pass |
| L2 | After this layer, we know whether reliability and governance hold across consumer and repo policy. | `SWU-INV-001`, `SWU-BW-001` | repo runtime-language policy checker, Body War consumes TS auth boundary, docs updated | broad migration of unrelated Python projects | shell policy check, Body War auth smoke/contract tests | scale to L3 if Body War no longer depends on Python auth |
| L3 | After this layer, we know whether production packaging and operational proof are credible. | `SWU-AUTH-008` | durable session/token store selection, token encryption, env docs, runbook, live Strava credential smoke gate | multi-project migration program | production readiness report and manual secret-gated smoke evidence | package/pilot or defer |

## Non Regression Guardrails

- No later layer may reintroduce Python as auth runtime.
- Domain files must stay framework/library free.
- Provider tokens never return to browser clients or tracked artifacts.
- Body War auth acceptance requires server-derived auth context, not request body auth state.
- Repo invariant must be machine-checkable by shell before it is considered active.

## Recommended Next Layer

- Next layer: L0
- Key decision unlocked: TypeScript package boundary can replace the Python auth foundation.
- Major deferred scope: production storage, live Strava credentials, broad legacy Python migration.
