---
docType: refine-seed-proposal
runId: 20260608T075521Z-inventory-interface-indexing-body-war
status: strategy-proposal
target: body-war-inventory-interface-indexing
updatedAt: 2026-06-08
---

# Refine Seed Proposal: Inventory Interface/Indexing For Body War

## Operator Intent

Use `/home/vrondelli/projects/domainspec-core/projects/body-war` as the new
target for the Inventory interface/indexing refine route.

## Target Boundary

Primary target:

```text
/home/vrondelli/projects/domainspec-core/projects/body-war
```

Run folder:

```text
development/refinement-runs/20260608T075521Z-inventory-interface-indexing-body-war/
```

Capability source:

```text
/home/vrondelli/projects/domainspec-core/arcanum/arcana/inventory/
```

## Desired Outcome

Produce a Body War-local, MVP-ready non-executed plan for using Inventory to
infer, confirm, inventorize, index, and later retrieve the project knowledge
already dispersed across Body War's DomainSpec docs, Arcanum harness, source
notes, and feature slices.

## Evidence Baseline

| Source                                                                           | Role                                                         |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| `README.md`                                                                      | Body War/TROQAR project identity and structure.              |
| `docs/PROJECT-OVERVIEW.md`                                                       | Product summary, source evidence, audience, and scope.       |
| `docs/features/game-rules/SPEC.md`                                               | First DomainSpec feature slice and open game-rule decisions. |
| `docs/features/park-track-pilot/DISTILL.md`                                      | Current smallest coherent pilot candidate.                   |
| `docs/research/source-notes/`                                                    | Curated source notes from supplied evidence.                 |
| `.codex/commands/`                                                               | Project-local Arcanum command surface.                       |
| `.arcanum/`                                                                      | Project-local Arcanum observability and Necronomicon state.  |
| `domainspec/`                                                                    | Local DomainSpec runtime/reference bundle.                   |
| `arcanum/arcana/inventory/development/WORK-PACK.md`                              | Inventory interface/indexing execution order.                |
| `arcanum/arcana/inventory/development/decisions/INTERFACE-INDEXING-OPEN-GATE.md` | Current Inventory blockers and deferrals.                    |

## Why Body War Is A Better Target

Body War is a live project with scattered but bounded knowledge:

- project overview,
- initial definitions,
- decisions and hypotheses,
- source-note research,
- game-rules feature spec,
- park-track-pilot distillation,
- local Arcanum/Codex surfaces.

That makes it a more realistic first Inventory target than an Arcanum-only
authority example. It tests whether `$inventory` can help a user ask "what do we
know about this project?" and get cards, selectors, links, gaps, and next routes.

## Recommended First Inventory Pilot Corpus

Recommended target after templates and validators exist:

```text
docs/features/park-track-pilot/
docs/features/game-rules/SPEC.md
docs/PROJECT-OVERVIEW.md
docs/PROJECT-DECISIONS.md
```

Reason: this corpus is small enough to confirm, but rich enough to test the
actual Inventory job: connect product intent, rules, decisions, candidate pilot
shape, and unresolved gaps.

## Write Scope For This Proposal

Allowed:

- this refinement run folder.

Not allowed during proposal:

- pilot slice mutation,
- source doc rewrites,
- broad Body War repository inventory sweep,
- mutation of `.codex`, `.arcanum`, or generated observability state,
- promotion of Inventory links into DomainSpec definitions or ontology.

## Preset And Research

- Preset: `standard`
- Research mode: `no-research`

Body War already has curated source notes; external research is not needed for
this retargeting pass.

## Selected Technique Overlays

| Overlay                               | Why                                                                                      |
| ------------------------------------- | ---------------------------------------------------------------------------------------- |
| `baseline_sequence`                   | Keep the standard ten-stage refine route.                                                |
| `route_menu_for_ambiguity`            | The first pilot corpus has multiple viable project-local options.                        |
| `xray_for_hidden_structure`           | Body War knowledge is spread across product, rules, pilot, decisions, and source notes.  |
| `memory_residue_for_context_recovery` | Prior Inventory and Body War MVP-readiness artifacts should be reused, not rediscovered. |

## Confirmation Gate

This proposal does not execute the refine route yet.

Confirm to run the Body War-targeted refine route.
