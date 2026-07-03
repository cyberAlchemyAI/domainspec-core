---
feature_code: DSD1
docType: traceability
status: draft
updatedAt: 2026-07-03
---

# Traceability: DS-D1 Improvement Plan

## Source To Task Mapping

| Source Signal | Plan Response | Tasks |
| --- | --- | --- |
| Backend 14 are shape/fixture-backed candidates. | Align maturity language before hardening. | TASK-DSD1-LEDGER, TASK-DSD1-BACKEND |
| UI 11 are endpoint-used but DS-D1 formation-deferred. | Gate UI authority behind owner decision. | TASK-DSD1-UI11 |
| Saga may need harden-or-collapse treatment. | Add Saga fork decision before mutation. | TASK-DSD1-SAGA |
| Some backend types need richer laws. | Add finite positive/negative examples and validator criteria. | TASK-DSD1-BACKEND, TASK-DSD1-VALIDATORS |
| Root authority should sit outside implementation. | Root definitions own authority; implementation receives only necessary views. | TASK-DSD1-LEDGER, TASK-DSD1-SYNC |
| Category laws matter but are not ready. | Defer full category law to a separate formalization route. | TASK-DSD1-VERIFY |

## Task To SWU Mapping

| Task | SWUs |
| --- | --- |
| TASK-DSD1-LEDGER | SWU-DSD1-001, SWU-DSD1-002 |
| TASK-DSD1-UI11 | SWU-DSD1-003, SWU-DSD1-004, SWU-DSD1-005, SWU-DSD1-006 |
| TASK-DSD1-SAGA | SWU-DSD1-007, SWU-DSD1-008, SWU-DSD1-009 |
| TASK-DSD1-BACKEND | SWU-DSD1-010, SWU-DSD1-011, SWU-DSD1-012 |
| TASK-DSD1-VALIDATORS | SWU-DSD1-013, SWU-DSD1-014 |
| TASK-DSD1-SYNC | SWU-DSD1-015 |
| TASK-DSD1-VERIFY | SWU-DSD1-016 |

## Recomposition Check

The plan is coherent only if these statements can all be true at closeout:

1. Root DS-D1 authority and implementation views agree.
2. DS-D8 relationship use does not silently promote DS-D1 types.
3. Every promoted or hardened type has human and machine evidence.
4. Every deferred category-law or UI/Saga branch remains visible as residue.
