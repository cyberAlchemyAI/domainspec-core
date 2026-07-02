# Fixture — Workflow (invalid: spans features → is a Saga)

Declared Workflow but `scope=cross-feature`. Expected: **REJECTED as Workflow**.

## Concept Registry
| Concept | Type |
| --- | --- |
| WireTransfer | Workflow |

## WireTransfer
| Attribute | Value |
| --- | --- |
| scope | cross-feature |
