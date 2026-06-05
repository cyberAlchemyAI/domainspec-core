# Codex Skill Surface Policy

Date: 2026-05-29
Status: active for Codex/Arcanum/DomainSpec cleanup

## Purpose

Keep one Codex-facing skill surface for the DomainSpec Core, Arcanum, and DomainSpec workflow stack.

The desired shape is not "hand-maintain every skill in every repository." The desired shape is:

```text
canonical source
  -> generated native runtime package
  -> thin aliases where operators need alternate names
```

## Decision

The machine-global Codex skill directory is the only Codex-facing install surface:

```text
/mnt/c/Users/vlad_/.codex/skills/
```

Repository-local skill directories may exist for other runtimes, fixtures, or source-controlled distribution, but they are not the Codex install surface. They are valid when generated from canonical source into the runtime's expected native package shape with provenance.

## Surface Types

| Surface | Paths | Role | Policy |
| --- | --- | --- | --- |
| Canonical Arcanum source | `arcanum/arcana/*`, `arcanum/spells/*`, `arcanum/transmutations/*` | lifecycle source | Edit here first. |
| Canonical DomainSpec source | `implementation/domainspec/copilot/skills/*`, DomainSpec framework docs | DomainSpec source | Owned by the DomainSpec submodule. |
| Personal Codex skill surface | `/mnt/c/Users/vlad_/.codex/skills/*` | only Codex install surface | Keep one canonical wrapper per capability plus thin aliases. |
| Root repository skill packages | `.github/skills/*` | non-Codex runtime/distribution surface | Keep as generated GitHub/Copilot-native adapters or root-owned non-Codex skills, with provenance. |
| Arcanum same-checkout facades | `arcanum/.agents/skills/*` | local discovery facade | Prefer symlink or source handle, not copied skill bodies. |
| DomainSpec local facades | `implementation/domainspec/.agents/skills/*` | submodule-local surface | Do not parent-edit except through a DomainSpec-owned task. |
| Command files | `.codex/commands/*`, `.arcanum/runtimes/codex/commands/*` | legacy compatibility | Delete or avoid unless a runtime requirement is explicitly documented. |

## Alias Rules

Aliases are allowed only when they are thin wrappers.

A valid alias skill:

- has its own `name` for discovery,
- names the canonical target skill in `origin`,
- tells the runtime to read the canonical `SKILL.md`,
- does not copy the canonical process, contracts, examples, or templates,
- does not point to a command file as the primary behavior source.

A valid generated native package:

- is shaped for the target runtime, not for another runtime's convenience,
- records canonical source and generator provenance,
- may copy enough instruction text to work natively in that runtime,
- is regenerated from canonical source rather than manually evolved,
- records `alias_of` when the package is an alternate invocation name.

Current accepted aliases:

| Alias | Canonical skill | Reason |
| --- | --- | --- |
| `/mnt/c/Users/vlad_/.codex/skills/arcanum-invoke` | `/mnt/c/Users/vlad_/.codex/skills/invoke` | prefixed Arcanum discovery name |
| `/mnt/c/Users/vlad_/.codex/skills/refine` | `/mnt/c/Users/vlad_/.codex/skills/arcanum-refine` | short operator name |

Future aliases should be added to this table before installation.

## Cleanup Gates

Before deleting or rewriting any non-personal skill surface, classify it as one of:

- `canonical-source`
- `personal-codex-install`
- `thin-alias`
- `non-codex-runtime-adapter`
- `generated-native-runtime-package`
- `same-checkout-facade`
- `submodule-owned`
- `generated-install`
- `cleanup-candidate`

Do not mutate:

- machine-global Codex home from a repository-only task without naming it explicitly,
- `implementation/domainspec/*` surfaces from the parent repo unless the task is DomainSpec-owned,
- generated runtime adapters that are needed by a runtime until their replacement native package path is verified.

## Current Inventory Summary

As of this pass:

- Personal Codex skill surface: 34 direct `SKILL.md` files.
- Root `.github/skills`: 145 `SKILL.md` files; not treated as the Codex install surface.
- DomainSpec `.agents/skills`: 115 `SKILL.md` files; submodule-local and not parent-edited in this task.
- Root Codex command files: removed in the prior skills-first pass.
- Personal duplicate normalized now: `refine` is a thin alias to `arcanum-refine`.

## Invoke Result

- Mode: design
- Target: one alias-backed Codex skill surface for DomainSpec Core, Arcanum, and DomainSpec
- Status: flag
- Canonical sources used: local skill scans, `ops/SKILLS-FIRST-RUNTIME-POLICY.md`, `ops/REPOSITORY-ORGANIZATION-DESIGN.md`
- Artifacts produced or updated: `ops/CODEX-SKILL-SURFACE-POLICY.md`
- Decisions: personal Codex home is the Codex install surface for this operator; runtime-native generated packages are valid for Claude/Copilot/GitHub surfaces; aliases are thin wrappers or generated native alias packages; repository-local skill folders are adapters/facades/source-owned, not independent canonical copies
- Gaps: root `.github/skills` and DomainSpec `.agents/skills` still need provenance and owner classification before deletion or conversion
- Validation: `tools/audit_codex_skill_surface.sh` reports the personal aliases and remaining non-Codex surfaces
- Next route: task-session
