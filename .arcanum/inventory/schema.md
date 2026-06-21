# Inventory Schema

Version: 0.1.0
Repository: `/home/vrondelli/projects/domainspec-core`

## Authority Rule

Raw repository files, submodules, ledgers, and generated runtime packages are
source evidence. Inventory pages are generated read models. A material claim in
this inventory must either cite a source path or be labeled as inference,
synthesis, or open question.

## Entry Fields

Durable generated pages should use repository YAML frontmatter before the main
heading. This profile follows the existing CyberAlchemy/capability-taxonomy
style:

```yaml
---
tags: [inventory, dispersed-knowledge]
node_type: findings
is_session: false
layer: architecture
nature: reference
status: draft
created: YYYY-MM-DD
dispatch_id: 2026-06-18-dispersed-knowledge-cartography
dispatch_type: research
working_folder: .arcanum/inventory/queries/<dispatch-id>/
sources: [arcanum/, implementation/domainspec/]
---
```

Rules:

- `tags` should use controlled tags from [tags.md](tags.md).
- `node_type` should describe artifact role, such as `source-manifest`,
  `research`, `findings`, `explore-strategy`, `ontology-map`,
  `lint-report`, `evidence-card`, or `evidence-set`.
- `is_session` is `false` for durable generated pages and `true` only for
  session transcripts.
- `layer` and `nature` preserve local vocabulary; do not promote them into
  canonical Arcanum definitions.
- `status` should be one of `draft`, `candidate`, `active`, `verified`,
  `pass`, `flag`, `block`, `stale`, `contradiction`, or `open-question`.
- `dispatch_id`, `dispatch_type`, and `working_folder` are required for
  dispatch-derived generated pages.
- `sources` should name concrete source roots or files.

Generated entries may also use these heading fields for shell-friendly lookup:

- ID: stable kebab-case identifier.
- Type: one of the controlled entry types below.
- Status: `active`, `candidate`, `stale`, `contradiction`, or `open-question`.
- Tags: comma-separated controlled tags from [tags.md](tags.md).
- Source refs: source paths and optional headings.
- Summary: short reusable explanation.
- Task fit: what downstream work this entry can support.
- Confidence: `high`, `medium`, or `low`.
- Residue: unresolved ambiguity, contradiction, or missing evidence.

## Entry Types

- `source`
- `entity`
- `concept`
- `architecture-layer`
- `implementation-pattern`
- `decision`
- `capability`
- `workflow`
- `interface`
- `dependency-rule`
- `test-pattern`
- `observability-signal`
- `question`
- `contradiction`
- `synthesis`

## Evidence Cards

Evidence-cards may be added under `entries/evidence-cards/` when selector-level
reuse is needed. A full card must include:

- ID
- Status
- Claim or candidate
- Source refs
- Authority level
- Promotion owner
- Trace
- Residue

Evidence-card handoffs are non-authority read models until the downstream owner
creates a governed artifact.

## EvidenceSets

EvidenceSets may be added under `entries/evidence-sets/` for repeat lookups.
They must reference evidence-card IDs instead of copying card content and must
include inclusion reasons, exclusions, handoff target, synthesis note, index
terms, status, and residue.

## Update Behavior

- Update `index.md` for every generated page or entry.
- Update `tags.md` when introducing a tag.
- Append `log.md` for install, ingest, lookup filing, lint, validate, backfill,
  and sync actions.
- Flag contradictions in `lint/` or as `contradiction` entries instead of
  overwriting them.
