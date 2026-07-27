---
artifact: ui-prototyping-studio-interface-workbench-ux-plan
status: design-validator-pass
evidence_ceiling: planned-contracts-only
human_study: unbound
---

# UX Plan: Governed Interface Workbench

## Outcome

An operator can always answer:

1. What lifecycle state am I in?
2. Which artifact is current?
3. What evidence or input needs attention now?
4. What action is valid next?
5. What changed after I acted?

The plan removes involuntary whole-page context loss and reorganizes the
preview around the current decision. It does not claim that people understand,
trust, enjoy, or succeed with the rework until a human study says so.

## Primary Actor And Jobs

The Studio operator:

- orients to current state and next valid action;
- inspects the current head;
- selects an exact `data-od-id` target and records intent;
- reviews comment/batch identity;
- compares current and staged documents;
- acknowledges live candidate/revision evidence;
- accepts, discards, or appends a Revert;
- consults history without mistaking it for current state; and
- exports only from the terminal when the separate handoff gate applies.

## Information Architecture

```text
┌ lifecycle + current identity + next valid action ┐
├ current governed canvas ┬ contextual inspector ──┤
│                         │ annotation / batch /    │
│                         │ staged / revision       │
├ state-specific evidence and action ──────────────┤
└ historical lineage (collapsed, secondary) ──────┘
```

Desktop uses a canvas/inspector split when space permits. Mobile keeps the same
semantic order in one column:

1. sticky lifecycle/action summary;
2. active canvas;
3. contextual inspector or review;
4. current action and feedback;
5. collapsed history.

## Surface Contracts

### Lifecycle And Action Spine

Shows:

- lifecycle state in human language;
- current head or staged candidate identity as appropriate;
- concise progress context;
- next valid browser action;
- terminal-only CLI detail in a disclosure; and
- recoverable connection status.

The spine never labels a staged candidate current and never calls an
acknowledged action authorized or release-ready.

### Active Canvas

- Always represents the application-owned current head when available.
- Carries an explicit “current head” label and revision identity.
- Remains the source of annotation.
- Keeps frame source stable while current-head identity is unchanged.
- Has load/error/open-full-preview affordance without replacing the outer shell.

### Contextual Inspector

The inspector is state-specific:

- annotation target and draft in BaselineReady/CommentsCaptured;
- comment or batch summary in MutationDrafted/MutationApproved;
- staged review in RevisionApplied;
- revision receipt and Revert context in RevisionRecorded.

Controls appear when their prerequisite identity exists. Disabled controls have
visible reasons. State changes invalidate only controls bound to stale identity.

### Staged Review

Order:

1. candidate identity and target state;
2. concise diff recap and changed-component list;
3. named Before/current and After/candidate frames;
4. exact acknowledgment;
5. Accept and Discard;
6. `act-msg` scoped feedback; and
7. terminal-only Export explanation after applicable state, never a browser control.

At 390px, Before and After stack. A later optional segmented view must not hide
the diff or remove keyboard/assistive access.

### Historical Lineage

- Collapsed by default after a current head exists.
- Clearly labeled non-current reference evidence.
- Preserves variant/revision labels and relationships.
- Does not precede the active task in DOM order.
- Open/closed state survives unrelated projection updates.

## Interaction Rules

- No unchanged poll moves focus, scroll, selection, draft, or expansion state.
- One unseen projection version is applied once.
- When an action completes during an older poll flight, the action waits for
  one queued trailing refresh before reporting the final observed state.
- A failed region commit rolls back every changed mount and local-context
  mutation before presenting recovery feedback.
- Target selection enables its exact annotation fields and posts status through
  `cf-msg`.
- Accept and Revert remain disabled until exact acknowledgment.
- Discard remains reversible and uses `act-msg`.
- Revert uses `act-msg2` and appends a revision.
- Errors preserve recoverable work and name one safe next step.
- Keyboard activation and pointer activation call the same governed handlers.
- Focus remains on the triggering control after nonterminal feedback; if a
  state transition removes it, focus moves to the new state/task heading.

## Content Rules

- Prefer “Review this staged change, then Accept or Discard” over raw CLI prose.
- Preserve exact CLI commands inside a secondary details disclosure.
- Use “current head,” “staged candidate,” “recorded revision,” and “historical”
  consistently.
- Name identity and target state at durable actions.
- Do not use “approved,” “ready,” “safe,” or “complete” without the exact predicate.
- Connection/poll failures say current work was retained.

## Accessibility Contract

Bounded current scope:

- one main landmark and named task regions;
- ordered headings that follow task hierarchy;
- distinct comparison-frame titles;
- label/name/state for all controls;
- keyboard paths for annotation and action gates;
- visible focus and state-change focus management;
- atomic polite status only for `cf-msg`, `act-msg`, and `act-msg2`;
- assertive status only for separately tested blocking error conditions;
- 4.5:1 for sampled normal-size light-surface text;
- calibrated action target-size floor; and
- no information conveyed by color alone.

UPW-FIX-021 and UPW-FIX-022 bind the keyboard/focus and
color/error-urgency statements to exact planned fixtures. These bounded checks
are not an accessibility certification.

## Responsive Contract

At 390×844:

- no horizontal document overflow;
- one-column semantic order matches the active task;
- the lifecycle/next-action summary stays visible without covering content;
- current canvas remains inspectable;
- staged frames stack and remain named/reachable;
- inputs and actions occupy usable width;
- history follows the active task; and
- nested frame scrolling is not silently reset.

No maximum page-height threshold is imposed.

## State Matrix

| State | Spine emphasis | Primary region | Inspector/review | Browser action |
| --- | --- | --- | --- | --- |
| BaselineReady | comment on current head | current canvas | target + annotation draft | Add comment |
| CommentsCaptured | comments captured | current canvas | comment queue | next synthesis guidance |
| MutationDrafted | batch needs approval | current canvas | batch identity/summary | CLI approval guidance |
| MutationApproved | candidate proposal needed | current canvas | approved batch | CLI apply guidance |
| RevisionApplied | staged, not current | current + comparison | staged review | Accept / Discard |
| RevisionRecorded | recorded current head | current canvas | revision receipt | Revert; terminal Export detail |

Other lifecycle states use the same shell with unavailable regions and exact
next-step guidance.

## Evidence Plan

- Automated hard evidence: UPW-FIX-001–024.
- Screenshot review: hierarchy, salience, canvas/inspector balance, history demotion.
- Human study: orientation, comprehension, interruption recovery, workload,
  perceived control, confidence, trust/safety, delight, and real-task success.
- Not automatable: aesthetic quality and whether this is the right creative
  environment for every operator.

## Gate

UX Plan is Design-authored. It becomes implementable only through the canonical
work-pack after Design Distill, Plan Distill, lifecycle acceptance, and explicit
SWU selection.
