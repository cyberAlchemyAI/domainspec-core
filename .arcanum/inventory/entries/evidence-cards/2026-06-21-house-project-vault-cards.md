---
tags: [inventory, evidence-card, source-import, house-project-vault, cyberalchemy-v2, ontology-lifecycle, schema, classification, taxonomy, constitution-governance, definitions-governance, idempotency, ledger-spec, promotion-guardrail, evidence-backfill, open-question]
node_type: evidence-card
is_session: false
layer: knowledge-governance
nature: reference
status: candidate
created: 2026-06-21
dispatch_id: 2026-06-21-house-project-vault-import
dispatch_type: ingest
working_folder: .arcanum/inventory/queries/2026-06-21-house-project-vault-import/
sources: [cyberAlchemy-v2/authority/imports/house_project/docs/vault/]
---

# Evidence Cards - House Project Vault Import

Source dispatch: `2026-06-21-house-project-vault-import`

These cards make the imported house_project vault searchable for CyberAlchemy
v2. They are Inventory read models. They do not promote definitions,
constitutions, axioms, disciplines, ontology, schema, validators, or runtime
contracts.

## Subsequent CAV2 Authority Consumption

Definitions-governance and constitution-governance consumed this read model on
2026-06-21. The read model did not promote itself; the authority now lives in:

- `CAV2-D22` orthogonal classification
- `CAV2-D23` authority lifecycle axis
- `CAV2-D24` provenance-first navigation
- `CAV2-D25` schema amendment witness
- `CAV2-D26` append-only event ledger
- `cyberAlchemy-v2/authority/constitutions/VAULT-CONCEPT-ADOPTION-CONSTITUTION.md`
- `cyberAlchemy-v2/authority/definitions/source-clusters/house-project-vault.md`

Remaining source-local terms, including `veracidade`, `conviccao`, the source
node-type vocabulary, and source-local event catalog, are still not CAV2
authority unless separately re-authored.

## `house-vault-import-snapshot`

- ID: `house-vault-import-snapshot`
- Type: source
- Status: active
- Claim or candidate: The latest local `house_project/docs/vault/` snapshot was
  imported into CyberAlchemy v2 as private source evidence: 529 retained files,
  4.5M, from source commit
  `777c9b4b60e99e192986207bf0d75f53707ccb4b`, after excluding 21 source
  `.obsidian/` local app/plugin config files before parent publish.
- Source refs:
  - `cyberAlchemy-v2/authority/imports/house_project/IMPORT-MANIFEST.md`
  - `.arcanum/inventory/raw/manifests/2026-06-21-house-project-vault-import.md`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/agent-navigation.md:37`
- Authority level: imported source snapshot; not CyberAlchemy authority.
- Promotion owner: downstream owner for any accepted concept; Inventory owns
  only the read model and source manifest.
- Trace: Source path existed; `docs/vault/` had no dirty paths according to
  `git -C ../house_project status --short -- docs/vault`; snapshot was copied
  under `cyberAlchemy-v2/authority/imports/house_project/docs/vault/`, then
  `.obsidian/` local app/plugin state was excluded from the publishable import.
- Residue: Snapshot refresh policy is not automated. Re-run this route if the
  sibling vault changes.

## `house-vault-orthogonal-ontology-basis`

- ID: `house-vault-orthogonal-ontology-basis`
- Type: concept
- Status: candidate
- Claim or candidate: The imported vault has a mature source cluster for
  orthogonality as an ontology/classification constraint: labels should be
  statistically independent, new labels/nodes must add unique information, and
  the admission test is grounded in mutual information and retrieval entropy.
- Source refs:
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/ontology-conventions.md:20`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/ontology-conventions.md:293`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/ontology-conventions.md:384`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/axiom/ontology-axioms.md:42`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/axiom/ontology-axioms.md:67`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/axiom/ontology-axioms.md:104`
- Authority level: candidate source evidence for definitions-governance and
  constitution-governance; not promoted.
- Promotion owner: `definitions-governance` for terms; `constitution-governance`
  for hard action rules; `ontology-vault` for any ontology adoption.
- Trace: Root conventions, ontology axioms, and ontology premises all converge
  on orthogonal labels, retrieval entropy, unique-node admission, and adaptive
  classification.
- Residue: Need a CyberAlchemy v2 mapping between this source's 7-label system
  and CAV2 four-facet action method before adoption.

## `house-vault-authority-lifecycle-and-confidence`

- ID: `house-vault-authority-lifecycle-and-confidence`
- Type: workflow
- Status: candidate
- Claim or candidate: The imported vault separates document role from maturity
  and confidence: `node_type` names epistemic role, `status` names maturity,
  `veracidade` names evidence, and `conviccao` names commitment. This is direct
  precedent for CyberAlchemy authority lifecycle and multiple-provenance
  handling.
- Source refs:
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/ontology-conventions.md:175`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/ontology-conventions.md:197`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/premise/ontology-premises.md:61`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/premise/ontology-premises.md:75`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/confidence-levels.md:32`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/ontology-architecture-draft.md:37`
- Authority level: candidate lifecycle evidence; not a CAV2 status model.
- Promotion owner: `ontology-vault`, `definitions-governance`,
  `constitution-governance`, and `decision-gate`.
- Trace: The vault's confidence and maturity material aligns with prior
  CyberAlchemy questions about multiple provenances, authority types, and
  promotion gates.
- Residue: House terms `veracidade` and `conviccao` need a CAV2 decision:
  preserve, translate, or treat as source-local axes.

## `house-vault-provenance-navigation-indexes`

- ID: `house-vault-provenance-navigation-indexes`
- Type: implementation-pattern
- Status: candidate
- Claim or candidate: The vault has agent navigation rules and generated graph
  indexes that reduce search cost: start at constitutions, use frontmatter
  tags, treat sessions as provenance, respect status, traverse `derives-from`,
  and use edge/session indexes before opening many files.
- Source refs:
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/agent-navigation.md:41`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/agent-navigation.md:55`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/agent-navigation.md:64`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/agent-navigation.md:78`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/graph-edges.md:12`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/graph-session-index.md:12`
- Authority level: candidate inventory/search precedent.
- Promotion owner: `inventory`, `ontology-vault`, and `context-builder`.
- Trace: The root navigation doc explicitly tells agents not to read the vault
  linearly; graph indexes give concrete selector-level lookup surfaces.
- Residue: CAV2 can adopt the search discipline without adopting the same node
  schema; a bridge mapping is still needed.

## `house-vault-ledger-idempotency-event-rules`

- ID: `house-vault-ledger-idempotency-event-rules`
- Type: dependency-rule
- Status: candidate
- Claim or candidate: The event-system constitution gives strong operational
  precedent for append-only ledger rules, registered event catalogs, stream
  hierarchy, idempotency via `event_key`, deterministic entity identity, and
  dictionary-backed event semantics.
- Source refs:
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/constitution/event-system-constitution.md:54`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/constitution/event-system-constitution.md:79`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/constitution/event-system-constitution.md:134`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/constitution/event-system-constitution.md:268`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/constitution/event-system-constitution.md:401`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/constitution/event-system-constitution.md:423`
- Authority level: candidate operational precedent; not CAV2 ledger authority.
- Promotion owner: `constitution-governance`, `definitions-governance`,
  `experiment-harness`, and implementation owners.
- Trace: Event rules instantiate several CAV2-relevant primitives already under
  discussion: append-only history, idempotent retries, typed catalog membership,
  stream/lifecycle identity, and semantic dictionary linkage.
- Residue: Need to separate business-specific event rules from project-agnostic
  CyberAlchemy ledger primitives.

## `house-vault-schema-amendment-runtime-witness`

- ID: `house-vault-schema-amendment-runtime-witness`
- Type: dependency-rule
- Status: candidate
- Claim or candidate: The imported framework constitutions contain reusable
  governance mechanisms for schema evolution and enforcement: schema amendment
  ledgers, single frontmatter owner, acyclic justification edges, runtime
  witness declarations, and conviccao bet ledgers.
- Source refs:
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/constitution/framework/schema-amendment-discipline-constitution.md:20`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/constitution/framework/schema-amendment-discipline-constitution.md:35`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/constitution/framework/frontmatter-ownership-constitution.md:20`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/constitution/framework/edge-acyclicity-constitution.md:22`
  - `cyberAlchemy-v2/authority/imports/house_project/docs/vault/constitution/framework/convicção-bet-ledger-constitution.md:20`
- Authority level: candidate governance precedent; not adopted as CAV2
  constitutions.
- Promotion owner: `constitution-governance`, `ontology-vault`, and
  `decision-gate`.
- Trace: Framework constitutions appear as peer-copies or proposed adoption in
  the source vault, so they are especially useful as patterns but require
  explicit CAV2 acceptance before becoming rules.
- Residue: Some source statuses are `proposed`; do not treat those files as
  active authority without owner review.
