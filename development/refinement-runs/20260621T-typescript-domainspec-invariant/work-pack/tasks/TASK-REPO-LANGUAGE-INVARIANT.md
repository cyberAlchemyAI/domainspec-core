# TASK-REPO-LANGUAGE-INVARIANT

## Objective

Make the private parent invariant enforceable: use shell where shell is sufficient; use TypeScript for runtime/application/domain behavior; do not add new Python auth/runtime code without an explicit exception.

## Source Contracts

- `REFINE-SEED-PROPOSAL.md`
- `IMPLEMENTATION-LAYERING.md`
- current drift scan from `projects/`

## Smallest Working Units

### SWU-INV-001 - Shell Runtime Language Policy Check

- Dependencies: `SWU-AUTH-001`.
- Write scope: `development/invariants/`, `tools/`, optional root docs index.
- Done criteria: policy doc and shell checker exist; checker has allowlist/legacy mode; checker blocks Python under new auth/runtime package paths.
- Acceptance evidence: `bash tools/check-runtime-language-policy.sh` passes on current accepted state and fails on a temporary fixture or documented dry-run scenario.
- Execution owner: local-fallback.
- Handoff note: this is private-parent policy first; do not write to public `arcanum`.

## Synchronization

Record any legacy Python allowlist as explicit debt. Do not silently grandfather new runtime work.
