# Cross-Task Gaps And Blockers

| ID | Type | Description | Affected scope | Owner | Repair path | Status |
| --- | --- | --- | --- | --- | --- | --- |
| HALP-B001 | blocker | Five human decision records are unresolved. | SWU 001–006, all later work | experiment/platform/resource owners | Execute SWU 001–005 sequentially with approval receipts. | open |
| HALP-B002 | blocker | Generator, provenance manifest, renderer, output grammar, scorer, and validation fixtures do not exist. | L0 witness | Task Session | SWU 006–010 after decisions. | open |
| HALP-B003 | blocker | Immutable checkpoint/template/runtime identities and compatibility evidence do not exist. | L1/L2 | platform owner | SWU 004 and 009. | open |
| HALP-B004 | blocker | Per-model/length resident-KV capacity evidence does not exist. | every long-bin run | platform owner | SWU 009; fail closed on fallback. | open |
| HALP-B005 | blocker | Single-H100 or equivalent authorized resource is not evidenced. | L1/L2 run | resource owner | Resource approval linked to SWU 011/012. | open |
| HALP-B006 | blocker | Numeric analysis rules and sample allocation are not approved. | L2 analysis | analysis owner | SWU 002. | open |
| HALP-B007 | blocker | Large run/evidence tracked-vs-ignored-vs-external storage policy is not selected. | run adapter and receipts | repository owner | SWU 005; document state namespaces. | open |
| HALP-B008 | blocker | Energy/cost measurement boundary is not approved. | resource frontier | resource owner | SWU 005. | open |
| HALP-B009 | blocker | License/publication boundary is not approved. | corpus and report publication | publication owner | SWU 005. | open |
| HALP-G001 | deferred | Oracle/retrieved arms lack a decision target. | optional L3 | experiment owner | Add only after L2 gate names decision value. | deferred |
| HALP-G002 | deferred | Phi/external-family comparator is not a replicate. | optional L3 | experiment owner | Separate external-comparator claim. | deferred |
| HALP-G003 | deferred | 128K is unadmitted. | optional L3 | platform owner | Exact fit and capacity witness. | deferred |
| HALP-G004 | deferred | Realistic T1 corpus and contamination policy are unset. | optional L3 | workload/publication owner | Dataset/license/contamination decision. | deferred |

## Gate Rule

An open blocker applies only to dependent work, but `workPackGateStatus` remains
`block` until the selected SWU's blockers are closed. Deferred gaps do not
authorize implementation.
