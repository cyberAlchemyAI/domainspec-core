# Ontologize — Definitions Index

Lookup layer for [DEFINITIONS.md](DEFINITIONS.md). One row per canonical term. Use the ID in
cross-references; keep wording in sync with the source file (drift check:
[DEFINITION-DRIFT-AUDIT.md](DEFINITION-DRIFT-AUDIT.md)).

| ID          | Term                       | Status            | One-line                                                                                              | Anchor |
|-------------|----------------------------|-------------------|-------------------------------------------------------------------------------------------------------|--------|
| DEF-ONT-001 | Ontology                   | candidate         | Explicit, governed model of what a company knows, with the evidence + decisions that make it trustworthy; requires branched + typed + edge-governed + evidence-graded + promotion-gated. | [↗](DEFINITIONS.md#def-ont-001--ontology--candidate-canonical) |
| DEF-ONT-002 | Ontology node              | candidate         | A single typed assertion: one instance of one of six node types (N1–N6), with identity, branch, and (for N3/N4/N6) `veracidade` + `evidence_refs`. | [↗](DEFINITIONS.md#def-ont-002--ontology-node--candidate-canonical) |
| DEF-ONT-003 | Ontology branch            | source-backed     | One of four independently governed facets — B1 meaning, B2 system, B3 run-context, B4 bridge — joined only by bridge edges. | [↗](DEFINITIONS.md#def-ont-003--ontology-branch--source-backed) |
| DEF-ONT-004 | Governed edge / edge catalog | seed            | A typed relation whose legality (source→target type, cardinality, inverse, category, acyclicity) is fixed by a single catalog table. | [↗](DEFINITIONS.md#def-ont-004--governed-edge--edge-catalog--seed) |

## Node-type quick reference (N1–N6)

| Node | Type                 | Primary branch | Evidence-bearing |
|------|----------------------|----------------|------------------|
| N1   | OutcomeEvent         | B2 system      | no (`source`)    |
| N2   | LifecycleState       | B3 run-context | no               |
| N3   | MetricObservation    | B3 run-context | yes              |
| N4   | PromotionCandidate   | B4 bridge      | yes              |
| N5   | OwnerDecision        | B4 bridge      | no               |
| N6   | KnowledgeProjection  | B1 meaning     | yes              |

## Related surfaces (not canonical authority)

- Layered load-bearing terms → [../DEFINITIONS.md](../DEFINITIONS.md)
- Client-facing glossary → [../GLOSSARY.md](../GLOSSARY.md)
- Branch mapping → [../ONTOLOGY-BRANCHES.md](../ONTOLOGY-BRANCHES.md)
- Node/edge/gate design → [../DAG-AND-METRICS.md](../DAG-AND-METRICS.md)
- Node schema → [../schemas/ontology-node.schema.json](../schemas/ontology-node.schema.json)
