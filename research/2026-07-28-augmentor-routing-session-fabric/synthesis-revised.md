## Augmentor routing and multi-session fabric — revised synthesis

### Product thesis

Augmentor should be one conversational shell that classifies each user turn against a thread-local active interaction, preserves consequential routing as an immutable host decision, and correlates approved foreground or child execution without taking authority away from the existing command, registry, approval, compute, goal, delegation, workspace, dispatch, artifact, evaluation, or memory owners.

### Evidence and freshness

`research.md` contains exactly four explorer sections:

1. session-state explorer;
2. route-decision explorer;
3. human-interface explorer;
4. consumer-runtime explorer.

The ResonantOS analysis was rechecked against local `dev`, seven commits behind `origin/dev`. The seven upstream commits do not touch the load-bearing `src/core`, `src/modules/chat`, `src/App.tsx`, or `public/addons/augmentor-chat.json` sources, although `package.json` changed; implementation must therefore update before treating test-command behavior as current. This synthesis is proposed architecture based on read-only source evidence, not accepted architecture or product proof. [`research.md` four explorer returns; `git:dev..origin/dev`]

### Public/private-safe admission boundary

Necronomicon supplies routing precedent—interaction fields, classification order, confidence semantics, checkpoint discipline and gap handling—but ResonantOS must not import a Necronomicon session directory, duplicate its state store, or expose private session prose/schema at runtime. The admissible boundary is a versioned, public-neutral rule/label/fixture artifact compiled or reviewed at build/admission time. ResonantOS owns its runtime `Interaction` and `RouteDecision` projections and resolves every result against current commands, enabled manifests, registries, approval gates and provider/compute/delegation owners. [`necronomicon/README.md:97-128,314-357,393-433`; Consumer-runtime explorer §“Smallest host-owned integration seam”]

Inventory remains discovery only. It can identify candidates and gaps but cannot authorize a route, execution, artifact acceptance, evaluation result, checkpoint intake, or lifecycle promotion.

### Current versus missing

| Concern | Current source-backed state | Missing boundary |
|---|---|---|
| Shell focus | `activeChatThreadId` is a UI preference rather than thread-owned state. [`contracts.ts:2806-2822`] | Focused surface and notification projection. |
| Projects/threads | `ChatProject` groups; `ConversationThread` owns identity, agent, workspace/channel/project references, summary and messages. [`contracts.ts:2769-2786`] | Thread-local runtime interaction and explicit ancestry projections. |
| Interaction precedent | Necronomicon defines owner, status, pending prompt, expected response, continuation, handoff and side notes. [`necronomicon/README.md:97-128`] | Public-neutral ResonantOS projection; no second Necronomicon store. |
| Routing | Slash commands and narrow natural-browser parsing precede provider execution. [`controller.ts:238-275`] | General conversation/execution disposition, candidates, rationale and gap outcome. |
| Active execution | One mutable token globally excludes another chat run; live events are transient. [`run-guard.ts:5-28`; `App.tsx:1224-1269`; `controller.ts:194-206`] | Per-thread foreground exclusion plus bounded child-run correlation. |
| Compute | `ComputeJob` already owns job type, constraints, node selection, policies, approval, audit path and job status; validation rejects invalid or unapproved work. [`contracts.ts:212-239,1034-1056`; `compute-fabric.ts:194-255,303-327`] | Optional correlation reference from a Run envelope, not replacement. |
| Goals | `GoalWorkspace` owns goal phase, steps, blockers, artifacts and delegation references. [`contracts.ts:2019-2105`] | Optional correlation reference from a Run envelope. |
| Delegation/workspace | `DelegationPacket` owns mission, context, scope, grants, approval, verification and return protocol; `TaskWorkspace` owns paths. [`contracts.ts:1958-2002`; `delegation.ts:39-96`] | General correlation, cancellation observation, join and resume projections. |
| Honest execution status | Workspace creation explicitly says execution has not started. [`delegation.ts:582-592`] | Preserve this distinction in every route/run surface. |
| Dispatch | Dispatch Spec validates parallel roles, join policy, authorization, waves, scopes and receipts; Orchestrate owns spawn/join/gates. [`dispatch-spec/SKILL.md:65-145`] | Run references to dispatch/run/action receipts, never a second scheduler. |
| Persistence | Host or local storage persists normalized shell state. [`runtime.ts:1369-1381,1458-1477`] | Append-only route/run outcomes and restart reconciliation. |
| Artifacts/notifications | Goal, delegation and compute owners already define artifacts; notification is manifest intent only. [`contracts.ts:1058-1069,2097-2110`; `augmentor-chat.json:56`] | Referenced artifact/blocker and UI notification projections; no unified replacement registry. |
| Background/floating claims | Manifest prose advertises broader surfaces. | Concurrency is absent and floating chat currently throws. [`runtime.ts:1383-1385`; Consumer-runtime explorer] |

### Normative one-way chain

```text
UserMessage + thread-local active Interaction
  -> immutable RouteDecision
  -> current host revalidation + required owner approval
  -> immutable ContextSnapshot
  -> Run correlation/lifecycle envelope
  -> append-only RunTransition and RouteOutcome
  -> references to owner-produced Artifact and/or Blocker
  -> Notification projection
  -> explicit thread attachment by reference
  -> owner-gated classified checkpoint/memory intake
```

Authority flows only forward through this chain:

- A `RouteDecision` cannot grant permission, enable a capability, select a compute node, create a workspace, approve a dispatch or validate an artifact.
- A `ContextSnapshot` cannot become memory or update its source thread.
- A `Run` cannot mutate the state of `ComputeJob`, `GoalWorkspace`, `DelegationPacket`, `TaskWorkspace` or Dispatch Spec; it observes/references their identifiers and receipts.
- A `RunTransition`, `RouteOutcome` or `Notification` cannot manufacture an owner artifact, blocker resolution or evaluation verdict.
- Thread attachment does not imply acceptance, truth, checkpointing, memory intake or promotion.
- No later projection may write authority backward into an earlier record. Corrections append a new decision/outcome/attempt linked to the prior identifier.

This preserves the IDE restraint floor: candidate is not promotion, preview is not execution, side note is not route switch, handoff is not execution proof, and recommendation is not execution. [`UNIFIED-PRODUCT-VIEW.md:87-88`; `PRODUCT-VIEW.md:188-192,240-241`]

### Ownership and reference model

| Record/surface | Authority owner | What Augmentor may persist |
|---|---|---|
| Shell/project/thread | ResonantOS consumer state | Focus and stable references. |
| Active `Interaction` | ResonantOS host projection; active capability interprets its own reply | Public-neutral owner/mode/status/pending-response contract. |
| `RouteDecision` | ResonantOS host router | Immutable interpretation, candidates, disposition, selected offer, confirmation requirement and outcome reference. |
| Commands/manifests/registries/approvals | Existing ResonantOS owners | References and revalidation results only. |
| `ContextSnapshot` | ResonantOS host projection | Immutable selector list, through-message boundary, memory references, exclusions, redaction policy and digest. |
| `Run` | ResonantOS correlation/lifecycle envelope | Parent/root/interaction/decision/snapshot IDs plus owner-record references and observed lifecycle. |
| `ComputeJob` | Compute Fabric | `computeJobId`; no copied job policy or status authority. |
| `GoalWorkspace` | Goal owner | `goalWorkspaceId`; no competing goal phase or artifact list. |
| `DelegationPacket` | Delegation owner | `delegationPacketId`; no duplicated mission, approval or return authority. |
| `TaskWorkspace` | Delegation bridge/workspace owner | `taskWorkspaceId`; existence never means execution. |
| Dispatch Spec/Orchestrate | Dispatch validator and orchestrator | Dispatch/run/action/receipt references and observed join outcome. |
| Artifact/blocker | Producing owner, including Whisper, goal, compute or delegated capability | Stable owner handle, provenance and validation reference. |
| Evaluation | Experiment Harness or equivalent declared evidence owner | Evaluation-report reference and status only. |
| Notification/ancestry | ResonantOS UI projections | Run/thread/parent handles, bounded summary and consumption state. |
| Checkpoint/memory | Necronomicon or another declared intake owner | Explicit intake request/result reference; never automatic raw context ingestion. |
| Reusable composition | Spellcraft | Proposal/reference only until Spellcraft accepts lifecycle work. |
| Primitive contract change | Sigil Development | Proposal/reference only until its owner accepts work. |

Experiment Harness owns repeatable test mechanics and evidence reporting, while semantic ownership stays with the tested artifact. Spellcraft owns reusable composition but cannot redefine a sigil. [`experiment-harness/SKILL.md:45-165`; `spellcraft/SKILL.md:31-163`]

#### User-facing notification policy

Notifications are host-owned ResonantOS projections derived from append-only `RunTransition` and `RouteOutcome` records. They are not a new registry and cannot create, alter, resume, cancel, validate, attach, consume, checkpoint or promote any run, interaction, owner artifact, blocker or memory record.

Policy resolution is hierarchical: **run override → thread override → project override → shell default**. Each level may inherit or override delivery channels, mute state and snooze expiry. Muting suppresses toast, sound and nonessential live announcements; unmuting restores future delivery only. Snoozing suppresses those channels until its expiry without marking anything read or consumed.

Event classes:

- **Completion:** quiet unread item and badge; at most one polite announcement.
- **Blocker:** persistent unread needs-attention item with owner residue and next action.
- **Clarification:** persistent unread question in both the run tray and parent-thread projection. It remains discoverable and answerable without stealing focus even when toast, sound or live delivery is muted or snoozed.
- **Failure:** persistent unread item with last verified state and safe next action.

Progress events are coalesced into the existing run item and do not each create notifications. Only a destructive failure or imminent risk of data loss may bypass mute/snooze for an assertive announcement; ordinary failure, blocker, completion and clarification may not.

Each meaningful transition creates at most one notification. Read state, delivery state and result consumption are independent per notification: reading or consuming one result cannot mark a sibling notification read, attach its artifact, resolve its blocker or consume its result. Restoration may hydrate unread items and policy state, but must not replay toast, sound or live-region announcements already delivered before shutdown.

All controls remain keyboard-operable with visible labels and programmatic state. Opening or dismissing notifications restores prior focus; new events never move focus. Routine announcements use `aria-live="polite"`; assertive delivery is reserved for the destructive/imminent-loss exception. Mute, unmute, snooze, mark-read, open-run and consume-result actions must be available without pointer input. These controls and thresholds remain proposals pending owner acceptance. [Human-interface explorer §§5–7 and “Keyboard and accessibility contract”; current polite live regions at `StrategistChatRail.tsx:596-603,762-795`]

### Minimal projections

```ts
type Interaction = {
  interactionId: string;
  threadId: string;
  owningCapability: string;
  mode: string;
  status: "running" | "awaiting-user" | "handoff-ready"
        | "blocked" | "completed" | "abandoned";
  pendingPrompt?: string;
  expectedResponseShape?: string;
  continuationPolicy: "continue-default" | "confirm" | "route-fresh";
  handoffTarget?: string;
};

type RouteDecision = {
  decisionId: string;
  requestDigest: string;
  interactionId?: string;
  sourceMessageIds: string[];
  conversationDisposition: "continue" | "side_note" | "fresh_route" | "clarify";
  executionDisposition:
    | "inline_answer" | "existing_capability_run"
    | "delegated_background_run" | "capability_gap" | "none";
  candidates: Array<{
    capabilityRef: string;
    mode: string;
    owner: string;
    evidenceSelectors: string[];
    installed: boolean;
    confidence: "high" | "medium" | "low";
    rejectedReason?: string;
  }>;
  selected?: { capabilityRef: string; mode: string; owner: string };
  confirmation: { required: boolean; reason?: string; ownerGate?: string };
  gap?: { kind: string; escalation?: string };
};

type Run = {
  runId: string;
  parentRunId?: string;
  resumesRunId?: string;
  rootThreadId: string;
  launchInteractionId: string;
  routeDecisionId: string;
  contextSnapshotId: string;
  kind: "foreground" | "child";
  ownerRefs: {
    computeJobId?: string;
    goalWorkspaceId?: string;
    delegationPacketId?: string;
    taskWorkspaceId?: string;
    dispatchId?: string;
    orchestrateRunId?: string;
  };
  joinPolicy: "notify" | "manual-consume" | "join-before-continue";
};
```

`ContextSnapshot`, `Notification` and ancestry are projection-only records. `RunTransition` and `RouteOutcome` are append-only; current state is derived from their accepted sequence rather than overwritten in place.

### Cardinalities and legal transitions

Per thread:

- active nonterminal `Interaction`: `0..1`;
- foreground `Run`: `0..1`;
- child runs: `0..n`, bounded by host policy.

These cardinalities are independent. An interaction may remain active with no foreground run while children execute; a foreground run may await external work while the interaction is `awaiting-user`; child runs never become conversational owners merely by finishing.

Legal `Interaction` transitions:

```text
running -> awaiting-user | handoff-ready | blocked | completed | abandoned
awaiting-user -> running | blocked | abandoned
handoff-ready -> completed | abandoned
blocked -> abandoned
completed -> [terminal]
abandoned -> [terminal]
```

Continuing after `blocked`, `completed` or `abandoned` creates a new Interaction linked to the prior interaction; it does not reopen the terminal record.

Legal observed `Run` transitions:

```text
queued -> running | cancel-requested | blocked | failed
running -> awaiting-user | cancel-requested | blocked | succeeded | failed
awaiting-user -> running | cancel-requested | blocked | failed
cancel-requested -> cancelled | cancellation-unknown
blocked | succeeded | failed | cancelled | cancellation-unknown -> [terminal]
```

`cancelled` requires acknowledgement from the execution owner. If acknowledgement cannot be established, the attempt terminates as `cancellation-unknown` with last verified owner state, outstanding risk and recovery instructions. `blocked` is terminal for that attempt. Resume always creates a new `runId`, sets `resumesRunId`, obtains a newly approved snapshot if context/input changes, and preserves the old transitions and residue. No terminal transition may be rewritten.

### Turn classification

Classification precedes capability choice:

1. explicit interrupt, stop, named command or clear topic switch;
2. marked side note;
3. response to the thread’s active `awaiting-user` interaction;
4. declared handoff continuation;
5. fresh route if no active interaction exists;
6. one focused continue-versus-fresh question when materially ambiguous.

Only then choose execution disposition. Explicit commands retain precedence and still pass their existing owner gates. Low-confidence routes are offers, never silent execution. [`necronomicon/README.md:97-128,413-433`; Route-decision explorer; `controller.ts:238-275`]

### Easy, Test and Hardening

- **Easy:** inline or one bounded existing capability run; reversible; no reusable correctness claim. Task Session may own one bounded task.
- **Test:** repeatable fixture/regime evidence against an existing contract. Experiment Harness or an explicitly equivalent evaluator owns test mechanics and report evidence.
- **Hardening:** lifecycle proposal justified by repetition, reuse, drift, recurring failure or changed contract. Spellcraft owns reusable composition; Sigil Development owns primitive contract changes.

A route card must expose owner, attention/execution cost, artifact, evidence ceiling, reversibility and required confirmation. Hardening is never inferred from one occurrence, and no evaluation result promotes a reusable artifact automatically. [Route-decision explorer §§3–5; `task-session/SKILL.md:32-110`; `experiment-harness/SKILL.md:45-165`; `spellcraft/SKILL.md:31-163`]

Capability gaps search current installed surfaces and canonical registries, offer only credible fallbacks, and block if none exists. Adding/installing a capability, authoring a spell/sigil, or making a consequential choice remains explicitly owner-gated. [`necronomicon/README.md:393-433`]

### First user-value acceptance slice: executable two-child browser witness

Infrastructure work does not establish product value. The first acceptance slice is this live browser sequence:

1. `T-arch/I-arch` is active and the user continues a normal main conversation.
2. The user requests, in parallel, a governed subagent-strategy proposal and a Whisper page.
3. A route preview shows two child owners, isolated context selectors, forbidden scopes, expected receipts and approval requirements; zero work begins before approval.
4. Approval creates distinct immutable snapshots and child envelopes `R-strategy-a1` and `R-whisper-a1`, each referencing its real execution owner.
5. The parent interaction remains active while both children run.
6. The user switches to `T-other`; neither child pauses, reparents, receives `T-other` content or steals focus.
7. Only `R-strategy-a1` enters `awaiting-user`. Its notification/run surface asks one clarification.
   With toast and audible delivery muted for `T-arch`, the strategy clarification remains unread and discoverable in the run tray and parent-thread projection without moving focus. Answering it from that notification targets only `R-strategy-a1`; the parent interaction, Whisper run, sibling thread and their snapshot digests remain unchanged.
8. The user answers through that surface. The answer is addressed only to the strategy owner; strategy receives an append-only context/input update under its owner contract. Whisper, the parent interaction, the sibling thread and sibling snapshot remain byte/digest unchanged.
9. Whisper succeeds with an owner artifact reference. Strategy subsequently either returns its owner result or terminates blocked with owner residue.
10. The user independently attaches the Whisper result and inspects/consumes the strategy result or blocker. Neither action consumes the sibling notification or changes the active interaction.
    Reload before consumption: unread notification projections restore, but toast, sound and live-region announcement counts do not increase. Consuming the Whisper result marks only its notification/result consumed; the strategy clarification, blocker or result retains its own unread and consumption state.
11. Assertions prove that planted prompt, secret and artifact markers never appear outside their allowed snapshot, owner request, output, notification or attachment.
12. No child transcript, artifact or answer enters checkpoint/memory state without a separate owner-gated intake action.

This is the first claimable session-fabric product acceptance. It requires live browser evidence; component rendering or workspace creation alone is insufficient. [Session-state explorer §“Witness trace”; Human-interface explorer §§3–6 and browser fixtures; current global-lock limitation at `run-guard.ts:8-18`]

### Named fixture suite

- `route-continuation-pending-owner`
- `route-side-note-no-focus-change`
- `route-fresh-explicit-interrupt`
- `route-ambiguity-one-question`
- `route-unsupported-no-invented-capability`
- `offer-easy-one-bounded-reversible`
- `offer-test-evidence-owner`
- `offer-hardening-lifecycle-owner`
- `two-child-browser-isolation-acceptance`
- `sibling-cancellation-independence`
- `strategy-clarification-targeted-answer`
- `blocked-attempt-terminal-residue`
- `restart-reconcile-no-fabricated-running`
- `resume-new-attempt-resumes-run-id`
- `notification-coalescing-and-selective-consume`
- `notification-policy-run-thread-project-inheritance`
- `notification-muted-clarification-still-discoverable`
- `notification-snooze-does-not-consume`
- `notification-progress-coalescing`
- `notification-one-transition-one-unread-item`
- `notification-restoration-does-not-reannounce`
- `notification-independent-read-and-result-consumption`
- `notification-destructive-imminent-loss-exception`
- `notification-keyboard-focus-and-live-region`
- `secret-prompt-artifact-no-bleed`
- `no-silent-memory-intake`
- `preview-is-not-execution`
- `focus-switch-does-not-reparent`
- `late-owner-result-after-cancel-ignored`

Unit tests cover immutable records, legal-transition rejection, owner revalidation, hydration defaults, append-only outcomes, target-only clarification delivery, snapshot digests, sibling independence and terminal resume semantics. Unit tests must also prove notification override precedence, mute/unmute and snooze expiry, one-notification-per-transition deduplication, independent unread/result-consumption state, progress coalescing, restoration without announcement replay, and rejection of notification attempts to mutate run, interaction, artifact or memory authority. Browser tests cover the executable witness, thread switching, no focus steal, independently consumed outputs, restart presentation, keyboard/focus behavior, polite-live-region counts and reduced motion. They must also prove that a muted clarification remains visible and keyboard-answerable from the correct run/parent thread without focus steal, that only the addressed child receives the answer, that consuming one sibling result leaves the other notification unchanged, and that assertive delivery occurs only for the destructive/imminent-loss fixture.

### Labeled route-quality corpus

| Corpus label | Expected disposition | Expected owner | Confirmation | Offer |
|---|---|---|---|---|
| `continue-decision-answer` | continue | active Decision Gate | no new confirmation | none |
| `continue-strategy-clarification` | continue | addressed child strategy owner | owner contract only | none |
| `side-note-later-sqlite` | side_note | thread interaction queue | no | none |
| `fresh-explicit-task-session` | fresh_route | Task Session | existing mutation gate if applicable | Easy |
| `ambiguous-oauth-reframe` | clarify | host router | no execution | none |
| `unsupported-canary` | capability_gap | none/fallback discovery | required before install/author | none/Hardening proposal |
| `easy-one-off-summary` | fresh_route | inline | no | Easy |
| `test-three-regimes` | fresh_route | Experiment Harness | batch/overwrite gate | Test |
| `hardening-repeated-composition` | fresh_route | Spellcraft | lifecycle approval | Hardening |
| `changed-sigil-contract` | fresh_route | Sigil Development | lifecycle approval | Hardening |
| `parallel-two-children` | fresh_route | Dispatch/Orchestrate plus child owners | explicit dispatch approval | delegated |
| `risky-publish-charge` | fresh_route/block | protected action owner | mandatory | Easy hidden |
| `ordinary-chat-low-fit` | fresh_route/inline conversation | provider chat | no | Easy or none |
| `thread-a-secret-thread-b` | fresh route in B | B owner only | as selected | no inherited A context |

Proposed acceptance thresholds, pending router/evaluation-owner acceptance:

- exact conversation disposition accuracy: **≥95%**;
- macro-F1 across `continue`, `side_note`, `fresh_route`, `clarify`: **≥0.95**;
- emit the complete confusion matrix for every corpus run;
- silent delegation count: **0**;
- protected false-continuation count: **0**;
- mutation owner and confirmation-gate correctness: **100%**;
- explicit command precedence regressions: **0**.

Proposed asymmetric error costs:

- false continuation: `5`;
- false fresh route: `2`;
- unnecessary clarification: `1`;
- other incorrect disposition: `3`.

Report `weighted_error_per_100 = 100 * sum(error_cost) / corpus_items`; proposed gate: **≤5**, while the zero-tolerance delegation, protected false-continuation and mutation-gate rules override the aggregate score. Evaluation belongs to Experiment Harness or an explicitly declared equivalent evidence owner, not the router or observability projection.

### Attention, latency, token and storage measures

All thresholds below are proposed and pending owner acceptance:

- route-card exposure on ordinary conversational turns: `≤20%`;
- clarification rate on the labeled production-like corpus: `≤5%`;
- median extra user actions: `0` for ordinary continuation, `≤1` for accepted low-risk offer, `≤2` for consequential launch;
- announcements per run: `≤1` per terminal or human-attention transition, with progress coalesced;
- median blocker-resume time: `≤60 seconds` and `≤2` user actions once the required input is available;
- deterministic classifier p95: `≤50 ms`;
- bounded semantic-assist p95, if admitted: `≤300 ms`;
- router-added context: `≤10%` of host prompt budget;
- routing telemetry: `≤1%` of routed-turn token volume;
- persisted RouteDecision/RouteOutcome payload: `≤2 KB` each, excluding referenced owner artifacts;
- initial choices: recommended, best alternative and “More options” only;
- recent visible terminal runs: `20`, with older summaries archived by reference;
- initial child concurrency ceiling: `2` until isolation, cancellation and restart gates pass.

Persist only request digest, interaction class, candidates, selection, confidence, clarification resolution, gap/offer class, owner references, outcome, validation and explicit correction. Do not persist full prompts, secrets, chain-of-thought or copied owner artifacts as router telemetry. Repetition may trigger a maintenance recommendation but cannot authorize lifecycle change. [`necronomicon/README.md:368-407`; Human-interface explorer §“Attention budget”]

### Increments

- **v0 — infrastructure only:** introduce public-neutral classification projections, immutable decisions/outcomes, current-owner revalidation, optional normalization, and honest workspace/owner references. Preserve commands and global-run behavior. Its browser check proves only preview, approval, persistence and “workspace created; execution has not started.” It is not product or session-fabric acceptance.
- **v1 — first user-value acceptance:** add per-thread interaction projection, independent foreground/child cardinalities, immutable snapshots, Run correlation envelopes, append-only transitions, targeted clarification, notification/run tray, cancellation acknowledgement, terminal blocker residue, restart reconciliation, resume-as-new-attempt and explicit artifact attachment. Pass the executable two-child browser witness.
- **v2 — evaluated hardening:** run the labeled corpus and browser regimes through Experiment Harness or equivalent owner; calibrate confidence, attention and cost thresholds; add bounded scheduler/join variants; admit only versioned public-neutral rule updates; route repeated reusable composition to Spellcraft and primitive changes to Sigil Development without automatic authoring or promotion.

No session-fabric, concurrency, routing-quality or memory-safety claim is justified until the corresponding v1/v2 live evidence passes.

## REPAIR_CLOSURE

| Reviewer axis | Revised sections |
|---|---|
| Explorer-count correction | “Evidence and freshness” explicitly records exactly four explorer sections. |
| Host/runtime precedent | “Public/private-safe admission boundary,” “Current versus missing,” and “Ownership and reference model.” |
| Run non-competition | “Normative one-way chain,” ownership table, and minimal `Run.ownerRefs`. |
| One-way authority and no reverse writes | “Normative one-way chain.” |
| Interaction/run non-collapse | “Cardinalities and legal transitions.” |
| Cancellation, blocked and resume semantics | “Cardinalities and legal transitions” plus named blocker/restart/resume fixtures. |
| Public/private safety | “Public/private-safe admission boundary.” |
| First non-vacuous product slice | “First user-value acceptance slice: executable two-child browser witness.” |
| Exact fixtures | “Named fixture suite.” |
| Quality corpus and gates | “Labeled route-quality corpus.” |
| Asymmetric costs and weighted error | Final paragraphs of “Labeled route-quality corpus.” |
| Attention and resource metrics | “Attention, latency, token and storage measures.” |
| v0 overclaim removal | “Increments,” where v0 is explicitly infrastructure-only. |

ORCHESTRATE_RECEIPT
action_id=spawn-0005
dispatch_id=2026-07-28-augmentor-routing-session-fabric-route
run_id=20260729T0145Z-routing-session-fabric-001
wave_id=synthesizer
step_id=s2
role=routing-session-synthesizer
capability_ref=research
status=pass
artifacts=[research/2026-07-28-augmentor-routing-session-fabric/research.md,arcanum/spells/necronomicon/README.md,arcanum/formulae/dispatch-spec/SKILL.md,arcanum/arcana/task-session/SKILL.md,arcanum/arcana/decision-gate/SKILL.md,arcanum/arcana/experiment-harness/SKILL.md,arcanum/arcana/spellcraft/SKILL.md,projects/ide-ergonomics/PRODUCT-VIEW.md,projects/ide-ergonomics/UNIFIED-PRODUCT-VIEW.md,../workspace-resonant/2.0.0-alpha/src/core/contracts.ts,../workspace-resonant/2.0.0-alpha/src/core/compute-fabric.ts,../workspace-resonant/2.0.0-alpha/src/core/delegation.ts,../workspace-resonant/2.0.0-alpha/src/core/runtime.ts,../workspace-resonant/2.0.0-alpha/src/modules/chat/controller.ts,../workspace-resonant/2.0.0-alpha/src/modules/chat/run-guard.ts,../workspace-resonant/2.0.0-alpha/src/modules/chat/StrategistChatRail.tsx,../workspace-resonant/2.0.0-alpha/public/addons/augmentor-chat.json,git:dev..origin/dev]
validation=pass
blockers=[]
residue=All architecture, thresholds, state projections and v1-v2 acceptance contracts remain proposed pending owner acceptance. Current ResonantOS still has one global transient chat-run guard and cannot execute or prove the two-child session-fabric witness. The analyzed checkout is seven commits behind origin/dev; scoped runtime sources are unchanged upstream, but package.json differs.
handoff_note=Treat v0 only as enabling infrastructure. The first product acceptance gate is the executable two-child browser witness with targeted child clarification, independent result/blocker consumption, no context or secret bleed, no focus steal, restart-safe residue and zero silent checkpoint or memory intake.
