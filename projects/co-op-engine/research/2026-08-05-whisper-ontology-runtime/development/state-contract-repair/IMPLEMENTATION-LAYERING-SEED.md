# Implementation layering seed

- L0 contract: closed enums, EV01-EV26 transition rules, EV22 guard.
- L1 proof: deterministic reducer/checker, positive/negative fixtures, live/replay/projection invariants.
- L2 research closeout: non-vacuity review, findings, auditor, closure and RESULT sync.
- L3 deferred owner work: ontology and proper runtime design/implementation outside this package.

The selected SWU spans L0-L1 because neither layer has independent acceptance: a written transition table without an executable proof leaves the original blocker unresolved, while a checker without the exact contract has no stable oracle.
