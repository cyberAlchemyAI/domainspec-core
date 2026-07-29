# Augmentor Unified-Agent Node Index

This is a review surface for the candidate nodes in `nodes/nodes.json`. The
index is explanatory and carries no authority effect.

| Concept | Role | Branches | Runtime posture | Primary owner route |
| --- | --- | --- | --- | --- |
| `Augmentor` | projection | experience, runtime, knowledge | observed | ResonantOS product governance plus module owners |
| `ConversationThread` | workflow | experience, runtime | observed | ResonantOS chat module |
| `Interaction` | workflow | experience, runtime | absent | Interaction resolver owner required |
| `SourceRecord` | evidence | experience, knowledge | observed | provider named by `ownerRef` |
| `DisposableSemanticIndex` | projection | knowledge | absent | derived-index owner required |
| `ContextSnapshot` | evidence | experience, runtime, knowledge | absent | ResonantOS request/session host |
| `RouteDecision` | workflow | experience, runtime | absent | ResonantOS route owner required |
| `StrategyProposal` | projection | experience, runtime | absent | proposal projection owner required |
| `ApprovalRecord` | evidence | experience, runtime, authority bridge | absent | consumer plus registrar owner required |
| `Dispatch` | workflow | runtime | observed contract | Dispatch Spec |
| `Run` | workflow | experience, runtime | designed | selected ResonantOS host-operation owner |
| `LifecycleJoin` | workflow | runtime | observed contract | Orchestrate |
| `ResultConsumption` | workflow | experience, runtime, knowledge | absent | result-consumption owner required |
| `MemoryIntakeRequest` | workflow | experience, knowledge, authority bridge | observed boundary | provider and archive review owners |
| `OntologyCandidate` | projection | knowledge, authority bridge | designed | CyberAlchemy v2 ontology route |
| `AuthorityDecision` | authority | authority bridge | absent | authority-kind-specific named owner |
| `ReasoningRequest` | workflow | runtime, authority bridge | deferred | applicability/catalog owner required |
| `JudgmentReceipt` | evidence | runtime, authority bridge | deferred | agent reasoning engine route |

## Non-Collapse Review

- `Augmentor interface ≠ router ≠ scheduler ≠ memory or authority owner`
- `ConversationThread ≠ Interaction ≠ Run`
- `SourceRecord ≠ DisposableSemanticIndex ≠ ContextSnapshot`
- `RouteDecision ≠ StrategyProposal ≠ ApprovalRecord`
- `Dispatch ≠ Run`
- `LifecycleJoin ≠ ResultConsumption`
- `ResultConsumption ≠ MemoryIntakeRequest`
- `OntologyCandidate ≠ AuthorityDecision`
- `JudgmentReceipt ≠ ApprovalRecord`
- `JudgmentReceipt ≠ effect gate ≠ effect owner ≠ effect runtime`

The authoritative candidate record fields, sources, challenge contracts, and
residue routes remain in `nodes/nodes.json`.
