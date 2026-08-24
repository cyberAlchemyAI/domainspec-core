# Goal

Determine the smallest build-from-owned architecture for adding the public Arcanum Subagent Strategy lifecycle to Augmentor without importing private DomainSpec authority or creating a second scheduler, registry, session store, execution owner, artifact owner, or memory path.

# TL;DR

The bounded implementation direction is an additive Augmentor proposal-and-control projection over existing owners: public Subagent Strategy supplies lifecycle semantics, Dispatch Spec validates the route, Orchestrate owns native action reconciliation, and ResonantOS delegation, workspace, compute, goal, provider, artifact, thread, and persistence owners carry host behavior. `StrategyProposal` and `RouteDecision` are both **`BUILD-FROM-OWNED + NOVEL-ATTEMPT`**: their semantics derive from owned lifecycle and routing contracts, but no Resonant implementation exists. The honest ceiling is **`NO_WITNESS_CURRENT`**. Build and deterministic-fixture work may proceed, but execution, user value, performance, readiness, release, promotion, and production claims may not. [Agent 1, `research.md:7-107`; Agent 2, `research.md:122-288`; closure C1, C2, C5, C8]

# Context

The accepted routing/session work proposed thread-local interactions, immutable route decisions, owner-correlated attempts, notifications, and a two-child Strategy-plus-Whisper witness. This dispatch was needed because current ResonantOS has reusable host owners but one global transient chat-run guard, while public Arcanum has a lifecycle seed but no Resonant runtime profile or medium/complex consumer proof. The four explorer lenses agree on the additive boundary: contract archaeology identifies lifecycle authority; runtime tracing identifies reusable owners and missing bytes; human-factors work defines a falsifiable conversational journey; official protocol precedent supports explicit approval, durable correlation, reconciliation, and non-authoritative notifications without supplying local authority. [Agents 1–4, `research.md:1-450`; closure C1–C4]

## Verdict and use-mode matrix

Evidence labels describe inspected bytes or proposed use, not production deployment.

| Surface | Current verdict | Required use mode |
|---|---|---|
| Public Subagent Strategy lifecycle/profile template | `CURRENT-SEED` | Reuse lifecycle ordering, exact freeze, registration order, dependency gates, closeout, and profile variables; do not claim consumer proof. |
| Dispatch Spec | Current owner contract | Validate authorization, role/capability bindings, waves, scopes, receipts, and terminal shape; never execute. |
| Orchestrate and its host profile | Current owner contract | Preflight persisted actions, invoke native operations exactly once, reconcile, gate, interrupt, and close. |
| Resonant grants, `DelegationPacket`, `TaskWorkspace`, optional `ComputeJob`, `GoalWorkspace`, provider and artifact owners | Current seams | Reference and invoke through adapters; never copy their policy or terminal truth. |
| Global chat-run guard | Current blocker | Replace its product-wide cardinality assumption with owner-aware foreground/child admission; do not repurpose it as a scheduler. |
| `StrategyProposal` | **`BUILD-FROM-OWNED + NOVEL-ATTEMPT`** | Side-effect-free Augmentor projection over the public lifecycle and accepted routing semantics. |
| `RouteDecision` | **`BUILD-FROM-OWNED + NOVEL-ATTEMPT`** | Immutable choice/rationale projection over accepted routing semantics; never approval or execution authority. |
| Runtime-profile discovery/admission | `BUILD-FROM-OWNED + NOVEL-ATTEMPT` | Bind the public profile template to current Resonant grants and native operations. |
| Approval, Resonant registrar binding, run/input/outcome/notification projections | `NOVEL-ATTEMPT` | Add consumer-owned projections and gates with opaque owner references. |
| Action-to-owner adapter, result delivery/consumption, two-child binding | `BUILD-FROM-OWNED + NOVEL-ATTEMPT` | Compose Orchestrate actions with current host owners and artifacts. |
| Proposal card, child tray, deterministic fixture | `NOVEL-ATTEMPT` | Acceptance implementation only. |

The route validator’s `VALIDATION=pass` proves route shape only. The current guard and explicit “execution has not started” delegation responses establish why the product witness is absent. [Agent 1, `research.md:11-71`; Agent 2, `research.md:140-206`; Agent 4, `research.md:352-450`; closure C2, C8]

## Public-neutral adapter and runtime-profile contract

The browser-safe `StrategyProposal` carries:

- proposal, request, thread, goal, and evidence-selector references/digests;
- trigger reasons and named capability;
- roles containing `roleId`, purpose, `capabilityRef`, target/mode, bounded input/output references, mutation policy, and allowed/forbidden scopes;
- dependency waves/edges, lifecycle join policy, gates, stop/loop ceilings;
- expected artifact, blocker, and receipt handle kinds;
- `requires_user_permission`;
- runtime-profile ID/version and sanitized capability/operation availability;
- a digest over the exact proposal bytes.

It is preview only: creating, editing, scoring, or selecting it must yield zero registration, spawn, execution-owner call, or owner Run mutation. `RouteDecision` stores immutable candidates, selection, rationale, version, and the proposal digest; it is choice evidence, not confirmation, Dispatch authority, or a run. Both reuse owned semantics while requiring new Resonant projections, hence **`BUILD-FROM-OWNED + NOVEL-ATTEMPT`**, not novelty-only. [Agent 1, `research.md:18-35,46-60,83-96`; closure C5]

The versioned runtime profile binds:

- supported public lifecycle and Orchestrate profile versions;
- dispatch type to live or reserved consumer owner;
- form/readiness, validation, tension, exact confirmation, registration, and drift behavior;
- required/optional native operations, wait targeting, join policy, timeout, cancellation/recovery support, and owner concurrency ceiling;
- opaque owner-handle schemas;
- sanitized result/observation hooks and publication boundary.

It must fail closed when required operations are absent and revalidate immediately before launch. Parallelism is a host property, not something the proposal can manufacture. [Agent 1, `research.md:46-71`; Agent 4, `research.md:352-411`; closure C1, C4]

Private/server-only bindings include DomainSpec schema `0.8.0`, `evidence_binding`, Inventory IDs, agent pool and identities, eligibility, two-checker evidence, registrar commands, ledger rows/events, private paths, constitution prose, secrets, publication targets, and research-stage repair roles. Client/public payloads receive only sanitized status, digests, named public owner/capability, and opaque handles. [Agent 1, `research.md:36-45,97-107`; closure C1]

## Owner, identity, and event mappings

| Identity/record | Meaning | Authority rule |
|---|---|---|
| `roleId` | Stable approved strategy role | A change requires revised bytes, validation, and approval. |
| `capabilityRef` | Bounded capability owner | Cannot be silently substituted. |
| `actionId` | Persisted Orchestrate action | Exactly-once native-call key; never synthesized by UI. |
| `agentId` | Native spawned child | Host identity; may change on resume. |
| `executionOwnerRef` | Opaque execution-truth owner handle | Returned by delegation/provider/compute owner, never manufactured by a projection. |
| `childId` | Stable UI/ancestry identity | Stable across attempts. |
| `runId` | One attempt correlation | New on resume; old attempt remains immutable. |
| `DelegationPacket` | Mission, grants, scope, verification, return protocol | Existing delegation owner. |
| `TaskWorkspace` | Preparation/evidence filesystem envelope | Never execution proof. |
| `ComputeJob` | Optional compute-backed execution truth | Used only when selected owner executes through compute. |
| `GoalWorkspace` | Supervision and references | Never equivalent to a child Run. |
| artifact/blocker handle | Owner-backed result or residue | Projection may reference, not redefine. |

The event chain is:

1. Augmentor produces preview-only `StrategyProposal`; no side effect.
2. Augmentor records `RouteDecision`; no approval.
3. One explicit consumer gate binds the exact proposal/Dispatch digest; any role, scope, selector, wave, policy, or fallback change invalidates it.
4. Dispatch Spec validates the frozen route; the consumer registrar records it before spawn.
5. Orchestrate preflights native operations and persists actions with zero spawns.
6. One owner call per persisted action returns `agentId` and `executionOwnerRef`; only then may Augmentor create a correlated `HostRunProjection`.
7. Owners persist truth; `RunTransitionProjection` and `RunOutcomeProjection` append observations with owner evidence handles.
8. `LifecycleJoin` reconciles expected actions, gates dependents, and closes lifecycle state.
9. Result delivery and consumption remain independently unread/consumable after lifecycle close.
10. Observation follows closeout and cannot approve, execute, or promote.

`RunOutcomeProjection` minimally carries `runId`, `childId`, `ownerRef`, `ownerEvidenceHandle`, observed state/time, `reconciliationStatus`, `artifactRefs[]`, and `blockerRefs[]`. Reconciliation distinguishes `unreconciled`, `confirmed`, `contradictory`, and `owner-unreachable`; hydration never fabricates owner state. [Agent 1, `research.md:46-60,83-96`; Agent 2, `research.md:157-229`; closure C6]

`LifecycleJoin` is not result delivery, notification, read state, consumption, attachment, or memory intake. Opening or attaching B cannot settle a gate, mutate A, mark a sibling read, merge transcripts, or ingest memory. [Agents 1–2, `research.md:15-16,63-96,220-229`; closure C6]

## Human journeys

The proposed UI is a conversational transition card plus compact run tray, not an infrastructure dashboard:

1. **Preview/edit/decline:** show “Proposed: 2 background runs; nothing has started,” roles, purposes, expected results, bounded context, and forbidden effects. `Not now` causes no registration or run. Editing changes the digest.
2. **Approve once:** `Approve and start 2` binds the exact frozen bytes. Ordinary chat never implies approval.
3. **Continue and switch:** after owner launch, keep the parent composer usable; switching threads neither reparents work nor changes snapshots or focus.
4. **Target one child:** an attention row names the child, question, reason, and scope effect. The answer produces one addressed input revision only.
5. **Inspect residue and value:** show truthful `Blocked`, `Done`, `Failed`, and reconciliation states. `Open result`, `Attach to this conversation`, and `Keep separate` act only on the selected handle.
6. **Cancel/resume control:** cancellation first projects `Cancel requested`; only owner acknowledgement allows `Cancelled`. Resume is a new attempt linked by `resumesRunId`.

All controls are real buttons/fields with visible focus and programmatic state; dialogs restore initiating focus, async events never steal it, routine announcements are coalesced and polite, reload does not replay announcements, reduced motion retains textual state, and color is never the sole signal. These are acceptance requirements, not current UI proof. [Agent 3, `research.md:296-350`; closure C3]

## Honest degraded modes

| Condition | Required behavior |
|---|---|
| Capability absent | Preview/export; separately authorized install/hardening offer; otherwise block. |
| Required spawn/wait/interrupt/inventory absent | Hard block naming the missing owner operation; zero spawn attempts. |
| User declines | Retain/discard proposal by choice; no registration or child projection. |
| Validation fails | Preserve defects; repair exact bytes, revalidate, and reapprove. |
| Parallelism unavailable before approval | Offer serial only as a revised proposal when semantics remain valid. |
| Owner capacity unavailable after approval | No Augmentor queue or silent serialization; preserve residue/block unless an owner-side queue policy was approved. |
| One helper truly suffices | Use the distinct bounded-helper lifecycle only when multi-lane semantics are no longer required. |
| Child A blocks/fails | Preserve B’s independent success; keep the dependent wave blocked under `join_policy=all` and `on_incomplete=block`. |
| Timeout | Interrupt once, record explicit timeout and residue; never infer success from silence. |
| Reload/reconnect | Hydrate projections, reconcile owner IDs, and show unknown when owner truth is unreachable. |
| General capability lacks proof | Fixture/experimental lane only; no readiness or promotion claim. |

[Agent 4, `research.md:352-450`; closure C4, C7]

## Ordered implementation slices

1. Refresh the consumer checkout from its seven-commit-behind state and rerun repository baselines.
2. Add neutral proposal, immutable decision/approval, context snapshot, run correlation, transition/outcome, and hydration contracts only.
3. Add profile/capability/operation discovery and launch-time revalidation.
4. Add preview/edit/decline UI and prove zero owner mutations.
5. Add exact digest-bound approval and a Resonant-owned registrar binding without copying DomainSpec.
6. Bind one persisted Orchestrate action to current `DelegationPacket` and `TaskWorkspace`; say “prepared, execution not started.”
7. Add one real action-to-owner adapter returning `executionOwnerRef` and optional `ComputeJob` handle.
8. Replace global cardinality with a non-authoritative foreground/child admission index; owners retain queue, capacity, execution, cancellation, and terminal truth.
9. Add two independent owner bindings with an initial owner-approved ceiling of two.
10. Add addressed clarification, owner-backed blocker projection, reconciliation, and resume-as-new-attempt.
11. Add cancellation acknowledgement/quarantine as a separate control path.
12. Add notification delivery/read controls and artifact consumption separated from lifecycle and memory.
13. Run deterministic tests and the browser witness below.

Slices 1–6 are infrastructure only. No product witness exists before real owner execution and the complete acceptance path. [Agent 2, `research.md:230-288`; closure C2, C8]

## Exact deterministic tests

- Preview, edit, and decline cause zero registration, spawn, owner call, or owner-Run mutation.
- Any digest-changing edit invalidates approval and prevents registration.
- Registration precedes every owner call.
- Replayed, unknown, or mismatched `actionId` causes zero additional owner calls.
- Projection writes cannot change owner truth.
- Resume keeps `childId`/`roleId`/`capabilityRef`, creates a new `runId`, and permits a new `agentId`.
- Parent, A, B, and other-thread planted markers remain confined to their exact snapshots and addressed owner payloads.
- One clarification creates exactly one A-addressed input revision and leaves B unchanged.
- Owner-backed A `Blocked` includes a nonempty opaque `blockerRef`; B `succeeded` includes its artifact handle.
- With A blocked and B succeeded, the dependent gate remains blocked under `join_policy=all`/`on_incomplete=block`.
- Reload reconciles both outcomes from owner references without fabricating state or duplicating announcements.
- B-only open/attach changes neither A, sibling notification/read state, lifecycle state, nor memory intake.
- Cancellation control separately proves `Cancel requested` until acknowledgement, terminal immutability, and late-result quarantine.
- Lifecycle close cannot report success while an expected action is pending, unknown, or unclosed.
- Missing required operations hard-block with zero spawns.
- Public/browser payload scanning finds no private DomainSpec schema, identities, ledger, paths, or evidence.

[Agents 1–3, `research.md:72-96,196-255,327-350`; closure C6, C7]

## Exact two-child browser witness

Use deterministic local-fixture children A (Strategy) and B (Whisper); this is not provider or production proof.

1. Enter an ordinary-language request and assert a preview of exactly A+B with zero registration/spawn/owner-call events.
2. Edit only A’s selector and assert B’s preview snapshot digest is unchanged.
3. Approve once and assert exactly two real owner calls with distinct `actionId`, `agentId`, `runId`, snapshot digest, and `executionOwnerRef`.
4. Send parent chat while both owners execute; assert the message succeeds and neither snapshot changes.
5. Switch thread; assert no reparenting, marker leak, announcement replay, or focus theft.
6. Fixture A requests clarification; answer A by keyboard and assert exactly one A-addressed input event and no B input change.
7. Make owner A return terminal **`Blocked` with a nonempty opaque `blockerRef`**. Make owner B return **`succeeded` with an artifact handle**. Do not use cancellation to create this partial outcome.
8. Assert Orchestrate reconciliation preserves both owner-backed outcomes and the dependent gate remains **blocked** because the wave requires all children and blocks on incomplete.
9. Reload before consuming B; hydrate projections, reconcile A and B through their owner references, preserve A’s `blockerRef`, B’s artifact handle, and the dependent-gate block, and emit no duplicate announcement.
10. Consume/attach **B only**; assert the parent receives only B’s artifact handle and that A’s blocker/transcript/state, sibling notification/read state, lifecycle/gate state, and memory intake are unchanged.
11. Verify parent/A/B/other-thread marker containment across snapshots, owner requests/outputs, bounded notifications, and explicit attachment.

Cancellation is a **separate control test**: request cancellation on a fresh fixture attempt, remain `Cancel requested` until owner acknowledgement, project `Cancelled` only after acknowledgement, quarantine a late result, and resume only as a new attempt. It is not the partial-failure witness above. [Agent 3, `research.md:327-350`; Agent 4, `research.md:374-411`; reviewer evidence spawn-0007; closure C7]

## Measurable overhead budgets

The initial acceptance budgets are:

- route cards on at most 20% of ordinary turns;
- clarification on at most 5% of routed attempts;
- no more than two extra user actions for consequential launch;
- at most one announcement per meaningful terminal/attention transition;
- initial owner-approved child concurrency ceiling of two;
- retention projection of 20 recent terminal attempts.

Instrument numerator, denominator, and observation window for the percentage budgets; record approval-to-owner-call latency, reconciliation latency, duplicate-announcement count, and bytes per retained projection. These thresholds are owner-pending and unmeasured, so they are test targets rather than current performance evidence. [Agent 3, `research.md:317-326`; closure C3, C8]

## Risks and hard rejects

- A client admission index becomes a queue, scheduler, capacity authority, execution registry, or source of terminal truth.
- Preview, confidence, or route selection becomes approval; approval silently survives changed bytes.
- `TaskWorkspace` is presented as execution, or `GoalWorkspace` as a Run.
- A `RunOutcomeProjection` lacks opaque owner/evidence references or hydration fabricates `running`, success, failure, or cancellation.
- Lifecycle join collapses into notification, read state, result consumption, attachment, or memory intake.
- Serial, one-helper, inline, or nested-CLI behavior silently replaces an approved route.
- DomainSpec-private schemas, identities, paths, ledgers, evidence, or prose enter public/browser bytes.
- A fixture/card/receipt is promoted as execution evidence; the seven-commit-behind checkout is treated as implementation freshness; narrow single-run tests are inflated into multi-agent proof.

[Agents 1–4, `research.md:62-107,245-288,341-350,415-450`; closure C5, C8]

## Next owner route

Route next to a bounded consumer implementation plan, not promotion:

1. **Consumer maintainer** refreshes the Resonant checkout and establishes baseline receipts.
2. **Resonant capability owner** defines discovery, grants, native-operation mapping, and launch revalidation.
3. **Consumer approval and registrar owners** define digest, eligibility, invalidation, and private-neutral registration.
4. **Orchestrate host-profile and execution-adapter owners** bind actions to existing delegation/provider/optional-compute owners.
5. **Projection persistence, context/input, notification, result, and memory owners** implement the non-authoritative records and separation invariants.
6. **UX/accessibility owner** implements the conversational card/tray and runs the deterministic witness.
7. **Arcanum promotion owner** receives evidence only after medium/complex consuming-profile proof; this findings document supplies none.

The work should remain fixture/experimental until the exact witness passes against owner-backed execution and is audited at the claim ceiling above. [Agents 1–4, `research.md:97-107,230-288,296-350,430-450`; closure C8]

## Connections

- derives-from: `./research.md`

## Open Questions

- **OQ-1 (BLOCKER)** — Which Resonant owner defines the runtime profile, grant mapping, required native operations, and launch-time revalidation? Recommendation: name the capability owner before implementation slice 3 and version the profile independently of private bindings. Owner: Resonant capability owner.
- **OQ-2 (BLOCKER)** — Who owns the digest-bound approval and registrar record without importing DomainSpec’s private schema or ledger? Recommendation: specify actor eligibility, invalidation, protected downstream gates, and an opaque registration handle before slice 5. Owner: Consumer approval owner and Consumer registrar owner.
- **OQ-3 (BLOCKER)** — Which existing execution operation will return `executionOwnerRef` for a general child, and when is `ComputeJob` applicable? Recommendation: implement one owner binding first and prohibit projection-created execution state. Owner: Execution-adapter owner.
- **OQ-4** — What are the exact reconciliation polling/subscription, TTL, contradictory-state, and owner-unreachable semantics? Recommendation: define them before hydration can display any nonterminal state. Owner: Projection persistence owner.
- **OQ-5** — What owner acknowledgement constitutes cancellation, and how long is quarantined late evidence retained? Recommendation: keep cancellation outside the blocker/success witness and test it as a separate terminal-immutability control. Owner: Cancellation and recovery owner.
- **OQ-6** — Which APIs keep result delivery, read state, attachment, checkpointing, and memory intake distinct? Recommendation: require separate commands and audit events, with B-only consumption as the collapse test. Owner: Result owner and Memory owner.
- **OQ-7** — Are the attention, concurrency, retention, and latency budgets acceptable once measured? Recommendation: instrument the stated budgets in the fixture lane and revise them only through named owner review. Owner: UX/accessibility owner and Resonant runtime owner.
- **OQ-8** — What evidence is sufficient to harden the public lifecycle seed? Recommendation: require audited medium/complex consuming-profile runs and canonical-versus-generated verification before any promotion proposal. Owner: Public Arcanum promotion owner.
