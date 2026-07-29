## Goal

Design the smallest useful, evolvable, and low-overhead architecture by which ResonantOS Augmentor can understand the user, retrieve a typed knowledge projection, and derive a bounded reasoning result while reusing existing ResonantOS memory and provider owners.

## TL;DR

Augmentor should compile a few explicit request/session user handles with existing Living Archive source records, ask the memory domain for a disposable source-bound graph projection, run one deterministic operation, and optionally explain that result with one grounded model call. The user-visible product is a better answer plus a quiet, inspectable account of the context used and controls to exclude, correct, forget, or disable it—not a graph browser, receipt console, second memory provider, durable host user ledger, or copy of private CyberAlchemy authority semantics. This is a design and verification target; no implementation, passing test, measured benefit, promotion, production readiness, or release is established.

## Context

The four investigations exposed a useful convergence across different constraints. Explorer 0 found candidate protected-handle and active-understanding patterns but no shipped user ledger; Explorer 1 found reusable typed-record and projection precedents but no consumer GraphDelta lifecycle; Explorer 2 found a promoted finite semantic evaluator but not a whole reasoning engine; Explorer 3 found the active browser-first host, existing memory search/read and prompt owners, but no archive context or reasoning presentation in the Alpha chat contract. The integration is therefore build-from-owned at its seams and net-new at its coordination, disposable index, operation DTOs, grounding validation, and user-control experience. [Explorer 0; `arcanum/development/user-guide/README.md:12-19,137-153`; C-004 observed] [Explorer 1; `cyberAlchemy-v2/ontology/projections/README.md:6-10,21-50`; C-007 inferred] [Explorer 2; `cyberAlchemy-v2/development/agent-reasoning-engine/.craft/ledger.yml`, selectors `contexts[CTX-ARE-ROOT]` and `artifacts[ART-ARE-L0-WITNESS-RECEIPT]`; C-009 observed] [Explorer 3; `../workspace-resonant/2.0.0-alpha/browser-first/host/augmentor-chat-contract.mjs:20-49`; C-002 observed]

## Product thesis

The smallest coherent feature is:

`explicit settings + ephemeral handles + owned source refs/digests → memory-owned disposable semantic index → bounded projection → one outcome-exclusive deterministic result → zero-or-one grounded presentation → visible user control`

Correction never flows backward from a model explanation into a trusted source. Retrieval and traversal select evidence; the deterministic operation derives the substantive result; the optional model call only explains it.

## Current versus missing

| Area | Current evidence | Missing design target |
|---|---|---|
| Alpha chat | Browser-first extension sends bounded transcript, page context, attachments, and explicit personalization through the active provider route. [Explorer 3; `../workspace-resonant/2.0.0-alpha/AGENTS.md`, `Alpha Runtime Boundary`; `docs/architecture/MODULE-OWNERSHIP.md:108-117`; C-001 observed] | Archive context, deterministic reasoning result, and presentation metadata in the active chat contract. |
| Source memory | Capability-gated memory search/read and intake already have host owners. [Explorer 3; `browser-first/host/memory-host-service.mjs:80-91`; C-002 observed] | One coordinator that calls those functions before provider execution and extends the sole prompt builder; no second provider or prompt owner. [Explorer 3; `docs/architecture/MODULE-OWNERSHIP.md:19-29,119-138`; `browser-first/host/provider-bridge-service.mjs:1122-1150`; C-006 inferred] |
| Personalization | Profile fields, Augmentor name, and free-form prompt are extension settings; durable preference memory is deferred. [Explorers 0, 3; `browser-first/resonantos-side-panel-extension/src/lib/personalization-settings.js:1-60`; `docs/augmentor-future-list-acceptance-matrix.md:91-95`; C-003 observed] | Request/session handles with inspect, correction, tombstone, and forgetting. v0 must not invent a durable owner. |
| Semantic access | Typed source-bound records, relations, projections, validation, and grounding have candidate precedents. [Explorer 1; `cyberAlchemy-v2/implementation/ontology-candidate-graph-prototype/src/contracts/candidate-v1.mjs:5-57,120-177,217-265,286-355`; `src/evaluator/grounding.mjs:13-85`; C-008 inferred] | Memory-owned disposable index and net-new GraphDelta/invalidation lifecycle. |
| Reasoning | The finite evaluator demonstrates deterministic conflict, missing-condition, cycle, precedence, residue, and replay atoms. [Explorer 2; `cyberAlchemy-v2/development/agent-reasoning-engine/packages/semantic-judgment-evaluator/src/reducer.mjs:44-158,202-313,333-444`; C-010 inferred] | Generic operation registry, outcome-discriminated consumer results, and separately grounded presentation. |
| Experience | Historical Context Memory and IDE Ergonomics provide inspect/edit and source-reference interaction grammar. [Explorers 0, 3; `../workspace-resonant/2.0.0-alpha/src/modules/chat/ContextMemoryPanel.tsx:55-97,116-124,157-208`; `projects/ide-ergonomics/knowledge-entry-references/SPEC.md:94-110,113-143,168-189`; C-011/C-013 inferred] | Alpha-native status chip, context drawer, per-turn exclusion, ephemeral-handle correction/forgetting, pending source correction, and memory-off rerun. |

## Non-collapsing layers and ownership

1. **Extension settings** remain explicit user-authored request inputs, never inferred traits.
2. **Owned source records** remain durable truth in Living Archive and current source owners. A graph record stores refs and digests, not copied source bytes.
3. **Ephemeral `UserHandle`s** live only in request/session scope in v0 and never become semantic graph nodes.
4. **Disposable semantic index** is owned by the existing memory domain/service. The coordinator and provider route consume bounded projections but do not own or mutate the index.
5. **Bounded projection** reports selected nodes/edges, source posture, freshness, contestation, omissions, truncation, and match reasons.
6. **Deterministic operation** returns exactly one operation-specific outcome. Traversal alone is not reasoning.
7. **`ReasoningPresentation`** may explain but cannot add premises, alter the outcome, or convert abstention into advice.
8. **Redacted presentation receipt** supports the status chip and drawer; it is supporting transparency, not authority.

This separation resolves the explorers’ central tension: user understanding improves selection and explanation without turning preference into identity; the graph improves reusable relation access without becoming source truth; reasoning adds typed semantic outcomes without relabeling retrieval; the host integration reuses current owners without duplicating memory or provider authority.

## Protected user handles

```ts
type BoundedText = string; // validated: 1..512 UTF-8 bytes
type BoundedLabel = string; // validated: 1..160 UTF-8 bytes
type BoundedSourceRefs = [string, ...string[]]; // validated: 1..4 unique refs

type HandleBase = {
  id: string;
  posture: "explicit" | "confirmed";
  retention: "request" | "session";
  sourceRefs: BoundedSourceRefs;
  observedAt: string;
  correctionOf?: string;
  tombstonedAt?: string;
};

type ExplicitUserHandle = HandleBase &
  (
    | {
        kind: "goal";
        value: {
          text: BoundedText;
          successCriteria: BoundedLabel[]; // 0..4
        };
      }
    | { kind: "rationale"; value: { text: BoundedText } }
    | {
        kind: "domain_anchor";
        value: {
          domain: BoundedLabel;
          nativeTerms: BoundedLabel[]; // 0..8
        };
      }
    | {
        kind: "vocabulary_preference";
        value: {
          canonicalTerm: BoundedLabel;
          preferredPhrase: BoundedLabel;
        };
      }
    | {
        kind: "failed_bridge";
        value: { bridgeId: BoundedLabel; reason: BoundedText };
      }
    | {
        kind: "constraint";
        value: {
          appliesTo: "recommendation" | "explanation";
          rule: "require_active_support";
          requirementRef: BoundedLabel;
        };
      }
  );

type ConceptStateHandle = {
  id: string;
  kind: "concept_state";
  value: {
    concept: BoundedLabel;
    state:
      | "unknown"
      | "exposed"
      | "clarified"
      | "practiced"
      | "transferable"
      | "mastered"
      | "stale";
  };
  posture: "explicit" | "confirmed" | "derived";
  retention: "request" | "session";
  evidence: Array<{
    kind: "teach_back" | "retrieval" | "contrast" | "transfer";
    sourceRef: string;
    observedAt: string;
  }>; // 1..8 when derived
  correctionOf?: string;
  tombstonedAt?: string;
};

type UserHandle = ExplicitUserHandle | ConceptStateHandle;
```

Only `concept_state` may be derived, and then only from one to eight named active-evidence records. A single utterance cannot become a durable preference, identity, sensitive trait, profession, personality, or global ability score. A failed analogy remains bridge residue, never an ability deficit. Every handle is visible, correctable, forgettable, and excluded from future composition after tombstoning. [Explorer 0; `arcanum/development/user-guide/packages/user-ledger/VISIBILITY-POLICY.md:7-22`; `RECEIPT-UPDATE-RULES.md:9-17,28-38`; C-005 inferred]

## Semantic index and GraphDelta

v0 uses validated canonical JSON plus direct scan; an in-process adjacency map is a disposable optimization. The compact graph admits only `Topic | Artifact | Claim | TaskGoal | TaskConstraint` and `about | supports | contradicts | requires | precedes | derived_from`. Every node carries source refs/digests, freshness, and contestation; every edge carries evidence refs/digests and the same orthogonal postures. `TaskGoal` and `TaskConstraint` describe source-backed object-domain work, not the user. `analogous_to` is not persisted: analogy selection is an operation over shared relation patterns and stated differences. [Explorer 1; `cyberAlchemy-v2/ontology/NODE-MODEL.md:12-27`; `RELATION-MODEL.md:13-26,73-77`; C-007 inferred]

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
      record?: never;
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
      record?: never;
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
  contradictions: Array<{ leftId: string; rightId: string; evidenceRefs: string[] }>;
  resultIndexVersion: string;
};
```

A stale base rejects and rebases. Source-digest changes stale or invalidate dependents. Contradictions coexist instead of overwriting claims. Same-ID/same-hash is idempotent; same-ID/different-hash remains an explicit conflict. Indexes and projections are rebuildable from current source records and accepted changes. These lifecycle rules are net-new and unimplemented even though stable IDs, endpoint/digest validation, and non-authorizing projection behavior have exact precedents. [Explorer 1; `cyberAlchemy-v2/development/ontology-candidate-graph-prototype/design/VALIDATION-CONTRACTS.md:5-28`; `cyberAlchemy-v2/implementation/ontology-candidate-graph-prototype/src/projection/research-lineage.mjs:1-28`; C-008 inferred]

## Bounded query, reasoning, and presentation

The operation registry admits `detect_conflict`, `find_missing_premise`, `select_analogy`, `order_task_dependencies`, and `compare_options`, each with an allow-listed predicate set and an outcome-exclusive result union. `invalid_context` and `abstained` carry non-empty errors or residue. A request binds the exact user turn, session-handle IDs and digest, index/projection versions, selected/excluded nodes and edges, limits, policy version, and context digest.

```ts
type ReasoningContext = {
  requestId: string;
  operation:
    | "detect_conflict"
    | "find_missing_premise"
    | "select_analogy"
    | "order_task_dependencies"
    | "compare_options";
  userTurn: string;
  sessionHandleIds: string[];
  userHandleDigest: string;
  indexVersion: string;
  projection: BoundedProjection;
  limits: { maxNodes: 24; maxEdges: 48; maxHops: 1 | 2 };
  excludedNodeIds: string[];
  excludedEdgeIds: string[];
  policyVersion: string;
  contextDigest: string;
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
};
```

Stage 1 validates and deterministically computes the result. Stage 2 is optional and receives only that normalized result, the smallest selected excerpts, the question, and explicit response-style input. Any rationale claim citing an unselected node/edge is rejected; model failure renders a deterministic template. The current evaluator’s finite algorithms are precedent, while graph reducers, operation registry, DTOs, user-handle admission, prompt compiler, grounding validator, budgets, cache, and ResonantOS adapter are all new. [Explorer 2; `cyberAlchemy-v2/development/agent-reasoning-engine/design/COMPONENT-CONTRACTS.md:146-196`; C-010 inferred]

## Literal vertical v0 witness

The v0 release unit is the whole vertical bundle, not any isolated schema, chip, graph view, or receipt.

Exact turn:

> Can I deploy this release today? Do not recommend it unless rollback support is verified.

The compiler creates session handle `uh-session-rollback`, kind `constraint`, rule `require_active_support`, requirement `task-constraint:rollback`, source `turn:deploy-001`, with digest `6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b`. It does not add the handle to the semantic index.

`gd-deploy-001` observes `archive:deployment-plan#release` and `archive:deployment-policy#rollback`, adds `task-goal:deploy`, adds `task-constraint:rollback`, and adds `edge:deploy-requires-rollback` with predicate `requires`; all record and evidence digests use the validated bare 64-character lowercase-hex wire format. Query `query:deploy-001` seeds `task-goal:deploy`, requires the handle, runs `find_missing_premise`, and projects exactly the two nodes and one edge at one hop.

The handle rule resolves its referenced `TaskConstraint` and searches only for a current, uncontested `Claim --supports--> TaskConstraint`. None exists, so the exact typed result is:

```ts
{
  operation: "find_missing_premise",
  outcome: "missing_premise",
  missingPremises: [{
    requirementNodeId: "task-constraint:rollback",
    requiredByEdgeIds: ["edge:deploy-requires-rollback"],
    supportSearchDisposition: "no_active_support"
  }]
}
```

Baseline: “The deployment plan appears ready; verify operational details before proceeding.”

Bounded answer: “I cannot recommend deployment yet: the retained policy requires rollback support, but the selected sources contain no active support showing that rollback is available. Please provide or verify rollback evidence.”

The drawer discloses two source records, match reason, selected dependency, missing premise, freshness/contestation, limits, and no false correction/persistence claim. Exclusion recomposes with reduced disclosed context; correcting the handle tombstones it and forces a digest/cache change; forgetting proves absence on the next request; memory-off omits archive-derived graph context; pending source correction leaves the source digest and result unchanged; accepted correction adds a source-backed support claim, invalidates/rebuilds the projection, and changes the exclusive result to `premises_satisfied`. This witness satisfies the non-vacuity gate as a specification, not as executed product evidence.

## Three end-to-end fixtures

| Fixture | Input through visible result | Required control proof |
|---|---|---|
| Deployment missing premise | The literal turn above creates one explicit session constraint, applies the source-bound delta, retrieves the two-node/one-edge projection, returns `missing_premise`, and changes the answer from generic readiness language to a refusal pending rollback evidence. | Exclude, correct, forget, memory-off, pending correction, and accepted correction each recompose the context and produce the specified distinct result/posture. |
| Repository onboarding through a known domain | User asks to understand a repository boundary “using logistics.” A session `domain_anchor` selects a source-backed structural analogy; `select_analogy` must report shared relation patterns and explicit differences. Augmentor keeps canonical terms beside the bridge and ends with one contrast/transfer check rather than inferring mastery. [Explorer 0; `arcanum/development/user-guide/packages/guide/GUIDE-TRANSLATE-INTEGRATION.md:7-23,34-48`; candidate-pattern basis] | Rejecting the bridge records only session `failed_bridge` residue; the next rerun must avoid it. No durable preference, profession, or ability claim is written. |
| Continuity and correction after compaction/provider change | Existing host-owned goal, rationale, artifact refs, and unresolved question recover the task; a failed prior bridge is excluded; source retrieval remains provider-independent; the bounded operation asks for the smallest missing evidence or transfer check. [Explorer 0; `../workspace-resonant/2.0.0-alpha/docs/architecture/ADR-016-context-memory-compaction.md:31-35,48-61,183-192`; observed basis, inferred integration] | Forgetting the handle removes it from the next composed request; memory-off preserves transcript/page-context behavior; a drafted source correction stays visibly pending until the source owner accepts it. |

## Operating envelope and exact measurements

All values are unverified acceptance targets until the named executable measurement runs with corpus size, operation count, warm/cold posture, token estimator, provider/stub posture, and percentile sample count recorded. [Explorers 1–3; `research.md:236-248,454-465,616-638`; C-012 unverified]

| Boundary | Target | Measurement |
|---|---:|---|
| Projection | ≤24 nodes, ≤48 edges; 1 hop default, 2 hard | `augmentor-reasoning-envelope-budget.test.mjs` |
| User handles | ≤8 | `augmentor-reasoning-envelope-budget.test.mjs` |
| Added source/graph prompt | ≤1,200 estimated tokens | `augmentor-reasoning-envelope-budget.test.mjs` |
| Total reasoning input | ≤2,000 estimated tokens | `augmentor-reasoning-envelope-budget.test.mjs` |
| Model calls | 0 or 1; no recursion | `augmentor-reasoning-envelope-budget.test.mjs` |
| Retrieval | 800 ms hard timeout; p50 ≤150 ms, p95 ≤500 ms | `augmentor-context-composition-benchmark.test.mjs` |
| GraphDelta | p95 ≤250 ms for ≤100 operations | `graph-delta-apply-benchmark.test.mjs` |
| Direct scan | p95 ≤150 ms | `augmentor-semantic-index-benchmark.test.mjs` |
| Deterministic operation | warm p95 ≤20 ms | `bounded-reasoner-benchmark.test.mjs` |
| Optional full reasoning | p50 ≤1.5 s, p95 ≤4 s excluding upstream congestion | `augmentor-reasoning-pipeline-benchmark.test.mjs` |
| Derived index/cache | ≤25 MB per measured fixture partition | `augmentor-semantic-index-storage.test.mjs` |
| Retrieval quality | Recall@5 ≥0.90; Precision@2 ≥0.80; MRR ≥0.85 | `augmentor-retrieval-quality.test.mjs` |

Direct scan and disposable adjacency remain the architectural target. SQLite or a graph database is blocked until measured latency, corpus, restart, or concurrency pressure shows that those approaches fail. [Explorers 1, 3; `research.md:225-250,556-576`; C-014 inferred]

## User experience, degraded modes, and privacy

The normal chat shows one quiet status: `Memory: 2 sources`, `No relevant memory`, `Memory off`, `Partial`, or `Unavailable`. Opening it reveals titles, kinds, freshness, contestation, and “matched because”; deeper disclosure adds bounded excerpts, source-qualified handles, selected paths, deterministic result, and residue; source history and durable correction remain in Memory Workspace. The user may exclude context for the current turn, correct or forget an ephemeral handle, disable memory for the session, or draft a source correction. A pending intake is not an accepted source change. [Explorer 3; `projects/ide-ergonomics/knowledge-entry-references/README.md:61-100`; C-011 inferred]

Degraded behavior is truthful and preserves the current path:

- no `archive-read` → transcript/page-context answer with `Memory off`;
- no match → “no directly relevant item,” never “the archive has none”;
- partial/stale → admit only usable items and disclose omissions;
- retrieval timeout → cancel at 800 ms and continue;
- invalid/oversized projection → narrow or abstain, never drop required premises silently;
- model or grounding failure → deterministic template;
- semantic index unavailable → current Augmentor behavior plus `Reasoning context unavailable`;
- correction intake unavailable → retain a local draft and claim neither submission nor persistence.

Privacy is structural: never infer or persist sensitive traits, profession, personality, politics, health, class, or global ability. A transcript is not a user model; exposure is not mastery; preference is not identity; graph projection is not source truth; traversal is not reasoning; model explanation is not evidence; evaluator output is not authorization. Generic DTOs, traversal, deterministic operations, grounding, and presentation may transfer into ResonantOS, but private CyberAlchemy vocabulary, authority snapshots, `CAV2-D*` terms, gate semantics, ACI bindings, and private receipt prose may not. [Explorers 0, 2; `arcanum/development/user-guide/packages/user-ledger/VISIBILITY-POLICY.md:7-22`; `cyberAlchemy-v2/development/agent-reasoning-engine/decisions/g-are-l0-promotion/PROMOTION-RECEIPT.json:36-44`; C-005/C-009]

## Implementation order

**v0 — complete verification target.** Refresh current `origin/dev` evidence, then deliver the response envelope/status chip, one host coordinator over existing memory/provider functions, memory-owned source-qualified direct-scan index, `find_missing_premise`, grounded presentation/fallback, drawer and turn/session controls, ephemeral correction/forgetting, pending-versus-accepted source correction, digest invalidation, literal deployment witness, and every named budget test. Partial steps are development increments, not releasable v0.

**v1 — broaden only after v0 measurement.** Add disposable in-process adjacency, projection cache, deterministic rebuild, contradiction display, and the remaining conflict/analogy/dependency/comparison operations with fixtures. Candidate relation proposals remain ranked suggestions; unknown predicates remain indeterminate.

**v2 — measured pressure only.** Consider SQLite or a graph-database adapter behind unchanged interfaces, temporal relations, explicit shared/private partitions, two-hop planning, and background compaction. No database adoption, durable preference store, whole reasoning engine, Logician, RecursiveMAS, private authority vocabulary, or product-local Inventory dependency belongs in v0.

## Verification suite

Functional and contract tests:

- `augmentor-context-composition-service.test.mjs`: ranking, bounded excerpts/tokens, source posture, degraded states, timeout, path redaction;
- `browser-first/test/augmentor-chat-contract.test.mjs`: delimited bounded memory block, prompt-injection resistance, permission-off omission, receipt/history separation;
- `graph-delta.test.mjs`: stale-base rejection, rebase, idempotency, same-ID conflict, digest invalidation, contradiction coexistence, deterministic rebuild;
- `bounded-reasoner.test.mjs`: exclusive unions, missing premise, cycle, conflict, structural analogy, option symmetry, abstention, replay, hallucinated-support rejection;
- `memory-host-service.test.mjs`: existing `archive-read` gate, intake-only correction, provider-owned forgetting;
- context-receipt renderer tests: all statuses, raw/stale badges, keyboard operation, focus return, and screen-reader labels.

Browser journeys must cover the literal missing-premise answer delta; permission-off; timeout/partial; pending then accepted source correction; turn exclusion; ephemeral-handle correction and forgetting; memory-off; raw-source posture; and keyboard/focus behavior. Each correction/forget/memory-off case must rerun composition and prove changed prompt/result bytes, not merely changed UI labels.

## Reviewer verdicts

| Gate | Final disposition | Closure carried into this blueprint |
|---|---|---|
| Lakatos — precedent and duplication | `FAIL_RESIDUE` only for a mechanical digest-wire mismatch; ownership and duplication blockers otherwise satisfied. | Mechanically closed without a third synthesis loop: all eight fixture digest literals in the controlling synthesis use bare 64-character lowercase hex and zero use a `sha256:` prefix. |
| Gödel — non-vacuity and visible benefit | `PASS` | Literal turn, handle binding, source-bound delta, bounded query, typed missing premise, answer delta, and control reruns are present. |
| Quine — non-collapse | `PASS` | User handles stay outside the graph; source memory, projection, deterministic result, optional presentation, and correction states remain distinct. |

## Supporting mechanics

The evidence closure is `ready` for this findings artifact only. Receipts record the frozen dispatch, evidence bindings, reviewer outcomes, and correction history; they do not become an Augmentor feature or establish implementation, test passage, measured budgets, authority, or release.

## Connections

- derives-from -> ./research.md

## Open Questions

- **OQ-1 (BLOCKER for durable preferences)** — Which existing owner, if any, may persist opt-in user preferences after v0? Recommendation: keep every v0 handle request/session-only and run a separate owner-selection decision before adding durable storage. Owner: ResonantOS product owner.
- **OQ-2 (BLOCKER for persistent correction claims)** — What exact review transition changes an intake draft into an accepted source record and digest? Recommendation: bind the current memory intake/review owner and executable transition before any UI says a source was corrected. Owner: ResonantOS memory-domain owner.
- **OQ-3** — What is the disposable index partition key across user, workspace, and shared sources? Recommendation: start with the narrowest workspace-scoped fixture partition, record privacy and cache behavior, and widen only from measured need. Owner: ResonantOS memory-domain owner.
- **OQ-4** — Do current `origin/dev` bytes alter the observed Alpha seams? Recommendation: fast-forward or inspect the refreshed branch before implementation and rerun module-ownership checks. Owner: ResonantOS integration owner.
- **OQ-5** — Do direct scan and in-process adjacency miss any latency, corpus, restart, or concurrency target? Recommendation: execute the named v0 benchmarks before selecting SQLite or a graph database. Owner: Augmentor performance owner.
- **OQ-6** — Does the complete vertical witness improve user outcomes rather than only technical traceability? Recommendation: after functional acceptance, run consented fixtures for time-to-useful-answer, correction friction, transfer success, boundary accuracy, control efficacy, and privacy regressions. Owner: Augmentor UX research owner.
