## Revised synthesis receipt

- `action_id`: `spawn-0004`
- `role_id`: `unified-architecture-synthesizer`
- `status`: `PASS_AS_RESEARCH_ARCHITECTURE_WITH_NO_EXECUTED_V0`
- `dispatch_id`: `2026-07-29-augmentor-unified-agent-architecture-route`
- `run_id`: `aua-20260729T051325Z`
- Zig-zag revision: `1/2`
- Mutation: none
- Proof posture: read-only synthesis. No fixture, test, browser run, runtime execution, measurement, or production adapter was observed.

### Evaluator disagreement resolved

Explorer 2 remains controlling. Explorer 1’s “bounded evaluator precedent” is only a research-contract precedent. The source says the repository owns no executable semantic relation, calls `semantic-judgment evaluator@1` an explicitly unwitnessed build/test candidate, and classifies it `UNWITNESSED CANDIDATE`. It is excluded from v0 code, calls, UI, effects, and acceptance. [Reasoning contract lines 5–9 and 122–132](projects/cyberalchemy-orchestrator/docs/research/2026-07-22-agent-reasoning-engine-contract/findings.md#L5); [precedent review](research/2026-07-29-augmentor-unified-agent-architecture/reviews/precedent.md); [non-vacuity review](research/2026-07-29-augmentor-unified-agent-architecture/reviews/non-vacuity.md).

## Product thesis and system context

Augmentor is a candidate single conversational interface over retained owners, with progressive projections for grounding, routing, approval, concurrent work, artifacts, and knowledge controls. One interface does not mean one state model.

Augmentor may adapt and project. It may not become a second router, scheduler, session store, job/workspace/artifact owner, memory provider, graph truth store, reasoning authority, ontology writer, or promotion authority. The defensible posture is:

- Architecture: `BUILD_FROM_OWNED + EXPLICIT ABSENT ADAPTERS`.
- Current unified product: absent.
- v0: future executable local-fixture family only.
- Production witness: absent.
- Evaluator: `UNWITNESSED CANDIDATE`.

[Explorer 2 findings](research/2026-07-29-augmentor-unified-agent-architecture/research.md#explorer-2--runtime-control-and-bounded-reasoning-plane); [Explorer 3 thesis](research/2026-07-29-augmentor-unified-agent-architecture/research.md#explorer-3--human-memory-and-one-interface-experience); [reviewer convergence](research/2026-07-29-augmentor-unified-agent-architecture/reviews/precedent.md).

## Planes and owners

| Plane | Retained current owner or unresolved selection | Augmentor’s permitted role | Posture |
|---|---|---|---|
| Conversation | ResonantOS `ConversationThread` and provider fabric | Project one interface | Thread/chat surfaces observed; `Interaction` adapter absent |
| Runtime/control | Dispatch Spec, Orchestrate, Resonant delegation/provider/compute/artifact owners | Translate approved route into existing owner operations | Core owners observed; bindings and durable multi-Run projection absent |
| Request-scoped user context | Resonant request/session host | Resolve ephemeral handles and compose launch bytes | Settings/context precedent observed; handle resolver absent |
| Durable source truth | Owner named by each `SourceRecord.ownerRef`; Living Archive is one observed read/intake seam | Read by ref; submit intake; never write around provider review | Read/intake seam observed; trusted write provider absent |
| Derived index/projection | **No selected owner** | Future adapter only after owner selection; derived state remains disposable | `ABSENT adapter/owner selection required` |
| Reasoning | Future separately versioned evaluator | Build request and render receipt only | Research contract; executable evaluator absent |
| Evidence | Inventory | Discover and package selector-bound candidate evidence | Observed discovery surface; candidate `EvidenceSet` fixture-level |
| Meaning | Ontology Vault/ontology route | Review admitted evidence into non-authoritative candidates | Designed/unverified |
| Authority | Authority-kind-specific named owner resolved from private authority map and canonical selector | Present decision/audit/projection; never infer owner | No universal owner; resolution/writer absent |
| Pillars | DomainSpec intent, public Arcanum execution, Saturn evidence loop | Preserve mappings and boundaries | Private intended architecture; Saturn is not runtime/storage |

[Explorer 1 owner matrix](research/2026-07-29-augmentor-unified-agent-architecture/research.md#explorer-1--authority-and-knowledge-plane); [precedent review row findings](research/2026-07-29-augmentor-unified-agent-architecture/reviews/precedent.md#row-findings).

## Non-collapsing typed object catalog

- `Thread`: conversation identity and transcript.
- `Interaction`: one active user concern within a thread.
- `ExplicitUserHandle` / `ConceptStateHandle`: request/session-scoped assertion, exclusion, correction, or tombstone.
- `SourceRecord{ownerRef,sourceRef,digest}`: provider-owned truth by immutable reference.
- `ProviderReview`: provider disposition of an intake request.
- `AcceptedSourceChange`: accepted provider mutation producing a new source digest.
- `AdmittedEvidence`: owner-admitted evidence that need not mutate a source record.
- `GraphDelta` / disposable `SemanticIndex`: derived invalidatable retrieval state.
- `BoundedProjection`: selected/excluded source, node, edge, and excerpt IDs under explicit limits.
- `ContextSnapshot{digest,horizon,selectors}`: immutable launch input.
- `RouteDecision`: immutable route classification; neither approval nor execution.
- `StrategyProposal{bytes,digest}`: preview only.
- `ApprovalRecord{proposalDigest,dispatchDigest}`: exact consumer approval.
- `Dispatch`: capability-bound shape validated by Dispatch Spec.
- `ReasoningRequest`, `JudgmentReceipt`, `ReasoningResult`: future non-authorizing evaluator objects.
- `Action`: Orchestrate-owned persisted operation.
- `Run` / `HostRunProjection`: host execution correlation, distinct from Thread/Interaction.
- `AttentionRequest` / addressed `InputRevision`: future child-specific clarification bound to `ownerRunId`.
- `LifecycleJoin`: lifecycle reduction, not delivery.
- `ArtifactRef` / `BlockerRef`: owner-backed outcome handles.
- `ResultConsumption`: explicit Open/Attach/Keep-separate operation.
- `EffectEnvelope` / effect-gate decision: protected effect boundary.
- `MemoryIntakeRequest`: separately authorized request, never an accepted source or evidence itself.
- `InventoryCandidateEvidenceSet`: selector package pending Inventory validation/admission.
- `OntologyCandidate`: non-authoritative meaning proposal.
- `AuthorityDecision`: scoped owner decision; durable identity/schema unresolved.
- `PromotionRecordCompatibleTransition`: transition/audit evidence; identity/cardinality/schema unresolved and not canonical authority.
- `CanonicalAuthorityArtifact`: authority-owning source bytes selected by exact canonical selector.
- `GovernedProjection`: optional generated read model with canonical backlink.

Required non-collapse:

`index ≠ source`; `retrieval ≠ reasoning`; `judgment ≠ approval`; `proposal ≠ execution`; `Dispatch ≠ Run`; `Run ≠ Thread`; `join ≠ consumption`; `consumption ≠ intake`; `MemoryIntakeRequest ≠ provider acceptance`; `accepted source/evidence ≠ Inventory package`; `Inventory ≠ ontology`; `OntologyCandidate ≠ AuthorityDecision`; `AuthorityDecision ≠ PromotionRecord-compatible transition`; transition record ≠ canonical authority artifact; projection ≠ canonical source.

[Non-collapse review](research/2026-07-29-augmentor-unified-agent-architecture/reviews/non-collapse.md).

## Exact connection catalog

Every target-only adapter name below is proposed and explicitly absent. “Identity” is an immutable correlation/digest requirement, not an implemented schema.

| ID | Producer → artifact/event → consumer | Exact owner and immutable identity | Selector / timing / failure / observability / proof |
|---|---|---|---|
| `AUA-C01` | Resonant chat shell → turn + thread ID → `InteractionResolverAdapter` | `ConversationThread` owns thread; `InteractionResolverAdapter` is **ABSENT host adapter**; `threadId+turnId` | Routing `#state-and-ownership-model`; sync; ambiguity asks one targeted question; transcript event; `thread observed / adapter absent` |
| `AUA-C02a` | Resonant request/session host → request-scoped handles → `SnapshotComposerAdapter` | Request/session host owns handles; both adapters **ABSENT**; handle IDs + revisions | Explorer 1 row 1, `#protected-user-handles`; sync; invalid/tombstoned handles excluded; selection log; `settings precedent / adapters absent` |
| `AUA-C02b` | Provider selected by `SourceRecord.ownerRef` → refs/excerpts/digests → `SnapshotComposerAdapter` | Source provider owns bytes; Living Archive read seam observed; composer **ABSENT**; `ownerRef+sourceRef+digest` | Explorer 1 row 2; ≤800 ms proposed timeout; timeout continues transcript-only and does not claim source absence; lookup log; `read seam observed / joined adapter absent` |
| `AUA-C03` | `GraphDeltaCompilerAdapter` → `GraphDelta` → disposable index | Compiler, index owner, and adapter are **ABSENT; owner selection required**; providers retain truth; `deltaId+base/result versions+source digests` | Explorer 1 row 3, `#semantic-index-and-graphdelta`; async; stale base rejects/rebases; rebuild receipt; `designed/absent` |
| `AUA-C04` | disposable index → `BoundedProjection` → snapshot composer | Index/projection owner and `BoundedProjectionAdapter` are **ABSENT; owner selection required**; projection digest + selected/excluded IDs | Explorer 1 row 4; sync bounded; narrow/abstain on missing premises; selection/residue log; `designed/absent` |
| `AUA-C05` | `SnapshotComposerAdapter` → `ContextSnapshot` → route/launch | Adapter **ABSENT**; host retains request context; snapshot digest | Routing `#state-and-ownership-model`, Explorer 2 row 2; stale/empty blocks; composed bytes/digest; `filtered provider context observed / immutable snapshot absent` |
| `AUA-C06` | `DeterministicRouteAdapter` → `RouteDecision` → route surface | Adapter and RouteDecision owner **ABSENT host selection required**; input/config/decision digests | Routing `#classification-and-route-decisions`; sync; low confidence offers, missing capability blocks; decision log; `accepted design/absent` |
| `AUA-C07` | `StrategyProposalAdapter` → exact proposal bytes/digest → proposal UI | Adapter and proposal projection owner **ABSENT host selection required**; proposal digest | Strategy `#public-neutral-adapter-and-runtime-profile-contract`; sync UI; edit invalidates digest and decline causes zero calls; UI event/counters; `designed/absent` |
| `AUA-C08` | User → `ApprovalRecord` → `ApprovalRegistrarAdapter` | Consumer owns approval act; registrar is **ABSENT host adapter/owner selection required**; Dispatch Spec validates later and is not approval owner; proposal/Dispatch digests | Strategy `#owner-identity-and-event-mappings`; Dispatch Spec `SKILL.md:87-124`; drift requires reapproval; registrar counter/audit; `contract/adapter absent` |
| `AUA-C09` | future reasoning adapter → `ReasoningRequest` → evaluator | Applicability/catalog owner and adapter **ABSENT**; request/snapshot/catalog digests | Reasoning contract lines 15–61; bounded sync; missing owner/facts/catalog defers; `UNWITNESSED CANDIDATE`, excluded from v0 |
| `AUA-C10` | evaluator → `JudgmentReceipt` → route/effect gate | Future evaluator owns derivation only; implementation **ABSENT**; receipt digest | Reasoning contract lines 63–78, 122–132; drift invalidates; derivation/residue; `UNWITNESSED CANDIDATE` |
| `AUA-C11` | route adapter → frozen Dispatch → Dispatch Spec | Dispatch Spec owns shape validation; Dispatch digest | `arcanum/formulae/dispatch-spec/SKILL.md:65-124`; deterministic; flag/block prevents execution; validation receipt; `implemented contract` |
| `AUA-C12` | approved validated Dispatch → run plan/actions → Orchestrate | Orchestrate owns preflight/action lifecycle; dispatch/run/action IDs | `arcanum/runtime/orchestrate/SKILL.md:77-116`; zero-spawn preflight; missing operation/authorization blocks; events/actions; `implemented contract` |
| `AUA-C13` | Orchestrate action → one spawn call → host-owned child Run | Orchestrate owns action; selected Resonant delegation/provider/compute owner owns execution; production binding **ABSENT**; `actionId+ownerRunId+parentRunId` | Strategy `#owner-identity-and-event-mappings`; async; duplicate/unknown blocks; owner transition log; `owners observed / adapter absent` |
| `AUA-C14` | selected host execution owner → `AttentionRequest`; user → addressed `InputRevision` → same owner | Future `AddressedInputAdapter` and object schemas **ABSENT**; authority remains with the execution owner selected in C13; mandatory `ownerRunId+revisionId+baseSnapshotDigest` | Routing `#child-runs-handoffs-isolation-and-recovery`; async; unmatched `ownerRunId` rejects and sibling/parent bytes remain equal; delivery/address counters; `absent` |
| `AUA-C15` | Orchestrate wait/inventory → child receipts → `LifecycleJoin` | Orchestrate owns join/close; action IDs + receipt digests | `orchestrate/SKILL.md:119-141`; bounded async; missing/mismatch blocks; join receipt; `implemented contract` |
| `AUA-C16` | execution/artifact owners → refs → `ResultConsumptionAdapter` | Existing artifact/blocker owners retain truth; consumption adapter **ABSENT**; ref digest + target interaction | Strategy `#owner-identity-and-event-mappings`; selective; attach changes no join/sibling/memory; post-command invariant snapshot; `artifact foundations observed / adapter absent` |
| `AUA-C17a` | User → `MemoryIntakeRequest` → provider review | Source provider resolved by `ownerRef`; trusted write/review adapter **ABSENT** where no provider exists; intake ID + source/result digest + scope tag | Integration guide `#scope-tag-discipline-lifecycle-mapping`; separately gated async; provider absence retains local draft and trusted-write count stays zero; `intake seam observed / writer absent` |
| `AUA-C17b` | Provider review → `AcceptedSourceChange` or `AdmittedEvidence` → source/evidence surface | Same source/evidence provider owns acceptance; new source digest or evidence digest | Precedent review C17/C18; rejection leaves trusted bytes unchanged; provider disposition and digest transition; `acceptance path unverified` |
| `AUA-C18` | Accepted source/evidence surface → candidate selector package → Inventory | Inventory owns discovery/validation only; package identity binds canonical selectors and digests | Ontology-population `#direct-answer/#handoff-shape-for-ontology-vault`; async; incomplete package remains candidate; Inventory validation receipt; `Inventory observed / EvidenceSet candidate fixture-level` |
| `AUA-C19` | Inventory → admitted `EvidenceSet` → Ontology Vault review → `OntologyCandidate` | Inventory owns package; ontology route owns candidate review; candidate ID + evidence digest | Ontology-population `#first-population-run`; async; reject/defer remains non-authoritative; candidate status; `designed/unverified` |
| `AUA-C20a` | Ontology route → candidate + evidence → authority-kind resolution | `AuthorityKindResolverAdapter` **ABSENT**; it must resolve one named owner and exact private canonical selector, never a universal “authority owner”; candidate/evidence digests | CAV2 `#cav2-d34-authority`; missing owner/selector blocks; resolution record; `normative map observed / adapter absent` |
| `AUA-C20b` | Resolved named owner → `AuthorityDecision` → transition/audit registrar | Decision belongs to the owner selected in C20a; durable schema/cardinality and registrar **UNRESOLVED/ABSENT**; decision identity TBD | CAV2 `#cav2-d5-promotion-gate`; no decision means no transition; decision basis/scope/challenge record; `normative definition / executable owner path unverified` |
| `AUA-C20c` | Owner-routed registrar → `PromotionRecordCompatibleTransition` → canonical writer gate | Registrar/writer owner and schema **UNRESOLVED/ABSENT**; transition must exact-bind decision + target canonical selector | Non-collapse required repair; transition records audit/state movement only; it is not authority; `absent` |
| `AUA-C20d` | Named canonical owner → canonical authority artifact → optional projection generator | Owner selected in C20a owns source bytes; writer/generator adapters **ABSENT**; canonical digest + exact selector | CAV2 authority definitions and `SOURCE-MAP.md#ingest-rules`; failed write/backlink blocks projection; source commit/write receipt then projection receipt; `rules observed / writers absent` |
| `AUA-C21` | positive judgment + separate exact effect-gate pass → effect envelope → effect owner | Exact effect owner/gate, never evaluator; idempotency key | Reasoning contract lines 110–114; non-positive gives zero attempts; effect receipt; `boundary contract only`, excluded from v0 |

## End-to-end control sequence

Ordinary path:

`Thread → Interaction → request-scoped handles + provider-owned source refs → optional disposable projection → immutable ContextSnapshot → RouteDecision → answer/presentation`.

Consequential route:

`StrategyProposal → exact ApprovalRecord → frozen Dispatch → Dispatch Spec → Orchestrate plan/actions → selected host operations → isolated parent/child Runs → addressed clarification → LifecycleJoin → independent artifact/blocker refs → selective ResultConsumption`.

The evaluator path is not in v0. If later implemented, it remains:

`ReasoningRequest → JudgmentReceipt → separate exact-effect gate`; receipt is never approval or permission.

## Session, Thread, Run, and child hierarchy

```text
Request/session host
└── Thread
    ├── Interaction N
    └── parent Run correlation
        ├── child Run A: ownerRunId A + immutable snapshot A
        └── child Run B: ownerRunId B + immutable snapshot B
```

Run is not Thread or Interaction. Reload must reconcile projections from persisted fixture/owner state without respawn, transcript merging, work reparenting, invented terminal state, repeated announcements, or effects.

## Knowledge lifecycle

The repaired lifecycle is:

```text
MemoryIntakeRequest
  → provider review
  → AcceptedSourceChange with new SourceRecord digest OR AdmittedEvidence
  → Inventory candidate EvidenceSet/selector package
  → admitted EvidenceSet
  → OntologyCandidate
  → authority-kind resolution to one named owner + exact canonical selector
  → AuthorityDecision
  → PromotionRecord-compatible transition/audit record
  → canonical authority artifact
  → optional governed projection with canonical backlink
```

An intake request manufactures neither source truth nor evidence. Inventory cannot promote. Ontology cannot decide authority. `AuthorityDecision` and `PromotionRecordCompatibleTransition` remain behaviorally separate while their durable identity/cardinality/schema remain unresolved. The transition/audit record is never canonical authority. [Precedent review C17–C20](research/2026-07-29-augmentor-unified-agent-architecture/reviews/precedent.md#row-findings); [non-collapse required repair](research/2026-07-29-augmentor-unified-agent-architecture/reviews/non-collapse.md#required-repair).

Forgetting also remains split:

- Request/session handle tombstone changes subsequent composed bytes.
- Durable deletion/correction requires provider acceptance, a changed digest or deletion marker, dependent invalidation, and rebuild.
- UI deletion alone proves neither.

## Control lifecycle

`turn → Interaction → ContextSnapshot → RouteDecision → optional StrategyProposal → exact approval → validated Dispatch → Orchestrate preflight/actions → host Runs → owner transitions → join → independent results → selective consumption → separately invoked MemoryIntakeRequest`.

Preview/edit/decline yields zero registration, spawn, or owner calls. Approval mutation invalidates the digest. Join does not deliver, attach, ingest, or authorize. Unknown owner state remains unknown.

## One-interface surfaces

- Transcript: turns and concise answers/summaries; no child transcript merging.
- Rationale/source chip: selected/excluded handles and sources, freshness, contestation, result, caveats.
- Proposal card: exact proposed bytes, roles, bounded context, forbidden effects, edit/decline/approve.
- Thread list: conversation identity and scoped unread/attention.
- Run tray: no more than two fixture children; state projection only.
- Artifact surface: Open / Attach / Keep separate.
- Knowledge/source view: inspect/exclude/correct/tombstone/memory-off and provider-review status.
- Notifications: polite, deduplicated, meaningful child/thread transitions only.

No card, receipt, graph, or dashboard proves its backend.

## Public/private boundary

Public Arcanum may expose generic lifecycle and neutral adapter behavior. It must not expose private DomainSpec state, Saturn framing, CyberAlchemy v2 paths/kinds/gates/owner bindings, or private promotion records. Saturn remains a private convergence-loop frame, not storage, graph, scheduler, runtime, or authority. DomainSpec and CAV2 remain separate and may align only through explicit mapping edges. [Explorer 1 reject tests](research/2026-07-29-augmentor-unified-agent-architecture/research.md#explorer-1--authority-and-knowledge-plane).

## Capability-gap routes

- `inline`: sufficient read-only answer; no durable Run/effect claim.
- `helper`: one bounded independent target; not Dispatch.
- `serial`: dependency/capacity-driven; changing approved parallel bytes requires reapproval.
- `parallel`: only validated independent lanes, exact approval, and available host operations.
- `Easy`: inline or one reversible bounded Run.
- `Test`: deterministic fixture family and explicit adapters.
- `Hardening`: reusable composition/primitive lifecycle under existing Arcanum owners.
- `install/compose`: separately authorized.
- `block`: missing owner, operation, authority, trusted provider, exact gate, or executable capability.

## Current and absent adapter map

Current owners/contracts:

- ResonantOS `ConversationThread`, provider request/budget construction, `DelegationPacket`, `TaskWorkspace`, `ComputeJob`, `GoalWorkspace`, artifact/blocker foundations.
- Dispatch Spec shape validation.
- Orchestrate preflight, persisted actions, native execution protocol, joins, and close.
- Inventory discovery/selector machinery.
- Normative private authority definitions/maps.

All production adapters in the proposed integrated path are absent:

- Interaction resolver, handle resolver, snapshot composer.
- Durable index owner, GraphDelta compiler, bounded projection, grounding.
- RouteDecision, proposal projection, approval registrar, runtime-profile admission.
- Orchestrate-to-Resonant operation binding, durable parent/child Run projection, addressed input, restart reconciliation.
- Selective result consumption and notification persistence.
- Trusted provider review/write/forgetting.
- Evidence-conversion, authority-kind resolution, authority decision registrar, transition/audit registrar, canonical writer, projection generator.
- Reasoning request builder, executable evaluator, exact effect runtime.

## Version dependency graph

### v0 — future `aua-local-fixture@0.1.0`, not currently present

v0 is admissible only as a versioned executable deterministic local-fixture family. It has no production adapter, durable-memory, evaluator, authority, or deployment claim.

Required literal fixture payload:

- Turns:
  - `T1`: “Plan a quiet two-day writing retreat using my explicit preferences and the two supplied records.”
  - `T2`: “Run two independent checks: A travel constraints, B workspace suitability.”
  - `T3A`: addressed answer “A: rail only.”
  - `T4`: “Attach only B.”
  - `T5`: “Draft a session correction: remove late-night work.”
  - `T6`: missing-operation request.
- Handles: `H-QUIET`, `H-RAIL`, plus tombstoned/excluded `H-LATE`.
- Sources: `SRC-TRAVEL@digest-a`, `SRC-WORKSPACE@digest-b`.
- Projection: explicit selected IDs `[H-QUIET,H-RAIL,SRC-TRAVEL,SRC-WORKSPACE]`; excluded `[H-LATE]`.
- Expected composed UTF-8 bytes, byte length, SHA-256 digest, and deterministic grounded result fixture.
- Expected `RouteDecision` for every turn, including input/config digest.
- Exact initial proposal bytes/digest, one edited byte sequence/new digest, stale-approval rejection, final `ApprovalRecord`.
- Fake-host scripts:
  - A: accepted → running → attention → addressed revision → blocked.
  - B: accepted → running → artifact → done.
- Identities: fixed parent/action/ownerRun IDs.
- Marker corpus proving no parent/sibling transcript/context bleed.
- `BLOCK-A-001`, `ART-B-001`.
- Seeded reload image with notification read state and owner correlations.
- Selective command `attach ART-B-001 to Interaction T4`.
- `MemoryIntakeDraft-001`; trusted-write count remains zero.
- Missing capability `host.operation.not-installed`; spawn count remains zero.

Exact fixture-local adapters:

- `FixtureThreadInteractionAdapter@0.1`
- `FixtureHandleSourceAdapter@0.1`
- `FixtureSnapshotComposer@0.1`
- `FixtureDeterministicRouteAdapter@0.1`
- `FixtureProposalApprovalRegistrar@0.1`
- `FixtureTwoChildHostAdapter@0.1`
- `FixtureLifecycleJoinReducer@0.1`
- `FixtureReloadReconciler@0.1`
- `FixtureResultConsumptionAdapter@0.1`
- `FixtureLocalIntakeDraftAdapter@0.1`

Machine counters/invariants:

- Preview/edit/decline: `registration=0`, `spawn=0`, `ownerCall=0`.
- Final approval: `registration=1`; exactly two distinct action and ownerRun IDs.
- Stale approval: rejected; all effect counters unchanged.
- Addressed input: A count `1`, B `0`; parent and B snapshot digests byte-equal before/after.
- Outcomes: A `Blocked`, B `Done`; join dependency blocked while B remains consumable.
- Reload: spawn/effect count unchanged; duplicate announcement count `0`.
- Attach B: attachment count `1`; A state, join, notification read state, and memory-write count unchanged.
- Intake draft: local draft count `1`, trusted-write count `0`.
- Missing capability: registration/spawn/owner calls all `0`.
- Evaluator calls/UI/effects: all `0`.

Future exact commands:

```text
node --test tests/augmentor/aua-local-fixture-0.1.0.contract.test.mjs
playwright test tests/augmentor/aua-local-fixture-0.1.0.browser.spec.ts --project=chromium --workers=1
```

Future browser selectors:

```text
[data-testid="augmentor-transcript"]
[data-testid="source-chip"]
[data-testid="source-row-H-QUIET"]
[data-testid="source-row-SRC-TRAVEL"]
[data-testid="strategy-proposal"]
[data-testid="proposal-edit"]
[data-testid="proposal-approve"]
[data-testid="run-A"]
[data-testid="run-B"]
[data-testid="attention-A"]
[data-testid="attention-input-A"]
[data-testid="artifact-ART-B-001"]
[data-testid="attach-ART-B-001"]
[data-testid="intake-draft-MemoryIntakeDraft-001"]
[data-testid="capability-gap-host.operation.not-installed"]
```

Browser assertions must inspect fixture event/counter output, not only rendered cards. These paths, commands, selectors, fixtures, and adapters are **specified future targets; none exists or ran**. [Non-vacuity required repair](research/2026-07-29-augmentor-unified-agent-architecture/reviews/non-vacuity.md#required-repair).

### v1 — owner-backed production integration

Depends on executed v0, then requires selected production owners and implemented adapters for provider-grounded context, route/proposal/approval, runtime profile, Orchestrate-to-host execution, durable Runs/restart, addressed input, selective consumption, and trusted provider intake. All are currently absent.

### v2 — governed evolution and optional reasoning

Depends on v1 owner-backed evidence. Adds admitted Inventory-to-ontology handoff, authority-kind-specific named decision owner, transition/audit registration, canonical writing/projection, and only separately an implemented/admitted semantic evaluator plus exact effect boundary. These are absent or unresolved.

## Exact vertical witness

The exact witness is the future `aua-local-fixture@0.1.0` family above. Acceptance requires:

1. Literal T1 proves exact handle/source selection, exclusions, composed bytes/digest, deterministic result, and source-chip expansion.
2. Literal T2 proves exact RouteDecision and proposal bytes/digest.
3. Edit changes the digest; stale approval yields zero effects; final one approval registers once.
4. Fake host receives exactly two actions with fixed distinct Run IDs.
5. Parent remains usable; T3A reaches A only.
6. A blocks and B completes with exact handles.
7. Reload seed restores both with no respawn or duplicate announcement.
8. T4 attaches B only and preserves all unrelated state.
9. T5 changes request-scoped composed bytes/result and produces only a local intake draft.
10. T6 names the missing operation and produces zero spawns.
11. Evaluator call/UI/effect counters remain zero.

Current verdict: `SPECIFIED FUTURE WITNESS; UNEXECUTED`.

## Tests and budgets

Test layers:

- Unit: canonical JSON/UTF-8 serialization, digest stability, selection/exclusion, deterministic route, proposal mutation, join reduction, notification dedupe.
- Contract: all fixture counters and non-collapse invariants.
- Restart: seeded hydration, owner reconciliation without respawn, late-result quarantine, preserved ancestry, no duplicate announcements/effects.
- Browser: literal fixture journey, keyboard-only controls, visible focus, non-color status, reduced motion, polite live regions, and machine-counter inspection.

All measurements are unexecuted targets:

| Operation | Target | Required future measurement contract |
|---|---:|---|
| Provider/source lookup | hard timeout `800 ms` | monotonic clock; named fixture/provider; timeout/degraded count |
| Deterministic bounded projection/result | warm p95 `≤20 ms` | fixed corpus, warmup count, sample count, percentile method |
| Deterministic route classification | warm p95 `≤50 ms` | fixed turn/config corpus, warmup/sample/percentile definition |
| Proposal UI projection | `≤100 ms` | deterministic browser seed; input event to visible committed state |
| Approval acknowledgement | `≤250 ms` | click to registrar acknowledgement before owner progress |
| Optional later reasoning | p50 `≤1.5 s`, p95 `≤4 s` | excluded from v0; model/provider/version and congestion policy required |

Other unexecuted budgets:

- Added source/graph context ≤1,200 estimated tokens; total reasoning input ≤2,000, with tokenizer/model version pinned.
- Zero or one presentation-model call; no recursion.
- Projection ≤24 nodes, ≤48 edges, one hop default/two hard; preservation proof against fixed corpus required.
- ≤8 session handles.
- Derived serialization ≤25 MB per fixture partition, measured at a named serialization boundary.
- Route cards on ≤20% of ordinary turns; clarification ≤5% of routed attempts; ≤2 additional actions and exactly one approval; ≤1 announcement per meaningful transition. Each needs denominator, cohort, and measurement window.

No target is acceptance evidence until its receipt exists.

## Verdict matrix

| Claim | Revised verdict |
|---|---|
| Candidate architecture | `GO — BUILD_FROM_OWNED + EXPLICIT ABSENT ADAPTERS` |
| Current v0 | `NO` |
| Future `aua-local-fixture@0.1.0` | `SPECIFIED, NOT IMPLEMENTED OR EXECUTED` |
| Production Augmentor integration | `BLOCKED — production adapters absent` |
| Executed vertical/browser witness | `NO_WITNESS_CURRENT` |
| Bounded evaluator implementation | `KILL` |
| `semantic-judgment evaluator@1` contract | `UNWITNESSED CANDIDATE` |
| Generic “memory domain” owner | `KILL — owner selection required` |
| Durable intake/correction/forgetting | `BLOCKED — trusted provider absent` |
| Two-child Resonant execution/restart | `BLOCKED — owner bindings/adapters absent` |
| End-to-end authority promotion | `BLOCKED — exact owner/selector and schemas unresolved` |
| Transition record as canonical authority | `KILL` |
| Public leakage of private authority/state semantics | `KILL` |

## Open owner decisions and blockers

1. Select durable index/projection owner; no generic memory domain may be appointed.
2. Select production RouteDecision, proposal projection, approval registrar, and runtime-profile owners.
3. Bind Orchestrate actions and addressed revisions to exact Resonant host owners/operations.
4. Select trusted provider review/write/forgetting owner.
5. Select authority-kind resolver behavior, one named authority owner, and exact canonical selector per candidate.
6. Resolve `AuthorityDecision` and `PromotionRecordCompatibleTransition` identity, cardinality, and durable schema without collapsing them.
7. Select canonical writer and optional projection generator.
8. Select evaluator applicability/catalog owner before any implementation.
9. Define cancellation acknowledgement, late-result quarantine, and notification read-state owners.

Blockers remain: no production, durable-memory, evaluator, promotion, or executed-witness claim; no protected effect from route/proposal/approval/judgment alone; no automatic intake from join/attachment/consumption; no graph, Inventory package, ontology candidate, model, or audit record may become authority.

## Repair-closure table

| Reviewer requirement | Revised closure |
|---|---|
| Split handle owner from source truth; mark resolver absent | `C02a`, `C02b`; planes table |
| Do not appoint generic memory domain | `C03`, `C04`; owner selection explicitly absent |
| Mark proposal and approval owners/adapters absent | `C06–C08`; production adapter map |
| Bind addressed revision to selected host owner via `ownerRunId` | `C14`; hierarchy and v0 counters |
| Insert provider acceptance before Inventory | `C17a`, `C17b`, `C18`; knowledge lifecycle |
| Split decision, transition/audit, canonical source, projection | `C20a–C20d`; object catalog and knowledge lifecycle |
| Keep decision/PromotionRecord identity/cardinality/schema unresolved | Catalog, `C20b–C20c`, open decision 6 |
| Define future executable versioned v0, not diagrams/cards | v0 `aua-local-fixture@0.1.0`; vertical witness |
| Supply literal turns, fixtures, bytes/digests, IDs, scripts, reload, attach, intake, gap | v0 fixture payload |
| Name exact local adapters and mark production adapters absent | v0 adapter list; current/absent map |
| Add machine counters and invariants | v0 counters/invariants |
| Add browser commands/selectors and require machine evidence | v0 commands/selectors; browser tests |
| Exclude evaluator from v0 | Evaluator resolution; `C09–C10`; v0 zero counters |
| Distinguish deterministic operation ≤20 ms from route classification ≤50 ms | Tests and budgets table |
| Keep all measurements unexecuted | Receipt posture and budget section |

## Unresolved evidence rows and feedback need

Unresolved evidence rows:

- Owner selection: `C03`, `C04`, `C06–C08`, `C20a–C20d`.
- Production adapters: `C01–C08`, `C13–C14`, `C16–C20d`.
- Executable reasoning/effect evidence: `C09`, `C10`, `C21`.
- Provider acceptance and evidence conversion: `C17a–C18`.
- Ontology execution: `C19`.
- v0 fixtures, commands, selectors, counters, tests, and measurements: entirely unimplemented/unexecuted.

No explorer feedback is genuinely needed to complete this research repair: the three reviews supply the necessary corrections. Further feedback would become useful only after a user/owner selects the durable index provider, production host bindings, trusted source provider, or authority-kind-specific canonical owner/selector. Those are owner decisions or new implementation evidence, not ambiguities resolvable by averaging existing explorer reports.

Evidence-contract self-check: generic owner nouns identified by reviewers were replaced with current owners or explicit absent adapter/owner-selection requirements; intake no longer manufactures evidence; authority decision, transition/audit, canonical artifact, and projection are separate; v0 is a future exact executable fixture family, not a current artifact; all production adapters and measurements are marked absent/unexecuted; evaluator remains excluded and `UNWITNESSED CANDIDATE`; no vertical witness is claimed executed.
