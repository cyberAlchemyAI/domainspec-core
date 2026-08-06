# Define dispatch technique trace

| Technique | Activation | Effect | Validation expectation | Status |
| --- | --- | --- | --- | --- |
| `sequence` | source closure must precede dependencies, build, tests, and handoff | fixes the route order | downstream phase never consumes a failed predecessor | selected |
| `owner_boundary_check` | Invoke, Task Session, WaveDB source, Craft, and publication have different owners | prevents authority collapse | receipt states local evidence ceiling | selected |
| `artifact_contract_bridge` | source/build inputs must become a Task Session contract | names manifests and terminal receipt | Design and Plan bind every artifact | selected |
| `execution_receipt_handoff` | native build effects require exact evidence | requires terminal build receipt before parent refresh | receipt schema exists before execution | selected |
| `validation_loop` | source, dependencies, build, load, and tests can each fail | makes every stage acceptance-critical | first failure blocks the artifact | selected |
| `residue_ledger` | platform, licenses, publication, and durability remain open | preserves non-goals | closeout repeats unresolved residue | selected |

A full sequential Dispatch Spec is required at Plan because the route crosses
external source/dependency evidence and hands native execution from Invoke to
Task Session. No subagent strategy is selected; the current developer boundary
forbids unrequested delegation and one local SWU is sufficient.
