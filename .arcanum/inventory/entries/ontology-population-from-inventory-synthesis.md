---
tags: [inventory, ontology, ontology-lifecycle, promotion-record, evidence-card, evidence-set, authority, map-vs-decision, promotion-guardrail, build-from-owned, knowledge-promotion, synthesis]
node_type: synthesis
is_session: false
layer: knowledge-governance
nature: reference
status: candidate
created: 2026-06-30
sources:
  - .arcanum/inventory/schema.md
  - .arcanum/inventory/index.json
  - .arcanum/inventory/entries/evidence-sets/2026-06-18-dispersed-knowledge-sets.md
  - .arcanum/inventory/entries/evidence-sets/2026-06-21-ontology-lifecycle-authority-sets.md
  - .arcanum/inventory/entries/evidence-sets/2026-06-21-authority-node-relationship-taxonomy-sets.md
  - .arcanum/inventory/entries/evidence-sets/2026-06-23-scientific-authority-lifecycle-sets.md
  - .arcanum/inventory/entries/authority-ontology-governed-artifact-synthesis.md
  - .arcanum/inventory/entries/scientific-authority-lifecycle-synthesis.md
  - .arcanum/inventory/entries/cav2-ontology-authority-organizing-synthesis.md
  - .arcanum/inventory/entries/ontology-operationalization-in-the-machine-synthesis.md
  - .arcanum/ontology-vault/map-2026-06-18-dispersed-knowledge.md
  - projects/ontology/ARCHITECTURE.md
  - projects/ontology/research/2026-06-18-materialization-model/findings.md
  - projects/ontology/research/2026-06-18-inventory-evolution-efficiency/findings.md
---

# Populating Ontology From Inventory - Synthesis

Candidate Inventory synthesis answering: how should the current inventory be used
to populate ontology without collapsing lookup, meaning, and authority?

## Direct Answer

Populate ontology from Inventory by selecting source-backed claims, not by
mirroring files, folders, or index rows. The safe ladder is:

```text
source selector -> inventory evidence card / EvidenceSet -> ontology candidate
  -> PromotionRecord -> governed ontology node or projection -> generated read models
```

Inventory owns evidence capture, selector-level lookup, indexes, residue, and
handoff packets. Ontology Vault owns governed meaning, relation review,
confidence, branch maps, drift, and promotion reports. Authority and definitions
owners decide what counts. The ontology can model authority; it must not decide
authority by itself.

## What Gets Promoted Into Ontology

The ontology intake unit is a selected claim with evidence, not a whole source
file. A source file becomes ontology material only after a claim is selected and
carried through an evidence record, candidate node, and promotion gate.

A candidate ontology node should carry at least:

- `kind`
- `claim`
- `branchTarget`
- `status`
- `evidence`
- `confidence`
- `promotionGate` or `promotionRecord`
- `reviewOwner`
- `invalidation`
- `agentUse`

Anything that lacks those fields stays source material, an inventory evidence
card, an EvidenceSet, a decision stub, a projection, or another generated read
model. It is not an ontology node.

## First Population Run

Use a small witness slice before attempting broad migration:

1. Choose one source cohort and record its source manifest.
2. Extract 3-5 selector-level evidence cards with source refs, authority level,
   `promotion_owner`, trace, and residue.
3. Create an EvidenceSet only where repeated retrieval or handoff needs a stable
   group of cards.
4. Draft one thick `OntologyCandidate` from those cards.
5. Draft one `PromotionRecord` for that candidate, with `gateResult: block` until
   owner decisions and bridge evidence exist.
6. Add a governed projection or ontology-vault map that reads the candidate,
   rather than treating the candidate file itself as promoted truth.
7. Run context-builder or equivalent lookup proof to verify downstream agents can
   retrieve the right slice without reading the whole corpus.

This keeps ontology population build-from-owned: the existing Inventory,
Ontology Vault, PromotionRecord, and context-builder surfaces are enough for the
first proof. A primary graph substrate is not the current authority base. Use
bounded graph projections only when correctness depends on typed multi-hop
traversal, invalidation closure, contradiction blocking, branch comparison, or
promotion impact analysis.

## Current Inventory Lookup Handles

Use these candidate handles before searching raw files:

| Handle | Use |
| --- | --- |
| `evset-knowledge-governance-stack` | General inventory -> ontology -> governance boundary and source-to-candidate control loop. |
| `evset-caol-nonvacuity-witness-path` | Source evidence -> InventoryEvidence -> OntologyCandidate -> PromotionRecord fixture path. |
| `evset-authority-node-record-slice` | Current buildable authority-node slice as records/projections, not vault node-type mutation. |
| `evset-authority-node-schema-evolution-open-link` | Blocked/open schema-evolution packet for future authority movement or bridge-edge admission. |
| `evset-scientific-authority-lifecycle-provenance-relations` | Operational evidence -> inventory evidence -> ontology view -> owner decision -> pattern/invariant pressure. |
| `entries-authority-ontology-governed-artifact-synthesis` | Map-vs-decision rule: authority decides; ontology maps; governed artifacts are vehicles. |
| `entries-ontology-operationalization-in-the-machine-synthesis` | Machine-level guardrail: no modeling surface may hold a write edge to promotion status or authority. |
| `entries-cav2-ontology-authority-organizing-synthesis` | Ontology as structural model and authority as governance surface, including the instantiation/specializes residue. |

## Handoff Shape For Ontology Vault

A useful Inventory-to-Ontology packet should include:

- inventory index entry id and path,
- evidence-card ids and EvidenceSet ids,
- concrete source refs or selectors,
- selected claim,
- branch target hypothesis,
- confidence split if known,
- promotion owner,
- excluded nearby evidence and why it was excluded,
- residue or contradiction blockers,
- non-authority notice,
- proposed PromotionRecord id or decision gate.

The packet should say "candidate evidence for ontology review," not "ontology
truth." `governed_ref` should appear only after the downstream owner creates the
real governed artifact.

## Do Not Populate This Way

- Do not convert every Markdown file into a node.
- Do not treat `.arcanum/inventory/index.json` rows as ontology nodes.
- Do not treat EvidenceSets as promoted relations.
- Do not create a primary graph store just to make the model look ontological.
- Do not import CyberAlchemy Operational Ontology wholesale into a subject
  `run-view`; B3 content needs legal subject-run traces.
- Do not let branch-as-view, `specializes`, authority movement, or bridge edges
  become canonical without owner decisions and schema review.

## Open Residue

- Branch-as-view remains an owner decision before it becomes canonical.
- B3 `run-view` still needs a legal subject-runtime producer.
- Authority movement and bridge-edge schema admission remain open where current
  inventory handles mark them as schema-evolution packets.
- The write-authority proviso is still a code-level proof obligation: ontology
  modeling must remain unable to write promotion status.
- The current ontology population plan is design/report/fixture-level, not a
  deployed incremental ontology compiler.
