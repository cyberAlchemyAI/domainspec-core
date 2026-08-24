## Candidate architecture synthesis

Timestamp: `2026-07-29T00:14:28-03:00`  
Mode: read-only; no files edited.  
Validation: `PASS` as a cited candidate architecture; `BLOCKED_CURRENT` for implementation, runtime readiness, and product acceptance.

### Verdict and evidence boundary

The four explorers converge on one viable architecture: Augmentor may own a conversational proposal/control experience and persisted read projections, but it must not become a scheduler, dispatch authority, execution registry, session store, job/workspace/artifact owner, or memory-intake authority. The executable chain remains:

```text
ordinary request
  -> preview-only StrategyProposal
  -> immutable RouteDecision
  -> exact-digest approval
  -> validated and registered Dispatch
  -> Orchestrate action plan
  -> host-owner calls
  -> Run projections referencing owner records
  -> owner-backed outcomes/blockers
  -> explicit result consumption
```

This is a proposed integration blueprint, not current ResonantOS behavior. Agent 1 establishes the public lifecycle/authority separation from Subagent Strategy, Dispatch Spec, Orchestrate, and the private adapter precedent (`research.md`, Agent 1, lines 7–17; `.agents/skills/subagent-strategy/SKILL.md:20-26,50-107`; `arcanum/formulae/dispatch-spec/SKILL.md:65-174`; `.agents/skills/orchestrate/SKILL.md:65-143`). Agent 2 confirms the necessary ResonantOS owner seams exist but no adapter or general child executor binds them (`research.md`, Agent 2, lines 122–227; consumer `src/core/contracts.ts:955-1069,1958-2105`, `src/core/delegation.ts:33-96,582-604`, `src/core/compute-fabric.ts:194-239`). Agent 3 shows the conversational journey is acceptance-ready only as a proposal because the current global run guard prevents parent-plus-two-child concurrency (`research.md`, Agent 3, lines 296–326; consumer `src/modules/chat/run-guard.ts:8-18`). Agent 4 validates the frozen route shape but explicitly denies that this proves a runtime profile, host operations, reconnect behavior, or product acceptance (`research.md`, Agent 4, lines 352–368, 444–450; `DISPATCH-ROUTE.json:308-378`).

The primary disagreement is therefore not architectural but evidentiary:

- Agent 1 calls the portable adapter contract viable.
- Agent 2 says current owner seams are sufficient for an additive implementation, but current execution is absent.
- Agent 3 says the UX is coherent but cannot pass today.
- Agent 4 says the only honest current product lane is preview/export plus explicit capability-gap reporting.

These positions reconcile as: `GO_FOR_BOUNDED_IMPLEMENTATION_DESIGN`, `NO_GO_FOR_CURRENT_EXECUTION_OR_ACCEPTANCE`.

## Public-neutral contract

### Browser/public projection contract

`StrategyProposal` should contain only portable intent:

- proposal ID, request/thread reference, goal/evidence-selector digests;
- trigger decision and reasons;
- named capability and dispatch type;
- roles with purpose, capability reference, target/mode, bounded inputs/outputs, mutation policy, and allowed/forbidden scopes;
- dependency waves/edges, join policy, gates, stop/loop ceilings;
- expected artifact/blocker/receipt handles;
- initial authorization state `requires_user_permission`;
- runtime-profile ID/version and sanitized capability/operation availability;
- a digest over the exact proposal bytes.

`AdmissionResult` should expose sanitized status, supported contract/profile versions, proposal digest, unmet obligations, and opaque validator/tension handles.

`ExecutionHandle` should expose dispatch/orchestrate references and correlations among `actionId`, `childId`, `attemptRunId`, `agentId`, and opaque host-run references.

`HostRunProjection` should contain references—not copied owner policy—to parent thread/goal, dispatch/action, `DelegationPacket`, `TaskWorkspace`, optional `ComputeJob`, execution owner, snapshot digest, observed state, artifacts/blockers, and `resumesRunId`.

These fields derive from Agent 1’s minimal contract and runtime-profile analysis (`research.md`, Agent 1, lines 18–45, 61–71; `.agents/skills/subagent-strategy/templates/runtime-profile.md:1-102`; `arcanum/formulae/dispatch-spec/SKILL.md:87-101,113-174`) and Agent 2’s proposed records (`research.md`, Agent 2, lines 185–206; consumer `src/core/contracts.ts:1958-2105`).

### Adapter/server-only bindings

The public/browser contract must not carry:

- DomainSpec schema `0.8.0` or `evidence_binding` layout;
- named agent pool, identities, eligibility, or final-approver implementation;
- Inventory packet/card IDs or private preflight method;
- exact two-checker rubric/evidence locations;
- registrar commands, append-only ledger rows/event identifiers, or exit enum;
- private constitution prose, repository paths, publication destinations, secrets, or evidence bytes;
- type-specific research repair/writer/auditor rules.

Those remain consumer runtime-profile or private adapter bindings. The client receives status, digest, owner name, and opaque handles only. This boundary is explicit in Agent 1 (`research.md`, lines 33–45; private precedent `implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md:46-122,217-268`) and Agent 4’s list of local obligations external protocols cannot settle (`research.md`, lines 421–441).

## Authority and event chain

| Stage | Authoritative owner | Augmentor behavior |
|---|---|---|
| Request/preview | Interaction plus proposal adapter | Classify intent, discover capability/profile, render a no-side-effect proposal. Zero registration, spawn, or Run creation. |
| Route choice | `RouteDecision` projection | Persist immutable candidates, selection, rationale, version, and proposal digest. Confidence is not approval. |
| Approval | consumer owner gate | One explicit action binds exact proposal/dispatch bytes. Any role, scope, selector, wave, or fallback change invalidates approval. |
| Dispatch | Dispatch Spec + consumer registrar | Validate authorization, capability bindings, waves, scopes, receipts, and lifecycle; register only after approval. Dispatch Spec does not execute. |
| Preflight | Orchestrate | Validate approved dispatch, authorization, host-operation availability, and persist actions with zero spawns. |
| Spawn | Orchestrate host adapter | Exactly one native spawn per persisted action; create child Run projection only after an owner binding is returned. |
| Execution | existing host owner | Execute through the chosen provider/delegation/compute owner. Workspace creation alone is not execution. |
| Join/gates | Orchestrate | Mailbox wait plus inventory reconciliation; interrupt unresolved actions once at timeout; deterministic gate reduction. |
| Outcome | execution/artifact owner | Persist owner evidence and reference artifact/blocker handles. Notifications never settle truth. |
| Closeout | Subagent Strategy + Dispatch/Orchestrate + consumer ledger | Require every expected child terminal, joined, and closed; preserve partial success, residue, and blocked dependents. |
| Observation | telemetry owner | Emit post-closeout behavior signals; observation cannot approve, execute, or promote. |

Sources: Agent 1 host-call mapping (`research.md`, lines 46–60; `.agents/skills/orchestrate/SKILL.md:79-143`; `.agents/skills/orchestrate/hosts/codex-native.md:21-67`), Agent 2 adapter boundaries (`research.md`, lines 167–184), and Agent 4’s routing, approval, durable-task, cancellation, and tracing precedents (`research.md`, lines 370–380; [OpenAI orchestration](https://openai.github.io/openai-agents-python/multi_agent/), [OpenAI human-in-the-loop](https://openai.github.io/openai-agents-python/human_in_the_loop/), [A2A specification](https://a2a-protocol.org/dev/specification/), [MCP Tasks](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks)).

## Exact existing owner references

- `Dispatch Spec`: executable role/capability/wave/scope/receipt validation; no execution (`arcanum/formulae/dispatch-spec/SKILL.md:65-174`).
- `Orchestrate`: approved-plan compilation, native spawn, wait/inventory reconciliation, interrupt, reduction, join, close (`.agents/skills/orchestrate/SKILL.md:79-143`).
- `DelegationPacket`: mission, capabilities, tools, scope, approval, expected artifacts, verification, return protocol (consumer `src/core/contracts.ts:1958-1982`; validation `src/core/delegation.ts:33-96`).
- `TaskWorkspace`: packet/result/verification filesystem envelope only; never execution proof (`src/core/contracts.ts:1984-2009`; `src/core/delegation.ts:582-604`).
- `ComputeJob`: optional execution owner for node roles, network/filesystem/secrets, approval, cost, timeout, artifact policy, and status (`src/core/contracts.ts:955-1056`; `src/core/compute-fabric.ts:194-239`).
- `GoalWorkspace`: supervisory thread, allowed agents/tools, steps, artifact/blocker and delegation references; not a Run (`src/core/contracts.ts:2019-2105`).
- `ComputeArtifact`/workspace result: authoritative result; Goal/chat/Run retain references (`src/core/contracts.ts:1058-1069,2040-2048`).
- provider policy: host-mediated, not selected around by Strategy (`public/addons/augmentor-chat.json:169-185`).
- notification projection: proposed attention/read/delivery owner; never execution truth. No scoped current notification owner was found (Agent 2, `research.md`, lines 140–165).

## Proposal and control UX

The ordinary experience should be a transition card followed by a compact two-row run tray, not an infrastructure dashboard.

Before approval, the card says “Proposed: 2 background runs; nothing has started,” names each role/purpose/result, summarizes included context and forbidden effects, and offers `Review & approve`, `Edit plan`, and `Not now`. Details may reveal selectors, owners, receipts, mutation policy, and join behavior. Editing invalidates prior approval. The final action is explicit: `Approve and start 2`.

After launch, the parent composer remains usable. Each child row uses human states such as `Starting`, `Working`, `Needs your answer`, `Cancel requested`, `Cancelled`, `Could not confirm cancellation`, `Done`, `Blocked`, and `Failed`. Child transcripts do not stream into the parent. Thread switching neither reparents nor injects context. A targeted answer creates one addressed input revision for one child. Result actions are `Open result`, `Attach to this conversation`, and `Keep separate`; attachment adds only the selected handle/summary.

Keyboard controls require real labeled buttons/fields, stable focus restoration, ordinary tab order unless a true composite widget is used, polite coalesced live regions, no async focus theft, reduced-motion support, and reload without replaying old announcements.

This is supported as proposed product evidence by Agent 3 (`research.md`, lines 306–350; `projects/ide-ergonomics/PRODUCT-VIEW.md:125-193,226-253`; accepted `research/2026-07-28-augmentor-routing-session-fabric/findings.md:130-189,231-249`). Current ResonantOS supplies thread buttons and polite single-run atoms only (`StrategistChatRail.tsx:393-415,519-603,762-795,900-918`).

## Capability discovery and degraded modes

Admission must resolve a stable profile/version, declared capability, required/optional host operations, concurrency ceiling, join targeting, cancellation/recovery support, and opaque handle schemas. Revalidate immediately before launch. Current ResonantOS declares `agent-delegation` and `notifications`, but no Subagent Strategy runtime profile or general executor (`research.md`, Agent 2, lines 140–165; `public/addons/augmentor-chat.json:30-66`; Agent 4, lines 412–420).

| Condition | Honest result |
|---|---|
| Capability absent | Preview/export; optionally route to separately authorized install/hardening; otherwise block. |
| Required spawn/wait/interrupt/inventory absent | Hard block, list missing operations, record zero spawns. No nested CLI/inline imitation. |
| User declines | No registration or child Run; retain/discard proposal by choice. |
| Validation fails | Preserve defects; bounded repaired proposal requires full revalidation and approval. |
| Parallelism unavailable before approval | Offer serial only as a revised route if semantics remain valid; reapprove. |
| Capacity exhausted after approval | Do not silently serialize; block/preserve residue unless a bounded queue policy was already approved. |
| One helper truly suffices | Use the separate one-helper lifecycle only if the requested outcome no longer needs multi-lane synthesis or independent gates. |
| Partial child failure | Preserve successful sibling; block dependent wave under current `join_policy=all`/`on_incomplete=block`. |
| Timeout | Interrupt once; emit explicit timed-out receipt; never infer success from silence. |
| Reload/reconnect | Reconcile persisted IDs with owner; display unknown when owner truth cannot be proven. |
| General capability lacks medium/complex proof | Fixture/experimental lane only; no readiness or promotion claim. |

This is Agent 4’s explicit table (`research.md`, lines 382–411; `.agents/skills/orchestrate/SKILL.md:85-105,121-140`; `DISPATCH-ROUTE.json:308-378`), consistent with Agent 3’s user-facing gap language (`research.md`, lines 313–326).

## Persistence, isolation, cancellation, join, and consumption

Minimum persisted records are `StrategyProposal`, immutable `RouteDecision`, digest-bound `StrategyApproval`, `HostRunProjection`, append-only `RunTransition`, addressed `RunInputRevision`, terminal `RunOutcome`, and independent `NotificationProjection`.

Semantics:

- Hydration restores projections, then reconciles every nonterminal attempt against owner truth; it never fabricates `running`.
- Each child has an immutable `childId`, unique attempt `runId`, and content-addressed snapshot.
- Parent/sibling/thread-switch messages cannot alter an existing snapshot.
- Clarification targets one child and produces a new snapshot/input revision; sibling and parent digests remain unchanged.
- Resume creates a new attempt with `resumesRunId`; terminal attempts never reopen.
- Cancellation first becomes `cancel-requested`; only owner acknowledgement yields `cancelled`. Unknown acknowledgement becomes `cancellation-unknown`.
- A late result after acknowledged cancellation is quarantined as owner evidence and does not reopen success.
- Orchestrate owns mechanical join; `notify`, `manual-consume`, and `join-before-continue` are product policies over terminal references.
- Opening or attaching a result does not merge transcripts, consume the sibling, change notification state, or promote memory.

Sources: Agent 2 (`research.md`, lines 185–229), Agent 1 collapse rules (`research.md`, lines 83–96), and MCP/A2A precedent through Agent 4 (`research.md`, lines 374–379).

## Smallest implementation slices

1. Refresh the consumer from `origin/dev` and rerun repository checks; inspected local HEAD was seven commits behind, although scoped runtime seams were byte-unchanged.
2. Add neutral proposal, immutable route/approval, owner-reference Run, transition/outcome, and hydration-normalization contracts.
3. Add installed capability/profile/operation discovery plus launch-time revalidation.
4. Add preview/edit/exact-approval UI, proving proposal and decline cause zero registration/spawn.
5. Bind one approved Orchestrate action to `DelegationPacket`/`TaskWorkspace`; truthfully show “prepared, execution not started.”
6. Add one real owner adapter returning execution/optional `ComputeJob` handles.
7. Replace the global guard with separate foreground and child registries; begin with child concurrency ceiling `2`.
8. Add append-only reconciliation, acknowledgement cancellation, targeted clarification, blocked outcomes, and resume-as-new-attempt.
9. Add notification projections and independent artifact consumption.
10. Execute the literal two-child browser witness.

Slices 1–5 are infrastructure only. Product acceptance begins only when slices 6–10 execute against real owners. Sources: Agent 2 (`research.md`, lines 230–244) and Agent 1 (`research.md`, lines 72–82).

## Literal two-child browser witness

Use deterministic local fixtures: child A is Strategy; child B is Whisper.

1. Enter the ordinary request; assert a proposal with exactly A+B and zero spawn events.
2. Edit A’s selector; assert B’s preview snapshot unchanged.
3. Approve once; assert exactly two owner calls and two child envelopes with distinct IDs, snapshot digests, and owner references.
4. Send ordinary parent chat while both run; assert success and unchanged child snapshots.
5. Switch thread; assert children continue with no reparenting, marker leak, or focus steal.
6. A enters `Needs your answer`; answer by keyboard while notifications are muted; assert exactly one addressed input revision to A.
7. Cancel A; assert `Cancel requested`, then acknowledged `Cancelled`; B continues and completes.
8. Resume A as a new linked attempt.
9. Reload before consuming B; reconcile owner IDs; restore unread state with no duplicate announcement.
10. Attach B only; assert the parent receives B’s artifact handle while A transcript/result and sibling notification/read state remain untouched.
11. Plant unique parent/A/B/other-thread markers and verify containment through snapshots, owner requests/outputs, notifications, and explicit attachment.

Agent 3 supplies this exact witness and its rejection criteria (`research.md`, lines 327–350; accepted findings `:174-189,231-243`). Agent 2 confirms current real child execution is absent (`research.md`, lines 140–165).

## Deterministic/browser tests and measurable overhead

Deterministic tests:

- proposal/edit/decline => zero registration/spawn/Run mutations;
- digest change => approval invalidated;
- no spawn before registered approved handle and persisted action;
- action replay/mismatch/unknown ID => zero extra host calls;
- Run owner fields are references and cannot write owner policy/status;
- snapshot/marker isolation across parent, siblings, and threads;
- one clarification => one child input revision;
- partial failure preserves sibling and gates dependents;
- no success with pending/unknown/unclosed child;
- read/mute/reload cannot mutate execution/artifact/memory truth;
- one result attachment does not consume sibling or intake memory;
- missing operation => explicit block and zero spawn;
- browser/public payload scan contains no DomainSpec schema, pool, ledger, paths, or evidence.

Browser/accessibility tests cover the literal witness plus keyboard-only editing/approval/answer/cancel/resume/consume, dialog focus restoration, no async focus theft, polite coalescing, reduced motion, and reload without replay.

Owner-pending measurable budgets, not measured performance:

- route cards in at most 20% of ordinary turns;
- clarification in at most 5%;
- no more than two extra actions for consequential launch;
- one announcement per meaningful terminal/attention transition;
- initial child concurrency ceiling `2`;
- retain 20 recent terminal projections.

These budgets originate in accepted proposed findings and Agent 3 (`research.md`, lines 317–326; accepted findings `:245-249`). They require measurement during the fixture/browser lane before acceptance.

## Public/private boundary and rejected collapses

Public Arcanum may define portable lifecycle meanings, invariants, profile slots, and sanitized handles. The consuming adapter owns private schema, identities, eligibility, evidence, registrar/ledger, paths, and publication policy. No private prose or bytes enter `arcanum/` or browser payloads.

Reject:

- Augmentor scheduling independently of Orchestrate;
- client registry as dispatch/job/workspace/artifact/memory authority;
- preview/confidence as approval or execution;
- `TaskWorkspace == execution`;
- `GoalWorkspace == Run`;
- notification/read state as truth;
- artifact attachment as transcript merge or memory intake;
- silent serial/helper/CLI substitution;
- external protocol precedent presented as a local implementation owner.

Sources: Agent 1 (`research.md`, lines 62–71, 83–96), Agent 2 (`research.md`, lines 245–258), and Agent 4 (`research.md`, lines 412–441).

## Named open owner decisions

1. Public Arcanum owner: finalize the neutral projection/lifecycle contract and supported contract version.
2. ResonantOS persistence owner: choose retention, normalization, transition storage, and reconciliation boundaries.
3. ResonantOS capability owner: define runtime-profile discovery, grants, operation mapping, and launch-time revalidation.
4. Orchestrate/host-profile owner: define exact spawn/wait/interrupt/inventory bindings, wait targeting, concurrency ceiling, and recovery support.
5. Execution-owner adapter: map each action to delegation/provider/optional compute without duplicating policy.
6. Approval owner: define actor eligibility and whether protected downstream owners require additional gates.
7. Cancellation/recovery owner: define acknowledgement, unknown state, late-result quarantine, TTL/retention, and reconnect behavior.
8. Notification owner: define delivery/read/mute/snooze/restoration separately from execution and consumption.
9. Result/memory owners: define explicit attachment versus checkpoint versus memory intake.
10. UX/accessibility owner: accept attention budgets and execute the keyboard/browser witness.
11. Consumer maintainer: refresh the seven-commit-behind checkout before mutation.
12. Arcanum promotion owner: require medium/complex consuming-profile evidence before readiness/promotion claims.

These decisions consolidate Agent 1’s blockers (`research.md`, lines 109–115), Agent 2’s current blockers (`research.md`, lines 276–288), Agent 3’s pressure-test blockers (`research.md`, lines 341–350), and Agent 4’s unsatisfied local obligations (`research.md`, lines 421–450).

## Claim/evidence closure matrix

| Claim | Explorer evidence | Underlying selector/source | Closure |
|---|---|---|---|
| Adapter, not scheduler | Agent 1 lines 7–17; Agent 4 lines 412–420 | Subagent Strategy `:50-107`; Dispatch Spec `:103-174`; Orchestrate `:79-143` | Closed for architecture |
| Proposal has no execution effect | Agent 1 lines 46–49; Agent 3 lines 306–316 | Subagent Strategy `:92-101`; PRODUCT-VIEW `:125-193` | Closed as invariant |
| Route requires exact approval before spawn | Agents 1, 3, 4 | Subagent Strategy `:91-107`; Orchestrate `:79-118`; OpenAI HITL | Closed as design; unproved in consumer |
| Existing consumer owners can be referenced | Agent 2 lines 140–184 | consumer contracts/delegation/compute selectors above | Closed for seam identification |
| Current consumer cannot run witness | Agents 2 lines 122–138; 3 lines 296–305; 4 lines 352–368 | `run-guard.ts:8-18`; `delegation.ts:582-604` | Closed blocker |
| Durable projection must reconcile owner truth | Agents 2 lines 185–229; 4 lines 374–379 | consumer runtime `:1360-1380,1876-1945`; A2A; MCP Tasks | Closed candidate semantics |
| Cancellation needs acknowledgement and late-result quarantine | Agents 2 and 4 | MCP Tasks; Orchestrate `:121-131` | Closed candidate semantics; owner decision open |
| Notifications are non-authoritative | Agents 1, 2, 4 | usage telemetry `:1-67`; MCP Tasks | Closed invariant; implementation owner absent |
| Result consumption is not memory intake | Agents 1–3 | routing/session findings `:146-148`; consumer artifact owners | Closed invariant; exact intake API open |
| Degraded paths cannot silently change approved strategy | Agent 4 lines 382–411 | Orchestrate `:85-105,134-140`; route `:308-378` | Closed |
| Literal witness establishes product value | Agent 3 lines 327–350 | routing/session findings `:174-189,231-243` | Open: not executed |
| Attention/concurrency/retention budgets are measurable | Agent 3 lines 317–326 | routing/session findings `:245-249` | Open: owner-pending/unmeasured |
| Private DomainSpec bytes stay adapter-side | Agents 1 and 4 | private adapter `:46-122,217-268`; runtime profile `:1-102` | Closed boundary |
| Dispatch route shape validates | Agent 4 lines 444–450 | validator command over `DISPATCH-ROUTE.json` | Closed narrowly: `VALIDATION=pass` |
| Runtime/readiness/product acceptance | All agents | absence of profile/executor plus global guard/no witness | Blocked |

Final result: the evidence closes a coherent, additive, public-neutral candidate architecture and its acceptance contract. It does not close implementation, current executability, performance, medium/complex proof, promotion, or product acceptance.
