---
tags: [inventory, authority-node, authority-harness, authority-movement, promotion-record, ontology-vault, bridge-edge, relationship-invariant, promotion-guardrail, evidence-backfill, open-question]
node_type: evidence-set
is_session: false
layer: architecture
nature: reference
status: candidate
created: 2026-06-21
dispatch_id: 2026-06-21-authority-node-relationship-taxonomy
dispatch_type: research
working_folder: cyberAlchemy-v2/development/research/2026-06-21-authority-node-relationship-taxonomy/
sources: [.arcanum/inventory/entries/evidence-cards/2026-06-21-authority-node-relationship-taxonomy-cards.md, .arcanum/inventory/entries/evidence-cards/2026-06-21-authority-harness-ledger-ontology-cards.md]
---

# EvidenceSets - Authority Node Relationship Taxonomy

Source dispatch: `2026-06-21-authority-node-relationship-taxonomy`
Source artifacts:
- `cyberAlchemy-v2/development/research/2026-06-21-authority-node-relationship-taxonomy/research.md`
- `cyberAlchemy-v2/development/research/2026-06-21-authority-node-relationship-taxonomy/findings.md`

EvidenceSets are candidate Inventory read models. They group evidence-card IDs
for repeated lookup and handoff assembly. They do not imply ontology,
definition, constitution, ledger, or Context Builder authority.

## `evset-authority-node-record-slice`

- Status: candidate
- Evidence cards:
  - `authority-node-deflated-surface-boundary`
  - `authority-relation-catalog-record-only`
  - `authority-workflow-confidence-axis-split`
  - `authority-harness-typed-hole-contract`
  - `authority-harness-extend-not-author`
- Inclusion reasons: Supports the next buildable slice: authority type and posture as owned envelope/profile values, record-level relation fields with CAV2-D16 metadata, typed-hole contract extension where the owner surface exists, and projection-only ontology references.
- Excluded card refs:
  - `authority-node-schema-evolution-boundary`: schema-evolution only, not buildable as a current implementation slice.
  - `ledger-ontology-bridge-edge-kill-until-amendment`: bridge-edge work remains a separately gated amendment.
- Handoff target: `sigil-development`, `definitions-governance`, `constitution-governance`, and `ontology-vault`.
- Synthesis note: Use this set when a future task needs the authority-node relationship taxonomy without mutating the ontology vault. It permits record/projection implementation work and blocks direct vault-node or vault-edge additions.
- Index terms: `authority-node`, `authority-type`, `authority-posture`, `lifecycle-envelope`, `owner-profile`, `PromotionRecord`, `record-relation`, `ontology_refs`, `CAV2-D16`, `promotion-guardrail`.
- Residue: PromotionRecord generalization ownership and the authority movement ledger validator remain unsettled.

## `evset-authority-node-schema-evolution-open-link`

- Status: open-question
- Evidence cards:
  - `authority-node-schema-evolution-boundary`
  - `ledger-ontology-bridge-edge-kill-until-amendment`
  - `authority-relation-catalog-record-only`
- Inclusion reasons: Isolates the blocked schema choices for future ontology-vault edge or node-type changes.
- Excluded card refs:
  - `authority-node-deflated-surface-boundary`: this is the current record-surface decision, not itself a schema-evolution change.
- Handoff target: `ontology-vault`, `constitution-governance`, and `decision-gate`.
- Synthesis note: Treat this as a decision packet seed, not an implementation task. The useful question is which schema-evolution route, if any, should admit authority movement or promotion-event material into the vault.
- Index terms: `schema-evolution`, `authority-node`, `promotion-event`, `movement`, `node_type`, `bridge-edge`, `forward-only`, `inverse`, `CAV2-D16`.
- Residue: No amendment has been selected; bridge edge remains KILL-until-amendment.
