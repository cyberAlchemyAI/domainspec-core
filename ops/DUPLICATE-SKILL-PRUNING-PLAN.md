# Duplicate Skill Pruning Plan

Date: 2026-05-29
Status: plan-ready, partially executed

## Objective

Reduce duplicated Codex/Arcanum/DomainSpec skill surfaces by leaving only the most recent full skill body for each capability, while preserving thin aliases when they are intentional operator names.

## Rule

For each normalized skill capability:

1. If there is one full skill body and one or more thin aliases, keep the full body and aliases.
2. If there are multiple full skill bodies for the same capability, keep the newest full body by file mtime.
3. If the older body belongs to a different owner surface, do not delete it until that owner is confirmed.
4. If two files are byte-identical and one is in an obvious copy folder, delete the copy only inside an owner-approved task.
5. Never use command files as the keeper for a skill capability.

## Normalization

Names are compared after removing these prefixes when they are only surface labels:

- `arcanum-`
- `arcanum-sigil-`
- `arcanum-spell-`
- `domainspec-`

Examples:

- `arcanum-sigil-context-builder`, `domainspec-context-builder`, and `arcanum-context-builder` normalize to `context-builder`.
- `invoke` and `arcanum-invoke` normalize to `invoke`.

## Current Safe Action

The personal Codex duplicate for `refine` was already converted:

- Keeper full body: `/mnt/c/Users/vlad_/.codex/skills/arcanum-refine/SKILL.md`
- Alias: `/mnt/c/Users/vlad_/.codex/skills/refine/SKILL.md`

This leaves one full personal skill body and one thin operator alias.

## Gated Duplicate Groups

These groups have duplicates but are not safe to delete from the parent repository task without owner confirmation.

| Group | Newest observed keeper | Older/gated copies | Gate |
| --- | --- | --- | --- |
| `domainspec-*` root vs DomainSpec `.agents` | `implementation/domainspec/.agents/skills/*` | `.github/skills/domainspec-*` | DomainSpec owner must confirm whether root copies are distribution adapters or stale copies. |
| `gsd-*` root vs DomainSpec `.agents` | `implementation/domainspec/.agents/skills/*` | `.github/skills/gsd-*` | DomainSpec/GSD owner must confirm root adapter role. |
| Arcanum sigil wrappers | personal Codex skill or `.github/skills/arcanum-*`, depending runtime | duplicate-looking root wrappers | Need distinguish Codex install from GitHub Copilot distribution adapters. |
| `gitnexus copy/*` vs `gitnexus/*` | same timestamp and identical content | `implementation/domainspec/.agents/skills/gitnexus copy/*` | DomainSpec-owned deletion candidate; exact duplicate but submodule-local. |

## Exact Duplicate Evidence

Exact duplicate `SKILL.md` hashes were found for:

- `implementation/domainspec/.agents/skills/gitnexus copy/*` vs `implementation/domainspec/.agents/skills/gitnexus/*`
- `.github/skills/domainspec-feature-glossary/SKILL.md` vs `implementation/domainspec/.agents/skills/domainspec-feature-glossary/SKILL.md`
- `.github/skills/domainspec-definitions-governance/SKILL.md` vs `implementation/domainspec/.agents/skills/domainspec-definitions-governance/SKILL.md`

These are strong cleanup candidates, but the first is submodule-local and the latter two cross owner boundaries.

## Work Plan

### TASK-DUP-001 - Personal Codex Duplicate Pass

Status: done

Deliverable:

- Convert personal duplicate short names into aliases or delete them if aliases are no longer desired.

Current result:

- `refine` is a thin alias to `arcanum-refine`.
- `arcanum-invoke` is a thin alias to `invoke`.

### TASK-DUP-002 - Root `.github/skills` Classification

Status: done / flag

Deliverable:

- Classify every root skill as `root-owned`, `distribution-adapter`, `personal-codex-duplicate`, `domainspec-duplicate`, `arcanum-duplicate`, or `cleanup-candidate`.

Done criteria:

- A table exists with keeper path, delete/keep action, owner, and evidence.
- No deletion happens until distribution adapters are distinguished from stale copies.

Result:

- Classification table: `ops/ROOT-GITHUB-SKILLS-CLASSIFICATION.md`.
- 33 Arcanum root skills classified as `distribution-adapter`.
- 15 root skills classified as `root-owned`.
- 3 root skills classified as `personal-codex-duplicate` with `keep-root-until-runtime-confirmed`.
- 94 root skills classified as `domainspec-duplicate` with `gate-delete`.
- No deletion performed in this task because `gate-delete` rows still need owner/runtime confirmation.

### TASK-DUP-003 - DomainSpec-Owned Duplicate Deletion

Status: gated

Deliverable:

- In a DomainSpec-owned task, delete exact duplicate `gitnexus copy/*` if the owner confirms it is an accidental copy.

Done criteria:

- DomainSpec submodule status is clean or intentionally changed.
- Exact duplicate hashes are recorded before deletion.

### TASK-DUP-004 - Root Adapter Pruning

Status: gated

Deliverable:

- Delete root `.github/skills` packages that are older duplicates and not required as GitHub Copilot distribution adapters.

Done criteria:

- Each deleted path has a newer keeper.
- Each deleted path is mapped to a canonical personal, Arcanum, or DomainSpec skill.

## Invoke Result

- Mode: plan
- Target: duplicate skill pruning, leaving only the most recent full skill body
- Status: flag
- Canonical sources used: `ops/CODEX-SKILL-SURFACE-POLICY.md`, `tools/audit_codex_skill_surface.sh`, current skill surface scan
- Artifacts produced or updated: `ops/DUPLICATE-SKILL-PRUNING-PLAN.md`
- Decisions: keep newest full body; preserve thin aliases; gate owner-boundary deletions
- Gaps: root `.github/skills` and DomainSpec `.agents/skills` require owner classification before deletion
- Validation: duplicate scans identified exact duplicates and normalized collision groups
- Next route: task-session
