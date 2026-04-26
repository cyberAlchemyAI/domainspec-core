# MARS Canonical Implementation Pack

This directory is the canonical implementation source for reusable MARS assets.

Canonical ownership now lives here for:

- MARS governance definitions and contracts
- MARS reusable templates
- MARS reusable copilot skill assets (`implementation/mars/copilot/skills/*`)
- MARS implementation-oriented pack scaffolding

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