# Implementation layering

| Layer | Owned outcome | Inputs | Outputs | Gate |
| --- | --- | --- | --- | --- |
| L0 contract | exact closed state vocabulary and 26-event oracle | ARCHITECTURE, revision 2 | schema, transition fixture, revision 3 | JSON and oracle completeness |
| L1 proof | fail-closed reducer/replay/projection evidence | L0 files | checker, negative fixtures, validation receipt | all positive/negative/replay checks pass twice |
| L2 research closeout | exact-binding research result | SWU receipt + prior research | completion review, findings, auditor receipt, closure, RESULT sync | independent audit pass |
| L3 deferred owner routes | ontology and proper runtime | completed research + owner decisions | later packages | outside this package |

## Delivery cut

`SWU-WHISPER-RSCH-STATE-001` owns L0 and L1 together. Splitting schema/table/checker would create partial receipts that cannot prove RS26. L2 is not a second implementation SWU: it is a governed evidence closeout with different ownership and no product mutation.

## Dependency and rollback

L1 depends on current L0 bytes in the same atomic change. L2 may start only from a passing content-addressed SWU receipt. All new L0/L1 files are candidate-local and reversible by removing only the new files; prior evidence is never rewritten. L2 may update `RESULT.md`, but only after its audit passes.
