# Inventory Explain View

## What Inventory Is Doing Here

Inventory is a Body War-local read-model package. It compiles selected project
knowledge into source-backed cards, JSON indexes, links, coverage notes, lookup
fixtures, and gap queues so future sessions can answer from a bounded evidence
set instead of rereading the whole project.

## What Inventory Is Not Doing

- It is not the Body War source of truth.
- It is not rewriting game rules.
- It is not creating the app, backend, Strava integration, or pilot operations.
- It is not inventorying the whole repository.
- It is not promoting generated links into definitions, ontology, or canonical
  product decisions.

## Canonical Source Docs

| Source | Authority Boundary |
| --- | --- |
| `docs/PROJECT-OVERVIEW.md` | Project identity, scope, and source policy. |
| `docs/PROJECT-DECISIONS.md` | Selected and unresolved project decisions. |
| `docs/features/game-rules/SPEC.md` | Game-rule design surface and rule gaps. |
| `docs/features/park-track-pilot/DISTILL.md` | Smallest coherent pilot concept. |
| `docs/features/park-track-pilot/implementation-layering.md` | Layered delivery and pilot promotion gates. |
| `docs/research/source-notes/` | Curated research notes when relevant. |

## Read Models

| Read Model | Role |
| --- | --- |
| Evidence Cards | Small source-backed claim records. |
| Selector Index | Maps source selectors to generated cards and records. |
| Link Index | Connects cards, sources, gaps, and handoffs using non-authority edges. |
| Gap/Risk Index | Keeps unresolved decisions visible with owners and next actions. |
| Coverage Report | Explains included sources, excluded sources, omissions, and warnings. |
| Retrieval Fixture | Shows what a lookup selected, excluded, and handed off. |

## Selected Evidence

{{selected_evidence_table}}

## Excluded Nearby Evidence

{{excluded_nearby_evidence_table}}

## What Is Missing

{{missing_or_unresolved_table}}

Minimum known gaps:

- Pilot validation city.
- First park and track set.
- Track boundary description format.
- App-backed validation implementation path.
- Operational scoring details for the first live pilot.

## Next Owner

{{next_owner}}

## Next Action

{{next_action}}
