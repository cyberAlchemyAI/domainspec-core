# Claude Code Instructions

Use the project Arcanum skill at `.claude/skills/orchestrate/SKILL.md` for Arcanum work.

Use `.claude/agents/arcanum-stage-worker.md` for bounded sidecar stages when subagent delegation is helpful.

Preserve Arcanum boundaries:

- `dispatch-spec` validates route shape.
- `invoke` authors define/design/plan/handoff/refresh artifacts.
- `task-session` executes one bounded task or SWU.
- `tools/arcanum` is a deterministic resolver, validator, handoff, and legacy adapter surface.
- Native skills and subagents are preferred over nested model-backed CLI execution.

## Submodule discipline (enforced)

This repo is a **private** umbrella of submodules — public: `arcanum`; private: this parent, `implementation/domainspec`, `validation/poker-team`. Full rules: `SUBMODULE-DISCIPLINE.md`. Every agent must follow these hard rules:

- **Submodule first, parent last.** Commit AND push inside a submodule before bumping/committing the parent gitlink. Never commit a parent pointer to an unpushed submodule commit. Run `make bump-check` before pushing the parent.
- **Branch tracking, no detached HEAD.** Submodules track `main` (pinned in `.gitmodules`); advance with `make sync`. If a submodule is detached, `git -C <path> checkout main`.
- **Open/private boundary.** Never put private content into `arcanum` (public). Public + private compose only here, in the private parent.
- **Setup/diagnose:** `make bootstrap` after clone; `make doctor` to check for detached HEADs, dirty submodules, and orphaned gitlinks; `make config` sets the enforcing git config (`push.recurseSubmodules=check`).
