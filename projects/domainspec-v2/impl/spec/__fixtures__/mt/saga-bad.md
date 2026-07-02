# Fixture — Saga (invalid: single feature → is a Workflow)

Declared Saga but `scope=intra-feature`. Expected: **REJECTED as Saga**.

## Concept Registry
| Concept | Type |
| --- | --- |
| OrderFulfillment | Saga |

## OrderFulfillment
| Attribute | Value |
| --- | --- |
| scope | intra-feature |
