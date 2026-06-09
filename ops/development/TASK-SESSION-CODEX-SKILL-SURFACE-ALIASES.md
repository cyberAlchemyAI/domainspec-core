# Task Session: Codex Skill Surface Aliases

Date: 2026-05-29
Task: make Codex-facing DomainSpec Core, Arcanum, and DomainSpec skills use one personal skill surface with aliases instead of copied skills in every location.
Result: FLAG

## Context Pack

Sources:

- User directive on 2026-05-29: "only one skill surface, that uses aliases"
- `/mnt/c/Users/vlad_/.codex/skills`
- `ops/SKILLS-FIRST-RUNTIME-POLICY.md`
- `ops/REPOSITORY-ORGANIZATION-DESIGN.md`
- `.github/skills/README.md`
- `arcanum/.agents/skills`
- `implementation/domainspec/.agents/skills`

Controlling constraints:

- Codex-facing behavior should live in one personal skill surface.
- Aliases should be thin wrappers, not copied skill bodies.
- Root `.github/skills` is not the Codex install surface; classify before deleting because it may serve GitHub Copilot or distribution.
- `implementation/domainspec/.agents/skills` is submodule-local; do not parent-edit from this task.
- Root command files were already removed in the prior skills-first pass.

## Decision Pack

Decision: which surface is the Codex install surface?

Selected option: `/mnt/c/Users/vlad_/.codex/skills`.

Rationale: it is the machine-global Codex skill directory currently used by this session and already contains Arcanum aliases such as `arcanum-invoke`.

Decision: how to handle duplicate personal names.

Selected option: keep both discoverable names only when one is a thin alias.

Rationale: this preserves operator ergonomics while preventing divergent skill bodies.

## Work Performed

- Added `ops/CODEX-SKILL-SURFACE-POLICY.md`.
- Added `tools/audit_codex_skill_surface.sh`.
- Replaced `/mnt/c/Users/vlad_/.codex/skills/refine/SKILL.md` with a thin alias to `/mnt/c/Users/vlad_/.codex/skills/arcanum-refine/SKILL.md`.

## Validation

Command:

```bash
tools/audit_codex_skill_surface.sh
```

Observed result:

```text
personal_codex_skills=34
root_github_skills=145
arcanum_agent_facades=25
domainspec_agent_skills=103
root_codex_command_files=0

personal_alias_candidates:
arcanum-invoke
refine

personal_arcanum_short_name_collisions:
invoke
refine
```

Interpretation:

- Root command files remain absent.
- Personal `refine` is now an alias instead of a stale full copy.
- `invoke`/`arcanum-invoke` and `refine`/`arcanum-refine` are intentional alias pairs.
- Root `.github/skills` and DomainSpec `.agents/skills` remain as non-Codex surfaces requiring classification before further cleanup.

## Follow-Up

- Classify root `.github/skills` into root-owned skills, generated adapters, and cleanup candidates.
- Create or update an alias manifest if more short names are desired.
- Move any future Codex installs into `/mnt/c/Users/vlad_/.codex/skills` only.
- Handle DomainSpec `.agents/skills` through a DomainSpec-owned task rather than parent-repo cleanup.

## Refine Result

- Target: Codex skill surface aliases across DomainSpec Core, Arcanum, and DomainSpec
- Status: flag
- Preset: compact
- Research: no-research
- Run manifest: `ops/development/TASK-SESSION-CODEX-SKILL-SURFACE-ALIASES.md`
- Evidence index: this task report and `tools/audit_codex_skill_surface.sh`
- Seed proposal: one personal Codex skill surface, thin aliases for alternate names, classify repository-local skill folders before deletion
- Dispatch route: local governed task-session instead of command-backed refine, because root command files were intentionally removed
- Runtime handoff: none
- Stage evidence: local scan, policy update, alias normalization, audit script
- Final synthesis: the Codex-facing surface now has an explicit single-surface policy and one stale personal duplicate was converted to an alias
- Recommended next routes: task-session for root `.github/skills` classification; DomainSpec-owned task for `implementation/domainspec/.agents/skills`

## Invoke Result

- Mode: design
- Target: alias-backed single Codex skill surface
- Status: flag
- Canonical sources used: `/mnt/c/Users/vlad_/.codex/skills`, `ops/SKILLS-FIRST-RUNTIME-POLICY.md`, `ops/REPOSITORY-ORGANIZATION-DESIGN.md`
- Artifacts produced or updated: `ops/CODEX-SKILL-SURFACE-POLICY.md`, `tools/audit_codex_skill_surface.sh`, this task report
- Decisions: personal Codex home is the Codex install surface; aliases are thin wrappers; repository-local folders are non-Codex until classified otherwise
- Gaps: root `.github/skills` and DomainSpec `.agents/skills` still contain many skill packages and need separate classification
- Validation: audit script passed and reported remaining surfaces
- Next route: task-session

## Task Session Result

- Task: Codex skill surface aliases
- Result: FLAG
- Decisions: 2 resolved; personal Codex home selected, aliases must be thin wrappers
- Context pack: 7 source groups and 5 controlling constraints
- Handoff pack: none
- Strict coverage: n/a
- Fallback search: named gaps only
- Runtime: local
- Adapter: none
- Gate verdict: safe to normalize personal `refine`; not safe to delete root or DomainSpec skill folders without classification
- Files updated: `ops/CODEX-SKILL-SURFACE-POLICY.md`, `tools/audit_codex_skill_surface.sh`, `/mnt/c/Users/vlad_/.codex/skills/refine/SKILL.md`, this task report
- Validation: `tools/audit_codex_skill_surface.sh` passed
- Experiment harness: not_applicable
- Synchronized records: `ops/CODEX-SKILL-SURFACE-POLICY.md`, `ops/development/TASK-SESSION-CODEX-SKILL-SURFACE-ALIASES.md`
- Follow-up: classify `.github/skills`; run DomainSpec-owned cleanup for `implementation/domainspec/.agents/skills`
