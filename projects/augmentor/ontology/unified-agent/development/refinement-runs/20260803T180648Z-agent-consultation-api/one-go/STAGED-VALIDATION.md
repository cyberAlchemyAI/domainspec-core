# Staged validation

The complete seven-unit L0 frontier passed in an isolated temporary repository. The check applied the exact prepared materials in order and deleted the temporary repository afterward; it did not modify product bytes.

| Scope | Result | Evidence |
| --- | --- | --- |
| SWU-ACAPI-000 | pass | Ontology validator with zero violations, 6/6 ontology tests, 12/12 deterministic validator runs |
| SWU-ACAPI-001 | pass | Query contract: 2 valid and 4 intentionally invalid fixtures, zero failures |
| SWU-ACAPI-002 | pass | Result contract: 10 valid and 3 intentionally invalid fixtures, zero failures |
| SWU-ACAPI-003 | pass | Projection contract: 1 valid and 2 intentionally invalid fixtures, zero failures |
| SWU-ACAPI-004 | pass | Deterministic build/check, zero leakage hits, 3/3 projection tests |
| SWU-ACAPI-005 | pass | 4/4 limit and status tests |
| SWU-ACAPI-006 | pass | 17/17 consultation scenarios, then zero ontology violations and 6/6 ontology tests |
| Transition gate | pass | Exact joins admitted; tampered closeout bytes blocked |
| Approved-chain builder | pass | Exact epoch admitted; drifted epoch digest blocked |

Evidence ceiling: isolated candidate application. This does not prove approval, product execution, deployment, publication, release, L1 integration, or production readiness.
