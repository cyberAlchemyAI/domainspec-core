# Traceability

| Review Finding | Planned Repair | Primary SWU | Acceptance Evidence |
| --- | --- | --- | --- |
| AR-CAND-001 attribution | Kernel-created unattested operator action; no caller approver field. | 003, 008 | [SWU-IDEAD-008 evidence](../evidence/SWU-IDEAD-008.md): forged attribution rejects and UI copy says local operator action with unattested assurance. |
| AR-CAND-002 replay | Atomic pending-to-terminal transition inside serialized command boundary. | 002, 006 | sequential and concurrent replay yield one success and one receipt total. |
| AR-CAND-003 typestate | Explicit L0 disposition semantics; no false `running` claim. | 002, 005 | state-transition tests and later SPEC delta proposal. |
| AR-CAND-004 grants | Closed versioned vocabulary and normalization before persistence. | 003, 005 | unknown, duplicate, malformed, and reordered grant tests. |
| AR-CAND-005 singleton | ID-addressed envelope/approval collections and routes. | 002, 008 | [SWU-IDEAD-008 evidence](../evidence/SWU-IDEAD-008.md): two proposals remain selectable through pending and terminal history. |
| AR-CAND-006 divergence | Serialized commands, authoritative events, projection replay/reconciliation. | 006 | [SWU-IDEAD-006 evidence](../evidence/SWU-IDEAD-006.md): repeated races, restart repair, interruption recovery, and event/projection checksum equality pass. |
| AR-CAND-007 evidence | Exclusive materialized before/after/receipt artifacts and reference validation. | 007, 008 | [SWU-IDEAD-007 evidence](../evidence/SWU-IDEAD-007.md) proves bound files; [SWU-IDEAD-008 evidence](../evidence/SWU-IDEAD-008.md) exposes them through bounded UI links. |
| AR-CAND-008 schemas | Ajv Draft 2020-12 adapter enforced at ingress and egress. | 004, 005 | [SWU-IDEAD-005 evidence](../evidence/SWU-IDEAD-005.md): malformed requests/objects reject before event/artifact/state writes. |

## Browser Workflow Evidence

[SWU-IDEAD-009](../evidence/SWU-IDEAD-009.md) proves the recomposed Approval Desk in real Chromium at desktop and mobile viewports: two proposals remain navigable, approval is exact-once, rejection mints no receipt, reload preserves event-derived history, every evidence view matches bound IDs, keyboard focus is visible, layouts do not overlap, and browser console/page errors remain empty.

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
