---
node_type: product-view
status: vision (honest about proven-vs-bet)
topic: what the Tower System is for, told as a story
last_updated: 2026-06-19
companions: SYSTEM-VIEW.md, findings.md, PRECEDENT-RECHECK.md
---

# Tower System — Product View

> A story-first explainer. The architecture is in [SYSTEM-VIEW.md](SYSTEM-VIEW.md). Where
> something is a **bet** rather than a built thing, it says so — this project's own research
> ([findings.md](findings.md)) found the core is not yet witnessed, and honesty about that is
> part of the product.

## 1. The frustration (why this exists)

You spend a week really learning Domain-Driven Design. You read the book, you argue with an
LLM about aggregates, you finally *get* the boundary between an aggregate and a bounded
context. Then Monday comes, you open a new chat to design a checkout flow, and all of it is
gone. The model has no memory of what you learned. It agrees with whatever you propose. When
you ask "is this aggregate boundary right?" it gives you a confident, flat, plausible answer —
and you have no idea whether a real expert would have torn it apart.

Two things are broken:

1. **Knowledge doesn't compound.** Every session starts from zero. What you understood
   yesterday isn't a thing you can pick up and reuse today.
2. **The AI never really disagrees.** A single model talking to itself can't hold a genuine
   opposing view — it drifts toward agreement. You lose the most valuable thing an expert
   gives you: a *good argument against your idea*.

The Tower System is a bet that both of these are fixable, and that fixing them turns
"learning" and "applying knowledge" into the same loop instead of two disconnected chores.

## 2. The idea (in one image)

A **tower** is a place where your understanding of a domain *accretes* and becomes
**inhabitable**. You build it once — by distilling sources, or by reading a book *through* it
so it grows as you go. Inside, the domain isn't a wall of notes; it's a **graph you can walk**,
and the important ideas in it become **personas** — small, opinionated experts you can summon.

> The DDD tower doesn't just *store* "Aggregate" and "Event-Driven Architecture." It lets you
> call up *the Aggregate-Boundaries purist* and *the Event-Driven pragmatist* as two characters
> who will genuinely argue with each other about your design.

That's the whole product in one sentence: **learn a domain into a tower, then summon its
personas to debate, design, and decide — and have the system score who was right and remember.**

## 3. A day with it (the scene we're building toward)

*This is the target experience — the witness unit ([witness-unit/](witness-unit/)) is the first
sliver of it we intend to actually prove.*

You're designing checkout. You type `/invoke design` and point it at your DDD tower.

- The system pulls two personas off the graph — **Aggregate-Boundaries** (anchored to the
  `Aggregate` node) and **Event-Driven** (anchored to `Bounded Context`). They are deliberately
  *tensioned*: built to disagree, not to nod along.
- They debate one sharp question: *"Should the Order aggregate span the Shipping context?"*
  Aggregate-Boundaries says no — consistency boundary violated. Event-Driven says yes — ship an
  event, stay decoupled.
- Mid-argument, Event-Driven realizes it's shaky on idempotency. It **spins up a sub-tower** on
  exactly that, learns just enough, and comes back. (Towers inside towers — the recursion you
  liked.)
- The disagreement gets **scored** — not "the model picked one," but a traceable resolution:
  judges weigh in, the system records *why* one position won and how confident it is, and the
  two personas' ratings move. Next time, the persona that keeps being right gets more weight.
- You get a **verdict you can audit**: the proposition, the winning position, the confidence,
  and the trail. Not a vibe — a receipt.

You didn't just get an answer. You watched two experts fight, saw the reasoning, and the tower
got a little smarter about checkout for next time.

## 4. Who it's for, and the job it does

| If you are… | The job it does for you |
|---|---|
| Someone learning a hard domain | Turns reading into a durable, reusable structure instead of notes you forget. |
| Someone designing/deciding with AI | Gives you *real disagreement* and a *traceable judgment*, not a flattering single answer. |
| A team building agentic tools | A composable substrate: the same tower personas feed debate, design, dispatch, or writing. |

The unifying move is small and reusable: **any action you take instantiates one tensioned
group of personas to explore and stress the case.** Debate, design review, a research
dispatch, even drafting prose — same primitive, different operation.

## 5. Why it can work — it's mostly *your own* prior work, reassembled

The honest good news from the research: this isn't a moonshot built from nothing. Most of the
parts already exist as **your own executed projects** (see [PRECEDENT-RECHECK.md](PRECEDENT-RECHECK.md)):

- building a tower from sources → **already done** (`autobayes`, `monoidal-categories` research towers).
- running a real multi-agent disagreement with preserved tension → **already done**
  (`dispatch-composition-attack`, `observability-adaptation`).
- scoring decisions across competing objectives and picking the next move → **MOGT**
  (`mogt-agentic-conversation`), your own decision-policy project.

The system is largely an **assembly** of owned pieces over a well-known integration pattern.
That's why it's credible.

## 6. The honest part (what's a bet, not a feature)

The research deliberately tried to break this idea, and found the **center is still a bet**.
Three things have to be invented and proven before the magic in §3 is real:

1. **What a persona actually *is*** — enough of a defined thing to *hold a position*, not just
   a label pointing at a graph node.
2. **How a graph node becomes a real disagreement** — neighboring concepts *compose*; they
   don't automatically *conflict*. Manufacturing genuine tension from the graph is the hard
   open problem.
3. **Scoring that actually grades** — a resolution that does more than count votes.

And one sequencing call we just made: **MOGT — the owned decision-policy piece — is real but
unproven (zero live experiment runs).** So before we build the tower on top of it, we run
MOGT's own experiments to get evidence. De-risk the foundation, then build.

So the pitch is not "this works." It's: *"this is a credible assembly of mostly-owned parts,
the three hard unknowns are named and isolated, and the first thing we build is the smallest
unit that proves or kills them."* That smallest unit is the [witness unit](witness-unit/).

## 7. The one-line promise

**Learn a domain once into a tower; summon its personas to argue, design, and decide; get a
traceable, scored verdict; and watch the knowledge compound.** Everything in
[SYSTEM-VIEW.md](SYSTEM-VIEW.md) exists to make that one loop real and honest.
