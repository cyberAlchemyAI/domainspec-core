---
tags: [inventory, authority-harness, ledger-spec, authority-movement, promotion-record, ontology-vault, bridge-edge, promotion-guardrail, evidence-backfill, open-question]
node_type: evidence-set
is_session: false
layer: architecture
nature: reference
status: candidate
created: 2026-06-21
dispatch_id: 2026-06-21-authority-harness-ledger-ontology-unification
dispatch_type: research
working_folder: cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/
sources: [.arcanum/inventory/entries/evidence-cards/2026-06-21-authority-harness-ledger-ontology-cards.md, .arcanum/inventory/entries/evidence-cards/2026-06-21-ontology-lifecycle-authority-cards.md]
---

# EvidenceSets - Authority-Harness / Ledger / Ontology Unification

EvidenceSets are candidate Inventory read models. They group evidence-card IDs
for repeated lookup and handoff assembly. They do not imply ontology,
definition, constitution, ledger, or Context Builder authority.

## `evset-authority-harness-build-slice-1`

- Status: candidate
- Evidence cards:
  - `authority-harness-extend-not-author`
  - `authority-harness-typed-hole-contract`
  - `ledger-spec-axis-selector`
  - `authority-workflow-vs-maturity-status-placement`
  - `caol-lifecycle-envelope-contract`
- Inclusion reasons: These cards jointly capture the buildable-today slice —
  extend the existing lifecycle envelope (cross-referenced from the sibling
  CAOL card) with the typed-hole `validate_and_promote` contract, add the
  `ledger_spec_axis` tag, build the missing append-only authority-ledger
  validator, read the signals JSONL schema, and record the workflow-vs-maturity
  placement as a conventions-amendment.
- Excluded card refs:
  - `ledger-ontology-bridge-edge-kill-until-amendment`: the bridge edge is gated
    behind a schema-evolution amendment and is not buildable in slice 1; it
    belongs to the open-link set.
- Handoff target: sigil-development (envelope extension + ledger-spec authoring),
  definitions-governance and constitution-governance (per-kind judgment
  profiles), register-dispatch owner (validator), decision-gate (cut line).
- Synthesis note: This set supports the claim that the cycle closes by assembling
  owned parts plus one net-new typed-hole contract; it does NOT support authoring
  a parallel harness object.
- Index terms: `authority-harness`, `lifecycle-envelope`, `typed-hole`,
  `validate_and_promote`, `ledger_spec_axis`, `promotion-record`,
  `workflow-vs-maturity`, `extend-owned`, `promotion-guardrail`
- Residue: The envelope itself is a candidate contract; no profile validators or
  the append-only authority-ledger validator are written; signals schema unread.

## `evset-ledger-ontology-open-link`

- Status: open-question
- Evidence cards:
  - `ledger-ontology-bridge-edge-kill-until-amendment`
  - `ledger-spec-axis-selector`
- Inclusion reasons: These cards isolate the single open link of the ontology
  tie — the node→promotion-record forward-only movement/bridge edge that the
  current ontology constitution cannot express — together with the append-only
  ledger dialect whose events the bridge would project.
- Excluded card refs:
  - `authority-harness-typed-hole-contract`: the typed-hole contract is buildable
    today and is independent of the bridge-edge amendment.
  - `authority-workflow-vs-maturity-status-placement`: a conventions-amendment
    that does not depend on the bridge-edge gate.
- Handoff target: ontology-vault and constitution-governance through the
  schema-evolution gate; decision-gate to choose amendment option A (third
  forward-only carve-out) vs option B (`promotion-event` node_type + lawful
  inverse).
- Synthesis note: This set marks the ontology-tie cycle as non-closing today and
  names the exact amendment that would close it. It is a gated slice-2 decision,
  not a build task.
- Index terms: `bridge-edge`, `movement-edge`, `forward-only`, `carve-out`,
  `node_type`, `schema-evolution-gate`, `OQ-C`, `OQ-6`, `typed-projection`,
  `open-question`
- Residue: No chosen amendment; promotion atomicity (OQ-6) is itself still Open,
  so the ledger-as-ontology identity would assert atomicity the repo lacks.
