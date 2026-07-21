# Planning Decisions And Assumptions

| ID | State | Decision or assumption | Consequence |
| --- | --- | --- | --- |
| P-BTE-001 | resolved lane decision | Target all 13 active backend types and exclude UI. | Plan belongs to FPR-02B; FPR-02U is neither a blocker nor evidence. |
| P-BTE-002 | recommended default | Version the expanded profile instead of widening experimental profile v1 in place. | Existing four-kind evidence remains reproducible. |
| P-BTE-003 | accepted successor design | Keep one canonical JSON file per node, add one canonical JSON file per edge, and adapt node/edge bodies into shared YAML-backed criteria. | No conversion of consumer source files to generated instance YAML; generated graph remains read-only. |
| P-BTE-004 | narrowed by DEC-BTE-FORMATION-AUTHORITY-001 | YAML criterion schemas are the selected owner for a new versioned replacement; current-v1 JSON formation schemas remain governing declarations until explicitly retired through machine admission and migration proof. | Do not treat the current adapter as authority or change current v1 in place. |
| P-BTE-005 | accepted scope rule | Exactly 16 backend relationship signatures are in the FPR-02B profile and require causal composition/removal evidence; UI/cross-layer signatures remain outside. | Edge schema, roots, resolver, traversal, composition, and negative controls are required. |
| P-BTE-006 | validation rule | `O_spec` must be frozen by a validation owner independently of engine output. | Engine cannot define its own completeness denominator. |

P-BTE-002 through P-BTE-006 are synchronized to DEC-FPR02-SUPPORTED-PROFILE. They remain plan/read-model decisions and do not authorize implementation, profile admission, or production.

## Post-Audit Formation Decision

| ID | State | Decision | Consequence |
| --- | --- | --- | --- |
| `DEC-BTE-FORMATION-AUTHORITY-001` | accepted 2026-07-21 | Option 2: Design a distinct versioned YAML-owned formation replacement with explicit retirement of the four current-v1 JSON body schemas and compatibility/migration proof. | Invoke Design is unblocked. Current v1 stays frozen; no YAML replacement, JSON retirement, implementation, profile admission, SWU selection, or release promotion occurs from the decision record alone. |

Human record:
`../../decisions/DEC-BTE-FORMATION-AUTHORITY-001.md`

Machine decision receipt:
`../../decisions/DEC-BTE-FORMATION-AUTHORITY-001.json`
