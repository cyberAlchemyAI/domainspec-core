# Traceability

| Requirement | Design component | SWU | Evidence |
| --- | --- | --- | --- |
| WEG-R1 evidence separation | evidence-axis recorder | 002 | [schema Task Session receipt](../session-evidence/SWU-WEG-002-RUN-001/receipt.json) and 16-case report |
| WEG-R2 deterministic status | admission evaluator | 003,005 | [status-ceiling receipt](../session-evidence/SWU-WEG-003-RUN-001/receipt.json) passes; generation admission remains 005 |
| WEG-R3 explicit approval | approval binder | 004 | ambient/digest-substitution controls |
| WEG-R4 composed first surface | profile + surface assembler | 006 | complete/incomplete role manifests |
| WEG-R5 comprehension envelope | binder + evidence recorder | 002,004 | schema shape passes in [SWU-WEG-002](../session-evidence/SWU-WEG-002-RUN-001/receipt.json); exact question/digest checks remain 004 |
| WEG-R6 post-apply verification | status evaluator | 003,004 | missing/blocked post-apply ceilings pass in [SWU-WEG-003](../session-evidence/SWU-WEG-003-RUN-001/receipt.json); prior-artifact binding remains 004 |
| WEG-R7 correction invalidation | correction ledger/reducer | 008 | append/replay test and signal |
| WEG-R8 retell/delta accountability | change manifest | 007 | unowned/rendered-retell controls |
| WEG-R9 reusable proof | Experiment Harness | 001, VERIFY | [fixture baseline receipt](../session-evidence/SWU-WEG-001-RUN-002/receipt.json); low/medium/complex live reports remain deferred |
| WEG-R10 safe packaging | local preset resolver | 009 | drift and privacy sweep |
