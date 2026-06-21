# DomainSpec Core Inventory

Status: installed
Mode: repository-local compiled knowledge layer
Installed: 2026-06-18

This inventory gives agents a fast, source-backed map of the private
`domainspec-core` umbrella. It does not replace canonical sources. Raw sources
stay where they already live; generated inventory pages cite them and record
uncertainty instead of silently promoting claims.

## Conventions

- Inventory root: `.arcanum/inventory/`
- Raw source policy: read-only in place; do not copy private repo content into
  `raw/` unless a later task explicitly needs a preserved snapshot.
- Generated pages: `wiki/` for narrative maps, `entries/` for reusable typed
  records, `queries/` for durable answers, and `lint/` for health checks.
- Links: normal Markdown links, not wiki links.
- Frontmatter: durable generated pages use the repository YAML frontmatter
  profile in [schema.md](schema.md); low-level entries may also keep stable
  heading fields for shell-friendly lookup.
- Tags: controlled in [tags.md](tags.md).
- Observability: `.arcanum/observability/` exists, so inventory runs should
  record mode, sources, files changed, and validation notes in the inventory log
  and optional by-sigil observability ledgers.

## Lookup Path

1. Read [index.md](index.md).
2. Follow entries by type, tag, source, and task fit.
3. Use generated pages only as compiled read models.
4. Return source references and unresolved gaps to downstream sigils.

## Current Package

- [schema.md](schema.md) defines local entry fields and evidence rules.
- [index.md](index.md) lists generated pages and typed entries.
- [tags.md](tags.md) controls tag names.
- [log.md](log.md) records install, ingest, lint, and query changes.
- [wiki/repository-map.md](wiki/repository-map.md) is the first high-level map
  for repository navigation and v2 structure work.
- [entries/source-systems.md](entries/source-systems.md) catalogs the source
  systems detected during install.
