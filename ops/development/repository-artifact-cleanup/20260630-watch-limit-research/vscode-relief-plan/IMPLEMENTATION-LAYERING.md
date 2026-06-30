---
module: vscode-workspace-file-watcher-relief
version: current
status: draft
updatedAt: 2026-06-30
docType: implementation-layering
---

# Implementation Layering: VS Code Workspace File-Watcher Relief

## Purpose

Define the smallest safe implementation path for relieving VS Code file watcher
pressure in `domainspec-core` without treating editor exclusions as repository
cleanup, deletion evidence, or ownership promotion.

## Source Contract

- Invoke mode contract: `.agents/skills/invoke/plan.md`
- Plan boundary contract:
  `arcanum/spells/invoke/development/PLAN-ARTIFACT-BOUNDARIES.md`
- Research evidence:
  `ops/development/repository-artifact-cleanup/20260630-watch-limit-research/findings.md`
- Workspace target: `vscode-workspaces/domainspec-core.code-workspace`

## Target And Scope

- Target: `vscode-workspaces/domainspec-core.code-workspace`
- Scope: editor workspace configuration
- Current state: brownfield workspace file with `settings.workbench.colorCustomizations`
  and no `files.watcherExclude` or `search.exclude` relief settings.

## Layer Boundary Rule

Every layer answers:

```text
After this layer, we know whether the current editor-relief move solves the
observed VS Code watcher pressure without broad cleanup.
```

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (POC) | After this layer, we know whether workspace-level watcher/search excludes can reduce the immediate high-pressure path classes. | Add `files.watcherExclude` and `search.exclude` entries to the single workspace file. | `.lake`, `node_modules`, `.venv`, `venv`, Python caches, build outputs, coverage, front-end generated dirs, `.formal-tools`, and `.claude/worktrees`. | Any deletion, `.gitignore` change, system inotify tuning, or owner-scoped cleanup. | JSONC-aware review succeeds and the workspace diff only touches the intended settings file. | Continue to L1 validation if the edit is clean. |
| L1 | After this layer, we know whether the editor warning is gone or materially reduced after reload. | Reload VS Code through the workspace and inspect `Log (File Watcher)`. | Operator-side validation plus optional count commands from the research packet. | Cleanup sigil, discipline, constitution, and directory-by-directory dry-run process. | VS Code no longer warns, or the remaining warning identifies a narrower pressure source. | Stop if warning is resolved; otherwise route a second relief slice. |
| L2 | After this layer, we know whether residual pressure requires policy or owner-bound cleanup rather than editor config. | Compare remaining warning/log evidence against pressure classes and owner boundaries. | Decision note or follow-up task-session route if editor config is insufficient. | Destructive cleanup and submodule/nested-owner mutation. | Residual issue is classified as editor setting gap, system limit gap, or cleanup-governance gap. | Route to decision-gate or cleanup discipline only if L1 evidence requires it. |
| L3 | After this layer, we know whether the relief pattern should be packaged for reuse. | Convert the successful pattern into a reusable rule or checklist. | Documentation or constitution/discipline candidate only after validated relief. | Generic cleanup sigil implementation. | Validated settings plus owner-safe caveats. | Package later; do not block immediate relief. |

## Non Regression Guardrails

- Do not delete, untrack, regenerate, archive, or move repository artifacts in
  this relief slice.
- Do not mutate `arcanum/`, `implementation/domainspec/`, `projects/*`, or
  `validation/*`; this plan targets the parent workspace file only.
- Treat `search.exclude` and `files.watcherExclude` as editor relief, not proof
  that a path is safe to remove.
- If the user is actively editing nested worktrees under `.claude/worktrees`,
  remove or defer that single exclude pattern before applying.
- If the repo is opened as a folder instead of through
  `vscode-workspaces/domainspec-core.code-workspace`, these workspace settings
  will not apply.

## Recommended Next Layer

- Next layer: L0
- Key decision unlocked: whether a single workspace settings patch can relieve
  VS Code watcher pressure.
- Major deferred scope: deletion, cleanup sigil development, constitution
  hardening, owner-scoped dry-run ledgers, and system-level inotify changes.
