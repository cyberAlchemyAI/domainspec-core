# CyberAlchemy v2

Status: project start
Owner: CyberAlchemy v2
Started: 2026-06-19
Current boundary: private `domainspec-core` project folder; future standalone repository candidate

CyberAlchemy v2 is the consolidation surface for the work dispersed through
`domainspec-core`. It is intended to become the next stable repository, but it
starts here as a source-ledgered project so authority, evidence, and promotion
boundaries are visible before extraction.

The project is an amalgamation by governance, not by copying. Source systems
stay in their homes. This project records the stable spine, local definitions,
constitution rules, source map, and promotion path that decide what may later
become repository authority.

## Repository Objective

CyberAlchemy v2 is intended to become the base repository someone receives when
they download CyberAlchemy: a governed starting point with authority, ontology,
inventory, definitions, constitutions, disciplines, and promotion routes already
made explicit. Downstream projects should be able to construct above this base
instead of reopening the source ambiguity that CyberAlchemy v2 is resolving.

The `ontology/` area is where v2 fixes the authority shape as a
candidate/projection package: it maps meaning, evidence, owner routes, promotion
requests, projection boundaries, and residue so the base can be extended without
letting ontology promote itself.

## Start Here

| Need | Open |
| --- | --- |
| Project authority model | [authority/README.md](authority/README.md) |
| Authority import ledgers | [authority/imports/README.md](authority/imports/README.md) |
| Source corpus and ingest boundary | [SOURCE-MAP.md](SOURCE-MAP.md) |
| Craft execution surface | [CRAFT.md](CRAFT.md) |
| Local definitions | [authority/definitions/DEFINITIONS.md](authority/definitions/DEFINITIONS.md) |
| Definition towers | [authority/definitions/DEFINITION-TOWERS.md](authority/definitions/DEFINITION-TOWERS.md) |
| Stable repository constitution | [authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md](authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md) |
| Constitution import pack | [authority/constitutions/CONSTITUTION-IMPORT-PACK.md](authority/constitutions/CONSTITUTION-IMPORT-PACK.md) |
| Initial constitution pack | [development/constitution-pack.md](development/constitution-pack.md) |
| Project discipline catalog | [disciplines/DISCIPLINES.md](disciplines/DISCIPLINES.md) |

## Import Spine

CyberAlchemy v2 starts from an explicit authority import layer:

- [authority/imports/definitions/MANIFEST.md](authority/imports/definitions/MANIFEST.md)
  stages 149 definition-like source candidates and 28 auxiliary sources.
- [authority/imports/constitutions/MANIFEST.md](authority/imports/constitutions/MANIFEST.md)
  stages 106 constitution/axiom source candidates and 3 auxiliary templates.

These imports are candidates until promoted. The smaller source spine below is
only the orientation layer for the first review, not the full authority corpus.

## Source Spine

The first source spine is deliberately small:

- inventory read model: [../.arcanum/inventory/index.md](../.arcanum/inventory/index.md)
- ontology candidate map: [../.arcanum/ontology-vault/map-2026-06-18-dispersed-knowledge.md](../.arcanum/ontology-vault/map-2026-06-18-dispersed-knowledge.md)
- CyberAlchemy method: [../arcanum/framework/CYBERALCHEMY-METHOD.md](../arcanum/framework/CYBERALCHEMY-METHOD.md)
- CyberAlchemy agentic system: [../cyberAlchemy/README.md](../cyberAlchemy/README.md)
- framework-unification map: [../projects/framework-unification/CONCEPT-MAP.md](../projects/framework-unification/CONCEPT-MAP.md)
- CyberAlchemy Lean fusion layer: [../projects/framework-unification/layers/cyber-alchemy-lean-fusion/README.md](../projects/framework-unification/layers/cyber-alchemy-lean-fusion/README.md)
- Arcanum framework: [../arcanum/README.md](../arcanum/README.md)
- DomainSpec v2 research precedent: [../projects/domainspec-v2/README.md](../projects/domainspec-v2/README.md)

## Stable Thesis

CyberAlchemy v2 should preserve four separations:

1. Source evidence is not the same as promoted authority.
2. Inventory and ontology are reusable read models, not promotion shortcuts.
3. Public Arcanum patterns and private DomainSpec implementation evidence must
   remain boundary-aware.
4. Research, specifications, runtime, validation, observability, and operations
   need separate homes even when they describe the same system.

## Repository Shape

| Area | Role |
| --- | --- |
| [authority/](authority/README.md) | Definitions, constitutions, boundaries, decisions, and promotion policy. |
| [disciplines/](disciplines/DISCIPLINES.md) | Evidence-backed recurring practices for this repository surface. |
| [research/](research/README.md) | Source-ledgered towers, investigations, and candidate synthesis. |
| [architecture/](architecture/README.md) | Promoted or candidate layer maps, structure decisions, and system views. |
| [capabilities/](capabilities/README.md) | Capability contracts, packages, and generated-surface boundaries after promotion. |
| [specs/](specs/README.md) | Domain, runtime, validation, and artifact contracts after promotion. |
| [implementation/](implementation/README.md) | Code and package work after a task-session or implementation gate. |
| [validation/](validation/README.md) | Fixtures, harnesses, reports, and evidence snapshots. |
| [inventory/](inventory/README.md) | Project-local exported read models and evidence-card links. |
| [ontology/](ontology/README.md) | Candidate branch maps and promotion requests, not self-promotion. |
| [observability/](observability/README.md) | Signals, reflections, dispatch traces, and maintenance evidence. |
| [ops/](ops/README.md) | Work-packs, task sessions, release notes, extraction plans, and handoffs. |

## Current Gate

Gate result: flag.

This project is started and navigable. It is not yet a standalone repository,
and none of its source-map claims are promoted architecture decisions. The next
gate is owner review of the top-level shape and whether `inventory/` and
`ontology/` should remain visible top-level areas or become `.arcanum/`
implementation details with exported docs.

## Open Questions

### OQ-1. When does this become a standalone repository?

Context: it is currently staged inside the private parent. Recommendation:
extract only after the authority model, source map, and public/private boundary
rules pass review. Status: OPEN.

### OQ-2. Which parts may become public?

Context: sources include public Arcanum, private implementation evidence, and
project-local research. Recommendation: run a boundary scrub before any public
derivative. Status: OPEN.
