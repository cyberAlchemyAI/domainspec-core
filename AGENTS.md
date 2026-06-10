# Agent Instructions

Operating rules for any agent working in this repository — the **private** `domainspec-core` umbrella. Claude-specific guidance lives in `CLAUDE.md`.

## Submodule discipline (enforced)

This repo composes submodules — public **`arcanum`**; private **`implementation/domainspec`**, **`validation/poker-team`** — under this private parent. Full rules: `SUBMODULE-DISCIPLINE.md`.

- **Submodule first, parent last.** Commit AND push inside the submodule before committing/pushing the parent gitlink. Never reference an unpushed submodule commit. Verify with `make bump-check` before pushing the parent.
- **Branch tracking, no detached HEAD.** Submodules track `main` (pinned in `.gitmodules`); advance them with `make sync`. Fix a detached submodule with `git -C <path> checkout main`. "Vanished" files almost always mean a detached HEAD or a `git submodule update` that snapped back to the recorded pointer — not data loss.
- **Open/private boundary.** `arcanum` is public — never commit private content into it. Public + private compose only in this private parent.
- **Setup/diagnose:** `make bootstrap` after clone; `make doctor` (detached HEADs / dirty submodules / orphaned gitlinks); `make config` sets the enforcing git config (`push.recurseSubmodules=check`).

## Arcanum boundaries

See `CLAUDE.md`: `dispatch-spec` validates route shape; `invoke` authors define/design/plan/handoff/refresh; `task-session` executes one bounded task/SWU; native skills and subagents are preferred over nested model-backed CLI execution.
