# Cross-Task Decisions

| Decision ID | Decision | Rationale | Applies To |
| --- | --- | --- | --- |
| DEC-RCI-001 | Use a local package staging root before external repo mutation. | Keeps private-parent evidence and shareable package content separate. | All tasks |
| DEC-RCI-002 | First executable unit is package skeleton, not schema copying or runtime behavior. | Prevents creating files without standalone identity. | W0, TASK-PACKAGE-BOUNDARY |
| DEC-RCI-003 | Use public-safe inventory evidence-card and `promotion_owner` language instead of private-only source names. | Preserves external handoff boundary. | TASK-CONTRACTS-VALIDATORS, TASK-ADAPTER-FIRST-SLICE |
| DEC-RCI-004 | Read-only observer/meter is a first runtime slice, not the first package slice. | Package identity must exist first. | W2 |
| DEC-RCI-005 | Host-side provider body is specified before implemented. | The ResonantOS seam is named but the body is absent from example code. | TASK-PROMOTION-BODY |
