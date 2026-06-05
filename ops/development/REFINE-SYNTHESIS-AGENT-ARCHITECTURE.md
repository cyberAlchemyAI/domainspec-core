# Refine Synthesis: Agent Architecture Canonicalization

Date: 2026-06-01
Mode: `refine`
Input design: `ops/development/INVOKE-DESIGN-AGENT-ARCHITECTURE.md`
Status: pass with approval gate

## Refined Target

Build a Claude/Codex-focused canonical-source and downstream-reader architecture for DomainSpec Core skills and agents.

The smallest coherent implementation unit is not "copy every newest file." It is:

```text
create a Claude/Codex canonical map plus a GitHub deletion-candidate report
```

That unit can prove the active runtime architecture without mutating child owner scopes or deleting GitHub prematurely.

## Refined Concept

The agent architecture should be a Claude/Codex source-map architecture, not a GitHub-preservation architecture.

Canonical ownership lives in owner surfaces:

- DomainSpec implementation automation: `implementation/domainspec/copilot/*`.
- Claude runtime adapters: `implementation/domainspec/.claude/agents/*`.
- Codex runtime adapters: `implementation/domainspec/.codex/agents/*` plus machine-global Codex skills when explicitly scoped.
- GSD workflow runtime: keep only if Claude/Codex still consume it.
- Lean proof-domain automation: `domainspec-lean-formalization/.agents/*`.
- Arcanum lifecycle capabilities: canonical Arcanum source and Codex/Claude runtime adapters, not GitHub generated copies.

Runtime surfaces read from canonical owners by one of four approved reader modes:

1. `claude-reader`: Claude agent prompt or skill surface.
2. `codex-reader`: Codex TOML/skill package surface.
3. `shared-skill-facade`: local `.agents/skills` facade where still needed.
4. `delete-candidate`: GitHub surface with active Claude/Codex replacement or no active use.

Anything else is `drift`, `orphan`, `residue`, or `blocked-owner`.

## Refinement Decisions

| Question | Refined decision |
| --- | --- |
| Should the plan copy newest files directly? | No. Newest mtime is evidence, not authority. |
| What should be canonical first? | A canonical map with owner/source/downstream relationships. |
| What is the first write scope? | Root-owned `ops` and `tools` only, then deletion after explicit approval. |
| Should child surfaces be edited? | No, not without owner-scoped task approval. |
| Should Lean proof-domain skills be merged into DomainSpec runtime skills? | No. Keep Lean lane separate. |
| Should GitHub be preserved as a target? | No. Treat root and implementation `.github` surfaces as deletion candidates. |

## Refined Architecture Shape

```text
Evidence ledgers
  -> canonical map
    -> Claude/Codex parity checker
      -> GitHub deletion-candidate report
        -> owner-scoped handoffs and deletion task
```

The canonical map should be the stable contract. It should allow future generators to update Claude and Codex surfaces. GitHub surfaces should be reported as delete candidates after usage and parity checks.

## Required Outputs For Plan

The plan should produce:

- `ops/development/skill-agent-canonical-map.json`
- `tools/check_skill_agent_surface_drift.py`
- `ops/development/CLAUDE-CODEX-SURFACE-DRIFT-REPORT.md`
- `ops/development/GITHUB-SURFACE-DELETION-CANDIDATES.md`
- `ops/development/DOMAINSPEC-OWNER-HANDOFF.md`
- `ops/development/LEAN-FORMALIZATION-OWNER-HANDOFF.md`
- optional deletion task for root `.github/skills`, root `.github/agents`, and implementation `.github/agents`

## Layering Seed

| Layer | Goal | Evidence |
| --- | --- | --- |
| L0 | Generate Claude/Codex canonical map and read-only drift report. | Checker runs and reports without mutation. |
| L1 | Build GitHub deletion-candidate report. | Report proves replacement, no active use, or blocked reason. |
| L2 | Add owner-scoped handoffs and deletion decision record. | Handoffs and deletion gate exist. |
| L3 | Delete approved GitHub surfaces and remove stale policy references. | Git status shows intended removals only. |

## Refined Risks

- If the checker tries to normalize too much body text at L0, it may hide real drift. L0 should prefer conservative hash/provenance reporting.
- If GitHub surfaces are deleted before usage scan, scripts/docs may break.
- If Lean utilities are deduped too early, proof-domain guardrails may be weakened.
- If DomainSpec-owned surfaces are updated from parent scope, the work violates current owner-boundary policy.

## Refine Result

- Target: DomainSpec skill and agent architecture
- Status: pass
- Preset: standard
- Research: no-research; local repository evidence already sufficient
- Seed proposal: use Claude/Codex source-map architecture and GitHub deletion lane
- Dispatch strategy: design/refine/plan chain; no subagent execution needed after completed research lanes
- Final synthesis: implement Claude/Codex canonical map, deletion-candidate report, then delete GitHub after approval
- Recommended next routes: `invoke plan`, then `task-session` after approval
