## Synthesis receipt

- `action_id`: `spawn-0004`
- `role_id`: `unified-architecture-synthesizer`
- `status`: `PASS_WITH_BLOCKED_VERTICAL_WITNESS`
- `dispatch_id`: `2026-07-29-augmentor-unified-agent-architecture-route`
- `run_id`: `aua-20260729T051325Z`
- Mutation: none
- Proof posture: read-only synthesis; no tests, browser run, runtime execution, or external browsing.

### Evaluator disagreement resolved

Explorer 2 is correct. Explorer 1’s “bounded evaluator precedent” is usable only as a **research-contract precedent**, not an executable witness. The controlling source says:

- the repository does not own an executable semantic relation;
- `semantic-judgment evaluator@1` is “an explicitly unwitnessed build/test candidate”;
- its verdict is `UNWITNESSED CANDIDATE`;
- the reviewer convergence passed only “as a research contract.”

Therefore every evaluator connection below is `unverified/absent implementation`; no vertical witness may be described as executed. [Reasoning contract lines 5–9, 122–132](projects/cyberalchemy-orchestrator/docs/research/2026-07-22-agent-reasoning-engine-contract/findings.md#L5) (Explorer 2; corrects Explorer 1).

## Product thesis and system context

Augmentor should be one trusted conversational interface over existing owners, with progressive projections for grounding, routing, approval, concurrent work, artifacts, and knowledge controls. “One interface” must not collapse state or authority.

It is an adaptation/projection layer, not a second router, scheduler, session store, job/workspace/artifact owner, memory provider, graph truth store, reasoning authority, ontology writer, or promotion authority. Build posture is `BUILD_FROM_OWNED + NOVEL_ADAPTERS`; present product posture is `NO_WITNESS_CURRENT`. [Explorer 2, findings 1–5](research/2026-07-29-augmentor-unified-agent-architecture/research.md#explorer-2--runtime-control-and-bounded-reasoning-plane); [Explorer 3 thesis/findings](research/2026-07-29-augmentor-unified-agent-architecture/research.md#explorer-3--human-memory-and-one-interface-experience).

## Planes and owners

| Plane | Owner retained | Augmentor’s permitted role | Posture |
|---|---|---|---|
| Human/conversation | ResonantOS thread/session and provider fabric | Compose one interface and typed projections | Thread/chat surfaces observed; joined experience absent |
| Runtime/control | Dispatch Spec, Orchestrate, delegation/provider/compute owners | Adapt decisions, approvals, actions, Runs, joins | Core owners exist; host adapters absent |
| Knowledge | Source providers/Living Archive; future existing memory domain | Compile disposable index and bounded projections | Read/intake seams observed; compiler absent |
| Reasoning | Separately versioned finite evaluator | Build request/present receipt; never authorize | Research contract only; evaluator absent |
| Evidence | Inventory | Discovery, selectors, evidence handoff | Observed; never authority |
| Meaning | Ontology Vault/ontology route | Candidate/review/projection route | Design/fixture-level |
| Authority | Named CyberAlchemy v2 owner routes | Present decision/projection only | Normative definitions observed; end-to-end writer unverified |
| Pillar framing | DomainSpec intent, public Arcanum execution, Saturn evidence loop | Preserve mapping and evidence | Private architecture; Saturn is not a runtime/store |

Sources: [Explorer 1 owner matrix](research/2026-07-29-augmentor-unified-agent-architecture/research.md#explorer-1--authority-and-knowledge-plane); [Explorer 2 current-owner map](research/2026-07-29-augmentor-unified-agent-architecture/research.md#explorer-2--runtime-control-and-bounded-reasoning-plane).

## Non-collapsing typed object catalog

The minimum behavioral types are:

- `Thread` → owns conversation identity and transcript.
- `Interaction` → one active user concern within a thread.
- `ExplicitUserHandle` / `ConceptStateHandle` → scoped user assertion, correction, exclusion, or tombstone.
- `SourceRecord{sourceRef,digest}` → owner-local authoritative bytes by reference.
- `GraphDelta` / disposable `SemanticIndex` → derived, invalidatable retrieval state; never truth.
- `BoundedProjection` → selected nodes/edges/excerpts under explicit limits.
- `ContextSnapshot{digest,horizon,selectors}` → immutable launch input.
- `RouteDecision` → immutable explanation of inline/capability/helper/strategy/block choice.
- `StrategyProposal{digest}` → preview only.
- `ApprovalRecord` → exact consumer approval; neither proposal nor execution.
- `Dispatch` → validated capability-bound execution shape.
- `ReasoningRequest{AuthoritySnapshot,ProblemFrame,RuleCatalogManifest}` → candidate evaluator input.
- `JudgmentReceipt` / `ReasoningResult` → non-authorizing deterministic conclusion or abstention.
- `ReasoningPresentation` → grounded human rendering; cannot add premises.
- `Action` → Orchestrate-owned persisted operation.
- `Run` / `HostRunProjection` → host-correlated execution lifecycle, distinct from Thread/Interaction.
- `AttentionRequest` / addressed `InputRevision` → child-specific clarification.
- `LifecycleJoin` → lifecycle reduction only; not delivery or memory.
- `ArtifactRef` / `BlockerRef` → owner-backed result handles.
- `ResultConsumption` → explicit open/attach/keep-separate act.
- `EffectEnvelope` / effect-gate decision → exact protected mutation boundary.
- `MemoryIntakeRequest` → separately authorized candidate; never implicit on consumption.
- `InventoryEvidence` / `EvidenceSet` → discovery package.
- `OntologyCandidate` → non-authoritative meaning proposal.
- `AuthorityDecision` and `PromotionRecord` → distinct owner decision/audit identities pending cardinality decision.
- `GovernedProjection` → generated read model with canonical backlink.

Adjacent types must not collapse: judgment ≠ approval; approval ≠ Dispatch; Dispatch ≠ Run; Run ≠ Thread; join ≠ consumption; consumption ≠ intake; index ≠ memory/source; evidence ≠ ontology; candidate ≠ authority decision; promotion record ≠ canonical source.

## Exact connection catalog

“Identity” means the immutable correlation/digest required in the target contract; where no schema exists, it is explicitly proposed.

| ID | Producer → artifact/event → consumer | Authority; immutable identity; exact selector | Timing / failure / observability / proof |
|---|---|---|---|
| `AUA-C01` | Chat shell → turn + thread ID → Interaction resolver | Resonant thread owner; `threadId+turnId`; routing findings `#state-and-ownership-model`, Explorer 2 row 1 | Sync; ambiguity asks one targeted question; transcript event; `observed thread / absent Interaction` |
| `AUA-C02` | Handle/source selector → handles + source refs → context coordinator | User/session and source owners; handle IDs + source digests; Explorer 1 rows 1–2, `#protected-user-handles` | Sync plus ≤800 ms lookup; exclude invalid/tombstoned, continue transcript-only on timeout; selection trace; `observed seam / adapter unverified` |
| `AUA-C03` | Index compiler → `GraphDelta` → disposable index | Memory domain; `deltaId+base/result version+source digests`; Explorer 1 row 3, `#semantic-index-and-graphdelta` | Async source change; reject/rebase stale base, invalidate changed digest; delta/rebuild receipt; `absent` |
| `AUA-C04` | Index → `BoundedProjection` → context/reasoning | Memory owns projection, source retains truth; projection digest + selected/excluded IDs; Explorer 1 row 4 | Sync bounded; narrow/abstain if required premises unavailable; selection/residue trace; `designed/unverified` |
| `AUA-C05` | Context coordinator → immutable `ContextSnapshot` → route/evaluator/launch | Host context adapter; snapshot digest; routing `#state-and-ownership-model`, Explorer 2 row 2 | Sync; stale/empty blocks, later turns invisible without addressed revision; composed-byte digest; `filtered context observed / snapshot absent` |
| `AUA-C06` | Classifier → `RouteDecision` → inline/capability/helper/strategy/block | Proposed Augmentor decision owner; decision ID + input/config digest; routing `#classification-and-route-decisions`, Explorer 2 row 3 | Sync; low confidence offers, missing owner blocks; quiet rationale projection; `accepted design/absent` |
| `AUA-C07` | Strategy planner → `StrategyProposal` → approval surface | Proposal projection owner; proposal digest; strategy `#public-neutral-adapter-and-runtime-profile-contract`, Explorer 2 row 4 | Sync UI; edit invalidates digest, decline causes zero effects; card event; `designed/absent` |
| `AUA-C08` | User gate → exact `ApprovalRecord` → Dispatch registrar | Consumer approval owner; proposal/Dispatch digest; strategy `#owner-identity-and-event-mappings`, Dispatch Spec `SKILL.md:87-124`, Explorer 2 row 5 | Sync; any material drift revalidates/reapproves; approval audit; `contract/host adapter absent` |
| `AUA-C09` | Reasoning adapter → `ReasoningRequest` → semantic evaluator | Authority-model owner supplies admissibility; request + snapshot/catalog digests; reasoning contract lines 15–61, Explorer 2 row 6 | Bounded sync; missing owner/facts/catalog defers or invalidates; request receipt; `UNWITNESSED CANDIDATE` |
| `AUA-C10` | Evaluator → `JudgmentReceipt` → route/effect gate | Evaluator owns derivation only; receipt digest; reasoning contract lines 63–78, 122–132, Explorer 2 row 7 | Replayable target; unknown never favorable, drift invalidates; derivation/residue; `absent/unverified` |
| `AUA-C11` | Route adapter → frozen `Dispatch` → Dispatch Spec | Dispatch Spec owns structural validation; Dispatch digest; `arcanum/formulae/dispatch-spec/SKILL.md:65-124`, Explorer 2 row 8 | Sync deterministic; flag/block prevents execution; validation receipt; `implemented contract` |
| `AUA-C12` | Approved Dispatch → run plan/actions → Orchestrate | Orchestrate owns preflight/action lifecycle; dispatch/run/action IDs; `arcanum/runtime/orchestrate/SKILL.md:77-116`, Explorer 2 row 9 | Preflight with zero spawn; missing authorization/operation blocks; persisted actions/events; `implemented contract` |
| `AUA-C13` | Orchestrate action → one native spawn → host child Run | Action authority in Orchestrate; execution truth in host owner; `actionId+ownerRunId+parentRunId`; strategy `#owner-identity-and-event-mappings`, Explorer 2 rows 10–11 | Async; duplicate/unknown blocks, owner unreachable remains unknown; owner transition projection; `owners observed / adapters absent` |
| `AUA-C14` | Child → `AttentionRequest`; user → addressed `InputRevision` → same child | Child context/input owner; child Run ID + snapshot revision; strategy `#human-journeys`, Explorer 3 connection 6 | Async; only addressed child changes; attention row/polite notification; `absent` |
| `AUA-C15` | Orchestrate wait/inventory → child receipts → `LifecycleJoin` | Orchestrate join/close; action IDs + receipt digests; `orchestrate/SKILL.md:119-141`, Explorer 2 row 12 | Bounded async; missing/mismatched blocks, timeout interrupts once; join receipt/residue; `implemented contract` |
| `AUA-C16` | Join/owners → artifact/blocker refs → `ResultConsumption` | Artifact/result owners; ref digest + selected interaction; strategy `#owner-identity-and-event-mappings`, Explorer 2 row 13 | Async selective; sibling failure preserves success, attach mutates no lifecycle/memory; consumption event; `artifacts observed / selective adapter absent` |
| `AUA-C17` | User → `MemoryIntakeRequest` → memory provider | Memory provider/review owner; intake ID + selected source/result digest + scope tag; integration guide `#scope-tag-discipline-lifecycle-mapping`, Explorers 1 row 6 and 2 row 14 | Separately gated async; provider absence retains draft and claims no persistence; intake status; `seam observed / trusted writer absent` |
| `AUA-C18` | Inventory → `EvidenceSet` → Ontology Vault | Inventory owns evidence only; evidence digest + selectors; ontology-population `#direct-answer/#handoff-shape-for-ontology-vault`, Explorer 1 row 7 | Governed async; incomplete package remains evidence; handoff receipt; `design/fixture-level` |
| `AUA-C19` | Ontology reviewer → candidate → named authority owner | Ontology route owns candidate; candidate ID + source/evidence digests; ontology-population `#first-population-run`, Explorer 1 row 8 | Async gate; reject/defer/block remains non-authoritative; candidate status; `designed/unverified` |
| `AUA-C20` | Authority owner → decision/promotion record → canonical surface/projection | Explicit scoped authority owner; decision/promotion IDs + exact canonical selector; CAV2 definitions `#cav2-d34-authority/#cav2-d5-promotion-gate`, Explorer 1 rows 9–10 | Async explicit gate; no decision means no promotion, stale backlink invalidates view; decision/projection receipt; `normative rules observed / writer absent` |
| `AUA-C21` | Positive judgment + exact effect gate → effect envelope → effect owner | Effect owner/gate, never evaluator; envelope idempotency key; reasoning contract lines 110–114, Explorer 2 row 15 | Sync gate/async effect; non-positive gives zero attempts, repeat is one logical effect; effect-owner receipt; `boundary contract only` |

## End-to-end control sequence and hierarchy

`Thread → Interaction → handles/sources → BoundedProjection → ContextSnapshot → RouteDecision`.

Inline answers stop there. Consequential multi-owner work continues:

`StrategyProposal → exact ApprovalRecord → optional ReasoningRequest/JudgmentReceipt → frozen Dispatch → Dispatch Spec validation → Orchestrate preflight/actions → host parent Run → isolated child Runs A/B → addressed clarification if needed → LifecycleJoin → independent artifact/blocker refs → selective ResultConsumption → optional separate MemoryIntakeRequest`.

Hierarchy is:

```text
Session host
└── Thread (conversation identity)
    ├── Interaction N (user concern)
    └── parent Run (execution correlation, not transcript)
        ├── child Run A ── immutable snapshot A ── blocker/attention/artifact refs
        └── child Run B ── immutable snapshot B ── blocker/attention/artifact refs
```

Reload reconstructs projections from thread/session plus execution owners. It must not replay effects, merge child transcripts, reparent Runs, infer unknown owner state, or repeat already-read announcements.

## Knowledge lifecycle

`ExplicitUserHandle + SourceRecord refs → disposable SemanticIndex via GraphDelta → BoundedProjection → candidate deterministic ReasoningResult → grounded ReasoningPresentation`.

Correction has two distinct paths:

1. Session handle correction/tombstone changes subsequent composed bytes immediately.
2. Durable source correction creates an intake draft; only source-owner acceptance changes trusted bytes, then digest invalidation retracts/stales dependents and rebuilds the index.

Governance continues separately:

`MemoryIntakeRequest → Inventory EvidenceSet → OntologyCandidate → explicit AuthorityDecision/PromotionRecord → canonical source or governed projection with backlink`.

Inventory discovers; ontology models/reviews; named authority decides. Neither model output, centrality, confidence, frequency, queue position, or result consumption promotes anything.

## One-interface surfaces

- Transcript: ordinary conversation and concise summaries; no child-transcript merging.
- Quiet rationale/source chip: opens handles, exact sources, freshness, contestation, selected premises, and caveats.
- Proposal card: roles, bounded context, expected outputs, forbidden effects, edit/decline/approve.
- Thread list: identity and unread/attention only.
- Run tray: at most two active children, meaningful progress/attention/blockers; not scheduler controls.
- Artifact surface: Open / Attach / Keep separate.
- Knowledge/source view: inspect, exclude, correct, tombstone/forget, memory-off.
- Notifications: polite, deduplicated, child/thread-scoped meaningful transitions only.

A card is never backend proof.

## Public/private boundary

Public Arcanum may expose generic execution lifecycle behavior and neutral adapter contracts. It must not expose private DomainSpec intent/state, Saturn framing, CyberAlchemy v2 paths/kinds/gates/owner bindings, or private promotion receipts. Saturn is a private reconciliation-loop concept, not storage, runtime, scheduler, graph, or promotion owner. DomainSpec and CAV2 ontologies align through explicit mapping edges; neither type-checks or subsumes the other. [Explorer 1 findings/reject tests](research/2026-07-29-augmentor-unified-agent-architecture/research.md#explorer-1--authority-and-knowledge-plane).

## Capability-gap routes

- Inline when a read-only answer is semantically sufficient.
- One bounded helper for one independent target; not Dispatch.
- Serial when dependency/capacity requires it; changing approved parallel shape requires new digest and approval.
- Parallel only with independent lanes, validated Dispatch, exact approval, and host capacity.
- `Easy`: inline or one reversible bounded Run.
- `Test`: repeatable deterministic/local fixtures under Experiment Harness.
- `Hardening`: reusable composition/primitive lifecycle under Spellcraft/Sigil Development.
- Install/compose only via separate authorization.
- Block when capability/owner/operation, authority evidence, trusted writer, exact effect gate, or host runtime is absent.

## Current versus absent adapter map

Current: thread persistence, provider routing/budgeting, `DelegationPacket`, `TaskWorkspace`, `ComputeJob`, `GoalWorkspace`, artifact foundations, Dispatch Spec, Orchestrate, and capability lifecycle routes.

Absent: `Interaction`, immutable launch snapshot, RouteDecision, proposal/approval registrar, runtime-profile admission, reasoning-request builder, executable evaluator, Orchestrate-to-Resonant action binding, durable parent/child Runs and reconciliation, targeted revisions, selective consumption, trusted memory intake/forgetting, GraphDelta/index compiler, grounding adapter, durable notifications, and promotion writer.

## Dependency graph

- `v0 — honest local fixture`: thread/interaction adapter → request-scoped handles/source fixture → immutable snapshot → RouteDecision → proposal/one approval → fake two-child host adapter → join → selective attach → local intake candidate. No durable memory or evaluator claim.
- `v1 — owner-backed product slice`: runtime-profile/registrar → Orchestrate-to-host adapter → durable Run projections/restart → addressed clarification → result consumption → trusted source/memory intake → GraphDelta/projection/grounding.
- `v2 — governed evolution`: executable admitted evaluator → exact effect boundary → Inventory evidence handoff → ontology candidate route → named AuthorityDecision/PromotionRecord → governed projection regeneration.

No v1 claim depends on pretending v2 authority exists.

## Exact vertical witness

The required witness is currently a **test specification, not executed proof**:

1. Ordinary user turn uses two explicit request-scoped handles and two source records.
2. Source chip reveals exact selection and deterministic bounded result.
3. User asks for two independent investigations.
4. Proposal shows exact roles/snapshots and one digest-bound approval.
5. Exactly two owner-correlated child Runs start; parent conversation remains usable.
6. A asks one targeted clarification; B continues unchanged.
7. A becomes `Blocked`; B becomes `Done` with artifact.
8. Reload restores both without duplicate announcement or inferred state.
9. User attaches B only; A, join, read state, and memory remain unchanged.
10. User separately creates a memory-intake candidate; absent trusted provider must visibly stop at local draft.
11. Correct/forget changes composed snapshot bytes and deterministic result.
12. Missing capability path produces zero spawn attempts.

The evaluator is excluded from v0 execution claims until an implementation passes its own counterfactual fixture family.

## Tests and budgets

Tests:

- Unit: digest stability/invalidation; graph delta/rebuild; bounded projection; route outcomes; judgment algebra once implemented; notification dedupe.
- Contract: preview/edit/decline zero effects; one approval/two action IDs; addressed revision affects A only; owner unknown remains unknown; join ≠ delivery; attach ≠ intake; result ≠ effect; candidate ≠ promotion.
- Restart: reconcile owner IDs without respawn; quarantine late results; preserve snapshot ancestry; no duplicate announcements/effects.
- Browser: all 12 vertical-witness assertions; keyboard-only operation; visible focus; non-color state; reduced motion; polite live regions.

Acceptance targets, all unmeasured:

- Retrieval timeout: 800 ms.
- Deterministic operation warm p95: ≤20 ms.
- Optional reasoning: p50 ≤1.5 s, p95 ≤4 s.
- Proposal UI ≤100 ms; approval acknowledgement ≤250 ms before owner progress.
- Added context ≤1,200 estimated tokens; total reasoning input ≤2,000.
- At most one presentation model call; no recursion.
- Projection ≤24 nodes, ≤48 edges, one hop default/two hard; ≤8 session handles.
- Derived cache ≤25 MB per fixture partition; no graph database without measured need.
- Route cards on ≤20% of ordinary turns; clarification ≤5% of routed attempts; ≤2 extra actions and exactly one approval; ≤1 announcement per meaningful transition.

## Verdict matrix

| Claim | Verdict |
|---|---|
| Coherent candidate architecture | `GO — BUILD_FROM_OWNED + ABSENT ADAPTERS` |
| Existing unified Augmentor product | `NO` |
| Executed vertical witness | `NO_WITNESS_CURRENT` |
| Existing bounded evaluator implementation | `KILL` |
| `semantic-judgment evaluator@1` research contract | `UNWITNESSED CANDIDATE` |
| Durable user memory/forgetting | `BLOCKED — owner/provider absent` |
| Two-child Resonant runtime/restart | `BLOCKED — adapters absent` |
| End-to-end ontology/promotion | `BLOCKED — fixture/design and writer absent` |
| Public Arcanum publication of private owner/state semantics | `KILL` |

## Open owner decisions, unresolved rows, feedback needs, blockers

Open decisions:

1. Name durable preference/source-memory owner; v0 otherwise remains request/session scoped.
2. Name approval registrar and runtime-profile admission owner.
3. Choose host operation bindings and durable Run/ancestry/reconciliation owner.
4. Name evaluator applicability/precedence/catalog authority owner before implementation.
5. Decide `AuthorityDecision` versus `PromotionRecord` identity/cardinality.
6. Name trusted intake/forgetting provider and deletion proof.
7. Assign GraphDelta, projection/cache, grounding, and invalidation adapters.
8. Define cancellation acknowledgement, late-result quarantine, and notification read-state owners.

Unresolved rows: `AUA-C03–C10`, `C13–C14`, `C16–C21` lack at least one executable adapter or owner-backed witness. `C09–C10` specifically require evaluator implementation evidence; they are not eligible for current-product claims.

Eligible feedback need: ask the runtime-control explorer only if exact current Resonant operation names or live capacity have changed since inspection; ask the authority explorer only after a named trusted memory/promotion provider exists. No feedback can repair the evaluator claim without new executable bytes and fixture receipts.

Blockers:

- No implemented-product, production, durable-memory, two-child, evaluator, or promotion claim.
- No protected effect from route confidence, proposal, approval, or judgment alone.
- No automatic intake from join, attachment, transcript, or result consumption.
- No graph, Inventory, ontology candidate, model, or receipt may become authority.
- No vertical witness can be marked executed from the inspected evidence.

Evidence-contract self-check: all load-bearing rows bind to an explorer row/section and an underlying selector; the evaluator claim was checked against its exact source and downgraded to `UNWITNESSED CANDIDATE`; no selector anchor was invented for implementation proof; observed, contract/design, absent, and unverified postures remain distinct.
