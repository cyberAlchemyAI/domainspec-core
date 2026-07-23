# Traceability

| Requirement | Finding | Task/SWU | Design component | Closure evidence |
| --- | --- | --- | --- | --- |
| WFE-R01 | TS-1 | TASK-002 / SWU-002 | Task Session decision/completion guard | [critical validation and auto-choice receipt](../session-evidence/SWU-WFE-002/receipt.json) |
| WFE-R02 | TS-2 | TASK-005 / SWU-005 | routed readiness consumer | [receipt match/mismatch receipt](../session-evidence/SWU-WFE-005/receipt.json) |
| WFE-R03 | INV-1 | TASK-003 / SWU-003A,003B | material-package validator | [validator receipt](../session-evidence/SWU-WFE-003A/receipt.json); [integration receipt](../session-evidence/SWU-WFE-003B/receipt.json) |
| WFE-R04 | INV-2 | TASK-010 / SWU-010 | status resolver | [three-axis mode receipt](../session-evidence/SWU-WFE-010/receipt.json) |
| WFE-R05 | DSS-1 | TASK-001 / SWU-001 | dispatch admission validator | [appender red/green receipt](../session-evidence/SWU-WFE-001/receipt.json) |
| WFE-R06 | DSS-2 | TASK-007 / SWU-007A,007B | dispatch evidence binder | [sheet substitution receipt](../session-evidence/SWU-WFE-007A/receipt.json); [overlay parity receipt](../session-evidence/SWU-WFE-007B/receipt.json) |
| WFE-R07 | DG-1 | TASK-006 / SWU-006A,006B | option/override validator | [option cardinality receipt](../session-evidence/SWU-WFE-006A/receipt.json); [override replay receipt](../session-evidence/SWU-WFE-006B/receipt.json) |
| WFE-R08 | INT-1 | TASK-004 / SWU-004A,004B | kind reconciler | [15→0 migration receipt](../session-evidence/SWU-WFE-004A/receipt.json); [producer guard receipt](../session-evidence/SWU-WFE-004B/receipt.json) |
| WFE-R09 | INT-2 | TASK-009 / SWU-009 | projection validator | [bidirectional conformance receipt](../session-evidence/SWU-WFE-009/receipt.json) |
| WFE-R10 | WH-1 | TASK-008 / SWU-008A,008B | runtime assembler | [manifest receipt](../session-evidence/SWU-WFE-008A/receipt.json); [parity/regeneration receipt](../session-evidence/SWU-WFE-008B/receipt.json) |

Completion requires one accepted finding, one current target witness, one
negative control, one positive control, and one lifecycle-owner receipt per row.

Terminal recomposition: [TASK-WFE-VERIFY final audit](../session-evidence/TASK-WFE-VERIFY/FINAL-AUDIT.md).
