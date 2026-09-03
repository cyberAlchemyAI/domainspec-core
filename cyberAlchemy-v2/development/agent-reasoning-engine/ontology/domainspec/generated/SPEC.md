# Agent Reasoning Engine Specification

Generated human view. Canonical semantics live in the project-local machine sources.
Graph digest: `139863fd3ca0de1fce90472b80494b9e9619b7f729ecff71cec445a17862cd36`.

## Nodes

| Node | Kind | Intent |
| --- | --- | --- |
| `agent-reasoning-engine.AuthoritySeparation` | Rule | Keep context selection, semantic judgment, validation, consensus, and receipts separate from owner authority and exact-effect permission. |
| `agent-reasoning-engine.CapabilitySelection` | Entity | Return the nearest uniquely supported capability, visible ambiguity, no-match, or invalid result with exact profile and provenance digests. |
| `agent-reasoning-engine.CheckpointReasoningState` | Operation | Verify and flush one selected Reasoning State epoch before a model request, accepted effect, or automatic continuation boundary advances. |
| `agent-reasoning-engine.CompletionFrontierBoundary` | Rule | Block automatic continuation or completion replay when the exact completed-turn frontier and after-completion checkpoint do not verify. |
| `agent-reasoning-engine.ConsequenceAssessment` | Entity | Classify proposed continuations by admissible cardinality, reversibility, hazards, authority implications, and required owner gates. |
| `agent-reasoning-engine.ContextAssembly` | Operation | Select and freeze only context that is relevant to the bounded request and its declared evidence obligations while recording exclusions and gaps. |
| `agent-reasoning-engine.ContextBasisConstruction` | Operation | Construct one deterministic Necessary Context Basis only after routing, definition closure, and ontology selector locking succeed. |
| `agent-reasoning-engine.ContextBoundSemanticIntegrity` | Rule | Block semantic reduction when the Context Envelope binding, Problem Frame, entry gate, authority snapshot, freshness, claim ceiling, or selected Context Item digests do not agree exactly. |
| `agent-reasoning-engine.ContextEnvelope` | Entity | Freeze the included and excluded context, dependency identities, contradictions, gaps, freshness state, and claim ceiling for one reasoning run. |
| `agent-reasoning-engine.ContextIntegrity` | Rule | Prevent context selection or compression from erasing load-bearing provenance, authority limits, contradictions, transformations, exclusions, or gaps. |
| `agent-reasoning-engine.ContextItem` | Entity | Preserve one candidate context unit with relevance, provenance, authority, temporal, transformation, and digest metadata. |
| `agent-reasoning-engine.ContextRefresh` | Rule | Create a successor context epoch when selected dependencies change and separate historical replay from current-state revalidation. |
| `agent-reasoning-engine.ContextRevision` | Entity | Record why a successor context epoch exists and which selected dependencies changed without rewriting historical context. |
| `agent-reasoning-engine.ContextViewBinding` | Operation | Bind one current Necessary Context Basis to a consumer-specific Context Window View without weakening identity, provenance, or residue. |
| `agent-reasoning-engine.ContextWindowView` | Entity | Expose an immutable consumer-specific projection of one Necessary Context Basis under explicit plan-bound or interaction-bound identity semantics. |
| `agent-reasoning-engine.ContinuationDecision` | Operation | Return complete, direct, gate, or block after every completion and permit continuation only through one non-consequential admissible option. |
| `agent-reasoning-engine.DecisionGateProfile` | Entity | Configure route signals, consequence classes, protected hazards, owner-gate mappings, provenance bindings, and continuation limits without becoming authority. |
| `agent-reasoning-engine.DefinitionClosure` | Entity | Preserve the route-profiled least fixed point of exact definitions needed to interpret one bounded request before ontology selection or strategy. |
| `agent-reasoning-engine.DefinitionClosureResolution` | Operation | Resolve exact request-relative definitions to the selected route profile's deterministic least fixed point before ontology selection. |
| `agent-reasoning-engine.ExactDispatchPreparation` | Operation | Materialize, append, reconstruct, verify, and checkpoint the exact outbound request before it crosses a model, effect, or continuation boundary. |
| `agent-reasoning-engine.GatewayConnection` | Operation | Authorize a declared consumer and lane, attach one isolated app-server transport, and resume only its existing in-memory session when allowed. |
| `agent-reasoning-engine.GatewayConsumerSession` | Entity | Bind one declared consumer and lane to isolated in-memory wrapper, upstream connection, context, turn, journal, and reconnect state. |
| `agent-reasoning-engine.IntentRouteResolution` | Operation | Derive advisory route disposition from a prepared typed intent and frozen owner-supplied capability-route catalog without dispatch or execution authority. |
| `agent-reasoning-engine.JournalReplay` | Operation | Verify one immutable runtime-journal cut and reconstruct its recorded lifecycle state deterministically with zero external calls. |
| `agent-reasoning-engine.NecessaryContextBasis` | Entity | Bind the minimum explicit request-relative semantic substrate required before a selected route creates strategy or begins work. |
| `agent-reasoning-engine.OntologySelectorBinding` | Operation | Close and freeze only owner-declared required ontology edges and their recursively required endpoints for the bounded request. |
| `agent-reasoning-engine.OntologySelectorLock` | Entity | Freeze the owner-declared dependency-closed ontology records required for one request while keeping omissions, conflicts, gaps, and authority limits explicit. |
| `agent-reasoning-engine.PersistentAppServerGateway` | Entity | Represent one long-lived local ARE transport runtime with an exact protocol binding, bounded consumers, and no durable or effect authority. |
| `agent-reasoning-engine.ReasoningAndContextManagement` | Rule | Compose fast routing, definition closure, ontology selector locking, Necessary Context Basis construction, dual-lane Context Window Views, semantic reduction, refresh, receipts, and authority-separation obligations as the candidate Agent Reasoning Engine system boundary. |
| `agent-reasoning-engine.ReasoningContextLifecycle` | Workflow | Orchestrate request routing, necessary-context formation, semantic reduction, and consequence evaluation as one bounded non-authorizing lifecycle. |
| `agent-reasoning-engine.ReasoningDispatch` | Entity | Bind the complete canonical outbound request to its Reasoning State epoch and exact request-series configuration for deterministic reconstruction. |
| `agent-reasoning-engine.ReasoningReceipt` | Entity | Bind one context epoch, derivation, support, defeaters, challenge closure, outcome, and residue without granting authority. |
| `agent-reasoning-engine.ReasoningReceiptConstraint` | Entity | Bind one explicitly dependent continuation proposal to a verified Reasoning Receipt outcome without granting authority or overriding structural consequence rules. |
| `agent-reasoning-engine.ReasoningRequest` | Entity | Represent one bounded attributable reasoning objective and its protected effect boundary. |
| `agent-reasoning-engine.ReasoningStateBoundary` | Rule | Fail closed when append-only state, exact reconstruction, or a required risk-aligned checkpoint cannot be proven before its boundary. |
| `agent-reasoning-engine.ReasoningStateCheckpoint` | Entity | Record that one verified Reasoning State epoch reached its declared durability posture before a risk-aligned boundary advanced. |
| `agent-reasoning-engine.ReasoningStateDerivedIndex` | Entity | Represent one disposable deterministic index derived only from a verified canonical Reasoning State record stream. |
| `agent-reasoning-engine.ReasoningStateEpoch` | Entity | Bind an immutable content-addressed selection of reasoning events to exact dependencies, context, consumer, request, and continuation frontier. |
| `agent-reasoning-engine.ReasoningStateFormation` | Operation | Append explicit reasoning products and seal one exact reusable Reasoning State epoch without rewriting prior bytes. |
| `agent-reasoning-engine.ReasoningStateFrontier` | Entity | Bind one completed reasoning boundary to its exact subject, context, semantic result, continuation result, and after-completion checkpoint. |
| `agent-reasoning-engine.ReasoningStateLedger` | Entity | Preserve the canonical append-only hash-chained sequence of explicit reasoning products without capturing hidden model chain-of-thought or granting authority. |
| `agent-reasoning-engine.ReasoningStateRecoveryAssessment` | Entity | Bind exact log, derived-index, and final-checkpoint identities to one non-authorizing recovery disposition. |
| `agent-reasoning-engine.ReasoningStateRecoveryBoundary` | Rule | Block reasoning-state recovery when exact log verification, derived-index rebuilding, final-checkpoint selection, or source rechecking fails. |
| `agent-reasoning-engine.RebuildReasoningStateIndex` | Operation | Verify canonical Reasoning State records and deterministically rebuild their disposable indexes with zero external calls. |
| `agent-reasoning-engine.RecoverReasoningState` | Operation | Hydrate one exact checkpointed Reasoning State ledger after verified index rebuilding and source rechecking. |
| `agent-reasoning-engine.RequestContext` | Entity | Preserve a raw request with explicit or inferred objective, effect, target, constraint, and provenance fields for fast deterministic routing. |
| `agent-reasoning-engine.RuntimeJournal` | Entity | Preserve a bounded immutable hash-chained sequence of compact lifecycle events and exact per-turn cuts without durable or effect authority. |
| `agent-reasoning-engine.SealCompletionFrontier` | Operation | Append, epoch-seal, and checkpoint one exact completed-turn semantic and continuation frontier before automatic continuation. |
| `agent-reasoning-engine.SemanticJudgment` | Entity | Represent exactly one typed semantic disposition under a frozen context, catalog, evaluator, and residue set. |
| `agent-reasoning-engine.SemanticReduction` | Operation | Derive exactly one typed semantic outcome from an admitted frozen context and finite rule catalog while abstaining on missing support or unresolved ownership. |

## Edges

| Edge | From | Type | To |
| --- | --- | --- | --- |
| `agent-reasoning-engine.edge.authority-separation-enforces-continuation` | `agent-reasoning-engine.AuthoritySeparation` | `enforces` | `agent-reasoning-engine.ContinuationDecision` |
| `agent-reasoning-engine.edge.authority-separation-enforces-reduction` | `agent-reasoning-engine.AuthoritySeparation` | `enforces` | `agent-reasoning-engine.SemanticReduction` |
| `agent-reasoning-engine.edge.authority-separation-enforces-route` | `agent-reasoning-engine.AuthoritySeparation` | `enforces` | `agent-reasoning-engine.IntentRouteResolution` |
| `agent-reasoning-engine.edge.authority-separation-enforces-view` | `agent-reasoning-engine.AuthoritySeparation` | `enforces` | `agent-reasoning-engine.ContextViewBinding` |
| `agent-reasoning-engine.edge.basis-construction-creates-basis` | `agent-reasoning-engine.ContextBasisConstruction` | `creates` | `agent-reasoning-engine.NecessaryContextBasis` |
| `agent-reasoning-engine.edge.basis-construction-reads-capability-selection` | `agent-reasoning-engine.ContextBasisConstruction` | `reads` | `agent-reasoning-engine.CapabilitySelection` |
| `agent-reasoning-engine.edge.basis-construction-reads-definition-closure` | `agent-reasoning-engine.ContextBasisConstruction` | `reads` | `agent-reasoning-engine.DefinitionClosure` |
| `agent-reasoning-engine.edge.basis-construction-reads-request-context` | `agent-reasoning-engine.ContextBasisConstruction` | `reads` | `agent-reasoning-engine.RequestContext` |
| `agent-reasoning-engine.edge.basis-construction-reads-selector-lock` | `agent-reasoning-engine.ContextBasisConstruction` | `reads` | `agent-reasoning-engine.OntologySelectorLock` |
| `agent-reasoning-engine.edge.checkpoint-state-creates-checkpoint` | `agent-reasoning-engine.CheckpointReasoningState` | `creates` | `agent-reasoning-engine.ReasoningStateCheckpoint` |
| `agent-reasoning-engine.edge.checkpoint-state-reads-epoch` | `agent-reasoning-engine.CheckpointReasoningState` | `reads` | `agent-reasoning-engine.ReasoningStateEpoch` |
| `agent-reasoning-engine.edge.completion-frontier-boundary-enforces-sealing` | `agent-reasoning-engine.CompletionFrontierBoundary` | `enforces` | `agent-reasoning-engine.SealCompletionFrontier` |
| `agent-reasoning-engine.edge.context-assembly-creates-envelope` | `agent-reasoning-engine.ContextAssembly` | `creates` | `agent-reasoning-engine.ContextEnvelope` |
| `agent-reasoning-engine.edge.context-assembly-reads-context-item` | `agent-reasoning-engine.ContextAssembly` | `reads` | `agent-reasoning-engine.ContextItem` |
| `agent-reasoning-engine.edge.context-assembly-reads-view` | `agent-reasoning-engine.ContextAssembly` | `reads` | `agent-reasoning-engine.ContextWindowView` |
| `agent-reasoning-engine.edge.context-bound-semantic-integrity-enforces-reduction` | `agent-reasoning-engine.ContextBoundSemanticIntegrity` | `enforces` | `agent-reasoning-engine.SemanticReduction` |
| `agent-reasoning-engine.edge.context-integrity-enforces-assembly` | `agent-reasoning-engine.ContextIntegrity` | `enforces` | `agent-reasoning-engine.ContextAssembly` |
| `agent-reasoning-engine.edge.context-integrity-enforces-basis` | `agent-reasoning-engine.ContextIntegrity` | `enforces` | `agent-reasoning-engine.ContextBasisConstruction` |
| `agent-reasoning-engine.edge.context-integrity-enforces-view` | `agent-reasoning-engine.ContextIntegrity` | `enforces` | `agent-reasoning-engine.ContextViewBinding` |
| `agent-reasoning-engine.edge.context-refresh-enforces-view-binding` | `agent-reasoning-engine.ContextRefresh` | `enforces` | `agent-reasoning-engine.ContextViewBinding` |
| `agent-reasoning-engine.edge.continuation-reads-judgment` | `agent-reasoning-engine.ContinuationDecision` | `reads` | `agent-reasoning-engine.SemanticJudgment` |
| `agent-reasoning-engine.edge.continuation-reads-receipt` | `agent-reasoning-engine.ContinuationDecision` | `reads` | `agent-reasoning-engine.ReasoningReceipt` |
| `agent-reasoning-engine.edge.continuation-reads-receipt-constraint` | `agent-reasoning-engine.ContinuationDecision` | `reads` | `agent-reasoning-engine.ReasoningReceiptConstraint` |
| `agent-reasoning-engine.edge.definition-closure-creates-definition-closure` | `agent-reasoning-engine.DefinitionClosureResolution` | `creates` | `agent-reasoning-engine.DefinitionClosure` |
| `agent-reasoning-engine.edge.definition-closure-reads-capability-selection` | `agent-reasoning-engine.DefinitionClosureResolution` | `reads` | `agent-reasoning-engine.CapabilitySelection` |
| `agent-reasoning-engine.edge.definition-closure-reads-request-context` | `agent-reasoning-engine.DefinitionClosureResolution` | `reads` | `agent-reasoning-engine.RequestContext` |
| `agent-reasoning-engine.edge.dispatch-preparation-creates-dispatch` | `agent-reasoning-engine.ExactDispatchPreparation` | `creates` | `agent-reasoning-engine.ReasoningDispatch` |
| `agent-reasoning-engine.edge.dispatch-preparation-reads-epoch` | `agent-reasoning-engine.ExactDispatchPreparation` | `reads` | `agent-reasoning-engine.ReasoningStateEpoch` |
| `agent-reasoning-engine.edge.frontier-sealing-creates-frontier` | `agent-reasoning-engine.SealCompletionFrontier` | `creates` | `agent-reasoning-engine.ReasoningStateFrontier` |
| `agent-reasoning-engine.edge.frontier-sealing-reads-consequence-assessment` | `agent-reasoning-engine.SealCompletionFrontier` | `reads` | `agent-reasoning-engine.ConsequenceAssessment` |
| `agent-reasoning-engine.edge.frontier-sealing-reads-ledger` | `agent-reasoning-engine.SealCompletionFrontier` | `reads` | `agent-reasoning-engine.ReasoningStateLedger` |
| `agent-reasoning-engine.edge.frontier-sealing-reads-semantic-judgment` | `agent-reasoning-engine.SealCompletionFrontier` | `reads` | `agent-reasoning-engine.SemanticJudgment` |
| `agent-reasoning-engine.edge.gateway-connection-creates-consumer-session` | `agent-reasoning-engine.GatewayConnection` | `creates` | `agent-reasoning-engine.GatewayConsumerSession` |
| `agent-reasoning-engine.edge.gateway-connection-reads-gateway` | `agent-reasoning-engine.GatewayConnection` | `reads` | `agent-reasoning-engine.PersistentAppServerGateway` |
| `agent-reasoning-engine.edge.intent-route-creates-capability-selection` | `agent-reasoning-engine.IntentRouteResolution` | `creates` | `agent-reasoning-engine.CapabilitySelection` |
| `agent-reasoning-engine.edge.intent-route-reads-request-context` | `agent-reasoning-engine.IntentRouteResolution` | `reads` | `agent-reasoning-engine.RequestContext` |
| `agent-reasoning-engine.edge.journal-replay-reads-runtime-journal` | `agent-reasoning-engine.JournalReplay` | `reads` | `agent-reasoning-engine.RuntimeJournal` |
| `agent-reasoning-engine.edge.lifecycle-orchestrates-basis-construction` | `agent-reasoning-engine.ReasoningContextLifecycle` | `orchestrates` | `agent-reasoning-engine.ContextBasisConstruction` |
| `agent-reasoning-engine.edge.lifecycle-orchestrates-completion-frontier` | `agent-reasoning-engine.ReasoningContextLifecycle` | `orchestrates` | `agent-reasoning-engine.SealCompletionFrontier` |
| `agent-reasoning-engine.edge.lifecycle-orchestrates-context-assembly` | `agent-reasoning-engine.ReasoningContextLifecycle` | `orchestrates` | `agent-reasoning-engine.ContextAssembly` |
| `agent-reasoning-engine.edge.lifecycle-orchestrates-continuation` | `agent-reasoning-engine.ReasoningContextLifecycle` | `orchestrates` | `agent-reasoning-engine.ContinuationDecision` |
| `agent-reasoning-engine.edge.lifecycle-orchestrates-definition-closure` | `agent-reasoning-engine.ReasoningContextLifecycle` | `orchestrates` | `agent-reasoning-engine.DefinitionClosureResolution` |
| `agent-reasoning-engine.edge.lifecycle-orchestrates-dispatch-preparation` | `agent-reasoning-engine.ReasoningContextLifecycle` | `orchestrates` | `agent-reasoning-engine.ExactDispatchPreparation` |
| `agent-reasoning-engine.edge.lifecycle-orchestrates-gateway-connection` | `agent-reasoning-engine.ReasoningContextLifecycle` | `orchestrates` | `agent-reasoning-engine.GatewayConnection` |
| `agent-reasoning-engine.edge.lifecycle-orchestrates-intent-route` | `agent-reasoning-engine.ReasoningContextLifecycle` | `orchestrates` | `agent-reasoning-engine.IntentRouteResolution` |
| `agent-reasoning-engine.edge.lifecycle-orchestrates-journal-replay` | `agent-reasoning-engine.ReasoningContextLifecycle` | `orchestrates` | `agent-reasoning-engine.JournalReplay` |
| `agent-reasoning-engine.edge.lifecycle-orchestrates-reasoning-checkpoint` | `agent-reasoning-engine.ReasoningContextLifecycle` | `orchestrates` | `agent-reasoning-engine.CheckpointReasoningState` |
| `agent-reasoning-engine.edge.lifecycle-orchestrates-reasoning-index-rebuild` | `agent-reasoning-engine.ReasoningContextLifecycle` | `orchestrates` | `agent-reasoning-engine.RebuildReasoningStateIndex` |
| `agent-reasoning-engine.edge.lifecycle-orchestrates-reasoning-recovery` | `agent-reasoning-engine.ReasoningContextLifecycle` | `orchestrates` | `agent-reasoning-engine.RecoverReasoningState` |
| `agent-reasoning-engine.edge.lifecycle-orchestrates-reasoning-state` | `agent-reasoning-engine.ReasoningContextLifecycle` | `orchestrates` | `agent-reasoning-engine.ReasoningStateFormation` |
| `agent-reasoning-engine.edge.lifecycle-orchestrates-selector-binding` | `agent-reasoning-engine.ReasoningContextLifecycle` | `orchestrates` | `agent-reasoning-engine.OntologySelectorBinding` |
| `agent-reasoning-engine.edge.lifecycle-orchestrates-semantic-reduction` | `agent-reasoning-engine.ReasoningContextLifecycle` | `orchestrates` | `agent-reasoning-engine.SemanticReduction` |
| `agent-reasoning-engine.edge.lifecycle-orchestrates-view-binding` | `agent-reasoning-engine.ReasoningContextLifecycle` | `orchestrates` | `agent-reasoning-engine.ContextViewBinding` |
| `agent-reasoning-engine.edge.reasoning-state-boundary-enforces-checkpoint` | `agent-reasoning-engine.ReasoningStateBoundary` | `enforces` | `agent-reasoning-engine.CheckpointReasoningState` |
| `agent-reasoning-engine.edge.reasoning-state-boundary-enforces-dispatch` | `agent-reasoning-engine.ReasoningStateBoundary` | `enforces` | `agent-reasoning-engine.ExactDispatchPreparation` |
| `agent-reasoning-engine.edge.reasoning-state-boundary-enforces-formation` | `agent-reasoning-engine.ReasoningStateBoundary` | `enforces` | `agent-reasoning-engine.ReasoningStateFormation` |
| `agent-reasoning-engine.edge.reasoning-state-formation-creates-epoch` | `agent-reasoning-engine.ReasoningStateFormation` | `creates` | `agent-reasoning-engine.ReasoningStateEpoch` |
| `agent-reasoning-engine.edge.reasoning-state-formation-reads-envelope` | `agent-reasoning-engine.ReasoningStateFormation` | `reads` | `agent-reasoning-engine.ContextEnvelope` |
| `agent-reasoning-engine.edge.reasoning-state-formation-reads-ledger` | `agent-reasoning-engine.ReasoningStateFormation` | `reads` | `agent-reasoning-engine.ReasoningStateLedger` |
| `agent-reasoning-engine.edge.rebuild-reasoning-index-creates-index` | `agent-reasoning-engine.RebuildReasoningStateIndex` | `creates` | `agent-reasoning-engine.ReasoningStateDerivedIndex` |
| `agent-reasoning-engine.edge.rebuild-reasoning-index-reads-ledger` | `agent-reasoning-engine.RebuildReasoningStateIndex` | `reads` | `agent-reasoning-engine.ReasoningStateLedger` |
| `agent-reasoning-engine.edge.recover-reasoning-state-creates-assessment` | `agent-reasoning-engine.RecoverReasoningState` | `creates` | `agent-reasoning-engine.ReasoningStateRecoveryAssessment` |
| `agent-reasoning-engine.edge.recover-reasoning-state-reads-checkpoint` | `agent-reasoning-engine.RecoverReasoningState` | `reads` | `agent-reasoning-engine.ReasoningStateCheckpoint` |
| `agent-reasoning-engine.edge.recover-reasoning-state-reads-index` | `agent-reasoning-engine.RecoverReasoningState` | `reads` | `agent-reasoning-engine.ReasoningStateDerivedIndex` |
| `agent-reasoning-engine.edge.recover-reasoning-state-reads-ledger` | `agent-reasoning-engine.RecoverReasoningState` | `reads` | `agent-reasoning-engine.ReasoningStateLedger` |
| `agent-reasoning-engine.edge.recovery-boundary-enforces-index-rebuild` | `agent-reasoning-engine.ReasoningStateRecoveryBoundary` | `enforces` | `agent-reasoning-engine.RebuildReasoningStateIndex` |
| `agent-reasoning-engine.edge.recovery-boundary-enforces-recovery` | `agent-reasoning-engine.ReasoningStateRecoveryBoundary` | `enforces` | `agent-reasoning-engine.RecoverReasoningState` |
| `agent-reasoning-engine.edge.selector-binding-creates-selector-lock` | `agent-reasoning-engine.OntologySelectorBinding` | `creates` | `agent-reasoning-engine.OntologySelectorLock` |
| `agent-reasoning-engine.edge.selector-binding-reads-definition-closure` | `agent-reasoning-engine.OntologySelectorBinding` | `reads` | `agent-reasoning-engine.DefinitionClosure` |
| `agent-reasoning-engine.edge.semantic-reduction-creates-judgment` | `agent-reasoning-engine.SemanticReduction` | `creates` | `agent-reasoning-engine.SemanticJudgment` |
| `agent-reasoning-engine.edge.semantic-reduction-reads-envelope` | `agent-reasoning-engine.SemanticReduction` | `reads` | `agent-reasoning-engine.ContextEnvelope` |
| `agent-reasoning-engine.edge.semantic-reduction-reads-runtime-journal` | `agent-reasoning-engine.SemanticReduction` | `reads` | `agent-reasoning-engine.RuntimeJournal` |
| `agent-reasoning-engine.edge.system-rule-enforces-assembly` | `agent-reasoning-engine.ReasoningAndContextManagement` | `enforces` | `agent-reasoning-engine.ContextAssembly` |
| `agent-reasoning-engine.edge.system-rule-enforces-basis` | `agent-reasoning-engine.ReasoningAndContextManagement` | `enforces` | `agent-reasoning-engine.ContextBasisConstruction` |
| `agent-reasoning-engine.edge.system-rule-enforces-continuation` | `agent-reasoning-engine.ReasoningAndContextManagement` | `enforces` | `agent-reasoning-engine.ContinuationDecision` |
| `agent-reasoning-engine.edge.system-rule-enforces-definition-closure` | `agent-reasoning-engine.ReasoningAndContextManagement` | `enforces` | `agent-reasoning-engine.DefinitionClosureResolution` |
| `agent-reasoning-engine.edge.system-rule-enforces-reduction` | `agent-reasoning-engine.ReasoningAndContextManagement` | `enforces` | `agent-reasoning-engine.SemanticReduction` |
| `agent-reasoning-engine.edge.system-rule-enforces-route` | `agent-reasoning-engine.ReasoningAndContextManagement` | `enforces` | `agent-reasoning-engine.IntentRouteResolution` |
| `agent-reasoning-engine.edge.system-rule-enforces-selector-binding` | `agent-reasoning-engine.ReasoningAndContextManagement` | `enforces` | `agent-reasoning-engine.OntologySelectorBinding` |
| `agent-reasoning-engine.edge.system-rule-enforces-view` | `agent-reasoning-engine.ReasoningAndContextManagement` | `enforces` | `agent-reasoning-engine.ContextViewBinding` |
| `agent-reasoning-engine.edge.view-binding-creates-view` | `agent-reasoning-engine.ContextViewBinding` | `creates` | `agent-reasoning-engine.ContextWindowView` |
| `agent-reasoning-engine.edge.view-binding-reads-basis` | `agent-reasoning-engine.ContextViewBinding` | `reads` | `agent-reasoning-engine.NecessaryContextBasis` |

This file is generated; edit machine sources and rebuild.
