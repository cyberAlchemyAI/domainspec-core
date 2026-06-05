# Task Session: Legacy Command Adapter Removal

Date: 2026-06-01
Task: `TASK-SURFACE-005`
SWU: `SWU-SURFACE-007`
Result: PASS

## Objective

Complete the skills-first cleanup for tracked root command snapshots.

## Work Performed

- Staged deletion of the already-missing root command files:
  - 9 files under `.codex/commands/`,
  - 7 files under `.arcanum/runtimes/codex/commands/`.
- Updated active Arcanum source docs that still described `.codex/commands` as the normal installed runtime surface:
  - `arcanum/arcana/sigil-runtime-installer/SKILL.md`,
  - `arcanum/arcana/sigil-runtime-installer/README.md`,
  - `arcanum/arcana/sigil-runtime-installer/templates/target-selection.md`,
  - `arcanum/arcana/invoke-example-runner/SKILL.md`,
  - `arcanum/arcana/distill/README.md`,
  - `arcanum/spells/arcanum-bootstrap/README.md`,
  - `arcanum/spells/observed-invocation-loop/README.md`.

## Validation

Commands/checks:

```bash
git ls-files .codex/commands .arcanum/runtimes/codex/commands | wc -l
find .codex/commands .arcanum/runtimes/codex/commands -maxdepth 1 -type f -print 2>/dev/null | wc -l
rg -n 'Arcanum now treats `\.codex/commands|Codex commands are the installed runtime surface|normal execution requires commands|`\.codex/commands/` as the installed runtime|Command surface: `\.codex/commands/`|User chooses command runtime: Codex|--runtime codex|codex-exec \| dry-run|Use `\.codex/commands/arcanum-spell-invoke.md` as the command bridge|Runtime commands own' arcanum/arcana arcanum/spells ops docs --glob '!**/development/**'
bash -n arcanum/tools/bootstrap_arcanum.sh
```

Validation result:

- tracked root command file count is now `0`,
- root command files on disk are `0`,
- stale active-source command-default wording is gone, except the task-plan note that required this cleanup,
- bootstrap shell syntax still passes.

## Follow-Up

`TASK-SURFACE-006` should classify generated observability ledgers and reflection state, then either keep durable evidence deliberately or untrack generated runtime ledgers by policy.
