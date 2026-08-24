# States and Effects

| State | Meaning | Allowed next state | Semantic effect |
|---|---|---|---|
| `draft` | source-bound proposal | reject, consult | none |
| `consultation_pending` | no current vault receipt | blocked, eligible | none |
| `consultation_blocked` | abstain/stale/denied/failure | reconsult, retire | none |
| `contradiction_quarantined` | a hard conflict is open | revise, owner-constrain, retire | none |
| `tournament_eligible` | hard gates pass | owner review | none |
| `owner_review_pending` | selection is not decided | select, reject, defer | none |
| `selected_for_plan` | planning is authorized | Task Session preflight | none |
| `task_session_admitted` | one SWU is authorized | execute or block | bounded product mutation only |
| `witness_executed` | local evidence exists | evaluate, retire | evidence append only |
| `subjectively_evaluated` | human judgment recorded | accept, reject, defer | none |
| `owner_accepted` | owner permits bounded reuse | later route | no ontology authority |
| `retired` | exact fingerprint will not be reused | new materially different candidate | none |

Source drift invalidates downstream candidates. Evidence revocation affects eligibility but never rewrites episode history. A new runtime, browser, image, timing, or candidate fingerprint creates a new witness identity.

