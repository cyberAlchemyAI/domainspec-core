# S01 - Context Builder Evidence Baseline

Owner: `context-builder`
Mode: `standard --strict --emit both --handoff runtime`
Verdict: `pass`

## Task

Build a strict evidence baseline for correcting the auth/user-management implementation so it follows the DomainSpec Functional TypeScript architecture and establishes the repo invariant: shell first where sufficient, TypeScript otherwise.

## Obligation Coverage

| Obligation | Status | Evidence |
| --- | --- | --- |
| Import DomainSpec architecture | covered | `implementation/domainspec/architecture/ARCHITECTURE.md`, `pattern-library/ARCHITECTURE-FOUNDATIONS.md`, `LAYERING-REFERENCE.md`, `DEPENDENCY-RULES.md`, `TESTING-ALIGNMENT.md` |
| Make shell-first/TypeScript invariant explicit | covered | User correction plus DomainSpec package/tooling evidence in `implementation/domainspec/package.json` |
| Supersede Python auth work | covered | `projects/auth-user-management/src/auth_user_management/`, `projects/body-war/app/server.py`, `projects/body-war/app/test_auth_adapter.py` |
| Preserve auth goal and Strava connection | covered | Prior auth project docs, Body War pilot server, Strava adapter intent, user request |
| Reuse local auth references | covered | `validation/poker-team/backend/src/domain/auth-access-control/`, `validation/poker-team/backend/src/use-cases/auth-access-control/`, `projects/savvy_legal-studio-ai/.../lib/auth/savvy-auth.ts` |
| Keep game/track work deferred | covered | User instruction and refine seed non-goals |
| Keep public/private boundaries clean | covered | `AGENTS.md`, submodule discipline, dispatch boundary evidence |

## Selected Sources

### DomainSpec Architecture

- `implementation/domainspec/architecture/ARCHITECTURE.md`: architecture index; task-specific import path.
- `implementation/domainspec/architecture/pattern-library/ARCHITECTURE-FOUNDATIONS.md`: Functional TypeScript baseline, domain-first rule, pure functions/factories, no domain framework imports.
- `implementation/domainspec/architecture/pattern-library/LAYERING-REFERENCE.md`: domain/application/infrastructure/interface responsibilities and suggested `src/modules/<module>/...` layout.
- `implementation/domainspec/architecture/pattern-library/DEPENDENCY-RULES.md`: inward-only import rules and architecture-drift heuristic.
- `implementation/domainspec/architecture/pattern-library/TESTING-ALIGNMENT.md`: domain/application/workflow/infrastructure/interface test obligations.
- `implementation/domainspec/package.json`: pnpm/TypeScript workspace conventions.

### Auth Reference

- `validation/poker-team/backend/src/domain/auth-access-control/session.entity.ts`: session is a domain type with status, permissions, creation, and expiry.
- `validation/poker-team/backend/src/domain/auth-access-control/access-token.entity.ts`: token status, session binding, expiry, revocation, and scope.
- `validation/poker-team/backend/src/use-cases/auth-access-control/authenticate-request.ts`: required bearer token, token claim validation, revocation lookup, active session lookup, and auth context derivation.
- `validation/poker-team/backend/src/use-cases/auth-access-control/authorize-request.ts`: canonical permission key, deny override, and access-denied event pattern.
- `validation/poker-team/backend/src/infrastructure/http/auth/auth.guard.ts`: interface guard attaches auth context before route handlers and maps auth errors to 401/403.

### Browser Session Reference

- `projects/savvy_legal-studio-ai/DECISIONS.md`: selected hybrid boundary: external IdP for identity, secure httpOnly SameSite cookie for app session, app-owned authorization.
- `projects/savvy_legal-studio-ai/frontend/savvy-legal-studio/lib/auth/savvy-auth.ts`: cookie parsing, session lookup, expiry/revocation checks, CSRF binding, permission/resource checks, audit context.
- `projects/savvy_legal-studio-ai/frontend/savvy-legal-studio/tests/auth/savvy-auth.test.ts`: denial matrix rejects forged client auth state, malformed/unknown/expired/revoked/inactive sessions, CSRF failures, and missing permission.

### Drift To Retire

- `projects/auth-user-management/src/auth_user_management/`: Python runtime package created by the wrong pass.
- `projects/auth-user-management/tests/test_*.py`: Python tests matching the wrong package.
- `projects/body-war/app/server.py`: Python Body War server imports the Python auth package and should not remain the auth foundation.
- `projects/body-war/app/test_auth_adapter.py`: Python Body War auth adapter test should be replaced by TypeScript-compatible proof.

## Authority Precedence

1. User correction: shell first, then TypeScript; no Python auth foundation.
2. DomainSpec architecture: Functional TypeScript, domain-first, layer boundaries.
3. Auth references: poker-team and Savvy provide patterns, not product-specific permission names.
4. Existing Python artifacts: migration residue only.

## Gaps And Resolutions

- Exact Strava production token encryption backend is not selected. Resolution: represent it as an infrastructure port with local JSON pilot adapter and production database/secret-store adapter deferred to L2.
- Body War currently runs as a Python pilot server. Resolution: plan a TypeScript auth consumer boundary and either migrate the pilot server surface or place auth behind a TypeScript service/API before accepting production auth.
- Existing unrelated Python projects exist. Resolution: invariant applies to new/runtime work and the auth correction; legacy surfaces require later grandfather/migration decisions.

## Context Pack Summary

- Files selected: 15 source anchors.
- Obligation coverage: 100%.
- Strict coverage: pass.
- Blockers: 0.
- Handoff pack: runtime-ready evidence baseline for Invoke Define.
