# Execution Pack: Governed State Projection

## Wave Order

1. [W1 - L0 projection truth](work-pack/waves/W1-L0-projection-truth.md)
2. [W2 - L1 diff/action trust](work-pack/waves/W2-L1-diff-action-trust.md)
3. [W3 - L2 evidence semantics](work-pack/waves/W3-L2-evidence-semantics.md)

## Parallelization

- W1 is serial. `SWU-GSP-001` is the first and only selected executable unit.
- After W1 passes, `SWU-GSP-002` and `SWU-GSP-003` may run in parallel if their
  write scopes are kept disjoint.
- `SWU-GSP-004` can run in parallel with W2 only for the e2e helper change; its
  handoff semantics sub-slice should wait for diff/action receipts.
- `SWU-GSP-006` waits for L0-L2 receipts.

## Receipt Shape

Each task-session result should report:

```yaml
swu_id: SWU-GSP-001
result: pass | flag | block | interrupted
receipt_kind: task-session
receipt_artifact: <path or none>
files_touched:
  - <path>
validation:
  - <command/check and result>
blockers:
  - <blocker or none>
residue:
  - <residue or none>
reroute: <next owner or none>
handoff_note: <what the coordinator should do next>
```
