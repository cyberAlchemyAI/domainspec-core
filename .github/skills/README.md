# Research Orchestration Skills

Place Type B research orchestration skills in this directory.

Rules:

- Keep Type A canonical DomainSpec implementation skills in `implementation/domainspec/copilot`.
- Keep Type C project-local overlays in their local consumer repositories.
- Treat skills as the default Arcanum and DomainSpec runtime surface. Do not add paired `.codex/commands` files unless a documented runtime-compatibility task requires them.
- Track any migration decisions in `ops/AGENT-SKILL-TRIAGE-MATRIX.md`.

Research-scoped discovery skills include:

- `mars-research-start` — unified research startpoint for greenfield init and brownfield baseline audits
- `mars-research-interview` — interview and scope research problems before protocol design
- `mars-research-foundations` — create project-level domain-context and methodology/theory baselines backed by source catalog, reference ledger, and library-grade inventory coverage
- `mars-research-emit-signals` — emit structured MARS telemetry for workflow gaps, contract gaps, evidence gaps, and reflection proposals

Project-general reusable skills include:

- `implementation-layering` — create a project-agnostic POC-first implementation layering model for features, workflows, infrastructure changes, research workflows, or system improvements using value/cost layer-boundary heuristics.
- `arcanum-orchestrate` — route Arcanum sigil and spell requests to the canonical Arcanum registry in `arcanum/`.
