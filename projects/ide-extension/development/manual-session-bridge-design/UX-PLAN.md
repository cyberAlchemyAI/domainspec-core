---
template_id: invoke.ux-plan
template_type: ux-plan
status: approved-instance
authority_level: invoke-local
project: ide-extension
updated_at: 2026-07-12
---

# UX Plan: Manual Codex Session Bridge

## User Goals

| Goal | Actor | Success signal |
| --- | --- | --- |
| State a real task instead of accidentally accepting a default. | Human operator | Proposal cannot be prepared until a visible task field contains intentional text. |
| Choose a skill privately and reveal it only after an explicit poll. | Human operator | Skill is absent from pre-claim agent responses and present in the claim packet. |
| Know whether approval, target selection, claim, execution, recovery, or evidence is pending. | Human operator | Each lifecycle state has distinct status and action language. |
| Run exactly one approved request in the intended session. | Active Codex session | One claim succeeds; duplicate claim receives a conflict without a skill packet. |
| See authorization and execution as separate evidence. | Human operator | Both receipts appear with different kinds and claims. |

## Actors

| Actor | Needs | Constraints |
| --- | --- | --- |
| Human operator | Clear task entry, private skill choice, exact approval scope, visible progress, recoverable failure. | Must trigger poll in chat; local approval is unattested. |
| Active Codex session | One ready handle, atomic claim, late-disclosure packet, result/interrupt endpoint. | Must not inspect before poll, choose among proposals, self-release, or widen effects. |
| Local kernel | Valid payloads, deterministic transitions, bound evidence, replay rejection. | Does not resolve skills or execute agent code. |

## Journeys

| Journey | Start state | End state | Notes |
| --- | --- | --- | --- |
| Prepare and approve | Empty form | `approved` | Task is visibly labeled and required; approval creates authorization receipt only. |
| Select poll target | `approved` | `ready_for_poll` | Desk permits exactly one target and rejects silent replacement. |
| Poll and claim | `ready_for_poll` | `claimed` | Operator says `poll`; claim response is first skill disclosure to session. |
| Execute and return | `claimed` | terminal | Session follows skill within grants and posts a bound result. |
| Recover interrupted claim | `interrupted` | `approved` | Human releases/requeues; attempt history and authorization receipt remain visible. |
| Reject | `awaiting_approval` | `blocked` | Skill is never disclosed through the bridge claim API. |
| Handle unsupported effects | `claimed` | `blocked` | Desk explains that write/network effects are outside the first bridge. |

## Surfaces

| Surface | Purpose | Entry points | Exit points |
| --- | --- | --- | --- |
| Prepare header/bar | Capture task and skill slug. | Empty local workbench. | Prepared proposal or inline validation error. |
| Proposal queue | Compare awaiting, approved, ready, claimed, interrupted, and terminal requests. | Prepare/refresh/history. | Proposal detail. |
| Proposal detail | Inspect task, skill, grants, receipts, claim attempts, result, and evidence. | Queue selection. | Approve, reject, ready/unready, release/requeue, inspect evidence. |
| Codex chat | Receive explicit `poll` trigger and report immediate execution progress. | Operator message. | Bound result posted to kernel and concise chat result. |
| Evidence rail | Distinguish authorization receipt from execution receipt and attempt artifacts. | Approved or terminal proposal detail. | Authorization/attempt/result/receipt views. |

## State Model

| State | User meaning | Allowed transitions | Error behavior |
| --- | --- | --- | --- |
| `awaiting_approval` | Prepared but not authorized. | approve, reject. | Run/claim rejected. |
| `approved` | Human authorized; no poll target selected. | ready, reject. | Duplicate approval or direct claim rejected. |
| `ready_for_poll` | Human selected this exact proposal for the next poll. | unready, claim. | Second ready target and wrong-target claim rejected. |
| `claimed` | An unattested session received the execution packet. | terminal result, interrupt. | Duplicate claim rejected without packet. |
| `interrupted` | Claim ended without a terminal result. | operator release/requeue. | Session self-release and automatic retry rejected. |
| `passed` | Skill completed within approved boundary. | history only. | Further result rejected. |
| `flagged` | Skill completed with named residue. | history only. | Further result rejected. |
| `blocked` | Skill or bridge correctly refused. | history/new proposal. | Reason remains visible. |
| `failed` | Unexpected execution or validation failure. | history/new proposal. | Evidence omits secrets and preserves bounded diagnostics. |

## Interaction Flows

| Flow | Steps | Risk | Recovery |
| --- | --- | --- | --- |
| Prepare | Enter task -> enter skill -> review grants -> Prepare proposal. | Generic/default task hides missing intent. | Empty default, visible label, required validation, focus task on error. |
| Approve | Select proposal -> inspect contract -> Approve proposal -> authorization receipt. | `Approve no-op` misstates skill request or receipt. | Dynamic truthful label and separate authorization evidence. |
| Target | Select approved proposal -> Ready for poll. | More than one target or silent replacement. | Kernel singleton constraint; explicit Unready action. |
| Poll | Say `poll` -> inspect singleton ready handle -> claim -> reveal skill. | Zero/stale/multiple ready targets. | Return conflict without skill packet; repair target in desk. |
| Return | Run skill -> post result -> refresh detail/evidence. | Chat says done while kernel has no result. | Session must attempt result post before claiming terminal success. |
| Recover | Session reports interruption -> desk shows interrupted -> human releases/requeues. | Silent duplicate execution. | Operator-only action, attempt ledger, read-only scope. |

## Content Requirements

| Content | Surface | Purpose | Constraint |
| --- | --- | --- | --- |
| `Proposal task` | Prepare form | Make task entry discoverable. | Visible label; empty by default; required; 240 characters maximum. |
| `Skill slug` | Prepare form | Capture private late-disclosure capability handle. | Safe slug pattern; no dropdown of real skills. |
| `Prepare proposal` | Prepare form | Create proposal without implying execution. | Disabled or rejected when task is blank. |
| `Approve proposal` | Detail action | Authorize exact task/skill/grants. | Never says `Approve no-op` for a skill request. |
| `Approved - select as poll target` | Detail status | Separate authorization from target selection. | Does not imply this proposal will be polled. |
| `Ready for poll` | Detail status | Identify the singleton request the next poll may claim. | Exactly one across the local workbench. |
| `Claimed by unattested local session` | Detail status | Show bridge ownership honestly. | Does not claim authenticated identity. |
| `Release and requeue` | Interrupted detail action | Allow explicit human recovery. | Never available to the claiming session. |
| Result status and summary | Detail/evidence | Report actual execution. | Bound to execution receipt; no full prompt/transcript. |

## Accessibility Considerations

| Consideration | Applies to | Required response |
| --- | --- | --- |
| Programmatic and visible labels | Task and skill inputs | Use associated labels; placeholder is not the only label. |
| Keyboard order | Prepare bar and approval actions | Task -> skill -> prepare; detail controls follow document order. |
| Status changes | Server, approval, target, claim, interruption, result | Announce concise changes through existing live regions without stealing focus. |
| Error association | Required task and invalid skill | Tie error text to the field and focus the first invalid control. |
| Narrow viewport | Header controls | Stack labeled fields with stable button dimensions and no horizontal overflow. |

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| A hidden/private skill field becomes visible in browser history. | Local shoulder-surfing exposure. | Clear the field after prepare; do not store it in browser local storage. |
| User confuses approval with execution. | False completion belief. | Distinct status, event, and receipt language. |
| Stale ready target blocks newer work. | Poll cannot reach intended task. | Show singleton target globally and provide explicit Unready. |
| Requeue repeats a read-only attempt. | Duplicate observations or cost. | Record attempt count and require operator release. |
| A skill blocks due read-only grants. | User perceives bridge as broken. | Show exact missing effect class and route to a new explicitly scoped proposal later. |

## Acceptance Signals

| Signal | Evidence | Owner |
| --- | --- | --- |
| Task field is unmistakable and required. | Playwright desktop/mobile assertions and screenshot. | ide-extension UI. |
| Approval does not terminalize proposal. | API lifecycle test and projected status. | local kernel. |
| Pre-claim response omits skill. | Contract test over claimable-list endpoint. | bridge API. |
| Exactly one poll target exists. | Singleton target transition and hostile replacement tests. | projector/storage. |
| Duplicate claim discloses nothing. | Concurrency/replay test. | projector/storage. |
| Interrupted claim requires operator recovery. | Actor-separation and requeue history tests. | kernel/workbench. |
| Result appears as execution evidence. | API, artifact, and Playwright history test. | kernel/workbench. |

## Handoff Boundaries

- Architecture handoff: satisfied by [ARCHITECTURE-BUNDLE.md](ARCHITECTURE-BUNDLE.md).
- Implementation-plan handoff: ready; design approval is recorded in `DECISIONS.md`.
- Research handoff: deferred; no external API claim is required for the manual L0 bridge.

## Gate Result

- Status: `pass` for the manual read/preview workflow.
- Reason: actors, surfaces, states, content, errors, and acceptance evidence are
  specified; mutation-capable effects and automatic workers remain outside the
  selected journey.
