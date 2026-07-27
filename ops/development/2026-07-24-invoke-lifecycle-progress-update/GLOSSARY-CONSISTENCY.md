# Glossary Consistency

Status: pass

## Checks

| Check | Result |
| --- | --- |
| authored validity is not used as readiness | pass |
| execution epoch always identifies exactly one selected SWU | pass |
| epoch control digest includes every same-epoch control category | pass |
| byte drift and change impact remain distinct | pass |
| producer, producer validator, and consumer remain distinct roles | pass |
| `complete` is qualified as execution, closeout, or epoch terminal | pass |
| progress is derived only from admitted transitions | pass |
| Inventory, observability, projections, status, and cursors remain non-authority | pass |
| `plan_repair` cannot preserve an epoch after a control change | pass |
| candidate terms are not claimed canonical | pass |

## Public/private check

The design vocabulary is generic. Private project witnesses are referenced only
as private source evidence and are not copied into proposed public wording,
schemas, or fixture names.

