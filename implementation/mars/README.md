# MARS Canonical Implementation Pack

This directory is the canonical implementation source for reusable MARS assets.

Canonical ownership now lives here for:

- MARS governance definitions and contracts
- MARS reusable templates
- MARS reusable copilot skill assets (`implementation/mars/copilot/skills/*`)
- MARS implementation-oriented pack scaffolding
- experimental paper-design workflow assets that will be iterated after pilot projects complete

## Canonical Model

- Canonical implementation and reusable assets: [implementation/mars](.)
- Research execution and evidence projection: [research/projects/mars](../../research/projects/mars)
- Orchestration-local runtime projection: [/.github](../../.github)

The research project is a generalized application of the DomainSpec solution to research workflows. It consumes the canonical MARS definition/template assets and stores run-time evidence artifacts.

## Sync Rule

When canonical definitions/templates or canonical copilot skills are updated, run sync:

```bash
./tools/sync_mars_canonical_assets.sh
```

This sync command now refreshes:

- `research/projects/mars/{definitions,templates}` projection copies
- managed runtime skill copies in `/.github/skills/*` for canonical skills under `implementation/mars/copilot/skills/*`

Then validate structure:

```bash
./tools/check_research_structure.sh
```

See [OWNERSHIP-MIGRATION.md](OWNERSHIP-MIGRATION.md) for ownership boundaries and synchronization guardrails.

## Experimental Paper Design Pilot

The canonical pack now also carries a pilot paper-design model for MARS research papers:

- derivation rules: `implementation/mars/definitions/PAPER-DERIVATION-RULES.md`
- reusable templates: `implementation/mars/templates/paper-*.md`

These assets are intentionally non-gating for now. They exist so project pilots such as MOGT can exercise a concrete working model before the workflow is hardened into a stable MARS stage or skill.

## Inventory Library Chain

The canonical pack now defines an explicit inventory-library pattern for research sources:

- contract: `implementation/mars/definitions/INVENTORY-LIBRARY-CONTRACT.md`
- templates: `implementation/mars/templates/inventory-schema-template.md`, `implementation/mars/templates/inventory-library-entry-template.md`, `implementation/mars/templates/raw-content-note-template.md`

The intended chain is:

1. source catalog
2. reference ledger
3. inventory index
4. per-source library file
5. raw content provenance

When web retrieval is not possible, user-provided raw files become the provenance base for the library entry.
