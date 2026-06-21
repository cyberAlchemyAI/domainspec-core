---
tags: [inventory, source-manifest, source-import, house-project-vault, cyberalchemy-v2, promotion-guardrail]
node_type: source-manifest
is_session: false
layer: knowledge-governance
nature: reference
status: active
created: 2026-06-21
dispatch_id: 2026-06-21-house-project-vault-import
dispatch_type: ingest
working_folder: .arcanum/inventory/queries/2026-06-21-house-project-vault-import/
sources: [cyberAlchemy-v2/authority/imports/house_project/docs/vault/]
---

# House Project Vault Import Source Manifest

## Source Cohort

- Original source: `/home/vrondelli/projects/house_project/docs/vault/`
- Imported source: `cyberAlchemy-v2/authority/imports/house_project/docs/vault/`
- Source repository commit: `777c9b4b60e99e192986207bf0d75f53707ccb4b`
- Source commit date: `2026-06-08T10:17:03-03:00`
- Source commit subject: `chore(claude): install Arcanum skill packages + retire legacy command surface`
- Import count: 529 retained files, 4.5M.
- Publish-safety exclusion: 21 source `.obsidian/` local app/plugin config files
  were excluded before parent publish because plugin settings can contain
  credentials or machine-specific state.
- Dirty-state note: `git -C ../house_project status --short -- docs/vault`
  returned no dirty paths at import time.

## Search Priority

Use this order for future CyberAlchemy v2 governance searches over this source:

1. Root navigation and schema docs:
   - `agent-navigation.md`
   - `ontology-conventions.md`
   - `ontology-constitution.md`
   - `confidence-levels.md`
2. Axioms and premises:
   - `axiom/ontology-axioms.md`
   - `axiom/system-axioms.md`
   - `premise/ontology-premises.md`
   - `premise/system-premises.md`
3. Framework constitutions:
   - `constitution/framework/schema-amendment-discipline-constitution.md`
   - `constitution/framework/frontmatter-ownership-constitution.md`
   - `constitution/framework/edge-acyclicity-constitution.md`
   - `constitution/framework/governs-runtime-witness-constitution.md`
   - `constitution/framework/convicção-bet-ledger-constitution.md`
4. Graph indexes:
   - `graph-edges.md`
   - `graph-session-index.md`
5. Session notes only after the indexes identify a relevant provenance route.

## Ingest Guardrails

- Treat imported vault files as raw source evidence.
- Do not edit imported knowledge files during Inventory ingest.
- Do not promote imported definitions, constitutions, axioms, schemas, or
  ontology nodes by copying their text into canonical CyberAlchemy surfaces.
- Use Inventory evidence cards as read models only.
- If a term becomes a CyberAlchemy v2 primitive, route it to the owning
  governance capability and preserve this manifest as provenance.
