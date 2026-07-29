# Augmentor unified agent architecture

## Status and direct thesis

**Verdict: `GO — BUILD_FROM_OWNED + EXPLICIT ABSENT ADAPTERS`; `NO_WITNESS_CURRENT`.**

Augmentor should be one trusted conversational interface over retained owners, not
one collapsed state model. It may adapt, correlate, and progressively project
grounding, route choice, approval, concurrent work, artifacts, and knowledge
controls. It must not become a second router, scheduler, session store, job,
workspace, artifact owner, memory provider, graph truth store, reasoning authority,
ontology writer, effect authority, or promotion authority.

This is an implementation-usable **research architecture** and an exact contract for
a future deterministic local fixture. No fixture path, test path, browser witness,
production adapter, evaluator, effect runtime, durable write, promotion, deployment,
or measurement described here currently exists or ran. The evidence closure permits
this candidate report and nothing above that ceiling.

Evidence posture:

- **Observed** means repository bytes or an existing owner contract were inspected.
- **Designed** means accepted research specifies the behavior, but no joined
  implementation was observed.
- **Absent** means the named adapter, owner selection, or executable capability was
  not found.
- **Blocked** means a claim or route cannot proceed until a named dependency is
  supplied.
- **Deferred** means intentionally outside the earlier increment.
- **Specified-unexecuted** means exact future fixture bytes or assertions are pinned,
  but no artifact or result exists.

Primary exact bindings: explorer record
`research/2026-07-29-augmentor-unified-agent-architecture/research.md:7-624`;
connection synthesis
`research/2026-07-29-augmentor-unified-agent-architecture/synthesis-revised.md:17-429`;
final semantic and fixture repair
`research/2026-07-29-augmentor-unified-agent-architecture/synthesis-final.md:17-450`;
closure packet
`research/2026-07-29-augmentor-unified-agent-architecture/receipts/evidence-closure.json:1-68`.

## System context and retained owners

The system has three distinct planes whose objects may correlate but never inherit
one another's authority.

| Plane | Retained owner | Augmentor role | Current posture |
|---|---|---|---|
| Human/conversation | ResonantOS `ConversationThread`, request/session host, provider fabric | Present one transcript and progressive projections | Thread, chat, switch, compact-memory, generic run/artifact surfaces **observed**; unified `Interaction` and joined projections **absent** |
| Runtime/control | Dispatch Spec for route shape; Orchestrate for preflight/actions/join/close; selected Resonant delegation/provider/compute/artifact owners for execution truth | Translate an approved route into owner operations and correlate results | Owner contracts **observed**; production bindings, durable multi-Run projection, addressed input, restart reconciliation, selective consumption **absent** |
| Knowledge/authority | Each `SourceRecord.ownerRef`; Inventory for discovery/validation; ontology route for meaning candidates; authority-kind-specific canonical owner for decisions and writes | Read by reference, form disposable projections, submit candidates, show owner dispositions | Read/intake and normative authority seams **observed**; durable index owner, trusted writer, promotion route, and joined adapters **absent or unresolved** |

Request-scoped user handles belong to the request/session host. Durable source bytes
belong to the provider named by `ownerRef`; Living Archive is one observed seam, not
a universal memory owner. A disposable index has **no selected owner**. Inventory
validates handoff fitness, never truth or promotion. Ontology may produce a
non-authoritative candidate. Authority belongs only to the named owner selected for
the applicable authority kind and exact canonical selector.

DomainSpec remains private intent, public Arcanum remains generic execution, and
Saturn remains the private intent-to-evidence convergence frame. Saturn is not a
runtime, store, graph, scheduler, or authority. These allocations are bound to
`research.md:37-117,313-392` and `synthesis-revised.md:32-61`.

## Non-collapsing object model

### Human and context objects

- `Thread`: conversation identity and transcript owner.
- `Interaction`: one active concern within a Thread; not a Run.
- `ExplicitUserHandle` / `ConceptStateHandle`: request/session-scoped assertion,
  exclusion, correction, or tombstone.
- `SourceRecord{ownerRef,sourceRef,digest}`: immutable reference to provider-owned
  bytes.
- `ContextSnapshot{digest,horizon,selectors}`: immutable launch input.
- `RouteDecision`: immutable classification over input/config digests; neither
  proposal, approval, nor execution.
- `ReasoningPresentation`: answer plus source-bound claims and caveats; it cannot add
  premises or rewrite a deterministic result.

### Knowledge and authority objects

- `ProviderReview`: provider disposition of an intake request.
- `AcceptedSourceChange`: provider-accepted mutation with a new digest.
- `ProviderAdmittedEvidence`: provider-admitted evidence that need not mutate a
  source record.
- `GraphDelta` and disposable `SemanticIndex`: invalidatable derived retrieval state,
  never source truth.
- `BoundedProjection`: selected/excluded IDs and excerpts under explicit bounds.
- `MemoryIntakeRequest`: separately authorized request; neither accepted source nor
  evidence.
- `InventoryCandidateEvidenceSet`: selector package pending Inventory validation.
- `InventoryValidatedCandidateEvidenceSet`: handoff-fit candidate after Inventory
  validation; still non-canonical and non-promotional.
- `OntologyCandidate`: non-authoritative meaning proposal.
- `AuthorityDecision`: scoped decision of one named authority-kind owner.
- `PromotionRecordCompatibleTransition`: transition/audit evidence, not authority.
- `CanonicalAuthorityArtifact`: exact canonical bytes owned by the named owner.
- `GovernedProjection`: optional generated read model with canonical backlink.

### Runtime and effect objects

- `StrategyProposal{bytes,digest}`: preview only.
- `ApprovalRecord{proposalDigest,dispatchDigest}`: exact consumer approval.
- `Dispatch`: capability-bound shape validated by Dispatch Spec.
- `ReasoningRequest`, `JudgmentReceipt`, `ReasoningResult`: future evaluator
  objects; a receipt owns only its derivation.
- `Action`: Orchestrate-persisted operation.
- `Run` / `HostRunProjection`: host execution correlation, distinct from Thread and
  Interaction.
- `AttentionRequest` / addressed `InputRevision`: child-specific clarification bound
  to `ownerRunId`.
- `LifecycleJoin`: lifecycle reduction, not delivery.
- `ArtifactRef` / `BlockerRef`: owner-backed outcome handles.
- `ResultConsumption`: explicit Open, Attach, or Keep-separate operation.
- `EffectEnvelope`: idempotent request that can proceed only after a separately
  selected exact effect gate and owner.

Mandatory inequalities:

`index ≠ source`; `retrieval ≠ reasoning`; `judgment ≠ approval`;
`proposal ≠ execution`; `Dispatch ≠ Run`; `Run ≠ Thread`;
`join ≠ consumption`; `consumption ≠ intake`;
`intake ≠ provider acceptance`; `accepted source/evidence ≠ Inventory package`;
`Inventory validation ≠ canonical admission`; `Inventory ≠ ontology`;
`OntologyCandidate ≠ AuthorityDecision`;
`AuthorityDecision ≠ transition record`; `transition record ≠ canonical artifact`;
`projection ≠ canonical source`; `evaluator ≠ effect gate/owner/runtime`.

The catalog and inequalities incorporate the final non-collapse repair at
`synthesis-final.md:17-51` and the passing closure at
`reviews/non-collapse-final.md:9-27`.

## Exact connection catalog

Every target-only adapter below is proposed and absent. “Identity” means required
immutable correlation, not a claim that a schema is implemented.

### C01 — turn to Interaction

- Producer → artifact → consumer: Resonant chat shell → turn plus `threadId` →
  `InteractionResolverAdapter`.
- Authority: `ConversationThread` owns the thread; the adapter is an **absent host
  adapter**.
- Identity/timing: `threadId+turnId`, synchronous.
- Failure/observation: ambiguity asks one targeted continue/fresh question; explicit
  interrupt wins; record a transcript event without inventing an Interaction.
- Proof: thread **observed**, adapter **absent**.
- Binding: `synthesis-revised.md:91`; `research.md:293-312,393-617`.

### C02 — handles and provider records to snapshot

- C02a: request/session host → request-scoped handles → `SnapshotComposerAdapter`.
  The host owns handles; resolver/composer are **absent**. Bind handle ID and
  revision; exclude invalid or tombstoned handles.
- C02b: provider selected by `SourceRecord.ownerRef` → refs, bounded excerpts, and
  digests → composer. Provider owns bytes; the joined composer is **absent**.
  Bind `ownerRef+sourceRef+digest`; use the proposed 800 ms hard timeout; on timeout,
  continue transcript-only and never claim the source does not exist.
- Proof: settings and provider read seam **observed**; adapters **absent**.
- Binding: `synthesis-revised.md:92-93`; `research.md:37-117`.

### C03 — source change to disposable index

- Producer → artifact → consumer: `GraphDeltaCompilerAdapter` → `GraphDelta` →
  disposable semantic index.
- Authority: source providers retain truth; compiler, index owner, and adapter are
  **absent and require owner selection**.
- Identity/timing: `deltaId`, base/result versions, source digests; asynchronous.
- Failure/observation: stale base rejects or rebases; digest change invalidates;
  contradictions coexist; emit rebuild residue.
- Binding: `synthesis-revised.md:94`; `research.md:118-176`.

### C04 — index to bounded projection

- Disposable index → `BoundedProjection` → snapshot composer.
- Index/projection owner and adapter are **absent and require owner selection**.
- Bind projection digest plus selected/excluded IDs; execute synchronously under
  explicit bounds; narrow or abstain when required premises are missing.
- Proof: **designed/absent**.
- Binding: `synthesis-revised.md:95`; `research.md:118-176`.

### C05 — immutable context composition

- `SnapshotComposerAdapter` → `ContextSnapshot` → route and launch consumers.
- Host retains request-context authority; composer is **absent**.
- Bind snapshot digest; empty or stale input blocks; observe exact composed bytes and
  digest.
- Proof: filtered provider context **observed**, immutable launch snapshot
  **absent**.
- Binding: `synthesis-revised.md:96`; `research.md:293-312`.

### C06 — deterministic route

- `DeterministicRouteAdapter` → `RouteDecision` → route surface.
- Adapter and decision owner are **absent; host owner selection required**.
- Bind input/config/decision digests; low confidence offers rather than silently
  launching; missing capability blocks.
- Proof: accepted design, no Resonant projection/runtime.
- Binding: `synthesis-revised.md:97`; `research.md:313-392`.

### C07 — strategy preview

- `StrategyProposalAdapter` → exact proposal bytes/digest → proposal UI.
- Proposal projection owner and adapter are **absent**.
- Edit invalidates the digest; preview, edit, or decline causes zero registration,
  spawn, owner call, Run mutation, memory write, or effect.
- Binding: `synthesis-revised.md:98`; `research.md:313-392`.

### C08 — exact approval

- User → `ApprovalRecord` → `ApprovalRegistrarAdapter`.
- The consumer owns the approval act; registrar/owner selection is **absent**.
  Dispatch Spec later validates shape and is not approval owner.
- Bind proposal and Dispatch digests. Any scope, role, selector, wave, fallback, or
  byte drift requires revalidation and reapproval.
- Binding: `synthesis-revised.md:99`; `research.md:265-292`.

### C09 — future reasoning request

- Future reasoning adapter → `ReasoningRequest` containing authority snapshot,
  problem frame, and rule-catalog manifest → evaluator.
- Applicability/catalog owner and adapter are **absent**.
- Bind request, snapshot, and catalog digests; missing owner, facts, or valid catalog
  returns typed defer/invalidity with zero evaluator/actor/effect calls.
- Proof: `UNWITNESSED CANDIDATE`, **excluded from v0**.
- Binding: `synthesis-revised.md:100`; `research.md:265-292,357-380`.

### C10 — future judgment

- Evaluator → `JudgmentReceipt` → route/effect gate.
- Future evaluator owns derivation only; executable implementation is **absent**.
- Bind receipt digest; drift invalidates; unknown is never favorable.
- A receipt is neither approval, permission, effect gate, nor effect owner.
- Binding: `synthesis-revised.md:101`; `research.md:265-292,357-380`.

### C11 — Dispatch validation

- Route adapter → frozen `Dispatch` → Dispatch Spec.
- Dispatch Spec owns shape validation; bind Dispatch digest.
- Deterministic `flag`/`block`, missing authority, impossible dependency, or open
  lifecycle prevents execution.
- Proof: **implemented contract**, not product integration.
- Binding: `synthesis-revised.md:102`;
  `arcanum/formulae/dispatch-spec/SKILL.md:65-124`.

### C12 — Orchestrate preflight and actions

- Approved, validated Dispatch → run plan and persisted actions → Orchestrate.
- Orchestrate owns preflight/action lifecycle; bind dispatch/run/action IDs.
- Missing operation, authorization, or validity blocks with zero spawns; no nested
  model-backed CLI fallback.
- Proof: **implemented contract**.
- Binding: `synthesis-revised.md:103`;
  `arcanum/runtime/orchestrate/SKILL.md:77-116`.

### C13 — action to host Run

- Orchestrate action → exactly one spawn call → host-owned child Run.
- Orchestrate owns the action; selected Resonant delegation/provider/compute owner
  owns execution truth. Production binding is **absent**.
- Bind `actionId+ownerRunId+parentRunId`; duplicate, replayed, or unknown action
  blocks. Owner error is recorded, never implicitly retried.
- Binding: `synthesis-revised.md:104`; `research.md:293-312`.

### C14 — addressed clarification

- Selected host owner → `AttentionRequest`; user → addressed `InputRevision` → the
  same owner.
- `AddressedInputAdapter` and object schemas are **absent**; authority remains with
  the C13 execution owner.
- Bind `ownerRunId+revisionId+baseSnapshotDigest`; unmatched owner rejects; parent
  and sibling bytes must remain byte-equal.
- Binding: `synthesis-revised.md:105`; `research.md:313-392`.

### C15 — lifecycle join

- Orchestrate wait/inventory → normalized child receipts → `LifecycleJoin`.
- Orchestrate owns join/close; bind action IDs and receipt digests.
- Missing or mismatched result blocks; timeout interrupts once and records residue.
  Join does not deliver, attach, ingest, or authorize.
- Proof: **implemented contract**.
- Binding: `synthesis-revised.md:106`;
  `arcanum/runtime/orchestrate/SKILL.md:119-141`.

### C16 — selective result consumption

- Execution/artifact owners → `ArtifactRef` or `BlockerRef` →
  `ResultConsumptionAdapter`.
- Existing artifact/blocker owners retain truth; consumption adapter is **absent**.
- Bind ref digest and target Interaction. Attach must change no join, sibling,
  notification read state, or memory state.
- Proof: artifact foundations **observed**, adapter **absent**.
- Binding: `synthesis-revised.md:107`; `research.md:293-312`.

### C17 — intake and provider disposition

- C17a: user → `MemoryIntakeRequest` → provider review. Provider is resolved by
  `ownerRef`; trusted review/write adapter is **absent** where no provider exists.
  Bind intake ID, source/result digest, and one scope tag. Failure retains a local
  draft and claims neither submission nor persistence.
- C17b: provider review → `AcceptedSourceChange` or
  `ProviderAdmittedEvidence` → provider-owned source/evidence surface. Rejection
  leaves trusted bytes unchanged.
- Proof: intake seam **observed**; acceptance path **unverified**.
- Binding: `synthesis-revised.md:108-109`; `synthesis-final.md:33-51`.

### C18 — Inventory candidate validation

- C18a: accepted source/evidence → `InventoryCandidateEvidenceSet` → Inventory.
  Inventory owns discovery/validation only; bind canonical selectors and digests.
- C18b: Inventory validation → `InventoryValidatedCandidateEvidenceSet` → ontology
  handoff. Failure blocks handoff; pass proves candidate fitness only.
- Neither object is canonical, admitted authority, nor promotional.
- Proof: Inventory **observed**, candidate fixture/design level, handoff
  **unverified**.
- Binding: `synthesis-final.md:17-26,33-51`.

### C19 — ontology candidate

- Inventory → validated candidate EvidenceSet → ontology review →
  `OntologyCandidate`.
- Inventory owns the package; ontology route owns candidate review. Bind candidate
  ID and evidence digest.
- Reject/defer remains non-authoritative.
- Proof: **designed/unverified**.
- Binding: `synthesis-final.md:24-28,33-51`.

### C20 — named authority decision to canonical artifact

- C20a: ontology route → candidate/evidence → `AuthorityKindResolverAdapter`.
  Resolver is **absent** and must select one named owner plus exact private canonical
  selector; missing owner/selector blocks.
- C20b: named owner → `AuthorityDecision` → transition registrar. Decision belongs
  to that owner; durable identity, cardinality, schema, and registrar are
  **unresolved/absent**.
- C20c: owner-routed registrar →
  `PromotionRecordCompatibleTransition` → canonical writer gate. Registrar/writer
  and schema are **unresolved/absent**; bind decision and target selector. The
  transition is audit/state movement, never authority.
- C20d: named canonical owner → `CanonicalAuthorityArtifact` → optional projection
  generator. Owner owns bytes; writer/generator are **absent**. Failed write or
  backlink blocks projection.
- Binding: `synthesis-revised.md:112-115`; `research.md:177-258`;
  `synthesis-final.md:33-51`.

### C21 — protected effect

- Positive judgment plus independently passing exact effect gate →
  `EffectEnvelope` → effect owner.
- Operation-specific gate/owner selection and runtime are **absent** and can never be
  supplied by the evaluator.
- Bind an idempotency key; every non-positive judgment produces zero effect attempts.
- Proof: boundary contract only; **excluded from v0**.
- Binding: `synthesis-final.md:29-31`.

## Control and knowledge sequences

Ordinary control:

```text
Thread
→ Interaction
→ request handles + provider-owned source refs
→ optional disposable projection
→ immutable ContextSnapshot
→ RouteDecision
→ answer / grounded presentation
```

Consequential control:

```text
StrategyProposal
→ exact ApprovalRecord
→ frozen Dispatch
→ Dispatch Spec validation
→ Orchestrate preflight/actions
→ selected host operations
→ isolated parent/child Runs
→ addressed clarification
→ LifecycleJoin
→ independent ArtifactRef / BlockerRef
→ selective ResultConsumption
→ separately invoked MemoryIntakeRequest
```

Future reasoning, excluded from v0:

```text
ReasoningRequest → JudgmentReceipt → independent exact-effect gate
```

Knowledge evolution:

```text
MemoryIntakeRequest
→ provider review
→ AcceptedSourceChange or ProviderAdmittedEvidence
→ InventoryCandidateEvidenceSet
→ InventoryValidatedCandidateEvidenceSet
→ OntologyCandidate
→ authority-kind-specific named owner + exact selector
→ AuthorityDecision
→ PromotionRecordCompatibleTransition
→ CanonicalAuthorityArtifact
→ optional GovernedProjection with canonical backlink
```

Forgetting is also split. A request/session handle tombstone must change subsequent
composed bytes. Durable correction/deletion requires provider acceptance, a changed
digest or deletion marker, dependent invalidation, and rebuild. UI deletion alone is
not evidence.

## Thread, Interaction, Run, and child hierarchy

```text
Request/session host
└── Thread THREAD-0001
    ├── Interaction T1 ... T6
    └── parent Run RUN-PARENT-0001
        ├── child Run RUN-A-0001
        │   └── immutable A snapshot + addressed revision only
        └── child Run RUN-B-0001
            └── immutable B snapshot
```

Thread switching never reparents work or merges transcripts. A later parent turn is
not visible inside a child snapshot. Reload reconciles from persisted owner/fixture
state without respawn, invented terminal state, replayed announcements, or effects.

## One-interface surfaces and browser-testable journeys

The transcript remains primary. Audit machinery is available for verification but
never leads the experience.

| Surface | Shows | Must not imply |
|---|---|---|
| Transcript | User/assistant turns, grounded answer, concise terminal summaries | Merged child transcripts or hidden execution |
| Source/rationale chip | Selected/excluded handles, source refs, freshness, contestation, result, caveats | Graph mystique or source ownership |
| Proposal card | Exact route bytes, roles, bounded context, forbidden effects, edit/decline/approve | Approval or launch before the user acts |
| Thread list | Conversation identity, scoped unread/attention, switching | Run reparenting |
| Run tray | At most two fixture children, owner-confirmed state, attention, blockers | Scheduler controls or fabricated truth |
| Artifact surface | Open / Attach / Keep separate | Lifecycle success or memory intake |
| Knowledge/source view | Inspect, exclude, correct, tombstone, memory-off, provider-review status | Accepted durable correction before provider disposition |
| Notifications | Polite, deduplicated, meaningful child/thread transitions | Focus theft or replay after reload |

Required journeys: ordinary inline conversation without a card; grounded answer with
source inspection; request-scoped correction/forgetting that changes composed bytes;
route preview and one exact approval; parent conversation while two children run;
child-A-only clarification; A Blocked/B Done partial outcome; B-only attachment;
thread switch and reload restoration; session-local intake draft with zero trusted
writes; and a named capability gap with zero launch calls.

Accessibility: keyboard reachability, visible and restored focus, polite live
regions, no color-only state, and reduced-motion textual equivalence. These are
future browser assertions, not observed compliance.

## Capability-gap modes

- `inline`: honest read-only answer; no durable Run or effect claim.
- `helper`: one bounded independent target; not a governed Dispatch.
- `serial`: required by dependency/capacity; changing approved parallel bytes
  requires reapproval.
- `parallel`: only independent validated lanes, exact approval, and available host
  operations.
- `Easy`: inline or one reversible bounded Run.
- `Test`: deterministic fixtures against existing contracts.
- `Hardening`: reusable composition or primitive lifecycle under existing Arcanum
  owners.
- `install/compose`: separately authorized; never automatic after a gap.
- `block`: missing owner, operation, authority, trusted provider, exact gate, or
  executable capability.

Degraded language must name what is unavailable: “Answered here; advanced routing
was unavailable,” “Owner status unavailable; last confirmed state shown,” or
“`host.operation.not-installed` is not installed; nothing started.” Unknown remains
unknown.

## Current capabilities versus absent adapters

Observed current owners/contracts:

- ResonantOS `ConversationThread`, provider request/budget construction,
  `DelegationPacket`, `TaskWorkspace`, `ComputeJob`, `GoalWorkspace`, and generic
  artifact/blocker foundations.
- Dispatch Spec validation.
- Orchestrate preflight, persisted actions, native execution protocol, join, and
  close.
- Inventory discovery and selector validation.
- Normative private authority definitions and maps.

Absent production adapters/selections:

- Interaction and handle resolvers; immutable snapshot composer.
- Durable index/projection owner, GraphDelta compiler, bounded projection, and
  grounding.
- RouteDecision, proposal projection, approval registrar, and runtime-profile
  admission.
- Orchestrate-to-Resonant binding, durable parent/child Run projection, addressed
  input, cancellation acknowledgement, late-result quarantine, restart
  reconciliation, selective consumption, and notification persistence.
- Trusted provider review/write/forgetting.
- Evidence conversion, authority-kind resolution, named decision owner/registrar,
  transition registrar, canonical writer, and projection generator.
- Reasoning request builder, executable evaluator, applicability/catalog owner,
  independent effect gate/owner/runtime.

## Public/private boundary

Public Arcanum may expose generic lifecycle behavior and neutral adapter contracts.
It must not expose private DomainSpec state, Saturn framing, CyberAlchemy v2 paths,
kinds, gates, owner bindings, promotion records, or private authority semantics.
DomainSpec and CyberAlchemy v2 remain separate schema/authority systems aligned only
through explicit mappings. No private artifact becomes a public Arcanum contract.
Evidence: `research.md:219-240`; `synthesis-revised.md:164-171`.

## Exact future v0 witness contract

### Claim ceiling and identity

Proposed name: `aua-local-fixture@0.1.0`.

Proposed path `fixtures/aua-local-fixture-0.1.0.json` **does not exist**.
Proposed test paths and commands below **do not exist and did not run**. v0 uses a
local deterministic fake host, zero network, zero model/evaluator/effect calls, and
zero trusted writes.

Fixed identities:

```text
threadId=THREAD-0001
otherThreadId=THREAD-OTHER
parentRunId=RUN-PARENT-0001
actionA=ACT-A-0001   ownerRunA=RUN-A-0001
actionB=ACT-B-0001   ownerRunB=RUN-B-0001
blocker=BLOCK-A-001  artifact=ART-B-001
```

### Exact sources, contexts, and results

| Object | UTF-8 bytes include final newline | Length | SHA-256 |
|---|---|---:|---|
| `SRC-TRAVEL` | `Travel by rail only.\n` | 21 | `d1254ac0d209cb33cd7cf2649dfd01a8539eccf4951d194ebb8342e143e5b842` |
| `SRC-WORKSPACE` | `Workspace is quiet and closes at 18:00.\n` | 40 | `4d46a65b30bffa794522ca98bd70df5e9c3afc953c62d4d83bd6e615beeed64e` |
| before context | Exact payload at `synthesis-final.md:88-92` | 267 | `c9ad07cc7d5063297b48394d44f5b7206bc9c4692e0e5a949fd9a2bf66d8820f` |
| after H-LATE tombstone | Exact payload at `synthesis-final.md:93-96` | 242 | `577f2bd79d53503170dd3cdd2777e75bb608593aab4b4fd13a19897f5121acf6` |
| result before | `Use rail travel; choose the quiet workspace; late-night work is allowed.\n` | 73 | `d366710327212b54afc9b13e88c68e0ad034a74ebcf652b6cda3580020b6f486` |
| result after | `Use rail travel; choose the quiet workspace; do not schedule late-night work.\n` | 78 | `5245b8e31ae35e425d2b2ccf0ae6829ec48838674f2633e5b1b71cc602af5019` |

Handles before: `H-QUIET@r1=quiet workspace`,
`H-RAIL@r1=rail only`, `H-LATE@r1=late-night work allowed`. T5 produces
`H-LATE@r2:tombstoned`; selected IDs become
`H-QUIET,H-RAIL,SRC-TRAVEL,SRC-WORKSPACE` and H-LATE is excluded.

### Turns and route records

Exact turn text and turn digests are at `synthesis-final.md:106-151`.
The required routes are:

| Turn | Required mode | RouteDecision SHA-256 |
|---|---|---|
| T1 | `INLINE_GROUNDED` | `0c8e86a5a00818fe3fbb67fe23d3568aabb60d4d6ffe2715658c9314937eca63` |
| T2 | `STRATEGY_PROPOSAL` | `9e559ebcd866bf53dafd35f860c620d00d8b771d265fac70e35d717150b0b8ad` |
| T3P | `INLINE_PARENT_CONTINUATION` | `a742d617bf481004e3df0270cedded9cb37743cad7d00080253e6914b7e535e8` |
| T3A | `ADDRESSED_REVISION` | `319b68f1709d5cca11d0e2d1023e994ab23455005d85c9c48ea4567409e66386` |
| T4 | `RESULT_CONSUMPTION` | `9c481b33c20152cafbd7dacd2dccc74c87438ccb0a75313e0aba91ad0fc3deea` |
| T5 | `HANDLE_TOMBSTONE_AND_LOCAL_INTAKE_DRAFT` | `dc8df635c14204a2e37a9af07e5d19197705e96f169df507e669b2566880e2a5` |
| T6 | `CAPABILITY_GAP_BLOCK` | `3fdea23c02175a4ce1f1d1844c42feeb376173e0bce6a56b6dab1e885401db64` |

Each RouteDecision is minified one-line JSON plus newline with ordered keys
`decisionId,turnId,turnDigest,configDigest,mode`;
`decisionId="ROUTE-"+turnId`. Route-config digest:
`f68969e64b04e0850374d47ab5ba046cec017820d746dda52799a0d2705ae366`.

### Proposal, approval, snapshots, and result commands

- Initial proposal digest:
  `838866e8d450e79ffb66c2866f9543752a5c27e99ce83b33c21bdfebdb93a2a6`.
- Edited proposal digest:
  `4d228e5ba8cd85d5f5c199a810ba4207dc28a445ec667558289df283c8840502`.
- Dispatch digest:
  `5486389debd693c2311230343636385d10887dd3d0a9c08a188e37fefb41aedc`.
- Final approval digest:
  `27f041e1a8579b03d8fab9508932f3b2bd28e3a34ac172a58a040c5929d356f4`.
- A snapshot digest:
  `f80a4f48909078b7cc04b5f8666e47a34fdcfd1bb27b47f4b8427802076652f1`.
- B snapshot digest:
  `d2541bcf0e8472ce511a99e0b634c85656fe9aa0274ace2c9e155dde2745946c`.
- Addressed revision digest:
  `1601d1c790ad5d7042eb43b732221826148a5178ed789dfd93404c2a482afe34`.
- Join input/output/receipt digests:
  `2b79c8ea88ff94ece225cb12d9403291007ae048dd1d8df7d9b34470b00c771c`,
  `4f18322e1d2cc287c8f525c05273a9b6cd7e09468dd46fc48f099f04d3d00b1e`,
  `29172edf63ea64852fc365d55f68df323632ef0946967978ae832503529da58f`.
- Consume, tombstone, and local-intake-draft command digests:
  `34b81ef7422132286f35a45dc2283f85eefd1b8c47bb3d4c6afff17c77e24eed`,
  `f35e92a4b78735ae102d12b8c6a7e18bcec86e3566622bf89c82b89d76d33308`,
  `422020627e5d8796a4028da0c6cc53bfa4384651d067d458060fb546a11f8988`.
- Reload seed digest:
  `5251f2a1ce9358abf89a9a1a3f0a25a7c6e547287a31a93935296ef82d426162`.

Exact bytes for these objects are specified-unexecuted at
`synthesis-final.md:152-197`.

### Ordered event protocol

The future event log is 20 minified JSONL records, each with a final newline and key
order `schema,eventId,seq,orderKey,kind,parentRunId,ownerRunId,actionId,payload`.
Schema is `aua.event@0.1.0`; sequence is 1–20; `orderKey` is six-digit padded.

Required kinds in order:

```text
parent.registered
child.spawn_requested(A)
child.accepted(A)
child.spawn_requested(B)
child.accepted(B)
child.running(A)
child.running(B)
parent.turn_accepted(T3P)
child.attention_requested(A)
child.input_revision_addressed(A)
child.input_revision_accepted(A)
child.artifact_published(B, ART-B-001)
child.done(B, ART-B-001)
child.blocked(A, BLOCK-A-001)
join.reduced
thread.switched(THREAD-OTHER)
reload.requested
reconciliation.observed(A blocked)
reconciliation.observed(B done)
reload.completed
```

Exact IDs and payloads are at `synthesis-final.md:218-255`. Required serialization:
4,774 bytes, SHA-256
`5bb37e0f6d0f56be9651924fe54bc7378bab3564da434daccc4ae001a5e91191`.
This digest was mechanically checked in the synthesis process; the event file is
still **unimplemented/unexecuted**.

### Counter invariants

| Checkpoint | registration | spawn | ownerCall | addressed A/B | announcement | duplicate | attachment | intakeDraft | trustedWrite | effect | evaluator |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Initial / preview / edit / stale approval | 0 | 0 | 0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Valid approval | 1 | 0 | 0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Children accepted | 1 | 2 | 2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Addressed A accepted | 1 | 2 | 2 | 1/0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| Join reduced / after reload | 1 | 2 | 2 | 1/0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| Attach B | 1 | 2 | 2 | 1/0 | 2 | 0 | 1 | 0 | 0 | 0 | 0 |
| T5 local draft | 1 | 2 | 2 | 1/0 | 2 | 0 | 1 | 1 | 0 | 0 | 0 |
| T6 capability block | 1 | 2 | 2 | 1/0 | 2 | 0 | 1 | 1 | 0 | 0 | 0 |

T3A changes A only. T3P changes neither child snapshot. Reload changes no spawn,
owner-call, effect, read-state, or duplicate-announcement count. T4 changes no child,
join, notification, snapshot, memory-write, or effect state. T5 changes context and
result digests but produces only `MemoryIntakeDraft-001`.

### Future adapters, commands, and browser contract

Exact fixture-local adapter identities:

```text
FixtureThreadInteractionAdapter@0.1
FixtureHandleSourceAdapter@0.1
FixtureSnapshotComposer@0.1
FixtureDeterministicRouteAdapter@0.1
FixtureProposalApprovalRegistrar@0.1
FixtureTwoChildHostAdapter@0.1
FixtureLifecycleJoinReducer@0.1
FixtureReloadReconciler@0.1
FixtureResultConsumptionAdapter@0.1
FixtureLocalIntakeDraftAdapter@0.1
```

Specified future commands, not present or run:

```text
node --test tests/augmentor/aua-local-fixture-0.1.0.contract.test.mjs
playwright test tests/augmentor/aua-local-fixture-0.1.0.browser.spec.ts --project=chromium --workers=1
```

Browser selectors must cover transcript/composer and parent continuation; source
chip and H-QUIET/H-LATE/SRC-TRAVEL rows; proposal edit/approval/digest; both threads
and switching; reload; A/B runs and statuses; blocker, attention, addressed input,
artifact and attachment; notification/read state; H-LATE correction/tombstone;
intake draft; capability gap; fixture counters/event log; focus sentinel; and polite
live region. The exact selector list is at `synthesis-final.md:304-346`.

The browser must assert machine event/counter output, not merely cards: exact T1
digests; zero-effect preview/edit/stale approval; one registration; two fixed Runs;
parent T3P with byte-identical child snapshots; A-only clarification and focus
restore; B Done/A Blocked and exact join receipt; thread switch without merge;
reload with zero deltas; B-only attachment; H-LATE tombstone and changed digests;
one local draft/zero trusted writes; T6 zero-delta block; keyboard, focus, polite
live-region, non-color, and reduced-motion behavior.

### Fully pinned measurement contract

All targets are **unmeasured**. Use one process/worker, fixed seed, no network,
monotonic high-resolution clock, 100 unrecorded warm-ups, and 1,000 recorded samples
per operation. Sort ascending; nearest-rank p95 is index
`ceil(0.95 × 1000) - 1`; remove no outliers. Report min, median, p95, max, failures,
timeouts, environment/runtime lock, and fixture digest.

| Operation | Corpus | Target |
|---|---|---:|
| Provider lookup | Alternate exact two SourceRecords | hard timeout `800 ms` |
| Bounded composition/result | Alternate exact before/after contexts | warm p95 `≤20 ms` |
| Route classification | Cycle T1–T6 including T3P/T3A under fixed config | warm p95 `≤50 ms` |
| Proposal projection | Exact initial/edited pair to committed digest text | p95 `≤100 ms` |
| Approval acknowledgement | Click to registrar acknowledgement before host progress | p95 `≤250 ms` |

v0 has zero model calls and no tokenizer; UTF-8 byte length and SHA-256 govern. A
later model lane must pin provider, model revision, tokenizer implementation,
version and vocabulary digest, prompt-template digest, and sample corpus.

No graph database is allowed in v0. Future projection bounds: 24 nodes, 48 edges,
one hop default/two hard, at most eight session handles. A one-thread partition
includes derived index/projection, event, reload, and notification state, serialized
as canonical UTF-8 JSON before compression/transport; target `≤25 MB`.

`ATTENTION-CORPUS-001` contains 1,000 deterministic one-turn synthetic sessions:
800 inline/no card, 190 routed/card/no clarification, 10 routed/card plus one
clarification. Targets: cards ≤200/1,000; clarification ≤10/200 routed attempts; no
more than two extra actions and exactly one approval per consequential launch; at
most one announcement per meaningful transition and zero replay announcements.
This is synthetic acceptance design, not real-user evidence.

## Version dependency sequence

### v0 — deterministic local fixture

Implement and execute only the exact `aua-local-fixture@0.1.0` contract above.
Acceptance requires exact bytes/digests, event order, counter invariants, restart,
browser, accessibility, and measurement receipts. No production, durable-memory,
evaluator, authority, effect, deployment, or readiness claim follows.

### v1 — owner-backed product integration

Depends on executed v0. Select owners and implement provider-grounded context,
route/proposal/approval, runtime profile, Orchestrate-to-host operations, durable
Runs/restart, addressed input, selective consumption, notifications, and trusted
provider intake. Acceptance requires owner-backed contract and browser evidence.

### v2 — governed knowledge evolution and optional reasoning

Depends on owner-backed v1 evidence. Add admitted Inventory-to-ontology handoff,
authority-kind-specific resolution, named decision owner, transition registration,
canonical writing/projection, and separately—never implicitly—an implemented and
admitted evaluator plus independent exact-effect boundary.

## Verdict matrix

| Claim | Verdict |
|---|---|
| Candidate research architecture | `GO — BUILD_FROM_OWNED + EXPLICIT ABSENT ADAPTERS` |
| Current v0 | `NO` |
| Future `aua-local-fixture@0.1.0` | `SPECIFIED; NOT IMPLEMENTED OR EXECUTED` |
| Production integration | `BLOCKED — production adapters absent` |
| Executed vertical/browser witness | `NO_WITNESS_CURRENT` |
| Bounded evaluator implementation | `KILL` |
| Evaluator research contract | `UNWITNESSED CANDIDATE` |
| Evaluator as effect gate/owner/runtime | `KILL` |
| Generic memory/index owner | `KILL — owner selection required` |
| Durable correction/forgetting | `BLOCKED — trusted provider absent` |
| Two-child production execution/restart | `BLOCKED — owner bindings absent` |
| Inventory-validated candidate as canonical/promoted | `KILL` |
| End-to-end authority promotion | `BLOCKED — owner/selector/schemas unresolved` |
| Transition record as authority | `KILL` |
| Public leakage of private authority semantics | `KILL` |

## Open owner decisions

1. Select the durable index/projection owner; do not appoint a generic “memory
   domain.”
2. Select production RouteDecision, proposal projection, approval registrar, and
   runtime-profile owners.
3. Bind Orchestrate actions and addressed revisions to exact Resonant host
   operations and owners.
4. Select trusted provider review, write, correction, and forgetting owner.
5. Define cancellation acknowledgement, late-result quarantine, restart
   reconciliation, and notification read-state owners.
6. Select authority-kind resolver behavior, one named authority owner, and exact
   private canonical selector per candidate.
7. Resolve `AuthorityDecision` and `PromotionRecordCompatibleTransition` identity,
   cardinality, and durable schemas without collapsing them.
8. Select transition registrar, canonical writer, and optional projection generator.
9. Select evaluator applicability/catalog owner before evaluator implementation.
10. Select independent operation-specific effect gate, owner, and runtime before any
    protected effect.

Until those decisions and executable receipts exist: no product, production,
durable-memory, reasoning, promotion, release, or readiness claim; no effect from
route/proposal/approval/judgment alone; no automatic intake from join, attachment, or
consumption; and no graph, Inventory package, ontology candidate, model, transition
record, or UI projection may become authority.
