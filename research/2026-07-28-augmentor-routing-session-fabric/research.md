# Verbatim Explorer Returns

## Agent 1 — session-state-explorer

## Session-state explorer — smallest surviving model

### Finding

The smallest survivor is not a single global session and not a fully independent “session” per agent. It is:

```text
Interface
  └─ Project/workspace
      └─ Thread
          ├─ Active interaction (0..1 foreground conversational owner)
          └─ Runs (0..n)
              ├─ foreground run (0..1)
              └─ child/background runs (0..n)
                  ├─ immutable context snapshot
                  ├─ artifact returns
                  └─ notifications / blocked residue
```

Durable memory is outside this live hierarchy: threads and runs hold references to memory, while checkpoints and accepted artifacts are the controlled intake path. Artifact surfaces and notifications are projections over run state, not owners of execution or truth.

This extends the current contracts rather than replacing them. ResonantOS already separates shell focus, projects, threads, goal workspaces, delegation packets, and filesystem task workspaces, but no current type binds them into a complete interaction/run lifecycle. The Inventory packet correctly identifies that as a current-source gap, but is discovery-only evidence (`strategy-inventory-packet.json#unresolved_gaps`).

### Why the model has these nodes

- **Interface** owns focus only: active project, active thread, visible surface, unread notification count. Current ResonantOS already puts `activeChatThreadId` in UI preferences rather than in the thread itself (`../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:2806-2822`).
- **Project/workspace** owns grouping and execution boundaries. A `ChatProject` currently supplies grouping identity and timestamps, while a conversation thread separately carries `workspaceId` and optional `projectId` (`contracts.ts:2769-2786`).
- **Thread** owns ordered conversational history and its default conversational agent. Current `ConversationThread` has stable identity, owner, workspace/channel/project binding, summary, and messages (`contracts.ts:2769-2778`).
- **Active interaction** owns interpretation of the next user turn, not the entire interface. Necronomicon requires a stable interaction ID, owning capability, mode, lifecycle status, pending prompt, expected response shape, continuation policy, handoff target, and side-note queue (`arcanum/spells/necronomicon/README.md#interaction-state-model`, lines 97-124).
- **Route decision** is an immutable decision record between intent and execution. The IDE card requires owner, artifact preview, permission state, source span, and blocked actions; preview and selection are explicitly not execution (`projects/ide-ergonomics/PRODUCT-VIEW.md#step-3-show-the-route-menu`, lines 156-176).
- **Run** owns execution lifecycle. A foreground run may drive the thread’s active interaction; a child/background run must not. ResonantOS goal workspaces already expose `proposed|active|waiting|delegated|blocked|completed|archived`, steps, blockers, artifacts, thread binding, and delegation refs (`contracts.ts:2019-2024`, `2081-2105`).
- **Delegation packet** owns the child’s bounded authority and frozen launch context: mission, context, source/system memory refs, workspace, file/tool scope, forbidden actions, grants, approval, verification, expected artifacts, return protocol, and audit log (`contracts.ts:1958-1982`). Validation already rejects missing workspace, return protocol, artifacts, risky unapproved work, and underspecified code tasks (`../workspace-resonant/2.0.0-alpha/src/core/delegation.ts:39-96`).
- **TaskWorkspace** is only an execution filesystem surface. Its current contract contains paths but no lifecycle, parent link, cancellation, join, or resume fields (`contracts.ts:1984-2002`). It must not be treated as the run itself.
- **Durable memory** owns accepted continuity, not raw live state. Necronomicon separates repository state from session state and routes/checkpoints from decisions and active interaction (`README.md#shared-state`, lines 314-333); checkpoints separate facts, inferences, decisions, contradictions, gaps, and candidates, apply privacy redaction, and never promote candidates themselves (`README.md#checkpoint-and-memory-policy`, lines 349-357).

### Minimal proposed records

```ts
InterfaceState {
  interfaceId
  focusedProjectId?
  focusedThreadId
  focusedSurface: "conversation" | "artifact" | "run-monitor"
}

ThreadState {
  threadId
  projectId?
  workspaceId
  owningAgentId
  activeInteractionId?
  foregroundRunId?
}

Interaction {
  interactionId
  threadId
  owningCapability
  mode
  status: "awaiting-user" | "running" | "handoff-ready"
        | "blocked" | "completed" | "abandoned"
  pendingPrompt?
  expectedResponseShape?
  continuationPolicy
  handoffTarget?
}

RouteDecision {
  routeDecisionId
  threadId
  interactionId
  sourceMessageIds[]
  chosenOwner
  permissionState
  decision: "draft" | "park" | "handoff" | "execute"
  createdRunIds[]
}

Run {
  runId
  parentRunId?
  rootThreadId
  launchInteractionId
  routeDecisionId
  kind: "foreground" | "child"
  owner
  contextSnapshotId
  state: "proposed" | "awaiting-approval" | "queued" | "running"
       | "awaiting-user" | "cancel-requested" | "cancelled"
       | "blocked" | "succeeded" | "failed"
  joinPolicy: "notify" | "manual-consume" | "join-before-continue"
  artifactIds[]
  blockerIds[]
}

ContextSnapshot {
  snapshotId
  threadId
  throughMessageId
  sourceMemoryRefs[]
  systemMemoryRefs[]
  immutableDigest
  redactionPolicy
}

Notification {
  notificationId
  runId
  targetThreadId
  kind: "success" | "blocker" | "approval" | "failure"
  consumedAt?
}
```

No separate project-level “session” object is necessary. `Thread + active interaction + runs` provides the missing semantics.

### Compact state machine

```text
user turn
  -> classify against focused thread's active interaction
     -> continue interaction
     -> capture side note without focus change
     -> clarify continuation vs fresh route
     -> create route decision

route decision
  -> draft/park/handoff
  -> awaiting-approval
  -> approved -> create immutable snapshot -> queued -> running

foreground run:
  running <-> awaiting-user
  running -> blocked | succeeded | failed | cancel-requested -> cancelled
  terminal -> interaction handoff-ready/completed/blocked

child run:
  running -> blocked | succeeded | failed | cancel-requested -> cancelled
  terminal -> artifact + notification
  notification consumption -> explicit merge/reference into current thread
```

Necronomicon’s classification order is preserved: explicit interrupt, side note, pending response, handoff continuation, fresh route, then one focused ambiguity question (`README.md#interaction-state-model`, lines 115-126). Missing capabilities produce bounded fallback offers and require consent before manifest mutation (`README.md#routing-rules`, lines 393-410).

### Invariants

1. Exactly one focused thread per interface; focus changes never mutate any thread or run.
2. At most one nonterminal active interaction and one foreground run per thread.
3. Every run has one immutable launch snapshot. Later messages in any thread are invisible unless an explicit context-update event creates a new snapshot.
4. Every child run has `parentRunId` or, for a direct thread spawn, `rootThreadId + launchInteractionId`; completion never replaces the parent interaction.
5. A route preview cannot create a run. IDE Ergonomics explicitly forbids spawn from preview alone and forbids side nodes from silently changing the active task (`PRODUCT-VIEW.md#pass-conditions`, lines 226-242).
6. A returned artifact is evidence, not memory or truth. It enters a thread only through explicit consume/attach; durable promotion stays with the owning capability.
7. Notifications contain bounded summaries and artifact/blocker handles, never the child’s full prompt/context.
8. Cancellation is per run and propagates to descendants only when explicitly requested; cancelling a parent interaction does not silently cancel detached children.
9. Join means “consume terminal result under a declared policy,” not “copy child history into parent.”
10. Blocked is terminal for that run attempt but resumable: residue must include blocker, last verified state, required owner/input, artifact refs, and prior snapshot ID. Resume creates a new attempt/run ID linked by `resumesRunId`; it does not rewrite history.
11. `TaskWorkspace.id` and `GoalWorkspace.id` may be referenced by a run, but neither substitutes for `runId`.
12. Raw conversation, task logs, and child prompts are not durable memory by default; checkpoints remain redacted, classified evidence (`README.md#checkpoint-and-memory-policy`, lines 349-357).

### Witness trace

1. User is in architecture thread `T-arch`, interaction `I-arch`, foreground conversation continuing normally.
2. “In parallel, prepare a governed subagent-strategy proposal and a Whisper page” creates two route decisions from the same source message.
3. After permission gates, child runs `R-strategy` and `R-whisper` receive distinct immutable snapshots. Each snapshot may share the architecture prefix, but has a different mission, capability owner, allowed scope, return contract, and memory refs.
4. `I-arch` remains the active interaction; neither child changes focus or consumes later architecture turns.
5. User focuses `T-other`. Both children continue; `T-other` classification uses only `T-other.activeInteractionId`.
6. `R-whisper` succeeds. Its artifact surface becomes available and a success notification targets `T-arch`.
7. `R-strategy` blocks. Its notification exposes blocker summary, required user/owner action, and residue handle—not its internal transcript.
8. User returns to `T-arch`. The architecture interaction resumes from its own latest state. The interface shows two notifications.
9. User explicitly consumes the Whisper result; it becomes a cited artifact attachment, not silently inserted conversational history.
10. User inspects the strategy blocker; the original child remains blocked. Resume, if chosen, creates a linked new attempt from an explicitly selected snapshot.

No context bleed occurs because focus, conversational ownership, execution state, and durable intake are separate.

### Failure cases that falsify the model

- A late message in `T-arch` appears in either child without a context-update event.
- Switching to `T-other` pauses, redirects, or reassigns a child run.
- Child success changes `activeInteractionId` or appends its transcript directly to `T-arch`.
- Blocked child state is represented only as notification text and cannot be resumed from cited residue.
- Cancelling `R-strategy` cancels `R-whisper`.
- A task workspace exists and UI claims execution is running although no run lifecycle record exists. Current messaging already distinguishes workspace creation from execution (“No agent execution has started yet”), supporting this boundary (`delegation.ts:582-592`).
- A route card spawns before approval.
- Consuming one result marks all notifications consumed.
- Two foreground runs simultaneously claim the next user turn in one thread.
- Durable memory receives raw child context or secrets without checkpoint classification/redaction.

### Exact fixture ideas

1. **`parallel-two-child-isolation.json`**  
   Seed `T-arch/I-arch`; spawn strategy and Whisper children from message `M42`. Append `M43` after launch. Assert both snapshot digests exclude `M43`, run IDs differ, and `I-arch` is unchanged.

2. **`focus-switch-does-not-reparent.json`**  
   Run both children, switch `focusedThreadId` to `T-other`, add messages there, then complete/block children. Assert parent links and target notification thread remain `T-arch`.

3. **`success-and-blocker-selective-consume.json`**  
   One `succeeded` with artifact, one `blocked` with residue. Consume only success. Assert blocker unread, active interaction unchanged, artifact attached by reference only.

4. **`resume-blocked-new-attempt.json`**  
   Resume blocked strategy child with one approved extra input. Assert new `runId`, `resumesRunId`, new snapshot digest, preserved old blocker and audit trail.

5. **`cancel-sibling-independence.json`**  
   Cancel strategy child while Whisper runs. Assert strategy reaches `cancelled`, Whisper can reach `succeeded`, parent remains active.

6. **`ambiguous-turn-one-question.json`**  
   While `I-arch` awaits an architecture choice, submit a possibly unrelated request. Assert no route/run creation and one “continue or fresh route?” prompt, matching Necronomicon ambiguity policy (`README.md#interaction-state-model`, lines 115-123).

7. **`preview-is-not-execution.json`**  
   Select delegated-run preview but withhold approval. Assert route decision exists, no run/task workspace exists, and permission state remains pending.

8. **`single-global-session-counterexample.json`**  
   Model one global active interaction. Focus `T-other` while `I-arch` awaits input and both children run. Assert the implementation must either misclassify `T-other` as an architecture continuation, overwrite `I-arch`, or suspend unrelated children. Any outcome falsifies the global model.

### Comparison with a single-global-session alternative

A global session can store one active thread, one pending prompt, and a bag of jobs, but it cannot simultaneously answer “which capability owns the next turn?” for multiple threads. Switching threads forces one of three bad choices: overwrite the architecture interaction, treat the other thread as a continuation, or embed per-thread interaction state inside the global session. The third choice merely recreates the proposed model under another name.

Likewise, a global mutable context lets background runs observe focus-dependent conversation changes, creating exactly the bleed in the witness. Adding per-run snapshots and parent links again recreates the proposed model.

Therefore the smallest survivor is **one interface focus projection over project-grouped threads, with one active interaction per thread and independently snapshotted runs**. GoalWorkspace, DelegationPacket, and TaskWorkspace remain useful owned records referenced by runs; they are not collapsed into a global session and are not themselves the missing session fabric.

ORCHESTRATE_RECEIPT
action_id=spawn-0001
dispatch_id=2026-07-28-augmentor-routing-session-fabric-route
run_id=20260729T0145Z-routing-session-fabric-001
wave_id=explorers
step_id=s1
role=session-state-explorer
capability_ref=research
status=pass
artifacts=[arcanum/spells/necronomicon/README.md#interaction-state-model,arcanum/spells/necronomicon/README.md#shared-state,arcanum/spells/necronomicon/README.md#checkpoint-and-memory-policy,arcanum/spells/necronomicon/README.md#routing-rules,projects/ide-ergonomics/PRODUCT-VIEW.md#step-3-show-the-route-menu,projects/ide-ergonomics/PRODUCT-VIEW.md#pass-conditions,../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:1958,../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:1984,../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:2019,../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:2081,../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:2769,../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:2780,../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:2806,../workspace-resonant/2.0.0-alpha/src/core/delegation.ts:39]
validation=pass
blockers=[]
residue=Current ResonantOS contracts do not yet define Run, RouteDecision, ContextSnapshot, Notification, cancellation, join, or resume records; TaskWorkspace is path-only. Proposed model is research, not accepted architecture or implementation authority.
handoff_note=Synthesis should preserve the separation between focus, thread interaction ownership, immutable run context, artifact consumption, and durable memory. The fixture suite should first falsify single-global-session behavior and then prove sibling isolation, selective consumption, cancellation independence, and blocked-run resumption.

## Agent 2 — route-decision-explorer

## Route-decision contract

### 1. Governing model

Augmentor should classify a turn before choosing a capability. Routing has two distinct layers:

1. **Conversation disposition** — what the turn does to the current interaction.
2. **Execution disposition** — who, if anyone, should act and at what lifecycle depth.

This preserves Necronomicon’s canonical precedence:

1. explicit interrupt/command,
2. marked side note,
3. response to an awaiting owner,
4. handoff continuation,
5. fresh route when no interaction is active,
6. one focused clarification when continuation and fresh routing remain plausible.

The active capability interprets responses inside its own contract; Necronomicon/Augmentor owns interaction state and the route ledger.  
[Necronomicon interaction classification: `arcanum/spells/necronomicon/README.md:97-128`]

The resulting `conversation_disposition` is one of:

- `continue`: give the turn to the current `owning_capability`.
- `side_note`: capture without changing the active route.
- `fresh_route`: suspend/record the active interaction and classify anew.
- `clarify`: ask exactly one continuation-versus-new-route question.

After that, `execution_disposition` is one of:

- `inline_answer`: answer directly; no capability run is proportionate.
- `existing_capability_run`: one installed capability clearly owns the request.
- `delegated_background_run`: bounded delegation is justified and its ownership contract is explicit.
- `capability_gap`: no credible installed route exists, or required lifecycle coverage is missing.

A small related blocker may run inline or as one bounded task; a non-blocking aside stays queued, and a broad aside gets one scope question.  
[Necronomicon side-note/unblocker policy: `arcanum/spells/necronomicon/README.md:124-128`]

### 2. `RouteDecision`

```yaml
RouteDecision:
  decision_id: string
  request_digest: string
  interaction:
    active_interaction_id: string | null
    active_owner: capability-id | null
    active_status: awaiting-user | running | handoff-ready | blocked | completed | abandoned | null
    matched_precedence:
      explicit-interrupt | side-note | pending-response |
      handoff-continuation | no-active-interaction | ambiguous
  conversation_disposition:
    continue | side_note | fresh_route | clarify
  execution_disposition:
    inline_answer | existing_capability_run |
    delegated_background_run | capability_gap | none
  interpretation:
    concise_intent: string
    target: string | null
    requested_outcome: answer | artifact | mutation | validation | decision | research
    explicit_capability: capability-id | null
    series_or_parallel_intent: boolean
  candidates:
    - capability_ref: string
      mode: string
      trigger_evidence: [selector]
      installed: boolean
      confidence: high | medium | low
      owner: string
      mutation_policy: read-only | artifact-only | lifecycle-owned
      rejected_reason: string | null
  selected:
    capability_ref: string | null
    mode: string | null
    owner: string | null
  confidence: high | medium | low | block
  ambiguity:
    tied_candidates: [capability-mode]
    material: boolean
    clarification_question: string | null
  offers: [RouteOffer]
  confirmation:
    required: boolean
    reason: capability-add | consequential-choice | delegated-run |
            reusable-artifact | protected-hazard | mutation | none
    owner_gate: string | null
  gap:
    kind: no-match | not-installed | deferred-mode |
          missing-adapter | missing-owner | missing-evidence | null
    escalation: fallback-discover | update-capabilities |
                spellcraft | sigil-development | decision-gate | null
  telemetry_policy: minimal-v1
```

Confidence must retain Necronomicon’s meanings:

- `high`: explicit command, canonical ID, or exact alias.
- `medium`: a selected capability’s trigger/description/mode strongly matches.
- `low`: a credible registry candidate fits but is not selected.
- `block`: no credible selected or fallback route.

Ask one focused question when multiple high/medium routes tie materially. A low-confidence candidate is an offer, never silent execution.  
[Necronomicon route confidence: `arcanum/spells/necronomicon/README.md:413-422`]

Explicit names win, but an explicit command does not bypass that capability’s gates. A sole admissible route is “direct,” not consent or execution.  
[Decision Gate cardinality and consent boundary: `arcanum/arcana/decision-gate/SKILL.md:51-73`]

### 3. `RouteOffer`

```yaml
RouteOffer:
  offer_id: string
  level: easy | test | hardening
  label: string
  route:
    capability_ref: string
    mode: string
    target: string
  outcome: string
  owner: inline | task-session | dispatch-orchestrator |
         experiment-harness | spellcraft | sigil-development
  cost:
    user_attention: none | low | medium | high
    execution_scope: inline | one-bounded-run | multi-run | lifecycle
    persisted_state: [path-or-artifact-kind]
  evidence_ceiling: explanation | one-run-receipt |
                    repeatable-test-evidence | lifecycle-evidence
  prerequisites: [string]
  confirmation_required: boolean
  confirmation_reason: string | null
  visibility: recommended | available | hidden
  hidden_reason: string | null
  risks: [string]
  reusable_effect: none | local-composition | spell-change | sigil-change
```

### 4. Easy, test, and hardening are evidence levels, not cosmetic choices

#### Easy

A genuine option when the result can be produced inline or through one existing capability run, is reversible, has no protected mutation, and does not claim reusable correctness.

- **Owner:** inline answer owner, or one capability such as `task-session`.
- **Cost:** lowest; one response or one bounded run.
- **Evidence ceiling:** explanation or one execution receipt.
- **Recommend:** ordinary questions, one-off transformations, bounded tasks with clear done criteria.
- **Hide:** when risk requires an owner gate, ambiguity is material, the user explicitly asks for repeatability, or the behavior does not exist.
- **Confirmation:** normally no for read-only/inline work; yes for mutation or an owner gate.
- **Composition:** may make a one-off sequence in the current run, but creates no reusable spell authority.

Task Session owns one bounded task/SWU and must not silently turn series intent into one task.  
[`arcanum/arcana/task-session/SKILL.md:32-69`; series routing at `:100-110`]

#### Test

A genuine option when the user needs repeatable evidence against an existing spell/sigil contract: fixture, realistic prompt, bounded run, validation report, or regime loop.

- **Owner:** `experiment-harness`; the target spell/sigil retains semantic ownership.
- **Cost:** harness state, fixtures/prompts, run evidence, validation/reporting.
- **Evidence ceiling:** repeatable behavioral evidence for the current contract.
- **Recommend:** “prove this works,” reproduce a failure, compare regimes, validate reusable behavior.
- **Hide:** for a pure one-off answer, when no reusable contract exists to test, or when the requested change is actually to the contract.
- **Confirmation:** required before mutating/overwriting existing evidence; batch execution must be explicit.
- **Composition:** tests a composition; it does not author or revise the spell/sigil.

Experiment Harness owns testing mechanics only; contract meaning routes to Spellcraft or Sigil Development.  
[`arcanum/arcana/experiment-harness/SKILL.md:47-60,97-99,123-148`]

#### Hardening

A genuine option only when evidence indicates reusable lifecycle work: repeated route misses, repeated composition, contract drift, new phases/gates, or a changed primitive.

- **Owner:** `spellcraft` for reusable multi-sigil workflow composition; `sigil-development` for a changed individual capability contract.
- **Cost:** design/revision, gates, validation, experiment evidence, observability, reflection, and explicit lifecycle review.
- **Evidence ceiling:** lifecycle evidence—not automatic promotion.
- **Recommend:** repeated useful one-off composition, stable cross-run trigger, recurring failure, or required contract change.
- **Hide:** first occurrence without reuse intent/evidence, speculative “maybe useful” behavior, or when a route preset/local composition suffices.
- **Confirmation:** explicit approval before creating or promoting reusable artifacts.
- **Composition distinction:**  
  - one-off composition: ephemeral route, no reusable artifact;  
  - reusable spell: stable workflow goal, triggers, phases, handoffs, gates, failure policy, observability;  
  - changed sigil: the primitive’s own input/output/quality contract changes.

Spellcraft owns spell artifacts; it may compose but cannot redefine a sigil. Reusable spells require experiment evidence.  
[`arcanum/arcana/spellcraft/SKILL.md:31-40,92-138,141-163`]

### 5. Capability-gap escalation

1. Search selected installed capabilities.
2. Inspect installed runtime surfaces and canonical registries.
3. Offer **2–5 credible** fallback sigils/spells with a fit reason.
4. If only one credible fallback exists, offer one; do not pad the menu.
5. If none exists, return `block`.
6. Ask before adding a fallback to the capability manifest.
7. If capability exists but is uninstalled/missing an adapter, route to `update-capabilities`.
8. If behavior does not exist:
   - repeated workflow/composition → `spellcraft`;
   - missing/changed primitive contract → `sigil-development`;
   - consequential choice between alternatives → `decision-gate`.
9. Do not author anything merely because a gap was observed.

[Fallback and lifecycle-gap rules: `arcanum/spells/necronomicon/README.md:393-411`; update flow: `:424-433`]

### 6. Delegation and parallelism

Use background delegation only for a bounded role with exact capability, target, mode, inputs, outputs, mutation policy, and scope. Multi-agent/parallel work additionally needs a validated Dispatch Spec, authorization, execution waves, join policy, gates, and closed receipts. Dispatch Spec validates; the parent orchestrator spawns and joins.  
[`arcanum/formulae/dispatch-spec/SKILL.md:65-101,103-145`; `arcanum/formulae/dispatch-spec/CAPABILITY-BOUND-DELEGATION.md:64-77`]

### 7. Minimal routing telemetry

Persist only fields that can improve later classification:

```yaml
request_digest
active_interaction_state
conversation_disposition
candidate capability-mode tuples
selected tuple
confidence
clarification asked and resolved tuple
fallback used
gap kind
offer level selected
result: pass | flag | block
validation status
user correction: true | false
repeated-pattern key
```

Exclude full prompt prose, chain-of-thought, secrets, incidental content, and redundant capability output. Aggregate repeated misses/corrections before recommending maintenance; repetition is evidence for review, not automatic lifecycle mutation.  
[Necronomicon route record and maintenance signals: `arcanum/spells/necronomicon/README.md:368-376,393-407`]

### 8. Exact fixtures

1. **Correct continuation**  
   Active: `decision-gate`, `awaiting-user`, options A/B. Turn: “B, because rollback matters.”  
   Expect: `continue`, owner `decision-gate`, `high`, no offers, no fresh route.

2. **Explicit fresh route**  
   Active: Invoke interview. Turn: “Pause this. Run task-session on SWU-12.”  
   Expect: record paused interaction; `fresh_route`; exact `task-session`; `high`; owner gates preserved.

3. **Side note**  
   Active: research. Turn: “For later: compare SQLite too.”  
   Expect: `side_note`, no execution, current research continues.

4. **Ambiguous**  
   Active: awaiting API-scope answer. Turn: “Could we use OAuth instead?”  
   Expect: `clarify`; one question asking whether this answers/reframes current scope or starts a new route.

5. **Inline easy**  
   No active interaction. Turn: “Explain the difference between a sigil and spell from these cited files.”  
   Expect: `inline_answer`, easy recommended, no capability mutation or test offer.

6. **Unsupported capability**  
   Turn: “Run a reusable deployment-canary capability,” with no credible selected/registry match.  
   Expect: `capability_gap`, `block` or honest fallback menu; never invent a capability; escalate to Spellcraft only if reusable workflow authoring is desired.

7. **Repeated request**  
   Three prior one-off routes compose the same capabilities with the same trigger. Turn repeats it.  
   Expect: easy remains runnable; hardening becomes available/recommended; explicit approval required before Spellcraft lifecycle work.

8. **Risky request**  
   Turn: “Use easy mode to publish and charge the account.”  
   Expect: easy hidden; protected owner gates required; `decision-gate` cannot manufacture consent.

9. **Test request**  
   Turn: “Run this spell against low, medium, and complex fixtures and report drift.”  
   Expect: test recommended; `experiment-harness`; confirmation for batch/overwrite as applicable; no contract rewrite.

10. **Parallel request**  
    Turn: “Have three agents independently modify the same spell now.”  
    Expect: no immediate spawn; delegated route requires authorization and non-overlapping scopes or sequentialization; Spellcraft remains lifecycle owner; overlapping concurrent writes block.

11. **One-off composition**  
    Turn: “For this answer only, inventory the context then summarize it.”  
    Expect: easy/local one-off composition; no Spellcraft artifact.

12. **Changed sigil**  
    Turn: “Make Context Builder always include web sources.”  
    Expect: hardening via `sigil-development`, not Spellcraft; test lane follows for behavioral proof.

ORCHESTRATE_RECEIPT
action_id=spawn-0002
dispatch_id=2026-07-28-augmentor-routing-session-fabric-route
run_id=20260729T0145Z-routing-session-fabric-001
wave_id=explorers
step_id=s1
role=route-decision-explorer
capability_ref=research
status=pass
artifacts=[
  "arcanum/spells/necronomicon/README.md:97-143",
  "arcanum/spells/necronomicon/README.md:368-433",
  "arcanum/formulae/dispatch-spec/SKILL.md:65-145",
  "arcanum/formulae/dispatch-spec/CAPABILITY-BOUND-DELEGATION.md:64-77",
  "arcanum/arcana/spellcraft/SKILL.md:31-163",
  "arcanum/arcana/experiment-harness/SKILL.md:47-148",
  "arcanum/spells/invoke/README.md:20-126",
  "arcanum/arcana/task-session/SKILL.md:32-110",
  "arcanum/arcana/decision-gate/SKILL.md:51-91",
  "arcanum/registry/SIGILS.md:7-43",
  "arcanum/registry/SPELLS.md:7-20"
]
validation=pass
blockers=[]
residue="Confidence thresholds remain categorical rather than numerically calibrated; easy/test/hardening are proposed route-offer semantics and require owner acceptance before becoming canonical."
handoff_note="Synthesis should preserve classification-before-execution, treat easy/test/hardening as materially different evidence/lifecycle offers, and keep capability addition, delegation, and reusable artifact work explicitly gated."

## Agent 3 — human-interface-explorer

## Human-interface finding

Augmentor should feel like one conversational shell with five nested objects whose boundaries remain visible:

```text
shell
  └─ project
      └─ thread
          └─ interaction
              ├─ foreground response
              └─ isolated child/background runs → artifacts
```

The interface must not pretend these are one transcript. A thread is the durable conversational context; an interaction is the currently addressed user intent; a run is an execution attempt with its own lifecycle; an artifact is a durable output linked back to its run. This preserves the governing restraint floor: preview is not execution, a side artifact does not switch the active route, and a handoff is not proof of completed work (`projects/ide-ergonomics/UNIFIED-PRODUCT-VIEW.md#the-coordinates`; `projects/ide-ergonomics/PRODUCT-VIEW.md#how-it-works`).

Current ResonantOS already provides useful thread primitives: projects and unprojected chats, pinned chats, recency labels, branching, moving, renaming, and deletion (`../workspace-resonant/2.0.0-alpha/src/modules/chat/StrategistChatRail.tsx:281-500`; `#chat-history` at lines 626-683). It also preserves message-level branching and archive citations (`StrategistChatRail.tsx:688-759`). But execution remains effectively foreground-global: `sendStrategistMessage` claims one active-thread token and rejects another send while `chatBusy` is true (`../workspace-resonant/2.0.0-alpha/src/App.tsx:1224-1269`), while the only live run card is rendered inside the active conversation (`StrategistChatRail.tsx:762-796`). A true multi-run experience therefore needs a run registry and per-thread/run projections, not merely more chat-history controls.

## Progressive-disclosure journeys

### 1. Ordinary free-form routing

1. User types normally; no mode or tool selection is required.
2. Augmentor answers in the transcript and, only when a consequential route exists, inserts a compact route card immediately after the user turn:
   `Recommended: continue here · Why: same objective and context · Boundary: no background work`.
3. The collapsed card exposes one primary action and “Why this route?”.
4. Expanding it reveals detected intent, context sources, owner, expected result, permission state, alternatives, and prohibited effects.
5. Low-risk, obvious continuation requires no extra confirmation. Anything that creates a run or artifact requires an explicit action.

This instantiates the bounded conversation-transition card, not a generic launcher (`PRODUCT-VIEW.md#what-the-product-is`; `#step-3-show-the-route-menu`).

### 2. Continue versus start fresh

After ambiguity such as “now investigate the renderer,” show an inline two-choice card:

- **Continue this thread** — inherits this thread’s selected context and summary.
- **Start fresh** — creates a sibling thread with a preview of the context that will be copied.

The recommendation must name its reason: same objective, strong referent continuity, different privacy boundary, conflicting instruction, or likely context contamination. “Start fresh” never silently activates the new thread; creation produces a notification with **Open thread** and leaves the current composer/focus intact. Branch-from-message is the natural current-source precedent (`StrategistChatRail.tsx:725-727`).

### 3. Background subagent-strategy proposal

“Have agents explore this” produces a **proposal card**, not a spawn:

- purpose and why delegation may help;
- proposed roles/lanes;
- context supplied to each lane;
- expected receipts;
- isolation and forbidden scopes;
- join/close policy;
- estimated attention cost;
- **Review proposal**, **Edit**, **Run after approval**, **Keep here**.

The product evidence explicitly requires role cards, receipts, join policy, permission, and no spawn from preview alone (`PRODUCT-VIEW.md#mvp-shape`; `ERGONOMICS-OPPORTUNITIES.md#4-subagent-fanout-preview`). After approval, the run leaves the transcript and enters the run tray; the transcript retains a concise immutable launch receipt.

### 4. Whisper page as a child artifact run

“Turn this into a Whisper page” opens an artifact-run preview:

- source interaction and selected messages;
- target type: Whisper page;
- proposed title/audience;
- context included/excluded;
- output location/owner;
- **Create isolated draft**.

On launch, place a small child-run chip beneath the source message and a run-tray row. Completion opens an **Artifact** tab without replacing the chat. The tab header shows `Draft`, source thread, source interaction, run receipt, and unresolved residue. Editing or promotion remains a later owner action. This follows the knowledge-reference rule that reusable handles retain source, freshness, authority boundary, and residue (`knowledge-entry-references/SPEC.md#6-popup-contract`; `#8-owner-safe-actions`).

### 5. Switch threads while runs continue

Switching threads changes only the center transcript and composer. Running work remains in a persistent tray collapsed to one line: `2 running · 1 needs attention`. Each thread row gets at most one semantic badge: running count, needs-attention, or completed-unseen. No automatic return to a finishing thread.

Opening the tray shows run name, parent thread, phase, elapsed time, cancellability, and next human action. The current in-transcript elapsed phase display is a good per-run atom (`StrategistChatRail.tsx:763-795`), but it must be projected globally rather than tied to `chatBusy`.

### 6. Completion, blocker, clarification

Use three interruption levels:

- **Completion:** quiet tray transition and thread badge; one polite notification, auto-collapsed.
- **Blocker:** notification rail item with the blocking fact, safe work preserved, and **Open run**.
- **Clarification required:** one focused question with **Answer here**, **Open parent thread**, and **Defer**; never steal composer focus.

Aggregate repeated events from one run. A memo-like item must retain addressee, status, source refs, open call, boundary, and next move rather than become an unowned task (`teammate-handoff-memos/SPEC.md#6-window-states`; `#7-actions`). `aria-live="polite"` is appropriate for state changes, as already used for activity/run status (`StrategistChatRail.tsx:596-603`, `:763`); urgent announcements should be reserved for destructive failure or imminent loss.

### 7. Inspect route rationale

“Why?” expands the local route card, never opens a global diagnostics dashboard. Show:

- interpreted intent;
- matched capability and fit: strong/acceptable/weak;
- context inherited;
- evidence/freshness;
- why alternatives ranked lower;
- effect and non-effect;
- confirmation requirement;
- “Report wrong route.”

Explainable matching is already a pass condition for knowledge references (`knowledge-entry-references/SPEC.md#9-ranking-hints`; `#10-pass-conditions`).

### 8. Weak fit: easy, test, hardening

When no capability fits strongly, do not fabricate certainty. Offer:

- **Easy** — one-off, reversible answer/action in this thread; minimal setup; no reusable capability claim.
- **Test** — isolated fixture/prototype run with explicit success criteria; recommended when behavior is uncertain.
- **Hardening** — propose governed reusable capability work; highest ceremony and never the default for a one-off need.

Each option previews time/attention, artifacts, validation, reversibility, and owner. Recommend Test when uncertainty is material but fixtureable; Hardening only when repetition, reuse, risk, or lifecycle ownership justifies it. Ask one question at a time and always include “Explain more,” matching the Connective choice contract (`connective-task-manager/SPEC.md#8-interactive-choice-contract`; `#7-recommendation-model`).

## Surface allocation

| Surface | Only what belongs there |
|---|---|
| Chat transcript | User/assistant turns; compact route decision; immutable launch/completion/blocker receipts; child-run link. No streaming background logs. |
| Route card | Interpretation, recommendation, rationale, alternatives, boundary, permission, expected receipt. Local to one interaction. |
| Thread list | Title, project, recency, pin, and one aggregated semantic status/count. No step-level run telemetry. |
| Run tray | All active/recent runs across threads; parentage, phase, elapsed time, cancel/pause support, needs-attention, resulting artifact. |
| Artifact tab | Draft/output body, provenance, status, source refs, validation, residue, owner actions. |
| Notification rail | Unseen completion, blocker, clarification, and failure events; grouped by run/thread with direct next action. |

## Keyboard and accessibility contract

- Full operation by keyboard; logical tab order follows shell → thread list → transcript → composer → tray/notifications.
- `Ctrl/Cmd+K` may search threads/actions but must not become a tool drawer. `Ctrl/Cmd+Shift+R` opens the run tray; `Ctrl/Cmd+Shift+N` opens notifications; `Esc` closes the topmost disclosure and restores prior focus.
- Route choices use a radiogroup or ordinary buttons with visible names; menus support arrows, Home/End, Enter/Space, and Esc.
- Dialogs trap focus, carry an accessible name/description, and restore focus to their trigger. The current agent picker has dialog semantics but needs explicit modal/focus management beyond `role="dialog"` (`StrategistChatRail.tsx:606-623`).
- Status cannot rely on color, animation, or icon alone. Every badge has text/accessible name; reduced-motion stops pulses while preserving phase.
- New background events never move focus. Polite live regions announce aggregated state once; clarification exposes the question in the notification rail and thread.
- Resizing must have a keyboard alternative because the current separator is pointer-only (`StrategistChatRail.tsx:521`).
- Preserve Enter-to-send and Shift+Enter newline (`StrategistChatRail.tsx:813-823`), but route-card shortcuts must not fire while typing or using IME composition.

## Attention budget

- At most one expanded route card per interaction.
- At most one foreground live status card; all other work collapses into the run tray.
- One notification per run state transition; coalesce progress chatter and repeated blockers.
- Completion does not toast repeatedly or reopen a thread.
- Clarification is the only ordinary state eligible for a persistent unread badge.
- Show no more than three route choices initially: recommended, best alternative, “More options.”
- Human attention indicators must be opt-in, reviewable, and allowed to remain unknown (`connective-task-manager/README.md#boundaries`).

## Anti-patterns

Reject:

- tool/capability drawers that require the user to know the ontology;
- dashboards that display state without a bounded next action;
- hidden inherited context or invisible context copying;
- one global “busy” state once concurrency exists;
- streaming background logs into the active transcript;
- silently changing thread, task, model, owner, or artifact tab;
- treating a proposal, handoff, draft, or completion notice as execution/approval proof;
- notification floods, duplicate live announcements, or status encoded only by motion/color;
- turning every side thought into a thread or every one-off into capability hardening.

These follow the recorded failure conditions: no generic launcher, no dashboard without a next action, no unclear owner/boundary, and no silent active-route switch (`PRODUCT-VIEW.md#fail-conditions`; `ERGONOMICS-OPPORTUNITIES.md#anti-patterns`).

## Browser-testable fixtures

1. **Same-intent continuation:** enter a pronoun-dependent follow-up; assert route card recommends Continue, rationale references the prior interaction, no thread is created before action.
2. **Fresh isolation:** enter a conflicting/new objective; choose Start fresh; assert copied-context preview is shown, current focus/thread remains unchanged until Open thread.
3. **Delegation proposal:** request parallel agents; assert zero runs before approval; expanded card exposes roles, receipts, scopes, join policy; approval creates isolated run rows.
4. **Whisper child:** launch from a selected assistant message; assert parent interaction ID on run and artifact, transcript unchanged except child chip, artifact opens in a tab.
5. **Concurrent switch:** start two fixture runs in different threads, switch twice; assert both clocks advance, composers remain thread-local, no auto-navigation on completion.
6. **Notification coalescing:** emit ten progress events plus completion; assert one completion rail item, one polite announcement, zero transcript log spam.
7. **Blocker/clarification:** emit blocker then one question; assert preserved partial artifact, persistent needs-attention badge, focus unchanged, Answer here routes to the correct run.
8. **Weak fit:** return fit=`weak`; assert Easy/Test/Hardening consequences differ, Test is recommended for fixtureable uncertainty, no execution before selection.
9. **Rationale provenance:** expand Why; assert capability, evidence freshness, inherited context, alternative ranking, and prohibited effects are visible.
10. **Accessibility:** keyboard-only create/switch/inspect/cancel flow; axe scan; dialog focus return; live-region event-count assertions; reduced-motion snapshot; keyboard resize.
11. **Context isolation:** plant a secret marker in Thread A, run Thread B, assert B request/context/artifact and notifications contain no marker.
12. **Silent-switch guard:** complete a background run while typing in another thread; assert active thread, selection, composer value, scroll, and focus are unchanged.

ORCHESTRATE_RECEIPT
action_id: spawn-0003
dispatch_id: 2026-07-28-augmentor-routing-session-fabric-route
run_id: 20260729T0145Z-routing-session-fabric-001
wave_id: explorers
step_id: s1
role: human-interface-explorer
capability_ref: research
status: pass
artifacts:
  - projects/ide-ergonomics/PRODUCT-VIEW.md#what-the-product-is
  - projects/ide-ergonomics/PRODUCT-VIEW.md#how-it-works
  - projects/ide-ergonomics/PRODUCT-VIEW.md#fail-conditions
  - projects/ide-ergonomics/UNIFIED-PRODUCT-VIEW.md#the-coordinates
  - projects/ide-ergonomics/ERGONOMICS-OPPORTUNITIES.md#4-subagent-fanout-preview
  - projects/ide-ergonomics/ERGONOMICS-OPPORTUNITIES.md#anti-patterns
  - projects/ide-ergonomics/knowledge-entry-references/SPEC.md#6-popup-contract
  - projects/ide-ergonomics/knowledge-entry-references/SPEC.md#8-owner-safe-actions
  - projects/ide-ergonomics/knowledge-entry-references/SPEC.md#9-ranking-hints
  - projects/ide-ergonomics/teammate-handoff-memos/SPEC.md#6-window-states
  - projects/ide-ergonomics/teammate-handoff-memos/SPEC.md#7-actions
  - projects/ide-ergonomics/connective-task-manager/SPEC.md#7-recommendation-model
  - projects/ide-ergonomics/connective-task-manager/SPEC.md#8-interactive-choice-contract
  - ../workspace-resonant/2.0.0-alpha/src/App.tsx:1224
  - ../workspace-resonant/2.0.0-alpha/src/modules/chat/StrategistChatRail.tsx:281
  - ../workspace-resonant/2.0.0-alpha/src/modules/chat/StrategistChatRail.tsx:626
  - ../workspace-resonant/2.0.0-alpha/src/modules/chat/StrategistChatRail.tsx:762
validation: pass
blockers: []
residue:
  - Current ResonantOS run state is foreground-global and cannot yet substantiate concurrent background-run behavior.
  - No accepted contract yet defines interface/project/thread/interaction/run/artifact/notification identities or easy/test/hardening thresholds.
  - Existing pointer-only rail resize needs a keyboard equivalent.
handoff_note: Use these journeys and fixtures to define the cross-lane state contract; preserve the current thread/history primitives, replace global busy projection with per-run state, and validate no-focus-steal plus context isolation before claiming the one-interface experience supports concurrency.

## Agent 4 — consumer-runtime-explorer

## Consumer runtime exploration — Turing, Alan

### Scope and upstream verification

The inspected checkout is `../workspace-resonant/2.0.0-alpha` on local `dev`, seven commits behind `origin/dev`.

`git diff --name-status dev..origin/dev` shows that all seven upstream commits affect only:

- `.github/workflows/agent-control-live.yml`
- `browser-first/resonantos-side-panel-extension/src/content.js`
- extension approval/browser-page-action libraries
- `browser-first/test/*`
- `docs/STATUS.md`
- `docs/reference/CAPABILITY_MATRIX.md`
- `package.json`

No upstream commit changes the requested `src/core`, `src/modules/chat`, `src/App.tsx`, or `public/addons/augmentor-chat.json` scope. The local bytes are therefore a valid basis for this scoped analysis, although any eventual implementation branch should first advance from current `origin/dev`.

The worktree status reports only `## dev...origin/dev [behind 7]`; no scoped dirty files were reported.

### Current-versus-missing matrix

| Capability | Status | Current evidence | Missing boundary |
|---|---|---|---|
| Multi-thread management | **Implemented** | `ConversationThread[]`; create, select, rename, pin, move, delete actions; history UI; state persistence and normalization preserve user-created threads. | No durable per-thread execution/session object distinct from transcript state. |
| Project management | **Implemented** | `ChatProject[]`; create, rename, pin, delete; threads carry optional `projectId`; project history UI. | Projects are organizational containers only: no project-owned routing policy, context, run queue, or artifact index. |
| Thread branching | **Implemented** | Whole-thread and branch-from-message actions clone messages, remap IDs, append transcript events, and copy compact memory. | No explicit durable ancestry fields; provenance is encoded in event payload/summary rather than queryable parent-child links. |
| Project branching | **Implemented** | Clones project and all member threads. | Does not copy compact memory for project-cloned threads and records no project ancestry. This differs materially from thread branching. |
| Context compaction | **Implemented** | Manual and automatic compaction; compact state enters system prompt; hard-stop threshold; editable compact memory; transcript events; branch propagation for a thread. | No router-facing compact-context contract; project branch gap noted above. |
| Active run handling | **Implemented, single global run** | `claimChatRun` synchronously guards a single mutable token; controller emits transient phase/events and ignores late results with `isRunCurrent`. | Run state is React-local/transient, not persisted; one active run blocks all threads, projects, and background jobs. |
| Abort | **Implemented conditionally** | Stop clears token, calls `abortProviderServiceChatCompletion`, appends an interrupted assistant message/event, and ignores late completion. Adapter contracts expose `supportsAbort`. | No persisted cancellation state or restoration reconciliation; transport abort is capability-dependent. |
| Goal workspaces | **Implemented** | Durable typed goals with phase, steps, blockers, artifacts, memory refs, cost policy, allowed agents/tools, delegation refs; normalization/migration/status helpers. `/goal` and `/status` use them. | Goal execution remains command-driven; no generic router decision automatically creates/attaches/resumes a goal. |
| Delegation | **Implemented for bounded targets/workspaces** | Typed packets, validation, target discovery from enabled manifests plus native Engineer, bridge workspace create/read/finish, explicit Hermes/OpenCode/Engineer paths. | No general session scheduler, fan-out graph, or background dispatch lifecycle. Several paths explicitly create a workspace while stating execution has not started. |
| Artifacts | **Implemented in goal/delegation contracts** | `GoalArtifact`, `ArtifactReturn`, verification evidence, residual risks, workspace finish payloads. | No unified session-level artifact registry or notification projection. Avoid creating one in the router. |
| Route classification | **Partial implementation** | Provider/model execution routing is mature; `WorkloadClass` and strategies exist. User intent interception supports explicit slash commands and a narrow natural-browser parser. | No general semantic classification into answer/tool/goal/delegation/background/session routes, no confidence/reason record, and no router contract. |
| Background concurrency | **Design-only / absent at runtime** | Types mention `WorkspaceBehavior: "background"`, `WorkloadClass: "background"`, background-task-monitor surfaces, and delegation monitor capabilities. | No concurrent run registry, per-thread run locks, scheduler, queue, concurrency ceiling, or background lifecycle implementation in inspected chat runtime. |
| Parent-child links | **Absent as a general model** | Goal-to-delegation refs and transcript source-thread payloads provide local associations. | Threads, projects, runs, and routed sessions have no normalized `parentId`/`rootId`/relation contract. |
| Notifications | **Fixture-only** | Augmentor manifest requests `notifications` with degrade behavior. | No inspected notification state, producer, restoration, or UI wiring. |
| Restoration | **Implemented for durable shell state; absent for live runs** | `persistState` writes through the host or `localStorage`; `hydrateState` builds defaults, normalizes old state, rebases manifests, preserves extra threads, compact memory, transcript ledger and goals. | No restoration of in-flight runs, queues, abort controllers, transient run events, or notification state. A reload turns execution into unclassified residue. |
| Floating chat | **Fixture/design mismatch** | Manifest advertises a floating surface; App has detach behavior. | `openFloatingChatWindow` throws because floating chat is outside the browser-first Chrome extension alpha. Treat manifest prose as catalog intent, not current runtime proof. |

### Smallest host-owned integration seam

The narrowest correct seam is in `executeChatTurn`, after the outgoing text and active thread are known but before `parseAugmentorCommand`, `parseNaturalBrowserIntent`, provider diagnostics, archive retrieval, or provider transport.

That location already owns the mutually exclusive choice between deterministic host command handling and model execution. Add one pure, host-owned classifier there. It should produce a typed decision using ResonantOS state and existing registries, then dispatch into existing functions:

1. explicit commands remain first-priority and backward compatible;
2. router classification handles otherwise-unclassified input;
3. provider chat remains the fail-safe fallback;
4. existing goal, delegation, browser, provider-route, artifact, and persistence mechanisms remain authoritative.

The Necronomicon contribution should be compiled knowledge—rules, labels, examples, or a versioned decision table—converted at build/admission time into a public neutral router fixture. Do not import its private session directory at runtime. Do not let it own agents, tools, goals, workspaces, or provider routes. The host resolves classifier output against `ResonantShellState`, enabled manifests, `delegationTargetsForState`, goal helpers, and provider routing. This avoids a second registry.

### Additive contract proposal

Add narrowly scoped types, preferably beside chat contracts:

```ts
type ChatRouteKind =
  | "conversation"
  | "goal-command"
  | "delegation"
  | "browser-command"
  | "status"
  | "clarification";

interface ChatRouteDecision {
  kind: ChatRouteKind;
  classifier: "explicit-command" | "host-rule-v0";
  ruleId: string;
  confidence: "deterministic" | "high" | "low";
  rationale: string;
  targetAgentId?: string;
  goalId?: string;
  delegationTargetId?: string;
  requiresConfirmation: boolean;
}
```

Pure functions:

```ts
classifyChatRoute(input: {
  text: string;
  thread: ConversationThread;
  state: ResonantShellState;
  manifests: AddOnManifest[];
}): ChatRouteDecision;

validateChatRouteDecision(
  decision: ChatRouteDecision,
  state: ResonantShellState,
  manifests: AddOnManifest[],
): { valid: boolean; reason?: string };

executeHostChatRoute(
  decision: ChatRouteDecision,
  existingControllerContext: ...
): Promise<"handled" | "fallback-to-conversation">;
```

Optional additive durability, only after v0 proof:

```ts
interface RoutedChatEvent {
  id: string;
  threadId: string;
  createdAt: string;
  decision: ChatRouteDecision;
  outcome: "handled" | "fallback" | "blocked";
}
```

Append that to the existing transcript ledger rather than creating a router registry. Parent-child support should later be additive optional fields such as `parentThreadId`, `rootThreadId`, and `branchedFromMessageId`, migrated from existing `thread-branched` transcript evidence where unambiguous.

### Migration posture

- Preserve all current slash-command parsing exactly.
- Run semantic host rules only when explicit parsing returns no command.
- Default unknown/low-confidence input to ordinary conversation or a clarification response; never silently delegate.
- Require the existing human-approval rules for delegation and risky actions.
- Add optional fields and `?? []` normalization; do not change existing persisted required shapes in v0.
- Keep current provider/model routing downstream of classification.
- Fix project-branch compact-memory copying separately or alongside ancestry migration, with a focused regression test.
- Rebase the implementation branch onto the seven upstream commits before coding; `package.json` changed upstream even though runtime sources did not.

### v0 browser witness

A single browser-visible witness can prove the seam without background execution:

1. Open Augmentor chat.
2. Enter: `Research the current provider fallback behavior and return a cited summary.`
3. Router shows a small preflight card: `Suggested route: delegation / research`, target, reason, and `Review task`.
4. No task executes yet.
5. Human confirms.
6. Existing delegation packet/workspace creation runs.
7. Chat displays the existing “workspace created; execution has not started” result and the Delegation workspace shows the packet.
8. Reload the browser.
9. The chat, route transcript event, goal/delegation ref if present, and workspace link restore; no in-flight execution is claimed.

This demonstrates classification, host validation, approval, reuse of the existing delegation authority, persistence, and honest lifecycle semantics without pretending concurrency exists.

### Exact tests to add

Unit tests:

- `src/modules/chat/chat-route-classifier.test.ts`
  - explicit `/goal`, `/delegate`, `/browser`, `/status` retain precedence;
  - deterministic research phrase produces delegation suggestion;
  - ambiguous request produces conversation/clarification;
  - disabled target fails validation;
  - classification cannot bypass approval;
  - classifier references existing target IDs only.
- `src/modules/chat/controller.test.ts`
  - classified route never calls provider before confirmation;
  - confirmed route calls existing task-workspace creation once;
  - invalid/stale decision falls back safely;
  - explicit commands remain byte-for-behavior compatible;
  - late classifier result cannot mutate after run token invalidation.
- `src/core/runtime.test.ts`
  - older persisted state hydrates without routed events;
  - routed transcript events survive JSON round trip;
  - no transient active run is falsely restored.
- `src/modules/chat/thread-controller.test.ts` (new focused file)
  - project branching copies/remaps compact-memory state;
  - ancestry fields are set for thread, message, and project branches;
  - deleting a parent does not delete descendants.
- Extend `src/modules/chat/run-guard.test.ts`
  - document and lock the current global single-run behavior;
  - if per-thread concurrency is later introduced, prove same-thread exclusion and different-thread allowance separately.

Browser/component tests in `src/App.test.tsx`:

- suggestion card appears for the v0 research phrase;
- dismissal performs no delegation;
- confirmation creates exactly one workspace and shows honest non-started status;
- reload restores the durable route/delegation evidence;
- unavailable target renders blocked reason;
- ordinary chat still streams normally;
- stop during downstream provider fallback aborts and ignores late reply.

Run the repository’s required shared React/TypeScript checks for implementation: `npm test -- --run` and `npm run build`. Because the acceptance witness is browser-visible, also run the appropriate browser-first test path and capture live Chrome proof; unit/component rendering alone is not a browser witness.

### Compatibility and product risks

- A semantic classifier can steal normal conversation turns; explicit precedence and conservative fallback are essential.
- Classification must not become authority: enabled capabilities, target registry, approvals, provider route, and workspace bridge must revalidate every decision.
- Persisting an “active” classifier/run state could fabricate restoration; persist decisions/outcomes, not in-memory execution.
- Global run locking prevents the promised session fabric from being concurrent; changing it prematurely risks cross-thread state races because controller callbacks still close over an active thread snapshot.
- Thread/project cloning currently relies on timestamp IDs and copied objects; ancestry and compact-memory remapping need collision and stale-reference tests.
- Manifest claims for notifications, floating windows, and background monitoring exceed inspected runtime implementation and must not be used as readiness evidence.
- Private Necronomicon session schemas will drift and may leak private semantics. Only admit a minimal versioned, public-neutral rule artifact at the host boundary.
- Upstream `package.json` changes mean test-command behavior may differ after updating even though scoped source behavior does not.

No files were edited and no tests were executed; validation here is read-only source, test-inventory, and Git-scope inspection.

ORCHESTRATE_RECEIPT  
action_id=spawn-0004  
dispatch_id=2026-07-28-augmentor-routing-session-fabric-route  
run_id=20260729T0145Z-routing-session-fabric-001  
wave_id=explorers  
step_id=s1  
role=consumer-runtime-explorer  
capability_ref=research  
status=pass  
artifacts=[public/addons/augmentor-chat.json,src/App.tsx,src/App.test.tsx,src/core/contracts.ts,src/core/chat.ts,src/core/goal-workspace.ts,src/core/goal-workspace.test.ts,src/core/delegation.ts,src/core/delegation.test.ts,src/core/runtime.ts,src/core/runtime.test.ts,src/modules/chat/thread-controller.ts,src/modules/chat/augmentor-commands.ts,src/modules/chat/augmentor-commands.test.ts,src/modules/chat/chat-route-request.ts,src/modules/chat/chat-route-request.test.ts,src/modules/chat/run-guard.ts,src/modules/chat/run-guard.test.ts,src/modules/chat/controller.ts,src/modules/chat/controller.test.ts,src/modules/chat/StrategistChatRail.tsx,git:dev..origin/dev]  
validation=pass  
blockers=[]  
residue=Implementation must begin from updated origin/dev; background concurrency, general ancestry, notifications, and live-run restoration remain absent; project branching does not propagate compact memory.  
handoff_note=Integrate a conservative pure host classifier immediately before existing command/provider dispatch in executeChatTurn, resolve decisions through existing host registries and approval gates, append evidence to the transcript ledger, and prove one confirmation-gated browser-visible delegation witness before adding concurrency.
