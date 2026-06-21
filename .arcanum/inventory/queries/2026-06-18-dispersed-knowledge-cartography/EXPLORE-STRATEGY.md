---
tags: [inventory, dispersed-knowledge, cartography, dispatch-spec, ontology-vault, knowledge-craft-governance, source-manifest, promotion-guardrail]
node_type: explore-strategy
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

# Explore Strategy - Dispersed Knowledge Cartography

## Objective

Create a real repository knowledge cartography pass that can feed
`.arcanum/inventory/` and then give `ontology-vault` a condensed candidate map.
This route is designed, validated, and handoff-ready. It has not run the main
cartographer subagents yet.

## Strategy

1. Build a concrete source manifest with the YAML frontmatter profile the repo
   already uses in `research/cyber-alchemy-space/capability-taxonomy/`.
2. Run four source-family cartographers in parallel after explicit operator
   approval.
3. Join returns into source-backed Inventory artifacts:
   - source summaries,
   - evidence-cards,
   - EvidenceSets,
   - lookup pages,
   - contradiction and residue records.
4. Let `ontology-vault` condense the inventory into branch-aware candidate
   ontology roles, edges, and gaps.
5. Validate route, source, inventory, and ontology boundaries before reporting
   success.

## Cartographer Lanes

| Role | Owns | Primary sources | Expected return |
| --- | --- | --- | --- |
| `cartographer-arcanum-capabilities` | Public Arcanum framework and generated runtime mirrors | `arcanum/`, `.agents/skills/`, `.claude/skills/`, `.codex/commands/`, `.github/skills/` | Capability and runtime-surface map with canonical-vs-generated notes. |
| `cartographer-domainspec-private` | Private implementation and validation evidence | `implementation/domainspec/`, `validation/poker-team/`, `docs/`, `ops/`, `sessions/`, `telemetry/` | Private authority and implementation-evidence map. |
| `cartographer-project-research` | Project research and product knowledge | `projects/`, `research/`, `cyberAlchemy/`, `projects/domainspec-v2/` | Research tower, project, and product knowledge map. |
| `cartographer-knowledge-governance` | Knowledge governance and operational memory | `.arcanum/`, ontology/vault folders, Craft ledgers, dispatch ledgers, observability | Inventory, ontology, definitions, Craft, dispatch, and observability map. |
| `cartography-skeptic` | Boundary and omission attack | Parent synthesis and candidate ontology map | Defect list: missed corpora, duplicate authority, source-less claims, promotion leakage. |

## Tagging Profile

Every durable generated research, findings, source-manifest, inventory query,
and ontology-map artifact should use this profile:

```yaml
---
tags: [inventory, dispersed-knowledge, cartography]
node_type: findings
is_session: false
layer: architecture
nature: reference
status: draft
created: 2026-06-18
dispatch_id: 2026-06-18-dispersed-knowledge-cartography
dispatch_type: research
working_folder: .arcanum/inventory/queries/2026-06-18-dispersed-knowledge-cartography/
sources: [arcanum/, implementation/domainspec/, projects/framework-unification, projects/ontologize, cyberAlchemy/, .claude/skills/]
---
```

Add tags only from `.arcanum/inventory/tags.md`, unless the run also updates
that controlled tag file.

## Inventory Outputs

| Output | Path | Authority |
| --- | --- | --- |
| Source manifest | `.arcanum/inventory/raw/manifests/2026-06-18-dispersed-knowledge-sources.md` | Pointer list; not a copy of sources. |
| Research returns | `.arcanum/inventory/queries/2026-06-18-dispersed-knowledge-cartography/research.md` | Raw delegated evidence after run. |
| Findings | `.arcanum/inventory/queries/2026-06-18-dispersed-knowledge-cartography/findings.md` | Synthesis; every claim cites returns or source refs. |
| Evidence-cards | `.arcanum/inventory/entries/evidence-cards/` | Candidate inventory records. |
| EvidenceSets | `.arcanum/inventory/entries/evidence-sets/` | Candidate grouping records. |
| Lint report | `.arcanum/inventory/lint/2026-06-18-dispersed-knowledge-cartography.md` | Health and boundary report. |

## Ontology Condensation

`ontology-vault` should consume inventory evidence as evidence records and
write candidate branch maps under `.arcanum/ontology-vault/`. It may condense:

- local roles into generic ontology concepts,
- business/system/bridge branch ownership,
- edge rules,
- evidence gaps,
- drift findings,
- confidence posture.

It must not promote candidate Inventory, Ontology, glossary, sigil, or spell
knowledge. Promotion requires a later owner decision.

## Confirmation Prompt

Run the required repository cartographer subagents for
`2026-06-18-dispersed-knowledge-cartography` and require source-backed receipts
before inventory ingest?
