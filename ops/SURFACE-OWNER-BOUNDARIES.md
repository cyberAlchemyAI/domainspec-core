# Surface Owner Boundaries

Date: 2026-06-01
Status: accepted

## Purpose

Protect nested, submodule-owned, project-owned, and validation-owned runtime surfaces from parent-level Arcanum cleanup.

Parent-level cleanup may classify these paths, but it must not mutate them unless a task explicitly names the owner scope and write boundary.

## Owner Map

| Surface family | Owner scope | Observed runtime surfaces | Parent cleanup rule |
| --- | --- | --- | --- |
| Root Arcanum/DomainSpec repository | parent repo | root `.github/skills`, root `.arcanum`, root `.codex`, root `tools` | Parent task may mutate only when the work-pack names the root path. |
| Nested Arcanum source repo | `arcanum/` | `arcanum/.agents`, `arcanum/.arcanum`, `arcanum/.codex`, `arcanum/.github`, `arcanum/benchmark/.agents`, `arcanum/benchmark/.codex` | Treat as Arcanum-owned source/runtime state. Do not parent-sweep; use an Arcanum-owned task. |
| DomainSpec implementation repo | `implementation/domainspec/` | `.agents`, `.arcanum`, `.claude`, `.codex`, `.github`, `AGENTS.md`, `CLAUDE.md` | Treat as DomainSpec-owned. Parent task may record handoff only. |
| Project/demo workspaces | `projects/*` | `projects/body-war/.arcanum`, `projects/body-war/.codex`, `projects/goldenquill/.github`, `projects/sonar-loop/.arcanum`, `projects/sonar-loop/.github`, `projects/whisky-doses/.agents`, `projects/whisky-doses/.codex`, project `AGENTS.md`/`CLAUDE.md` | Treat as project-owned sandboxes. Do not move, delete, or normalize during root cleanup. |
| Validation fixtures | `validation/*` | `validation/poker-team/.github`, fixture `copilot-instructions.md` | Treat as fixture-owned. Mutate only from a validation task that names fixture expectations. |

## Guardrails

1. Before deleting or regenerating any runtime surface, classify the path as root-owned, nested Arcanum-owned, DomainSpec-owned, project-owned, validation-owned, machine-global, or generated local state.
2. Root cleanup tasks may update root policy docs that mention child scopes, but they must not edit child runtime files unless the task explicitly enters that owner scope.
3. Dirty nested repos or submodules are not evidence that parent cleanup should repair them.
4. If a child surface needs migration, create a separate work-pack with:
   - owner scope,
   - source of truth,
   - write scope,
   - validation surface,
   - rollback or backup policy.
5. Generated root state may be ignored or untracked from the parent only when it is parent-owned. Generated child state must be handled at the child owner boundary.

## Current Follow-Ups

- `implementation/domainspec/`: downstream native-skill/profile cleanup should be a DomainSpec-owned task.
- `arcanum/`: nested Arcanum runtime docs and benchmark surfaces should be migrated in an Arcanum-owned task, not by parent sweep.
- `projects/*`: project/demo surfaces should be classified only if the user asks to clean that project.
- `validation/*`: fixture runtime surfaces should be changed only with fixture expectation updates.
