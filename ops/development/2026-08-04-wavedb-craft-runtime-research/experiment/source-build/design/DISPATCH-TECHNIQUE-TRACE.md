# Design dispatch technique trace

| Technique | Design effect | Evidence/gate | Status |
| --- | --- | --- | --- |
| `sequence` | fixes source -> dependencies -> generated source -> build -> test -> handoff | workflow and decision views | selected |
| `owner_boundary_check` | separates upstream, Invoke, Task Session, parent experiment, Craft, publication | context and dependency views | selected |
| `artifact_contract_bridge` | maps source/lock/toolchain/addon identities to manifests and receipt | low-level algorithms and planned witnesses | selected |
| `execution_receipt_handoff` | makes parent consumption conditional on a terminal receipt | interface and state flow | selected |
| `validation_loop` | gives every build stage an acceptance-critical oracle | failure branches and planned witnesses | selected |
| `concrete_path_evidence` | fixes ignored work area and receipt paths | persistence and dependency views | selected |
| `residue_ledger` | preserves platform, license, package, durability and release gaps | evidence ceiling | selected |

Full sequential dispatch remains required at Plan, where exact Task Session
steps, gates, receipts, and observability are available. Subagent strategy is
`none`; one local Task Session SWU owns the end-to-end source-built artifact.
