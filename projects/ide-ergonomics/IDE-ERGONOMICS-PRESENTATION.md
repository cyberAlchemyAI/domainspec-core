# IDE Ergonomics
## Flow with receipts inside the IDE

A presentation about what the end user actually sees when an AI chat turns into governed work.

Status: product strategy. Not yet a runtime IDE plugin.

---

# Before
## The user has to hold the whole workflow in their head

Example chat moment:

```text
User: That phrase "evidence rail" might matter later.
Also, the observability tangent is useful, but keep working on the routing card.

Assistant: We should probably define it, save the tangent,
and prepare a handoff for next session.

User: Which Arcanum route owns this?
I do not want it to silently become a canonical definition.
```

The session is productive, but the useful residue is scattered across chat and memory.

---

# What The User Sees
## A small card appears on the live phrase

```text
Possible workflow transition detected

Span: "evidence rail"

1. Create definition candidate      -> draft packet, no promotion
2. Save observability tangent       -> side node, active task unchanged
3. Prepare next-session handoff     -> memo with refs, gaps, restart prompt
4. Preview delegated lanes          -> roles and receipts, approval required
```

The user sees practical choices with the result and the boundary attached.

---

# Example Result 01
## The user clicks: create definition candidate

What gets created:

```text
Definition candidate: evidence rail

Source span:
"the evidence rail should show what was run, proposed, or blocked"

Owner:
Definitions Governance

Draft meaning:
A side surface that keeps receipts, gaps, and proof status visible beside the work.

Blocked action:
No canonical promotion until the owner route approves it.
```

Nothing canonical changed.

---

# Example Result 02
## The user saves a tangent without losing the main task

What the side-node queue shows:

```text
SIDE NODE
Observability tangent
Why do failed routes leave weak receipts?

SOURCE
Chat span 14:22
Captured from current IDE session.

NEXT
Revisit after card MVP
Can feed evidence-rail design later.
```

The active task stays open.

---

# Example Result 03
## The user ends the session with a real restart surface

What the handoff draft contains:

```text
Handoff: transition-card proof

Start prompt:
Open the card fixture set and test one span: "evidence rail".

Open calls:
Does the route menu need 4 choices or 6?

Source refs:
PRODUCT-VIEW.md, ERGONOMICS-OPPORTUNITIES.md, current chat span.

Boundary:
Drafting the handoff does not mean the fixture passed.
```

The next session starts from the work, not from memory.

---

# Example Result 04
## Delegation becomes readable before it becomes expensive

What the delegated-lane preview shows:

- Research lane: check fixture examples for route ambiguity. Receipt: 3 cards with owner and blocked action.
- Design lane: stress the card layout against handoff and side-node cases. Receipt: screenshot plus failure notes.
- Validation lane: run the static proof and mark pass, flag, or block. Receipt: fixture table.
- User gate: choose "Approve fanout" or "Keep single-lane". No spawn from preview alone.

The user approves a route only after seeing what each lane owes.

---

# Example Result 05
## A knowledge search becomes a reusable reference

What the knowledge popup shows:

```text
knowledge: operational ontology lifecycle

Surface:
Inventory evidence-card

Authority:
Read model, not definition promotion.

Actions:
Open entry, copy handle, add to handoff, refresh search.

Warning:
Marks stale if index changed since the query.
```

The user can reuse knowledge without leaving the work surface.

---

# Example Result 06
## The user starts work and gets a ranked next move

What Connective recommends:

```text
Recommended next

1. Run focused validation sweep
   Why: high domain priority, low ambiguity, fits 45 minutes.
   Expected receipt: command output plus screenshot.

2. Ask one decision-gate question
   Why: use if validation hits the hosted-preview blocker.

3. Defer high-ambiguity design
   Why: important, but wrong task shape for this session.
```

The result is a recommended lane, not automatic execution.

---

# Example Result 07
## The user marks intent before the agent misreads it

What the validator reports:

```text
User span:
[literal] "owner-safe preview"

Check:
Verbatim diff found the exact phrase.

Result:
PASS for literal span.

Boundary:
Goal and constraint checks remain flag-grade until grounded.
```

Exact text stays exact; flexible goals stay flexible.

---

# End-User Result
## After ten minutes, the session has durable outputs

```text
CANDIDATE
Definition: evidence rail
Drafted with source span, owner, and blocked promotion.

SIDE NODE
Observability tangent
Parked without changing the active task.

HANDOFF
Transition-card proof restart
Next prompt, open calls, refs, and boundaries.

DECISION
Delegation not approved yet
Role lanes previewed; no agents spawned.
```

The workbench is cleaner than the chat that produced it.

---

# Before And After
## The difference is visible in the user's workbench

Before:

- "evidence rail" is somewhere in chat.
- The next session reconstructs context manually.
- Delegation pressure is vague.
- The user remembers what not to promote.

With IDE Ergonomics:

- The definition candidate has owner and source attached.
- The side node is parked and visible.
- The handoff opens with a restart prompt and refs.
- The non-action is explicit: delegation is previewed, not approved.

---

# First Demo
## The proof should look like a usable session, not a system diagram

1. Select a phrase: the user highlights "evidence rail" in a static chat fixture.
2. Pick a route: the card shows definition, side node, handoff, delegation, and park.
3. Inspect the result: the prototype opens the drafted packet with owner and blocked actions.

The demo passes when a reader can point at the screen and say:

```text
This is what I would get.
This is what did not happen automatically.
This is who owns the next step.
```

---

# Takeaway
## The product is flow with receipts

The end user does not buy a governance model.

They get a cleaner workbench at the exact moment a chat turns into work.

One card. A concrete result. A visible boundary. The next session can continue without archaeology.
