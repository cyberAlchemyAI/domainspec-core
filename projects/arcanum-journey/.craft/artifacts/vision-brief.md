# Arcanum Journey — Vision Brief (source authority)

> Captured verbatim-in-substance from the operator's `/craft` intent on
> 2026-06-22. This file is **source authority** for the ledger: rows trace back
> here. Do not rewrite the intent; refine it through `decide` / `refine` / child
> contexts instead.

## One-line

A learning course that explains what Arcanum is by **constructing it piece by
piece** — each tool (sigil/spell) added is a new chapter in the tutorial.

## Goal

The user should understand the **potential** of Arcanum: how to leverage it for
any type of work, how each concept **inherits from** another, **builds upon**
another, and how they **integrate** with each other. Present **Craft as the
control surface** — every sigil has its place inside Craft.

## Surface area (for now)

A **standalone downloadable skill** that:

- installs the repo,
- asks what the user wants to learn, **or** offers to install the whole repo and
  let them pick / explore,
- teaches **while** it installs, so users who prefer learning by testing and
  probing can work as they learn.

## Routing idea

1. `/interrogation` to understand the person's **primary goal** with Arcanum.
2. Redirect to a **first tool** by goal:
   - creative tools → **Whisper** (writing; no software knowledge needed) as the
     first creative tool;
   - automation → **Craft** + `spells/goal/` or **task-session**.
3. Identify the **types of routes** available and how the user (or the system)
   selects the starting point.
4. After each learning session, offer **possible next paths** — requires a map
   of all sigils and spells.
5. Explain what **refine** and **invoke** do, and how each sigil has its place
   inside **Craft**.

## How we build the knowledge (named downstream route)

1. `/invoke` define → design → plan the journey definition (this comes first;
   make it durable).
2. `/dispatch-spec` fan-out exploration — bring the **max** amount of
   information: definitions, lifecycles, and the **Cyber Alchemy method /
   framework** (do not forget it).
3. `/inventory` the findings so the knowledge is **durable** and reusable for
   other things.
4. `/research-tower` so the user ends with their **first tower**, in their own
   language, with insights applicable inside their own context.
5. Use `arcanum/spells/reading-learning-package/` as the **base tool** for
   building the learning package from the tower.
6. `/refine` the approach — offer it as a **companion to the installer**.

## Learning preset

A preset focused on **distilling knowledge for people who don't understand much
about a tool or AI**. It should:

- reach for **clever analogies** without losing **simplicity**,
- explain in a **Veritasium** way,
- draw an explainer persona from
  `implementation/domainspec/telemetry/agents/` (agent pool),
- leave **room for user tweaking** so it speaks the user's language.

Precedent to model the tweakable preset on:
`arcanum/spells/goal/decision-profile.schema` and
`arcanum/development/user-guide/`.

## First bounded step (this Craft run)

Create the journey **definition** and make it **durable** as ledger state.
