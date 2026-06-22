# Cross-Task Gaps

| Gap | Affects | Handling |
| --- | --- | --- |
| GAP-ZRIG-COVERAGE-APPROVAL | readiness audit | Final coverage approval was pending in the product-mode review status. |
| GAP-ZRIG-OPERATOR-CONTRACT | F5/F6 | Live bridge and deploy/sentinel operator contracts need docs/checks. |
| GAP-ZRIG-DEPENDENCY-MANIFEST | F8 and all tests | Declare test/runtime deps before claiming command success. |
| GAP-ZRIG-REPRO-HARNESS | F1/F3/F9 | Focused regression tests should replace ad hoc repros as each SWU lands. |
| GAP-ZRIG-RECOMPOSITION-PACKET | public extraction | No public-safe extraction until product proofs and policy exist. |

Blocked evidence rule: when a command fails because the environment lacks declared dependencies, record it as F8. Do not mark the target SWU complete.
