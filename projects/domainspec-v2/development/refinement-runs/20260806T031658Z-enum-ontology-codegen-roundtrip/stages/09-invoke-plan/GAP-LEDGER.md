---
artifact_kind: plan-gap-ledger
status: no-current-blocker
authority_effect: none
---

# Gap Ledger

| Gap | Acceptance impact now | Owner | Repair/next route |
|---|---|---|---|
| concrete `OrderStatus` is a candidate fixture, not canonical domain authority | bounded by claim ceiling; not a blocker for prototype proof | future canonical-definition owner | replace snapshot authority reference in a later owner-issued run |
| legacy adapter accepts caller-supplied `expectedValues` | blocks reuse as the new expectation path; owned by SWU-ARE-009 | TypeScript adapter owner | add no-expectations entry point without breaking legacy tests |
| composition requires relation and alias evidence | outside direct first unit | ontology/profile plus adapter owners | follow-up design after SWU-ARE-014 |
| Python/Rust realization not planned here | outside selected TypeScript unit | language owners | new Work Packs reusing validated portable contracts |
| checked-in generated-source policy is undecided | no effect on isolated proof | product/source owner | decision gate after first proof |
| no current implementation receipt exists | expected at `selection-ready`, not a plan defect | implementation-readiness then Task Session | select one SWU only when execution is explicitly requested |

There is no open acceptance-critical planning blocker. A failed live validation,
ontology insufficiency, or required scope expansion becomes a terminal blocker at
execution time.
