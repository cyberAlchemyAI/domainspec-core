---
tags: [ide, ergonomics, flagship, task-manager, craft, attention, cognitive-load]
node_type: feature
layer: product, workflow, governance, human-factors
nature: design-seed
status: flagship-proposal
created: 2026-06-23
---

# Connective Task Manager

Connective is the flagship IDE Ergonomics primitive: a task manager that consumes
Craft work state, reads it through cognitive-load and attention lenses, and uses
user-executed tests plus domain priorities to guide task execution.

It is also the clearest proof of the CyberAlchemy v2 proposition: the value is
not only an agent system, a knowledge system, a software system, or an IDE
interface. The value is synergetic cybernetic human-machine integration, where
the next move is selected from the interaction between human state, machine
capability, evidence, task readiness, and domain priority.

The earlier primitives make individual moments easier: a route card, a handoff
popup, a knowledge reference, a Craft control panel. Connective composes them into
the question the user actually has while working:

> What should I work on next, given what matters, what is blocked, what I can
> attend to right now, and what evidence says is safe to execute?

## Why it belongs here

Craft already knows the work graph: contexts, blockers, gaps, decisions,
artifacts, next moves, and recomposition. The control panel can expose that graph.
But a plain task list still misses the lived part of work: attention is finite,
cognitive load changes during the day, some tasks are domain-critical but wrong
for the current human state, and some tasks need a user-run test before the system
can recommend execution honestly.

Connective balances three inputs:

- **Craft work state** - pending nodes, open decisions, gaps, blockers, next moves,
  receipts, and stale/missing evidence;
- **human indicators** - opt-in signals such as focus, fatigue, confidence,
  frustration, available time, interruption risk, and preferred collaboration mode;
- **domain priorities** - project priority, deadline, risk, blocked downstream work,
  owner requirements, and validation need.

Its output is not "the agent runs the next task." Its output is a recommended
execution lane with an explanation, a confidence level, and a reversible route
choice.

## User Experience

Connective opens as an IDE task manager:

```text
Connective
Scope: projects/body-war
Attention budget: medium, 45 minutes
Human indicators: focus medium, fatigue low, confidence high
Domain priority: auth/profile onboarding blocks MVP path

Recommended next:
1. Run focused auth validation sweep
   Why: high domain priority, low ambiguity, fits current attention budget
2. Defer track/game design
   Why: high ambiguity, not current MVP path
3. Ask one decision-gate question on hosted-preview posture
   Why: blocker-level choice, small cognitive footprint
```

When a task is selected, Connective asks for confirmation through a compact,
editor-style question:

```text
This task is execution-ready but attention-sensitive.

Recommended: run the focused validation sweep now.

Why:
- Craft next move is unblocked.
- Domain priority is high.
- User indicators say 45 minutes of focused work is available.
- The required test is bounded and reversible.

Options:
- Run validation sweep
- Ask one Interrogation question first
- Defer to later
- Explain / more context
```

## Owner-Safe Route

```text
Craft state export
  -> task candidates
  -> human indicator snapshot
  -> user-executed test evidence
  -> domain priority lens
  -> ranked execution lanes
  -> interactive choice
  -> selected owner route with receipt
  -> Craft update only through governed write path
```

Connective recommends and explains. It does not replace Craft, assign human state
without consent, or execute domain work without the selected owner route.

## What It Balances

| Lens | Example signals | Why it matters |
| --- | --- | --- |
| Craft readiness | gate, blockers, decisions, gaps, next move, receipts | Keeps recommendations tied to source-of-truth work state. |
| Cognitive load | complexity, ambiguity, context needed, switching cost | Prevents "right task, wrong moment" recommendations. |
| Attention | available time, focus, interruption risk, desired collaboration style | Matches task shape to the current human session. |
| User-executed tests | validation commands, UI checks, review prompts, small proof tasks | Grounds execution readiness in evidence the user can inspect. |
| Domain priority | risk, blocked downstream work, deadline, owner priority, product path | Keeps comfortable tasks from crowding out important work. |

## Surfaces

Connective may appear as:

- a flagship IDE side panel;
- a task manager view over Craft scopes;
- a start-work triage step before execution;
- a companion to the Craft control panel, using its selected row as one candidate;
- a daily or session-level planning prompt;
- a receipt rail showing why a recommendation changed.

## Files

- [SPEC.md](SPEC.md) - task candidate model, human indicator snapshot, attention
  lens, user-executed test evidence, priority scoring, route decisions, and pass
  conditions.

## Boundaries

- Strategy proposal only; no task-manager runtime is built here.
- Human indicators are opt-in, local, and reviewable. They are not medical,
  psychological, or productivity-surveillance claims.
- Connective may recommend lower-load or higher-priority work, but the user keeps
  final control.
- `.craft/ledger.yml` remains the work-state source of truth.
- Domain execution still belongs to the selected owner route, such as Task
  Session, Decision Gate, Interrogation, Refine, or a project-specific workflow.
