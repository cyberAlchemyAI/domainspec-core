# Augmentor routing and session fabric — findings

## Status and product thesis

This is an implementation-usable **blueprint**, not an implementation, accepted runtime schema, or product proof. Current ResonantOS has project/thread contracts, goal workspaces, bounded delegation/task workspaces, durable shell persistence, command routing, and goal/delegation artifact contracts. [Consumer-runtime explorer, “Current-versus-missing matrix”; `../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:2769-2822,2019-2105,1958-2002,1058-1069,2097-2110`, `../workspace-resonant/2.0.0-alpha/src/core/delegation.ts:39-96`, `../workspace-resonant/2.0.0-alpha/src/core/runtime.ts:1369-1381,1458-1477`, `../workspace-resonant/2.0.0-alpha/src/modules/chat/controller.ts:238-275`]

Active chat execution remains **one global transient run**. General concurrent child runs, durable run ancestry, notification runtime, join/resume semantics, and the browser witness defined here are not current behavior. [Consumer-runtime explorer, “Current-versus-missing matrix”; `../workspace-resonant/2.0.0-alpha/src/modules/chat/run-guard.ts:5-28`, `../workspace-resonant/2.0.0-alpha/src/App.tsx:1224-1269`, `../workspace-resonant/2.0.0-alpha/src/modules/chat/controller.ts:194-206`]

The product thesis is one conversational shell in which each turn is first interpreted against a thread-local active interaction and only then routed to an execution owner. Consequential routing becomes an immutable host decision; approved execution is correlated through a `Run` envelope without transferring authority from commands, registries, approvals, compute, goals, delegation, task workspaces, dispatch, artifacts, evaluation, or memory. [Route-decision explorer, “Governing model”; `arcanum/spells/necronomicon/README.md:97-128`; Session-state explorer, “Why the model has these nodes”; `../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:1958-2105`]

The experience is primary: the user keeps talking in the parent thread, can see why work was routed, can approve or refuse consequential launches, can change focus while bounded children continue, and receives independently controllable results or blockers. Receipts support these actions but never replace them. [Human-interface explorer, “Progressive-disclosure journeys”; `projects/ide-ergonomics/PRODUCT-VIEW.md#step-3-show-the-route-menu`, `projects/ide-ergonomics/PRODUCT-VIEW.md#pass-conditions`]

## Current versus missing

| Concern | Current, claimable state | Missing contract |
|---|---|---|
| Focus and threads | UI preferences hold `activeChatThreadId`; projects, thread history, branching, moving, renaming, and deletion exist. [Session-state explorer, “Why the model has these nodes”; `../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:2769-2822`; Human-interface explorer, “Human-interface finding”; `../workspace-resonant/2.0.0-alpha/src/modules/chat/StrategistChatRail.tsx:281-759`] | Thread-local interaction ownership and a focus-independent run projection. |
| Active execution | One mutable token excludes any other chat run, and live run events are transient. [Consumer-runtime explorer, “Current-versus-missing matrix”; `../workspace-resonant/2.0.0-alpha/src/modules/chat/run-guard.ts:5-28`, `../workspace-resonant/2.0.0-alpha/src/modules/chat/controller.ts:194-206`] | Per-thread foreground exclusion, bounded children, durable transitions, ancestry, join, cancellation acknowledgement, and restart reconciliation. |
| Compute | `ComputeJob` already owns job type, constraints, node selection, policy, approval, audit path, and job status; validation rejects invalid or unapproved work. [Consumer-runtime explorer, “Current-versus-missing matrix” and “Smallest host-owned integration seam”; `../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:212-239,1034-1056`, `../workspace-resonant/2.0.0-alpha/src/core/compute-fabric.ts:194-255,303-327`] | Only an optional `computeJobId` correlation from `Run`; no copied compute policy or status. |
| Delegation and workspaces | Typed delegation packets and path-bearing task workspaces exist; some flows explicitly create a workspace while stating execution has not started. [Session-state explorer, “Why the model has these nodes”; `../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:1958-2002`, `../workspace-resonant/2.0.0-alpha/src/core/delegation.ts:39-96,582-592`] | A run lifecycle that references these owners without pretending workspace creation is execution. |
| Artifacts and memory | Goal/delegation contracts own artifacts; checkpoint intake separates evidence classes and redacts private content. [Consumer-runtime explorer, “Current-versus-missing matrix”; `../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:1058-1069,2097-2110`; Session-state explorer, “Invariants”; `arcanum/spells/necronomicon/README.md:349-357`] | Explicit artifact attachment and owner-gated memory intake; no silent transcript or child-context merge. |
| Notifications and restoration | The Augmentor manifest asks for notifications, but inspected runtime code has no notification state, producer, restoration, or UI wiring; durable shell hydration does not restore live runs. [Consumer-runtime explorer, “Current-versus-missing matrix”; `../workspace-resonant/2.0.0-alpha/public/addons/augmentor-chat.json:56`, `../workspace-resonant/2.0.0-alpha/src/core/runtime.ts`] | Projection state, policy inheritance, selective consumption, delivery deduplication, and reconciliation of interrupted attempts. |

## State and ownership model

The smallest surviving hierarchy is:

```text
Interface focus
  └─ Project/workspace
      └─ Thread
          ├─ Active Interaction (0..1)
          ├─ Foreground Run (0..1)
          └─ Child Runs (0..n, policy-bounded)
              ├─ immutable ContextSnapshot
              ├─ owner artifact/blocker references
              └─ Notification projections
```

Focus is a projection, not execution ownership. `Interaction` owns interpretation of the next turn. `RouteDecision` records classification and proposed ownership. `Run` correlates one execution attempt. `ContextSnapshot` freezes admitted launch context. `Notification` and ancestry are UI projections. Durable memory remains outside the live hierarchy. [Session-state explorer, “Finding,” “Minimal proposed records,” and “Invariants”; `../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:2769-2822`, `arcanum/spells/necronomicon/README.md:97-124,314-357`]

The authority chain is one-way:

```text
user turn
  -> immutable RouteDecision
  -> existing owner gate
  -> immutable ContextSnapshot
  -> Run correlation envelope
  -> owner execution / owner receipt
  -> append-only RunTransition and RouteOutcome
  -> explicit artifact attach or memory-intake action
```

No reverse edge is permitted: route confidence cannot authorize execution; `Run` cannot mutate `ComputeJob`, `GoalWorkspace`, `DelegationPacket`, `TaskWorkspace`, or Dispatch state; notifications cannot settle run or artifact truth; artifact consumption cannot imply memory acceptance. [Route-decision explorer, “RouteDecision”; `arcanum/arcana/decision-gate/SKILL.md:51-73`; Session-state explorer, “Invariants”; `../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:1958-2105`]

Minimal projections:

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

These are proposed host projections. In particular, `Run.ownerRefs.computeJobId` points to the existing Compute Fabric owner; `Run` must never copy or adjudicate compute constraints, approval, scheduling, audit, or status. [Consumer-runtime explorer, “Smallest host-owned integration seam” and “Additive contract proposal”; `../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:212-239,1034-1056`, `../workspace-resonant/2.0.0-alpha/src/core/compute-fabric.ts:194-255,303-327`]

## Classification and route decisions

Classification precedes capability choice:

1. explicit interrupt, stop, named command, or clear topic switch;
2. marked side note;
3. answer to the thread’s active `awaiting-user` owner;
4. declared handoff continuation;
5. fresh route when no interaction is active;
6. one focused “continue here or start fresh?” question when ambiguity is material.

Then choose `inline_answer`, `existing_capability_run`, `delegated_background_run`, `capability_gap`, or `none`. Explicit commands retain precedence but still pass their owner gates; low-confidence candidates are offers, never silent execution. [Route-decision explorer, “Governing model” and “RouteDecision”; `arcanum/spells/necronomicon/README.md:97-128,413-433`; Consumer-runtime explorer, “Smallest host-owned integration seam”; `../workspace-resonant/2.0.0-alpha/src/modules/chat/controller.ts:238-275`]

A route card exposes the recommendation, reason, owner, included context, expected artifact, attention/execution cost, evidence ceiling, reversibility, forbidden effects, and required confirmation. Preview and selection create no run. [Human-interface explorer, “Ordinary free-form routing” and “Background subagent-strategy proposal”; `projects/ide-ergonomics/PRODUCT-VIEW.md#step-3-show-the-route-menu`, `projects/ide-ergonomics/PRODUCT-VIEW.md#pass-conditions`]

### Easy, Test, Hardening

| Offer | When genuine | Owner and ceiling |
|---|---|---|
| Easy | Inline or one reversible bounded run; no protected mutation and no reusable-correctness claim. | Inline owner or Task Session; explanation or one-run receipt. [Route-decision explorer, “Easy”; `arcanum/arcana/task-session/SKILL.md:32-69,100-110`] |
| Test | Repeatable fixtures/regimes against an existing contract. | Experiment Harness owns mechanics and evidence; it does not rewrite the target contract. [Route-decision explorer, “Test”; `arcanum/arcana/experiment-harness/SKILL.md:47-60,97-99,123-148`] |
| Hardening | Repetition, reuse, drift, recurring failure, new gates, or a changed primitive justifies lifecycle work. | Spellcraft owns reusable composition; Sigil Development owns primitive contract changes; neither is auto-promoted. [Route-decision explorer, “Hardening”; `arcanum/arcana/spellcraft/SKILL.md:31-40,92-163`] |

For a capability gap, search installed surfaces and canonical registries, offer only credible fallbacks, and block if none exists. Installing or adding a capability, authoring a spell/sigil, or resolving a consequential alternative remains explicitly gated; observing a gap authorizes none of them. [Route-decision explorer, “Capability-gap escalation”; `arcanum/spells/necronomicon/README.md:393-433`]

## Child runs, handoffs, isolation, and recovery

A child launches only from an approved bounded contract naming capability, target, mode, inputs, outputs, mutation policy, allowed/forbidden scope, expected artifact/receipt, and join policy. Parallel multi-agent work additionally requires a validated Dispatch Spec and explicit authorization; the orchestrator owns spawn, join, gates, and closeout. [Route-decision explorer, “Delegation and parallelism”; `arcanum/formulae/dispatch-spec/SKILL.md:65-145`, `arcanum/formulae/dispatch-spec/CAPABILITY-BOUND-DELEGATION.md:64-77`]

Each run receives one immutable snapshot identified by digest and message horizon. Later parent or sibling messages are invisible unless an explicit, addressed context-update event creates a new snapshot/input revision under the execution owner. Completion returns artifact or blocker handles, never a transcript merge. [Session-state explorer, “Invariants” and “Witness trace”; `arcanum/spells/necronomicon/README.md:314-357`; Human-interface explorer, “Whisper page as a child artifact run”; `projects/ide-ergonomics/knowledge-entry-references/SPEC.md#6-popup-contract`, `projects/ide-ergonomics/knowledge-entry-references/SPEC.md#8-owner-safe-actions`]

The following cancellation acknowledgement, `cancellation-unknown`, terminal-blocker, `resumesRunId`, and join-policy state machine is **proposed acceptance semantics from the explorer and synthesis, not current ResonantOS behavior**. Current evidence establishes only bounded delegation packets/task workspaces and a global transient run guard. [Session-state explorer, “Compact state machine” and “Invariants”; `../workspace-resonant/2.0.0-alpha/src/core/delegation.ts:39-96,582-592`, `../workspace-resonant/2.0.0-alpha/src/modules/chat/run-guard.ts:5-28`]

Proposed legal observed run transitions are:

```text
queued -> running | cancel-requested | blocked | failed
running -> awaiting-user | cancel-requested | blocked | succeeded | failed
awaiting-user -> running | cancel-requested | blocked | failed
cancel-requested -> cancelled | cancellation-unknown
blocked | succeeded | failed | cancelled | cancellation-unknown -> terminal
```

Under that proposed contract, `cancelled` requires owner acknowledgement; otherwise the attempt ends `cancellation-unknown` with last verified state and outstanding risk. `blocked` is terminal for that attempt. Resume creates a new `runId`, sets `resumesRunId`, preserves old transitions, and records a new approved snapshot if inputs changed. Join means consuming a terminal result under `notify`, `manual-consume`, or `join-before-continue`; it never copies child history into the parent. [Session-state explorer, “Compact state machine” and “Invariants”; `../workspace-resonant/2.0.0-alpha/src/core/delegation.ts:39-96,582-592`, `../workspace-resonant/2.0.0-alpha/src/modules/chat/run-guard.ts:5-28`]

## Repaired notification-control contract

Notification inheritance, deduplication, selective consumption, restoration, and user controls in this section are **proposed acceptance requirements, not current runtime behavior**. Current `StrategistChatRail` supplies polite activity/live-region and active-run UI atoms; the consumer-runtime explorer found no implemented notification state, producer, restoration, or control runtime. [Human-interface explorer, “Completion, blocker, clarification,” “Keyboard and accessibility contract,” and “Attention budget”; `../workspace-resonant/2.0.0-alpha/src/modules/chat/StrategistChatRail.tsx:596-603,762-795`; Consumer-runtime explorer, “Current-versus-missing matrix”; `../workspace-resonant/2.0.0-alpha/public/addons/augmentor-chat.json:56`]

The proposed notification policy resolves from **run override → thread override → project override → user default**. Muting or snoozing suppresses toast, sound, and live-region delivery, but never hides the run-tray item, parent-thread projection, artifact, clarification, blocker, or recovery action. Snooze expiry changes future delivery only; it does not consume or replay prior events. [Human-interface explorer, “Completion, blocker, clarification,” “Keyboard and accessibility contract,” and “Attention budget”; current UI atoms at `../workspace-resonant/2.0.0-alpha/src/modules/chat/StrategistChatRail.tsx:596-603,762-795`]

The proposed contract creates at most one notification per meaningful transition and coalesces progress into the existing run item. Read state, delivery state, and result consumption are independent per notification. Reading or consuming one sibling must not mark another read, attach its artifact, resolve its blocker, or consume its result. Hydration must restore unread items and policy state without replaying toast, sound, or live-region announcements already delivered. [Human-interface explorer, “Completion, blocker, clarification,” “Attention budget,” and browser fixtures; current run UI atom at `../workspace-resonant/2.0.0-alpha/src/modules/chat/StrategistChatRail.tsx:762-795`; Session-state explorer, “Invariants”; `arcanum/spells/necronomicon/README.md:349-357`]

As proposed acceptance requirements, all controls—mute, unmute, snooze, mark read, open run, answer clarification, and consume result—must be keyboard-operable with visible labels and programmatic state. Events never move focus; opening/dismissing restores prior focus. Routine events use polite announcements. Only destructive failure or imminent data-loss risk may bypass mute/snooze with assertive delivery; ordinary completion, failure, blocker, and clarification may not. [Human-interface explorer, “Keyboard and accessibility contract” and “Attention budget”; current polite activity/run UI atoms at `../workspace-resonant/2.0.0-alpha/src/modules/chat/StrategistChatRail.tsx:596-603,762-795`]

## Literal v1 browser witness

1. `T-arch/I-arch` is active and ordinary architecture conversation continues.
2. The user says: **“In parallel, prepare a governed subagent-strategy proposal and a Whisper page.”**
3. A route preview shows two child owners, isolated context selectors, forbidden scopes, expected receipts/artifacts, join policies, and approval requirements. No work begins from preview.
4. Approval creates distinct snapshots and child envelopes `R-strategy-a1` and `R-whisper-a1`, each referencing its real execution owner.
5. The parent interaction remains active while both children run.
6. The user switches to `T-other`; neither child pauses, reparents, receives `T-other` content, or steals focus.
7. Only `R-strategy-a1` enters `awaiting-user`. With toast and sound muted for `T-arch`, its question remains unread and keyboard-answerable in the run tray and parent-thread projection without focus steal.
8. The answer targets only `R-strategy-a1` through an append-only owner input/context update. The parent, Whisper run, sibling thread, and their snapshot digests remain unchanged.
9. Whisper succeeds with an owner artifact reference. Strategy later succeeds or terminates blocked with owner residue.
10. Before consumption, reload. Unread projections restore; toast, sound, and live-region counts do not increase.
11. The user attaches the Whisper artifact and separately consumes or inspects the strategy result/blocker. Neither action changes the active interaction or sibling notification.
12. Planted secret, prompt, and artifact markers appear only in their allowed snapshot, owner request/output, bounded notification, or explicit attachment; no child material enters memory without a separate owner-gated intake.

This concurrent subagent-strategy plus Whisper-page witness is the **first product acceptance contract**, not a claim that the behavior exists. [Session-state explorer, “Witness trace,” “Failure cases,” and fixtures 1–5; `../workspace-resonant/2.0.0-alpha/src/modules/chat/run-guard.ts:8-18`; Human-interface explorer, journeys 3–6 and “Browser-testable fixtures”; `projects/ide-ergonomics/PRODUCT-VIEW.md#mvp-shape`, `projects/ide-ergonomics/PRODUCT-VIEW.md#pass-conditions`]

## Routing-quality fixture matrix

| Fixture | Expected result |
|---|---|
| `continue-decision-answer` | `continue`; active Decision Gate; no new confirmation |
| `continue-strategy-clarification` | `continue`; addressed strategy child only |
| `side-note-later-sqlite` | `side_note`; queue only; no focus change |
| `fresh-explicit-task-session` | `fresh_route`; Task Session; preserve mutation gate |
| `ambiguous-oauth-reframe` | `clarify`; one question; no execution |
| `unsupported-canary` | `capability_gap`; honest fallback or block; never invent |
| `easy-one-off-summary` | inline/one bounded route; no reusable claim |
| `test-three-regimes` | Experiment Harness; repeatable evidence; no contract rewrite |
| `hardening-repeated-composition` | Spellcraft proposal; lifecycle approval required |
| `changed-sigil-contract` | Sigil Development; lifecycle approval required |
| `parallel-two-children` | Dispatch/Orchestrate plus child owners; explicit approval |
| `risky-publish-charge` | Easy hidden; protected owner gate mandatory |
| `ordinary-chat-low-fit` | inline conversation; no forced route card |
| `thread-a-secret-thread-b` | B owner only; no inherited A context |

These labels instantiate the explorer’s exact continuation, side-note, ambiguity, unsupported, evidence-level, risky, parallel, and changed-contract cases against current command precedence and installed-owner resolution. [Route-decision explorer, “Exact fixtures”; `arcanum/spells/necronomicon/README.md:97-128,393-433`, `arcanum/arcana/decision-gate/SKILL.md:51-91`; Consumer-runtime explorer, “Exact tests to add”; `../workspace-resonant/2.0.0-alpha/src/modules/chat/controller.ts:238-275`]

Proposed v2 gates are exact disposition accuracy `≥95%`, macro-F1 `≥0.95`, complete confusion matrix output, zero silent delegations, zero protected false continuations, `100%` mutation-owner/confirmation correctness, and zero explicit-command precedence regressions. Error costs are false continuation `5`, false fresh route `2`, unnecessary clarification `1`, other error `3`; `weighted_error_per_100 = 100 * sum(error_cost) / corpus_items` must be `≤5`, subject to the zero-tolerance overrides. These thresholds require evaluation-owner acceptance and evidence; the router cannot grade itself. [Route-decision explorer, “Minimal routing telemetry” and “Exact fixtures”; `arcanum/arcana/experiment-harness/SKILL.md:47-60,97-99,123-148`; Consumer-runtime explorer, “Exact tests to add”; `../workspace-resonant/2.0.0-alpha/src/modules/chat/controller.ts:238-275`]

## Exact tests

Unit tests:

- reject mutation of immutable `RouteDecision`, snapshots, terminal transitions, and outcomes;
- reject illegal interaction/run transitions and terminal reopening;
- revalidate selected commands, manifests, registries, approval, delegation, and ComputeJob ownership before launch;
- normalize absent optional projection arrays during hydration without fabricating a running owner;
- prove snapshot digests exclude late parent/sibling messages;
- target clarification answers to one child only;
- prove sibling cancellation independence and ignore late owner results after acknowledged cancellation;
- resume a blocker as a new attempt with `resumesRunId` and preserved residue;
- prove notification override precedence, mute/unmute, snooze expiry, one-transition/one-item deduplication, progress coalescing, independent read/delivery/result-consumption, and restoration without replay;
- reject any notification attempt to mutate run, interaction, artifact, ComputeJob, or memory authority.

These tests close the state, ownership, restoration, and notification failure modes identified by the explorers rather than asserting UI presence alone. [Session-state explorer, “Failure cases” and “Exact fixture ideas”; `../workspace-resonant/2.0.0-alpha/src/core/delegation.ts:39-96`; Consumer-runtime explorer, “Exact tests to add”; `../workspace-resonant/2.0.0-alpha/src/modules/chat/run-guard.ts:5-28`, `../workspace-resonant/2.0.0-alpha/src/core/runtime.ts`]

Browser tests:

- execute the full two-child witness, including approval-before-launch and literal strategy/Whisper owners;
- switch threads during both children and assert no pause, reparent, context bleed, or focus steal;
- answer one muted child clarification by keyboard and assert only that child changes;
- independently consume one success and one blocker/result;
- reload and prove unread restoration without reannouncement or fabricated running state;
- verify cancellation acknowledgement, sibling survival, terminal blocker residue, and resume-as-new-attempt;
- plant secret/prompt/artifact markers and assert allowed-surface containment;
- verify keyboard focus restoration, visible state labels, reduced motion, polite counts, and assertive delivery only for the destructive/imminent-loss fixture;
- prove no silent checkpoint or memory intake.

These are product acceptance tests because current rendering has only an active-conversation run card and a global busy guard; component rendering or workspace creation cannot prove concurrent user value. [Human-interface explorer, “Browser-testable fixtures”; `../workspace-resonant/2.0.0-alpha/src/modules/chat/StrategistChatRail.tsx:762-796`; Consumer-runtime explorer, “v0 browser witness”; `../workspace-resonant/2.0.0-alpha/src/modules/chat/run-guard.ts:5-28`, `../workspace-resonant/2.0.0-alpha/src/core/delegation.ts:582-592`]

## Bounded overhead

Pending owner acceptance, bound the product to: route cards on `≤20%` of ordinary turns; clarification rate `≤5%`; median extra actions `0` for continuation, `≤1` for an accepted low-risk offer, and `≤2` for consequential launch; at most one announcement per terminal or attention transition; blocker resume median `≤60s` and `≤2` actions after input is available; deterministic classification p95 `≤50ms`; admitted semantic assist p95 `≤300ms`; router context `≤10%` of host prompt budget; routing telemetry `≤1%` of routed-turn token volume; decision/outcome payload `≤2KB` each excluding referenced artifacts; two primary choices plus “More options”; 20 recent terminal runs; and initial child concurrency `2`. [Human-interface explorer, “Attention budget”; `../workspace-resonant/2.0.0-alpha/src/modules/chat/StrategistChatRail.tsx:281-500,626-683`; Route-decision explorer, “Minimal routing telemetry”; `arcanum/spells/necronomicon/README.md:368-407`]

Persist only digest, interaction class, candidate/selection/confidence, clarification resolution, gap/offer class, owner references, outcome, validation, and explicit correction. Never persist full prompts, secrets, chain-of-thought, or copied owner artifacts as router telemetry. [Route-decision explorer, “Minimal routing telemetry”; `arcanum/spells/necronomicon/README.md:368-407`; Session-state explorer, “Invariants”; `arcanum/spells/necronomicon/README.md:349-357`]

## Integration route and verdict

| Increment | Scope | Verdict |
|---|---|---|
| **v0 — infrastructure only** | Public-neutral classification projections, immutable decisions/outcomes, owner revalidation, optional-field normalization, and honest workspace/owner references. Preserve current commands and global-run behavior. Browser proof is limited to preview, approval, persistence, and “workspace created; execution has not started.” [Consumer-runtime explorer, “Migration posture” and “v0 browser witness”; `../workspace-resonant/2.0.0-alpha/src/core/delegation.ts:582-592`, `../workspace-resonant/2.0.0-alpha/src/modules/chat/run-guard.ts:5-28`] | **Proposed; not implemented; not product acceptance.** |
| **v1 — first product acceptance contract** | Thread-local interaction projection; independent foreground/child cardinalities; snapshots; correlation runs; transitions; targeted clarification; repaired notifications; cancellation acknowledgement; blocker residue; reconciliation; resume-as-new-attempt; explicit attachment; full two-child browser witness. [Session-state explorer, “Witness trace” and “Exact fixture ideas”; `../workspace-resonant/2.0.0-alpha/src/modules/chat/run-guard.ts:8-18`; Human-interface explorer, journeys 3–6 and browser fixtures; `projects/ide-ergonomics/PRODUCT-VIEW.md#pass-conditions`] | **Evidence-ready contract; not implemented or passed.** |
| **v2 — evaluated quality** | Run the labeled corpus and browser regimes through Experiment Harness or an explicit equivalent; calibrate confidence, attention, cost, scheduling, and join variants; admit only versioned public-neutral rule updates; route reusable composition/primitive changes to their lifecycle owners. [Route-decision explorer, “Easy, test, and hardening” and “Exact fixtures”; `arcanum/arcana/experiment-harness/SKILL.md:47-148`, `arcanum/arcana/spellcraft/SKILL.md:31-163`] | **Evaluation owner; no quality result exists.** |

No concurrency, session-fabric, routing-quality, notification-safety, or memory-safety claim is justified until its v1/v2 live evidence passes. [Consumer-runtime explorer, “Compatibility and product risks”; `../workspace-resonant/2.0.0-alpha/public/addons/augmentor-chat.json:56`, `../workspace-resonant/2.0.0-alpha/src/modules/chat/run-guard.ts:5-28`; Session-state explorer, “Failure cases”; `arcanum/spells/necronomicon/README.md:349-357`]

## Open decisions

The accepting owners still need to decide:

1. the exact public-neutral admission artifact and versioning policy for routing precedent;
2. the host persistence location and retention policy for projections and append-only outcomes;
3. scheduler and per-project/per-user child ceilings after the initial ceiling of two;
4. whether any execution owner supports safe in-place context updates, or all clarified input creates a new snapshot revision;
5. exact cancellation acknowledgement and late-result quarantine contracts per owner;
6. reconciliation behavior when an owner cannot prove whether work continued across restart;
7. default notification policy, destructive/imminent-loss taxonomy, snooze durations, and accessibility acceptance owner;
8. artifact attachment and checkpoint/memory intake owner gates;
9. the v2 evaluation owner, corpus stewardship, threshold acceptance, and drift cadence;
10. the update point from the analyzed checkout before implementation, because scoped runtime sources were unchanged across the observed seven upstream commits but `package.json` differed.

These are real owner decisions, not permission for this research dispatch to select schemas, change product behavior, or claim implementation. [Consumer-runtime explorer, “Scope and upstream verification,” “Migration posture,” and “Compatibility and product risks”; `git:dev..origin/dev`, `../workspace-resonant/2.0.0-alpha/package.json`; Route-decision explorer, “Capability-gap escalation”; `arcanum/spells/necronomicon/README.md:393-433`]
