# Two-Lane MVP Research Returns

Dispatch ID: `2026-06-19-ide-ergonomics-mvp-two-lane`
Route dispatch ID: `ide-ergonomics-mvp-two-lane-20260619T172822Z`
Status: lanes completed

## Anti-Bias Gate

- Checker agent `019ee10c-231d-7042-814f-b19b9d95b974` returned PASS.
- Reviewer agent `019ee10c-2684-74f3-b7f1-4fdbfaf821cd` returned PASS.
- The accepted tension axis was `methodology`: adversarial current-MVP validation
  against alternative first-proof exploration.

## Lane Z: MVP Validator

Runtime agent: `019ee10d-f235-7e31-81a6-052e8ce65504`
Pool name: `Bell, John S.`
Role: `lane-z-mvp-validator`

### RZ-1 Strongest Current MVP

The strongest version of the current three-card MVP is not three unrelated
widgets. It is one IDE action-card substrate tested across three transition
classes:

- knowledge capture through a definition candidate;
- lifecycle continuation through a handoff composer;
- delegation safety through a subagent preview.

The strongest claim it could prove is that conversation spans can become
owner-safe action frames without canonical mutation or hidden runtime execution.

### RZ-2 Toy Scenario

A user says: "This route keeps using evidence rail; make sure the next session
can continue, and maybe split a research lane for host APIs."

The three-card MVP can highlight `evidence rail` as a definition candidate,
draft a next-session handoff with source refs and gaps, and preview subagent
roles and receipts without spawning until approved. In this scenario the MVP
feels useful and preserves boundaries.

### RZ-3 Counterexample

A user says: "I am not sure whether this should be invoke, dispatch-spec,
task-session, side note, or just keep chatting."

The current three-card MVP has no first-class route-menu card and no side-node
capture, even though the underlying problem explicitly includes route and side
node recognition. It may offer handoff or definition too early, or escalate to
subagent preview when the real need is route disambiguation.

### RZ-4 Failure Interpretation

If the current MVP fails, it fails to prove the underlying problem: that IDE
assistance can notice and route workflow transitions broadly. It only proves
that three attractive actions can be previewed safely. It does not prove
detection coverage for route ambiguity or side-node capture, nor that subagent
preview belongs in the first proof.

### RZ-5 Repaired MVP

The repaired MVP is a single conversation transition card with a bounded route
classifier and preview frame.

Required classes:

- definition candidate;
- handoff;
- route menu;
- side node;
- delegation preview.

In the first implementation, only definition and handoff need to produce draft
artifacts. Route and side node may be preview-only. Delegation remains
permission-gated and non-runtime.

### RZ-6 Scores

| Candidate | Value Signal | Proof Cost | Boundary Safety | Owner Clarity | Implementation Surface | Recomposition |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Current three-card MVP | 4 | 3 | 4 | 4 | 2 | 4 |
| Repaired transition-card MVP | 5 | 4 | 5 | 5 | 4 | 5 |

Lane Z blockers:

- Current MVP omits route and side node, two named transition types from the
  underlying problem.
- Subagent fanout preview is too governance-heavy for the first proof unless
  it stays preview-only.

Lane Z residue:

- Host-specific feasibility was not verified.
- No runtime IDE, browser, or subagent execution evidence was gathered.

Lane Z reroute:

- Replace the current three-card MVP with the repaired transition-card MVP, or
  at minimum swap subagent preview for route menu in the first proof.

## Lane A: Alternative Angles

Runtime agent: `019ee10d-f31a-7272-954a-d0d0cf7bcd2e`
Pool name: `Abramsky, Samson`
Role: `lane-a-alternative-angles`

### RA-1 Strongest Challenge

The three-card MVP proves three attractive downstream widgets, but the
underlying problem is upstream recognition and routing. It omits two central
failure modes named by the problem itself: "this is a route ambiguity" and
"this is a side node." Subagent preview is also too expensive and
permission-heavy for a first proof.

### RA-2 Alternative Scores

| MVP Angle | Value Signal | Proof Cost | Boundary Safety | Owner Clarity | Implementation Surface | Recomposition |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Bounded route-menu MVP | 5 | 4 | 5 | 5 | 4 | 5 |
| Side-node capture MVP | 4 | 5 | 5 | 5 | 5 | 4 |
| Evidence/receipt rail MVP | 4 | 4 | 5 | 4 | 4 | 5 |
| Handoff-first MVP | 4 | 4 | 5 | 4 | 4 | 4 |
| Current three-card MVP | 4 | 2 | 4 | 4 | 2 | 5 |

### RA-3 Strongest Alternative

The strongest alternative is the bounded route-menu MVP. First proof: detect a
conversation span and offer a small owner-safe route menu:

- definition candidate;
- side node;
- handoff;
- delegate preview;
- park or ignore.

This validates the recognition and routing problem before investing in polished
per-route widgets.

### RA-4 Second Strongest Alternative

The second strongest alternative is side-node capture. It cheaply tests whether
IDE ergonomics can prevent useful context from either derailing the active flow
or disappearing. It has clear Necronomicon ownership and composes naturally
into later route menus and handoffs.

### RA-5 Rejected Alternatives

- Definition-only MVP: safe and cheap, but too narrow. It proves the definitions
  workflow, not general conversation-to-owner routing.
- Knowledge Graph side-panel proof: valuable later, but too much visualization
  and state surface for first validation.
- Generated host-rules package before UI: low implementation cost, but weak
  value signal. It tests packaging, not live recognition.
- Subagent-first MVP: too expensive and permission-heavy for a first proof. It
  is better as a preview route behind a route-menu item.
- Full three-card build: broad and appealing, but likely to validate
  presentation breadth rather than the smallest proof of the underlying
  problem.

### RA-6 Residue And Reroute

Residue:

- Host-specific IDE affordances were not verified.
- No toy UI or browser/IDE proof was run.
- Scoring is artifact-grounded strategy judgment, not implementation evidence.

Reroute:

- Replace the current MVP with a narrower bounded route-menu over conversation
  span, optionally with side-node capture as the first implemented route.
- Defer subagent fanout preview until route-menu value is shown.
