# Task Session: Skills-First Runtime Layer

Date: 2026-05-29
Task: Fix the skills and command layers first; keep skills, not commands.
Result: PASS

## Context Pack

Sources:

- User directive on 2026-05-29: "we should fix the skills and command layers first, we dont need to have commands, only skills"
- `ops/REPOSITORY-ORGANIZATION-DESIGN.md`
- `ops/development/refinement-runs/2026-05-27-zone-taxonomy/RUNTIME-SURFACE-INVOKE.md`
- `ops/development/refinement-runs/2026-05-27-zone-taxonomy/SYMLINK-STRATEGY-REFINE.md`
- `.github/skills/README.md`
- current root `.codex/commands`, `.arcanum/runtimes/codex/commands`, and `.github/skills` scan

Controlling constraints:

- Do not blur canonical source, install surfaces, generated state, and local state.
- Keep Arcanum behavior canonical under Arcanum source and expose it through skill surfaces.
- Avoid duplicate command and skill wrappers when the skill layer is sufficient.
- Do not mutate machine-global Codex home from this repository cleanup task.
- Do not parent-edit submodule-owned runtime surfaces.

## Decision Pack

Decision: what to do with root command files.

Selected option: remove tracked root `.codex/commands/*.md` and `.arcanum/runtimes/codex/commands/*.md`, then document a skills-first policy.

Rationale: the root repository already has `.github/skills/arcanum-*` skill wrappers, and the command files were adapter wrappers rather than canonical behavior.

Rejected option: keep commands as generated snapshots.

Reason: this keeps two discoverable surfaces for the same behavior and preserves the duplication problem the cleanup pass is supposed to remove.

## Gate Verdict

PASS.

Equivalent skill surfaces are present under `.github/skills/arcanum-*`. The deleted root command files were command bridges or thin aliases, not canonical Arcanum source. Machine-global Codex skills and submodule-local command files were left untouched.

## Files Updated

- Deleted root command bridges under `.codex/commands/*.md`.
- Deleted root Codex command adapters under `.arcanum/runtimes/codex/commands/*.md`.
- Added `ops/SKILLS-FIRST-RUNTIME-POLICY.md`.
- Updated `ops/REPOSITORY-ORGANIZATION-DESIGN.md`.
- Updated `.github/skills/README.md`.

## Validation

Checks performed:

- `find .codex/commands .arcanum/runtimes/codex/commands -maxdepth 1 -type f -name '*.md' -print 2>/dev/null || true`: no remaining root command files in the working tree.
- `find .github/skills -maxdepth 2 -name SKILL.md | rg '/arcanum-'`: Arcanum skill wrappers remain discoverable.
- `rg -n "\.codex/commands|command-adapter|commands are|skills-first|Skills-First" ops/REPOSITORY-ORGANIZATION-DESIGN.md ops/SKILLS-FIRST-RUNTIME-POLICY.md .github/skills/README.md`: docs now describe commands as legacy compatibility adapters, not the default layer.

Note: deleted command files still appear in `git ls-files` until the deletion is staged and committed.

## Follow-Up

- Adjust Arcanum bootstrap/runtime installer scripts so they do not regenerate root command files unless a compatibility flag is explicitly requested.
- Create the fuller runtime-surface inventory after the skills-first policy is accepted.
- Continue cleanup with `sigils-library/` preservation diff.

## Task Session Result

- Task: skills-first runtime layer
- Result: PASS
- Decisions: 1 resolved; skills are default, commands are legacy compatibility adapters only
- Context pack: 6 source groups and 5 controlling constraints
- Handoff pack: none
- Strict coverage: n/a
- Fallback search: named gaps only
- Runtime: local
- Adapter: none
- Gate verdict: root command files are removable because skill surfaces exist and command files are non-canonical bridges
- Files updated: `.codex/commands/*.md`, `.arcanum/runtimes/codex/commands/*.md`, `ops/SKILLS-FIRST-RUNTIME-POLICY.md`, `ops/REPOSITORY-ORGANIZATION-DESIGN.md`, `.github/skills/README.md`
- Validation: pass for working-tree cleanup and skill-wrapper discovery; staging/commit still needed to remove tracked command files from the index
- Experiment harness: not_applicable
- Synchronized records: `ops/REPOSITORY-ORGANIZATION-DESIGN.md`, `ops/SKILLS-FIRST-RUNTIME-POLICY.md`, `.github/skills/README.md`
- Follow-up: installer/bootstrap adjustment, runtime-surface inventory, `sigils-library/` preservation diff
