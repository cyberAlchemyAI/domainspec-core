# States

## CapacityAdmissionDecision

| State | Meaning | Spawn actions emitted | Next route |
| --- | --- | ---: | --- |
| unassessed | no evidence evaluated | 0 | observe or block |
| blocked-missing | no evidence handle | 0 | acquire evidence or offer alternatives |
| blocked-stale | evidence expired or digest drifted | 0 | refresh evidence |
| blocked-unknown | provider cannot state usable capacity | 0 | revise, fresh-session handoff, or defer |
| blocked-insufficient | authoritative units are below requested width | 0 | offer revalidated topology choices |
| blocked-unsupported | requested policy, including reservation-required admission, has no admitted host/evaluator contract | 0 | use snapshot-only policy or defer for host extension |
| blocked-unreserved | future reservation-aware policy requires an absent/invalid lease | 0 | deferred L2 host-owner route |
| admitted | complete wave fits under the declared policy | exact requested width | compile persisted actions |

Terminal capacity decisions are immutable. A changed wave, policy, evidence
record, reservation, or user choice creates a new decision identity.

## SlotLifecycleObservation

| State | Proven meaning | May count as spawnable? |
| --- | --- | --- |
| active | host reports currently running/occupying | no |
| terminal-retained | work ended but host still retains the thread | unknown unless host says |
| reusable | host explicitly permits safe reuse under a named isolation contract | yes for reuse only, not fresh spawn |
| released | host explicitly proves physical capacity release | yes under the matching scope |
| unknown | host cannot classify physical effect | no authority to infer |

`agent_closed` is an Orchestrate logical event and does not transition this
state machine.
