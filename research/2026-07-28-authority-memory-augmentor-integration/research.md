## Agent 0 — protected user understanding

# Explorer report — smallest useful Augmentor user-understanding model

## Status boundary

**Observed:** The Arcanum User/Translate/Guide corpus is explicitly a candidate pattern and development evidence; it neither creates runtime user state nor proves promotion or installation. [`arcanum/development/user-guide/README.md:12-19,137-153`; candidate evidence]

**Observed:** ResonantOS currently has editable identity/Augmentor prompt settings and structured per-thread compact memory, but opt-in preference memory with reset is still deferred. [`browser-first/resonantos-side-panel-extension/src/lib/personalization-settings.js:1-16,23-35`; `.../settings/personalization-section.js:110-147,282-304`; `docs/augmentor-future-list-acceptance-matrix.md:91-95`]

Therefore the model below is an **inferred integration target**, not a shipped capability.

## Minimal user-model schema

```ts
type UserUnderstanding = {
  schemaVersion: 1;
  scope: "thread" | "workspace" | "user";
  consent: {
    durablePreferenceMemory: boolean; // default false
  };
  intent: {
    goal: string;
    why: string;
    successCriteria: string[];
    prioritySignals: string[];
    sourceRefs: string[];
  };
  handles: Array<{
    id: string;
    kind:
      | "domain_anchor"
      | "vocabulary_preference"
      | "concept_state"
      | "failed_analogy";
    subject: string;
    value: string;
    state?: "unknown" | "exposed" | "clarified" | "practiced"
          | "transferable" | "mastered" | "stale";
    evidence: {
      type: "explicit_user" | "teach_back" | "retrieval"
          | "transfer" | "contrast" | "failed_bridge";
      sourceRefs: string[];
      observedAt: string;
    };
    lifecycle: "session" | "durable" | "stale";
    editable: true;
    forgettable: true;
  }>;
  activeEvidence: {
    recentTurns: string[];
    artifactRefs: string[];
    openQuestions: string[];
  };
};
```

This is deliberately smaller than the candidate ledger: omit `profile_seed`, user glossary, receipt rows, promotion state, and generalized “facts about the user” from the first user-facing model. Receipts can remain internal proposed-update envelopes because the candidate contract says Guide/Translate propose while the ledger owns accepted writes, and bounded summaries—not transcripts—are preferred. [`arcanum/development/user-guide/packages/user-ledger/DESIGN.md:59-68,79-91`; `USER-LEDGER-SCHEMA.yml:152-173,233-241`; observed]

The existing `ContextMemoryState.userIntent`, facts, preferences, tasks, artifact references, risks, questions, sources, timestamp, and checksum provide the continuity substrate; Augmentor should add typed learning handles beside it rather than overload free-text preferences. [`src/core/contracts.ts:2646-2689,2706-2730`; observed]

## Handle policy

| Handle | Lifecycle and control |
|---|---|
| User intent and rationale | **Session/workspace durable**, source-linked, editable, forgettable. Never derive `why` from a task list: it is first-class. [`docs/architecture/ADR-016-context-memory-compaction.md:48-60`; observed] |
| Domain anchor | **Session-only by default**; durable only after explicit user confirmation/opt-in. Mark stale after disuse or contradictory evidence. Editable and forgettable. The candidate requires confidence and evidence, but an inferred occupation or identity must never become the anchor. [`packages/user-ledger/USER-LEDGER-SCHEMA.yml:83-103`; observed contract, inferred lifecycle] |
| Vocabulary preference | **Session-only by default**; optionally durable under #236 consent. Explicit/source-linked, editable, resettable, forgettable. Never infer personality, ability, politics, health, class, or identity from wording. [`packages/user-ledger/VISIBILITY-POLICY.md:7-22`; `docs/...acceptance-matrix.md:91-95`; observed boundary] |
| Concept state | **Derived**, evidence-linked, narrow to named concept and purpose; staleable, editable, forgettable. Passive “I understand” reaches at most `clarified`; teach-back, retrieval, transfer, or contrast can support higher states. [`packages/user-ledger/RECEIPT-UPDATE-RULES.md:9-17,28-38`; observed candidate rule] |
| Failed analogy | **Session residue by default**; durable only as an explicit “avoid this bridge” preference. Forgettable and never converted into an ability deficit. [`packages/user-ledger/MASTERY-FIXTURES.md:71-90`; `VISIBILITY-POLICY.md:19-22`; observed] |
| Active evidence | **Session-only/ephemeral prompt input**: current source turns, artifacts, unresolved questions, recent demonstrations. Recompute rather than profile. [`src/core/contracts.ts:2706-2729`; inferred use from observed state] |
| Identity/contact | Keep in existing explicit settings, not the understanding model. Never use email/subtitle to infer expertise or preferred pedagogy. [`browser-first/.../personalization-settings.js:1-5,23-28`; observed settings, inferred prohibition] |
| Sensitive traits or global “user ability score” | **Never inferred or stored.** The candidate goal is better explanation, not diagnosis, and `clarification_turns` is explicitly friction rather than ability. [`packages/user-ledger/DEFINE.md:14-20,35-43`; `DESIGN.md:87-91`; observed] |

## How the handles improve one turn

**Inferred from observed contracts:**

1. Read the current `goal`, `why`, success criteria, priorities, artifacts, and unresolved questions before choosing an explanation route. This prevents a fluent but irrelevant answer. ResonantOS already injects these compact-state fields into the prompt. [`src/core/context-memory.ts:550-571`; observed]
2. Select one confirmed domain anchor and vocabulary preference; request a Translate-style bridge that includes the target-domain definition and where the analogy breaks. [`packages/translate/DEFINE.md:14-33`; `packages/guide/GUIDE-TRANSLATE-INTEGRATION.md:7-23,34-48`; observed candidate contract]
3. Use concept state to skip established primitives but revisit stale or merely exposed ones.
4. Avoid recorded failed analogies.
5. End with one active-evidence prompt appropriate to the user’s goal—contrast, transfer, retrieval, or teach-back—not a UI-heavy receipt. Guide’s candidate responsibility includes an active-evidence prompt and only a proposed update. [`packages/guide/DESIGN.md:29-38,56-78`; observed]

## Adaptation loop

**Inferred design:**

`frame intent → load consented handles + active evidence → choose anchor/terms → explain target truth + mapping limit → ask one active check → classify evidence → show a small “remember this?” control only when durable memory would help → accept/edit/reject/forget → mark stale when evidence ages or conflicts`

The current Context Memory Panel already proves the useful interaction model: users can inspect and edit intent, rationale, summary, facts, decisions, preferences, and tasks; edits affect compact memory while raw transcript remains intact. [`src/modules/chat/ContextMemoryPanel.tsx:55-97,116-124,157-208`; observed] Destructive reset/clear must require confirmation. [`docs/architecture/ADR-016-context-memory-compaction.md:242-260`; observed]

## Three Augmentor journeys

1. **Repository onboarding:** User asks to understand an architecture “using logistics.” Augmentor uses logistics as a session anchor, explains dependency boundaries through staged handoffs, states where the analogy fails, then asks the user to identify what must not cross the boundary. A correct contrast proposes `clarified`/`transferable`; no durable write occurs without opt-in. [`README.md:103-133`; observed candidate journey, inferred Augmentor integration]

2. **Cross-functional planning:** A product lead prefers outcome language and dislikes “pipeline.” Augmentor translates the current technical workflow into stakeholder outcomes while retaining canonical technical terms alongside the bridge. On explicit approval, “prefer outcome language; retain native term in parentheses” becomes a forgettable durable preference; it does not become a claim about profession or competence. [`README.md:85-99`; `VISIBILITY-POLICY.md:17-21`; observed basis, inferred journey]

3. **Recovery after compaction/provider switch:** A long thread resumes with goal, why, decisions, artifacts, open tasks, and recent turns preserved. Augmentor notices an earlier analogy failed, avoids it, retrieves the linked artifact, and asks a short transfer question before assuming mastery. This uses host-owned structured continuity rather than provider memory. [`ADR-016-context-memory-compaction.md:31-35,48-61,183-192`; observed basis, inferred journey]

## Privacy and anti-profiling failure tests

- Preference memory enabled or written before explicit opt-in.
- A single utterance becomes a durable anchor, trait, or expertise claim.
- User-authored text is marked “verified” merely because the user said it; current deterministic extraction does exactly this for candidate facts and is unsafe for sensitive profile claims. [`src/core/context-memory.ts:313-335`; observed risk]
- Keyword matching mistakes “I need…” for a durable preference; current extraction is heuristic and workstream-wide. [`src/core/context-memory.ts:352-361`; observed risk]
- Failed analogy becomes “low ability,” “beginner,” or other deficiency label.
- Passive agreement becomes mastery.
- Stale handles continue shaping answers without visible freshness.
- Forget/reset removes compact handles but silently leaves equivalent durable archive/profile state.
- Raw transcripts are copied into learning records instead of source-linked bounded evidence.
- A user-local definition silently mutates canonical knowledge.
- Receipt machinery dominates the UI; the user should see understandable controls—why this adaptation happened, edit, don’t remember, forget—not internal proposal plumbing.

## Measurable user benefits

Run consented A/B fixtures and measure:

- **Time to useful answer:** turns until the user says the explanation is actionable.
- **Clarification friction:** follow-up corrections per target concept; treat as route friction, never ability.
- **Transfer success:** percentage of users who correctly apply the concept to a new example.
- **Boundary accuracy:** percentage who can state both where the analogy works and breaks.
- **Continuity recovery:** required facts/intent/rationale retained after compaction or provider switch, with source validity.
- **Adaptation precision:** accepted durable suggestions ÷ all suggestions; separately track edited/rejected suggestions.
- **Control efficacy:** reset/forget tests prove the handle no longer appears in future prompt state or adaptation.
- **Privacy regressions:** zero durable preference writes while default-off; zero sensitive-trait inference fixtures.
- **Staleness safety:** stale/contradicted handles used in zero subsequent routes without reconfirmation.

These metrics establish user benefit and control; they do not prove shipped runtime readiness until #236’s default-off and reset tests exist and pass. [`docs/augmentor-future-list-acceptance-matrix.md:91-95`; observed]

## Agent 1 — incremental knowledge graph

## Explorer report — smallest evolvable graph substrate for Augmentor

### Recommendation

Use a rebuildable, query-driven semantic sidecar over existing source and memory records: canonical JSON records plus an optional in-process adjacency index. Do not introduce a graph database or graph every file/conversation.

This is consistent with the observed ontology boundary: projections are read models and create no authority; candidate records must remain source-bound, challengeable, and owner-routed; branches are views, not node types or lifecycle states. [`ontology/projections/README.md:6-10`; `NODE-MODEL.md:12-27`; `BRANCH-AS-VIEW.md:6-24` — **observed**]

### Four non-collapsing layers

1. **SourceRecord — existing evidence/memory owner**

   ```ts
   {
     sourceId, sourceKind, locator, selector?, digest,
     capturedAt, validFrom?, validTo?, privacyScope, owner
   }
   ```

   This is the durable referent: document selector, user-authored memory record, decision, or conversation segment explicitly selected for retention. A transcript is not automatically a graph node.

2. **UserHandle — protected host-owned personalization**

   ```ts
   {
     handleId, userId, kind: "goal"|"preference"|"known-domain"|"constraint",
     valueRef, confidence, provenance, consent, validUntil?, correctionOf?
   }
   ```

   Store only explicit or user-confirmed handles. Keep them outside the semantic graph so preference does not become identity, exposure does not become mastery, and forgetting does not require ontology mutation. This separation is **inferred** from the requirement to avoid a second memory/profile system; the source model supports it by distinguishing source context from promoted meaning. [`PACKAGE-MODEL.md:14-19,32-54` — **observed basis**]

3. **SemanticGraph — rebuildable claims and typed relations**

   ```ts
   Node {
     id, kind, label, sourceRefs[], sourceDigests[],
     ownerRoute, status, confidence,
     useGuidance, invalidationRoute, authorityEffect: "none"
   }

   Edge {
     id, from, predicate, to, evidenceRefs[],
     status: "active"|"stale"|"contradicted"|"blocked",
     confidence, validFrom?, validTo?,
     ownerRoute, authorityEffect: "none"
   }
   ```

   Product-facing v0 node kinds should be only `Topic`, `Goal`, `Constraint`, `Artifact`, and `Claim`; predicates only `about`, `supports`, `contradicts`, `depends_on`, and `derived_from`. Each edge must name endpoints, direction, owner, evidence, and effect or remain residue. [`RELATION-MODEL.md:13-26,73-77` — **observed**]

   Reuse the executable candidate carrier’s hard properties: exact fields, stable IDs, repository-relative selectors, source digests, resolved endpoints, duplicate rejection, challenge metadata, and `authority_effect:none`. [`implementation/.../candidate-v1.mjs:5-57,120-177,217-265,286-355` — **observed**]

4. **Projection — ephemeral query result**

   ```ts
   {
     projectionId, queryHash, graphVersion, seedRefs[],
     nodeIds[], edgeIds[], sourceRefs[],
     allowedUse, blockedUse, generatedAt, staleAfter?,
     truncation, explanation
   }
   ```

   A projection is the only graph-shaped object injected into Augmentor. It is derived, cacheable, discardable, and must report omitted nodes and limits. This follows the authored projection contract and executable research-lineage precedent. [`ontology/projections/README.md:21-50`; `src/projection/research-lineage.mjs:1-28` — **observed**]

### Incremental `GraphDelta`

```ts
GraphDelta {
  deltaId, baseGraphVersion, producedAt, producerVersion,
  sourceChanges: [{sourceId, oldDigest?, newDigest?, op:"upsert"|"retract"}],
  nodeOps: [{op:"upsert"|"retract", id, beforeHash?, record?, reason}],
  edgeOps: [{op:"upsert"|"retract", id, beforeHash?, record?, reason}],
  invalidates: [{targetId, reason, sourceRef}],
  contradictions: [{leftId, rightId, evidenceRefs[], disposition:"visible"|"blocked"}],
  diagnostics: [],
  resultGraphVersion
}
```

Rules:

- Reject if `baseGraphVersion` is not current; rebase by replaying against the latest source snapshot.
- IDs are content-stable logical IDs, while record hashes detect concurrent edits.
- Apply source changes first, then retract invalid dependents, validate endpoints/predicate policy, then materialize affected projections.
- A changed source digest marks dependent nodes/edges `stale`; it does not silently delete or rewrite them.
- Contradictions coexist as explicit edges and appear in retrieval; they do not overwrite either claim. The current implementation already keeps `contradicts` visible but outside derivation closure. [`research-lineage.mjs:16-27`; `.arcanum/...ontology-working-prototype...md:104-121` — **observed**]
- Merge independent operations by stable ID. Same-ID/same-hash is idempotent; same-ID/different-hash becomes a merge conflict requiring deterministic precedence or review.
- Retraction tombstones remain through one rebuild epoch so stale caches and explanations can identify why context disappeared.
- Unknown relation policy is `indeterminate`, never implicit admission; the implemented `specializes` witness establishes this behavior. [`VALIDATION-CONTRACTS.md:15-17` — **observed**]

### Storage and query strategy

| Strategy | Best use | Cost/risk |
|---|---|---|
| Direct scan of validated JSON | v0; up to roughly 10k nodes / 50k edges | Simplest rebuild/debug path; linear per query |
| In-memory adjacency + property maps | v1 default; repeated bounded traversal | O(N+E) rebuild, near O(visited subgraph) query; no new durable owner |
| SQLite tables/indexes | v1.5 if restart/rebuild or corpus size becomes measurable pain | Transactional deltas and indexes, still operationally small |
| Graph database | v2 only after measured multi-tenant, deep-path, or concurrent-write need | Adds migration, access-control, backup, and query-language burden without improving small-subgraph semantics |

Direct-scan-first has current precedent: the Akashic candidate design explicitly retains only source/claim records and direct query joins, with no persisted edge file, graph index, or graph database. That proposal is unexecuted and unaudited, so it is design evidence only. [`.arcanum/...akashic-periodic-table...md:62-92,99-111,118-129` — **observed**]

### Initial budgets

These are **inferred engineering targets**, not current measured guarantees:

- Seed resolution: ≤8 exact handles; semantic fallback ≤3 candidate seeds.
- Traversal: default 1 hop, maximum 2; never unrestricted.
- Retrieved subgraph: ≤24 nodes, ≤48 edges, ≤12 source excerpts.
- Prompt contribution: target ≤2,000 tokens; hard ceiling 3,500.
- Local retrieval: p95 ≤50 ms with warm adjacency index; ≤150 ms direct scan.
- Graph-delta validation/application: p95 ≤250 ms for ≤100 operations.
- Projection cache: keyed by `{queryHash, graphVersion, user-handle-version}`.
- Per-user semantic graph storage: target ≤25 MB before compaction; source bytes remain in their owning store, not duplicated.
- If any ceiling is exceeded: truncate by predicate priority, confidence, recency, and source diversity; return truncation metadata and optionally fall back to existing retrieval.

The “sub-50 ms” read path appears only as a candidate Inventory hypothesis with uncosted ingest/maintenance and non-zero grounding residue; it must not be presented as verified. [`.arcanum/...resonantos-and-ontology-retrieval...md:48-67,94-99` — **observed caveat**]

### Retrieval examples

**Goal-aware answer**

Seed `UserHandle(goal="learn categorical deep learning")`; exact link to `Topic`; traverse one hop over `depends_on` and `supports`; select at most six claims with diverse sources. Projection explanation: “Used your confirmed learning goal plus six source-backed prerequisites.”

**Conflict surfacing**

Seed the artifact currently discussed; traverse `about` then `contradicts`. Return both claims and source selectors. Augmentor says: “Two retained sources disagree; here are their dates and provenance,” rather than merging them into one answer.

**Missing premise**

Seed a task/goal; traverse `depends_on`. If a dependency has no supporting active claim or artifact, emit a gap, not an invented fact.

**Correction and forgetting**

A user correction creates a new UserHandle version plus retraction of the old handle. Semantic source claims remain unchanged. Cached projections keyed to the old handle version become invalid. Forgetting user context deletes/tombstones host-owned handles and derived per-user links; it does not delete shared source records.

### Rebuild and migration

- Durable truth is source records plus reviewed deltas; indexes and projections are disposable.
- Full rebuild: read current source snapshot → validate records → deterministically sort nodes/edges → rebuild adjacency maps → recompute only pinned smoke-test projections → compare semantic checksums.
- Every graph record carries `schemaVersion`; migrations are pure `vN -> vN+1` transforms with fixture snapshots and rollback by rebuilding the prior version.
- Preserve old predicates until queries migrate; translate at projection time rather than rewriting all sources immediately.
- Golden fixtures must cover unresolved endpoints, wrong direction, cycles, forbidden authority effect, persisted inverse edges, contradictions outside derivation closure, stale source digest, conflicting deltas, and deterministic rebuild. Current prototype supplies the first six patterns and deterministic adjacency traversal precedent. [`VALIDATION-CONTRACTS.md:5-28`; `grounding.mjs:13-85` — **observed**]

### Evolution path

**v0 — useful sidecar**

Direct-scan validated records; explicit user handles; 1-hop, ≤24-node projections; inspect/correct/forget UI; no graph DB, learned edge creation, authority effect, or transcript-wide extraction.

**v1 — incremental and measurable**

`GraphDelta`, dependency invalidation, in-memory adjacency indexes, projection cache, contradiction display, deterministic rebuild, latency/token telemetry, and fixture-backed Augmentor journeys. Candidate relation proposals may be ranked, but unknown predicates remain indeterminate.

**v2 — only from measured pressure**

SQLite or graph database adapter behind the same interfaces; temporal edges, shared/private graph partitions, 2-hop planning queries, background compaction, and optional semantic seed grounding. Database adoption requires evidence that v1 misses latency, concurrency, or corpus-size budgets. Promotion, authority decisions, and canonical ontology remain separate owner routes throughout. [`README.md:12-18`; `PACKAGE-MODEL.md:56-88` — **observed**]

The key product constraint is simple: graph only selected, source-backed claims needed by named Augmentor queries. The Inventory guidance explicitly rejects converting every Markdown file or index row into a node and recommends bounded graphs only where typed multi-hop traversal, invalidation, contradiction, branch comparison, or impact analysis requires them. [`.arcanum/...ontology-population-from-inventory-synthesis.md:31-45,47-92,129-149` — **observed**]

## Agent 2 — bounded reasoning support

## Explorer report — bounded reasoning support for Augmentor

### Bottom line

**Observed:** The only promoted executable capability is the private, finite `semantic-judgment evaluator@1`; the whole reasoning engine, integrated ACI runtime, real effects, and anti-bias efficacy are explicitly unpromoted and unauthorized. The current next route is plan revision, with no selected downstream SWU. (`cyberAlchemy-v2/development/agent-reasoning-engine/.craft/ledger.yml`, selectors `contexts[CTX-ARE-ROOT]`, `artifacts[ART-ARE-L0-WITNESS-RECEIPT]`; `decisions/g-are-l0-promotion/PROMOTION-RECEIPT.json:36-44`; `decisions/aci-reasoning-binding/BINDING-RECEIPT.json:36-51`)

**Inferred recommendation:** Give Augmentor a small hybrid reasoning service that performs deterministic graph selection and constraint analysis, then bounded model synthesis. Call the consumer capability “reasoning support” or “bounded reasoner,” not “the Agent Reasoning Engine.” Its substantive witness is machine-readable context → repository-defined traversal/constraint operations → typed derived result, satisfying the accepted non-vacuity test without inflating orchestration, retrieval, or the current evaluator. (`.arcanum/inventory/entries/cyberalchemy-orchestrator-reasoning-engine-purpose-strategy-result-synthesis.md:109-122`, discovery-only; `.arcanum/inventory/entries/agent-reasoning-engine-contract-strategy-result-synthesis.md:56-76`, discovery-only)

## Proposed contracts

```ts
type ReasoningContext = {
  schemaVersion: "0.1";
  requestId: string;
  operation:
    | "detect_conflict"
    | "find_missing_premise"
    | "select_analogy"
    | "order_task_dependencies"
    | "compare_options";
  question: string;
  userHandles: Array<{
    id: string;
    kind: "goal" | "constraint" | "vocabulary" | "concept_state" | "failed_bridge";
    value: unknown;
    posture: "declared" | "corrected" | "derived";
    sourceRef: string;
    staleAt?: string;
  }>;
  subgraph: {
    nodes: Array<{
      id: string;
      kind: string;
      label: string;
      sourceRefs: string[];
      posture: "source" | "user_declared" | "derived";
    }>;
    edges: Array<{
      id: string;
      from: string;
      to: string;
      kind:
        | "supports"
        | "conflicts_with"
        | "requires"
        | "precedes"
        | "analogous_to"
        | "instantiates";
      sourceRefs: string[];
      strength?: "explicit" | "derived";
    }>;
  };
  constraints: {
    maxNodes: number;
    maxEdges: number;
    maxHops: number;
    requiredPremises?: string[];
    excludedNodeIds?: string[];
  };
  graphDigest: string;
  userHandleDigest: string;
  policyVersion: string;
};
```

```ts
type ReasoningResult = {
  schemaVersion: "0.1";
  requestId: string;
  operation: ReasoningContext["operation"];
  outcome:
    | "derived"
    | "conflict"
    | "missing_premise"
    | "ambiguous"
    | "abstained"
    | "invalid_context";
  deterministic: {
    selectedNodeIds: string[];
    selectedEdgeIds: string[];
    paths: Array<{ edgeIds: string[]; conclusion: string }>;
    conflicts: Array<{ left: string; right: string; edgeIds: string[] }>;
    missingPremises: string[];
    candidateOptions: Array<{
      id: string;
      satisfied: string[];
      violated: string[];
      unresolved: string[];
    }>;
  };
  synthesis?: {
    answer: string;
    rationaleClaims: Array<{
      text: string;
      supportNodeIds: string[];
      supportEdgeIds: string[];
    }>;
    caveats: string[];
  };
  residue: string[];
  contextDigest: string;
  deterministicDigest: string;
  model?: { providerClass: string; modelId: string; promptVersion: string };
  cacheStatus: "miss" | "deterministic_hit" | "full_replay";
};
```

**Observed basis:** Existing contracts already distinguish a `ProblemFrame` containing questions/handles from accepted facts, require immutable input digests, preserve residue, and produce exactly one typed outcome plus a derivation. (`design/COMPONENT-CONTRACTS.md:146-176`; `packages/semantic-judgment-evaluator/src/receipt.mjs:15-59`)

**Inferred boundary:** `ReasoningContext` is consumer-facing and generic. It must not expose `CAV2-D*`, `GateDecision`, authority snapshots, private catalog wording, or private receipt semantics. A private adapter may translate generic records into evaluator inputs where an owned finite rule family applies, but ResonantOS owns only the generic request/result DTO and presentation.

## Two-stage reasoning

### Stage 1 — deterministic traversal and constraints

1. Validate schema, digests, unique IDs, bounded size, and edge endpoints.
2. Select seeds from the question, explicitly selected user handles, and requested operation.
3. Traverse only allow-listed edge kinds to `maxHops`; produce a stable node/edge order.
4. Run operation-specific logic:
   - **Conflict:** find explicit `conflicts_with` edges and incompatible supported conclusions; unresolved equal candidates yield `conflict`.
   - **Missing premise:** walk `requires` edges and report absent/unresolved nodes.
   - **Analogy:** require a shared relation pattern plus explicit differences; rank by matched structural features, never embedding similarity alone.
   - **Task dependency:** topologically order `requires`/`precedes`; cycles yield `conflict` or `abstained`.
   - **Option comparison:** evaluate each option against the same declared constraints and return satisfied/violated/unresolved sets.
5. If evidence is missing, cyclic, stale, or contradictory beyond pinned precedence, stop with typed residue before any model call.

**Observed reuse:** The reducer already supplies digest/schema rejection, cycle detection, transitive precedence, finite comparisons, missing-condition extraction, defeater/exception handling, unresolved conflict escalation, and a deterministic derivation. (`packages/semantic-judgment-evaluator/src/reducer.mjs:44-158, 202-313, 333-444`)

**Inferred net-new work:** Typed graph traversal, graph-pattern analogy scoring, dependency DAG production, symmetric option matrices, user-handle admission, staleness handling, and operation-specific result serialization are new. They should not be forced into the current flat field/rule evaluator.

### Stage 2 — model synthesis

The model receives only the normalized deterministic result, the smallest supporting node excerpts, the user’s current question, and response-style preferences. It may explain, compare, or suggest the next question; it may not add premises, change selected paths, resolve conflicts silently, or turn `abstained` into advice.

Validate model output by requiring every rationale claim to cite node/edge IDs present in Stage 1. If validation fails, return the deterministic result with a plain template response.

**Observed constraint:** A synthesizer may structure returns but cannot convert disagreement into support or decide applicability; loop ceilings retain residue. (`design/DECISION-AND-EFFECT-FLOW.md:113-120`) The evaluator itself makes no actor/tool calls. (`design/COMPONENT-CONTRACTS.md:169-196`)

## Cache, replay, and fallback

**Inferred cache keys:**

- Deterministic key: `hash(operation + normalized question selectors + graphDigest + userHandleDigest + constraints + policyVersion)`.
- Synthesis key: deterministic key plus `modelId + promptVersion + response-style digest`.
- Never cache across changed graph/user digests, corrected/forgotten handles, changed policy, or stale source versions.

Historical replay may reuse the exact stored subgraph and deterministic result. Model replay is only “full replay” if the exact prior prompt input and output are retained; otherwise reuse Stage 1 and regenerate synthesis, labeled as a new synthesis. Current revalidation must rebuild the subgraph and use a new request ID.

**Observed basis:** Existing replay reproduces deterministic receipt bytes and tracks zero provider/effect calls; current revalidation is explicitly distinct from historical replay. (`packages/semantic-judgment-evaluator/src/replay.mjs:5-22`; `design/COMPONENT-CONTRACTS.md:226-234`; `design/DECISION-AND-EFFECT-FLOW.md:122-130`)

**Fallback ladder:**

1. Full two-stage response.
2. Model failure/timeout → deterministic template with paths, gaps, conflicts, and residue.
3. Graph unavailable → existing Augmentor retrieval/prompt path, explicitly “reasoning context unavailable.”
4. Invalid or oversized context → abstain and offer a narrower question.
5. No support → ask for the smallest missing premise; do not fabricate an analogy or winner.

## Initial budgets

These are **inferred product budgets**, not observed current guarantees:

- 2–3 seeds, ≤2 hops.
- ≤32 nodes, ≤64 edges.
- ≤8 user handles; never bulk conversation history.
- ≤1,200 input tokens for graph facts and paths, ≤500 for user/question/instructions, ≤500 output tokens.
- Hard prompt ceiling: 2,000 input tokens; deterministic fallback if compaction would remove required premises.
- Stage 1 target ≤20 ms p95 in-memory / direct scan; complete reasoning-support target ≤1.5 s p50 and ≤4 s p95 excluding upstream retrieval.
- One model call; no recursive model loop in v0.
- Cache deterministic results by content digest; cap each stored result to the selected IDs, paths, typed findings, and digests rather than copied source prose.

## Evaluation fixtures

1. **Preference conflict:** user declares “concise answers,” later explicitly requests a detailed tutorial. Expect conflict surfaced and current-turn instruction selected without rewriting the durable preference.
2. **Missing premise:** deployment option requires rollback support, but the subgraph lacks it. Expect `missing_premise`, zero model recommendation, and a request for rollback evidence.
3. **Analogy selection:** two analogies share keywords, only one shares the same `requires → failure mode → mitigation` structure. Expect structural analogy selected and differences stated.
4. **Dependency cycle:** A requires B, B requires C, C requires A. Expect cycle path and abstention, not an invented order.
5. **Option comparison:** options A/B evaluated against identical latency, privacy, and reversibility constraints; unresolved fields remain unresolved and cannot count as wins.
6. **Contradictory sources:** equal-posture source nodes support incompatible claims with no precedence. Expect `conflict`/`abstained`; adding an explicit precedence edge changes only the selected path.
7. **User correction/cache invalidation:** correction changes one user-handle digest. Expect deterministic cache miss and absence of the forgotten value in the model prompt.
8. **Model hallucination:** synthesis cites an absent node. Validator rejects synthesis and returns Stage 1 template.
9. **Replay:** identical context reproduces byte-identical deterministic output with zero provider calls.
10. **Second domain:** the same engine code handles both task dependencies and learning-analogy fixtures, preventing a fixture-specific conditional.

**Observed precedent:** Current tests already cover two independently owned rule families, missing facts, defeaters, timeout, irrelevant-consensus invariance, unresolved conflict/precedence, temporal drift, persistence order, idempotency, and byte-identical replay. (`packages/semantic-judgment-evaluator/test/evaluator.test.mjs:35-256, 276-404`; `fixtures/evaluator-v1/refund-eligibility.json`, selectors `rules`; `fixtures/evaluator-v1/release-readiness.json`, selectors `rules`)

## Reuse versus net-new

**Reusable current atoms (observed):**

- Canonical serialization, sealing, content digests, and atomic persistence.
- Stable typed outcome/residue patterns.
- Cycle and transitive-precedence algorithms.
- Missing-required-fact, defeater, exception, and conflict handling.
- Immutable derivation and receipt assembly.
- Historical deterministic replay and revalidation separation.
- Zero-effect/non-authorizing claim ceiling.

(`src/reducer.mjs:44-158, 333-444`; `src/receipt.mjs:15-59`; `src/replay.mjs:5-22`; `design/COMPONENT-CONTRACTS.md:198-208`)

**Net-new engine pieces (inferred):**

- Generic `ReasoningContext`/`ReasoningResult`.
- Small-subgraph selector and traversal executor.
- User-handle adapter and correction/forget invalidation.
- Operation registry for conflict/gap/analogy/dependency/comparison.
- Deterministic-to-model prompt compiler.
- Grounding validator for synthesized claims.
- Budget enforcement, cache manager, fallback templates, and consumer telemetry.
- ResonantOS host adapter and visible “why this context”/correction experience.
- Fixture corpus proving user-visible benefit across operations.

Do not reuse the current effect dispatcher or ACI binding in the first Augmentor slice: the binding only selects a future ACI-subordinate ownership disposition, while compatibility and runtime readiness remain false. (`decisions/aci-reasoning-binding/BINDING-RECEIPT.json:26-51`)

## Agent 3 — Augmentor experience and host integration

## Explorer 3 report — ResonantOS-native Augmentor memory experience

### Scope/current branch

- **Observed:** The product authority is the browser-first Alpha: MV3 extension plus authenticated loopback Node bridge. The React/Tauri-era `src/` surfaces are historical/design evidence, not Alpha route ownership (`AGENTS.md`, “Alpha Runtime Boundary”; `docs/architecture/MODULE-OWNERSHIP.md:108-117`).
- **Observed:** Local `dev` is seven commits behind `origin/dev`. The incoming commits only harden Agent Control live certification and public-submit safety; none changes Augmentor chat, memory, personalization, or archive routes (`git diff --name-status HEAD..origin/dev`; commits `328d8ac..3b07e63`).
- **Inferred:** `origin/dev` drift does not change this investigation’s scope or conclusions, though implementation should begin after fast-forwarding to current `dev`.

### Current vs missing capability matrix

| Capability | Current | Missing |
|---|---|---|
| Replaceable Augmentor UI | **Observed:** Augmentor Chat supplies rail, floating window, and settings surfaces and occupies replaceable `primary-agent`/`chat-interface` slots (`public/addons/augmentor-chat.json:8-28,112-126`). | **Inferred:** No per-turn memory disclosure surface exists in the active Alpha UI. |
| Memory boundary | **Observed:** `archive-read` degrades rather than hard-stops; trusted-page writes are forbidden and chat writes are intake-only (`public/addons/augmentor-chat.json:43-53,137-155`). | **Inferred:** Need explicit “answered without memory” and partial-retrieval UI, not silent omission. |
| Active memory system | **Observed:** Personalization displays the active memory add-on, curated-page/intake/source counts, and links to Memory Settings/Workspace (`personalization-section.js:150-175,222-259`). | **Observed:** Personalization stores only profile, Augmentor display name, and free-form system prompt (`personalization-settings.js:1-60`). Preference memory is explicitly deferred, opt-in, resettable, and non-profiling (`docs/augmentor-future-list-acceptance-matrix.md:91-95`). |
| Chat composition | **Observed:** The extension sends bounded transcript history, page context, attachments, and user system prompt to `/augmentor/chat` (`chat-turn-controller.js:90-138`). The provider host immediately builds request messages; it performs no archive retrieval (`provider-bridge-service.mjs:1122-1150`). | **Observed:** No host-composed memory context, retrieval receipt, citations, or reason metadata enters the Alpha chat contract (`augmentor-chat-contract.mjs:20-49`). |
| Archive retrieval | **Observed:** The bridge already owns capability-gated `/memory/search` and `/memory/wiki/page/read` (`memory-host-service.mjs:80-91`); memory policy belongs to `memory-host-service`/`memory-*`, while provider invocation belongs to provider services (`MODULE-OWNERSHIP.md:23-29`). | **Inferred:** Missing orchestration between those existing owners. Creating another provider would duplicate authority. |
| Context continuity | **Observed:** The historical `ContextMemoryState` models intent, facts, preferences, decisions, tasks, artifacts, risks, unresolved questions, provenance IDs, and checksum (`src/core/contracts.ts:2706-2730`). Its panel supports correction while preserving raw transcript and visualizes prompt layers (`ContextMemoryPanel.tsx:55-97,122-145,157-220`). | **Inferred:** Useful UX vocabulary, but porting this React component or compact-state store directly into Alpha would violate runtime ownership. |
| Explainable knowledge reference | **Observed:** The IDE proposal requires source-qualified handles, bounded snippets, freshness, authority boundary, source refs, residue, and “matched because”; it forbids promotion or synthesis from cache alone (`knowledge-entry-references/SPEC.md:94-110,113-143,168-189`). | **Inferred:** ResonantOS lacks machine Inventory, so Inventory/ontology-specific integration is discovery only. Reuse the interaction grammar against Living Archive hits, not its storage model. |

### One host-owned composition seam

**Inferred recommendation:** Add exactly one `augmentor-context-composition-service.mjs` under `browser-first/host/`, invoked by `provider-host-service` before `executeBridgeChat` builds provider messages.

It should:

1. Receive normalized latest user turn, surface, granted capabilities, active-memory identity, and a retrieval budget.
2. Call the existing memory host/search-and-read seam—never instantiate another memory provider.
3. Return a bounded `contextEnvelope`:

```text
status: used | no-match | disabled | unavailable | partial
query
items[]: {handle, title, kind, snippet, sourceRef, freshness, authority, score, matchedBecause}
failures[]
timingMs
estimatedTokens
```

4. Format a clearly delimited memory-evidence system block and append it in `buildAugmentorSystemPrompt`.
5. Return a redacted `contextReceipt` alongside the assistant response for UI rendering.

**Why host-owned:** Extension surfaces may read bounded bridge results but cannot own host filesystem/provider state (`MODULE-OWNERSHIP.md:19-21`); provider and memory policies already have distinct host owners (`:26-29`). The composition service coordinates them without moving either authority. Any new bridge contract must name its capability and focused test (`:119-138`).

### Default UX and progressive disclosure

**Inferred default:**

- Every answer gets a quiet footer chip: `Memory: 2 sources used`, `No relevant memory`, `Memory off`, or `Memory unavailable`.
- Clicking opens a “Context used” drawer:
  - “What Augmentor knows”: retrieved claims grouped as trusted page vs raw/imported evidence.
  - “Why used”: query plus plain “matched because” explanation.
  - “Sources”: title, bounded excerpt, source-qualified handle, freshness, authority boundary.
  - “Correct”: creates an editable correction draft and submits only to Living Archive intake/review; it never rewrites trusted memory directly.
  - “Forget”: removes the item from this turn immediately, then offers the existing reversible source/archive-management route; destructive source deletion requires explicit confirmation.
  - “Don’t use memory for this chat” session toggle.
- Settings-level preference memory remains **off by default**. Enabling it explains scope, shows every stored preference, and provides “reset all preferences.”

**Progressive disclosure:**

1. Level 0: one status chip.
2. Level 1: titles, kinds, match reason, freshness.
3. Level 2: bounded excerpts, source refs, authority/residue.
4. Level 3: open Memory Workspace for source history, review, correction, or forgetting.

This adapts the IDE reference-popup grammar—visibility and reuse without authority promotion (`knowledge-entry-references/README.md:61-74,76-100`)—to the Living Archive.

### Degraded modes

- **No `archive-read`:** answer from transcript/page context; chip says “Memory off—permission not granted.”
- **No active provider/unavailable bridge:** answer normally; say memory was unavailable, with retry/settings action.
- **No match:** do not imply absence from the archive; say retrieval found no directly relevant item.
- **Partial read:** use successful items, list failed count, never fabricate missing content.
- **Stale item:** badge stale; exclude by default unless user expands/opts in.
- **Budget/latency exceeded:** cancel retrieval and answer without it; receipt says “Skipped to keep response responsive.”
- **Raw/imported hit only:** show “source evidence—not trusted page,” matching the existing historical formatting boundary (`src/modules/chat/archive-context.ts:186-224`).
- **Correction/forget write unavailable:** preserve local draft and route user to Memory Workspace; do not claim persistence.

### Implementation increments

1. **Receipt-only foundation:** define `contextEnvelope/contextReceipt`, extend chat contract response, render status chip; no retrieval yet.
2. **Read composition:** service calls existing `/memory/search`/read logic with strict count/character/time budgets and authority labels.
3. **Inspectable drawer:** source handles, freshness, matched-because, bounded excerpts, open-source action.
4. **Control:** per-turn exclusion and session memory-off toggle.
5. **Correction:** intake-only correction proposal with receipt and review link.
6. **Forgetting:** detach-from-turn first; then explicit reversible provider-owned source action.
7. **Opt-in preferences:** only after issue #236 is activated; default-off, enumerable, individually removable, reset-all.

### Exact tests to add

**Unit/contract**

- `augmentor-context-composition-service.test.mjs`
  - ranks exact title/handle above tag/summary; emits `matchedBecause`;
  - caps two documents, excerpt bytes, and estimated tokens;
  - distinguishes trusted page/raw source and preserves freshness/residue;
  - returns each degraded status deterministically;
  - timeout aborts retrieval and does not block provider call;
  - redacts absolute/private paths from the client receipt.
- Extend `augmentor-chat-contract.test.mjs`
  - memory block is delimited, bounded, and resistant to source prompt injection;
  - no block when permission is absent;
  - receipt never enters user-authored message history.
- Extend `memory-host-service.test.mjs`
  - composition read uses existing `archive-read` gate;
  - correction uses intake/review capability; forgetting cannot bypass provider ownership.
- `augmentor-context-receipt-renderer.test.mjs`
  - all five statuses, keyboard/ARIA behavior, source expansion, stale/raw badges.
- `personalization-memory-controls.test.mjs`
  - preference memory defaults off; opt-in, enumerate, remove-one, reset-all; system-prompt reset remains independent.

**Browser acceptance**

- Live side-panel: ask a fixture-known question → answer chip → drawer shows exact source and match reason.
- Disable `archive-read` → answer still succeeds with “Memory off.”
- Simulate timeout/partial read → responsive answer plus truthful degraded receipt.
- Correct a fact → intake/review receipt appears; trusted page remains unchanged.
- Forget for turn → regenerate excludes that item; reload behavior matches selected session/persistent scope.
- Raw-source-only fixture → visible non-authority badge.
- Keyboard-only open/close drawer, focus return, screen-reader labels.
- Restart continuity proof for issue #228 without claiming preference memory.
- Run `npm run test:browser-first`; because this crosses bridge ownership, also run module ownership check and `npm run verify:alpha` (`AGENTS.md`, “Change-To-Check Matrix”; `MODULE-OWNERSHIP.md:119-138`).

### Measurable acceptance targets

These are **inferred proposed budgets**, not current performance claims:

- Retrieval composition p50 ≤150 ms, p95 ≤500 ms on local fixture corpus; hard timeout 800 ms.
- Added memory context ≤1,200 estimated tokens and ≤20% of usable input budget; maximum two full pages plus three source snippets.
- Retrieval quality fixture set: Recall@5 ≥0.90, Precision@2 ≥0.80, MRR ≥0.85; 100% of displayed hits include source ref, authority, freshness, and match reason.
- Correction: 100% produce intake/review receipt; 0 direct trusted-page mutations.
- Forgetting: excluded from the next turn immediately; provider-owned persistent action receipt within 2 seconds locally.
- User control: memory-off state visible before submit; preference memory 100% default-off; all stored preferences enumerable and removable; no context use without a visible post-turn receipt.
- Degradation: provider response begins within 1 second after retrieval timeout; 0 false claims that memory was used, corrected, forgotten, or persisted.

## Connections

- derives -> ./findings.md
