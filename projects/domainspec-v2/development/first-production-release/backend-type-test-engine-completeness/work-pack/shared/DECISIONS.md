# Planning Decisions And Assumptions

| ID | State | Decision or assumption | Consequence |
| --- | --- | --- | --- |
| P-BTE-001 | resolved lane decision | Target all 13 active backend types and exclude UI. | Plan belongs to FPR-02B; FPR-02U is neither a blocker nor evidence. |
| P-BTE-002 | recommended default | Version the expanded profile instead of widening experimental profile v1 in place. | Existing four-kind evidence remains reproducible. |
| P-BTE-003 | accepted successor design | Keep one canonical JSON file per node, add one canonical JSON file per edge, and adapt node/edge bodies into shared YAML-backed criteria. | No conversion of consumer source files to generated instance YAML; generated graph remains read-only. |
| P-BTE-004 | authority rule | YAML criterion schemas own formation rules; JSON node schema owns the source envelope. | Do not hand-author nine duplicate formation rule sets. |
| P-BTE-005 | accepted scope rule | Exactly 16 backend relationship signatures are in the FPR-02B profile and require causal composition/removal evidence; UI/cross-layer signatures remain outside. | Edge schema, roots, resolver, traversal, composition, and negative controls are required. |
| P-BTE-006 | validation rule | `O_spec` must be frozen by a validation owner independently of engine output. | Engine cannot define its own completeness denominator. |

P-BTE-002 through P-BTE-006 are synchronized to DEC-FPR02-SUPPORTED-PROFILE. They remain plan/read-model decisions and do not authorize implementation, profile admission, or production.
