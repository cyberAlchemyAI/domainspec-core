# Refined Synthesis: Finish Surface Migration

Date: 2026-06-01
Status: pass

## Current Finish State

The migration blocker-level decision has been resolved:

- GitHub/Copilot Arcanum package naming policy: preserve current root discovery names.

Everything else is either already accepted policy or a bounded task waiting behind that naming decision.

## Accepted Policies Already Available For Execution

| Area | Accepted policy | Next execution task |
| --- | --- | --- |
| Personal Codex | Stage, back up replaced packages, promote generated native packages. Completed. | none |
| GitHub/Copilot cache | Use `.arcanum/runtimes/github-copilot` as untracked/regenerated cache after root packages are self-provenanced. | `TASK-SURFACE-004` |
| Root duplicate DomainSpec/GSD skills | Keep until runtime confirmation. | no deletion in Arcanum cleanup |
| Observability generated state | Ignore generated ledgers by default, promote selectively. | `TASK-SURFACE-006` |
| Legacy `sigils-library` | Delete candidate after targeted diff/preservation review. | legacy-name cleanup task |
| Root command adapters | Preserve current tracked deletions unless compatibility reopens. | `TASK-SURFACE-005` |

## Remaining Blocker

`TASK-SURFACE-003` can continue with the selected policy: preserve current GitHub/Copilot discovery names and regenerate package bodies behind those names:

- `arcanum-sigil-context-builder`
- `arcanum-sigil-task-session`
- `arcanum-spell-invoke`
- `arcanum-spell-implementation-readiness`

This avoids renaming the collaboration runtime while still removing wrapper-to-cache behavior.

## Finish Path After Decision

1. Implement GitHub/Copilot naming profile in `arcanum/tools/bootstrap_arcanum.sh`.
2. Stage `github-copilot` output and verify it generates the accepted package names.
3. Replace only root `.github/skills/arcanum-*` packages, preserving DomainSpec/GSD families.
4. Confirm root Arcanum packages no longer point to `.arcanum/runtimes/github-copilot`.
5. Apply cache policy 2B: untrack/regenerate `.arcanum/runtimes/github-copilot` on demand.
6. Finalize root legacy command adapter deletions.
7. Apply observability generated-state policy 4A.
8. Run targeted `sigils-library` diff/preservation review, then delete if no unique value remains.
9. Record owner-boundary protection for submodules and projects.

## Recommended Next Route

`task-session` for `TASK-SURFACE-003`.
