# Augmentor Ontology Views

These are interpretive views over one shared node and relation set. They are
not separate ontologies, schema namespaces, lifecycle states, or promotion
routes.

| View | Role | Primary question |
| --- | --- | --- |
| `experience.json` | meaning | What should one conversational interface mean to the user? |
| `runtime.json` | system | Which retained owner controls each route, approval, Run, join, and consumption step? |
| `knowledge.json` | evidence | How do provider-owned sources become bounded context and non-authoritative candidates? |
| `authority-bridge.json` | bridge | Where must ontology, judgment, approval, authority, and effects remain separate? |
| `intent-route.json` | system | How may Augmentor consume a deterministic zero-authority disposition while product and runtime owners remain separate? |

## Cross-View Map

```text
EXPERIENCE
Augmentor → ConversationThread → Interaction → ContextSnapshot → RouteDecision
                                             │
                                             ▼
RUNTIME
StrategyProposal → ApprovalRecord → Dispatch → Run
                                             │
                                             ▼
                                  LifecycleJoin → ResultConsumption
                                                            │
                                                            ▼
KNOWLEDGE
SourceRecord → bounded projection → ContextSnapshot   MemoryIntakeRequest
     │                                                       │
     └──────── provider disposition + Inventory handoff ─────┘
                                      │
                                      ▼
                               OntologyCandidate
                                      │
                                      ▼
AUTHORITY BRIDGE
                          named-owner AuthorityDecision

ContextSnapshot → ReasoningRequest → JudgmentReceipt
                                      │
                                      └─ may inform; never authorizes

INTENT ROUTE
ContextSnapshot → IntentRouteRequest ─┐
                                      ├→ ResolverInvocation → RouteDisposition
RouteCatalogProjection ───────────────┘                         │
                                                                └─ may inform RouteDecision; never approves
```

## Shared Reading Rules

- Every alignment claim cites evidence from both sides of its bridge.
- An observed owner contract does not prove the proposed joined adapter.
- A system artifact cannot redefine user meaning.
- A meaning view cannot claim implementation without runtime evidence.
- A source, index, Inventory package, ontology candidate, decision record, and
  canonical artifact remain distinct objects.
- All current package relations retain `authority_effect: none`.
- `RouteDisposition` remains separate from product `RouteDecision`, semantic
  `JudgmentReceipt`, exact `ApprovalRecord`, and every execution object.
