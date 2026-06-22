# TASK-AUTH-TYPESCRIPT-SPINE

## Objective

Replace the Python auth foundation with a DomainSpec-aligned TypeScript auth/user-management package.

## Source Contracts

- `implementation/domainspec/architecture/pattern-library/ARCHITECTURE-FOUNDATIONS.md`
- `implementation/domainspec/architecture/pattern-library/LAYERING-REFERENCE.md`
- `implementation/domainspec/architecture/pattern-library/DEPENDENCY-RULES.md`
- `validation/poker-team/backend/src/domain/auth-access-control/`
- `validation/poker-team/backend/src/use-cases/auth-access-control/`
- `projects/savvy_legal-studio-ai/frontend/savvy-legal-studio/lib/auth/savvy-auth.ts`
- `projects/auth-user-management/src/auth_user_management/`

## Smallest Working Units

### SWU-AUTH-001 - TypeScript Auth Package Baseline

- Dependencies: none.
- Write scope: `projects/auth-user-management/`.
- Source anchors: current Python package, DomainSpec layer reference, package conventions.
- Done criteria: package metadata, TypeScript config, source layer folders, public exports, shell validation script; Python auth runtime removed/quarantined/marked obsolete.
- Acceptance evidence: `bash projects/auth-user-management/scripts/validate.sh` passes.
- Execution owner: local-fallback.
- Handoff note: do this first; do not implement behavior until language/package boundary is fixed.

### SWU-AUTH-002 - Domain Auth Model

- Dependencies: `SWU-AUTH-001`.
- Write scope: `projects/auth-user-management/src/modules/auth/domain/`.
- Done criteria: principal, session, access token, permission, auth context, lifecycle policies, OAuth state/provider account domain types.
- Acceptance evidence: domain tests pass.
- Execution owner: local-fallback.

### SWU-AUTH-003 - Application Use Cases

- Dependencies: `SWU-AUTH-002`.
- Write scope: `projects/auth-user-management/src/modules/auth/application/`.
- Done criteria: create session, authenticate request, authorize request, logout/revoke, start/complete provider link contracts.
- Acceptance evidence: use-case tests with mocked ports pass.
- Execution owner: local-fallback.

### SWU-AUTH-004 - Browser Session Interface

- Dependencies: `SWU-AUTH-003`.
- Write scope: `projects/auth-user-management/src/modules/auth/interface/`, `src/modules/auth/infrastructure/`.
- Done criteria: cookie parsing, httpOnly session cookie contract, readable CSRF binding, same-origin check, resource scope authorization, local stores.
- Acceptance evidence: forged/missing/malformed/expired/revoked/inactive/CSRF/permission denial matrix passes.
- Execution owner: local-fallback.

### SWU-AUTH-005 - Strava Provider Module

- Dependencies: `SWU-AUTH-003`.
- Write scope: `projects/auth-user-management/src/modules/providers/strava/`.
- Done criteria: OAuth start/callback, scope validation, token custody, refresh, redacted activity summary import behind ports.
- Acceptance evidence: mocked Strava tests pass; public status omits tokens.
- Execution owner: local-fallback.

## Synchronization

Update `WORK-PACK.md` after each SWU with receipt path, files touched, validation, blockers, and residue.
