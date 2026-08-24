# Cross-task Decisions

| ID | Decision | Basis |
| --- | --- | --- |
| D-001 | Use one `ConsultationBoundary` with a native-tool adapter first. | Smallest coherent unit and host fit. |
| D-002 | Keep model query separate from host-verified execution context. | Reviewer H1. |
| D-003 | Return a status-tagged union of mechanical evidence states. | Reviewer H2 and H5. |
| D-004 | Use atomic statements and a compiler manifest for provenance/freshness. | Reviewer H3 and H9. |
| D-005 | L0 uses a synthetic or target-local fixture; no consumer projection. | Private boundary and unresolved owners. |
| D-006 | Defer `traverse`, `compare`, `explain`, and HTTP until evidence selects one. | Reviewer H6 and layer value/cost. |

