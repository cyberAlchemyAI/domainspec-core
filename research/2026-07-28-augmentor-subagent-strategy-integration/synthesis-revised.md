## Revised candidate architecture synthesis — zig-zag 1/2

Timestamp: `2026-07-29T00:22:53-03:00`  
Mode: read-only; no files edited.  
Result: `PASS_AS_CANDIDATE_ARCHITECTURE`; `NO_WITNESS_CURRENT`; implementation, product acceptance, performance, promotion, and production readiness remain unproved.

### Evidence labels

These labels describe repository evidence, not production deployment:

- `ALREADY-DEPLOYED`: present in the inspected current repository/runtime bytes.
- `BUILD-FROM-OWNED`: proposed composition that reuses named current owners without taking their authority.
- `NOVEL-ATTEMPT`: absent from current ResonantOS and requiring an explicit owner, implementation, and evidence.
- `CURRENT-SEED`: present public lifecycle seed, but not medium/complex consumer proof or promotion evidence.

## Reconciled verdict

The viable architecture remains:

```text
ordinary request
  -> StrategyProposal projection
  -> RouteDecision projection
  -> digest-bound consumer approval
  -> validated and registered Dispatch
  -> Orchestrate preflight/action plan
  -> existing execution-owner calls
  -> non-authoritative Run projections
  -> LifecycleJoin / orchestrateJoin
  -> independent result delivery and consumption
```

`StrategyProposal` and `RouteDecision` are `NOVEL-ATTEMPT` Augmentor projections. They do not add a lifecycle authority. The public Subagent Strategy lifecycle is the `CURRENT-SEED` owner of trigger, readiness, exact confirmation/freeze, registration ordering, dependency-aware execution, final approval, closeout, and observation semantics. Dispatch Spec and Orchestrate remain the current executable route and lifecycle owners. The consumer projection is undeployed. Agent 1 establishes this separation (`research.md`, Agent 1, lines 7–17; `.agents/skills/subagent-strategy/SKILL.md:20-26,50-107`; `.agents/skills/subagent-strategy/README.md:1-11`; `arcanum/formulae/dispatch-spec/SKILL.md:65-174`; `.agents/skills/orchestrate/SKILL.md:65-143`).

Agent 2 identifies existing ResonantOS owners but confirms the binding is missing (`research.md`, Agent 2, lines 122–229; consumer `src/core/contracts.ts:955-1069,1958-2105`, `src/core/delegation.ts:33-96,582-604`, `src/core/compute-fabric.ts:194-239`). Agent 3 supplies a proposed human journey and literal acceptance witness, while confirming the global guard prevents it today (`research.md`, Agent 3, lines 296–350; consumer `src/modules/chat/run-guard.ts:8-18`). Agent 4 validates only route shape and requires honest capability gaps rather than simulated execution (`research.md`, Agent 4, lines 352–450; `DISPATCH-ROUTE.json:308-378`).

Therefore:

- `GO`: bounded implementation and fixture design.
- `NO_GO`: claims of current two-child execution, accepted user value, readiness, release, or promotion.

## Deployment and ownership catalog

| Surface | Label | Owner and authority |
|---|---|---|
| Public Subagent Strategy lifecycle | `ALREADY-DEPLOYED / CURRENT-SEED` | Public lifecycle ordering and invariants; no consumer execution proof. |
| Runtime-profile template | `ALREADY-DEPLOYED / CURRENT-SEED` | Defines variable owner bindings; no ResonantOS profile exists. |
| Dispatch Spec | `ALREADY-DEPLOYED` | Validates authorization, role/capability bindings, waves, scopes, receipts, and terminal lifecycle; does not execute. |
| Orchestrate and Codex host profile | `ALREADY-DEPLOYED` | Preflight, persisted actions, native spawn/wait/interrupt/inventory, lifecycle reconciliation, gates, closeout. |
| DomainSpec registrar/ledger/profile | `ALREADY-DEPLOYED`, private precedent only | Private consumer authority; not reusable as public/browser schema. |
| Resonant capability grants/tokens | `ALREADY-DEPLOYED` | Current host-reviewed admission surfaces; no Subagent Strategy operation profile. |
| `DelegationPacket` | `ALREADY-DEPLOYED` | Bounded mission, grants, scope, verification, artifacts, return protocol. |
| `TaskWorkspace` | `ALREADY-DEPLOYED` | Filesystem preparation/evidence envelope; never execution truth. |
| `ComputeJob` | `ALREADY-DEPLOYED` | Optional execution truth for compute-backed actions, including timeout/cost/artifact policy. |
| `GoalWorkspace` | `ALREADY-DEPLOYED` | Supervision and references; not a child Run. |
| Current artifacts/workspace results | `ALREADY-DEPLOYED` | Authoritative result objects referenced by projections. |
| Provider mediation | `ALREADY-DEPLOYED` | Host policy; Strategy cannot select around it. |
| Global chat run guard | `ALREADY-DEPLOYED` | Current single-run exclusion; a blocker, not a reusable child scheduler. |
| `StrategyProposal` | `NOVEL-ATTEMPT` | Augmentor preview projection only; zero lifecycle or execution authority. |
| `RouteDecision` | `NOVEL-ATTEMPT` | Immutable Augmentor choice/rationale projection; confidence is not approval. |
| `ContextSnapshot` projection | `NOVEL-ATTEMPT` | Addressed immutable context digest; source content remains with current thread/file owners. |
| Digest-bound `StrategyApproval` | `NOVEL-ATTEMPT` | Consumer gate binding exact proposed/dispatch bytes; owner/eligibility open. |
| Resonant registrar/ledger binding | `NOVEL-ATTEMPT` | Must be defined by the consumer; DomainSpec implementation may not be copied. |
| Runtime-profile discovery/admission | `BUILD-FROM-OWNED + NOVEL-ATTEMPT` | Reuses capability grants and profile template; exact Resonant binding absent. |
| Action-to-owner adapter | `BUILD-FROM-OWNED + NOVEL-ATTEMPT` | Maps Orchestrate actions to current delegation/provider/compute owners; no new scheduler. |
| Non-authoritative child admission/index projection | `NOVEL-ATTEMPT` | Correlation/cardinality/read model only; cannot queue, dispatch, execute, cancel, or declare terminal truth. |
| `HostRunProjection` | `NOVEL-ATTEMPT` | References owner records and observed state; no copied execution policy. |
| `RunTransitionProjection` | `NOVEL-ATTEMPT` | Observed append-only projection with owner evidence reference. |
| Addressed `RunInputRevision` | `NOVEL-ATTEMPT` | One-child clarification projection; owner protocol absent. |
| `RunOutcomeProjection` | `NOVEL-ATTEMPT` | Opaque projection of owner truth, never terminal authority. |
| Cancellation acknowledgement/quarantine | `NOVEL-ATTEMPT` | Owner semantics and late-result policy remain open. |
| `NotificationProjection` | `NOVEL-ATTEMPT` | Delivery/read/mute/snooze projection; owner absent and non-authoritative. |
| Result delivery/consumption controls | `BUILD-FROM-OWNED + NOVEL-ATTEMPT` | Reuse artifact handles; delivery and consumption semantics absent. |
| Proposal card and child tray | `NOVEL-ATTEMPT` | Proposed Augmentor UX. |
| Actual two-child binding | `BUILD-FROM-OWNED + NOVEL-ATTEMPT` | Requires real Orchestrate-to-owner execution for two independent actions. |
| Deterministic two-child browser fixture | `NOVEL-ATTEMPT` | Acceptance harness, not provider/production proof. |

Sources: Agent 1’s current/proposed boundary and runtime-profile analysis (`research.md`, lines 11–71); Agent 2’s current-versus-missing matrix and adapter boundaries (`research.md`, lines 140–206); Agent 3’s current UI and proposed experience (`research.md`, lines 297–350); Agent 4’s build-from-owned inventory (`research.md`, lines 398–441).

## Public-neutral projection contract

### `StrategyProposal` — `NOVEL-ATTEMPT`

Portable fields:

- proposal ID and request/thread reference;
- request, goal, and evidence-selector digests;
- trigger reasons and named capability;
- roles with `roleId`, purpose, `capabilityRef`, target/mode, bounded input/output references, mutation policy, and allowed/forbidden scopes;
- dependency waves/edges, lifecycle join policy, gates, and stop/loop ceilings;
- expected artifact, blocker, and receipt handles;
- `requires_user_permission`;
- runtime-profile ID/version and sanitized capability/operation availability;
- digest over exact proposal bytes.

It is a side-effect-free Augmentor projection. Proposal creation, editing, confidence, or selection cannot register, spawn, create an owner Run, or approve a route. Agent 1 provides the minimal neutral fields and no-side-effect requirement (`research.md`, lines 18–35, 46–50; `.agents/skills/subagent-strategy/SKILL.md:91-101`; runtime profile `:21-40`).

### `RouteDecision` — `NOVEL-ATTEMPT`

Stores immutable candidates, selection, rationale, version, and proposal digest. It is evidence of the user-facing route choice, not Dispatch authority, owner approval, or execution state. The accepted Interaction/RouteDecision/Run model is proposed evidence only (`research.md`, Agent 1, lines 15–16; routing/session findings `:35-55,119-132`).

### Runtime-profile admission — `BUILD-FROM-OWNED + NOVEL-ATTEMPT`

The consumer profile must bind:

- supported public lifecycle version;
- dispatch type to live/reserved owner;
- form/readiness, validation, tension, confirmation, registration, and drift behavior;
- required and optional host operations;
- Orchestrate profile/version;
- wait targeting, lifecycle join policy, recovery/cancellation support, and owner concurrency ceiling;
- opaque owner-handle schemas;
- sanitized result/observation hooks and publication boundary.

The template exists, but Resonant discovery and binding do not (`research.md`, Agent 1, lines 60–71; `.agents/skills/subagent-strategy/templates/runtime-profile.md:7-102`; Agent 2 lines 140–165).

### Private/server-only bindings

The browser/public contract excludes DomainSpec schema `0.8.0`, `evidence_binding`, Inventory IDs, agent pool/identities, eligibility, two-checker evidence, registrar commands, ledger rows/event enums, private paths, constitution prose, secrets, publication destinations, and research-specific repair roles. Those remain private consumer bindings. The client receives sanitized status, digest, named owner/capability, and opaque handles only (`research.md`, Agent 1, lines 36–45; private adapter `implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md:46-122,217-268`).

## Authority and event chain

| Stage | Deployment label | Authority and behavior |
|---|---|---|
| Preview | `NOVEL-ATTEMPT` | Augmentor emits `StrategyProposal`; zero registration, spawn, or owner-Run mutation. |
| Route selection | `NOVEL-ATTEMPT` | Augmentor records `RouteDecision`; no approval authority. |
| Exact approval | `NOVEL-ATTEMPT` | Consumer owner gate binds exact proposal/Dispatch digest. Any role, scope, selector, wave, or fallback change invalidates it. |
| Dispatch validation | `ALREADY-DEPLOYED` | Dispatch Spec validates route shape and authorization; it does not execute. |
| Registration/ledger binding | private precedent current; Resonant binding `NOVEL-ATTEMPT` | Consumer registrar records the approved exact route before spawn. |
| Orchestrate preflight | `ALREADY-DEPLOYED` owner; host binding `NOVEL-ATTEMPT` | Validate approval and required host operations; persist action plan with zero spawns. |
| Owner invocation | `BUILD-FROM-OWNED + NOVEL-ATTEMPT` | Exactly one owner call per persisted action; use delegation/provider/optional compute owners. No Augmentor queue. |
| Run projection | `NOVEL-ATTEMPT` | Create correlation/read projection only after owner binding is returned. |
| Lifecycle reconciliation | `ALREADY-DEPLOYED` Orchestrate semantics; Resonant binding `NOVEL-ATTEMPT` | `LifecycleJoin`/`orchestrateJoin` waits, inventories, interrupts, gates, and closes. |
| Owner outcome | owner current; projection `NOVEL-ATTEMPT` | Execution owner persists truth/evidence; Augmentor stores opaque references only. |
| Result delivery/consumption | `BUILD-FROM-OWNED + NOVEL-ATTEMPT` | May remain unread after lifecycle close. Consumption cannot modify lifecycle state. |
| Observation | current lifecycle slot; consumer hook `NOVEL-ATTEMPT` | Telemetry after owner closeout; no approval, execution, or promotion authority. |

Sources: Agent 1 host-call sequence (`research.md`, lines 46–60; `.agents/skills/orchestrate/SKILL.md:79-143`; Codex host profile `:21-67`), Agent 2 adapter seams (`research.md`, lines 157–180), and Agent 4’s validation/degraded constraints (`research.md`, lines 382–411).

## Identity mapping and invariants

| Identity | Meaning | Authority |
|---|---|---|
| `roleId` | Stable role in the approved strategy | Proposal/Dispatch identity; changing it requires reapproval. |
| `capabilityRef` | Bounded capability owner required by the role | Dispatch/profile binding; changing it requires revalidation and reapproval. |
| `actionId` | Persisted Orchestrate action | Orchestrate authority; exactly-once native call key. |
| `agentId` | Native spawned child identity | Host-native execution identity; may change on a resumed attempt. |
| `executionOwnerRef` | Opaque reference to the owner carrying execution truth | Delegation/provider/ComputeJob or other approved owner. |
| `runId` | Correlation identity for one attempt | Augmentor projection; changes on resume. |
| `childId` | Stable UI and ancestry identity across attempts | Projection identity; remains stable across resume. |

Resume creates a new `runId` and may receive a new `agentId`; it never changes `childId`, `roleId`, or `capabilityRef`. Changing the role or capability creates a revised proposal requiring validation and approval. `actionId` and `executionOwnerRef` must never be synthesized from UI state. This refines Agent 2’s per-child mapping (`research.md`, lines 181–194, 220–229) under Agent 1’s owner-reference collapse test (`research.md`, lines 83–96).

## Non-authoritative admission/index projection

The current global run guard must not be replaced by an Augmentor execution registry or queue.

The proposed `ChildAdmissionIndex` is `NOVEL-ATTEMPT` and may contain only:

- active foreground interaction references;
- known child `childId`/`runId` correlations;
- observed nonterminal/attention state;
- owner concurrency availability returned by admission;
- projection hydration/reconciliation status.

It may prevent duplicate UI submissions and enforce presentation/cardinality rules, but it cannot:

- queue or schedule children;
- determine execution order;
- manufacture `running`, `cancelled`, or terminal state;
- replace Orchestrate persisted actions;
- replace `ComputeJob` or another execution owner;
- infer capacity from stale local state.

Queue, capacity, execution, cancellation, and terminal truth remain with Orchestrate and the selected execution owner. Agent 2 explicitly rejects a strategy queue (`research.md`, lines 148, 245–255); Agent 4 likewise prohibits another scheduler or registry (`research.md`, lines 415–426).

## Lifecycle join versus result consumption

`LifecycleJoin` or `orchestrateJoin` is reserved for agent reconciliation, dependency gates, final approval, and closeout. It answers whether expected actions reached a mechanically reconciled terminal/closed state and whether dependents may proceed.

The product Run projection instead carries:

- `resultDeliveryPolicy`: for example `notify`, `silent`, or attention routing;
- `resultConsumptionPolicy`: for example `manual-consume` or an explicitly approved automatic attachment policy.

Lifecycle join may finish while every result remains unread. Reading, opening, attaching, dismissing, muting, or consuming a result cannot:

- reopen or close an action;
- change lifecycle success/failure/cancellation;
- satisfy an Orchestrate gate;
- consume a sibling result;
- merge child transcripts;
- perform memory intake.

This corrects the earlier overloaded “join-before-continue” product wording while preserving Agent 2’s core separation between Orchestrate join and product consumption (`research.md`, lines 220–229) and Agent 1’s notification/consumption non-authority rules (`research.md`, lines 15–16, 63–70, 83–96).

## Projection persistence and owner truth

All following records are `NOVEL-ATTEMPT` Augmentor projections:

- `StrategyProposal`;
- `RouteDecision`;
- `StrategyApproval`;
- `HostRunProjection`;
- `RunTransitionProjection`;
- `RunInputRevision`;
- `RunOutcomeProjection`;
- `NotificationProjection`.

`RunOutcomeProjection` must contain:

```text
runId
childId
ownerRef
ownerEvidenceHandle
observedState
observedAt
reconciliationStatus
artifactRefs[]
blockerRefs[]
```

`reconciliationStatus` distinguishes at least `unreconciled`, `confirmed`, `contradictory`, and `owner-unreachable`. The execution owner persists terminal truth and evidence. Augmentor stores only opaque references and observations; hydration cannot fabricate `running`, success, cancellation, or failure.

Other semantics:

- child snapshots are content-addressed and immutable;
- parent, sibling, and switched-thread messages cannot mutate them;
- targeted clarification creates exactly one addressed `RunInputRevision`;
- cancellation begins as a projected request; only owner acknowledgement permits projected `cancelled`;
- unknown acknowledgement remains attention-required;
- late results after acknowledged cancellation are quarantined as owner evidence and cannot reopen the attempt;
- resume creates a new attempt linked by `resumesRunId`.

These are `NOVEL-ATTEMPT` semantics, not current consumer behavior (`research.md`, Agent 2, lines 196–229; Agent 4, lines 374–395; [A2A specification](https://a2a-protocol.org/dev/specification/); [MCP Tasks](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks)).

## Proposal and control UX — `NOVEL-ATTEMPT`

The proposed experience is a conversational transition card plus compact run tray, not an agent console.

The preview says: “Proposed: 2 background runs; nothing has started.” It shows role, purpose, expected result, context summary, forbidden effects, and `Review & approve`. Editing roles, selectors, scopes, lifecycle policy, delivery policy, or consumption policy changes the digest and invalidates prior approval.

The exact approval action is `Approve and start 2`. Ordinary chat cannot imply approval.

After owner launch, the parent composer remains usable. Rows show `Starting`, `Working`, `Needs your answer`, `Cancel requested`, `Cancelled`, `Could not confirm cancellation`, `Done`, `Blocked`, or `Failed`. Thread switching does not reparent work or mutate snapshots. Targeted answers name the receiving child. Result controls are `Open result`, `Attach to this conversation`, and `Keep separate`.

Keyboard/focus/live-region/reduced-motion requirements remain as Agent 3 specified (`research.md`, lines 306–326; `projects/ide-ergonomics/PRODUCT-VIEW.md:125-193,226-253`; routing/session findings `:130-189,231-249`). Current ResonantOS provides thread buttons and polite single-run UI atoms only (`StrategistChatRail.tsx:393-415,519-603,762-795,900-918`).

## Degraded-mode decision table

| Condition | Honest behavior |
|---|---|
| Capability absent | Preview/export; separately authorized install/hardening offer; otherwise block. |
| Required spawn/wait/interrupt/inventory absent | Hard block, state missing owner operation, record zero spawn attempts. |
| User declines | No registration or child projection; proposal may be retained or discarded. |
| Validation failure | Preserve exact defects; revised bytes require full validation and approval. |
| Parallelism unavailable before approval | Serial execution only as a revised proposal when semantics remain valid. |
| Owner capacity unavailable after approval | No Augmentor queue and no silent serialization; block/preserve residue unless owner-side queue semantics were already approved. |
| One helper truly suffices | Use the separate bounded-helper lifecycle only when multi-lane semantics are no longer required. |
| Partial child failure | Preserve successful sibling; block dependent wave under current `join_policy=all` and `on_incomplete=block`. |
| Timeout | Orchestrate interrupts once and records explicit timeout; silence is never success. |
| Reload/reconnect | Hydrate projections, then reconcile opaque IDs with the owner; show unknown if unprovable. |
| General capability lacks medium/complex proof | Fixture/experimental lane only; no readiness or promotion claim. |

Source: Agent 4’s explicit degraded table (`research.md`, lines 382–411; `.agents/skills/orchestrate/SKILL.md:85-105,121-140`; `DISPATCH-ROUTE.json:308-378`).

## `NO_WITNESS_CURRENT`

Current evidence does not show:

1. a persisted preview-only `StrategyProposal` or immutable `RouteDecision`;
2. digest-bound Resonant approval and registrar/ledger binding;
3. actual two-child launch through Orchestrate-to-owner bindings;
4. parent conversation continuing while two children execute;
5. one addressed clarification affecting only one child;
6. independently reconciled partial child outcome/cancellation;
7. reload reconciliation against execution-owner truth;
8. selective result consumption without sibling or memory effects.

The current global guard expressly blocks concurrent foreground/child use, and current Engineer/Hermes workspace responses state execution has not started (`research.md`, Agent 2, lines 122–155; `run-guard.ts:8-18`; `delegation.ts:582-604`). Agent 3 therefore rates the journey `BLOCKED_CURRENT / READY_AS_ACCEPTANCE_SPEC` (`research.md`, lines 341–350).

The reviewer-reported `29/29` narrow current tests are retained only as evidence for existing single-run exclusion/token release and workspace/delegation behavior. They do not establish any missing item above. The explorer independently characterizes `run-guard.test.ts` as proving only global exclusion and token release (`research.md`, line 350).

## Exact repair and test sequence

1. Refresh the seven-commit-behind consumer checkout and rerun baseline checks.
2. Add projection contracts and hydration normalization only; no owner mutation.
3. Add runtime-profile/capability/operation discovery with launch-time revalidation.
4. Add preview/edit/decline UI and prove zero registration/spawn/owner mutations.
5. Add exact digest-bound approval and consumer registrar binding.
6. Bind one persisted Orchestrate action to existing `DelegationPacket` and `TaskWorkspace`; show “prepared, execution not started.”
7. Add one real action-to-execution-owner adapter returning `executionOwnerRef` and optional `ComputeJob` reference.
8. Add the non-authoritative foreground/child admission index; leave queue, capacity, and truth with owners.
9. Add two independent owner bindings with ceiling `2`.
10. Add addressed clarification, owner-acknowledged cancellation, quarantine, reconciliation, and resume-as-new-attempt.
11. Add `NotificationProjection`, `resultDeliveryPolicy`, and `resultConsumptionPolicy`.
12. Run the deterministic fixture and browser witness.

Slices 1–6 remain infrastructure. No product witness exists before real owner execution in slices 7–12. This preserves Agent 2’s ordered implementation sequence (`research.md`, lines 230–244) with the reviewer-required authority correction.

Deterministic tests, in order:

- preview/edit/decline yields zero registration/spawn/owner-Run mutation;
- changed digest invalidates approval;
- registration precedes any owner call;
- replayed/unknown/mismatched `actionId` yields zero extra owner calls;
- projection writes cannot change owner truth;
- identities obey the mapping and resume rules above;
- snapshots and planted markers remain isolated;
- one clarification yields one addressed child input;
- acknowledged cancellation and late-result quarantine preserve terminal immutability;
- partial success preserves sibling evidence and blocks dependents;
- lifecycle close succeeds only with every expected action reconciled/closed;
- unread/read/mute/consume operations do not alter lifecycle state;
- one attached artifact does not consume sibling data or perform memory intake;
- missing required operation yields a hard block and zero spawns;
- public/browser payload contains no private DomainSpec schema, identities, ledger, paths, or evidence.

Browser witness:

1. Preview exactly Strategy A + Whisper B; zero spawns.
2. Edit A’s selector; B’s snapshot remains unchanged.
3. Approve once; exactly two owner calls produce distinct `actionId`, `agentId`, `runId`, snapshot digest, and `executionOwnerRef` bindings.
4. Send parent chat while both execute.
5. Switch thread without reparenting, marker leakage, or focus theft.
6. A requests input; keyboard-answer A only.
7. Request cancellation of A; project `Cancelled` only after owner acknowledgement.
8. B survives and completes; lifecycle reconciliation closes independently of unread result state.
9. Resume A with stable `childId`, new `runId`, and possibly new `agentId`.
10. Reload and reconcile owner references without duplicate announcements.
11. Consume B only; parent receives B artifact handle while A, sibling read state, and memory remain unchanged.
12. Verify parent/A/B/other-thread marker containment end to end.

Agent 3 supplies the underlying literal witness (`research.md`, lines 327–350; routing/session findings `:174-189,231-243`).

## Measurable overhead budgets

Still owner-pending and unmeasured:

- route cards in at most 20% of ordinary turns;
- clarification in at most 5%;
- no more than two extra actions for consequential launch;
- one announcement per meaningful terminal/attention transition;
- initial owner-approved concurrency ceiling `2`;
- 20 recent terminal projections retained.

These are acceptance budgets, not current performance evidence (`research.md`, Agent 3, lines 317–326; routing/session findings `:245-249`).

## Public/private and authority collapse rejects

Reject any implementation where:

- Augmentor owns a queue, scheduler, execution registry, or terminal truth;
- the admission/index projection substitutes for Orchestrate or `ComputeJob`;
- StrategyProposal or RouteDecision becomes lifecycle authority;
- preview/confidence becomes approval;
- approval silently survives changed bytes;
- `TaskWorkspace == execution`;
- `GoalWorkspace == Run`;
- `RunOutcomeProjection` lacks an opaque owner/evidence reference;
- lifecycle join is conflated with delivery/read/consumption;
- notification state becomes execution truth;
- result attachment becomes transcript merge or memory intake;
- serial/helper/CLI execution silently replaces the approved route;
- DomainSpec schema, identities, ledgers, paths, or evidence enter public/browser bytes.

Sources: Agent 1 collapse tests (`research.md`, lines 62–96), Agent 2 rejected collapses (`research.md`, lines 245–255), and Agent 4’s ownership boundary (`research.md`, lines 415–441).

## Open owner decisions

1. Public Arcanum owner: lifecycle/profile contract version and seed hardening criteria.
2. Resonant capability owner: exact profile discovery, grants, operation mapping, and launch revalidation.
3. Consumer approval owner: digest format, actor eligibility, invalidation, and protected downstream gates.
4. Consumer registrar/ledger owner: exact Resonant binding without importing DomainSpec private authority.
5. Orchestrate host-profile owner: native operations, wait targeting, concurrency, timeout, and reconciliation mapping.
6. Execution adapter owner: action-to-delegation/provider/optional-compute binding.
7. Projection persistence owner: retention, normalization, `ChildAdmissionIndex`, transitions, and reconciliation state.
8. Context/input owner: snapshot construction and addressed clarification protocol.
9. Cancellation/recovery owner: acknowledgement, unknown state, quarantine, TTL, and resume semantics.
10. Notification owner: delivery/read/mute/snooze/restoration contract.
11. Result/memory owners: delivery, consumption, attachment, checkpoint, and memory-intake separation.
12. UX/accessibility owner: attention budgets and browser acceptance.
13. Consumer maintainer: upstream refresh and repository checks before mutation.
14. Arcanum promotion owner: medium/complex live consuming-profile evidence.

## Reviewer dispositions

- Lakatos / duplication gate: `SATISFIED_BY_REVISION`. Every surface now carries an explicit deployment/use label. The execution path reuses Dispatch Spec, Orchestrate, DelegationPacket, TaskWorkspace, ComputeJob, GoalWorkspace, artifacts, and provider mediation. No Augmentor queue or authoritative registry is proposed.
- Gödel / non-vacuity gate: `SATISFIED_AS_ACCEPTANCE_SPEC; NO_WITNESS_CURRENT`. The exact missing user-value chain and ordered deterministic/browser repair sequence are explicit. The `29/29` narrow tests remain bounded current evidence only.
- Quine / definition/authority gate: `SATISFIED_BY_REVISION`. Proposal, decision, approval, Dispatch, action, native child, owner execution, attempt Run, lifecycle join, outcome projection, delivery, consumption, notification, and memory intake are distinct. Identity and resume invariants are explicit.

## Updated claim/evidence closure matrix

| Claim | Label | Evidence | Closure |
|---|---|---|---|
| Public Subagent Strategy owns lifecycle semantics | `ALREADY-DEPLOYED / CURRENT-SEED` | Agent 1 lines 11–16; Subagent Strategy `:20-26,50-107`; README `:1-11` | Current seed; no promotion proof |
| Dispatch Spec validates but does not execute | `ALREADY-DEPLOYED` | Agent 1 line 12; Dispatch Spec `:65-174` | Closed |
| Orchestrate owns native action reconciliation and lifecycle join | `ALREADY-DEPLOYED` | Agent 1 line 13 and lines 52–57; Orchestrate `:79-143` | Closed for current contract |
| Resonant execution/workspace/artifact/provider owners exist | `ALREADY-DEPLOYED` | Agent 2 lines 140–194; consumer selectors above | Closed for seam identification |
| StrategyProposal and RouteDecision are projections only | `NOVEL-ATTEMPT` | Agent 1 lines 8, 15, 50; routing/session findings `:35-55,119-132` | Closed definition; undeployed |
| Digest-bound Resonant approval and registrar | `NOVEL-ATTEMPT` | Agents 1 lines 51–53; 2 lines 145, 200–202 | Open owner |
| Runtime-profile discovery | `BUILD-FROM-OWNED + NOVEL-ATTEMPT` | Agent 1 line 60; runtime template `:7-102`; Agent 2 lines 140–165 | Open binding |
| Action-to-owner adapter | `BUILD-FROM-OWNED + NOVEL-ATTEMPT` | Agent 2 lines 157–180 | Open implementation |
| Admission/index is non-authoritative and not a queue | `NOVEL-ATTEMPT` | Agent 2 lines 148, 245–255; Agent 4 lines 415–426 | Closed constraint; open implementation |
| Identity mappings preserve owner boundaries | `NOVEL-ATTEMPT` projection over current owners | Agent 2 lines 181–229; Agent 1 lines 83–96 | Closed candidate invariant |
| Addressed input revision | `NOVEL-ATTEMPT` | Agents 2 lines 203–226; 3 lines 310–312, 327–350 | Open implementation/witness |
| Cancellation acknowledgement/quarantine | `NOVEL-ATTEMPT` | Agent 2 lines 220–226; Agent 4 lines 374–395; MCP Tasks | Open owner/witness |
| `RunOutcomeProjection` references owner truth | `NOVEL-ATTEMPT` | Agent 2 lines 196–229; A2A/MCP precedent | Closed definition; open implementation |
| NotificationProjection is non-authoritative | `NOVEL-ATTEMPT` | Agents 1 lines 15–16, 57–58; 2 lines 151–165; MCP Tasks | Owner absent |
| Lifecycle join is independent of consumption | `BUILD-FROM-OWNED + NOVEL-ATTEMPT` | Orchestrate `:121-143`; Agent 2 lines 220–229 | Closed definition; open consumer behavior |
| Two-child action/owner binding | `BUILD-FROM-OWNED + NOVEL-ATTEMPT` | Agents 2 lines 230–244; 3 lines 327–350 | `NO_WITNESS_CURRENT` |
| Current global guard blocks the witness | `ALREADY-DEPLOYED` | Agents 2, 3, 4; `run-guard.ts:8-18` | Closed blocker |
| Existing 29/29 tests prove only narrow current behavior | current-test evidence | reviewer gate; Agent 3 line 350; `run-guard.test.ts` | Closed narrowly; no witness |
| Degraded routes cannot silently change approved semantics | mixed current contract/proposed binding | Agent 4 lines 382–411; Orchestrate `:85-105,134-140` | Closed constraint |
| Private DomainSpec bytes stay server-side | current private precedent/public boundary | Agent 1 lines 36–45; private adapter `:46-122,217-268` | Closed boundary |
| Frozen route shape validates | `ALREADY-DEPLOYED` validator | Agent 4 lines 444–450; `DISPATCH-ROUTE.json` | `VALIDATION=pass` narrowly |
| Product execution/acceptance/readiness | none | Missing chain and unexecuted witness | `NO_WITNESS_CURRENT` |

Final disposition: the revised architecture survives all three reviewer gates as a bounded, additive candidate. It preserves current owners, makes every new surface explicitly undeployed, and supplies a falsifiable repair and browser-witness sequence. It does not establish current execution or user value.
