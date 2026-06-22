# Runtime Language Policy

Status: active for new auth/runtime work
Scope: private `domainspec-core` parent and project work

## Invariant

1. Use shell scripts for deterministic orchestration, bootstrap, validation, repo checks, and simple glue when shell can express the job clearly.
2. Use TypeScript for runtime, domain, application, infrastructure, interface, auth, user-management, provider, and app behavior.
3. Do not add new Python runtime/application code for project work unless a decision gate grants a scoped exception.
4. Existing Python-heavy projects are legacy surfaces until a later migration/grandfather decision names them explicitly.

## Current Enforcement

The shell checker at `tools/check-runtime-language-policy.sh` enforces the active auth correction boundary:

- no Python under `projects/auth-user-management/src` or `projects/auth-user-management/tests`,
- no Python server/test runtime under `projects/body-war/app`,
- TypeScript auth package metadata and validation script must exist,
- Body War app must use a TypeScript server/package boundary.

## Legacy Handling

Legacy Python prefixes are named in `runtime-language-legacy-allowlist.txt`.
They are not examples for new work. They are debt or separately governed systems.

## Promotion Rule

This policy becomes broader only when the checker broadens with it. Prose alone is not enough; every new invariant claim needs a shell validation path.
