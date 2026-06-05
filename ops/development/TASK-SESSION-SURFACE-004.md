# Task Session: GitHub/Copilot Runtime Cache Cleanup

Date: 2026-06-01
Task: `TASK-SURFACE-004`
SWU: `SWU-SURFACE-006`
Result: PASS

## Objective

Apply the accepted `.arcanum/runtimes/github-copilot` policy after root `.github/skills/arcanum-*` packages became self-provenanced.

## Decision Applied

Accepted option: untrack and regenerate `.arcanum/runtimes/github-copilot` on demand.

The cache remains available locally, but it is no longer a tracked source or a required active runtime dependency.

## Work Performed

- Added `.arcanum/runtimes/github-copilot/` to root `.gitignore`.
- Updated `ops/ARCANUM-STATE-CLASSIFICATION.md` to classify this path as a generated runtime package cache.
- Ran:

```bash
git rm -r --cached .arcanum/runtimes/github-copilot
```

## Validation

Commands/checks:

```bash
git ls-files .arcanum/runtimes/github-copilot | wc -l
find .arcanum/runtimes/github-copilot -type f | wc -l
git check-ignore -v .arcanum/runtimes/github-copilot/skills/arcanum-orchestrate/SKILL.md
rg -n "\\.arcanum/runtimes/github-copilot" .github --glob 'SKILL.md'
```

Validation result:

- tracked cache file count is now `0`,
- local cache files still exist on disk: `83`,
- ignore rule applies to regenerated cache files,
- no active `.github/**/SKILL.md` file references the cache.

## Follow-Up

`TASK-SURFACE-005` is next: finish legacy command adapter removal. The current worktree already has command adapter deletions staged by prior work; the next pass should validate docs and tracked file state before treating those deletions as complete.
