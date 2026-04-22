# DomainSpec Documentation and Packaging Sync

## What This Is

This project aligns DomainSpec implementation documentation with what is actually shipped in the framework and copilot pack. It is maintainers-first and focuses on command catalogs, pipeline behavior, template inventories, and installer behavior.

## Core Value

Maintainers and adopters can trust that documented commands, templates, and install instructions match shipped assets.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] DOC-01 Main framework README reflects shipped capabilities and current version references.
- [ ] DOC-02 Root mirror README remains synchronized with the canonical implementation README.
- [ ] DOC-03 Copilot README lists shipped agents and commands accurately.
- [ ] DOC-04 INSTALL guide matches real installer behavior and bridge/internal command handling.
- [ ] PKG-01 Required bridge skills referenced by agents are included in distributable copilot skills.
- [ ] GOV-01 A repeatable drift guard exists for docs versus shipped assets.

### Out of Scope

- Product behavior changes — this effort is documentation and packaging alignment only.
- New framework features unrelated to documentation or packaging drift.
- UI or infra implementation changes in consumer projects.

## Context

A gap audit identified mismatches between implementation assets and documentation coverage:
- Main README contains stale version references and incomplete advanced capability coverage.
- Copilot README omits multiple shipped commands and agents.
- INSTALL guidance references bridge behavior that depends on skills not shipped in the distributable pack.
- Template inventory documentation omits shipped artifacts.

## Constraints

- **Source of Truth**: `implementation/domainspec` is the canonical implementation source.
- **Mirror Discipline**: `implementation/README.md` must mirror canonical README changes.
- **Path Policy**: Canonical paths only; no compatibility aliases unless explicitly requested.
- **Scope Control**: Preserve existing public APIs and behavior while correcting documentation and packaging drift.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Optimize docs for maintainers | This update targets operational accuracy and governance confidence | — Pending |
| Place tuning and observer content in advanced sections | Keep onboarding readable while preserving full capability coverage | — Pending |
| Keep public commands in main tables and internal commands in appendix | Expose what users should run while still documenting bridge mechanics | — Pending |
| Fix packaging for required bridge skills | Agent references must resolve after standard install | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

After each phase transition (via `/gsd-transition`):
1. Requirements invalidated -> Move to Out of Scope with reason.
2. Requirements validated -> Move to Validated with phase reference.
3. New requirements emerged -> Add to Active.
4. Decisions to log -> Add to Key Decisions.
5. What This Is still accurate -> Update if drifted.

After each milestone (via `/gsd-complete-milestone`):
1. Full review of all sections.
2. Core Value check — still the right priority.
3. Audit Out of Scope — reasons still valid.
4. Update Context with current state.

---
*Last updated: 2026-04-21 after gsd planning bootstrap*
