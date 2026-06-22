# Ergonomics Opportunities

Status: strategy-proposal

This map translates repository evidence into IDE-side workflow improvements for
Arcanum and DomainSpec. Items are candidates, not implementation commitments.

## Priority Map

| Priority | Opportunity | Why it matters | First owner |
| --- | --- | --- | --- |
| P0 | Action-card model for conversation spans | The user needs buttons over live work, but each button must preserve route ownership. | `dispatch-spec` plus Necronomicon |
| P0 | Candidate definition action | Definitions are common and easy to miss; the route must create a candidate without promoting it. | `definitions-governance` |
| P0 | Handoff composer popup | Handoffs already exist, but composing them manually is high-friction. | Necronomicon plus Invoke |
| P0 | Side node capture | Useful asides should not derail active interactions or vanish into chat. | Necronomicon |
| P1 | Subagent fanout preview | Subagents are powerful but require explicit roles, join policy, receipts, and permission. | `dispatch-spec` plus the active owner |
| P1 | Spell or sigil improvement nudge | Repeated route misses should become governed maintenance, not ad hoc edits. | `spellcraft`, `sigil-development`, `sigil-maintenance-loop` |
| P1 | Evidence and receipt rail | Users need to see what was run, what is only proposed, and what remains blocked. | `observability`, `signal-observer` |
| P1 | Intent-latitude annotation | The input-side analog of route ambiguity: the user knows what they mean but has no governed way to signal how literally a span should be taken, so the agent drifts. | `intent-latitude-tags` validator (research-backed; L0 PoC planned) |
| P2 | Knowledge graph side panel | Existing DomainSpec graph ideas can make definitions, handoffs, routes, and evidence visible. | Knowledge Graph IDE feature owner |
| P2 | Host-surface package | A generated IDE package can expose commands, rules, sidebars, and action providers. | `arcanum-bootstrap` or a future host-surface capability |

## Core Interaction Patterns

### 1. Candidate Definition Card

Trigger:

- The conversation introduces a stable term, especially one used in a route,
  handoff, artifact title, concept graph, or repeated decision.

Card contents:

- detected term and local context;
- why it might be a definition candidate;
- likely authority path;
- source span or artifact handle;
- proposed destination;
- "Create candidate", "Park as side node", and "Ignore" actions.

Owner-safe route:

```text
conversation span
  -> action candidate frame
  -> Definitions Governance candidate packet
  -> optional index/drift audit
  -> explicit promotion later, if ever
```

Guardrail:

- The button must not write to canonical definitions without
  `definitions-governance`.

### 2. Handoff Composer Popup

Trigger:

- The active interaction is `handoff-ready`, or the user asks to hand off work,
  or a route reaches a natural lifecycle split.

Popup fields:

- destination type: new session, project folder, work-pack, task-session,
  Spellcraft, Sigil Development, Definitions Governance, or Necronomicon
  checkpoint;
- suggested summary;
- source refs and artifact handles;
- unresolved gaps;
- blocked or deferred work;
- next-session prompt;
- validation checks to run before execution.

Owner-safe route:

```text
active interaction
  -> handoff draft frame
  -> owner-specific handoff artifact
  -> route ledger update
  -> observer signal
```

Guardrail:

- Handoff is not execution proof. It is a durable start point for the next owner.

### 3. Side Node Capture

Trigger:

- The user says "side note", "for later", "this might matter", or introduces a
  useful but non-blocking tangent.

Behavior:

- Capture the span as a side node with class: fact candidate, research seed,
  definition candidate, unblocker, contradiction, reminder, or route gap.

Owner-safe route:

```text
conversation aside
  -> Necronomicon side_note_queue
  -> optional gap ledger or inventory candidate
  -> active flow continues
```

Guardrail:

- Side nodes cannot silently switch the active route.

### 4. Subagent Fanout Preview

Trigger:

- A route has genuine role tension, cross-layer evidence, or parallel research
  lanes.

Preview contents:

- role cards;
- what each role owns;
- context each role can see;
- join policy;
- receipt requirements;
- permission prompt;
- fallback if fanout is declined or unavailable.

Owner-safe route:

```text
route ambiguity or research need
  -> dispatch-spec subagent_strategy
  -> explicit user approval
  -> spawned lanes, if approved and available
  -> lifecycle closeout receipts
  -> parent synthesis
```

Guardrail:

- A route may recommend subagents, but runtime cannot spawn them without
  explicit authorization.

### 5. Spell Or Sigil Improvement Nudge

Trigger:

- The same action card appears repeatedly, a route misses, or the user keeps
  asking for the same multi-step workflow.

Behavior:

- Suggest a maintenance route:
  - Spellcraft if the issue is a repeated composition;
  - Sigil Development if one capability's contract needs revision;
  - Discipline Governance if the practice is broader than one capability;
  - Sigil Maintenance Loop when telemetry supports reflection.

Guardrail:

- The IDE may suggest the route, but it must not author or promote reusable
  capability changes without owner approval.

### 6. Intent-Latitude Annotation

Where the other patterns act on what the agent produced, this one acts on the
user's own message before the agent reads it. Detail and validator contract:
[intent-latitude-tags/](intent-latitude-tags/README.md).

Trigger:

- The user selects (or the surface detects) a span whose intended latitude is
  load-bearing: an exact string to preserve, an outcome to achieve, or a boundary
  not to cross.

Card / annotation contents:

- the selected span and a one-tap latitude choice: `[literal]`, `[goal]`, or
  `[constraint]`;
- what the validator will do with it (verbatim diff-check, exclude+rubric, or
  predicate/judge) and the grounding strength of that check;
- a preview of the draft latitude verdict over the agent's last output.

Owner-safe route:

```text
selected message span
  -> latitude annotation frame
  -> intent-latitude-tags validator (post-hoc, draft verdict)
  -> STRONG for [literal]; FLAG-grade for [goal]/[constraint]; unenforced is never passed
  -> no canonical or runtime behavior promoted
```

Guardrail:

- The tag's force lives in the post-hoc validator, never in the agent "understanding"
  a magic marker — an ungrounded tag collapses to a prose header (the tautology-kill).
- A span the validator cannot check is reported `unenforced`, never silently passed.
- This pattern overlaps the selected MVP's "route ambiguity" branch; the strongest
  alternative to tagging — a clarification loop that asks before acting — is the
  feature's outstanding Lane A debt and should be compared before promotion.

## Suggested MVP

Build the first proof around three actions:

1. Candidate definition card.
2. Handoff composer popup.
3. Subagent fanout preview.

These three cover the most valuable cycle:

```text
notice useful knowledge
  -> route it to the right owner
  -> prepare or approve delegation
  -> preserve receipt and next step
```

## Host Surface Notes

- A VS Code-compatible extension can provide code lenses, chat action buttons,
  side panels, and command palette entries.
- A Codex IDE or editor integration can expose similar actions if it can access
  conversation spans, workspace files, and command APIs.
- A generated rules or modes package, such as the previously researched
  Zoo-Code/Roo-compatible path, can be a lower-cost first host surface.
- Host-specific details must be verified at implementation time; this project
  only defines the Arcanum-side behavior model.

## Anti-Patterns

- Button that directly mutates canonical definitions.
- Popup that hides source refs or unresolved gaps.
- Subagent action that skips permission and receipt closeout.
- Side note capture that changes the active route.
- Dashboard-only signal with no owner or next action.
- Generic "run agent" button with no bounded route menu.
- Reusable spell or sigil creation from one anecdote.
