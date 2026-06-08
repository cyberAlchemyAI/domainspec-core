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

# DomainSpec Runtime Reference Bundle

This directory is a thin DomainSpec reference bundle for Codex runtime use.

It intentionally does not vendor the full DomainSpec framework. It contains only framework docs, templates, architecture/layering references, and helper scripts that installed `.Codex/skills/` and `.codex/agents/` apply while producing real project artifacts.

Excluded by design:

- `copilot/` package and installer docs.
- `plan/` framework roadmap and internal task-session docs.
- framework example feature docs.
- ADLC/framework-roadmap docs that are not consumed by project-facing runtime skills.

Canonical source remains the DomainSpec framework repository.
