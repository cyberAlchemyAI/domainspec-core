# Task Session: Duplicate Skill Pruning

Date: 2026-05-29
Task: plan duplicate skill cleanup so only the most recent full skill body remains.
Result: FLAG

## Context Pack

Sources:

- `ops/CODEX-SKILL-SURFACE-POLICY.md`
- `ops/development/TASK-SESSION-CODEX-SKILL-SURFACE-ALIASES.md`
- `tools/audit_codex_skill_surface.sh`
- `/mnt/c/Users/vlad_/.codex/skills`
- `.github/skills`
- `arcanum/.agents/skills`
- `implementation/domainspec/.agents/skills`

Constraints:

- Keep one Codex-facing skill surface.
- Preserve thin aliases when they are intentional aliases.
- Keep the most recent full skill body when two full bodies duplicate the same capability.
- Do not delete submodule-local or cross-runtime skill packages without owner classification.
- Do not restore command surfaces.

## Decision Pack

Decision: what counts as a duplicate?

Selected option: a second full skill body for the same normalized capability.

Reason: aliases are allowed by policy and should not be deleted merely because they share a capability name.

Decision: how to pick the keeper.

Selected option: newest full skill body by mtime, unless ownership policy overrides it.

Reason: this matches the user request while preserving owner boundaries.

## Work Performed

- Created `ops/DUPLICATE-SKILL-PRUNING-PLAN.md`.
- Reused the existing audit script and duplicate scans to identify exact duplicate hashes and normalized collision groups.
- Performed no additional deletions in this task because the remaining exact duplicates cross owner boundaries or live inside the DomainSpec submodule.

## Validation Evidence

Audit command:

```bash
tools/audit_codex_skill_surface.sh
```

Current result:

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

Exact duplicate hash scan found:

- `implementation/domainspec/.agents/skills/gitnexus copy/*` duplicates `implementation/domainspec/.agents/skills/gitnexus/*`.
- `.github/skills/domainspec-feature-glossary/SKILL.md` duplicates `implementation/domainspec/.agents/skills/domainspec-feature-glossary/SKILL.md`.
- `.github/skills/domainspec-definitions-governance/SKILL.md` duplicates `implementation/domainspec/.agents/skills/domainspec-definitions-governance/SKILL.md`.

## Gate Verdict

FLAG.

The duplicate-pruning plan is ready and the personal duplicate layer was already normalized, but the remaining concrete deletions need owner-boundary approval or a DomainSpec-owned task.

## Task Session Result

- Task: duplicate skill pruning
- Result: FLAG
- Decisions: 2 resolved; duplicate means duplicate full body, keeper is newest full body unless ownership overrides
- Context pack: 7 source groups and 5 constraints
- Handoff pack: none
- Strict coverage: n/a
- Fallback search: named gaps only
- Runtime: local
- Adapter: none
- Gate verdict: safe to plan; unsafe to delete remaining exact duplicates from parent task
- Files updated: `ops/DUPLICATE-SKILL-PRUNING-PLAN.md`, this report
- Validation: `tools/audit_codex_skill_surface.sh`; exact duplicate hash scan; normalized collision scan
- Experiment harness: not_applicable
- Synchronized records: `ops/DUPLICATE-SKILL-PRUNING-PLAN.md`
- Follow-up: TASK-DUP-002 root `.github/skills` classification, TASK-DUP-003 DomainSpec-owned `gitnexus copy` deletion, TASK-DUP-004 root adapter pruning
