## Augmentor routing and multi-session fabric — cited synthesis

**Product thesis:** Augmentor should be one conversational shell that classifies each turn against a thread-owned interaction, previews consequential routes before execution, and runs explicitly approved work in independently snapshotted foreground or child runs whose artifacts and notifications never silently rewrite conversation or memory.

### Evidence status and freshness

The synthesis reconciles four distinct explorer roles, each preserved once in `research.md`. The ResonantOS analysis was rechecked against the local `dev` checkout: it remains seven commits behind `origin/dev`, but the seven upstream commits do not touch the load-bearing `src/core`, `src/modules/chat`, `src/App.tsx`, or Augmentor manifest sources. `package.json` did change upstream, so implementation must update before relying on test-command behavior. This is source analysis and proposed architecture, not accepted design or runtime proof. [Consumer explorer, `research.md` §“Scope and upstream verification”; current `git:dev..origin/dev`]

### Current versus missing

| Concern | Current source-backed state | Missing target boundary |
|---|---|---|
| Shell/focus | Active thread is a UI preference, separate from thread data. [`contracts.ts:2806-2822`] | Durable shell projection for visible surface and unread status. |
| Projects/threads | `ChatProject` groups threads; `ConversationThread` owns identity, workspace/channel/project binding, summary, and messages. [`contracts.ts:2769-2786`; Human-interface explorer] | Thread-owned active interaction, run references, explicit ancestry. |
| Interaction routing | Necronomicon defines interaction owner/status, pending prompt, continuation policy, handoff and side notes, plus classification precedence. [`arcanum/spells/necronomicon/README.md:97-128`; Route explorer] | Public-neutral host contract and durable route-decision evidence. |
| Current execution | One mutable `activeChatRunTokenRef` blocks another run globally; live events are transient and capped at ten. [`run-guard.ts:5-28`; `App.tsx:1224-1269`; `controller.ts:194-206`] | Per-thread foreground lock, child-run registry, scheduler and concurrency ceiling. |
| Goals/delegation | Durable goals already contain phases, blockers, artifacts and delegation refs; delegation packets already bound mission, context, memory, scope, approval, verification and return protocol. [`contracts.ts:1958-1982,2019-2105`; `delegation.ts:39-96`] | Generic parent-child run lifecycle, cancellation, join and resume. |
| Task workspace | Paths and packet linkage exist; the UI truthfully says workspace creation is not execution. [`contracts.ts:1984-2002`; `delegation.ts:582-592`] | Never substitute workspace existence for a running run. |
| Persistence/restoration | Shell state persists and normalizes through host storage or `localStorage`. [`runtime.ts:1369-1381,1458-1477`] | No restoration/reconciliation of running work, queues, notifications, or cancellation. |
| Routing | Slash commands and narrow browser intent route before provider chat. [`controller.ts:238-275`; Consumer explorer] | General conversation/execution classifier with confidence, alternatives, and gap behavior. |
| Artifacts/notifications | Goal/delegation artifacts exist; notification capability is manifest intent only. [`contracts.ts:2097-2110`; `augmentor-chat.json:56`] | Run-linked artifact projection and coalesced notification state; avoid a competing artifact authority registry. |
| Floating/background claims | Manifest advertises floating chat/background-related intent. | Floating chat currently throws; background concurrency is absent. [`runtime.ts:1383-1385`; Consumer explorer] |

### Non-collapsing state model

```text
ShellInterface
  -> focusedProjectId?, focusedThreadId, focusedSurface
Project
  -> organizational grouping only
Thread
  -> transcript, summary, default agent, activeInteractionId?, foregroundRunId?
Interaction
  -> owningCapability, mode, pending user contract, continuation policy, status
RouteDecision
  -> immutable interpretation, candidates, selection/offer, permission and gap
Run
  -> parentRunId?, rootThreadId, routeDecisionId, immutable ContextSnapshot
     -> foreground | child; lifecycle; join policy; artifacts; blockers
Artifact
  -> output + provenance + validation + residue; explicitly consumed by reference
Notification
  -> bounded projection of a run transition, targeted to its parent thread
Memory
  -> outside live hierarchy; only classified/redacted checkpoints or accepted artifacts enter
```

The key invariants are: one focused thread per shell; at most one nonterminal foreground conversational owner per thread; every run receives an immutable launch snapshot; focus changes never reparent or pause work; child completion never changes `activeInteractionId`; an artifact is evidence, not truth or memory; notifications carry handles and bounded summaries, not child context; join consumes a declared result rather than copying history; blocked attempts remain immutable and resume through a new run linked by `resumesRunId`. [Session-state explorer; `necronomicon/README.md:314-357`; IDE restraint floor, `UNIFIED-PRODUCT-VIEW.md:87-88`]

### Turn-classification order

1. Explicit interrupt, stop, capability command, or clear topic switch.
2. Marked side note: capture without changing focus.
3. Response to the active owner when `awaiting-user`.
4. Continuation to a declared handoff target.
5. Fresh classification when no active interaction exists.
6. If continuation and fresh routing both remain plausible, ask exactly one focused “continue here or start fresh?” question.
7. Only after conversation disposition is settled, select execution disposition: `inline_answer`, `existing_capability_run`, `delegated_background_run`, `capability_gap`, or `none`.

This preserves current slash-command precedence and prevents semantic routing from stealing ordinary conversation. [`necronomicon/README.md:97-128`; `controller.ts:238-275`; Route explorer]

### Contracts

```ts
type RouteDecision = {
  decisionId: string;
  requestDigest: string;
  threadId: string;
  interactionId?: string;
  matchedPrecedence:
    | "explicit-interrupt" | "side-note" | "pending-response"
    | "handoff-continuation" | "no-active-interaction" | "ambiguous";
  conversationDisposition: "continue" | "side_note" | "fresh_route" | "clarify";
  executionDisposition:
    | "inline_answer" | "existing_capability_run"
    | "delegated_background_run" | "capability_gap" | "none";
  intent: { outcome: "answer" | "artifact" | "mutation" | "validation" | "decision" | "research";
            target?: string; seriesOrParallel: boolean };
  candidates: Array<{ capabilityRef: string; mode: string; owner: string;
                      triggerSelectors: string[]; installed: boolean;
                      confidence: "high" | "medium" | "low";
                      mutationPolicy: "read-only" | "artifact-only" | "lifecycle-owned";
                      rejectedReason?: string }>;
  selected?: { capabilityRef: string; mode: string; owner: string };
  confidence: "high" | "medium" | "low" | "block";
  clarificationQuestion?: string;
  offers: RouteOffer[];
  confirmation: { required: boolean; reason?: string; ownerGate?: string };
  gap?: { kind: string; escalation?: string };
};

type RouteOffer = {
  offerId: string;
  level: "easy" | "test" | "hardening";
  route: { capabilityRef: string; mode: string; target: string };
  outcome: string;
  owner: "inline" | "task-session" | "experiment-harness"
       | "dispatch-orchestrator" | "spellcraft" | "sigil-development";
  cost: { attention: "none" | "low" | "medium" | "high";
          scope: "inline" | "one-bounded-run" | "multi-run" | "lifecycle" };
  evidenceCeiling:
    | "explanation" | "one-run-receipt"
    | "repeatable-test-evidence" | "lifecycle-evidence";
  confirmationRequired: boolean;
  visibility: "recommended" | "available" | "hidden";
  risks: string[];
};
```

A preview or sole admissible route is not permission or execution. [`PRODUCT-VIEW.md:188-192,240-241`; `decision-gate/SKILL.md:51-73`; Route explorer]

### Easy, Test, Hardening and ownership

- **Easy:** inline or one bounded Task Session; reversible, one-off, no reusable correctness claim. Hide it when risk, ambiguity, repeatability, or protected mutation requires a stronger owner.
- **Test:** Experiment Harness owns fixtures, regimes, execution evidence and reports; the target spell/sigil retains semantic ownership. Use for repeatability or uncertainty against an existing contract.
- **Hardening:** only when repetition, stable reuse, recurring failure, drift, or changed gates/contracts justify lifecycle work. Spellcraft owns reusable multi-sigil composition; Sigil Development owns changes to a primitive capability contract. Neither evidence nor repetition automatically authorizes creation or promotion.

[`task-session/SKILL.md:32-110`; `experiment-harness/SKILL.md:47-148`; `spellcraft/SKILL.md:31-163`; Route explorer]

For a capability gap, search installed registries and runtime surfaces, offer only 1–5 credible alternatives, and block honestly if none exists. Never invent a capability or mutate a manifest without consent. Missing adapter/install routes to capability update; repeated composition to Spellcraft; changed primitive to Sigil Development; consequential alternatives to Decision Gate. [`necronomicon/README.md:393-433`; Route explorer]

### Context, runs, handoffs, and notifications

A launch snapshot records the parent thread, last included message, explicit source/system memory refs, inclusion/exclusion preview, redaction policy and digest. Later thread messages are invisible unless an explicit context-update event creates a new snapshot. Each child receives its own mission, owner, scope, forbidden actions and return protocol, revalidated through the existing delegation registry and approval gates. [`contracts.ts:1958-1982`; Session-state and Consumer explorers]

Cancellation is per run; descendant propagation is explicit. `cancel-requested` becomes `cancelled` only after acknowledgement or honest unknown residue. A terminal child produces an artifact/blocker handle and one coalesced notification. `join` applies the declared `notify`, `manual-consume`, or `join-before-continue` policy. A blocked attempt records blocker, last verified state, required owner/input, artifacts and snapshot; resume creates a new linked attempt. Completion and blockers never move focus, rewrite the transcript, or silently enter memory.

### Literal witness

While `T-arch/I-arch` remains active, one approved child prepares a governed subagent-strategy proposal and another creates an isolated Whisper draft from distinct snapshots. The user continues `I-arch`, switches to `T-other`, and both children continue without receiving later messages. Whisper succeeds, creating an artifact and quiet notification to `T-arch`; strategy blocks, creating residue and a needs-attention notification. Returning to `T-arch` shows both handles. Consuming Whisper attaches a reference only; inspecting or resuming strategy does not change the parent interaction. This witness is the v1 concurrency acceptance case—not a current-runtime claim. [All four explorers; global-lock evidence at `run-guard.ts:8-18`]

### Exact validation matrix

Unit/contract fixtures:

1. pending Decision Gate answer continues the owner;
2. explicit “pause and run X” records fresh route;
3. marked side note creates no run;
4. ambiguous OAuth follow-up asks one question;
5. low-confidence input never delegates silently;
6. disabled/stale target fails host revalidation;
7. preview/decline creates zero workspaces/runs;
8. immutable child snapshots exclude post-launch secret marker;
9. switching thread does not reparent, pause, or retarget notifications;
10. sibling cancellation independence;
11. success and blocker consume independently;
12. blocked resume creates new `runId`/snapshot and preserves old residue;
13. older persisted state hydrates with empty route/run/notification collections;
14. project branching copies/remaps compact memory and ancestry;
15. same-thread foreground exclusion and different-thread allowance;
16. late completion after abort cannot mutate current state.

Browser tests:

- conservative research phrase shows route card; dismissal does nothing; approval creates exactly one workspace and honestly says execution has not started;
- reload restores decision/workspace evidence but no fabricated active run;
- ordinary chat and explicit commands remain behavior-compatible;
- proposal exposes roles, scopes, receipts and join policy before spawn;
- the literal two-child witness supports thread switching, one artifact and one blocker without focus/context bleed;
- ten progress events coalesce to one completion item and one polite announcement;
- completion while typing preserves thread, composer, selection, scroll and focus;
- keyboard-only route/run/cancel/notification journey, focus-return checks, axe scan, reduced motion and keyboard resize.

### Budgets and observability

Initial proposed guardrails, requiring measurement rather than authority claims:

- classifier p95 ≤50 ms for deterministic rules and ≤300 ms for any bounded semantic assist;
- route-card decision payload ≤2 KB persisted, snapshot references rather than copied transcripts;
- no more than three initial offers and one expanded route card per interaction;
- one notification per meaningful state transition; progress coalesced;
- router-added prompt context ≤10% of the host context budget and telemetry ≤1% of routed-turn token volume;
- default visible recent-run window 20 entries; archive older terminal summaries, never raw child prompts;
- configurable child concurrency, beginning at two until isolation/cancellation tests pass.

Persist only digest, interaction state, candidate tuples, selected route, confidence, clarification resolution, gap/offer level, result/validation and explicit user correction. Exclude full prompts, secrets, chain-of-thought and redundant capability output. Aggregate repeated misses and corrections before suggesting maintenance; telemetry may recommend review but cannot invoke Spellcraft, mutate contracts or promote artifacts. [Route explorer; `necronomicon/README.md:368-407`]

### Increments

- **v0 — honest routing seam:** add a pure host classifier immediately before existing command/provider dispatch; preserve explicit commands; validate against existing host registries and approvals; append compact routed events to the transcript ledger; deliver the confirmation-gated workspace-creation browser witness. No background/concurrency claim.
- **v1 — session fabric witness:** add optional Interaction, RouteDecision, ContextSnapshot, Run, Notification and ancestry fields with normalization; replace the global lock with per-thread foreground locks plus bounded child registry; implement run tray, artifact tab, cancellation, blocker residue, resume and restoration reconciliation; pass the literal two-child isolation witness.
- **v2 — evidence-driven quality:** calibrate confidence and budgets from correction/miss fixtures; add scheduler ceilings and richer join policies; admit versioned public-neutral routing rules; integrate Experiment Harness evidence; allow explicit Spellcraft proposals for repeated composition while keeping lifecycle acceptance and promotion outside Augmentor.

No implementation should begin until the ResonantOS branch is advanced from current `origin/dev`; browser-visible concurrency must not be claimed before v1 isolation, cancellation, restoration and no-focus-steal evidence passes.

ORCHESTRATE_RECEIPT
action_id=spawn-0005
dispatch_id=2026-07-28-augmentor-routing-session-fabric-route
run_id=20260729T0145Z-routing-session-fabric-001
wave_id=synthesizer
step_id=s2
role=routing-session-synthesizer
capability_ref=research
status=pass
artifacts=[research/2026-07-28-augmentor-routing-session-fabric/research.md,arcanum/spells/necronomicon/README.md,arcanum/arcana/task-session/SKILL.md,arcanum/arcana/decision-gate/SKILL.md,arcanum/arcana/experiment-harness/SKILL.md,arcanum/arcana/spellcraft/SKILL.md,projects/ide-ergonomics/PRODUCT-VIEW.md,projects/ide-ergonomics/UNIFIED-PRODUCT-VIEW.md,../workspace-resonant/2.0.0-alpha/src/core/contracts.ts,../workspace-resonant/2.0.0-alpha/src/core/delegation.ts,../workspace-resonant/2.0.0-alpha/src/core/runtime.ts,../workspace-resonant/2.0.0-alpha/src/modules/chat/controller.ts,../workspace-resonant/2.0.0-alpha/src/modules/chat/run-guard.ts,../workspace-resonant/2.0.0-alpha/src/modules/chat/StrategistChatRail.tsx,../workspace-resonant/2.0.0-alpha/public/addons/augmentor-chat.json,git:dev..origin/dev]
validation=pass
blockers=[]
residue=The architecture and budgets are synthesis proposals, not accepted contracts. Current ResonantOS proves thread/project management, command routing, persistence, bounded delegation packets, workspace creation, and one global transient run only; concurrency, general run ancestry, notifications, cancellation restoration, join, resume, and the literal parallel witness remain unimplemented. The checkout is seven commits behind origin/dev, although current upstream diff does not touch the analyzed runtime source scope; package.json does differ.
handoff_note=Use v0 as the first implementation boundary: conservative host-owned classification plus confirmation-gated workspace creation and persistence. Do not claim session-fabric concurrency until v1 passes the literal two-child browser witness and isolation, cancellation, restoration, selective-consumption, accessibility, and no-focus-steal tests.
