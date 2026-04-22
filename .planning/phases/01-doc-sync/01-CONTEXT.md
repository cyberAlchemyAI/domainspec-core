# Phase 1: README and Pack Sync - Context

**Gathered:** 2026-04-21
**Status:** Ready for planning
**Source:** gsd discuss synthesis from implementation-versus-docs gap audit and maintainer decisions

<domain>
## Phase Boundary

This phase updates framework and copilot documentation plus packaging metadata so shipped assets and maintainer references are consistent. The phase does not change framework runtime behavior or domain semantics.

</domain>

<decisions>
## Implementation Decisions

### Audience and Structure
- Primary audience is framework maintainers.
- Keep onboarding readable while placing advanced capabilities in dedicated advanced sections.

### Command and Capability Exposure
- Main command tables list public commands only.
- Internal and bridge commands are documented in explicit appendices.
- Tuning loop and observer flow are documented as advanced operations, not hidden.

### Scope and Files
- Update these files in this phase:
  - implementation/domainspec/README.md
  - implementation/README.md
  - implementation/domainspec/copilot/README.md
  - implementation/domainspec/copilot/INSTALL.md
- Fix packaging for required bridge skills in distributable copilot assets.
- Add a deterministic docs-versus-assets drift guard.

### the agent's Discretion
- Exact heading names and table layout may vary as long as maintainers can verify public/internal command mapping quickly.
- Drift guard implementation can be script-based as long as checks are deterministic and reproducible.

</decisions>

<canonical_refs>
## Canonical References

Downstream agents MUST read these before planning or implementing.

### Core framework docs
- implementation/domainspec/README.md — Canonical framework operating model and command catalog
- implementation/README.md — Root mirror that must remain synchronized
- implementation/domainspec/CHANGELOG.md — Current version and capability history

### Copilot pack docs and assets
- implementation/domainspec/copilot/README.md — Copilot pack capability manifest
- implementation/domainspec/copilot/INSTALL.md — Installation behavior and post-install verification guidance
- implementation/domainspec/copilot/install.sh — Installer copy logic and packaging behavior
- implementation/domainspec/copilot/skills — Distributable DomainSpec skills
- implementation/domainspec/copilot/agents — Distributable DomainSpec agents

### Internal bridge and runtime references
- implementation/domainspec/.github/skills/domainspec-plan-phase-bridge/SKILL.md — Bridge skill referenced by planner
- implementation/domainspec/.github/skills/domainspec-execute-phase-bridge/SKILL.md — Bridge skill referenced by implementer
- implementation/domainspec/.github/get-shit-done/workflows/plan-phase.md — Planning workflow contract
- implementation/domainspec/.github/get-shit-done/templates/phase-prompt.md — PLAN file contract

</canonical_refs>

<specifics>
## Specific Ideas

- Close these known drift areas first: command/agent tables, advanced signal/observer coverage, template inventory, and stale version pointers.
- Keep implementation and mirror READMEs synchronized in one execution pass.
- Verify packaging by comparing referenced bridge skills against shipped `copilot/skills` directories.

</specifics>

<deferred>
## Deferred Ideas

- CI hard gate integration beyond local deterministic script output (candidate for next phase).
- Broader refactors of DomainSpec/GSD command naming taxonomy.

</deferred>

---

*Phase: 01-doc-sync*
*Context gathered: 2026-04-21 via focused maintainer decisions*
