# Execution Pack

## Entry gate

No Task Session may start while `HANDOFF-STATE.json.selection_allowed` is false or the latest readiness report has `runtime_admission_status != pass`.

Even after admission passes, exactly one dependency-ready SWU requires explicit user selection. No-argument Task Session discovery must not infer selection from `ready_frontier`.

## Ordered execution graph

| Order | Step | SWU | Task | Layer/wave | Depends on | Successor |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | s1 | SWU-AKV-QRY-001 | POLICY | L0/W0 | none | QRY-002 |
| 2 | s2 | SWU-AKV-QRY-002 | SCHEMA | L0/W0 | QRY-001 receipt | QRY-003 |
| 3 | s3 | SWU-AKV-QRY-003 | MIGRATION | L0/W0 | QRY-002 receipt | QRY-004 |
| 4 | s4 | SWU-AKV-QRY-004 | VALIDATOR | L1/W1 | QRY-003 receipt | QRY-005 |
| 5 | s5 | SWU-AKV-QRY-005 | REPLAY | L1/W1 | QRY-004 receipt | none |

## Per-unit lifecycle

1. resolve one explicit SWU;
2. build fresh strict Context Builder session evidence;
3. revalidate dependency receipts and final Plan snapshot;
4. verify current material package/producer receipt and exact write union;
5. persist mutation-admission receipt;
6. apply admitted material bytes only;
7. run the exact command matrix;
8. reconcile writes;
9. emit canonical governance receipt plus package terminal projection;
10. dispatch and join exact Invoke Refresh closeout;
11. expose but never execute the unique successor.

## Runtime and write policy

- runtime: local Codex with exact tool identity captured at admission;
- network: forbidden;
- browser: not applicable;
- new package root or dependency: forbidden;
- destructive cleanup: forbidden;
- publication/ontology paths: forbidden.

## Current execution state

- plan contract: authored pass, independent audit pending;
- runtime admission: block because material packages and producer receipts do not exist;
- selected SWU: none;
- next route: Work Pack Readiness Audit, not Task Session.
