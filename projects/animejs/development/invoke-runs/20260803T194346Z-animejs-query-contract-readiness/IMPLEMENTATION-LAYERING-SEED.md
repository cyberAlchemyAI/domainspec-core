# Implementation Layering Seed

| Layer | Decision unlocked | Minimum slice | Deferred |
| --- | --- | --- | --- |
| L0 | Whether the query contract is closed, internally consistent, and migratable without rewriting history. | Schema, policy data, and migration note. | Executable replay. |
| L1 | Whether all eight terminal paths are deterministically accepted or rejected by one candidate validator. | Validator, fixtures, runner, and execution receipt. | Relation repair. |
| L2 | Whether candidate evidence remains trustworthy under integrated review and pre-session admission checks. | Integrated validation and readiness reports. | Ontology admission. |
| L3 | Whether the validated contract can be consumed by a separately governed knowledge-vault build. | Owner-confirmed Ontology Vault/Harness handoff. | Publication, deployment, release. |

Recommended next implementation layer after Plan: L0, but only after material-package admission and explicit SWU selection.
