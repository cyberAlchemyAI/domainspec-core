---
module: cyberalchemy-agentic-system
slice: 05-memory-context
status: candidate
updatedAt: 2026-05-19
docType: slice-concepts
---

# Concepts: Memory And Context

Work: [README.md](README.md)

## What This Slice Compiles

This slice gathers the memory and context model from:

- Necronomicon;
- Knowledge Substrate Flow;
- Context Builder;
- the agentic-system definition;
- the inventory-to-ontology pipeline;
- Operational Ontology requirements.

Memory gives continuity. Context Builder gives task-shaped focus. Promotion governance decides when either becomes durable knowledge.

## Memory Is Continuity

Memory helps the system resume work without replaying the whole conversation.

Necronomicon's repository harness keeps:

- setup decisions;
- session memory;
- route history;
- checkpoints;
- unresolved gaps;
- side notes;
- research briefs;
- maintenance recommendations;
- active interaction state.

Its day-to-day loop is:

```text
open repo
  -> recover context
  -> route request
  -> execute through owner capability
  -> record route, rationale, validation, and follow-up
  -> checkpoint useful facts and gaps
  -> improve harness when repeated misses appear
```

Memory is what lets the system feel situated.

## Memory Is Not Authority

Memory cannot silently become truth.

A memory observation can say:

```text
the user preferred this route here
this task was blocked by this decision
this command failed last time
this side note may matter later
```

It cannot say:

```text
this is now a permanent system rule
```

That jump requires inventory, ontology review, and sometimes decision-gate approval.

## Active Interaction

Necronomicon uses active interaction state to decide whether a user turn continues a current flow or starts a new route.

Important fields:

| Field                     | Meaning                                                                             |
| ------------------------- | ----------------------------------------------------------------------------------- |
| `interaction_id`          | Stable id for the current back-and-forth.                                           |
| `owning_capability`       | Capability responsible for interpreting the next user turn.                         |
| `mode`                    | Active mode: research, invoke define, setup, task-session, etc.                     |
| `status`                  | awaiting-user, running, handoff-ready, blocked, completed, abandoned.               |
| `pending_prompt`          | The question, approval, or evidence request the user is answering.                  |
| `expected_response_shape` | Option choice, free-form answer, approval, correction, artifact path, interruption. |
| `continuation_policy`     | Whether next turn continues by default or routes fresh.                             |
| `handoff_target`          | Next capability after completion.                                                   |
| `side_note_queue`         | Notes, research seeds, contradictions, reminders, unblockers.                       |

Incoming turns are classified as:

1. explicit interrupt or command;
2. side note;
3. pending response;
4. handoff continuation;
5. fresh route;
6. ambiguous turn requiring one focused question.

## Side Notes

Side notes preserve useful material without derailing the active flow.

They can become:

- active artifact input;
- durable project fact;
- research idea;
- related unblocker;
- contradiction;
- governance claim;
- reminder.

The default behavior should be capture first, switch only when the user intends to switch.

## User Workflow Model

The user workflow model captures ergonomics:

- how the user tends to think;
- how much context they want;
- which routes they prefer;
- which explanations help;
- what repeated friction appears;
- what cadence makes work easier.

This is valuable and sensitive.

User workflow memory should have a privacy class before ontology use. A repeated preference can guide local ergonomics, but it should not become a global operating rule without explicit approval.

## Context Builder

Context Builder creates compact task-ready context packs from existing project evidence.

It solves the problem of repositories burying the relevant facts under too much background.

Its method:

- link-first retrieval;
- selector-level evidence;
- obligation coverage;
- excluded noise;
- unresolved gaps.

It should produce:

| Output Part          | Purpose                                            |
| -------------------- | -------------------------------------------------- |
| Target task          | The concrete task being prepared.                  |
| Obligation matrix    | What must the context support?                     |
| Selected excerpts    | Only evidence needed to execute the task.          |
| Selectors or anchors | Where the evidence came from.                      |
| Obligation coverage  | Which obligations are covered.                     |
| Excluded candidates  | What was considered but rejected as noise.         |
| Unresolved gaps      | What still needs clarification or source evidence. |
| Optional index       | Machine-readable retrieval support.                |

## Context Solution Cards

A context solution card is a reusable retrieval pattern.

It says:

- what situation this is;
- what context to load;
- what evidence to cite;
- which route to consider;
- which pitfalls to avoid;
- what not to load;
- when the card expires.

Example:

```text
context-solution-invoke-define-design
  trigger: moving from define baseline into architecture or design
  load: definition, glossary, architecture, gaps, source map
  route: invoke design
  avoid: whole-repo read unless source evidence is missing
  expiry: definition baseline changes materially
```

## Memory To Inventory To Ontology

Memory can feed knowledge, but it must pass through gates.

```text
memory observation
  -> session evidence
  -> inventory candidate when durable
  -> ontology candidate when reusable and governed
  -> decision gate when personal workflow or privacy is involved
```

Examples:

| Memory Pattern          | Destination                                                     |
| ----------------------- | --------------------------------------------------------------- |
| One task decision       | Session evidence.                                               |
| Repeated route miss     | Inventory entry, then operational candidate.                    |
| User preference         | Privacy-scoped memory pattern, maybe decision gate.             |
| Side note contradiction | Inventory contradiction, then ontology review if consequential. |
| Repeated context bundle | Context solution candidate.                                     |

## Core Boundary

Memory helps the present. Ontology guides the future.

The system should use memory to reduce friction, but it should use promotion governance before memory changes rules.
