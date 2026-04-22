# MARS Implementation Scaffold

This directory establishes an implementation-facing home for MARS assets.

Current ownership remains split intentionally:
- Active Type B research orchestration assets stay under [/.github](../../.github) and [research/projects/mars](../../research/projects/mars).
- This scaffold exists so MARS can gain a canonical implementation pack layout without introducing duplicate active sources of truth today.

## Current Scope

- `implementation/mars/.github/` is reserved for future install-target material if MARS pack assets are promoted into an implementation distribution path.
- `implementation/mars/copilot/` is reserved for future canonical pack assets if ownership is explicitly migrated.

## Migration Rule

Do not manually mirror active MARS agents or skills into this scaffold unless ownership policy is updated first.

See [OWNERSHIP-MIGRATION.md](OWNERSHIP-MIGRATION.md) for the explicit promotion trigger and migration shape.