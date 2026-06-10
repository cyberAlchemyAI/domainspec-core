# Ontologize — Definition Drift Audit

Drift check for the canonical [DEFINITIONS.md](DEFINITIONS.md) against the rest of the project.
Produced under `definitions-governance` step 8 (downstream drift). Re-run whenever a canonical
term or a downstream surface changes.

**Scope.** Conflicting wording · stale anchors · undefined critical terms · narrative text that
redefines authority · missing references.

## Findings

| # | Surface checked | Finding | Severity | Recommended action |
|---|-----------------|---------|----------|--------------------|
| D1 | [../GLOSSARY.md](../GLOSSARY.md) "Ontology [generic]" | Two definitions of "ontology" now coexist: the client-facing generic gloss and canonical DEF-ONT-001. **Not a conflict** — DEF-ONT-001 explicitly frames the glossary entry as the weaker client-facing pitch and itself as the stronger contract. | info | Add a back-reference from GLOSSARY "Ontology" to DEF-ONT-001 so readers know the canonical sense exists. (Not done here — GLOSSARY is the feature-glossary surface; defer to its owner.) |
| D2 | [../DAG-AND-METRICS.md §2](../DAG-AND-METRICS.md) node types | N1–N6 node-type set and `veracidade`/`evidence_refs` fields match DEF-ONT-002 exactly. Schema [../schemas/ontology-node.schema.json](../schemas/ontology-node.schema.json) is the machine form. | none | None — aligned. |
| D3 | [../ONTOLOGY-BRANCHES.md](../ONTOLOGY-BRANCHES.md) | Branch set B1–B4 and the run-context rename match DEF-ONT-003. | none | None — aligned. |
| D4 | [../DEFINITIONS.md](../DEFINITIONS.md) (layered) | The root file defines layered product terms (two-axis ontology, card primitive, etc.), not the word "ontology" itself. No collision; the two files are complementary layers. | info | Optionally add a one-line pointer in the root DEFINITIONS.md header to `definitions/` for the canonical sense. |
| D5 | Branch ↔ node-type assignment | DEF-ONT-002's "primary branch" column is a **new mapping** not previously stated as a 1:1 in DAG-AND-METRICS (which maps branches→DAGs, not node-types→branches). It is consistent with the branch→DAG mapping but is an interpretation. | low | Mark the primary-branch column as candidate; confirm against the engine spec (ENGINE.md) in assessment. |

## Undefined-but-load-bearing terms surfaced

- **`record_kind`** — used as a gate (`= promotion_record` on N6) but defined only inline in
  DAG-AND-METRICS §4. _Candidate for a future DEF entry if it recurs in client artifacts._
- **`approved_allowed_uses` / `proposed_allowed_uses`** — load-bearing for the promotion gates;
  currently defined only by the GoldenQuill rules. _Candidate for a future DEF entry._

## Authority guardrail

- These definitions are **candidate** project-canonical. No promotion to canonical Arcanum or
  CyberAlchemy vocabulary, and no client-facing commitment, without an explicit owner-review
  route. GoldenQuill source remains read-only.
