# System-Boundary Critic Brief

## Role

`system-boundary-critic`

## Objective

Independently falsify the proposed cohesive modular Arcanum building system. Look specifically for authority collapse, duplicate gates, missing producers or consumers, circular owner dependencies, replay/freshness holes, fixture-to-product proof inflation, migration dead ends, and public/private leakage.

## Selected route

Arcanum Route 2, bounded read-only helper inside Refine dispatch `20260805T164345Z-cohesive-modular-arcanum`.

## Required reads

- `ops/development/2026-08-05-arcanum-building-system-research/findings.md`
- this run's `REFINE-SEED-PROPOSAL.md`
- this run's `REFINE-DISPATCH.json`
- later, when requested by the parent: `stages/06-invoke-design.md`, `stages/08-distill-repair.md`, and `stages/09-invoke-plan.md`

## Allowed writes

None. Return native messages only. The parent will persist normalized receipts and critic findings inside the run folder.

## Forbidden scope

- all repository mutation
- Arcanum canonical or generated sources
- Craft and Inventory state
- telemetry dispatch ledger
- Git, submodules, registries, external research, publication, promotion, release, and deployment

## First-pass done criteria

Return a structured counterexample dossier covering:

1. hidden authority collapse;
2. missing or duplicated transition owners;
3. gate ordering and replay/freshness failure modes;
4. alternative-architecture arguments against the selected hypothesis;
5. proof-ceiling violations;
6. migration and compatibility hazards;
7. public/private boundary risks;
8. a provisional `pass|flag|block` owner-boundary verdict;
9. exact residue and reroute recommendations.

## Receipt shape

Return `agent_id`, `role_id`, `spawn_status`, `join_status`, `close_status`, `dispatch_id`, `step_id`, `capability_ref`, `status`, `artifacts`, `validation`, `observer_status`, `blockers`, `residue`, `reroute`, `handoff_note`, `scope reviewed`, `counterexamples`, `owner-boundary verdict`, and `migration risks`.

