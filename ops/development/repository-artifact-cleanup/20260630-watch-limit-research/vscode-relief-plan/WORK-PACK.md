---
module: vscode-workspace-file-watcher-relief
version: current
status: draft
updatedAt: 2026-06-30
docType: work-pack
---

# WORK-PACK: VS Code Workspace File-Watcher Relief

## Purpose

Create an execution-ready, low-complexity plan for the first safe relief action
after VS Code reported that it could not monitor file changes because of
repository size.

`SWU-VSCODE-001` has applied the settings change. The remaining validation
slice is `SWU-VSCODE-002`: reload VS Code through the workspace and inspect
Output: `Log (File Watcher)`.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Ready for bounded execution. |
| complexity | low | One workspace file, no source mutation, no cleanup/deletion. |
| outputMode | single-file | Task and SWU contracts are inline. |
| executionPackRef | n/a | Not required for low complexity. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | Companion layer-governance artifact. |
| dispatchTechniqueTrace | inline | Required Invoke plan technique trace below. |
| distillValidationStatus | pass | Distill validate pass recorded below. |
| activeLayerWindow | L0-L1 | Apply settings, then validate editor relief. |
| lastUpdatedAt | 2026-06-30T07:47:00Z | Updated after `SWU-VSCODE-001` execution. |
| readinessProfile | pilot | Local editor-relief pilot for this checkout. |

## Objective Summary

- Objective: Add workspace-level VS Code watcher/search exclusions for the
  high-pressure generated/runtime path classes identified by the research
  dispatch.
- Primary inputs:
  - `findings.md`
  - `research.md`
  - `vscode-workspaces/domainspec-core.code-workspace`
  - `validation/poker-team/domainspec-unified.code-workspace`
- Success condition: VS Code can monitor the workspace after reload, or the
  remaining warning/log gives a narrower follow-up cause, with no repository
  cleanup or owner-boundary mutation performed.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | Workspace settings patch contains watcher/search excludes for identified pressure classes. | L0 | W0 | Research findings and workspace file. | JSONC-aware review plus targeted diff review. |
| S-002 | Operator reload confirms whether VS Code watcher pressure is relieved. | L1 | W0 | S-001 complete. | Check VS Code `Log (File Watcher)` and absence/persistence of warning. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TASK-VSCODE-001 | Patch workspace watcher/search excludes. | L0 | low | W0 | `findings.md`, `research.md`, `vscode-workspaces/domainspec-core.code-workspace` | pass | completed |
| TASK-VSCODE-002 | Validate relief after reload and classify any residual issue. | L1 | low | W0 | TASK-VSCODE-001 result and VS Code Output logs | ready | not-started |

## Smallest Working Units

| SWU ID | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-VSCODE-001 | TASK-VSCODE-001 | `findings.md#Immediate VS Code Relief`; `research.md#Agent 1 - Robertson, Sam - Filesystem Pressure And VS Code Relief`; `vscode-workspaces/domainspec-core.code-workspace` | Prior workspace-config memory says this file is the local VS Code config target. | none | `vscode-workspaces/domainspec-core.code-workspace` | Add `files.watcherExclude` and `search.exclude` under existing `settings` without changing color settings. | Targeted diff shows only the intended workspace settings file changed. | Key-presence check, `git diff --check`, targeted diff review, and VS Code reload. | local-fallback | completed |
| SWU-VSCODE-002 | TASK-VSCODE-002 | TASK-VSCODE-001 diff; VS Code Output: `Log (File Watcher)` | If workspace is opened directly as a folder, use the `.code-workspace` file instead. | SWU-VSCODE-001 | no repository write required unless validation note is added later | Reload VS Code and determine whether warning disappears or residual pressure remains. | Operator-observed VS Code result; optional command outputs listed below. | `cat /proc/sys/fs/inotify/max_user_watches`; `cat /proc/sys/fs/inotify/max_user_instances`; optional `find . -path './.git' -prune -o -path '*/.git' -prune -o -type f | wc -l` | manual | ready |

Validation commands for SWU-VSCODE-001:

```bash
node -e "const s=require('fs').readFileSync('vscode-workspaces/domainspec-core.code-workspace','utf8'); for (const k of ['\"files.watcherExclude\"','\"search.exclude\"']) if (!s.includes(k)) throw new Error(k + ' missing')"
git diff --check -- vscode-workspaces/domainspec-core.code-workspace
git diff -- vscode-workspaces/domainspec-core.code-workspace
```

The workspace file is VS Code JSONC and already contains trailing commas, so a
strict JSON parser is not the right validation tool for this file.

## Proposed Workspace Settings Patch

Add these keys inside the existing `settings` object in
`vscode-workspaces/domainspec-core.code-workspace`:

```json
"files.watcherExclude": {
  "**/node_modules/**": true,
  "**/.lake/**": true,
  "**/.venv/**": true,
  "**/venv/**": true,
  "**/__pycache__/**": true,
  "**/.pytest_cache/**": true,
  "**/.mypy_cache/**": true,
  "**/.ruff_cache/**": true,
  "**/.formal-tools/**": true,
  "**/.claude/worktrees/**": true,
  "**/dist/**": true,
  "**/build/**": true,
  "**/coverage/**": true,
  "**/target/**": true,
  "**/.next/**": true,
  "**/.nuxt/**": true,
  "**/.svelte-kit/**": true,
  "**/out/**": true
},
"search.exclude": {
  "**/node_modules": true,
  "**/.lake": true,
  "**/.venv": true,
  "**/venv": true,
  "**/__pycache__": true,
  "**/.pytest_cache": true,
  "**/.mypy_cache": true,
  "**/.ruff_cache": true,
  "**/.formal-tools": true,
  "**/.claude/worktrees": true,
  "**/dist": true,
  "**/build": true,
  "**/coverage": true,
  "**/target": true,
  "**/.next": true,
  "**/.nuxt": true,
  "**/.svelte-kit": true,
  "**/out": true
}
```

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target Date |
| --- | --- | --- | --- | --- | --- |
| none | n/a | No acceptance-critical blocker remains for workspace reload validation. | n/a | Execute SWU-VSCODE-002 manually in VS Code. | 2026-06-30 |

## Execution Evidence

| Evidence | Result |
| --- | --- |
| `SWU-VSCODE-001` | completed |
| Context pack | `CONTEXT-PACK-SWU-VSCODE-001.md` |
| Task-session receipt | `TASK-SESSION-SWU-VSCODE-001.md` |
| File updated | `vscode-workspaces/domainspec-core.code-workspace` |
| Key-presence check | pass |
| JSONC-normalized parse | pass |
| `git diff --check` | pass |
| Kernel watch values | `max_user_watches=524288`; `max_user_instances=128` |
| Remaining validation | Reload VS Code through `vscode-workspaces/domainspec-core.code-workspace` and inspect Output: `Log (File Watcher)`. |

## Risks And Caveats

| Risk | Impact | Guardrail |
| --- | --- | --- |
| `.claude/worktrees` is actively being edited in this VS Code workspace. | Watch/search could skip files the operator currently cares about. | Drop or defer only that pattern during execution if active nested worktree editing is needed. |
| Broad `build`, `target`, and `out` excludes hide useful search results. | Search misses tracked benchmark/evidence files. | Keep these as editor relief only; do not use them as deletion proof. |
| User opens the repository folder directly instead of the `.code-workspace`. | Settings do not apply. | Reopen through `vscode-workspaces/domainspec-core.code-workspace`. |
| VS Code still warns after reload. | First relief slice is insufficient. | Use L2 classification: residual editor setting gap, system limit gap, or cleanup-governance gap. |

## Dispatch Technique Trace

| Technique ID | Applied To | Validation Expectation | Status |
| --- | --- | --- | --- |
| sequence | Research findings -> Invoke plan -> task-session SWU. | Execution consumes explicit evidence and source paths. | pass |
| concrete_path_evidence | Workspace target and research paths. | Plan cites concrete files, not broad globs as authority. | pass |
| scu_swu_reduction | First execution unit. | Selected unit is one config patch that recomposes into watcher relief. | pass |
| recomposition_proof | SWU-VSCODE-001 + SWU-VSCODE-002 -> immediate VS Code relief. | Settings patch plus reload can prove or narrow the original warning. | pass |
| validation_loop | JSONC-aware key check, targeted diff, VS Code reload/log check. | Every slice has executable evidence. | pass |
| owner_boundary_check | Parent workspace config only. | Plan does not mutate submodules, child projects, generated caches, or cleanup candidates. | pass |
| handle_handoff | Next route to `task-session`. | Handoff uses artifact paths and SWU IDs, not copied context. | pass |
| residue_ledger | Deferred cleanup and residual warning cases. | Remaining issues have owners and next routes. | pass |
| execution_receipt_handoff | Expected task-session receipt. | Execution should report files touched, validation commands, and VS Code result. | pass |

Full dispatch document: not required. This is a single-owner, single-file
workspace configuration plan with no subagents, protected external context, or
cross-capability delegation beyond a straightforward `task-session` handoff.

## Distill Validation

| Check | Result | Evidence Or Gap |
| --- | --- | --- |
| Smallest coherent unit or SWU boundary | pass | One `.code-workspace` settings patch is the smallest useful mutation; splitting by individual patterns would lose relief behavior. |
| Recomposition proof | pass | The patch covers the pressure classes that account for most files: `.lake`, `node_modules`, virtual environments, caches, and generated outputs. |
| Hidden acceptance-critical gaps | pass | The only operator caveat is whether `.claude/worktrees` is actively edited; it is named as a runtime choice, not a blocker. |
| Deferred complexity | pass | Repository cleanup, generated artifact deletion, discipline/constitution hardening, and inotify tuning are deferred. |
| Navigation to first executable unit | pass | Start with `SWU-VSCODE-001`; validation and residual classification are in `SWU-VSCODE-002`. |

Role trace:

| Role | Claim Or Objection | Reconciliation |
| --- | --- | --- |
| Proposer | The first relief move should be a workspace-only watcher/search exclude patch. | Accepted because research shows high generated/runtime file pressure and no existing excludes. |
| Balancer | Broad excludes can hide useful search results and `.claude/worktrees` may be actively edited. | Accepted as explicit caveats; no deletion or cleanup proof follows from the settings. |
| Balancer | If the repo is opened directly, workspace settings may not apply. | Accepted as validation guidance for SWU-VSCODE-002. |

Distill verdict: pass.

## Plan Transport Report

| Field | Value |
| --- | --- |
| observed capability | `invoke` |
| invoke mode | `plan` |
| target artifact name | VS Code Workspace File-Watcher Relief |
| target artifact type | neutral repository workspace configuration |
| owner/cycle | private parent workspace config; next route `task-session` |
| output paths | `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md` |
| invoke-specific gaps | none |
| target-artifact gaps | residual VS Code warning can only be classified after operator reload |
| recommended next route | `task-session` on `SWU-VSCODE-001`, then manual/operator validation on `SWU-VSCODE-002` |

## Gate Checks

1. Work-pack gate status is pass.
2. Complexity remains low: two tasks, two output artifacts, one workspace file.
3. Implementation-layering companion exists.
4. Dispatch technique trace is concrete and used.
5. Distill validation is pass.
6. SWUs include source anchors, write scope, done criteria, acceptance evidence,
   validation surfaces, execution owners, and handoff status.
7. No cleanup, deletion, generated-artifact mutation, submodule mutation, or
   owner-boundary mutation is authorized by this plan.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-06-30 | Initial Invoke plan for VS Code watcher relief. | Codex |
| 2026-06-30 | Executed `SWU-VSCODE-001`; workspace watcher/search excludes added and validated. | Codex |
