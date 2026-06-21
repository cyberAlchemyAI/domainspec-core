---
tags: [inventory, dispersed-knowledge, source-manifest, cartography, knowledge-system, public-private-boundary]
node_type: source-manifest
is_session: false
layer: architecture
nature: reference
status: draft
created: 2026-06-18
dispatch_id: 2026-06-18-dispersed-knowledge-cartography
dispatch_type: research
working_folder: .arcanum/inventory/queries/2026-06-18-dispersed-knowledge-cartography/
sources: [arcanum/, implementation/domainspec/, projects/framework-unification, projects/ontologize, cyberAlchemy/, .claude/skills/, docs/, research/, projects/domainspec-v2/, .arcanum/]
---

# Source Manifest - Dispersed Knowledge Cartography

This manifest is a pointer list, not a copy of raw sources. Raw repository
sources remain read-only inputs.

## Cohorts

| Cohort | Source paths | Branch hypothesis | Expected inventory types | Priority |
| --- | --- | --- | --- | --- |
| Public Arcanum capability system | `arcanum/`, `arcanum/registry/`, `arcanum/formulae/`, `arcanum/transmutations/`, `arcanum/arcana/`, `arcanum/spells/` | system, bridge | `capability`, `workflow`, `architecture-layer`, `dependency-rule`, `observability-signal` | high |
| Generated runtime mirrors | `.agents/skills/`, `.claude/skills/`, `.codex/commands/`, `.github/skills/` | system | `capability`, `interface`, `workflow`, `source` | high |
| Private DomainSpec implementation | `implementation/domainspec/` | system, bridge | `architecture-layer`, `implementation-pattern`, `interface`, `test-pattern`, `decision` | high |
| Parent governance and decisions | `AGENTS.md`, `CLAUDE.md`, `SUBMODULE-DISCIPLINE.md`, `docs/`, `ops/`, `sessions/`, `telemetry/` | bridge | `decision`, `dependency-rule`, `workflow`, `observability-signal` | high |
| DomainSpec v2 research | `projects/domainspec-v2/` | business, bridge | `concept`, `workflow`, `decision`, `question`, `synthesis` | high |
| CyberAlchemy system knowledge | `cyberAlchemy/`, `research/cyber-alchemy-space/` | business, bridge | `concept`, `capability`, `workflow`, `synthesis`, `question` | high |
| Framework unification | `projects/framework-unification/` | bridge | `concept`, `architecture-layer`, `decision`, `synthesis` | medium |
| Ontologize product/method knowledge | `projects/ontologize/` | business, bridge | `concept`, `workflow`, `decision`, `synthesis` | medium |
| Repository research towers | `research/`, excluding very large/generated build outputs | business, bridge | `source`, `concept`, `test-pattern`, `decision`, `synthesis`, `question` | medium |
| Local Arcanum state | `.arcanum/necronomicon/`, `.arcanum/observability/`, `.arcanum/profiles/`, `.arcanum/runtime/` | system, bridge | `workflow`, `observability-signal`, `source`, `question` | medium |

## Exclusions And Guards

- Do not ingest `.git/`, `node_modules/`, generated build folders, binary
  archives, or PDFs without a separate extraction plan.
- Do not mutate public `arcanum/` during this private inventory route.
- Treat sessions, dispatch returns, and observability as evidence records, not
  authority.
- Treat generated skill mirrors as runtime surfaces; trace canonical ownership
  before claiming a capability definition.

## Required Receipt Fields

Each cartographer return must include:

- role id,
- source paths inspected,
- source paths excluded and why,
- source-backed claims,
- candidate inventory entries,
- candidate evidence-card selectors,
- contradictions,
- open questions,
- branch hypothesis,
- promotion guardrail notes,
- residue.
