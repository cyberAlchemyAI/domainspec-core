# Candidate synthesis — Augmentor user understanding, graph, and bounded reasoning

## Product thesis

Augmentor should become more useful by composing a small, user-controlled set of protected handles with existing Living Archive records, materializing only the source-backed graph slice needed for the current question, deriving a typed bounded result, and showing the user what context changed the answer—without introducing a second memory provider, treating retrieval as reasoning, or presenting CyberAlchemy authority machinery as a ResonantOS feature. [C-001–C-011]

## Current versus missing capability

| Area | Current | Missing |
|---|---|---|
| Alpha chat | Browser-first extension sends bounded transcript, page context, attachments, and explicit system prompt to the provider host. [C-001] | No archive retrieval or reason metadata in the active chat contract. [C-002] |
| Memory | Existing host owns capability-gated search/read and intake; Personalization displays the active provider. [C-002] | One host-owned composition seam coordinating memory retrieval and provider invocation. [C-006] |
| Personalization | Explicit profile, Augmentor name, and free-form prompt exist. [C-003] | Default-off, enumerable, correctable preference memory remains deferred; session handles can precede it. [C-003, C-004] |
| User understanding | Candidate User/Translate/Guide artifacts define useful protected-handle and active-evidence patterns. [C-004] | Product-owned, minimal handles with consent, lifecycle, correction, forgetting, and stale semantics. [C-005] |
| Knowledge graph | CyberAlchemy supplies candidate typed record, relation, projection, and deterministic-validation precedents. [C-007] | A rebuildable query projection over existing records, with bounded deltas and invalidation. [C-007, C-008] |
| Reasoning | A private finite semantic evaluator has deterministic conflict, missing-condition, cycle, precedence, residue, and replay atoms. [C-009] | Generic bounded reasoning DTOs, graph operations, grounding validation, and ResonantOS adapter. [C-009, C-010] |
| User experience | Historical Context Memory UI demonstrates inspect/edit interaction vocabulary; IDE Ergonomics supplies source-reference disclosure grammar. [C-011] | Alpha-native status chip, context drawer, correction, per-turn exclusion, memory-off, and truthful degradation. [C-011] |

## Smallest coherent layer model

1. **Existing source and memory records**

   Living Archive pages, imported/raw evidence, explicit retained conversation records, project artifacts, and provider-owned profile/preferences remain with their current owners. A `SourceRef` points to them; graph records do not copy their full bytes. [C-002, C-007]

2. **Protected user handles**

   A small host-owned view contains only:

   - current goal, rationale, and success criteria;
   - confirmed domain anchor;
   - explicit vocabulary preference;
   - concept state supported by active evidence;
   - failed bridge/analogy to avoid;
   - current-turn constraints.

   Session-only is the default. Durable preference writes require explicit opt-in and the future preference-memory owner. Handles remain editable, staleable, and forgettable and never become semantic-graph identity nodes. [C-003–C-005]

3. **Rebuildable semantic graph**

   A disposable workspace-side projection contains selected source-backed nodes and relations. It is rebuilt from source references and accepted deltas; it is not another archive, user profile, or authority store. [C-007, C-008]

4. **Retrieved query projection**

   Each turn receives only the bounded subgraph relevant to the question, with omitted-item/truncation metadata, freshness, source posture, and “matched because.” [C-008]

5. **Reasoning result**

   Deterministic traversal and constraints produce conflicts, missing premises, dependency paths, option matrices, or abstention. One optional model call explains only those normalized results and must cite selected node/edge IDs. [C-009, C-010]

6. **Presentation receipt**

   A redacted response companion powers the status chip and context drawer. It supports transparency but is not the product narrative or a source of authority. [C-011]

Derivation direction is one-way:

`owned source records + consented handles → rebuildable graph → bounded projection → deterministic result → grounded explanation`

Corrections travel back to the relevant owner, invalidate derived graph/projection caches, and never mutate shared source knowledge merely by changing a user preference.

## Compact contracts

```ts
type UserHandle = {
  id: string;
  kind:
    | "goal"
    | "rationale"
    | "domain_anchor"
    | "vocabulary_preference"
    | "concept_state"
    | "failed_bridge"
    | "constraint";
  value: unknown;
  scope: "turn" | "thread" | "workspace" | "user";
  posture: "explicit" | "confirmed" | "derived";
  sourceRefs: string[];
  consent: "session_only" | "durable_opt_in";
  observedAt: string;
  staleAt?: string;
  correctionOf?: string;
};
```

`derived` is allowed only for narrow concept state backed by teach-back, retrieval, contrast, or transfer evidence. It must not encode occupation, personality, sensitive traits, or a global ability score. [C-005]

```ts
type GraphNode = {
  id: string;
  kind: "Topic" | "Artifact" | "Claim" | "Constraint" | "Task";
  label: string;
  sourceRefs: string[];
  sourceDigests: string[];
  status: "active" | "stale" | "contradicted" | "blocked";
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
  status: "active" | "stale" | "contradicted" | "blocked";
};
```

This deliberately removes a generic graph `Goal` from v0: the current user goal remains a protected handle, while project tasks and constraints may be source-backed graph nodes. `analogous_to` is not persisted in v0; analogy is derived from shared relation patterns and explicit differences. This reconciles the graph explorer’s compact vocabulary with the reasoning explorer’s non-collapse requirement. [C-005, C-007, C-010]

```ts
type GraphDelta = {
  deltaId: string;
  baseGraphVersion: string;
  sourceChanges: Array<{
    sourceId: string;
    oldDigest?: string;
    newDigest?: string;
    op: "upsert" | "retract";
  }>;
  nodeOps: Array<{ op: "upsert" | "retract"; id: string; beforeHash?: string }>;
  edgeOps: Array<{ op: "upsert" | "retract"; id: string; beforeHash?: string }>;
  invalidates: Array<{ targetId: string; reason: string; sourceRef: string }>;
  contradictions: Array<{ leftId: string; rightId: string; evidenceRefs: string[] }>;
  resultGraphVersion: string;
};
```

A stale base version fails and rebases; changed source digests stale dependents; contradictions coexist; same-ID/different-hash changes become explicit conflicts; indexes and projections remain disposable. [C-008]

```ts
type ReasoningContext = {
  requestId: string;
  operation:
    | "detect_conflict"
    | "find_missing_premise"
    | "select_analogy"
    | "order_task_dependencies"
    | "compare_options";
  question: string;
  userHandles: UserHandle[];
  projection: {
    nodes: GraphNode[];
    edges: GraphEdge[];
    graphDigest: string;
    truncation?: string[];
  };
  constraints: {
    maxNodes: number;
    maxEdges: number;
    maxHops: number;
    excludedNodeIds?: string[];
  };
  userHandleDigest: string;
  policyVersion: string;
};

type ReasoningResult = {
  requestId: string;
  outcome:
    | "derived"
    | "conflict"
    | "missing_premise"
    | "ambiguous"
    | "abstained"
    | "invalid_context";
  selectedNodeIds: string[];
  selectedEdgeIds: string[];
  paths: Array<{ edgeIds: string[]; conclusion: string }>;
  missingPremises: string[];
  conflicts: Array<{ left: string; right: string; edgeIds: string[] }>;
  options: Array<{
    id: string;
    satisfied: string[];
    violated: string[];
    unresolved: string[];
  }>;
  synthesis?: {
    answer: string;
    supportNodeIds: string[];
    supportEdgeIds: string[];
    caveats: string[];
  };
  residue: string[];
  deterministicDigest: string;
  cacheStatus: "miss" | "deterministic_hit" | "full_replay";
};
```

## End-to-end evolution loop

1. Receive the user turn and current explicit settings.
2. Load only consented/session handles and resolve bounded source candidates through the existing memory owner.
3. Produce proposed handle/source/graph deltas; do not accept inferred durable preferences automatically.
4. Validate consent, provenance, source digests, endpoints, allowed predicates, and budgets.
5. Apply accepted source changes through their existing owner; update only the rebuildable graph projection and cache.
6. Resolve at most a small seed set and materialize a one-hop projection, expanding to two hops only for a named reasoning operation.
7. Run deterministic conflict/gap/analogy/dependency/comparison logic.
8. If valid and useful, make one grounded synthesis call; otherwise return a deterministic explanation or abstention.
9. Render the answer with a quiet memory/context status chip.
10. Let the user inspect, exclude, correct, forget, or disable context.
11. Route correction to intake or the preference owner, invalidate the changed handle/source digest, and rebuild affected projections.

## Low-overhead operating envelope

These are proposed targets, not current measurements. [C-012]

| Boundary | v0 target |
|---|---|
| Exact seeds | ≤3 normal; ≤8 hard |
| Hops | 1 default; 2 hard maximum |
| Projection | ≤24 nodes, ≤48 edges, ≤5 displayed excerpts |
| User handles | ≤8 |
| Added graph/memory prompt | ≤1,200 estimated tokens |
| Total reasoning input | 2,000-token hard ceiling |
| Output | ≤500 tokens |
| Model calls | 0 or 1; no recursive loop |
| Direct-scan graph query | p95 ≤150 ms |
| Warm deterministic evaluation | p95 ≤20 ms |
| Memory composition | p50 ≤150 ms, p95 ≤500 ms, 800 ms hard timeout |
| Complete optional model reasoning | p50 ≤1.5 s, p95 ≤4 s, excluding upstream provider congestion |
| Derived graph/cache storage | ≤25 MB per workspace/user partition before compaction |
| Cache key | query + graph digest + handle digest + operation/policy version |

Start with canonical JSON plus direct scan. Add an in-process adjacency index when repeated traversal warrants it; adopt SQLite only on measured restart/rebuild or corpus pressure. A graph database is v2-only and requires demonstrated latency, concurrency, or corpus-size failure.

## Progressive-disclosure experience

- **Level 0:** `Memory: 2 sources`, `No relevant memory`, `Memory off`, `Partial`, or `Unavailable`.
- **Level 1:** source titles, kinds, freshness, and “matched because.”
- **Level 2:** bounded excerpts, source-qualified handles, authority/source posture, selected graph paths, and any unresolved conflict.
- **Level 3:** open Memory Workspace for source history, intake review, correction, and provider-owned forgetting.

Controls:

- exclude this item from the current turn;
- disable memory for this chat;
- propose a correction without directly rewriting trusted memory;
- forget a session handle immediately;
- route persistent removal to the owning provider with explicit confirmation;
- enumerate and reset durable preferences once that capability is activated.

The normal chat never exposes graph databases, ontology governance, evaluator receipts, or internal promotion language. [C-011]

## Three fixture-backed journeys

1. **Architecture onboarding through a known domain**

   The user asks for an explanation using logistics. A session domain anchor seeds a small dependency projection. Structural analogy selection explains the shared pattern and where it breaks, then asks one contrast/transfer question. A failed bridge is retained only for the session unless the user explicitly asks to remember it.

2. **Deployment planning with a missing premise**

   A retained task requires rollback support, but no active source-backed claim establishes it. The bounded reasoner returns `missing_premise`; the model cannot recommend deployment. The answer names the missing evidence, and the context drawer shows the dependency path. A user correction creates intake, invalidates the old digest, and re-evaluates.

3. **Recovery after compaction or provider switch**

   Host-owned goal, rationale, decisions, artifact refs, and open questions restore continuity. Retrieval finds two source-backed claims that conflict. Augmentor displays both instead of blending them, explains their freshness/provenance, and lets the user exclude or correct one without changing canonical shared knowledge.

## Degraded modes

- No `archive-read`: use transcript/page context and show `Memory off`.
- No match: say retrieval found no directly relevant item; never claim archive absence.
- Partial/stale result: use only valid items and disclose omissions; stale items are excluded by default.
- Retrieval timeout: cancel and continue without memory.
- Invalid/oversized graph: narrow or abstain; never compact away required premises.
- Model failure or ungrounded citation: return the deterministic template.
- Graph unavailable: preserve existing Augmentor behavior and show `Reasoning context unavailable`.
- Correction write unavailable: retain a local draft and route to Memory Workspace; do not claim persistence.

## Privacy and anti-profiling boundary

Never infer or persist sensitive traits, profession, personality, politics, health, class, or global ability. A transcript is not a user model; passive exposure is not mastery; a single utterance is not a durable preference; failed analogy is not deficiency; user-local terminology cannot mutate canonical knowledge. Default-off durable preference memory, visible freshness, enumerable values, correction, reset, and prompt-state absence after forgetting are acceptance requirements. [C-003–C-005]

## Public/private transfer boundary

ResonantOS may implement generic DTOs, typed graph records, bounded traversal, conflict/gap operations, grounding validation, and user-facing explanations. It must not copy private CyberAlchemy vocabulary, authority snapshots, `CAV2-D*` terms, gate semantics, promotion claims, ACI bindings, or private receipt prose. The private semantic evaluator is implementation precedent for finite algorithms, not a shipped whole-engine dependency or authorization source. [C-009, C-010]

## Implementation increments

- **v0a — truthful context surface:** extend the chat response with a redacted context envelope and render the five-state chip; no retrieval.
- **v0b — existing-memory read composition:** add one host composition service coordinating the existing memory and provider owners under hard budgets.
- **v0c — inspect and control:** context drawer, source posture, matched-because, per-turn exclusion, and session memory-off.
- **v0d — one substantive reasoned journey:** direct-scan graph projection plus `find_missing_premise`, deterministic fallback, and grounding validation.
- **v0e — correction loop:** intake-only source correction, session-handle correction/forgetting, digest invalidation, deterministic re-evaluation.
- **v1 — broader bounded reasoning:** conflict, structural analogy, dependency order, comparison, adjacency cache, stale/contradiction handling, and fixture telemetry.
- **v2 — measured scale only:** optional SQLite/graph adapter, deeper temporal queries, partitions, and background compaction after v1 budget failures are demonstrated.

Durable preference memory is not smuggled into v0; it waits for its explicit default-off/resettable owner.

## Exact verification targets

Unit and contract tests:

- `augmentor-context-composition-service.test.mjs`
  - existing-owner retrieval only;
  - deterministic statuses;
  - two-page/three-snippet and token caps;
  - timeout cancellation;
  - source posture/freshness/matched-because;
  - private-path redaction.
- Extend `augmentor-chat-contract.test.mjs`
  - delimited injection-resistant context block;
  - absent without permission;
  - receipt excluded from authored message history.
- `graph-delta.test.mjs`
  - stale base, endpoint failure, deterministic rebuild, contradiction coexistence, digest invalidation, tombstone, idempotent replay.
- `bounded-reasoner.test.mjs`
  - missing premise, explicit conflict, cycle abstention, structural analogy, symmetric option matrix, stale evidence, hallucinated support-ID rejection, deterministic replay.
- Extend `memory-host-service.test.mjs`
  - existing `archive-read` gate;
  - correction remains intake-only;
  - persistent forgetting cannot bypass ownership.
- `personalization-memory-controls.test.mjs`
  - durable preferences default off, enumerable, removable, resettable.

Browser acceptance:

- known fixture → chip → exact source and match reason;
- missing rollback premise → no recommendation, visible dependency path;
- archive permission disabled → answer still succeeds truthfully;
- timeout/partial read → responsive degraded answer;
- correction → intake receipt, trusted source unchanged, next projection invalidated;
- forget-for-turn → regenerated answer excludes item;
- raw-only hit → visible non-authority badge;
- keyboard/ARIA drawer and focus return;
- restart continuity without claiming durable preference memory.

Proposed quality targets—unverified until fixture execution—are Recall@5 ≥0.90, Precision@2 ≥0.80, MRR ≥0.85, 100% displayed sources with ref/freshness/posture/match reason, zero false persistence/use claims, and zero default-off durable writes.

## Conflicts and residue preserved for reviewers

1. **Graph vocabulary conflict:** Explorer 1 proposes graph `Goal`; Explorer 0 treats goal/rationale as protected user state. Candidate resolution: user goals remain handles; only source-backed `Task`/`Constraint` enter v0 graph.
2. **Reasoning edge conflict:** Explorer 2 proposes `analogous_to` and `instantiates`; Explorer 1’s v0 predicates omit them. Candidate resolution: derive analogy structurally in v0; do not persist these relations until fixtures prove need.
3. **Budget conflict:** Explorers propose 24/48 versus 32/64 graph ceilings and 1,200 versus 2,000–3,500 prompt budgets. Candidate resolution: adopt the stricter 24/48 and 1,200 contribution, with 2,000 total reasoning hard ceiling.
4. **Runtime ownership residue:** Historical `ContextMemoryState` is useful interaction precedent but is not Alpha runtime authority.
5. **Inventory residue:** ResonantOS has no product-local machine Inventory index; Inventory entries remain discovery leads, not runtime dependencies.
6. **Freshness residue:** Explorer 3 observed local `dev` seven commits behind `origin/dev`; implementation must recheck/fast-forward before modifying the consumer.
7. **Measurement residue:** All numeric latency, storage, token, and retrieval-quality targets are unverified until executed against fixture and browser runs.
8. **Exact-path residue:** Several Explorer 1 citations abbreviate repository paths with `.arcanum/...` or `implementation/...`; those cannot support evidence closure without explorer clarification.

## Evidence matrix

| Claim | Explorer | Exact repository-relative source path and selector | Posture | Scope and ceiling |
|---|---:|---|---|---|
| C-001 Alpha authority is browser-first; historical React/Tauri surfaces do not own the active route. | 3 | `../workspace-resonant/2.0.0-alpha/AGENTS.md`, selector `Alpha Runtime Boundary`; `../workspace-resonant/2.0.0-alpha/docs/architecture/MODULE-OWNERSHIP.md:108-117` | observed | Current local product bytes only; branch is behind origin. |
| C-002 Memory search/read already has a host owner, while active chat composition does not retrieve it. | 3 | `../workspace-resonant/2.0.0-alpha/browser-first/host/memory-host-service.mjs:80-91`; `../workspace-resonant/2.0.0-alpha/browser-first/host/provider-bridge-service.mjs:1122-1150`; `../workspace-resonant/2.0.0-alpha/browser-first/contracts/augmentor-chat-contract.mjs:20-49` | observed | Supports build-from-owned coordination; does not prove proposed service. |
| C-003 Current personalization is explicit settings only; preference memory is deferred/default-off/resettable. | 0, 3 | `../workspace-resonant/2.0.0-alpha/browser-first/resonantos-side-panel-extension/src/lib/personalization-settings.js:1-60`; `../workspace-resonant/2.0.0-alpha/docs/augmentor-future-list-acceptance-matrix.md:91-95` | observed | Durable preference implementation remains missing. |
| C-004 User/Translate/Guide is candidate development evidence, not installed runtime. | 0 | `arcanum/development/user-guide/README.md:12-19,137-153` | observed | Pattern evidence only; no ResonantOS runtime claim. |
| C-005 Protected handles must remain narrow, consented, correctable, forgettable, and separate from identity/graph knowledge. | 0 | `arcanum/development/user-guide/packages/user-ledger/VISIBILITY-POLICY.md:7-22`; `arcanum/development/user-guide/packages/user-ledger/RECEIPT-UPDATE-RULES.md:9-17,28-38` | inferred | Product design derived from candidate policy; not shipped. |
| C-006 One host composition seam should coordinate existing memory and provider owners. | 3 | `../workspace-resonant/2.0.0-alpha/docs/architecture/MODULE-OWNERSHIP.md:19-29,119-138` | inferred | Ownership recommendation; exact service name is new. |
| C-007 Graphs/projections should be source-bound, typed, rebuildable, and non-authorizing. | 1 | `cyberAlchemy-v2/ontology/projections/README.md:6-10,21-50`; `cyberAlchemy-v2/ontology/NODE-MODEL.md:12-27`; `cyberAlchemy-v2/ontology/RELATION-MODEL.md:13-26,73-77` | inferred | Transfers generic structure only; private authority semantics stay out of consumer. |
| C-008 Incremental deltas should stale dependents, preserve contradictions, and keep projections disposable. | 1 | `cyberAlchemy-v2/ontology/projections/README.md:21-50` | inferred | Underlying executable citation was abbreviated; exact implementation support is unverified. |
| C-009 Current reusable reasoning precedent is a finite semantic evaluator, not a complete engine. | 2 | `cyberAlchemy-v2/development/agent-reasoning-engine/.craft/ledger.yml`, selectors `contexts[CTX-ARE-ROOT]`, `artifacts[ART-ARE-L0-WITNESS-RECEIPT]`; `cyberAlchemy-v2/development/agent-reasoning-engine/decisions/g-are-l0-promotion/PROMOTION-RECEIPT.json:36-44` | observed | Only promoted finite capability; whole-engine/runtime claims prohibited. |
| C-010 Deterministic traversal must precede grounded optional synthesis, with typed residue and abstention. | 2 | `cyberAlchemy-v2/development/agent-reasoning-engine/packages/semantic-judgment-evaluator/src/reducer.mjs:44-158,202-313,333-444`; `cyberAlchemy-v2/development/agent-reasoning-engine/design/COMPONENT-CONTRACTS.md:146-196` | inferred | Algorithms are precedent; graph traversal and model grounding are net-new. |
| C-011 Alpha needs progressive context disclosure and correction/forget controls, adapting source-reference grammar without copying its storage model. | 3 | `projects/ide-ergonomics/knowledge-entry-references/SPEC.md:94-110,113-143,168-189`; `projects/ide-ergonomics/knowledge-entry-references/README.md:61-100` | inferred | Interaction grammar only; ResonantOS lacks product-local machine Inventory. |
| C-012 Numeric graph, prompt, latency, storage, and quality budgets are initial acceptance targets. | 1, 2, 3 | `research/2026-07-28-authority-memory-augmentor-integration/research.md:236-248,454-465,616-638` | unverified | Must not be reported as measured until unit/browser fixtures execute. |
| C-013 User correction must route through intake/provider ownership; compact or derived state cannot silently rewrite trusted source records. | 0, 3 | `../workspace-resonant/2.0.0-alpha/src/modules/chat/ContextMemoryPanel.tsx:55-97,116-124,157-208`; `../workspace-resonant/2.0.0-alpha/public/addons/augmentor-chat.json:137-155` | inferred | Historical panel is UX precedent; Alpha correction implementation remains new. |
| C-014 v0 must use direct scan and existing provider seams; database adoption is contingent on measured pressure. | 1, 3 | `research/2026-07-28-authority-memory-augmentor-integration/research.md:225-250,556-576` | inferred | Architectural recommendation, not benchmark evidence. |

## Proposed reviewer input

Review the candidate against these kill conditions:

- **Lakatos:** prove whether the host composition service, handle view, graph sidecar, prompt compiler, context drawer, and reasoning adapter duplicate an existing owner. Treat a found owner as simplification, not failure. Require exact replacement/extension points.
- **Gödel:** require Journey 2 to execute end to end: explicit user constraint → accepted small handle/source change → typed graph delta → bounded query → `missing_premise` → visibly changed answer → inspect/correct/forget → measured overhead. Kill receipt-only, schema-only, hidden-profile, or unmeasured-model slices.
- **Quine:** attack any collapse among identity, preference, concept evidence, archive record, graph claim, retrieval, deterministic derivation, model explanation, and authorization. In particular, test the candidate resolution that user goals remain handles, analogy is derived rather than persisted in v0, and evaluator reuse does not import private authority semantics.

Evidence closure should remain `needs_feedback` for C-008’s abbreviated implementation citations and `unverified` for C-012’s budgets until the explorer supplies exact selectors or implementation fixtures execute.
