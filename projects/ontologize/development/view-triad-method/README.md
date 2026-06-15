# Ontologize View-Triad Method Development Pack

Invoke-authored development pack for making the DomainSpec view triad a repeatable Ontologize method.

## Purpose

Ontologize already has a BI-led ontology+DAG engagement baseline, with the optimization chain as the contract that turns operational action, evidence-linked metrics, analysis methods, and BI optimizations into governed client language.

This pack adds a second repeatable method spine, now refined so each view materializes the four ontology branches without creating a separate branch-view:

```text
source corpus or discovery
-> branch materialization register maps B1/B2/B3/B4 evidence
-> system-view names shape and live stances
-> engineer-view owns one verdict row per stance
-> ontology-view types terms, edges, and forbidden relations
-> client or product deliverable cites the three views without deciding twice
```

The goal is not to replace `OPTIMIZATION-CHAIN-METHOD.md`. The goal is to make the view triad the method Ontologize uses when a client, product, or research corpus needs explainable structure, auditable decisions, and typed ontology governance before BI claims or agent work are trusted.

## Pack Contents

| Artifact | Role |
| --- | --- |
| [SPEC.md](SPEC.md) | Define-mode baseline for the method extension. |
| [GLOSSARY.md](GLOSSARY.md) | Local glossary for terms introduced by this pack. |
| [BRANCH-MATERIALIZATION.md](BRANCH-MATERIALIZATION.md) | Branch coverage profile for B1 meaning, B2 system, B3 run-context, and B4 bridge. |
| [DESIGN.md](DESIGN.md) | Six-view architecture/design bundle. |
| [SKILL-ROUTING.md](SKILL-ROUTING.md) | Inventory of sibling skills and when to use them here. |
| [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0-L3 layer decisions. |
| [PLAN.md](PLAN.md) | Implementation plan with delivery slices and validation. |
| [WORK-PACK.md](WORK-PACK.md) | Task-session-ready work-pack and SWU manifest. |
| [EXECUTION-PACK.md](EXECUTION-PACK.md) | Wave choreography for the work-pack. |
| [INVOKE-RESULT.md](INVOKE-RESULT.md) | Invoke result, transport notes, and next route. |
| [work-pack/tasks/](work-pack/tasks/) | Task-local execution contracts. |
| [work-pack/waves/](work-pack/waves/) | Layer-mapped wave contracts. |

## Source Boundary

Primary Ontologize sources:

- `projects/ontologize/README.md`
- `projects/ontologize/PRODUCT.md`
- `projects/ontologize/SPEC.md`
- `projects/ontologize/DESIGN.md`
- `projects/ontologize/PLAN.md`
- `projects/ontologize/WORK-PACK.md`
- `projects/ontologize/GLOSSARY.md`
- `projects/ontologize/OPTIMIZATION-CHAIN-METHOD.md`
- `projects/ontologize/ONTOLOGY-BRANCHES.md`
- `projects/ontologize/DAG-AND-METRICS.md`

Primary sibling skill sources:

- `implementation/domainspec/.claude/skills/system-view/SKILL.md`
- `implementation/domainspec/.claude/skills/engineer-view/SKILL.md`
- `implementation/domainspec/.claude/skills/ontology-view/SKILL.md`
- `implementation/domainspec/.claude/skills/domainspec-subagents-strategy/SKILL.md`
- `implementation/domainspec/.claude/skills/domainspec-interview-kits/SKILL.md`
- `implementation/domainspec/.claude/skills/domainspec-context-builder/SKILL.md`
- `implementation/domainspec/.claude/skills/domainspec-task-session/SKILL.md`
- `implementation/domainspec/.claude/skills/domainspec-decision-gate/SKILL.md`

## Current Gate

`workPackGateStatus = pass-for-planning`.

Mutation-capable execution should start with [TASK-VTM-001](work-pack/tasks/TASK-VTM-001-METHOD-BOUNDARY.md). It must not edit public/product-facing Ontologize docs until the L0 method boundary artifact and branch materialization register pass review.
