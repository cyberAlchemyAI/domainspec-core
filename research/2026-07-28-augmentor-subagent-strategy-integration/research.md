## Agent 1 — portable contract and authority

Portable-contract explorer report (spawn-0001)

Time: started approximately 2026-07-29T00:03:00-03:00; finished 2026-07-29T00:07:33-03:00. Read-only; no files edited. Worktree was already dirty when checked, including generated Subagent Strategy surfaces and the arcanum submodule; I made no mutation.

VERDICT
A minimal public-neutral integration is viable as an adapter over three separate owners, not as a new Augmentor scheduler: (1) Subagent Strategy owns lifecycle ordering and human authority; (2) Dispatch Spec validates executable route shape; (3) Orchestrate maps approved persisted actions to host-native spawn/wait/interrupt/inventory and owns execution/join/close. Augmentor should own only UI/projection and correlation: preview a StrategyProposal, persist an immutable RouteDecision and ContextSnapshot, reference the approved dispatch/orchestrate run and host execution owners from child Run envelopes, and project notifications/results. This is a proposed integration blueprint, not implemented behavior.

STATE BOUNDARY
- CURRENT public seed: the generated public contract declares universal lifecycle trigger -> owner/preflight -> exact persisted sheet -> composite readiness -> two independent digest-bound tension checks -> one explicit confirmation/freeze -> deterministic registration -> dependency-aware execution -> final approval -> join/close -> result/observation hooks. It explicitly disowns dispatch field definitions, type judgment, agent eligibility, constitution/ledger schemas, other capability output semantics, and artifact/publication policy (`.agents/skills/subagent-strategy/SKILL.md:20-26,50-78,91-107`; seed status `.agents/skills/subagent-strategy/README.md:1-11`).
- CURRENT route validator: Dispatch Spec validates authorization, role/capability bindings, waves, scopes, receipt requirements, and terminal lifecycle, but does not execute; parent orchestrator owns spawning/joining/gating/synthesis (`arcanum/formulae/dispatch-spec/SKILL.md:65-101,103-174`).
- CURRENT host executor: Orchestrate preflights approved validated dispatches, compiles persisted actions without spawning, performs exactly-once native spawn, mailbox-wide bounded join/reconciliation, timeout interrupt, deterministic reduction and closeout (`.agents/skills/orchestrate/SKILL.md:65-89,104-143`). Codex profile is only one host binding, mapping spawn/wait/interrupt/inventory/message and failing closed when required operations are absent (`.agents/skills/orchestrate/hosts/codex-native.md:1-20,49-67`).
- CURRENT private precedent: DomainSpec binds schema 0.8.0, Inventory preflight, agent pool/identity, final approver, exact sheet hash, two PASS handles, confirmation handle, deterministic registrar, append-only ledger, typed research handoff and private paths. Those are consumer authority, not portable fields (`implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md:46-83,85-122,217-268`).
- PROPOSED host fabric: Interaction, RouteDecision, Run, ContextSnapshot and Notification are projections; authority flows one way from decision through owner gate/snapshot/run to owner receipt and append-only outcome. Run cannot adjudicate ComputeJob/workspace/delegation/dispatch truth; notification cannot settle truth; consumption cannot imply memory intake (`research/2026-07-28-augmentor-routing-session-fabric/findings.md:35-55,57-117`). Preview/selection create no run (`.../findings.md:119-132`).
- PROPOSED acceptance only: cancellation acknowledgement, resume-as-new-attempt, selective joins and notification restoration are not current ResonantOS behavior (`.../findings.md:144-170`).

MINIMAL PUBLIC-NEUTRAL CONTRACT
Input proposal (portable semantics, consumer-selected representation):
- request/goal digest and bounded evidence selectors;
- trigger decision and reasons;
- dispatch type plus named owner capability;
- roles `{roleId,purpose,capabilityRef,target,mode,inputRefs,outputRefs,mutationPolicy,allowed/forbiddenScopes}`;
- dependency waves/edges, join policy, gates/stop and loop ceilings;
- expected receipt/artifact handles;
- human authorization state, initially `requires_user_permission`;
- profile id/version and capability/operation availability results.
Lifecycle results:
- readiness `{status,schema/profile versions,proposalDigest,closed obligations}`;
- independent tension verdict handles bound to that digest (where configured);
- confirmation handle bound to exact digest;
- registration/dispatch handle;
- action/run correlations `{actionId,agentId,hostRunRef}`;
- per-action receipt `{spawn,join,close,status,residue,reroute,artifact/blocker handles}`;
- aggregate gate/partial-failure/final-approval result;
- paired closeout and observation handles.
The portable contract should specify meanings and invariants, not mandate DomainSpec’s sheet schema or ledger. Dispatch Spec already supplies the executable neutral role fields and lifecycle evidence (`arcanum/formulae/dispatch-spec/SKILL.md:87-101,113-174`).

KEEP ADAPTER/SERVER-SIDE
- DomainSpec schema version `0.8.0`, `evidence_binding` shape, exact appender commands, sheet and telemetry paths.
- Inventory packet/card IDs and preflight method; Inventory is discovery only.
- named agent pool, selection rules and identities; final-approver eligibility implementation.
- exact two-checker tension rubric and evidence storage handles.
- registrar, append-only ledger schema/event identifiers, local exit reason enum.
- type-specific research evidence closure/repair routing, writer/auditor rules.
- private constitution prose, publication paths, artifact destinations and private evidence.
These are precisely the variable bindings anticipated by the public runtime-profile template (`.agents/skills/subagent-strategy/templates/runtime-profile.md:1-73`) and its validation rules (`:75-102`). Sending them to the browser is unnecessary; the client needs sanitized statuses/handles, not authority bytes.

HOST-CALL MAPPING
1. Preview: Augmentor classifier/capability discovery + profile resolver constructs a side-effect-free StrategyProposal; deterministic form/readiness and tension endpoints may be server calls, but no registration or host action. UI shows owners/scopes/outputs/gaps. (`subagent-strategy/SKILL.md:92-100`; runtime profile `:21-40`).
2. Confirmation: one explicit user action binds proposal digest; any byte change invalidates it. This is an owner-gate record, not route confidence (`subagent-strategy/SKILL.md:99-101`).
3. Registration: adapter invokes its deterministic registrar and returns a dispatch handle; DomainSpec uses one dispatch + one close event, but other profiles may use their own equivalent (`runtime-profile.md:46-50,75-88`).
4. Execution preflight: call Orchestrate on the approved Dispatch Spec; it validates route/authorization and active host operations and emits persisted wave actions with zero spawns (`orchestrate/SKILL.md:79-102`).
5. Spawn: one native spawn call per persisted action, exactly once; Augmentor creates/projections child Run refs only after returned binding (`orchestrate/SKILL.md:108-118`; codex host `:21-34`).
6. Join/gates: native mailbox wait + inventory reconcile known pending IDs; normalize receipts, interrupt unresolved once at timeout, reduce gate deterministically; never interpret a notification as completion (`orchestrate/SKILL.md:121-132`; codex host `:35-46`).
7. Closeout: audit all expected agents terminal joined/closed and pair the consumer close event; partial results/residue remain visible (`dispatch-spec/SKILL.md:152-174`; `subagent-strategy/SKILL.md:102-106`).
8. Observation: emit compact behavior telemetry/read models after authority-bearing closeout; observation never registers, executes, approves, or promotes (`subagent-strategy/SKILL.md:124-143`; `templates/usage-telemetry.md:1-67`).

VERSIONABLE CONSUMER RUNTIME PROFILE
Version: stable profile id; supported public lifecycle contract version; dispatch type -> live/reserved owner and read-only preflights; form/readiness and registration endpoints plus drift behavior; tension-check capability/availability; capability discovery and host-operation bindings; dependency semantics; final-approval rules; human-gate semantics; result/observation hooks; public/private publication rules. The existing template covers nearly all (`runtime-profile.md:7-73`). Add only neutral host binding metadata: orchestrate profile/version, required/optional operation names, cancellation/recovery support, wait targeting, join policies, concurrency ceiling, and opaque handle schemas. Do not version agent identities, ledger rows, private paths, secrets, or artifacts into a public/browser profile.

SECOND-AUTHORITY REJECTS
- Augmentor queues/schedules children independently of Orchestrate or changes owner status.
- A client-side registry becomes authoritative for dispatch, agents, jobs, workspaces, artifacts or memory.
- Strategy preview or route confidence counts as confirmation/registration/execution.
- RouteDecision/Run duplicates ComputeJob, DelegationPacket, TaskWorkspace, GoalWorkspace or Dispatch status/policy.
- UI notification/read state settles run/result truth.
- Result attachment implies transcript merge or memory promotion.
- Browser profile embeds DomainSpec schema, agent pool, ledger, private paths or evidence.
- Silent fallback to serial/one-helper/nested CLI when required operations are absent. Orchestrate explicitly blocks missing host behavior (`orchestrate/SKILL.md:83-89,134-143`).

ORDERED IMPLEMENTATION BLUEPRINT
A. Define neutral StrategyProposal/AdmissionResult/ExecutionHandle projection schemas; enforce proposal-no-run.
B. Implement server adapter resolving a versioned profile and installed capabilities; sanitize private readiness evidence to statuses/digests/handles.
C. Materialize/validate Dispatch Spec with `requires_user_permission`; render preview.
D. Bind one confirmation to digest, then register via adapter.
E. Invoke Orchestrate preflight; persist action plan; create Run projections referencing, never copying, owner records.
F. Execute first two-child wave through native host calls; keep parent active and contexts immutable/addressed.
G. Reconcile joins/partial failures, enforce gates, pair closeout, then project notifications and independently consumable artifact/blocker handles.
H. Add observation after closeout and prove it cannot mutate authority.
The literal first acceptance witness is already specified as strategy + Whisper children, parent continuation, thread switch, one targeted clarification, reload, selective consumption and marker containment (`...routing-session-fabric/findings.md:174-189`).

COLLAPSE TESTS
- Preview-no-side-effect: proposal/edit/decline yields zero registration/spawn/run-owner mutations.
- Digest gate: changed role/scope/input after confirmation is rejected until full revalidation/reconfirmation.
- Registration-before-spawn: no native action without registered approved handle and persisted matching action.
- Exactly-once: replay/unknown/mismatched action causes zero extra host calls.
- Owner-reference: Run contains IDs only; attempts to write owner policy/status fail.
- Isolation: late parent/sibling messages and thread switch do not change child snapshot digest.
- Targeted input: clarification updates one child only.
- Partial failure: successful sibling remains independently consumable; dependents stay gated; residue/confidence visible.
- Join/close completeness: success impossible with pending/unknown/unclosed child.
- Notification non-authority: mark-read/mute/reload cannot change run, artifact, dispatch or memory state.
- Consumption split: attach/inspect one result does not merge transcripts, consume sibling, or promote memory.
- Missing-operation honesty: zero spawn attempts; explicit block/fallback offer, never silent substitution.
- Private-boundary scan: browser payload/public artifacts contain no DomainSpec paths/schema/pool/ledger/evidence.

ARTIFACTS/EVIDENCE REVIEWED
- Dispatch and inventory proposal: `research/2026-07-28-augmentor-subagent-strategy-integration/{dispatch-sheet.json,STRATEGY.md,DISPATCH-ROUTE.json,strategy-inventory-packet.json}` (proposal/discovery, non-authority).
- Public generated lifecycle + profile/telemetry: `.agents/skills/subagent-strategy/{SKILL.md,README.md,templates/runtime-profile.md,templates/usage-telemetry.md}` (seed/current bytes; generated mirror).
- Route validator: `arcanum/formulae/dispatch-spec/SKILL.md` (current public owner; assigned prompt’s `arcanum/arcana/...` path does not exist).
- Executor/host: `.agents/skills/orchestrate/SKILL.md`, `hosts/codex-native.md` (current generated runtime contract/profile).
- Private precedent: `implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md` (current private owner binding).
- Accepted research: `research/2026-07-28-augmentor-routing-session-fabric/findings.md` (verified research, proposed product contract clearly labeled).

VALIDATION
PASS for contract extraction and authority separation: every lifecycle stage maps to an existing named owner or is explicitly a proposed Augmentor projection. No files were edited. BLOCKED for implementation/readiness claims: public Subagent Strategy is seed and lacks medium/complex consumer proof; no ResonantOS runtime profile/adapter exists; accepted two-child browser witness has not run; cancellation/reconnect/selective notification semantics remain proposed. Also, generated public surfaces are currently modified in the shared worktree, so canonical-vs-generated comparison is required before using exact bytes for implementation.

BLOCKERS / OWNER DECISIONS
- Choose canonical neutral projection schemas and retention/persistence owner.
- Define ResonantOS profile, capability discovery, operation mapping and concurrency ceiling.
- Choose exact cancellation acknowledgement/reconnect semantics per execution owner.
- Define sanitized readiness/error payloads without leaking private evidence.
- Refresh/verify consumer checkout before mutation and execute the literal browser witness before claiming product acceptance.

## Agent 2 — consumer runtime seam

Consumer-runtime explorer report — spawn-0002  
Observed: `2026-07-29T00:07:52-03:00`  
Mode: read-only; no files changed.

## Verdict

The smallest honest seam is an additive, persisted host projection that binds an approved public Subagent Strategy dispatch to existing ResonantOS owners. It must not schedule work itself.

```text
preview-only StrategyProposal / immutable RouteDecision
  -> one explicit approval
  -> validated Dispatch Spec
  -> Orchestrate action handles
  -> host Run projections
       -> existing DelegationPacket / TaskWorkspace
       -> optional existing ComputeJob
       -> existing GoalWorkspace references
       -> owner artifact/blocker handles
```

The current consumer cannot yet provide a real two-child product witness. It has bounded delegation/workspace contracts, compute validation/submission, provider policy, persisted shell state, and a visible chat-run atom, but the active chat guard permits only one transient run globally and Engineer/Hermes workspace creation explicitly does not start execution.

## Current versus missing

| Concern | Current evidence | Missing additive behavior |
|---|---|---|
| Capability admission | `Capability` includes `agent-delegation` and `notifications`; Augmentor requests both with hard-stop/degrade semantics. [`src/core/contracts.ts:4-20`](../workspace-resonant/2.0.0-alpha/src/core/contracts.ts), [`public/addons/augmentor-chat.json:30-66`](../workspace-resonant/2.0.0-alpha/public/addons/augmentor-chat.json) | Runtime-profile discovery for Subagent Strategy/Dispatch/Orchestrate operations; revalidation immediately before launch |
| Proposal and approval | Delegation packets carry `humanApprovalRequired`, approval reasons, capabilities, tools, scope, verification, artifacts, and return protocol. [`src/core/contracts.ts:1958-1982`](../workspace-resonant/2.0.0-alpha/src/core/contracts.ts) | Persisted preview-only `StrategyProposal`, immutable `RouteDecision`, approval record binding the exact proposal/dispatch digest |
| Dispatch | `validateDelegationPacket` enforces bounded missions, workspace, returns, risky approval, and capability warnings. [`src/core/delegation.ts:33-96`](../workspace-resonant/2.0.0-alpha/src/core/delegation.ts) | Resonant adapter from each approved Orchestrate action to a packet plus owner correlation IDs; no local copy of Dispatch rules |
| Workspace | `TaskWorkspace` is paths/packet/result/verification metadata. [`src/core/contracts.ts:1984-2009`](../workspace-resonant/2.0.0-alpha/src/core/contracts.ts) | No change in meaning: workspace remains preparation/evidence storage, never proof of execution |
| Execution | ComputeJob owns node roles, workspace/network/filesystem/secrets/artifacts/approval/cost/timeouts/status. [`src/core/contracts.ts:955-1056`](../workspace-resonant/2.0.0-alpha/src/core/contracts.ts); compute validates and submits through existing fabric. [`src/core/compute-fabric.ts:194-239`](../workspace-resonant/2.0.0-alpha/src/core/compute-fabric.ts), selector `submitComputeJob` | An execution-owner adapter choosing an existing compute/provider/delegation operation and returning its handle; no strategy-owned queue |
| Goal supervision | GoalWorkspace already owns thread, allowed agents/tools, memory refs, steps, artifacts, blockers, and delegation refs. [`src/core/contracts.ts:2019-2105`](../workspace-resonant/2.0.0-alpha/src/core/contracts.ts) | Correlation references from goal to strategy/dispatch/run/child attempts; do not put runtime transitions into GoalWorkspace |
| Chat execution | One `activeChatRunTokenRef`: any active run rejects another, regardless of thread. [`src/modules/chat/run-guard.ts:5-28`](../workspace-resonant/2.0.0-alpha/src/modules/chat/run-guard.ts) | Independent foreground interaction and child-run cardinalities, keyed by owner/thread/run rather than one global token |
| Runtime events | `ChatRunEvent` is transient, UI-local, last ten events. [`src/core/contracts.ts:85-95`](../workspace-resonant/2.0.0-alpha/src/core/contracts.ts); [`src/modules/chat/controller.ts:194-212`](../workspace-resonant/2.0.0-alpha/src/modules/chat/controller.ts) | Persisted append-only run transitions, input revisions, cancellation acknowledgements, outcomes, and reconciliation |
| Persistence | Shell state persists through host state or localStorage and normalizes compute/threads/goals. [`src/core/runtime.ts:1360-1380`](../workspace-resonant/2.0.0-alpha/src/core/runtime.ts), [`src/core/runtime.ts:1876-1945`](../workspace-resonant/2.0.0-alpha/src/core/runtime.ts) | Optional strategy/route/run/notification projections normalized during hydration; never fabricate a running owner |
| Artifacts | Compute artifacts bind job/node/path/hash/retention/sensitivity; Goal artifacts separately project useful results. [`src/core/contracts.ts:1058-1069`](../workspace-resonant/2.0.0-alpha/src/core/contracts.ts), [`src/core/contracts.ts:2040-2048`](../workspace-resonant/2.0.0-alpha/src/core/contracts.ts) | Run outcomes reference owner artifacts; consuming/attaching an artifact must not copy sibling transcripts or imply memory intake |
| Notifications | Manifest requests notification capability; chat has polite live activity/status atoms. [`public/addons/augmentor-chat.json:55-60`](../workspace-resonant/2.0.0-alpha/public/addons/augmentor-chat.json), [`src/modules/chat/StrategistChatRail.tsx:596-603`](../workspace-resonant/2.0.0-alpha/src/modules/chat/StrategistChatRail.tsx), [`src/modules/chat/StrategistChatRail.tsx:762-795`](../workspace-resonant/2.0.0-alpha/src/modules/chat/StrategistChatRail.tsx) | No notification state/producer/restoration/control owner exists in the scoped bytes; add a projection owner, not truth-bearing execution state |
| Real child start | Engineer and Hermes replies explicitly say execution has not started. [`src/core/delegation.ts:582-604`](../workspace-resonant/2.0.0-alpha/src/core/delegation.ts) | Actual owner launch operations and correlation handles for both children |

## Exact adapter boundaries

1. `StrategyAdmissionAdapter`

   Reads installed capability/operation availability and exact versions. Produces availability only; it cannot install, approve, dispatch, or execute.

2. `StrategyProjectionAdapter`

   Persists preview, immutable route decision, approval reference, dispatch digest, and current owner correlations in `ResonantShellState`. It owns projections, never authoritative Dispatch/Orchestrate state.

3. `OrchestrateHostAdapter`

   Consumes validated Orchestrate actions. For every child, creates a bounded `DelegationPacket`, optional `TaskWorkspace`, and invokes one existing execution owner. Returns identifiers only.

4. `RunReconciler`

   Polls/subscribes to owner truth, appends transitions, and quarantines contradictory or late outcomes. It cannot infer success from a workspace, notification, or stale local state.

5. `ResultProjectionAdapter`

   Converts owner artifact/blocker handles into Goal/chat/run projections. Explicit attach or consume remains separate from checkpoint or memory intake.

Provider selection remains host-mediated, as required by the Augmentor connector contract. [`public/addons/augmentor-chat.json:169-185`](../workspace-resonant/2.0.0-alpha/public/addons/augmentor-chat.json)

## Per-child owner mapping

Each child needs a distinct immutable `childId` and attempt `runId` with:

- `GoalWorkspace`: parent supervisory reference through `threadId`, step owner, artifact/blocker, and `delegationRefs`; never execution truth.
- `DelegationPacket`: exact mission, snapshot/context references, allowed/forbidden scope, capability grants, provider/cost/approval policy, expected artifacts, verification, return protocol.
- `TaskWorkspace`: packet/task/result/verification filesystem envelope only.
- `Dispatch/Orchestrate`: authoritative capability/action/join identity, referenced by digest/handle; do not copy their policy into ResonantOS.
- `ComputeJob`: only when the chosen owner executes through compute; bind `consumerId`, approval, timeout/cancellation, artifact policy, and status.
- Provider owner: resolves model/runtime through current host provider policy; the strategy must not choose around it.
- Artifact owner: ComputeArtifact/TaskWorkspace result remains authoritative; Goal/chat holds references.
- Approval owner: one approval binds frozen proposal/dispatch input; each protected owner still enforces its own action gate.
- Notification owner: projects attention from an observed transition; cannot mutate run state.
- Parent interaction: retains its own thread and foreground chat run; no transcript merge from either child.

## Proposed state and events

Minimum persisted records:

- `StrategyProposal`: ID, request/thread, roles, selectors, scope, expected outputs, join policy, digest, status `preview`.
- `RouteDecision`: immutable candidates/selection/rationale/version.
- `StrategyApproval`: proposal and dispatch digest, actor/time, scope.
- `HostRunProjection`: run/child/attempt IDs, parent thread/goal, dispatch and Orchestrate refs, packet/workspace/job/owner refs, snapshot digest, current observed state, artifact/blocker refs, `resumesRunId`.
- `RunTransition`: append-only sequence/time/from/to/source-owner/evidence handle.
- `RunInputRevision`: addressed child, prior/new snapshot digest, clarification reference.
- `RunOutcome`: terminal state and owner evidence.
- `NotificationProjection`: run/transition reference plus delivery/read state, independent of result consumption.

Suggested legal attempt states:

```text
queued -> running | cancel-requested | blocked | failed
running -> awaiting-user | cancel-requested | blocked | succeeded | failed
awaiting-user -> running | cancel-requested | blocked | failed
cancel-requested -> cancelled | cancellation-unknown
```

Terminal attempts never reopen.

## Restart, cancel, clarification, and join

- Restart/reload: hydrate projections, then reconcile every nonterminal attempt with its owner. Unknown owner state becomes `cancellation-unknown`/attention-required, never fabricated `running`.
- Resume: creates a new attempt/run ID with `resumesRunId`; old blocker, artifacts, and transitions remain immutable.
- Cancel: send cancellation through the real execution owner. Mark `cancelled` only after acknowledgement; otherwise `cancellation-unknown`. A sibling continues independently.
- Late result: quarantine after acknowledged cancellation; retain as owner evidence without converting the cancelled attempt to success.
- Clarification: `awaiting-user` belongs to one child. Answer creates an addressed append-only input revision/new snapshot; parent and sibling digests remain unchanged.
- Join: Orchestrate owns mechanical join. Product consumption references a terminal artifact or blocker under explicit `notify`, `manual-consume`, or `join-before-continue`; it never merges child history.
- Parent continuation: requires replacing the global run guard with separate foreground and child-run registries/cardinality, while retaining owner-level concurrency ceilings.

## Smallest ordered implementation slice

1. Refresh consumer from `origin/dev`; run baseline checks.
2. Add public-neutral proposal, immutable route/approval, run-correlation, transition/outcome contracts plus hydration normalization.
3. Add capability/operation discovery and launch-time revalidation; preserve existing explicit-command precedence.
4. Add preview and single exact approval UI. Approval still must not imply execution.
5. Bind one approved action to existing DelegationPacket/TaskWorkspace and show truthfully: workspace created, execution not started.
6. Add one real execution adapter returning existing owner/ComputeJob handles.
7. Replace the global run guard with foreground-versus-child ownership and initial child concurrency ceiling `2`.
8. Add append-only reconciliation, acknowledged cancellation, targeted clarification, terminal blocker, and resume-as-new-attempt.
9. Add notification projections and independent artifact consumption.
10. Prove the literal two-child browser path: strategy child plus Whisper child, parent remains usable, thread switch, one targeted clarification, sibling-independent cancellation/failure, reload restoration, and selective artifact/result consumption.

Slices 1–5 are infrastructure only. Product acceptance begins only after 6–10 execute against real owners.

## Rejected collapses

- No strategy scheduler/queue: Orchestrate plus existing host execution owners schedule and join.
- No duplicated provider, grant, approval, compute, artifact, workspace, or memory policy.
- `TaskWorkspace != execution`; current source says so explicitly.
- `GoalWorkspace != run`; it is supervision and projection.
- Notification/read state != run truth or result consumption.
- Preview/confidence != approval.
- Result consumption/attachment != memory intake.
- The stale local checkout cannot establish current implementation status.

## Freshness prerequisite

Local consumer state:

- branch: `dev`
- HEAD: `6f92af7b32b17d2eef66230d463eb8b6a21a98f7`
- upstream: `origin/dev` at `3b07e635d596c18f9a047ef5921892acc7cba4ff`
- status: behind by seven commits.

The seven commits are `328d8ac` through merge `3b07e63`. A scoped `git diff --quiet HEAD..origin/dev` over all inspected runtime sources and the Augmentor manifest returned exit `0`, so those exact seams are byte-unchanged upstream. However, upstream changes `package.json` and browser/approval/security files. Therefore the current tracing is useful evidence but implementation must refresh/rebase and rerun validation before claiming current behavior.

## Validation and blockers

Validation performed:

- Read consumer operating contract.
- Recorded branch, worktree, local/upstream hashes, and seven-commit log.
- Inspected exact contracts, compute, goal, delegation, runtime persistence, controller, run guard, Augmentor manifest, and chat UI owners.
- Verified zero scoped runtime diff across the seven upstream commits.
- Confirmed no scoped notification implementation beyond capability declaration and polite UI atoms.
- Confirmed no files were edited.

Blockers to real acceptance:

- no installed/discovered Subagent Strategy runtime profile or operation adapter;
- no persisted immutable proposal/route/approval/run model;
- global single-run guard;
- no real generic child launch/join owner binding;
- no acknowledgement-based cancellation or restart reconciliation;
- no targeted clarification/input revision;
- no notification persistence/restoration/control owner;
- no two-child browser execution proof;
- implementation branch must first absorb the seven upstream commits and rerun repository-required checks.

## Agent 3 — human experience

Explorer report — Ahrens / human experience (spawn-0003)

Timestamp/evidence state: inspected read-only at 2026-07-29T00:08:01-03:00; consumer HEAD `6f92af7b32b17d2eef66230d463eb8b6a21a98f7`. No files edited.

Verdict
The one-conversation experience should be a conversational transition card plus a compact, focus-independent run tray—not an agent console. The target journey is evidence-ready as a proposed acceptance contract, but is not implemented and cannot pass today: current ResonantOS has thread switching and accessible single-run atoms, while `run-guard.ts:8-18` admits exactly one global mutable run token. The accepted blueprint itself says concurrent children, durable ancestry, notifications, join/resume, and the browser witness are absent (`research/...routing-session-fabric/findings.md:5-22,253-259`).

Evidence boundary
- Canonical candidate product evidence: `projects/ide-ergonomics/PRODUCT-VIEW.md:125-176` defines conversation span → route menu → owner-safe preview → explicit choice; preview is not execution. `:184-193` requires role/receipt/join/permission visibility and no spawn before explicit approval. `:226-253` requires users understand why/owner/non-actions and rejects generic launchers and dashboards without a next action.
- Current consumer bytes: `../workspace-resonant/2.0.0-alpha/src/modules/chat/StrategistChatRail.tsx:393-415` implements keyboard-native thread buttons; `:519-575` supplies labeled controls; `:596-603` and `:762-795` supply polite single-run activity/status; `:900-918` supplies one stop-response control. No child tray, proposal editor, targeted clarification, selective result consumption, or resume control was found in these atoms.
- Hard blocker: `../workspace-resonant/2.0.0-alpha/src/modules/chat/run-guard.ts:8-18` rejects every run while any token is active; this prevents parent continuation plus two children.
- Accepted prior blueprint: `research/2026-07-28-augmentor-routing-session-fabric/findings.md:130-148` defines route-card content and snapshot isolation; `:150-172` defines proposed cancel/resume/notification semantics; `:174-189` defines the two-child witness; `:231-247` defines browser/accessibility checks and attention budgets. These are proposals, not current bytes.

Ordinary-language journeys (proposed UI)
1. Preview only — User: “In parallel, prepare a governed strategy proposal and a Whisper page.” Inline transition card says “Proposed: 2 background runs; nothing has started.” Default face shows two role names, purpose, expected result, context summary, and one `Review & approve` action. `Not now` dismisses/parks without launch. Expanders reveal exact selectors, forbidden scope, owner, join policy, and receipts.
2. Edit before approval — `Edit plan` opens a semantic form, not JSON/infrastructure: rename/remove/add role; choose “this thread through message X” or selected messages/files; inspect included/excluded context; set read-only/write scope; choose notify/manual-consume/join behavior. Any change updates a visible preview revision and invalidates prior approval. Back returns focus to `Edit plan`.
3. Approve once — One final summary states “Start these 2 runs with this frozen context?” Primary `Approve and start 2`; secondary `Back`. Approval is bound to exact preview bytes and launches both; no per-child confirmation unless a child later requests a new consequential scope. Never infer approval from sending ordinary chat.
4. Keep talking — Card collapses into a two-row tray attached to the parent thread. Composer remains usable. Rows show user states, not infrastructure: `Starting`, `Working`, `Needs your answer`, `Cancel requested`, `Cancelled`, `Could not confirm cancellation`, `Done`, `Blocked`, `Failed`. Progress coalesces in-place; do not stream child transcripts.
5. Switch threads — Thread switch uses existing thread buttons. Runs continue under their original parent; inactive thread gets a bounded count/badge. Switching neither reparents, pauses, injects new-thread content, nor moves focus.
6. Answer one child — A `Needs your answer` row exposes the exact question, child name, why it is needed, and scope effect. `Answer` opens a labeled field. Submission explicitly says “Send only to Strategy run”; sibling snapshot/digest and parent context stay unchanged. No answer broadcast.
7. Cancel/resume — Per-row `Cancel` requires confirmation only when destructive/irreversible risk warrants it. First state is `Cancel requested`; only owner acknowledgement becomes `Cancelled`; otherwise `Could not confirm cancellation` with last verified state/risk. Resume never reopens history: `Resume as new attempt` previews inherited inputs, any changed context, and `resumesRunId`, then requires approval when scope changed.
8. Consume one result — A completed row shows a 1–2 sentence outcome and `Open result`, `Attach to this conversation`, `Keep separate`. Opening is read-only; attaching adds only the selected artifact/summary handle. It must not merge transcript, mark sibling read, resolve sibling blocker, or ingest memory.
9. Capability/host-operation gap — Before approval, say exactly: `Can preview, cannot run here: parallel spawn/join is unavailable` and offer only genuine actions: save/export proposal, run one eligible bounded helper, serialize if semantics permit, or install/harden through the proper owner. After approval/preflight failure, state `No child started`; if partial start occurred, enumerate each child’s last verified state. Never fake fan-out inline.

Progressive disclosure / attention budget
- Default preview: recommendation + reason, two role/purpose/result rows, included-context summary, forbidden-effects summary, approval state. Detail drawers: exact selectors/digests, owner/capability, receipts, join, mutation policy.
- Run tray default: only nonterminal children plus unread terminal/attention items; max two primary actions, remaining actions under `More options`. Infrastructure IDs/logs live under diagnostics.
- Adopt proposed ceilings from findings `:245-249`: route cards ≤20% ordinary turns; clarification ≤5%; ≤2 extra actions for consequential launch; one announcement per meaningful terminal/attention transition; initial concurrency 2; 20 recent terminal runs. Treat these as owner-pending acceptance budgets, not measured performance.

Keyboard/accessibility contract
- All card, tray, edit, approve, cancel, answer, resume, and consume operations are real buttons/fields with visible focus and programmatic names/state (`aria-expanded`, `aria-controls`, status text). Use roving focus only if tray is implemented as a composite; otherwise preserve normal tab order.
- Opening/closing dialogs restores initiating-control focus; async events never steal focus. Escape closes non-destructive disclosure/dialogs but cannot silently decline/cancel.
- Routine progress, completion, blocker, failure, and clarification use coalesced `aria-live=polite`; only imminent destructive/data-loss risk may be assertive. Muted/snoozed events remain discoverable in tray. Reload restores unread state without replaying toast/sound/live-region announcements.
- Reduced motion removes pulses/animated progress while retaining textual state. Do not encode state by color alone. Current polite atoms exist at `StrategistChatRail.tsx:596-603,762-795`, but focus restoration, reduced-motion, per-run mute/snooze, and targeted-answer behavior remain unproved.

Smallest browser-testable two-child witness
Use deterministic local-fixture children A (Strategy) and B (Whisper), not provider/network proof:
1. Enter the ordinary request; assert preview shows exactly A+B and zero spawn events.
2. Edit A’s context selector; assert B snapshot preview unchanged. Approve once; assert exactly two child envelopes with distinct snapshot digests and owner refs.
3. Type/send ordinary parent chat while both run; assert it succeeds and neither child snapshot changes.
4. Switch to another thread; assert both continue, no reparent/context marker leak, no focus steal.
5. Fixture A enters `Needs your answer`; keyboard-answer it while notifications muted; assert only A gets one addressed input event.
6. Cancel A: assert `Cancel requested` then owner-acknowledged `Cancelled`; B survives and completes. Resume A as a new attempt linked to old ID.
7. Reload before consuming B; assert unread projections restore with no duplicate announcement.
8. Consume/attach B only; assert parent gets B artifact handle, A transcript/result and sibling notification/read state remain untouched.
9. Plant unique parent/A/B/other-thread markers; assert containment at snapshots, owner requests/outputs, bounded notification, and explicit attachment.
This is the minimum product witness because it demonstrates launch gating, actual two-child execution, parent continuity, isolation, targeted control, recovery, and selective value. A rendered card, workspace, receipt, or two mocked rows alone fails (`findings.md:231-243`).

Pressure-test failures / blockers
- Hidden fan-out: any child start before the exact `Approve and start 2` event is a blocker.
- Infrastructure dashboard: raw actions, wave IDs, receipts, token counts, or schedulers as primary UI fails PRODUCT-VIEW’s next-action test (`PRODUCT-VIEW.md:244-253`).
- Transcript merge: any sibling/child history copied into parent or memory without explicit attachment/intake is a blocker (`findings.md:146-148`).
- Receipt-only proof: lifecycle receipts support truth but cannot establish composer usability, focus behavior, thread switching, targeted answers, reload restoration, or selective consumption.
- Global run guard: must be replaced/augmented by thread-local foreground ownership plus bounded child run projection before the witness can execute.
- Missing current runtime: durable per-child transitions/ancestry, targeted addressed inputs, notification/read/delivery/consumption separation, cancellation acknowledgement, reconciliation, and resume-new-attempt.
- Accessibility validation gap: no inspected accessibility/browser test currently proves the new journey. Current `run-guard.test.ts` only proves global exclusion and token release.

Validation performed
Read-only source inspection and cross-source contradiction check against current consumer HEAD. No browser execution was claimed because the proposed controls/runtime do not exist. Status: `BLOCKED_CURRENT / READY_AS_ACCEPTANCE_SPEC`; next honest validation is implementation plus the deterministic two-child browser witness above.

## Agent 4 — protocol precedent and degraded mode

## Protocol/degraded-mode explorer report

Completed read-only at `2026-07-29T00:10:15-03:00`. External sources were accessed on `2026-07-29`. No files or external state were changed.

### Verdict

The integration direction is sound only as a proposed adapter contract. It is not currently executable in ResonantOS:

- The dispatch route itself passes deterministic validation: `VALIDATION=pass`.
- Current ResonantOS exposes explicit addon grant states and capability tokens, but no `subagent-strategy` runtime profile or general native multi-agent executor.
- Its chat guard admits only one global active run.
- Therefore the honest first slice is preview/export plus explicit capability-gap reporting. Concurrent two-child execution remains a target acceptance witness, not current behavior.
- A fallback that changes roles, wave order, concurrency, or execution owner after approval is a new proposal. It must be revalidated and explicitly re-approved; it cannot be a silent runtime substitution.

### Current official precedents

| Concern | Official precedent | Pressure-test result |
|---|---|---|
| Routing and handoff | OpenAI Agents SDK distinguishes manager-owned “agents as tools” from control-transferring handoffs, and permits filtering forwarded context. [Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/), [Handoffs](https://openai.github.io/openai-agents-python/handoffs/) | Augmentor must decide whether children remain bounded under a parent or take conversational control. The proposed children should remain parent-owned tools/runs; sibling transcript merging is unjustified. |
| Sessions/threads | Agents SDK sessions are explicit history stores and cannot be layered indiscriminately with server-managed continuation mechanisms. [Sessions](https://openai.github.io/openai-agents-python/sessions/) | Reuse ResonantOS thread/run persistence; do not add a second session store merely to host Subagent Strategy. |
| Parallel execution | Official guidance treats independent parallel agents as code-level orchestration, e.g. `asyncio.gather`, rather than an inherent handoff behavior. [Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/) | Parallelism is a host operation/capacity property. A strategy declaring `parallel` does not prove the host can execute concurrently. |
| Approval/interruption | Pending approvals surface as interruptions; serialized run state can be approved or rejected and resumed. Nested delegated-agent approvals surface on the outer run. [Human-in-the-loop](https://openai.github.io/openai-agents-python/human_in_the_loop/), [Run results](https://openai.github.io/openai-agents-python/results/) | Supports the local “proposal → explicit approval → execution” split. Decline must terminate or return to editing without spawning. Approval belongs to the parent run, not a child. |
| Task lifecycle/reconnect | A2A defines task/context identity, interrupted `input-required`/`auth-required` states, terminal completed/failed/canceled/rejected states, artifacts, polling, streaming, and push updates. [A2A specification](https://a2a-protocol.org/dev/specification/) | ResonantOS needs durable child/run correlation and reconciliation. A reconnect cannot infer “still running” from stale UI state. |
| Durable task retrieval | MCP Tasks defines durable task IDs, polling, deferred results, timestamps, TTL, terminal immutability, auth-context binding, and optional notifications that clients must not rely upon. It is explicitly experimental. [MCP Tasks](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks) | Persist authoritative run state and reconcile by ID; notifications are projections, not truth. MCP supplies precedent, not an implementation owner. |
| Cancellation | MCP requires canceled tasks to remain canceled even if underlying execution later completes; needed data may disappear after cancellation/TTL. [MCP Tasks](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks) | Record cancellation acknowledgement, quarantine late results, and preserve required residue before cleanup. Current local contracts already require timed-out children to receive explicit receipts. |
| Tracing | OpenAI traces runs, agents, tools, handoffs and guardrails; OpenTelemetry correlates distributed spans through propagated trace context. [OpenAI tracing](https://openai.github.io/openai-agents-python/tracing/), [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/) | Carry `dispatch_id`, run/action/agent IDs, thread/context ID and parent-child causality. Traces remain observability, never lifecycle authority. |
| Independent approval | GitHub protected environments can require approval, withhold secrets until approval, and prevent initiators from self-approving. [GitHub environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) | Reinforces independent final approval and “approval unlocks capability” semantics, but does not define local eligibility or promotion authority. |

### Explicit degraded-mode table

| Condition | Honest disposition | Required behavior |
|---|---|---|
| Capability absent | Proposal export, then optional install/hardening offer; otherwise hard block | Show the missing capability and owner. Do not label a generic model call as Subagent Strategy execution. Installation is a separate authorized lifecycle. |
| Required host operation absent | Hard block for the approved capability-bound route | Orchestrate requires native spawn, wait, interrupt and inventory. Record missing operations and zero spawn attempts. A nested CLI or inline imitation is forbidden. |
| User declines | No execution; retain or discard proposal according to user choice | No registration or spawn. Rejection is not a failed child run. Editing later creates a newly validated proposal. |
| Validation failure | Hard block; bounded repair proposal | No execution plan and zero spawns. Preserve validator defects. Revalidate exact revised bytes and seek new approval. |
| Partial child failure | Partial terminal result plus blocked dependent wave | Preserve successful sibling receipts, failed-child residue and confidence limit. Current route’s `join_policy=all` and `on_incomplete=block` prohibit synthesis from proceeding. |
| Timeout | Interrupt once, emit explicit `timed_out` receipt, block dependents | Never convert silence into success. Preserve pending identity, interruption event, residue and reroute. |
| Reconnect/reload | Reconcile persisted run/task IDs with the owner; show unknown if unprovable | Do not fabricate running state from a restored UI projection. Late results after acknowledged cancellation must not reopen the canceled run. |
| Parallelism unavailable before approval | Offer a serial route only if dependencies and semantics remain valid; otherwise export/block | Serial execution changes the strategy’s wave/concurrency contract, so present it as a revised proposal and reapprove. |
| Parallelism exhausted after approval | Do not silently serialize | For this route, block/preserve residue because every wave says `on_incomplete: block`. A retry or serial alternative requires a new proposal unless a pre-approved bounded queue policy exists. |
| Exactly one bounded helper suffices | Use one helper outside dispatch lifecycle | Honest only when scope remains within the parent, no multi-lane synthesis/independent tension requirement remains, and the user’s requested outcome is still met. Report helper closeout post hoc. |
| General capability exists but lacks medium/complex proof | Hardening offer or explicitly experimental proposal | Do not claim promotion/readiness. A proposal-only or fixture lane may continue without claiming product execution. |

### Local contract comparison and exact selectors

- Public lifecycle ownership and one-helper exception: `.agents/skills/subagent-strategy/SKILL.md:67-88`.
- Exact validation, tension, confirmation/freeze, registration and dependency process: `.agents/skills/subagent-strategy/SKILL.md:91-107`.
- Partial-result preservation and complete closeout: `.agents/skills/subagent-strategy/SKILL.md:102-106`.
- Dispatch authorization and lifecycle receipt requirements: `arcanum/formulae/dispatch-spec/SKILL.md:87-101`.
- Parent-owned execution and non-self-approval: `arcanum/formulae/dispatch-spec/SKILL.md:126-150`; `.agents/skills/subagent-strategy/SKILL.md:103-105`.
- Orchestrate’s validator/authorization/host-operation preflight: `.agents/skills/orchestrate/SKILL.md:79-89`.
- Missing-operation hard block and forbidden nested fallback: `.agents/skills/orchestrate/SKILL.md:85-105`, `134-140`.
- Timeout/interruption and dependent-gate withholding: `.agents/skills/orchestrate/SKILL.md:121-131`.
- Proposed protocol lane: `dispatch-sheet.json:72-73`.
- Approved execution shape: `DISPATCH-ROUTE.json:308-378`; every wave has `join_policy: all` and `on_incomplete: block`.
- Current discovery record explicitly says no runtime profile/general executor/degraded contract: `strategy-inventory-packet.json:142-169`.
- Current single-run guard: consumer `src/modules/chat/run-guard.ts:8-17`.
- Current explicit grant states: consumer `browser-first/resonantos-side-panel-extension/src/lib/addon-capability-review.js:12-19,42-48`.
- Current bridge tokens include `agent-control-plan` and addon runtime control, but no general subagent-strategy execution capability: consumer `browser-first/host/bridge-capability-tokens.mjs:24-46`.

### Build-from-owned reuse

Reuse:

- ResonantOS capability review and token/grant surfaces for capability discovery and denial/pending presentation.
- Existing thread/run, compute, delegation, workspace, artifact and notification owners identified by the accepted routing/session blueprint.
- Public Subagent Strategy for proposal/confirmation/lifecycle semantics.
- Dispatch Spec for exact route validation.
- Orchestrate’s host-operation preflight, action identity, join reduction and timeout semantics.
- Existing telemetry correlation surfaces, extended with dispatch/wave/action/agent identifiers.

Do not create another scheduler, registry, session store, job model, artifact owner, approval authority, or memory intake path.

### Local obligations external precedents cannot satisfy

External protocols do not establish:

- which ResonantOS capability grants authorize each child operation;
- the local runtime-profile schema and deterministic admission validator;
- exact mapping from Dispatch actions to ComputeJob, DelegationPacket, TaskWorkspace and GoalWorkspace;
- local agent eligibility, final-approver eligibility, or registration ledger ownership;
- context snapshot and sibling-isolation rules;
- publication/private-boundary rules;
- result-consumption versus memory-intake separation;
- the browser-visible two-child acceptance witness;
- deterministic reconciliation and late-result quarantine against current persistence;
- performance, attention, concurrency and retention budgets;
- medium/complex live evidence or release/promotion readiness.

### Validation and blockers

- Deterministic check: `python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py research/2026-07-28-augmentor-subagent-strategy-integration/DISPATCH-ROUTE.json`
- Result: `VALIDATION=pass`.
- This proves route shape only. It does not prove a ResonantOS runtime profile, host operations, concurrent execution, reconnect behavior, or product acceptance.
- Blocking product gaps: no consumer runtime profile; no general executor binding; one global chat-run token; no accepted degraded-mode/reconciliation contract; no live two-child browser proof.
- Research-lane result: complete, read-only, with no write residue.
