# DomainSpec Owner Handoff: Claude/Codex Skill And Agent Surface

Date: 2026-06-01
Source task: `SWU-AGENTARCH-009`
Status: handoff; no implementation-owned files edited

## Purpose

This handoff records the DomainSpec-owned follow-up needed after the root
Claude/Codex canonical map and drift report.

Root scope produced:

- `ops/development/skill-agent-canonical-map.json`
- `tools/check_skill_agent_surface_drift.py`
- `ops/development/CLAUDE-CODEX-SURFACE-DRIFT-REPORT.md`
- `ops/development/GITHUB-SURFACE-DELETION-CANDIDATES.md`

## DomainSpec-Owned Surfaces

The map treats these surfaces as DomainSpec-owned:

- `implementation/domainspec/copilot/skills/*`
- `implementation/domainspec/copilot/agents/*`
- `implementation/domainspec/.agents/skills/**/*`
- `implementation/domainspec/.claude/agents/*`
- `implementation/domainspec/.codex/agents/*`
- `implementation/domainspec/.github/agents/*`

Root task-session did not edit any of those paths.

## Current Findings

From `ops/development/skill-agent-canonical-map.json` and the generated reports:

- DomainSpec map records: 69.
- GSD map records under implementation ownership: 75.
- Claude readers present across the full map: 50.
- Codex readers present across the full map: 43.
- Implementation `.github/agents` deletion candidates: 36, all marked `owner-scoped`.
- Root GitHub candidates marked `safe-delete`: 182 across all owner families, pending approval and usage review.
- Root GitHub candidates needing replacement or active-use review: 28.

## Recommended DomainSpec Task

Create a DomainSpec-owned task to reconcile the implementation-local source and
runtime surfaces:

1. Confirm whether `implementation/domainspec/copilot/skills/*` remains the canonical source for DomainSpec skills.
2. Confirm whether `implementation/domainspec/copilot/agents/*` remains the canonical source for DomainSpec agents.
3. For DomainSpec agents missing either Claude or Codex readers, decide whether to create the missing reader or mark the logical agent retired.
4. For GSD agents and skills, decide whether the implementation-local `.agents` and `.claude` surfaces are canonical source, runtime adapter, or generated output.
5. Delete or deprecate `implementation/domainspec/.github/agents/*` only inside a DomainSpec-owned cleanup task.
6. Update any local policies that still describe GitHub as an active target runtime.

## Root Expectations

Root-level automation now expects:

- Claude and Codex are the only target runtime surfaces.
- GitHub is a deletion/deprecation lane, not a preserved runtime target.
- DomainSpec-owned files must not be rewritten by parent cleanup tasks.
- Root reports may classify and recommend, but implementation-owned mutation needs a DomainSpec task.

## Suggested Validation

After DomainSpec-owned reconciliation, rerun:

```bash
python3 tools/check_skill_agent_surface_drift.py --map ops/development/skill-agent-canonical-map.json --format json
python3 tools/check_skill_agent_surface_drift.py --map ops/development/skill-agent-canonical-map.json --format markdown --output ops/development/CLAUDE-CODEX-SURFACE-DRIFT-REPORT.md --deletion-output ops/development/GITHUB-SURFACE-DELETION-CANDIDATES.md
```

Expected improvement:

- Fewer `missing` Claude/Codex agent readers.
- Fewer `blocked-active-use` GitHub candidates.
- Clearer source-vs-reader separation for GSD.
