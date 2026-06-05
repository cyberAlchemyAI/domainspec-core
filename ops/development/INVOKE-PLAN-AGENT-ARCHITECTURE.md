# Invoke Plan: Agent Architecture Canonicalization

Date: 2026-06-01
Mode: `invoke plan`
Input design: `ops/development/INVOKE-DESIGN-AGENT-ARCHITECTURE.md`
Input refine: `ops/development/REFINE-SYNTHESIS-AGENT-ARCHITECTURE.md`
Status: pass with implementation approval gate
Complexity: medium
Output mode: split-ready work-pack plan

## Objective

Implement the first safe slice of the refined agent architecture: a Claude/Codex canonical map, read-only parity checker, and GitHub deletion-candidate report.

## Delivery Boundary

In scope:

- Root-owned `ops/development/*` planning and evidence artifacts.
- Root-owned `tools/*` read-only Claude/Codex parity and deletion-candidate checker.
- Root-owned report artifacts produced by the checker.
- Owner-scoped handoff documents for DomainSpec and Lean formalization.
- Deletion plan for GitHub surfaces after approval.

Out of scope until separately approved:

- Editing `implementation/domainspec/*`.
- Editing `domainspec-lean-formalization/*`.
- Immediate deletion before the deletion-candidate report is reviewed.
- Editing root `.github/skills/*`, root `.github/agents/*`, or implementation `.github/agents/*` as preserved target surfaces.
- Mutating machine-global Codex home.
- Regenerating GSD or GitHub distribution packages.

## Implementation Layering

| Layer | Scope | Tasks | Promotion evidence |
| --- | --- | --- | --- |
| L0 | Claude/Codex canonical map and read-only parity report. | T1, T2 | Checker runs and emits report without mutation. |
| L1 | GitHub deletion-candidate classification. | T3 | Report distinguishes safe-delete, blocked-use, needs-replacement, and owner-scoped. |
| L2 | Owner handoffs and deletion gate. | T4, T5 | DomainSpec and Lean handoffs exist; GitHub deletion decision exists. |
| L3 | Approved deletion and reference cleanup. | T6 | GitHub surfaces removed only after approval and usage checks. |

## Work-Pack

### T1. Build Canonical Map Schema And Seed

Goal: Create `ops/development/skill-agent-canonical-map.json` focused on Claude/Codex active runtime surfaces.

Write scope:

- `ops/development/skill-agent-canonical-map.json`
- optional `ops/development/skill-agent-canonical-map.schema.yml`

Implementation detail:

- Read `domainspec-skill-agent-candidate-ledger.md` and `lean-formalization-skill-agent-candidate-ledger.md`.
- Create one map record per logical skill/agent.
- Include fields: `logical_id`, `artifact_kind`, `owner_family`, `canonical_path`, `canonical_status`, `claude_reader`, `codex_reader`, `shared_skill_facade`, `github_delete_candidate`, `blocked_owner`, `validation_notes`.
- Use conservative defaults:
  - DomainSpec skills -> `implementation/domainspec/copilot/skills` when present.
  - DomainSpec agents -> `implementation/domainspec/copilot/agents` when present.
  - Claude agents -> `implementation/domainspec/.claude/agents`.
  - Codex agents -> `implementation/domainspec/.codex/agents`.
  - GSD -> keep only if Claude/Codex reader exists or active use is proven.
  - Lean proof-domain -> Lean-owned canonical.
  - GitHub entries -> delete-candidate unless active use blocks deletion.

Validation:

- JSON parses.
- Every record has a logical id and canonical status.
- Every downstream path exists or is marked missing.

SWUs:

- SWU-AGENTARCH-001: Draft map schema and minimal map records.
- SWU-AGENTARCH-002: Populate map from current ledgers.
- SWU-AGENTARCH-003: Validate map completeness against ledger counts.

### T2. Add Read-Only Claude/Codex Parity Checker

Goal: Add `tools/check_skill_agent_surface_drift.py`.

Write scope:

- `tools/check_skill_agent_surface_drift.py`

Implementation detail:

- Accept `--map ops/development/skill-agent-canonical-map.json`.
- Accept `--format markdown|json`.
- Never write unless `--output <path>` is supplied.
- For each Claude/Codex reader, report:
  - `in-sync`
  - `runtime-rewrite`
  - `drift`
  - `orphan`
  - `blocked-owner`
  - `missing`
- For GitHub surfaces, report deletion status:
  - `safe-delete`
  - `blocked-active-use`
  - `needs-claude-replacement`
  - `needs-codex-replacement`
  - `owner-scoped`
- Do not normalize body text beyond frontmatter extraction at L0.

Validation:

- `python3 tools/check_skill_agent_surface_drift.py --map ops/development/skill-agent-canonical-map.json --format json`
- `python3 tools/check_skill_agent_surface_drift.py --map ops/development/skill-agent-canonical-map.json --format markdown --output ops/development/CLAUDE-CODEX-SURFACE-DRIFT-REPORT.md`

SWUs:

- SWU-AGENTARCH-004: Implement CLI and map loading.
- SWU-AGENTARCH-005: Implement Claude/Codex parity and GitHub deletion status checks.
- SWU-AGENTARCH-006: Implement Markdown and JSON output.

### T3. Produce Claude/Codex Drift And GitHub Deletion Reports

Goal: Produce `ops/development/CLAUDE-CODEX-SURFACE-DRIFT-REPORT.md` and `ops/development/GITHUB-SURFACE-DELETION-CANDIDATES.md`.

Write scope:

- `ops/development/CLAUDE-CODEX-SURFACE-DRIFT-REPORT.md`
- `ops/development/GITHUB-SURFACE-DELETION-CANDIDATES.md`

Implementation detail:

- Summarize counts by owner family, Claude reader status, and Codex reader status.
- List root `.github/skills`, root `.github/agents`, and implementation `.github/agents` as deletion candidates by default.
- For every GitHub candidate, record replacement evidence or blocker.
- List blocked owner paths for DomainSpec and Lean.

Validation:

- Report generated by checker, not handwritten.
- Deletion report includes no deletion actions marked complete.

SWUs:

- SWU-AGENTARCH-007: Generate first report.
- SWU-AGENTARCH-008: Verify report matches inventory counts.

### T4. Create DomainSpec Owner Handoff

Goal: Create `ops/development/DOMAINSPEC-OWNER-HANDOFF.md`.

Write scope:

- `ops/development/DOMAINSPEC-OWNER-HANDOFF.md`

Implementation detail:

- Name DomainSpec-owned surfaces and drift findings.
- Recommend a DomainSpec-owned task to reconcile `copilot`, `.agents`, `.claude`, and `.codex` surfaces, with `.github` classified only for deletion/deprecation.
- Include root expectations for generated readers.

Validation:

- Handoff does not instruct parent repo to edit child surfaces.

SWUs:

- SWU-AGENTARCH-009: Draft DomainSpec handoff.

### T5. Create Lean Formalization Owner Handoff

Goal: Create `ops/development/LEAN-FORMALIZATION-OWNER-HANDOFF.md`.

Write scope:

- `ops/development/LEAN-FORMALIZATION-OWNER-HANDOFF.md`

Implementation detail:

- Preserve proof mechanics and theorem governance as separate canonical candidate units.
- Mark `custom/*`, `gitnexus/*`, and `implement-filter` as residue requiring active-use proof.
- Preserve claim <= proof, precedent search, Lean build evidence, and mathlib PR constraints.

Validation:

- Handoff does not weaken Lean guardrails.

SWUs:

- SWU-AGENTARCH-010: Draft Lean handoff.

### T6. Delete Approved GitHub Surfaces

Goal: After approval, delete GitHub surfaces that are proven unnecessary for Claude/Codex.

Write scope:

- root `.github/skills/*`
- root `.github/agents/*`
- `implementation/domainspec/.github/agents/*`
- documentation/policy references that describe GitHub as an active target

Implementation detail:

- Use `GITHUB-SURFACE-DELETION-CANDIDATES.md` as the deletion source.
- Delete only rows marked `safe-delete`.
- Leave blocked rows untouched and record blockers.
- Update policies to say Claude and Codex are target runtimes; GitHub is deprecated or removed.

Validation:

- `git status --short` shows only intended GitHub deletions and policy/doc updates.
- No DomainSpec or Lean owner surfaces are edited except approved handoffs.
- Claude/Codex parity report still passes after deletion.

SWUs:

- SWU-AGENTARCH-011: Delete approved GitHub candidates and update references.

## Validation Strategy

Required checks before execution handoff can close:

```bash
python3 -m json.tool ops/development/skill-agent-canonical-map.json
python3 tools/check_skill_agent_surface_drift.py --map ops/development/skill-agent-canonical-map.json --format json
python3 tools/check_skill_agent_surface_drift.py --map ops/development/skill-agent-canonical-map.json --format markdown --output ops/development/CLAUDE-CODEX-SURFACE-DRIFT-REPORT.md
```

Review checks:

- No source edits under `implementation/domainspec`.
- No source edits under `domainspec-lean-formalization`.
- No GitHub deletions before `GITHUB-SURFACE-DELETION-CANDIDATES.md` is reviewed and approved.
- After approval, GitHub deletions match only `safe-delete` rows.
- Lean handoff preserves proof-domain guardrails.

## Execution Handoff

Recommended next route: `task-session`.

Suggested first executable SWU: `SWU-AGENTARCH-001`.

Reason: it creates the Claude/Codex canonical map schema without mutating any runtime surfaces. After T1 and T2 pass, GitHub deletion can be evidence-backed instead of vibes-backed, which is better for everyone’s blood pressure.

## Invoke Result

- Mode: plan
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `spells/invoke/plan.md`
- Outputs: `ops/development/INVOKE-PLAN-AGENT-ARCHITECTURE.md`
- Implementation layering: included
- Work-pack: single-file, split-ready
- Complexity: medium
- Per-layer planning: L0, L1, L2, L3
- SWU coverage: 11 SWUs
- Validation: command and review checks listed
- Next route: `task-session`
