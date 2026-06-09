# Task Session: Root Arcanum Evidence And State Classification

Date: 2026-06-01
Task: `TASK-SURFACE-006`
SWU: `SWU-SURFACE-008`
Result: PASS

## Objective

Separate durable `.arcanum` observability config and structure from generated evidence and reflection state.

## Decision Applied

Accepted option from `docs/decisions/surface-cleanup-blocker-decisions.md`: ignore generated observability ledgers by default and promote selectively.

## Work Performed

- Added root ignore rules:
  - `.arcanum/observability/**/*.jsonl`,
  - `.arcanum/observability/reflection-state.json`.
- Untracked generated observability state while preserving the local files:
  - `.arcanum/observability/by-sigil/experiment-harness.jsonl`,
  - `.arcanum/observability/signals/sigil-invocations.jsonl`,
  - `.arcanum/observability/reflection-state.json`.
- Updated `ops/ARCANUM-STATE-CLASSIFICATION.md` so generated ledgers and reflection state are local by default.

## Validation

Commands/checks:

```bash
git ls-files .arcanum/observability | rg '\.(jsonl|json)$' | rg -v 'config\.json$' | wc -l
git check-ignore -v .arcanum/observability/by-sigil/experiment-harness.jsonl
git check-ignore -v .arcanum/observability/signals/sigil-invocations.jsonl
git check-ignore -v .arcanum/observability/reflection-state.json
test -f .arcanum/observability/by-sigil/experiment-harness.jsonl
test -f .arcanum/observability/signals/sigil-invocations.jsonl
test -f .arcanum/observability/reflection-state.json
```

Validation result:

- tracked generated observability file count is now `0`,
- ignore rules apply to future generated JSONL ledgers and reflection state,
- local generated evidence files remain on disk,
- durable observability config and structure markers remain tracked.

## Follow-Up

`TASK-SURFACE-007` is next: protect submodule, nested Arcanum, project, and validation surfaces with explicit owner boundaries before any broader cleanup.
