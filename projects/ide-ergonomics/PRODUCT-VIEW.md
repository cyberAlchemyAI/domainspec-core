---
tags: [ide, product, arcanum, workflow, mvp]
node_type: product-view
is_session: false
layer: product
nature: product-brief
status: draft
created: 2026-06-19
---

# Product View: IDE Ergonomics

## One-Sentence Product

IDE Ergonomics is a routing layer for AI work inside an IDE: when a
conversation produces a definition, side note, handoff, route choice, or
delegation opportunity, it shows a small card that helps the user choose the
right governed next step.

The product is not "another agent button." It is the missing moment between
noticing useful work and safely sending that work to the right place.

## The Story

Imagine you are deep in a development session.

You and the assistant have just uncovered a useful phrase: "evidence rail."
It feels important. It may need a definition later. At the same time, the
conversation has drifted into a side thought about observability. You also know
the next session will need a handoff, and there may be enough uncertainty to
split two research lanes.

Today, you have to hold all of that in your head:

- should "evidence rail" become a definition candidate?
- should the observability tangent be saved as a side node?
- is this handoff-ready, or should the current task continue?
- is this an `invoke`, `dispatch-spec`, `task-session`, or `spellcraft` moment?
- would subagents help, and what receipts would they need?

The work is not blocked because Arcanum lacks structure. The work is blocked
because the right structure is hidden behind the user's memory.

With IDE Ergonomics, the IDE notices the moment and offers a small card:

```text
Possible workflow transition detected

Span: "evidence rail"

Suggested routes:
1. Create definition candidate
2. Capture side node
3. Compose handoff draft
4. Open route menu
5. Preview delegated lanes
6. Park for later
```

Each option shows what will happen, who owns it, and what is not allowed to
happen automatically.

The user stays in flow. The system stays governed.

## What The Product Is

The product is a conversation-transition card.

It appears over a selected or detected span in chat, then answers four
questions:

1. What kind of workflow moment is this?
2. Which routes are available?
3. What artifact would this route draft or preview?
4. What boundary prevents unsafe execution or promotion?

The first version is intentionally small. It can be tested without a full IDE
extension, because the product value is the routing decision itself.

## What People Gain

| Gain | Before | With IDE Ergonomics |
| --- | --- | --- |
| Less cognitive load | The user remembers which Arcanum capability owns each moment. | The card names the likely owner and route. |
| Fewer lost ideas | Side thoughts vanish or derail the task. | Side nodes are captured without switching the active route. |
| Faster handoffs | The user reconstructs context at the end of a session. | Handoff drafts collect source refs, gaps, and next prompt while context is fresh. |
| Safer definitions | Important terms are either missed or promoted too quickly. | Terms become candidates first, with explicit promotion boundaries. |
| Safer delegation | "Run agents" is tempting but underspecified. | Delegation starts as a preview with roles, receipts, join policy, and permission. |
| Better continuity | Receipts, evidence, and next actions are scattered. | The card can feed a side rail of evidence, handoffs, and blocked fields. |

The user gain is speed without looseness. The system gain is more workflow
evidence without silent mutation.

## How It Works

The card follows one simple path:

```text
conversation span
  -> transition candidate
  -> route menu
  -> owner-safe preview
  -> explicit user choice
  -> draft, park, handoff, or approved execution route
```

### Step 1: Notice Or Select A Span

The user may highlight text manually, or the system may suggest a span when the
conversation contains a stable term, tangent, route choice, handoff point, or
delegation signal.

### Step 2: Classify The Moment

The system classifies the span as one or more candidate transition types:

- definition candidate;
- side node;
- handoff draft;
- route ambiguity;
- delegated-run preview;
- maintenance nudge;
- park or ignore.

### Step 3: Show The Route Menu

The card shows the options as a bounded menu, not an open tool drawer. Each
option names:

- owner;
- artifact preview;
- permission state;
- source span;
- blocked or unsafe actions.

### Step 4: Let The User Choose

The user can create a draft, park the item, ignore it, or approve a downstream
route. Preview is not execution. Selection is explicit.

### Step 5: Preserve The Result

The chosen route can produce a candidate packet, side note, handoff draft,
route decision, or permission-gated execution handoff. The result carries
enough evidence for the next owner to continue.

## MVP Shape

The selected MVP is not three separate widgets. The two-lane validation showed
that a definition card, handoff composer, and subagent preview are useful, but
too broad as the first proof.

The sharper MVP is one bounded conversation-transition card with this menu:

| Route | User Sees | Boundary |
| --- | --- | --- |
| Definition candidate | Term, local context, destination, and candidate packet preview. | No canonical definition promotion. |
| Side node | A saved aside with class, source span, and optional follow-up. | Does not switch the active route. |
| Handoff draft | Destination, summary, source refs, gaps, and next prompt. | Handoff is not execution proof. |
| Route ambiguity | Suggested owners such as `invoke`, `dispatch-spec`, or `task-session`. | Selection records intent; it does not execute. |
| Delegated-run preview | Role cards, receipts, join policy, and permission prompt. | No subagent spawn without explicit approval. |
| Park or ignore | Save for later or dismiss. | No write by default. |

## How We Will Test It

We will test the product with static conversation fixtures before building a
real IDE extension.

This first test should answer one product question:

> Can a user understand and choose the right governed route from a live
> conversation moment?

### Fixture Set

The test needs at least five snippets:

1. A new term appears and should become a definition candidate.
2. A tangent appears and should become a side node.
3. A task reaches a natural handoff point.
4. The user is unsure which Arcanum owner should take the next step.
5. A problem has enough role tension to preview delegated lanes.

For each snippet, the proof should output:

- detected or selected span;
- route menu;
- route rationale;
- owner for each option;
- draft or preview artifact;
- blocked actions;
- permission state;
- final user choice.

### Pass Conditions

The MVP passes if a reader can inspect the card and answer:

- what is happening here?
- why is this route suggested?
- what will be drafted?
- what will not happen automatically?
- who owns the next step?

The MVP also passes only if it preserves safety:

- no canonical definition, ontology, spell, sigil, or runtime behavior is
  promoted by the card;
- no subagent is spawned from preview alone;
- no side node silently changes the active task;
- no handoff pretends to be execution evidence.

### Fail Conditions

The MVP fails if it becomes:

- a pretty wrapper around commands;
- a generic agent launcher;
- a dashboard with no next action;
- a route menu whose owner or boundary is unclear;
- a demo that proves only definitions and handoffs, not general transition
  routing.

## What We Build First

First artifact: an Invoke design packet for the transition card.

It should define:

- card states;
- route-menu schema;
- fixture inputs;
- route outputs;
- owner map;
- artifact previews;
- validation criteria;
- pass, flag, and block outcomes.

Second artifact: a small toy proof over static fixtures.

This can be markdown, CLI, or a very small local UI. It should not start as a
full IDE plugin. The first proof is about the product decision, not host
integration.

## Future Product

If the toy proof works, the product grows into an IDE-side action layer for
Arcanum:

- cards over conversation spans and artifact handles;
- a side rail for evidence, receipts, gaps, and handoffs;
- route menus that expose Arcanum owners without overwhelming the user;
- definition and side-node capture that preserve flow;
- handoff composers that make session continuity cheap;
- subagent previews that make delegation legible before permission;
- usage signals that suggest Spellcraft, Sigil Development, or discipline work
  only after repeated evidence exists.

The future is an IDE that helps the user keep momentum while preserving the
ownership rules that make the work durable.

## Product Boundary

IDE Ergonomics does not begin as a full IDE plugin.

It also does not replace Arcanum owners:

- definitions still belong to Definitions Governance;
- route shape still belongs to Dispatch Spec;
- side notes and handoffs still belong to Necronomicon-style workflow memory;
- execution still belongs to Task Session or another approved owner;
- reusable spells still route through Spellcraft.

The first product question is smaller:

> Can a conversation span become a safe route decision before it becomes a
> command, file, agent run, or canonical change?

## Source Trail

- [MVP-TWO-LANE-SYNTHESIS.md](development/mvp-validation/20260619T172822Z-two-lane-mvp/MVP-TWO-LANE-SYNTHESIS.md)
- [findings.md](development/mvp-validation/20260619T172822Z-two-lane-mvp/findings.md)
- [MVP-NEXT-HANDOFF.md](development/mvp-validation/20260619T172822Z-two-lane-mvp/MVP-NEXT-HANDOFF.md)
- [ERGONOMICS-OPPORTUNITIES.md](ERGONOMICS-OPPORTUNITIES.md)
