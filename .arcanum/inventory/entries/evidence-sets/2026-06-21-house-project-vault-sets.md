---
tags: [inventory, evidence-set, source-import, house-project-vault, cyberalchemy-v2, ontology-lifecycle, schema, classification, constitution-governance, definitions-governance, idempotency, ledger-spec, promotion-guardrail, evidence-backfill]
node_type: evidence-set
is_session: false
layer: knowledge-governance
nature: reference
status: candidate
created: 2026-06-21
dispatch_id: 2026-06-21-house-project-vault-import
dispatch_type: ingest
working_folder: .arcanum/inventory/queries/2026-06-21-house-project-vault-import/
sources: [.arcanum/inventory/entries/evidence-cards/2026-06-21-house-project-vault-cards.md]
---

# EvidenceSets - House Project Vault Import

EvidenceSets are candidate Inventory read models. They group evidence-card IDs
for repeated lookup and handoff assembly. They do not imply definition,
constitution, axiom, discipline, ontology, schema, validator, or Context Builder
authority.

## `evset-house-vault-definition-seed`

- Status: candidate
- Evidence cards:
  - `house-vault-orthogonal-ontology-basis`
  - `house-vault-authority-lifecycle-and-confidence`
  - `house-vault-provenance-navigation-indexes`
- Inclusion reasons: Supports definitions-governance searches for
  orthogonality, taxonomy/classification, ontology, provenance, confidence, and
  authority lifecycle terms.
- Excluded card refs:
  - `house-vault-ledger-idempotency-event-rules`: more operational than
    definitional.
  - `house-vault-schema-amendment-runtime-witness`: better routed to
    constitution-governance.
- Handoff target: `definitions-governance`, `ontology-vault`, and
  `context-builder`.
- Synthesis note: Use this set to compare CyberAlchemy v2 primitive definitions
  against the imported vault's ontology-language cluster.
- Index terms: `orthogonality`, `retrieval entropy`, `classification`,
  `taxonomy`, `status`, `veracidade`, `conviccao`, `session provenance`,
  `derives-from`, `graph traversal`
- CAV2 authority consumption: selected terms are mapped through `CAV2-D22`,
  `CAV2-D23`, and `CAV2-D24`; source-local status and confidence vocabulary
  remains unpromoted.
- Residue: Primordial `orthogonality` and the source-local status/confidence
  terms still need separate decisions before becoming canonical.

## `evset-house-vault-constitution-lifecycle-seed`

- Status: candidate
- Evidence cards:
  - `house-vault-authority-lifecycle-and-confidence`
  - `house-vault-schema-amendment-runtime-witness`
  - `house-vault-ledger-idempotency-event-rules`
- Inclusion reasons: Supports constitution-governance searches for schema
  amendment discipline, runtime witness, event/ledger governance, idempotency,
  maturity lifecycle, and promotion gates.
- Excluded card refs:
  - `house-vault-import-snapshot`: source-scoping evidence, not a lifecycle
    mechanism.
  - `house-vault-provenance-navigation-indexes`: search-supporting, not
    enforcement-supporting.
- Handoff target: `constitution-governance`, `discipline-governance`, and
  `decision-gate`.
- Synthesis note: Use this set when drafting CAV2 action constitutions, schema
  amendment rules, and ledger/event-style invariants.
- Index terms: `schema amendment`, `runtime witness`, `frontmatter owner`,
  `acyclic edges`, `bet ledger`, `append-only ledger`, `idempotency`,
  `deterministic identity`, `event catalog`
- CAV2 authority consumption: selected governance patterns are mapped through
  `CAV2-D25`, `CAV2-D26`, and
  `cyberAlchemy-v2/authority/constitutions/VAULT-CONCEPT-ADOPTION-CONSTITUTION.md`.
- Residue: Several source constitutions are proposed or source-local; source
  event catalogs and validators still need owner review before adoption.

## `evset-house-vault-search-shortcut`

- Status: candidate
- Evidence cards:
  - `house-vault-import-snapshot`
  - `house-vault-provenance-navigation-indexes`
  - `house-vault-orthogonal-ontology-basis`
- Inclusion reasons: Gives future agents the shortest route into the imported
  vault without opening 474 conversation files.
- Excluded card refs:
  - `house-vault-ledger-idempotency-event-rules`: relevant after a ledger/event
    query is already selected.
- Handoff target: `inventory`, `context-builder`, `ontology-vault`.
- Synthesis note: Start with this set when the user says to search the house
  vault for definitions, constitutions, ontology, graph, or provenance.
- Index terms: `house_project vault`, `source import`, `agent-navigation`,
  `graph-edges`, `graph-session-index`, `constitution-first`,
  `sessions as provenance`
- Residue: No automated lookup tool points at this imported snapshot yet; use
  Inventory index and shell search for now.
