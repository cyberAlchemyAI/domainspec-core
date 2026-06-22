# Refine Seed Proposal

Run ID: `20260621T-typescript-domainspec-invariant`

## Target

Repository-wide implementation invariant for projects inside `domainspec-core`, with immediate correction of the auth/user-management and Body War auth work that was incorrectly started in Python.

Primary architecture import:

- `implementation/domainspec/architecture/`
- `implementation/domainspec/architecture/pattern-library/ARCHITECTURE-FOUNDATIONS.md`
- `implementation/domainspec/architecture/pattern-library/LAYERING-REFERENCE.md`
- `implementation/domainspec/architecture/pattern-library/DEPENDENCY-RULES.md`
- `implementation/domainspec/architecture/pattern-library/TESTING-ALIGNMENT.md`

## Operator Intent

The previous auth implementation went the wrong direction. It should follow DomainSpec's Functional TypeScript implementation model. Across projects in this umbrella, implementation should be shell-first where shell is sufficient; otherwise TypeScript is the default runtime/application language.

## Invariant

1. Use `sh` scripts for deterministic orchestration, bootstrap, validation, repo checks, simple migrations, and glue where shell can express the job clearly.
2. Use TypeScript for application, domain, infrastructure, interface, and runtime behavior when shell is not the right tool.
3. Do not introduce Python as the default runtime/application implementation language for new `domainspec-core` project work.
4. Existing Python code is legacy or migration residue unless a future decision gate explicitly grants a scoped exception.
5. TypeScript implementation must follow the DomainSpec architecture model: domain-first, functional style, inward-only dependency flow, framework-agnostic domain, and explicit layer tests.

## Current Drift To Supersede

- `projects/auth-user-management/src/auth_user_management/*.py`
- `projects/auth-user-management/tests/test_*.py`
- `projects/body-war/app/server.py` auth integration changes that depend on the Python package
- `projects/body-war/app/test_auth_adapter.py`

These files should not become the production-ready auth foundation. They should be replaced or retired by a TypeScript package plus shell validation checks.

## Desired Outcome

A non-executed, DomainSpec-aligned implementation plan that:

- migrates `projects/auth-user-management` to a TypeScript package,
- uses shell scripts for repo-level validation and policy enforcement,
- provides Strava OAuth, browser cookie/session security, bearer-token API auth, and user-management boundaries in TypeScript,
- gives Body War a TypeScript-compatible auth integration path,
- records Python auth work as superseded drift,
- adds an enforceable language invariant for future project work.

## Write Scope

This refine run may write only:

- `development/refinement-runs/20260621T-typescript-domainspec-invariant/`

Later implementation may write:

- `projects/auth-user-management/`
- `projects/body-war/`
- a private parent-level invariant/check surface such as `development/invariants/` or `tools/check-runtime-language-policy.sh`

No writes are allowed to public `arcanum` unless a separate public-boundary decision approves it.

## Non-Goals

- Do not implement tracks, game mechanics, or non-auth Body War gameplay.
- Do not preserve Python as the auth runtime.
- Do not make existing unrelated historical Python projects conform in this run.
- Do not claim all legacy project code already satisfies the invariant.

## Validation Surface

Before runtime implementation is accepted, the follow-up task should validate:

- shell checker blocks new Python runtime/auth files outside explicit legacy allowlists,
- TypeScript package builds and checks with the repo's package-manager conventions,
- DomainSpec layer import rules are enforced or tested,
- auth domain/application tests cover sessions, token lifecycle, Strava linking, CSRF, and provider-state validation,
- Body War auth integration uses the TypeScript package or a typed boundary, not the retired Python package.

## Preset And Research

- Preset: `standard`
- Research: `no-research`

Local repository evidence is enough for this correction. External auth best-practice research can be a later bounded pass if a named gap appears.
