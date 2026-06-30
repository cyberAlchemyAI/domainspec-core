---
task: SWU-VSCODE-001
mode: lean
status: pass
createdAt: 2026-06-30
docType: task-session-context-pack
---

# Context Pack: SWU-VSCODE-001

## Task

Patch `vscode-workspaces/domainspec-core.code-workspace` with workspace-level
VS Code watcher/search exclusions for the generated/runtime pressure classes
identified by the repository cleanup research dispatch.

## Obligation Coverage

| Obligation | Required Evidence | Coverage |
| --- | --- | --- |
| Select exactly one executable SWU. | `WORK-PACK.md#Smallest Working Units` selects `SWU-VSCODE-001`. | covered |
| Keep writes inside declared scope. | `WORK-PACK.md` write scope is `vscode-workspaces/domainspec-core.code-workspace`. | covered |
| Preserve existing workspace color settings. | Current workspace file contains `settings.workbench.colorCustomizations`. | covered |
| Add watcher and search excludes for pressure classes. | `findings.md#Immediate VS Code Relief` and `research.md#Agent 1 - Robertson, Sam - Filesystem Pressure And VS Code Relief`. | covered |
| Treat exclusions as editor relief, not cleanup evidence. | `IMPLEMENTATION-LAYERING.md#Non Regression Guardrails`. | covered |
| Validate with key presence, diff check, and targeted diff review. | `WORK-PACK.md#Smallest Working Units` and validation commands. | covered |

Strict coverage: pass.

## Included Context

- `WORK-PACK.md` - task contract, write scope, validation commands, and
  selected SWU.
- `IMPLEMENTATION-LAYERING.md` - non-regression guardrails and deferred cleanup
  scope.
- `findings.md` - recommended initial settings and caveats.
- `research.md` - pressure counts and high-pressure path classes.
- `vscode-workspaces/domainspec-core.code-workspace` - target workspace file.
- `validation/poker-team/domainspec-unified.code-workspace` - local example of
  workspace-level `search.exclude`.
- Memory note `MEMORY.md:2599-2627` - this checkout's workspace config target
  and tight edit-scope precedent.

## Constraints

- Do not delete, untrack, archive, regenerate, or move repository artifacts.
- Do not mutate submodules, nested project owners, or generated caches.
- Keep `.claude/worktrees` exclusion as editor relief only; if the operator is
  actively editing those nested worktrees in this workspace, remove that single
  pattern in a later scoped patch.
- Do not use a strict JSON parser as the workspace syntax check; the file is
  VS Code JSONC and already contains trailing commas.

## Execution Path

1. Add `files.watcherExclude` and `search.exclude` under the existing
   `settings` object.
2. Preserve `window.title` and `workbench.colorCustomizations`.
3. Run key-presence, diff whitespace, and targeted diff checks.
4. Synchronize the work-pack with completion evidence.
5. Leave VS Code reload/log inspection as `SWU-VSCODE-002`.
