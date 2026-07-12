---
id: ide-extension-manual-session-bridge-decisions
project: ide-extension
title: "Manual Session Bridge Decision Gate"
status: approved
node_type: decision-record
updatedAt: 2026-07-12
decision_gate_result: pass
---

# Decision Gate: Manual Codex Session Bridge

## Target Scope

Close every blocker-level design decision required to move the manual session
bridge from Invoke design `flag` to design `pass` before implementation
planning.

## Prior Approved Boundary

The operator had already selected the manual current-session bridge:

- browser approval does not automatically invoke an agent;
- the operator explicitly says `poll` in the intended Codex session;
- persistent workers and server push are deferred.

Source: operator response, `1 we should this first poll thing`, 2026-07-12.

## Resolved Blocker Decisions

### DG-MSB-001: Initial Effect Boundary

**Question:** What effects may the first bridge execute?

| Option | Benefit | Cost/risk | Selection |
| --- | --- | --- | --- |
| Read/preview only | Truthfully demonstrable without claiming the server sandboxes Codex. | Mutation-needing skills return `BLOCK`. | selected |
| Cooperative workspace writes | Immediately more useful. | Scope is advisory and could be mistaken for enforcement. | rejected |
| Require enforceable executor first | Strong effect isolation. | Blocks the manual proof and pulls worker/SDK architecture into L0. | rejected |

- Decision: L0 permits `skill.invoke` plus `preview.read` only.
- Rationale source: operator selected option 1 after trade-offs were presented.
- Downstream effect: write, shell mutation, network, provider, browser-act,
  commit, push, publication, and external-account effects must return `BLOCK`.

### DG-MSB-002: Approval Evidence Model

**Question:** What durable evidence should approval create?

| Option | Benefit | Cost/risk | Selection |
| --- | --- | --- | --- |
| Authorization event/artifact only | Smallest schema and one receipt meaning. | Approval is less visible in receipt-oriented audit views. | rejected |
| Separate authorization and execution receipts | Explicitly preserves both human authorization and actual execution evidence. | Adds two receipt types and UI/schema complexity. | selected |

- Decision: approval mints an `authorization.receipt`; a later admitted result
  mints a separate `skill.execution` receipt.
- Rationale source: operator selected option 2 after trade-offs were presented.
- Downstream effect: neither receipt may substitute for the other, and the
  authorization receipt must not carry an execution `passed` claim.

### DG-MSB-003: Lost Claim Recovery

**Question:** What happens when a claiming session disappears?

| Option | Benefit | Cost/risk | Selection |
| --- | --- | --- | --- |
| Explicit operator release and requeue | Human-controlled recovery without timers or silent retries. | Adds release/requeue states and controls. | selected |
| No L0 recovery | Smallest implementation. | Ordinary interruption permanently strands the request. | rejected |
| Timed claim lease | Automatic recovery. | Adds clock, heartbeat, expiry, and duplicate-execution complexity. | rejected |

- Decision: only the operator may release an interrupted claim and requeue the
  request.
- Rationale source: operator selected option 1 after trade-offs were presented.
- Downstream effect: because L0 is read/preview-only, the same authorization may
  be reused after explicit release; every claim attempt and release remains in
  the event ledger. Mutation-capable layers must define a stricter retry policy.

### DG-MSB-004: Session Assurance

**Question:** How strongly must L0 identify the claiming Codex session?

| Option | Benefit | Cost/risk | Selection |
| --- | --- | --- | --- |
| Unattested local session | Fits loopback, manual poll, and read-only proof with minimum overhead. | Another local process could impersonate the claimant. | selected |
| Human-paired one-time token | Proves token possession. | Adds friction and still does not authenticate Codex itself. | rejected |
| Authenticated runtime integration | Stronger process identity. | Blocks L0 and requires CLI/SDK integration first. | rejected |

- Decision: record caller-generated `session_ref` with
  `assurance: unattested`.
- Rationale source: operator selected option 1 after trade-offs were presented.
- Downstream effect: UI and receipts must never describe the session as
  authenticated; remote or mutation-capable use remains blocked.

### DG-MSB-005: Multiple Approved Requests

**Question:** What should plain `poll` do when multiple approved requests exist?

| Option | Benefit | Cost/risk | Selection |
| --- | --- | --- | --- |
| Ask in chat using opaque handles | No extra browser state. | Adds a second chat decision and possible handle confusion. | rejected |
| Automatically claim oldest | Fastest path. | Can execute the wrong approved task. | rejected |
| Require Approval Desk target selection | The human chooses the exact poll target before chat polling. | Adds `ready_for_poll` state and UI action. | selected |

- Decision: the operator must mark exactly one approved proposal
  `ready_for_poll` in the Approval Desk before saying `poll`.
- Rationale source: operator selected option 3 after trade-offs were presented.
- Downstream effect: the kernel rejects a second ready target until the first is
  explicitly unmarked, claimed, rejected, or completed. The poll API returns no
  skill and no claim packet when zero or multiple ready targets exist.

## Deferrable Decisions

| Decision | Deferred to | Reason |
| --- | --- | --- |
| Timed claim leases and automatic reclaim | L1 reliable local bridge | Explicit operator recovery is sufficient for L0. |
| Authenticated session identity | L2/L3 executor/session architecture | L0 is loopback, manual, unattested, and read-only. |
| Mutation-capable skill effects | L2 enforceable executor | Current server cannot constrain the active Codex tool surface. |
| Persistent worker or server push | L3 packaged routing | Operator selected manual poll first. |
| Exact numeric layer label in top-level spec | Invoke plan/spec delta | Does not alter the selected architecture or acceptance behavior. |

## Assumptions Recorded

- Skill resolution remains owned by the active Codex runtime and occurs only
  after successful claim.
- Proposal task is visibly labeled, empty by default, and required.
- Full prompts, secrets, and model transcripts remain outside kernel state.
- Authorization can survive an explicit release/requeue only in the read-only
  L0 profile; every attempt remains auditable.
- Marking a second proposal ready fails closed rather than silently replacing
  the existing target.

## Gate Result

- Result: `PASS`.
- Decisions resolved: 5 blocker decisions plus the prior manual-poll boundary.
- Blockers remaining: 0.
- Deferred decisions: 5, each assigned to a later layer or planning delta.
- User override: none.
- Validation:
  - all five blocker questions offered concrete trade-offs and a standing
    `Explain / more context` option;
  - all five operator selections are recorded with rejected alternatives;
  - architecture, UX, glossary, layering, transport, and Invoke result agree;
  - Dispatch Spec validation returned `VALIDATION=pass`;
  - ten package files, six architecture views, five decisions, two receipt
    contracts, relative links, JSON, whitespace, and ASCII checks passed;
  - `git diff --check` passed.
- Next step: reconcile the design package to these decisions, validate it, then
  proceed to `invoke plan` only when requested. Reconciliation and validation
  are complete.
