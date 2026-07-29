# Revised synthesis — Augmentor user understanding, graph, and bounded reasoning

## Product thesis

Augmentor should improve a turn by compiling ephemeral, user-controlled request/session handles together with existing Living Archive source records, querying a rebuildable source-bound semantic index, deriving one bounded typed result, and showing why that context changed the answer—without creating a second memory provider, a host user ledger, a second prompt builder, or a ResonantOS copy of private CyberAlchemy authority semantics. [C-001–C-011]

## Current versus missing capability

| Area | Current | Missing |
|---|---|---|
| Alpha chat | The browser-first extension sends bounded transcript, page context, attachments, and its explicit personalization settings into the active provider route. [C-001, C-003] | The active chat contract contains no archive context or reasoning presentation. [C-002] |
| Source memory | Existing memory-host functions own capability-gated search/read and intake. Owned source records remain truth. [C-002] | One coordinator that calls those functions before provider execution and extends the sole existing prompt builder. [C-006] |
| Personalization | Profile fields, Augmentor name, and free-form Augmentor prompt are extension settings, not provider-owned user memory. [C-003] | Durable preference memory remains deferred; its storage/owner is unresolved. v0 must not invent one. [C-003] |
| User understanding | Candidate User/Translate/Guide artifacts provide protected-handle and active-evidence patterns. [C-004] | Request/session-only typed handles, correction/tombstone semantics, and visible controls. [C-005] |
| Semantic access | CyberAlchemy supplies candidate typed-record, relation, projection, grounding, and validation precedents. [C-007, C-008] | A disposable semantic index plus net-new graph-delta lifecycle over existing source refs/digests. [C-008] |
| Reasoning | A private finite evaluator demonstrates deterministic conflict, missing-condition, cycle, precedence, residue, and replay atoms. [C-009] | Generic operation registry, operation-discriminated results, and separately grounded presentation. [C-010] |
| User experience | Historical Context Memory UI and IDE Ergonomics demonstrate inspect/edit and source-reference interaction grammar. [C-011] | Alpha-native status chip, context drawer, turn exclusion, immediate ephemeral-handle correction/forgetting, pending source correction, and memory-off reruns. [C-011, C-013] |

## Non-collapsing layer model

1. **Extension settings**

   Explicit profile fields, Augmentor display name, and user-authored Augmentor prompt remain extension settings. They are inputs to a request, not a provider-owned user model and not evidence for inferred traits. [C-003]

2. **Owned source records**

   Living Archive pages, raw/imported evidence, retained conversation records, and project artifacts remain the durable truth under their existing memory/source owners. A semantic record contains only source-qualified references and digests; it does not replace or duplicate source bytes. [C-002, C-007]

3. **Ephemeral `UserHandle` set**

   The request compiler creates at most eight handles from the current request/session. No v0 host ledger exists. Explicit and confirmed handles may express the current user goal, rationale, domain anchor, vocabulary preference, failed bridge, or constraint. Only a narrow `concept_state` may be derived, and only from named active evidence. Every handle is inspectable, correctable, tombstonable, and forgettable inside its request/session. Durable preference persistence remains deferred until a separate owner is selected. [C-003–C-005]

4. **Rebuildable semantic index**

   Typed nodes/edges, adjacency maps, projections, and caches are derived from owned source refs/digests. They are disposable and rebuildable. They are neither source truth nor a memory provider. [C-007, C-008]

5. **Bounded query projection**

   A named operation retrieves a small graph slice with freshness, contestation, omissions, truncation, source posture, and match reasons. Freshness and contestation are orthogonal: a current record may be contested, and a stale record may be uncontested. [C-008]

6. **Deterministic reasoning result**

   The operation registry selects allowed predicates and returns one operation-specific deterministic result. Retrieval or traversal alone is not reasoning. [C-010]

7. **`ReasoningPresentation`**

   Zero or one model call may explain the deterministic result. Its rationale is claim-level and must cite selected node/edge IDs. It cannot add premises, change the deterministic outcome, or turn abstention into advice. [C-010]

8. **Presentation receipt**

   A redacted response companion powers a quiet context status and an inspectable drawer. It is transparency support, not authority or the center of the product. [C-011]

The derivation direction is:

`extension settings + ephemeral handles + owned source refs/digests → disposable semantic index → bounded projection → deterministic operation result → optional grounded presentation`

Correction never flows backward from a model explanation into a trusted source.

## Compact contracts

```ts
type ExplicitUserHandle = {
  id: string;
  kind:
    | "goal"
    | "rationale"
    | "domain_anchor"
    | "vocabulary_preference"
    | "failed_bridge"
    | "constraint";
  value: unknown;
  posture: "explicit" | "confirmed";
  retention: "request" | "session";
  sourceRefs: string[];
  observedAt: string;
  correctionOf?: string;
  tombstonedAt?: string;
};

type ConceptStateHandle = {
  id: string;
  kind: "concept_state";
  concept: string;
  state:
    | "unknown"
    | "exposed"
    | "clarified"
    | "practiced"
    | "transferable"
    | "mastered"
    | "stale";
  posture: "explicit" | "confirmed" | "derived";
  retention: "request" | "session";
  evidence: Array<{
    kind: "teach_back" | "retrieval" | "contrast" | "transfer";
    sourceRef: string;
    observedAt: string;
  }>;
  correctionOf?: string;
  tombstonedAt?: string;
};

type UserHandle = ExplicitUserHandle | ConceptStateHandle;
```

No other handle kind admits `posture: "derived"`. A single utterance cannot become a durable preference, identity claim, sensitive trait, profession, personality, or global ability score. [C-005]

```ts
type GraphNode = {
  id: string;
  kind: "Topic" | "Artifact" | "Claim" | "TaskGoal" | "TaskConstraint";
  label: string;
  sourceRefs: string[];
  sourceDigests: string[];
  freshness: "current" | "stale";
  contestation: "uncontested" | "contested" | "blocked";
};

type GraphEdge = {
  id: string;
  from: string;
  to: string;
  predicate:
    | "about"
    | "supports"
    | "contradicts"
    | "requires"
    | "precedes"
    | "derived_from";
  evidenceRefs: string[];
  evidenceDigests: string[];
  freshness: "current" | "stale";
  contestation: "uncontested" | "contested" | "blocked";
};
```

`TaskGoal` and `TaskConstraint` describe source-backed object-domain work. They are never user-handle nodes. `analogous_to` is not persisted in v0; structural analogy is an operation over shared relation patterns plus explicit differences. [C-005, C-007, C-010]

```ts
type NodeOp =
  | {
      op: "upsert";
      id: string;
      beforeHash?: string;
      record: GraphNode;
      reason: string;
    }
  | {
      op: "retract";
      id: string;
      beforeHash?: string;
      reason: string;
    };

type EdgeOp =
  | {
      op: "upsert";
      id: string;
      beforeHash?: string;
      record: GraphEdge;
      reason: string;
    }
  | {
      op: "retract";
      id: string;
      beforeHash?: string;
      reason: string;
    };

type GraphDelta = {
  deltaId: string;
  baseIndexVersion: string;
  sourceChanges: Array<{
    sourceRef: string;
    oldDigest?: string;
    newDigest?: string;
    change: "observed" | "accepted_correction" | "retracted";
  }>;
  nodeOps: NodeOp[];
  edgeOps: EdgeOp[];
  invalidates: Array<{ targetId: string; reason: string; sourceRef: string }>;
  contradictions: Array<{
    leftId: string;
    rightId: string;
    evidenceRefs: string[];
  }>;
  resultIndexVersion: string;
};
```

The graph-delta lifecycle is net-new. Existing candidate contracts support typed records, stable IDs, endpoint/digest validation, and non-authorizing projections; they do not establish this consumer lifecycle as implemented. A stale base fails and rebases. Accepted source-digest changes stale/invalidate dependents. Contradictions coexist. Same-ID/different-hash changes remain explicit conflicts. [C-008]

## Predicate-to-operation registry

```ts
const OPERATION_REGISTRY = {
  detect_conflict: {
    predicates: ["supports", "contradicts", "derived_from"],
    result: "ConflictResult",
  },
  find_missing_premise: {
    predicates: ["requires", "supports", "derived_from"],
    result: "MissingPremiseResult",
  },
  select_analogy: {
    predicates: ["about", "requires", "precedes"],
    result: "AnalogyResult",
  },
  order_task_dependencies: {
    predicates: ["requires", "precedes"],
    result: "DependencyOrderResult",
  },
  compare_options: {
    predicates: ["about", "supports", "contradicts", "requires"],
    result: "OptionComparisonResult",
  },
} as const;
```

```ts
type DeterministicResult =
  | {
      operation: "detect_conflict";
      outcome: "conflict" | "derived" | "abstained" | "invalid_context";
      conflicts: Array<{ left: string; right: string; edgeIds: string[] }>;
    }
  | {
      operation: "find_missing_premise";
      outcome: "missing_premise" | "derived" | "abstained" | "invalid_context";
      missingPremises: Array<{ nodeId: string; requiredByEdgeIds: string[] }>;
    }
  | {
      operation: "select_analogy";
      outcome: "derived" | "ambiguous" | "abstained" | "invalid_context";
      selected?: {
        sourceNodeIds: string[];
        sharedEdgePatterns: string[];
        differences: string[];
      };
    }
  | {
      operation: "order_task_dependencies";
      outcome: "derived" | "conflict" | "abstained" | "invalid_context";
      orderedNodeIds: string[];
      cycleEdgeIds: string[];
    }
  | {
      operation: "compare_options";
      outcome: "derived" | "ambiguous" | "abstained" | "invalid_context";
      options: Array<{
        id: string;
        satisfied: string[];
        violated: string[];
        unresolved: string[];
      }>;
    };

type ReasoningResult = {
  requestId: string;
  selectedNodeIds: string[];
  selectedEdgeIds: string[];
  deterministic: DeterministicResult;
  residue: string[];
  contextDigest: string;
  deterministicDigest: string;
  cacheStatus: "miss" | "deterministic_hit" | "full_replay";
};

type ReasoningPresentation = {
  answer: string;
  rationaleClaims: Array<{
    text: string;
    supportNodeIds: string[];
    supportEdgeIds: string[];
  }>;
  caveats: string[];
  model?: {
    providerClass: string;
    modelId: string;
    promptVersion: string;
  };
};
```

The validator rejects any `rationaleClaim` whose support IDs are absent from the deterministic selection. On rejection or model failure, the UI renders a deterministic template. [C-010]

## Correction, exclusion, and invalidation semantics

| User action | Immediate effect | Durable/source effect | Required rerun |
|---|---|---|---|
| Exclude for this turn | Remove selected source/handle from the current request and change its context digest. | None. | Recompose projection and reasoning for this turn. |
| Correct an ephemeral handle | Tombstone the old request/session handle and add a corrected handle immediately. | None; no host ledger exists. | Change handle digest, invalidate request cache, recompose. |
| Forget an ephemeral handle | Tombstone/remove it from request/session state. | None. | Prove absence from the next composed prompt and result. |
| Propose source correction | Create pending intake/review work and show `pending`. | Owned source bytes and digests remain unchanged. | Existing result remains source-current; user may exclude the disputed item meanwhile. |
| Accept source correction | Source owner changes the record and digest. | Accepted source change becomes truth. | Emit invalidation delta, rebuild affected index/projections, rerun reasoning. |
| Memory off | Omit archive retrieval and source-derived graph context. | None. | Run the existing transcript/page-context path and show truthful degradation. |

Pending intake is not an accepted correction. Immediate user control and durable source correction are distinct experiences. [C-013]

## Releasable v0: one complete vertical bundle

The separate v0a–v0e labels remain implementation work order only. None is a releasable claim by itself. Releasable v0 requires the complete vertical journey:

`typed ephemeral handle → source-bound GraphDelta → disposable semantic index → bounded projection → find_missing_premise result → visibly improved answer → presentation receipt → correction/forget/exclusion/memory-off reruns`

Literal deployment fixture:

```ts
const handle: UserHandle = {
  id: "uh-session-rollback",
  kind: "constraint",
  value: "Do not recommend deployment without verified rollback support",
  posture: "explicit",
  retention: "session",
  sourceRefs: ["turn:deploy-001"],
  observedAt: "fixture-time",
};
```

```ts
const delta: GraphDelta = {
  deltaId: "gd-deploy-001",
  baseIndexVersion: "idx-000",
  sourceChanges: [{
    sourceRef: "archive:deployment-policy#rollback",
    newDigest: "sha256:fixture-policy-v1",
    change: "observed",
  }],
  nodeOps: [
    {
      op: "upsert",
      id: "task-goal:deploy",
      record: {
        id: "task-goal:deploy",
        kind: "TaskGoal",
        label: "Deploy the release",
        sourceRefs: ["archive:deployment-plan#release"],
        sourceDigests: ["sha256:fixture-plan-v1"],
        freshness: "current",
        contestation: "uncontested",
      },
      reason: "source-backed task goal",
    },
    {
      op: "upsert",
      id: "task-constraint:rollback",
      record: {
        id: "task-constraint:rollback",
        kind: "TaskConstraint",
        label: "Rollback support is required",
        sourceRefs: ["archive:deployment-policy#rollback"],
        sourceDigests: ["sha256:fixture-policy-v1"],
        freshness: "current",
        contestation: "uncontested",
      },
      reason: "source-backed deployment constraint",
    },
  ],
  edgeOps: [{
    op: "upsert",
    id: "edge:deploy-requires-rollback",
    record: {
      id: "edge:deploy-requires-rollback",
      from: "task-goal:deploy",
      to: "task-constraint:rollback",
      predicate: "requires",
      evidenceRefs: ["archive:deployment-policy#rollback"],
      evidenceDigests: ["sha256:fixture-policy-v1"],
      freshness: "current",
      contestation: "uncontested",
    },
    reason: "policy explicitly requires rollback support",
  }],
  invalidates: [],
  contradictions: [],
  resultIndexVersion: "idx-001",
};
```

The disposable index contains those two nodes and one `requires` adjacency. The bounded projection is:

```ts
{
  seedIds: ["task-goal:deploy"],
  nodeIds: ["task-goal:deploy", "task-constraint:rollback"],
  edgeIds: ["edge:deploy-requires-rollback"],
  sourceRefs: [
    "archive:deployment-plan#release",
    "archive:deployment-policy#rollback",
  ],
  graphVersion: "idx-001",
  hops: 1,
  truncated: false,
}
```

No current `Claim` supports `task-constraint:rollback`, so deterministic reasoning returns:

```ts
{
  operation: "find_missing_premise",
  outcome: "missing_premise",
  missingPremises: [{
    nodeId: "task-constraint:rollback",
    requiredByEdgeIds: ["edge:deploy-requires-rollback"],
  }],
}
```

- **Baseline answer without the vertical bundle:** “The deployment plan appears ready; verify operational details before proceeding.”
- **Improved bounded answer:** “I cannot recommend deployment yet: the retained policy requires rollback support, but the selected sources do not establish it. Please provide or verify rollback evidence.”

The presentation receipt reports `2 source records`, the match reason, selected dependency edge, missing premise, freshness/contestation, and zero claim that correction or persistence occurred.

Required reruns:

- exclude the policy for this turn → recomposition cannot use that dependency and must disclose reduced context;
- correct the ephemeral constraint → old handle tombstoned, new handle digest, cache miss;
- forget the handle → it is absent from the next request/prompt;
- memory off → no archive-derived graph context and a truthful degraded chip;
- pending source correction → source digest/result unchanged and `pending` visible;
- accepted source correction adding a source-backed rollback-support claim → changed digest, invalidation delta, rebuilt projection, and `outcome: "derived"`.

## Coherent operating envelope and executable measurements

All targets below are unverified until their named tests execute. [C-012]

| Boundary | v0 target | Executable measurement |
|---|---:|---|
| Projection | ≤24 nodes, ≤48 edges, 1 hop default/2 hard | `augmentor-reasoning-envelope-budget.test.mjs` |
| User handles | ≤8 | `augmentor-reasoning-envelope-budget.test.mjs` |
| Added source/graph prompt | ≤1,200 estimated tokens | `augmentor-reasoning-envelope-budget.test.mjs` |
| Total reasoning input | ≤2,000 estimated tokens | `augmentor-reasoning-envelope-budget.test.mjs` |
| Model calls | 0 or 1; no recursive loop | `augmentor-reasoning-envelope-budget.test.mjs` |
| Retrieval timeout | 800 ms hard | `augmentor-context-composition-benchmark.test.mjs` |
| Memory composition | p50 ≤150 ms; p95 ≤500 ms | `augmentor-context-composition-benchmark.test.mjs` |
| Direct-scan graph query | p95 ≤150 ms | `augmentor-semantic-index-benchmark.test.mjs` |
| Warm deterministic operation | p95 ≤20 ms | `bounded-reasoner-benchmark.test.mjs` |
| Complete optional model reasoning | p50 ≤1.5 s; p95 ≤4 s, excluding upstream provider congestion | `augmentor-reasoning-pipeline-benchmark.test.mjs` |
| Derived index/cache storage | ≤25 MB per measured fixture partition | `augmentor-semantic-index-storage.test.mjs` |
| Retrieval quality | Recall@5 ≥0.90; Precision@2 ≥0.80; MRR ≥0.85 | `augmentor-retrieval-quality.test.mjs` |

The measurement fixtures must record corpus size, warm/cold posture, token estimator, model/provider class or deterministic stub posture, and percentile sample count. Passing unit shape assertions alone does not verify latency or retrieval quality.

Start with validated canonical JSON and direct scan. Add an in-process adjacency index for repeated traversal. SQLite or a graph database remains contingent on measured v0/v1 pressure; it is not part of v0.

## Progressive-disclosure experience

- **Level 0:** `Memory: 2 sources`, `No relevant memory`, `Memory off`, `Partial`, or `Unavailable`.
- **Level 1:** source titles, kinds, freshness, contestation, and “matched because.”
- **Level 2:** bounded excerpts, source-qualified handles, selected graph paths, deterministic result, and residue.
- **Level 3:** Memory Workspace for source history, pending intake/review, and owner-routed source correction.

The default chat does not expose graph implementation, ontology governance, evaluator receipts, or private promotion language. [C-011]

## Degraded modes

- No `archive-read`: use transcript/page context and show `Memory off`.
- No match: say retrieval found no directly relevant item; never claim archive absence.
- Partial or stale result: use only admitted items and disclose omissions.
- Retrieval timeout: cancel at 800 ms and continue without archive context.
- Invalid/oversized projection: narrow or abstain; never remove required premises silently.
- Model failure or unsupported rationale claim: render the deterministic template.
- Semantic index unavailable: preserve existing Augmentor behavior and show `Reasoning context unavailable`.
- Correction intake unavailable: preserve a local draft and do not claim submission or persistence.

## Privacy and public/private boundaries

Never infer or persist sensitive traits, profession, personality, politics, health, class, or global ability. A transcript is not a user model; passive exposure is not mastery; a preference is not identity; a graph projection is not source truth; traversal is not reasoning; a model explanation is not evidence; evaluator output is not authorization. [C-005, C-009, C-010]

ResonantOS may implement generic DTOs, typed derived records, bounded traversal, deterministic operations, grounding validation, and user-facing presentation. It must not copy private CyberAlchemy vocabulary, authority snapshots, `CAV2-D*` terms, gate semantics, ACI bindings, or private receipt prose. The finite evaluator is an algorithmic precedent, not a shipped whole engine. [C-009, C-010]

## Implementation work order and verification

The complete v0 release bundle contains:

1. response `contextEnvelope`/presentation receipt and status chip;
2. one coordinator calling existing memory functions before provider execution and extending `buildAugmentorSystemPrompt`;
3. source-qualified read composition and disposable semantic index;
4. `find_missing_premise` deterministic operation plus grounded presentation/fallback;
5. context drawer and per-turn exclusion/session memory-off;
6. ephemeral handle correction/tombstone/forgetting;
7. pending versus accepted source-correction flows and digest invalidation;
8. the literal vertical fixture and all budget/latency/storage/quality tests.

Exact functional tests remain:

- `augmentor-context-composition-service.test.mjs`;
- extensions to `browser-first/host/augmentor-chat-contract.test.mjs`;
- `graph-delta.test.mjs`;
- `bounded-reasoner.test.mjs`;
- extensions to `memory-host-service.test.mjs`;
- context receipt renderer accessibility tests;
- browser journeys for missing premise, permission-off, timeout/partial, pending correction, accepted correction, turn exclusion, handle forgetting, memory-off, raw-source posture, and keyboard/focus behavior.

The v0 bundle is a design and verification target only. Nothing in this synthesis claims implementation, passing tests, measured budgets, promotion, or release.

## Remaining product decisions and residue

1. **Durable preference owner:** unresolved and deferred; v0 creates no host ledger or durable handle store.
2. **Accepted source correction owner/path:** intake exists, but the exact review-to-accepted-source transition must be bound before persistent correction is claimed.
3. **Index partition/location:** the index must be derived and disposable, but its exact workspace/user partition owner remains an implementation decision.
4. **Branch freshness:** Explorer 3 observed local product `dev` behind `origin/dev`; implementation must recheck current bytes first.
5. **Machine Inventory gap:** ResonantOS still has no product-local machine Inventory index; Inventory is discovery only.
6. **Performance and quality:** every numeric target remains unverified until the named executable measurement runs.
7. **Database adoption:** blocked absent measured direct-scan/adjacency failure.

## Evidence matrix

| Claim | Explorer | Exact repository-relative source path and selector | Posture | Scope and claim ceiling |
|---|---:|---|---|---|
| C-001 Alpha authority is browser-first; historical React/Tauri surfaces do not own the active route. | 3 | `../workspace-resonant/2.0.0-alpha/AGENTS.md`, selector `Alpha Runtime Boundary`; `../workspace-resonant/2.0.0-alpha/docs/architecture/MODULE-OWNERSHIP.md:108-117` | observed | Current local product bytes only; branch freshness must be rechecked. |
| C-002 Memory search/read already has a host owner, while the active chat contract does not carry archive/reasoning context. | 3 | `../workspace-resonant/2.0.0-alpha/browser-first/host/memory-host-service.mjs:80-91`; `../workspace-resonant/2.0.0-alpha/browser-first/host/provider-bridge-service.mjs:1122-1150`; `../workspace-resonant/2.0.0-alpha/browser-first/host/augmentor-chat-contract.mjs:20-49` | observed | Supports composition from existing owners; does not prove the coordinator. |
| C-003 Profile fields and Augmentor prompt are extension settings; durable preference memory is deferred. | 0, 3 | `../workspace-resonant/2.0.0-alpha/browser-first/resonantos-side-panel-extension/src/lib/personalization-settings.js:1-60`; `../workspace-resonant/2.0.0-alpha/docs/augmentor-future-list-acceptance-matrix.md:91-95` | observed | No provider-owned profile or v0 durable handle owner is established. |
| C-004 User/Translate/Guide is candidate development evidence, not installed runtime. | 0 | `arcanum/development/user-guide/README.md:12-19,137-153` | observed | Pattern evidence only. |
| C-005 Request/session handles must remain narrow, correctable, forgettable, and separate from identity and semantic graph knowledge. | 0 | `arcanum/development/user-guide/packages/user-ledger/VISIBILITY-POLICY.md:7-22`; `arcanum/development/user-guide/packages/user-ledger/RECEIPT-UPDATE-RULES.md:9-17,28-38` | inferred | Candidate-policy-derived product design; no runtime or durable-store claim. |
| C-006 One coordinator should call existing memory/provider functions and extend the sole prompt builder. | 3 | `../workspace-resonant/2.0.0-alpha/docs/architecture/MODULE-OWNERSHIP.md:19-29,119-138`; `../workspace-resonant/2.0.0-alpha/browser-first/host/provider-bridge-service.mjs:1122-1150` | inferred | New orchestration seam; not a new provider or prompt owner. |
| C-007 Semantic records/projections should be source-bound, typed, rebuildable, and non-authorizing. | 1 | `cyberAlchemy-v2/ontology/projections/README.md:6-10,21-50`; `cyberAlchemy-v2/ontology/NODE-MODEL.md:12-27`; `cyberAlchemy-v2/ontology/RELATION-MODEL.md:13-26,73-77` | inferred | Generic structural transfer only; private authority semantics remain excluded. |
| C-008 Stable typed records, endpoint/digest validation, conflict-visible projections, and grounding have exact precedents; the proposed GraphDelta lifecycle remains net-new. | 1 | `cyberAlchemy-v2/implementation/ontology-candidate-graph-prototype/src/contracts/candidate-v1.mjs:5-57,120-177,217-265,286-355`; `cyberAlchemy-v2/implementation/ontology-candidate-graph-prototype/src/projection/research-lineage.mjs:1-28`; `cyberAlchemy-v2/development/ontology-candidate-graph-prototype/design/VALIDATION-CONTRACTS.md:5-28`; `cyberAlchemy-v2/implementation/ontology-candidate-graph-prototype/src/evaluator/grounding.mjs:13-85` | inferred | Exact precedent closes shorthand residue; it does not prove GraphDelta, consumer invalidation, or Augmentor integration. |
| C-009 Current reusable reasoning precedent is a finite semantic evaluator, not a complete engine. | 2 | `cyberAlchemy-v2/development/agent-reasoning-engine/.craft/ledger.yml`, selectors `contexts[CTX-ARE-ROOT]`, `artifacts[ART-ARE-L0-WITNESS-RECEIPT]`; `cyberAlchemy-v2/development/agent-reasoning-engine/decisions/g-are-l0-promotion/PROMOTION-RECEIPT.json:36-44` | observed | Whole-engine/runtime/authorization claims prohibited. |
| C-010 Deterministic operation results must precede separately grounded optional presentation. | 2 | `cyberAlchemy-v2/development/agent-reasoning-engine/packages/semantic-judgment-evaluator/src/reducer.mjs:44-158,202-313,333-444`; `cyberAlchemy-v2/development/agent-reasoning-engine/design/COMPONENT-CONTRACTS.md:146-196` | inferred | Existing finite algorithms are precedent; registry, graph operations, union DTO, and presentation validator are net-new. |
| C-011 Alpha needs progressive context disclosure and user controls, adapting source-reference grammar without copying its storage model. | 3 | `projects/ide-ergonomics/knowledge-entry-references/SPEC.md:94-110,113-143,168-189`; `projects/ide-ergonomics/knowledge-entry-references/README.md:61-100` | inferred | Interaction grammar only; no Inventory/runtime dependency. |
| C-012 Numeric graph, token, latency, storage, and retrieval-quality values are executable acceptance targets. | 1, 2, 3 | `research/2026-07-28-authority-memory-augmentor-integration/research.md:236-248,454-465,616-638` | unverified | Remain unverified until each named measurement test executes with recorded fixture posture. |
| C-013 Turn exclusion, ephemeral-handle correction, pending source correction, and accepted source correction are distinct states. | 0, 3 | `../workspace-resonant/2.0.0-alpha/src/modules/chat/ContextMemoryPanel.tsx:55-97,116-124,157-208`; `../workspace-resonant/2.0.0-alpha/public/addons/augmentor-chat.json:137-155` | inferred | Historical UI and intake-only boundary are precedent; Alpha implementation remains new. |
| C-014 v0 should use direct scan/disposable adjacency and existing provider seams; database adoption requires measured pressure. | 1, 3 | `research/2026-07-28-authority-memory-augmentor-integration/research.md:225-250,556-576` | inferred | Architectural target only; no performance or database claim. |

## Evidence-closure posture

- C-001–C-004 and C-009 are observed only within their stated current-source ceilings.
- C-005–C-008, C-010–C-011, C-013–C-014 are design inferences, not implemented capabilities.
- C-008 now has exact repository paths, but the GraphDelta lifecycle remains explicitly net-new.
- C-012 remains unverified until all named executable measurements run.
- No claim here establishes implementation, human benefit, test passage, production readiness, authority promotion, or release.
