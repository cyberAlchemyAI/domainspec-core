---
tags: [domainspec, codex, runtime, reference-bundle]
node_type: readme
is_session: false
layer: architecture, application
nature: reference
status: active
version: 0.1.0
last_updated: 2026-05-20
---

# DomainSpec Runtime Bundle

This is a thin runtime reference bundle for DomainSpec skills installed in this project.

It is not the full DomainSpec framework and it is not an installer package. The bundle contains only assets that project-facing DomainSpec skills apply while creating, auditing, or verifying real project artifacts:

- framework constraints and vocabulary (`CHANGELOG.md`, `TAXONOMY.md`, `RELATIONSHIPS.md`, `CONSTITUTION.md`);
- architecture and layering references (`ARCHITECTURE.md`, `ARCHITECTURE-PATTERN-LIBRARY.md`, `architecture/pattern-library/`);
- delivery rules (`TEST-PIPELINE.md`, `OBSERVABILITY.md`);
- artifact templates (`templates/`);
- referenced runtime helper scripts (`tools/`).

Runtime commands and skills live outside this bundle:

- `.codex/commands/`
- `.codex/agents/`
- `.Codex/skills/`
- `.Codex/get-shit-done/`
