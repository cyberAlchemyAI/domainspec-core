# Plan Technique Trace

| Technique | Applied to | Check |
| --- | --- | --- |
| `sequence` | units 000-006 | every non-first unit consumes the predecessor receipt |
| `scu_swu_reduction` | seven SWUs | each unit owns one primary behavior |
| `recomposition_proof` | Work Pack chain | complete generation or complete rollback |
| `validation_loop` | local and production gates | failure routes to repair or rollback |
| `owner_boundary_check` | DomainSpec, ResonantOS, production | writes stay with the selected owner |
| `handle_handoff` | candidate and receipts | exact refs cross boundaries, not private source prose |
| `residue_ledger` | G-03 to G-05 | every open item has an owner and route |
| `execution_receipt_handoff` | each Task Session step | structured receipt fields are mandatory |
| `concrete_path_evidence` | source and target inventories | no unresolved product glob authorizes mutation |
| `authority_split_gate` | local vs production | separate external-effect authorization |
| `protected_action_mapping` | remote switch and auth hash | exact protected action and fail behavior named |
| `artifact_contract_bridge` | neutral bundle to packager | seven-file runtime closure |
| `state_namespace_boundary` | candidate, consumer, remote, evidence | write policy per state root |
| `approval_semantics_map` | production gate | planning approval is not execution authorization |
| `observability_grouping` | dispatch | all future receipts share the dispatch id |

