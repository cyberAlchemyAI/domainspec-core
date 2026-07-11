# Traceability

| Review Finding | Planned Repair | Primary SWU | Acceptance Evidence |
| --- | --- | --- | --- |
| AR-CAND-001 attribution | Kernel-created unattested operator action; no caller approver field. | 003, 008 | forged `approved_by` ignored/rejected; UI copy makes no identity claim. |
| AR-CAND-002 replay | Atomic pending-to-terminal transition inside serialized command boundary. | 002, 006 | sequential and concurrent replay yield one success and one receipt total. |
| AR-CAND-003 typestate | Explicit L0 disposition semantics; no false `running` claim. | 002, 005 | state-transition tests and later SPEC delta proposal. |
| AR-CAND-004 grants | Closed versioned vocabulary and normalization before persistence. | 003, 005 | unknown, duplicate, malformed, and reordered grant tests. |
| AR-CAND-005 singleton | ID-addressed envelope/approval collections and routes. | 002, 008 | two pending proposals remain individually resolvable. |
| AR-CAND-006 divergence | Serialized commands, authoritative events, projection replay/reconciliation. | 006 | race and restart tests show event/projection equality. |
| AR-CAND-007 evidence | Exclusive materialized before/after/receipt artifacts and reference validation. | 007, 008 | every receipt ref resolves and is inspectable from UI. |
| AR-CAND-008 schemas | Ajv Draft 2020-12 adapter enforced at ingress and egress. | 004, 005 | malformed requests/objects reject before event/artifact/state writes. |

## Product Recomposition

```text
hostile evidence
  + exact-once ID lifecycle
  + honest closed contracts
  + recoverable event projection
  + resolvable evidence
  + restrained HTML controls
  + real browser proof
= local human-workable L0 Approval Desk
```
