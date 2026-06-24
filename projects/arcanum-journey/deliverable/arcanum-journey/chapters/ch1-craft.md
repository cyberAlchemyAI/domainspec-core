---
chapter: 1
title: Craft — the control surface
teaches: arcana/craft
inherits_from: []
builds: a durable project ledger
integrates_with: every later chapter returns here
preset: applies learning-preset (analogy-first, novice)
---

# Chapter 1 — Craft, the control surface

> Persona: The Explainer. We just learned the tiers. Now we meet the one place the
> whole journey keeps coming back to.

## Hook

Back to the slipping problem: how does a *long* job not fall apart halfway through?
The answer isn't a smarter model. It's a **place to write things down** that the
work itself can read back.

## Analogy

Craft is a **project notebook** — but a magic one. Each page knows:

- what you're trying to do (a **context**),
- what's stuck (a **blocker**),
- what's helping (an **enabler**),
- choices you haven't made yet (an **open decision**),
- holes you've spotted (a **gap**),
- and what to do next (a **next move**).

Unlike a normal notebook, you can *ask* this one questions ("what's blocking me?")
and it answers, because every line has an ID and a link.

## The real thing

Craft is a **file-backed recursive ledger**. The source of truth is a single
`ledger.yml`; a human-friendly `CRAFT.md` is just a readable view of it. You don't
hand-edit the truth file randomly — you use small, named operations:

| You want to… | Craft operation |
| --- | --- |
| start a project | `start` |
| see where things stand | `state` |
| record something stuck | `add_blocker` |
| make a choice | `open_decision` → `decide` |
| note a hole | `add_gap` |
| set the next step | `next` |
| close a sub-task back into its parent | `recompose` |

The deep idea: **raw blockers can't be resolved directly.** You must *refine* a
blocker into a clear closure condition first. That one rule stops hand-wavy
"it's done" — Craft makes you say *how* you'd know it's done.

## Why it's called the control surface

Every other tool in Arcanum — refine, invoke, task-session, goal — **reads from and
writes back to Craft.** It's the dashboard. Learn Craft and you have the place where
every other chapter plugs in.

> Where the analogy breaks: a notebook is private scribbles; a Craft ledger is
> structured so *other tools and other people* can act on it without you re-explaining.

## Probe (try it)

This very journey was planned in a Craft ledger. Open
`projects/arcanum-journey/CRAFT.md` (the readable view) and find: the closed
decisions, the active gaps, and the current next move. You're reading a real control
surface right now.

## One-sentence recap

**Craft is the project's memory and dashboard — a queryable ledger that every other
Arcanum tool plugs into.**

## Where next

- How do you get a vague idea *into* Craft in good shape? Two entry tools:
  **Refine** (Chapter 2) and **Invoke** (Chapter 3).
