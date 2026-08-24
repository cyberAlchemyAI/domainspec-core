# Augmentor Unified Agent Architecture — Explorer Record

This file is mechanically assembled by the strategist from verbatim explorer
returns. It is evidence input, not an authority decision, implementation claim,
or promoted architecture.

## Explorer 1 — authority and knowledge plane

```json
{
  "action_id": "spawn-0001",
  "role_id": "authority-knowledge-explorer",
  "status": "complete",
  "proof_posture": "Local source inspection only; no runtime execution, browser validation, writes, or external browsing.",
  "sources_selectors": [
    "research/2026-07-28-authority-memory-augmentor-integration/findings.md#product-thesis",
    "research/2026-07-28-authority-memory-augmentor-integration/findings.md#current-versus-missing",
    "research/2026-07-28-authority-memory-augmentor-integration/findings.md#non-collapsing-layers-and-ownership",
    "research/2026-07-28-authority-memory-augmentor-integration/findings.md#protected-user-handles",
    "research/2026-07-28-authority-memory-augmentor-integration/findings.md#semantic-index-and-graphdelta",
    "research/2026-07-28-authority-memory-augmentor-integration/findings.md#bounded-query-reasoning-and-presentation",
    "research/2026-07-28-authority-memory-augmentor-integration/findings.md#operating-envelope-and-exact-measurements",
    "research/2026-07-28-authority-memory-augmentor-integration/findings.md#user-experience-degraded-modes-and-privacy",
    "development/resonantos-integration/RESONANTOS-INTEGRATION-GUIDE.md#the-exact-hooks-to-attach-to",
    "development/resonantos-integration/RESONANTOS-INTEGRATION-GUIDE.md#scope-tag-discipline-lifecycle-mapping",
    "development/resonantos-integration/findings.md#critical-claim-proof-correction-e1-caveat-1",
    ".arcanum/inventory/entries/ontology-population-from-inventory-synthesis.md#direct-answer",
    ".arcanum/inventory/entries/ontology-population-from-inventory-synthesis.md#first-population-run",
    ".arcanum/inventory/entries/ontology-population-from-inventory-synthesis.md#handoff-shape-for-ontology-vault",
    ".arcanum/inventory/entries/ontology-population-from-inventory-synthesis.md#do-not-populate-this-way",
    ".arcanum/inventory/entries/ontology-operationalization-in-the-machine-synthesis.md#decision-spine",
    ".arcanum/inventory/entries/ontology-operationalization-in-the-machine-synthesis.md#routing-owner-gates-inventory-cannot-promote",
    "cyberAlchemy-v2/authority/definitions/DEFINITIONS.md#cav2-d3-authority-layer",
    "cyberAlchemy-v2/authority/definitions/DEFINITIONS.md#cav2-d5-promotion-gate",
    "cyberAlchemy-v2/authority/definitions/DEFINITIONS.md#cav2-d34-authority",
    "cyberAlchemy-v2/authority/definitions/DEFINITIONS.md#cav2-d35-provenance",
    "cyberAlchemy-v2/authority/definitions/DEFINITIONS.md#cav2-d48-authority-promotion-lifecycle",
    "cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md#kind-contract",
    "cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md#use-rule",
    "cyberAlchemy-v2/SOURCE-MAP.md#ingest-rules",
    "ops/development/2026-06-21-paper-saturn-explainer/SATURN-LAYER-MAP.md#reconciliation-table",
    "ops/development/2026-06-21-paper-saturn-explainer/SATURN-LAYER-MAP.md#public-safety-flags",
    "projects/framework-unification/CONCEPT-MAP.md#two-distinct-edge-catalogs-do-not-conflate-them"
  ],
  "typed_objects_ids": {
    "current_or_accepted_design": [
      "ExplicitUserHandle/ConceptStateHandle: id, posture, retention, sourceRefs/evidence, correctionOf?, tombstonedAt?",
      "SourceRecord: owner-local sourceRef plus digest; bytes remain with source owner",
      "GraphNode/GraphEdge: source/evidence refs and digests, freshness and contestation",
      "GraphDelta: deltaId, baseIndexVersion, sourceChanges, nodeOps, edgeOps, invalidates, contradictions, resultIndexVersion",
      "ReasoningContext: requestId, operation, handle digest, index/projection versions, selected/excluded IDs, limits, policy/context digest",
      "ReasoningResult: requestId, selected IDs, outcome-exclusive deterministic result, residue, context/deterministic digests, cacheStatus",
      "ReasoningPresentation: answer, source-bound rationaleClaims, caveats",
      "InventoryEvidence/EvidenceSet -> OntologyCandidate -> PromotionRecord -> governed projection"
    ],
    "ids_requiring_owner_assignment": [
      "MemoryIntakeRequest/intake candidate identifier",
      "Durable correction identifier and accepted-source-change event",
      "AuthorityDecision identifier separate from PromotionRecord",
      "GovernedProjection identifier and canonical source backlink"
    ]
  },
  "owner_matrix": [
    {
      "plane": "explicit user context",
      "current_owner": "extension/request-session host",
      "target_owner": "same; ephemeral UserHandles outside graph",
      "status": "designed from current settings precedent; durable preference owner absent"
    },
    {
      "plane": "durable source truth",
      "current_owner": "Living Archive/current source providers",
      "target_owner": "unchanged",
      "status": "read and intake seams observed; trusted promotion provider absent"
    },
    {
      "plane": "semantic index",
      "current_owner": "no accepted implementation",
      "target_owner": "existing memory domain/service",
      "status": "designed; disposable direct-scan/adjacency, never truth"
    },
    {
      "plane": "deterministic reasoning",
      "current_owner": "bounded evaluator precedent",
      "target_owner": "operation-specific deterministic adapter",
      "status": "finite evaluator observed by accepted research; generic registry/adapters absent"
    },
    {
      "plane": "Inventory",
      "current_owner": "Inventory",
      "target_owner": "evidence capture, selector lookup, residue and handoff only",
      "status": "observed discovery surface; explicitly non-authoritative"
    },
    {
      "plane": "ontology",
      "current_owner": "Ontology Vault/ontology route",
      "target_owner": "meaning, relation review, branch/drift maps and governed projections",
      "status": "candidate/design/fixture-level; incremental compiler absent"
    },
    {
      "plane": "authority/promotion",
      "current_owner": "CyberAlchemy v2 named owner routes and authority surfaces",
      "target_owner": "unchanged; explicit AuthorityDecision/PromotionRecord",
      "status": "definitions active; execution not end-to-end proven"
    },
    {
      "plane": "system framing",
      "current_owner": "DomainSpec intent; Arcanum execution; Saturn evidence loop",
      "target_owner": "unchanged",
      "status": "private intended architecture; only Arcanum is publicly shipped"
    }
  ],
  "connection_rows": [
    {
      "producer": "user/settings/session host",
      "artifact_event": "ExplicitUserHandle or evidence-qualified ConceptStateHandle",
      "consumer": "context coordinator",
      "authority_owner": "user plus request/session host",
      "selector": "accepted findings#protected-user-handles",
      "timing": "sync per turn/session",
      "failure": "exclude tombstoned/invalid handles; do not infer durable traits",
      "proof": "designed; settings precedent observed"
    },
    {
      "producer": "Living Archive/source provider",
      "artifact_event": "SourceRecord refs, bounded excerpts, digests",
      "consumer": "memory-owned index builder",
      "authority_owner": "source provider",
      "selector": "integration guide#the-exact-hooks-to-attach-to; accepted findings#non-collapsing-layers-and-ownership",
      "timing": "async lookup with 800 ms proposed hard timeout",
      "failure": "continue transcript-only; say unavailable/no relevant match, not source absence",
      "proof": "read seam observed; timeout budget unverified"
    },
    {
      "producer": "index compiler",
      "artifact_event": "GraphDelta",
      "consumer": "disposable semantic index",
      "authority_owner": "memory service for derived state; source owner remains truth owner",
      "selector": "accepted findings#semantic-index-and-graphdelta",
      "timing": "async on source change; deterministic apply/rebuild",
      "failure": "stale base rejects/rebases; digest change invalidates; contradictions coexist",
      "proof": "designed, unimplemented"
    },
    {
      "producer": "semantic index",
      "artifact_event": "BoundedProjection",
      "consumer": "deterministic operation",
      "authority_owner": "memory service owns projection; operation owns result",
      "selector": "accepted findings#bounded-query-reasoning-and-presentation",
      "timing": "sync bounded scan, 24 nodes/48 edges/1-2 hops target",
      "failure": "narrow or abstain; never silently omit required premises",
      "proof": "designed; budgets unverified"
    },
    {
      "producer": "deterministic operation",
      "artifact_event": "ReasoningResult with exclusive outcome and residue",
      "consumer": "grounded renderer or optional model presenter",
      "authority_owner": "reasoning contract, not model",
      "selector": "accepted findings#bounded-query-reasoning-and-presentation",
      "timing": "sync after validated projection",
      "failure": "invalid_context/abstained; model failure uses deterministic template",
      "proof": "finite evaluator precedent; generic adapter absent"
    },
    {
      "producer": "user/agent correction flow",
      "artifact_event": "MemoryIntakeRequest/candidate with one scope tag",
      "consumer": "Living Archive INTAKE/review queue",
      "authority_owner": "memory provider plus review owner",
      "selector": "integration guide#scope-tag-discipline-lifecycle-mapping",
      "timing": "async, explicitly separate from answer/result consumption",
      "failure": "retain local draft; claim neither submission nor persistence",
      "proof": "intake/review seam observed; per-runtime scope shims absent"
    },
    {
      "producer": "Inventory",
      "artifact_event": "selector-level evidence card or EvidenceSet",
      "consumer": "Ontology Vault review",
      "authority_owner": "Inventory only for evidence package",
      "selector": "ontology population#direct-answer/#handoff-shape-for-ontology-vault",
      "timing": "async governed handoff",
      "failure": "missing kind/claim/evidence/confidence/owner/invalidation stays evidence, never ontology",
      "proof": "designed/fixture-level"
    },
    {
      "producer": "Ontology Vault reviewer",
      "artifact_event": "OntologyCandidate plus PromotionRecord initially block",
      "consumer": "named authority owner",
      "authority_owner": "definitions/constitution/decision/spec owner route",
      "selector": "ontology population#first-population-run; authority-kinds#candidate-kinds",
      "timing": "async owner gate",
      "failure": "block/defer/reject; candidate remains non-authoritative",
      "proof": "designed; promotion execution unverified"
    },
    {
      "producer": "authority owner",
      "artifact_event": "AuthorityDecision/PromotionRecord",
      "consumer": "governed ontology projection or canonical authority surface",
      "authority_owner": "explicit scoped owner route",
      "selector": "DEFINITIONS.md#cav2-d34-authority/#cav2-d5-promotion-gate",
      "timing": "async explicit gate",
      "failure": "flag carries risk; no decision means no promotion",
      "proof": "normative definitions observed; end-to-end writer absent"
    },
    {
      "producer": "canonical authority/source surface",
      "artifact_event": "generated read model with backlink",
      "consumer": "Inventory/context/reasoning consumers",
      "authority_owner": "canonical source owner, never projection",
      "selector": "SOURCE-MAP.md#ingest-rules",
      "timing": "async regeneration/invalidation",
      "failure": "broken backlink or stale digest makes projection unusable/residue",
      "proof": "rule observed; unified adapter absent"
    }
  ],
  "findings": [
    "The safe flow is source -> disposable index -> bounded projection -> deterministic result -> optional grounded presentation; intake is a separate branch, not a side effect of result consumption.",
    "The governance continuation is intake candidate -> Inventory evidence -> OntologyCandidate -> PromotionRecord/AuthorityDecision -> governed projection/canonical surface. Inventory and ontology cannot promote.",
    "Allowed edges are read/source-ref, evidence handoff, candidate submission, explicit owner decision, and generated projection with canonical backlink. No modeling, graph, evaluator, model, or Inventory operation may write authority/promotion status.",
    "Forgetting requires handle tombstones plus recomposition; source correction requires accepted provider change, digest invalidation, dependent retraction/staleness, and rebuild. UI-only deletion is insufficient.",
    "Provenance must type source, relation, operation, owner, and posture at each step. Confidence, freshness, contestation, and uncertainty do not confer authority.",
    "Users need inspect/exclude/correct/forget controls; each control must change subsequent composed bytes/results. Pending correction must remain visibly distinct from accepted source change.",
    "DomainSpec and CyberAlchemy authority ontologies remain independent: language/type schema versus promotion/authority map. They align via explicit mapping edges; neither becomes the other's type-checker.",
    "Saturn is the private convergence-loop frame, not a runtime/store. DomainSpec is private intent/baseline; Arcanum is public execution. Private CAV2 state and promotion vocabulary must not leak into public Arcanum contracts."
  ],
  "reject_tests": [
    "Reject if a graph node contains UserHandle identity/preferences or copied authoritative source bytes.",
    "Reject if retrieval/traversal is labeled reasoning, or model presentation changes deterministic outcome/premises.",
    "Reject if confidence, importance, frequency, graph centrality, queue position, or Inventory verification becomes authority.",
    "Reject if result consumption automatically persists memory or creates ontology candidates.",
    "Reject if ontology/modeling code can write promotion-status or authority decisions.",
    "Reject if an ontology candidate, EvidenceSet, map, generated view, or PromotionRecord proposal is treated as canonical.",
    "Reject if correction flows backward from model prose rather than through provider-owned intake/review.",
    "Reject if private DomainSpec, Saturn, CAV2 paths, kinds, gates, receipts, or owner bindings become public Arcanum contracts.",
    "Reject if Saturn is implemented as a second scheduler, memory store, graph, runtime, or promotion owner."
  ],
  "gaps_residue": [
    "Durable preference owner is unresolved; v0 must remain request/session-scoped.",
    "GraphDelta compiler, projection/cache, invalidation adapter, generic reasoning registry, grounding adapter, and measured graph budgets are absent.",
    "Trusted Living Archive promotion provider behind the existing 501 seam is absent; scope-tag shims, port indirection, and b1/b2 store split are unbuilt.",
    "Ontology population is design/report/fixture-level; write-incapability remains a code-level proof obligation.",
    "AuthorityDecision versus PromotionRecord identity/cardinality needs an explicit owner decision.",
    "No unified vertical witness proves grounded context, reasoning, correction/intake, ontology candidate, and promotion while retaining separate owners."
  ],
  "validation": {
    "method": "Inspected frozen dispatch, selected Inventory packet, and exact local selectors.",
    "result": "PASS for architecture evidence extraction; NOT a runtime, promotion, implementation, or release proof.",
    "mutations": "none",
    "browser_or_tests": "none",
    "external_sources": "none"
  },
  "blockers": [
    "Any implementation claiming durable memory requires selection of an existing durable preference owner.",
    "Any promotion witness requires the host-resident trusted-write provider and explicit owner decision.",
    "Any operational non-collapse claim requires code proof that modeling surfaces have no write edge to promotion status."
  ]
}
```

## Explorer 2 — runtime, control, and bounded reasoning plane

action_id: `spawn-0002`  
role_id: `runtime-control-explorer`  
status: `PASS_WITH_BLOCKED_ADAPTERS`

## Sources/selectors

- Routing/session blueprint: `research/2026-07-28-augmentor-routing-session-fabric/findings.md`
  - `#status-and-product-thesis`
  - `#state-and-ownership-model`
  - `#classification-and-route-decisions`
  - `#child-runs-handoffs-isolation-and-recovery`
  - `#literal-v1-browser-witness`
- Strategy integration: `research/2026-07-28-augmentor-subagent-strategy-integration/findings.md`
  - `#public-neutral-adapter-and-runtime-profile-contract`
  - `#owner-identity-and-event-mappings`
  - `#honest-degraded-modes`
- Reasoning contract: `projects/cyberalchemy-orchestrator/docs/research/2026-07-22-agent-reasoning-engine-contract/findings.md`
  - `#converged-model-three-non-substitutable-layers`
  - `#candidate-machine-objects-and-invariants`
  - `#stable-judgment-algebra`
  - `#replay-and-effect-boundary`
  - `#final-verdict-matrix-and-reviewer-convergence`
- Dispatch Spec: `arcanum/formulae/dispatch-spec/SKILL.md:65-174`
- Orchestrate: `arcanum/runtime/orchestrate/SKILL.md:63-141`
- Lifecycle guide: `arcanum/development/user-guide/ARCANUM-MANUAL.md:106-178`
- Current ResonantOS:
  - `../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:1958-2113,2769-2822`
  - `../workspace-resonant/2.0.0-alpha/src/core/delegation.ts:1-96`
  - `../workspace-resonant/2.0.0-alpha/src/modules/chat/controller.ts:194-275`
  - `../workspace-resonant/2.0.0-alpha/src/modules/chat/run-guard.ts:5-28`
  - `../workspace-resonant/2.0.0-alpha/src/modules/chat/chat-route-request.ts:22-99`

## Connection rows

| # | Producer → typed artifact/event → consumer | Authority owner; exact selector | Posture | Failure/degraded behavior | Proof |
|---|---|---|---|---|---|
| 1 | User/chat shell → user turn + thread ID → `Interaction` resolver | Resonant thread owner; routing findings `:24-40,119-130`; contracts `:2769-2822` | Sync | Ambiguous active interaction asks one targeted continue/fresh question; explicit interrupt/command wins | Thread exists; `Interaction` adapter absent |
| 2 | Context selector → immutable `ContextSnapshot{digest,messageHorizon,selectors}` → route/reasoning/launch | Proposed host context adapter; routing `:42-55,144-148`; current provider request `chat-route-request.ts:22-99` | Sync | Empty/stale prompt blocks; later parent/sibling turns remain invisible absent addressed revision | Current filtered provider context exists; immutable launch snapshot absent |
| 3 | Route classifier → immutable `RouteDecision` → inline/capability/helper/strategy route | Proposed Augmentor route-decision owner; routing `:73-94,119-142` | Sync | Low confidence offers; no credible installed owner means capability gap/block | Accepted design; no Resonant projection/runtime |
| 4 | Strategy planner → digest-bound preview-only `StrategyProposal` → user gate | Augmentor proposal projection; strategy `:33-59` | Sync UI | Preview/edit/decline causes zero registration, spawn, owner call, or Run mutation; edits invalidate digest | Accepted design; absent implementation |
| 5 | User/consumer gate → exact approval record over proposal/Dispatch digest → Dispatch registrar | Consumer approval owner; strategy `:78-84`; Dispatch Spec `:87-99,103-124` | Sync | Scope/role/selector/wave/fallback drift requires revalidation and reapproval | Contract/design; current host adapter absent |
| 6 | Context/reasoning adapter → `AuthoritySnapshot + ProblemFrame + RuleCatalogManifest` (`ReasoningRequest`) → semantic evaluator | Authority-model owner supplies admissibility; evaluator owns finite reduction; reasoning findings `:15-61` | Sync/bounded | Entry block/defer causes zero evaluator/actor calls; missing applicability owner, facts, or valid catalog yields typed defer/invalidity | Research contract only; no executable L0 evaluator bytes found |
| 7 | Semantic evaluator → typed `JudgmentReceipt` → route/effect gate | Evaluator owns derivation only; reasoning `:63-78,110-120` | Sync/replayable | Unknown is never favorable; drift triggers revalidation | Unwitnessed candidate. Receipt is neither approval nor permission |
| 8 | Route adapter → frozen Dispatch document → Dispatch Spec validator | Dispatch Spec owns shape validation; `dispatch-spec/SKILL.md:65-101` | Sync deterministic | `flag`/`block`, missing authority, impossible dependency, or open lifecycle prevents execution | Implemented validator contract |
| 9 | Approved validated Dispatch → preflight/run plan + persisted actions → native execution | Orchestrate owns preflight/actions; `orchestrate/SKILL.md:77-116` | Sync preflight, zero spawn | Missing operation/authorization/validity blocks with `spawn_attempt_count=0`; no nested CLI fallback | Canonical runtime contract |
| 10 | Orchestrate persisted action → exactly one host spawn call → host-owned child identity/Run correlation | Orchestrate action authority; execution truth stays delegation/provider/compute owner; strategy `:63-91`; Orchestrate `:106-116` | Async | Duplicate/replayed/unknown action blocks; owner error is recorded, never implicitly retried | Orchestrate proven; Resonant action-to-owner and `HostRunProjection` adapters absent |
| 11 | Host owner → owner transitions/artifact/blocker handles → `RunTransitionProjection`/`RunOutcomeProjection` | Delegation, TaskWorkspace, ComputeJob, GoalWorkspace, artifact owners; strategy `:61-93`; contracts `:1958-2113` | Async observed | Owner unreachable remains unknown/unreconciled; projection cannot fabricate state | Current owners exist; general Run projection absent |
| 12 | Orchestrate wait/inventory → normalized child receipts → deterministic reducer/`LifecycleJoin` | Orchestrate join/gate/close owner; `orchestrate/SKILL.md:119-141` | Async bounded wait | Unknown/missing/mismatched result blocks; timeout interrupts once and records residue | Canonical runtime contract |
| 13 | Lifecycle join → closed lifecycle + independent result handles → user result consumption | Result/artifact owner; strategy `:87-93,97-104` | Async, selective | Join does not deliver, read, attach, merge transcript, or ingest memory; one child’s failure preserves sibling success | Designed; result-delivery/consumption adapter absent |
| 14 | User explicit intake action → memory-intake request referencing selected result/source → memory provider | Memory owner, never Run/join/evaluator; routing `:42-55,148-162`; strategy `:93` | Async separately gated | No silent intake from attachment, join, transcript, or judgment; absent trusted-write provider blocks | Intake boundary designed; trusted-write adapter absent |
| 15 | Positive judgment + separately passing exact-effect gate → effect envelope → effect owner | Effect gate/owner, not evaluator; reasoning `:39-43,110-114` | Sync gate, async effect | Every non-positive judgment produces zero effects; repeat delivery is one logical effect | Boundary contract only; full effect runtime absent |

## Current owner / absent adapter map

Current owners:

- Conversation/thread persistence: ResonantOS `ConversationThread`.
- Provider/model/runtime selection and prompt budgeting: Resonant provider fabric plus `ProviderChatRouteRequest`.
- Delegation scope and return protocol: `DelegationPacket`.
- Preparation filesystem envelope: `TaskWorkspace`; explicitly not execution.
- Compute policy/job truth: `ComputeJob`; proposed Run may only correlate its ID.
- Supervision/artifact references: `GoalWorkspace`.
- Dispatch structure: Dispatch Spec.
- Native spawn/join/gates/close: Orchestrate.
- Capability lifecycle: Task Session, Experiment Harness, Spellcraft, Sigil Development.
- Semantic conclusion, if built: separately versioned finite evaluator.
- Approval/effects/memory: their respective external owners.

Absent adapters:

- Thread-local `Interaction`.
- Context-selector output → immutable launch `ContextSnapshot`.
- Immutable `RouteDecision`.
- Browser-safe `StrategyProposal`.
- Digest-bound consumer approval → registration/preflight.
- Resonant runtime-profile discovery/admission.
- `ReasoningRequest` builder and admitted authority/rule-catalog owner.
- Executable L0 semantic evaluator and higher actor/effect protocol.
- Orchestrate action → Resonant delegation/provider/compute owner.
- Host parent/child `Run`, ancestry, durable transitions, cancellation acknowledgement, restart reconciliation.
- Result delivery/selective consumption.
- Explicit artifact attachment and memory-intake request/provider.
- Durable notification projection.

## Honest route modes

- `inline`: direct explanation/read-only answer; no protected effect, durable Run, or reusable-correctness claim.
- `helper`: one bounded independent target with explicit scope and receipt; not a Dispatch.
- `serial`: dependencies or host concurrency require ordering; if parallel was approved, serial requires revised proposal/digest and reapproval.
- `parallel`: only when problem shape needs independent lanes, Dispatch validates them, user approves exact bytes, and live host operations/capacity support them.
- `Easy`: inline or one reversible bounded run; Task Session ceiling.
- `Test`: repeatable fixtures against an existing contract; Experiment Harness owns evidence.
- `Hardening`: recurring/reusable workflow or primitive change; Spellcraft for composition, Sigil Development for primitive lifecycle.
- `install/compose`: capability absence may offer a separately authorized install; repeatable multi-capability behavior may enter Spellcraft. Neither follows automatically from a gap.
- `block`: no credible capability/owner; missing required host operation; invalid/changed dispatch; unresolved material authority/evidence; protected effect without exact gate; absent memory writer.

## Findings

1. The non-collapsing control chain is:

   `turn → Interaction → ContextSnapshot → RouteDecision → [StrategyProposal → exact approval] → [ReasoningRequest → JudgmentReceipt] → validated Dispatch → Orchestrate plan/actions → host-owned Runs/effects → LifecycleJoin → selective result consumption → separate memory intake`.

2. `RouteDecision`, proposal, approval, judgment, Dispatch, Run, result, effect, join, and memory intake exist because each has different owner, lifecycle, and failure semantics. Collapsing any adjacent pair creates unauthorized behavior.

3. Augmentor should be a projection/adaptation layer, not a new router, scheduler, registry, job system, workspace, session store, artifact store, memory provider, or reasoning authority.

4. ResonantOS presently has one global transient chat-run token. General concurrent children, durable ancestry, joins, recovery, and notifications remain absent.

5. The claimed “bounded L0 evaluator” is not supported by inspected bytes. The accepted reasoning finding calls `semantic-judgment evaluator@1` an `UNWITNESSED CANDIDATE`; no implementation file was found. Any synthesis must correct the packet’s “bounded local evaluator witness exists” wording.

## Gaps/residue

- No executable unified vertical witness.
- No two-child Resonant runtime or reload reconciliation.
- No admitted applicability/precedence authority owner for evaluator input.
- No exact-effect runtime beyond contract-level test shape.
- No trusted memory-write adapter.
- No measured latency, token, storage, or attention budgets.
- Cancellation, late-result quarantine, notification dedupe, and selective consumption are acceptance designs, not current behavior.

## Validation

Read-only source comparison completed. No files edited, no browser/network calls, and no subagents spawned. The route is architecturally coherent only as `BUILD-FROM-OWNED + NOVEL-ADAPTERS`; current product/runtime proof remains `NO_WITNESS_CURRENT`.

## Blockers

- Block implementation claim until live Resonant state is refreshed and adapters are assigned owners.
- Block “reasoning engine” or “L0 evaluator implemented” claims.
- Block parallel execution if native spawn/wait/inventory/interrupt operations or owner capacity are absent.
- Block any effect based only on route confidence, proposal, approval, or evaluator receipt.
- Block any memory mutation implied by result attachment or consumption.

## Explorer 3 — human memory and one-interface experience

```json
{
  "action_id": "spawn-0003",
  "role_id": "human-experience-explorer",
  "status": "completed_read_only",
  "verdict": "DESIGNED_BUILD_FROM_OWNED",
  "thesis": "One interface means one trusted conversation with progressive disclosure, not one collapsed state model. Transcript stays primary; route proposal, child execution, knowledge grounding, artifacts, and notifications remain typed projections of their owners. No joined browser witness currently exists.",
  "sources": [
    {
      "source": "research/2026-07-28-authority-memory-augmentor-integration/findings.md",
      "selectors": ["#product-thesis:13-19", "#non-collapsing-layers-and-ownership:32-43", "#bounded-query-reasoning-and-presentation:186-233", "#literal-vertical-v0-witness:235-265", "#operating-envelope:275-294", "#user-experience-degraded-modes-and-privacy:296-332"]
    },
    {
      "source": "research/2026-07-28-augmentor-routing-session-fabric/findings.md",
      "selectors": ["#state-and-ownership-model:24-118", "#classification-and-route-decisions:119-143", "#child-runs-handoffs-isolation-and-recovery:144-163", "#repaired-notification-control-contract:164-173", "#literal-v1-browser-witness:174-190", "#bounded-overhead:245-250"]
    },
    {
      "source": "research/2026-07-28-augmentor-subagent-strategy-integration/findings.md",
      "selectors": ["#public-neutral-adapter-and-runtime-profile-contract:33-60", "#owner-identity-and-event-mappings:61-94", "#human-journeys:95-107", "#honest-degraded-modes:108-125", "#exact-two-child-browser-witness:165-182", "#measurable-overhead-budgets:183-195"]
    },
    {
      "source": "projects/ide-ergonomics/UNIFIED-PRODUCT-VIEW.md",
      "selectors": ["#one-sentence-product:35-47", "#coordinate-admission-and-evolution-lifecycle:136-168", "#the-witness:169-204", "#mvp-shape:234-246", "#owner-boundary-preservation:247-260"]
    },
    {
      "source": "arcanum/development/user-guide/ARCANUM-MANUAL.md",
      "selectors": ["#processes:82-141", "#how-refine-helps:221-230", "#constructing-a-dispatch-spec:232-246"]
    },
    {
      "source": "../workspace-resonant/2.0.0-alpha/src/modules/chat/ContextMemoryPanel.tsx",
      "selectors": ["ContextMemoryPanelProps:8-16", "memoryItems/editing:55-97", "context-map-and-layer-disclosure:99-155", "editor:157-208"]
    },
    {
      "source": "../workspace-resonant/2.0.0-alpha/src/modules/chat/StrategistChatRail.tsx",
      "selectors": ["strategistThreads/onSetActiveThread:61,107", "thread-switch control:395", "polite activity status:597", "run-status card:763"]
    },
    {
      "source": "../workspace-resonant/2.0.0-alpha/docs/architecture/ADR-004-chat-rail.md",
      "selectors": ["#ux-principles:17-22", "#composer-rules:24-33", "#runtime-rules:35-42", "#trust-rules:44-48"]
    }
  ],
  "connection_rows": [
    {
      "visible_connection": "ordinary turn -> answer",
      "typed_object": "Interaction + immutable RouteDecision",
      "producer_consumer": "chat controller -> active provider/coordinator",
      "owner": "Resonant thread/interaction owner",
      "truth_boundary": "decision explains routing; it is neither approval nor execution",
      "selector": "routing findings #state-and-ownership-model/#classification-and-route-decisions",
      "surface": "transcript; quiet rationale disclosure only when useful",
      "degraded_language": "Answered here; advanced routing was unavailable.",
      "proof": "accepted design; current single-chat basis observed"
    },
    {
      "visible_connection": "grounded answer -> source inspection",
      "typed_object": "ReasoningPresentation + BoundedProjection + source refs",
      "producer_consumer": "reasoning/presentation adapter -> knowledge/source view",
      "owner": "source owner for truth; memory service for disposable index; reasoning owner for result",
      "truth_boundary": "presentation cannot add premises; projection is not source truth",
      "selector": "memory findings:17-19,32-43,186-233,296-309",
      "surface": "one `Memory: N sources` chip opening source titles, freshness, contestation, match reason, then bounded excerpts/result",
      "degraded_language": "No directly relevant item; answered from this conversation and page context.",
      "proof": "designed; absent joined adapter"
    },
    {
      "visible_connection": "correct/forget -> next recomposition",
      "typed_object": "UserHandle correction/tombstone or source-correction draft",
      "producer_consumer": "user control -> handle compiler/memory intake owner",
      "owner": "session handle owner; durable source owner separately",
      "truth_boundary": "ephemeral correction changes future composition; pending source correction changes no trusted bytes",
      "selector": "memory findings:265,271-273,298-309,332",
      "surface": "knowledge/source view, not transcript rewriting",
      "degraded_language": "Saved for this session only. Source correction remains a local draft.",
      "proof": "designed; compact-memory editing alone observed"
    },
    {
      "visible_connection": "route preview -> approval",
      "typed_object": "StrategyProposal + proposal digest + approval record",
      "producer_consumer": "Augmentor strategy projection -> consumer approval/registrar",
      "owner": "proposal owner; approval and registrar owners distinct",
      "truth_boundary": "preview/edit/decline has zero side effects; changed bytes invalidate approval",
      "selector": "strategy findings:33-60,95-107",
      "surface": "inline rationale/proposal card after the triggering turn",
      "degraded_language": "Proposed: two background runs. Nothing has started.",
      "proof": "accepted design; card/backend absent"
    },
    {
      "visible_connection": "approved proposal -> child progress",
      "typed_object": "actionId + HostRunProjection + RunOutcomeProjection",
      "producer_consumer": "Orchestrate/host owner observations -> run tray",
      "owner": "execution owner holds terminal truth; UI owns projection only",
      "truth_boundary": "prepared is not running; projected state cannot manufacture owner state",
      "selector": "strategy findings:61-94,165-182",
      "surface": "compact run tray, maximum two active children; parent composer remains usable",
      "degraded_language": "Owner status unavailable; last confirmed state shown.",
      "proof": "designed; current generic run-phase card only"
    },
    {
      "visible_connection": "child clarification -> addressed input",
      "typed_object": "AttentionRequest + addressed InputRevision",
      "producer_consumer": "child A -> parent user -> child A owner",
      "owner": "child input/context owner",
      "truth_boundary": "one answer revises only A; no sibling or parent snapshot mutation",
      "selector": "strategy findings:95-107,165-182",
      "surface": "single inline attention row plus polite notification",
      "degraded_language": "A needs one answer to continue; B is still running independently.",
      "proof": "designed; absent"
    },
    {
      "visible_connection": "partial terminal outcomes -> selective use",
      "typed_object": "blockerRef/artifactRef + ResultConsumption",
      "producer_consumer": "execution owners -> artifact surface -> selected parent interaction",
      "owner": "artifact/blocker owners; consumption owner separate from lifecycle",
      "truth_boundary": "opening/attaching B changes neither A, join, read state, nor memory intake",
      "selector": "strategy findings:61-94,165-182",
      "surface": "tray says A Blocked, B Done; artifact surface offers Open, Attach, Keep separate",
      "degraded_language": "One result is ready; one run is blocked. You can use the ready result independently.",
      "proof": "designed; generic artifacts observed, selective child consumption absent"
    },
    {
      "visible_connection": "thread switch/reload -> restored projections",
      "typed_object": "Thread + owner-correlated Run projections + notification read state",
      "producer_consumer": "session/hydration owners -> thread list/run tray",
      "owner": "thread/session owner and execution owners remain distinct",
      "truth_boundary": "switching does not reparent work or merge transcripts; reload does not replay announcements",
      "selector": "routing findings:24-118,144-190; chat rail:61,107,395",
      "surface": "thread list plus tray scoped to selected thread",
      "degraded_language": "Status could not be refreshed; no outcome was inferred.",
      "proof": "thread switching observed; multi-run restoration designed"
    }
  ],
  "journeys": [
    "Ordinary conversation: answer inline; no card when inline is honest.",
    "Grounded preference/source answer: quiet source chip; expand to exact handles, sources, result, caveats.",
    "Correction/forgetting: correct session handle or tombstone it; rerun proves changed request/result bytes. Durable source correction is separately pending.",
    "Route preview/one approval: preview two roles and bounded context; edit or decline with zero effects; one exact digest-bound approval starts both.",
    "Concurrent continuity: parent composer and thread switching remain available while A and B run.",
    "Targeted clarification: child-specific attention row; keyboard answer creates exactly one addressed revision.",
    "Partial result: A Blocked with blocker reference; B Done with artifact; dependent join remains blocked while B stays consumable.",
    "Selective consumption: attach B only; prove no A, sibling notification, lifecycle, or memory mutation.",
    "Capability absence: inline if semantically sufficient; otherwise preview/export, separately offer install/hardening, or hard-block naming the missing operation.",
    "Escalation: Easy = inline/no proposal; Test = deterministic fixture/local owner adapters and visible experimental label; Hardening = explicit proposal/approval for consequential multi-owner execution, with no readiness claim until owner-backed witness passes."
  ],
  "surface_allocation": {
    "transcript": "user/assistant turns, bounded answer, clarification exchange, concise terminal summaries; never merge child transcripts",
    "rationale_proposal_card": "route rationale, roles, bounded context, expected outputs, forbidden effects, edit/decline/approve; never receipts-first",
    "thread_list": "conversation identity, unread/attention cue, thread switching; no run reparenting",
    "run_tray": "two-child compact progress, attention, blockers, reconciliation uncertainty; not scheduler controls or infrastructure dashboard",
    "knowledge_source_view": "handles, sources, freshness, contestation, match reason, exclusion, correction, forgetting, memory-off",
    "artifact_surface": "owner-backed artifact preview and Open/Attach/Keep separate; not proof of lifecycle success",
    "notifications": "only meaningful attention/terminal transitions, polite/coalesced, scoped to child/thread, never focus-stealing"
  },
  "budgets": {
    "accessibility": [
      "All functions keyboard reachable; visible focus; dialogs restore initiating focus.",
      "Routine updates use polite coalesced announcements; reload announces nothing already seen.",
      "No color-only state; reduced motion preserves textual status; blocker/result labels programmatic."
    ],
    "attention": [
      "Route cards on <=20% of ordinary turns.",
      "Clarification on <=5% of routed attempts.",
      "<=2 extra user actions for consequential launch; exactly one approval.",
      "<=1 announcement per meaningful attention or terminal transition."
    ],
    "latency": [
      "Retrieval hard timeout 800ms; continue honestly.",
      "Deterministic operation warm p95 <=20ms.",
      "Optional reasoning p50 <=1.5s, p95 <=4s excluding upstream congestion.",
      "Proposal interaction itself local/instant target <=100ms; approval acknowledgement target <=250ms before owner-call progress."
    ],
    "token": [
      "Added source/graph context <=1200 estimated tokens.",
      "Total reasoning input <=2000 estimated tokens.",
      "0 or 1 presentation model call; no recursion.",
      "Display only selected excerpts; raw receipts never lead."
    ],
    "graph_size": [
      "<=24 nodes, <=48 edges, one hop default/two hard.",
      "<=8 session handles.",
      "Derived index/cache <=25MB per measured fixture partition.",
      "No graph database until measured pressure defeats direct scan/disposable adjacency."
    ],
    "user_control": [
      "Per-turn exclude; session memory-off; inspect, correct, tombstone/forget handles.",
      "Proposal edit/decline causes zero effects; approval invalidated by byte change.",
      "Attach/consume selected result only; memory intake always separate.",
      "Cancel remains requested until owner acknowledgement; unknown remains unknown."
    ]
  },
  "findings": [
    "The one-interface product is a trusted conversation plus progressive projections, not a dashboard.",
    "Current chat rail, thread switch, run-phase status, compact-memory editor, context meter, and artifact foundations are reusable observed surfaces.",
    "Compact memory is not the proposed source-grounded memory model; editing its summary does not prove handle tombstoning, source correction, or forgetting.",
    "Easy/Test/Hardening must describe execution posture and proof ceiling, not expose a tool drawer.",
    "A card never establishes a router, approval owner, scheduler, execution, reasoning, memory write, or promotion backend."
  ],
  "gaps_residue": [
    "No current joined contracts for StrategyProposal, exact approval, child Run projections, addressed clarification, selective consumption, or memory intake.",
    "No browser witness combines grounding, one approval, two isolated children, parent continuation, partial success, reload, selective consumption, and separate intake.",
    "Budgets are acceptance targets, unmeasured.",
    "Durable preference owner, graph-delta compiler, reasoning adapter, and trusted forgetting/write provider remain absent or deferred.",
    "Runtime profile, approval/registrar owner, and multi-run host adaptation remain blocker decisions."
  ],
  "validation": {
    "method": "read-only source and selector reconciliation; no browsing, mutation, runtime execution, or browser claim",
    "required_browser_assertions": [
      "No proposal UI or event on honest inline turn.",
      "Preview/edit/decline emits zero registration/spawn/owner calls.",
      "One approval yields two distinct owner-correlated runs; parent turn and thread switch preserve snapshots.",
      "Keyboard clarification targets A only.",
      "A Blocked and B Done persist across reload without duplicate announcements.",
      "Attach B only leaves A, join, read state, and memory unchanged.",
      "Correct/forget/memory-off changes composed bytes and result, not merely labels.",
      "Missing capability names the missing operation and emits zero spawn attempts."
    ]
  },
  "blockers": [
    "BLOCKED for implemented-product or production claims: complete owner-backed vertical witness is absent.",
    "BLOCKED for durable forgetting claims until a named trusted memory/source owner and executable deletion/tombstone proof exist.",
    "BLOCKED for multi-child launch until runtime-profile, approval/registrar, and owner-operation bindings are named and tested."
  ],
  "hard_rejects": [
    "hidden routing or implied approval",
    "parent/child/sibling transcript merging",
    "graph visualizations presented as truth or intelligence",
    "receipts as the primary user experience",
    "generic tool drawers or infrastructure dashboards",
    "proposal, status, or artifact cards claimed as backend execution",
    "consumption silently becoming memory intake",
    "unknown owner state rendered as running, success, failure, or cancelled"
  ]
}
```
