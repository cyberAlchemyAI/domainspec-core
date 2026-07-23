# Agent reasoning engine execution pack

Status: **planned; no execution authorization**

## Dependency flow

```text
owner policy records
       |
       v
W0: evaluator@1 witness
       |
       v
W1: governed inputs + actor protocol --------+
       |                   |
       +-> immutable replay|
       v                   v
W2: gates/effort + current revalidation + durability/governance
       |
       v
W3: private packaging and controlled rollout
```

Waves are sequential because every later layer consumes prior evidence. Within
W1, journal transition work and observation-transport design may be prepared in
parallel but join before validation. Within W2, durability and failure-injection
fixtures may run in parallel after current-revalidation semantics are fixed.

## Wave contracts

- [`W0-L0.md`](work-pack/waves/W0-L0.md): owner policies then one evaluator SWU.
- [`W1-L1.md`](work-pack/waves/W1-L1.md): bounded protocol and immutable replay.
- [`W2-L2.md`](work-pack/waves/W2-L2.md): drift, durability, degraded behavior.
- [`W3-L3.md`](work-pack/waves/W3-L3.md): private packaging and rollout evidence.

## Synchronization rules

1. A downstream wave consumes terminal receipts and exact artifact digests, not
   prose summaries.
2. Failed or partial lanes remain visible to joins and later owner gates.
3. No worker may edit an upstream receipt or reinterpret its verdict.
4. One SWU is handed off at a time; unknown or unselected SWU IDs block.
5. The parent verifies every claimed test and write scope before work-pack state
   changes.
6. Promotion, public publication, and real effects require separate routes.

## Expected SWU result

```yaml
swu_id: SWU-ARE-NNN
result: pass | flag | block | interrupted
capability_ref: task-session | goal | manual-owner
receipt_kind: native-stage | subagent | local-fallback | blocked
receipt_artifact: path | none
files_touched: []
validation: []
blockers: []
residue: []
reroute: string | none
handoff_note: string
```

## Stop boundary

This pack is a future handoff description only. The current dispatch must not
invoke Task Session, goal, implementation workers, external effects, or public
packaging.
