# Dispatch Technique Trace

No governed multi-agent dispatch is used for Invoke authoring or experiment
execution. One repository-required bounded background helper performs a
read-only validator audit and returns a separate receipt.

| Technique | Applied boundary | Expected proof | Status |
| --- | --- | --- | --- |
| sequence | Define -> Design -> Plan -> Task Session | Every downstream stage consumes exact upstream artifacts | pass |
| owner_boundary_check | Craft authority, adapter, package/security, publication, destructive controls | No stage claims another owner's authority | pass |
| validation_loop | every WP/SWU | Exact positive or negative oracle and receipt | pass |
| retry_policy | package/build/verification failures | No implicit retry; new exact run only | pass |
| rollback_strategy | isolated store operations | Quarantine and rebuild a sibling; never edit YAML or repair in place | pass |
| partitioning | canonical Craft vs candidate experiment vs external receipts | Disjoint write and authority boundaries | pass |
| scu_swu_reduction | Work Pack decomposition | One independently reviewable behavior per SWU | pending Plan validation |
| recomposition_proof | SWU results -> experiment verdict | All receipts preserve claim ceiling and unresolved residue | pending Plan validation |
