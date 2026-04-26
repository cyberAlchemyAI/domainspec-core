# MARS Agent Rollout Plan

This rollout converts the research lifecycle from partially manual to fully owned.

## Canonical Asset Ownership

- Canonical MARS definitions/contracts: `implementation/mars/definitions/*`
- Canonical MARS templates: `implementation/mars/templates/*`
- Research projection and evidence execution: `research/projects/mars/**`

Projection refresh command:

```bash
./tools/sync_mars_canonical_assets.sh
```

## Lifecycle Coverage Snapshot

| Lifecycle step | Current owner | Status |
|---|---|---|
| Source discovery and validation | Sourcer | Covered |
| Inventory extraction and lookup | Inventorist | Covered |
| Execution orchestration | Orchestrator + Scientist | Covered |
| Data analysis and validity assessment | Analyst | Covered |
| Protocol design governance | Protocol Designer | Covered |
| Claim evidence governance | Evidence Auditor | Covered |

## Reusable Pattern Translation (DomainSpec Pass)

Full-pass source:

- `runbooks/DOMAINSPEC-REUSABLE-PATTERN-TRANSLATION-2026-04-26.md`

Immediate skill translations approved:

| Pattern | Translation | Owner | Priority |
|---|---|---|---|
| Authority source governance (pins/waivers/linkage) | `.github/skills/mars-research-authority-governance/SKILL.md` | Sourcer | P0 |
| Brownfield knowledge-stack normalization | `.github/skills/mars-research-knowledge-stack-normalization/SKILL.md` | Planner | P0 |

Queued next translations:

- Context bundle governance skill (P1)
- Gate preflight skill for protocol-local executable checks (P2)

## New Agents to Add First

## P0 (first)

### mars-research-orchestrator

Mission:
- Execute approved MARS plans using dependency-safe parallel waves across specialist agents.

Owns:
- Task graph and wave decomposition
- Parallel subagent dispatch for independent tasks
- Gate barrier enforcement between waves
- Consolidated execution status and blocker routing

Trigger:
- Approved runbook execution request
- Multi-agent execution request requiring parallelizable work

## P1 (second)

### mars-research-protocol-designer

Mission:
- Design and validate experiment protocols before any execution begins.

Owns:
- Criteria measurability
- Data schema completeness
- Dependency declaration
- Protocol pass/fail decision

Trigger:
- New experiment proposal
- Protocol modification request

## P2 (third)

### mars-research-evidence-auditor

Mission:
- Maintain claim-level evidence status across experiments and prioritize next runs.

Owns:
- Claim evidence matrix updates
- Coverage gaps per claim
- Recommendation order for pending experiments

Trigger:
- New result published
- Milestone evidence review

## P3 (future)

- Reproducibility Verifier
- Retrospective Conductor
- Claim Manager
- Publication Coordinator

## Reuse from DomainSpec + GSD

The MARS rollout reuses proven planning, execution, and context patterns:

- Planning baseline: `implementation/domainspec/.github/skills/gsd-plan-phase/SKILL.md`
- Execution baseline: `implementation/domainspec/.github/skills/gsd-execute-phase/SKILL.md`
- Execution orchestration pattern: `implementation/domainspec/.github/agents/gsd-executor.agent.md`
- Context mapping pattern: `implementation/domainspec/.github/agents/gsd-codebase-mapper.agent.md`
- Context artifacts template set:
	- `implementation/domainspec/.github/get-shit-done/templates/context.md`
	- `implementation/domainspec/.github/get-shit-done/templates/requirements.md`
	- `implementation/domainspec/.github/get-shit-done/templates/project.md`

## Rollout Sequence

0. Initialize MARS context pack and templates before first protocol design.
1. Introduce Protocol Designer and wire hard gate before execution.
2. Introduce Evidence Auditor and wire updates after analysis.
3. Backfill evidence status from existing completed experiments.
4. Run one foundation-tier dry run with explicit G1-G4 tabletop gate walkthrough.
5. Add future P2 agents when MARS reaches publication prep.

## Foundation Dry-Run Reference

- Protocol artifact: `experiments/MARS-DRY-RUN-E1-foundation/protocol.md`
- Gate policy (canonical): `implementation/mars/definitions/INVENTORY-READINESS-GATE.md`
- Multi-source policy (canonical): `implementation/mars/definitions/MULTI-SOURCE-CONTEXT-PATTERN.md`
- Bundle migration plan: `runbooks/EXPERIMENT-BUNDLE-MIGRATION-PLAN.md`

Expected dry-run outcome:

- G1 and G2 pass in tabletop mode.
- G3 and G4 remain pending until inventory and run-data artifacts are generated.
