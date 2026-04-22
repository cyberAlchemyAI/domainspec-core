# MARS Agent Rollout Plan

This rollout converts the research lifecycle from partially manual to fully owned.

## Lifecycle Coverage Snapshot

| Lifecycle step | Current owner | Status |
|---|---|---|
| Source discovery and validation | Sourcer | Covered |
| Inventory extraction and lookup | Inventorist | Covered |
| Execution orchestration | Scientist | Covered |
| Data analysis and validity assessment | Analyst | Covered |
| Protocol design governance | Missing | Gap |
| Claim evidence governance | Missing | Gap |

## New Agents to Add First

## P0 (first)

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

## P1 (second)

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

## P2 (future)

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
- Gate policy: `definitions/INVENTORY-READINESS-GATE.md`
- Multi-source policy: `definitions/MULTI-SOURCE-CONTEXT-PATTERN.md`
- Bundle migration plan: `runbooks/EXPERIMENT-BUNDLE-MIGRATION-PLAN.md`

Expected dry-run outcome:

- G1 and G2 pass in tabletop mode.
- G3 and G4 remain pending until inventory and run-data artifacts are generated.
