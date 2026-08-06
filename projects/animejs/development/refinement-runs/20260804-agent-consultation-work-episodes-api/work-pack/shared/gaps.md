# Gap and Blocker Ledger

| ID | Effect | Owner | Required resolution |
| --- | --- | --- | --- |
| G-01 | blocks any source mutation | work-pack readiness owner | audit the immutable frontier and bind current target baselines |
| G-02 | blocks Task Session | user/dispatch owner | select exactly one SWU after readiness passes |
| G-03 | blocks non-loopback or consumer integration | consumer security/product owners | choose transport, auth, retention, deployment, and owner routes in a separate Work Pack |
| G-04 | blocks durable production store claims | persistence/data owners | select store and retention policy with atomicity evidence |
| G-05 | blocks Lesson creation | ontology Lesson-review owner | define candidate/verified Lesson admission separately |

G-01 and G-02 do not invalidate the authored Plan; they deliberately keep the
mutation handoff closed. G-03 through G-05 are outside the current delivery
boundary.

