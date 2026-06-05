# Arcanum State Classification

Date: 2026-05-29
Task: `TASK-RUNTIME-002`
SWU: `SWU-RUNTIME-002`
Status: pass

## Objective

Classify `.arcanum` state before untracking, deleting, regenerating, or treating any runtime artifact as canonical source.

Covered scopes:

- root `.arcanum/`
- `arcanum/.arcanum/`
- `implementation/domainspec/.arcanum/`

## Summary

| Scope | Status | Policy |
| --- | --- | --- |
| root `.arcanum/` | mixed tracked config, generated adapters, durable ledgers, ignored run state | Keep only classified config, intentional evidence, and generated-native package surfaces with provenance. |
| `arcanum/.arcanum/` | local/private runtime and smoke state; not tracked by parent | Do not track; ignore or preserve locally. |
| `implementation/domainspec/.arcanum/` | no parent-tracked files found | DomainSpec-owned if present; do not parent-edit. |

## Root `.arcanum` Classification

| Path | Class | Current tracking | Policy | Target action |
| --- | --- | --- | --- | --- |
| `.arcanum/necronomicon/README.md` | durable repo-local knowledge config | tracked | Keep if Necronomicon remains an accepted root capability index. | Preserve; revisit only in Necronomicon-specific cleanup. |
| `.arcanum/necronomicon/capabilities.json` | durable repo-local knowledge index | tracked | Keep if used as root capability index; not canonical source. | Preserve with provenance note in future. |
| `.arcanum/necronomicon/capability-updates/.gitkeep` | structure marker | tracked | Keep only if capability update queue remains used. | Preserve. |
| `.arcanum/necronomicon/sessions/.gitkeep` | structure marker | tracked | Keep only if Necronomicon sessions remain accepted local state. | Preserve. |
| `.arcanum/observability/README.md` | durable observability config/doc | tracked | Keep. | Preserve. |
| `.arcanum/observability/config.json` | durable observability config | tracked | Keep. | Preserve. |
| `.arcanum/observability/by-sigil/.gitkeep` | structure marker | tracked | Keep. | Preserve. |
| `.arcanum/observability/by-sigil/experiment-harness.jsonl` | generated evidence ledger | tracked before `TASK-SURFACE-006` | Generated/local by default; promote only by explicit evidence decision. | Untrack and ignore by default. |
| `.arcanum/observability/signals/sigil-invocations.jsonl` | generated evidence ledger | tracked before `TASK-SURFACE-006` | Generated/local by default; promote only by explicit evidence decision. | Untrack and ignore by default. |
| `.arcanum/observability/reflection-state.json` | generated reflection state | tracked before `TASK-SURFACE-006` | Generated/local by default; promote only by explicit evidence decision. | Untrack and ignore by default. |
| `.arcanum/observability/reflections/.gitkeep` | structure marker | tracked | Keep. | Preserve. |
| `.arcanum/observability/runs/.gitignore` | ignore policy | tracked | Keep. | Preserve. |
| `.arcanum/observability/runs/.gitkeep` | structure marker | tracked | Keep. | Preserve. |
| `.arcanum/observability/runs/**` | generated run state | untracked/ignored by current git listing | Do not track by default. | Preserve locally; no parent cleanup unless explicitly requested. |
| `.arcanum/observability/hooks/.gitignore` | ignore policy | tracked | Keep. | Preserve. |
| `.arcanum/observability/hooks/*.jsonl` | generated hook state | not tracked by current git listing | Do not track by default. | Preserve locally; no parent cleanup unless explicitly requested. |
| `.arcanum/runtimes/codex/commands/*.md` | legacy command adapter snapshots | tracked but currently deleted in worktree | Commands are not default runtime surface. | Preserve deletion unless explicit compatibility requirement appears. |
| `.arcanum/runtimes/github-copilot/sigils/**` | generated Copilot/GitHub-native package source snapshot | tracked before `TASK-SURFACE-004` | Generated runtime package cache, not canonical source. | Untrack and regenerate on demand; root `.github/skills/arcanum-*` is now self-provenanced. |
| `.arcanum/runtimes/github-copilot/skills/**` | generated Copilot/GitHub-native skill package snapshot | tracked before `TASK-SURFACE-004` | Generated runtime package cache, not canonical source. | Untrack and regenerate on demand; active root packages no longer depend on this cache. |
| `.arcanum/runtimes/github-copilot/spells/**` | generated Copilot/GitHub-native spell package snapshot | tracked before `TASK-SURFACE-004` | Generated runtime package cache, not canonical source. | Untrack and regenerate on demand; root `.github/skills/arcanum-*` is now self-provenanced. |

## `arcanum/.arcanum` Classification

`arcanum/.arcanum` contains local runtime state including:

- `codex-home/`
- `codex-home-smoke/`
- runtime adapters/config/runs
- local observability state
- Necronomicon state

Parent repository tracking check found no parent-tracked files under `arcanum/.arcanum`.

Classification:

- `surface_class`: local/private and submodule-local runtime state
- `target_action`: do not parent-track; do not parent-edit
- `cleanup_policy`: preserve locally unless the Arcanum submodule owner approves cleanup
- `ignore_policy`: should be ignored at the owning repository boundary

## `implementation/domainspec/.arcanum` Classification

Parent repository tracking check found no parent-tracked files under `implementation/domainspec/.arcanum`.

Classification:

- `surface_class`: DomainSpec-owned runtime state if present
- `target_action`: do not parent-edit
- `cleanup_policy`: route through DomainSpec-owned task

## Decisions Recorded

- Root `.arcanum/runtimes/codex/commands/*.md` deletions are valid under the current skills-first policy.
- Root `.arcanum/runtimes/github-copilot/**` is a generated runtime package cache, not canonical source, and is ignored after `TASK-SURFACE-004`.
- Root `.arcanum/observability` has a split policy:
  - config/docs/structure markers are durable,
  - ledgers and reflection state are generated/local by default,
  - promoted evidence requires an explicit decision and should not be default runtime churn.
- `arcanum/.arcanum/codex-home*` is local/private state and should never become tracked parent source.

## Recommended Follow-Up

1. Add provenance metadata for generated runtime packages during `TASK-RUNTIME-007`.
2. Promote selected observability JSONL excerpts only when they are intentionally durable repository evidence.
3. Add ignore rules at the appropriate repository boundary for local/private `.arcanum` runtime homes if the owning repo lacks them.
4. Preserve command adapter deletions through `TASK-RUNTIME-006`.

## Validation

Commands used:

```bash
find .arcanum -maxdepth 5 -type f -o -type d
find arcanum/.arcanum implementation/domainspec/.arcanum -maxdepth 5 -type f -o -type d
git ls-files .arcanum arcanum/.arcanum implementation/domainspec/.arcanum
git status --short .arcanum arcanum/.arcanum implementation/domainspec/.arcanum
```

Gate verdict:

- `G-RUNTIME-002`: pass. `.arcanum` generated/private state is classified before untracking or deletion.
