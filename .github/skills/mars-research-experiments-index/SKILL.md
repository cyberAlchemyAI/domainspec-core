---
name: mars-research-experiments-index
description: "Maintain experiment bundle README pattern, auto-refresh experiments dashboard, and regenerate OPEN-DECISIONS rollup from current artifacts."
argument-hint: "[--refresh|--check] [--project domainspec]"
agent: mars-research-scientist
allowed-tools: Read, Write, Bash, Glob, Grep
---

<objective>
Keep experiment documentation navigable and current by enforcing a consistent bundle README pattern and regenerating aggregate indexes from actual bundle state.

This skill exists to prevent drift between:
- per-bundle evidence (protocol/data/results),
- program status dashboard (`experiments/README.md`), and
- unresolved adjudication inventory (`experiments/OPEN-DECISIONS.md`).
</objective>

<context>
Primary artifacts:
- `research/projects/domainspec/experiments/EXPERIMENTS.md`
- `research/projects/domainspec/experiments/README.md`
- `research/projects/domainspec/experiments/OPEN-DECISIONS.md`
- `research/projects/domainspec/experiments/E*-*/README.md`
- `tools/update_experiments_index.sh`

Bundle contract references:
- `research/projects/domainspec/experiments/E*-*/context.md`
- `research/projects/domainspec/experiments/E*-*/protocol.md`
- `research/projects/domainspec/experiments/E*-*/sources.md`
- `research/projects/domainspec/experiments/E*-*/data/`
- `research/projects/domainspec/experiments/E*-*/results/`
</context>

<process>
1. Validate bundle README coverage.
   - Ensure every `E*-*` bundle has `README.md`.
   - If missing, create one using the standard section pattern:
     - Status Snapshot
     - Read Order
     - Bundle Chart
     - Task Completeness
     - Open Decisions and Adjudications
     - Navigation

2. Validate root README automation markers.
   - Ensure `experiments/README.md` contains:
     - `<!-- AUTO-DASHBOARD:START -->`
     - `<!-- AUTO-DASHBOARD:END -->`

3. Regenerate aggregates.
   - Run:
     - `./tools/update_experiments_index.sh`
   - This refreshes:
     - status chart and dashboard table in `experiments/README.md`
     - unresolved decision rollup in `experiments/OPEN-DECISIONS.md`

4. Verify outputs.
   - Confirm each bundle appears in dashboard table.
   - Confirm latest evidence links resolve where results exist.
   - Confirm unresolved decision counts align with rollup table.

5. Report deltas.
   - Summarize files created/updated and unresolved-decision totals.
</process>

<quality-bar>
- No stale manual counts in root dashboard sections.
- Bundle README links must be relative and clickable.
- Open-decision rollup must include source file links and signal snippets.
- Script execution should be idempotent: re-running without artifact changes produces no meaningful diff.
</quality-bar>

<output-contract>
Return a compact summary:

```markdown
## Experiments Index Refresh
- Bundles scanned: <n>
- Bundle READMEs added: <n>
- Dashboard updated: yes/no
- Open decisions updated: yes/no
- Experiments with unresolved signals: <n>
- Unresolved items: <n>

### Files Changed
- <path>
- <path>
```
</output-contract>
