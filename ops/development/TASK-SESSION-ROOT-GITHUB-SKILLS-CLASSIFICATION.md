# Task Session: Root GitHub Skills Classification

Date: 2026-05-29
Task: TASK-DUP-002 - classify root `.github/skills` duplicates.
Result: FLAG

## Context Pack

Sources:

- `ops/DUPLICATE-SKILL-PRUNING-PLAN.md`
- `ops/CODEX-SKILL-SURFACE-POLICY.md`
- `tools/audit_codex_skill_surface.sh`
- `tools/classify_root_github_skills.sh`
- `.github/skills`
- `/mnt/c/Users/vlad_/.codex/skills`
- `arcanum/.agents/skills`
- `implementation/domainspec/.agents/skills`

Controlling constraints:

- Keep one Codex-facing skill surface.
- Root `.github/skills` is not the personal Codex install surface.
- Preserve root skills that are real GitHub/distribution adapters.
- Gate deletion where the keeper is submodule-owned or runtime role is not yet proven.
- Do not restore `.codex/commands`.

## Decision Pack

Decision: classify before deletion.

Selected option: generate an auditable classification table and perform no deletion in this task.

Rationale: many root entries are older than DomainSpec `.agents` entries, but root `.github/skills` may still be a distribution surface. Deleting without runtime confirmation could break GitHub/Copilot discovery.

Decision: action labels.

Selected labels:

- `keep`: root-owned or distribution adapter.
- `gate-delete`: cleanup candidate, but deletion needs owner/runtime confirmation.
- `keep-root-until-runtime-confirmed`: overlaps personal Codex skill, but may be non-Codex runtime adapter.

## Work Performed

- Added `tools/classify_root_github_skills.sh`.
- Generated `ops/ROOT-GITHUB-SKILLS-CLASSIFICATION.md`.
- Updated `ops/DUPLICATE-SKILL-PRUNING-PLAN.md` with TASK-DUP-002 result.

## Classification Summary

| Class | Count | Meaning |
| --- | ---: | --- |
| `distribution-adapter` | 33 | Arcanum root GitHub skill adapter; keep for now. |
| `root-owned` | 15 | Unique root skill or root-owned package; keep. |
| `personal-codex-duplicate` | 3 | Personal Codex skill exists; keep root until runtime role is confirmed. |
| `domainspec-duplicate` | 94 | Newer DomainSpec-owned skill exists; gate-delete candidate. |

| Action | Count | Meaning |
| --- | ---: | --- |
| `keep` | 48 | Keep in root. |
| `keep-root-until-runtime-confirmed` | 3 | Do not delete until root runtime role is confirmed. |
| `gate-delete` | 94 | Candidate for deletion after owner/runtime confirmation. |

## Validation

Commands:

```bash
tools/classify_root_github_skills.sh
tools/audit_codex_skill_surface.sh
```

Results:

- Classification table generated at `ops/ROOT-GITHUB-SKILLS-CLASSIFICATION.md`.
- Root Codex command files remain absent: `root_codex_command_files=0`.
- Personal aliases remain present: `arcanum-invoke`, `refine`.
- No root skill files were deleted.

## Gate Verdict

FLAG.

The classification is complete, but deletion is intentionally blocked until one of these follow-up gates is satisfied:

- Confirm root `.github/skills/domainspec-*` and `.github/skills/gsd-*` are not required as root GitHub/Copilot distribution adapters.
- Confirm the three personal-overlap root skills are not needed outside personal Codex.
- Run a DomainSpec-owned task for submodule-local cleanup.

## Task Session Result

- Task: TASK-DUP-002 root `.github/skills` classification
- Result: FLAG
- Decisions: 2 resolved; classify before deletion, use keep/gate-delete/keep-root-until-runtime-confirmed actions
- Context pack: 8 source groups and 5 constraints
- Handoff pack: none
- Strict coverage: n/a
- Fallback search: named gaps only
- Runtime: local
- Adapter: none
- Gate verdict: classification complete; deletion blocked by runtime/owner confirmation
- Files updated: `tools/classify_root_github_skills.sh`, `ops/ROOT-GITHUB-SKILLS-CLASSIFICATION.md`, `ops/DUPLICATE-SKILL-PRUNING-PLAN.md`, this report
- Validation: `tools/classify_root_github_skills.sh`; `tools/audit_codex_skill_surface.sh`
- Experiment harness: not_applicable
- Synchronized records: `ops/DUPLICATE-SKILL-PRUNING-PLAN.md`
- Follow-up: decide whether to delete 94 `gate-delete` root skills, then run TASK-DUP-004 root adapter pruning
