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
| P0 | Craft control panel | Craft state should export into an actionable panel where users choose Interrogation, Decision Gate, Refine, export, or defer from pending nodes. | `craft` plus selected owner route |
| P0 | Connective task manager | The flagship should rank next execution lanes by balancing Craft work, cognitive load, attention, user-run tests, and domain priorities. | Craft plus IDE Ergonomics host owner |
| P1 | Subagent fanout preview | Subagents are powerful but require explicit roles, join policy, receipts, and permission. | `dispatch-spec` plus the active owner |
| P1 | Spell or sigil improvement nudge | Repeated route misses should become governed maintenance, not ad hoc edits. | `spellcraft`, `sigil-development`, `sigil-maintenance-loop` |
| P1 | Evidence and receipt rail | Users need to see what was run, what is only proposed, and what remains blocked. | `observability`, `signal-observer` |
| P1 | Knowledge entry reference popup | Recent inventory and ontology searches should reopen as source-aware knowledge references instead of forcing repeated lookup. | `inventory` plus `ontology-vault` |
| P1 | Referenced field hover popover | Reading a schema, doc, or chat span, the user hits governed tokens (`valid_challenge_modes`, `confidence_reference`, `CAV2-D40`) and must leave flow to learn what they mean; hover should peek the authoritative content in place. | `definitions-governance` plus schema/contract source plus `inventory`/`ontology-vault` |
| P1 | Teammate handoff memo window | Agent + human teammate work needs addressed memos, start-work checks, replies, and resolutions instead of unowned task lists. | Handoff owner plus `decision-gate` |
| P1 | Intent-latitude annotation | The input-side analog of route ambiguity: the user knows what they mean but has no governed way to signal how literally a span should be taken, so the agent drifts. | `intent-latitude-tags` validator (research-backed; L0 PoC planned) |
| P2 | Self-assembling ergonomics action | The opportunity map should become a loop the surface can run on itself — suggest, assemble, test — while the human stays the only gate that can promote. | `invoke` plus `spellcraft`/`sigil-development` plus `experiment-harness` plus `decision-gate` |
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

### 7. Knowledge Entry Reference Popup

Where the evidence rail shows what happened in the current run, this pattern makes
the repository knowledge system cheap to reuse while the user is still in flow.
Detail and draft contract: [knowledge-entry-references/](knowledge-entry-references/README.md).

Trigger:

- The user runs or repeats an inventory or ontology search;
- the user hovers or inserts a `knowledge:<surface>/<handle>` reference;
- a handoff, context pack, route menu, or side node needs a precise knowledge
  entry instead of a broad file path.

Popup contents:

- the cached query that produced the result;
- source surface: inventory, ontology-vault, evidence-card, EvidenceSet, query,
  or manifest;
- title, handle, summary, matching snippet, tags, status, confidence, and updated
  date when available;
- source refs, authority boundary, promotion owner, and residue;
- actions to open entry, open source refs, copy handle, add to handoff, add to
  context pack, park as side node, or refresh the search.

Owner-safe route:

```text
inventory or ontology query
  -> recent search cache
  -> selected knowledge entry handle
  -> reference popup
  -> optional handoff, context pack, side node, or route-menu insert
  -> no authority promotion
```

Guardrail:

- Cached search results are convenience, not proof. If the underlying inventory or
  ontology entry changed, the popup must mark the result stale and offer refresh.
- Inventory and ontology entries must remain visually distinguishable; the popup
  cannot collapse read models, candidate condensations, and canonical authority
  into one generic "knowledge" badge.

### 8. Teammate Handoff Memo Window

This pattern makes agent + human partnership visible in the IDE. It is based on
the local addressed memo style in
[cyberAlchemy-v2/TO-VLAD/](../../cyberAlchemy-v2/TO-VLAD/) and is detailed in
[teammate-handoff-memos/](teammate-handoff-memos/README.md).

Trigger:

- a new work session starts inside a project with addressed memos;
- the current route reaches a human or teammate handoff boundary;
- the user needs to leave a memo for a person, role, future session, or agent
  lane;
- an existing memo needs a reply, consumed marker, or resolution artifact.

Window contents:

- recipient, source, subject, project scope, and status;
- why this memo matters now;
- next-session prompt or suggested route;
- key points, open calls, concrete next actions, source refs, and boundaries;
- resolution link, superseded state, and still-open items when available.

Owner-safe route:

```text
active work or start-work check
  -> addressed memo scan
  -> teammate handoff window
  -> user chooses read, draft, reply, resolve, or defer
  -> memo artifact or resolution draft
  -> owner decision remains explicit
```

Guardrail:

- The window may draft or surface teammate memos, but it cannot impersonate a human
  recipient, send external messages, or mark human-owned decisions as answered
  without an explicit response or governed decision record.
- A polished memo is not proof of resolution. Resolution requires a separate
  consumed/decision/validation record.

### 9. Craft Control Panel

This pattern turns Craft from file-backed project memory into an IDE workbench.
It exports current Craft state, shows pending work by node, and asks one focused
interactive route question before sending the selected item to Interrogation,
Decision Gate, Refine, export, or defer. Detail and draft contract:
[craft-control-panel/](craft-control-panel/README.md).

Trigger:

- a project has a `.craft/ledger.yml`, `CRAFT.md`, or derived Craft index;
- the user asks for status, pending work, decisions, blockers, gaps, or next
  moves;
- the selected Craft item needs an owner route but the user has not chosen which
  one;
- a work session starts and multiple Craft scopes or pending nodes are available.

Panel contents:

- owning Craft scope, ledger path, human view, source freshness, stage, and gate;
- pending by node: blockers, blocking decisions, open decisions, gaps, pending
  artifacts/routes, recomposition residue, and next move;
- selected row or next move with source selector and summary;
- route options: ask Interrogation question, open Decision Gate, start Refine,
  refresh/export state, or defer;
- one interactive question at a time, with recommended option, consequences, and
  "Explain / more context" for consequential choices.

Owner-safe route:

```text
Craft ledger or all-status export
  -> control-panel state model
  -> user selects a node, row, or next move
  -> interactive route question
  -> selected owner route: interrogation | decision-gate | refine | export | defer
  -> owner capability produces artifact, receipt, or blocked reason
  -> Craft receives the result only through a governed update
```

Guardrail:

- `.craft/ledger.yml` remains the source of truth. The panel is a read model until
  a selected owner route returns a receipt and a governed Craft update records the
  result.
- The panel must not close raw blockers directly, hide stale state, choose a
  consequential route on behalf of the user, or treat Refine strategy proposals as
  execution evidence.

### 10. Connective Task Manager

This is the flagship composition: a task manager that receives Craft work state,
applies cognitive-load and attention lenses, incorporates user-executed test
evidence, and balances all of that against domain priorities. Detail and draft
contract: [connective-task-manager/](connective-task-manager/README.md).

Trigger:

- a session starts and the user needs to choose what to work on next;
- Craft exposes several pending nodes, next moves, blockers, gaps, or decisions;
- domain priorities conflict with what feels easy or attention-friendly;
- a user-run validation check should happen before execution;
- the IDE needs to recommend a route without pretending to own the user's
  attention or the project's authority.

Panel contents:

- imported Craft candidates with row IDs, source selectors, readiness, and next
  moves;
- opt-in human indicator snapshot: available time, focus, fatigue, confidence,
  frustration, interruption risk, and desired collaboration mode;
- user-executed test evidence: command, UI check, fixture, review prompt, or manual
  confirmation;
- domain priority lens: risk, blocked downstream work, owner requirement, deadline,
  product path, and validation need;
- ranked execution lanes with explanation, fit, warnings, required confirmation,
  expected owner route, and expected receipt.

Owner-safe route:

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

Guardrail:

- Connective recommends and explains; it does not diagnose, surveil, override the
  user, or execute domain work without confirmation.
- Human indicators are opt-in, local, reviewable, and may remain unknown.
- Domain-critical work should not be hidden merely because it is high load; the
  panel should expose a lower-load first move when needed.

### 11. Referenced Field Hover Popover

Where the knowledge entry popup (#7) reopens a *search result* the user already
ran, this pattern resolves a *token already present in the text* the moment the
user hovers it. It is the LSP "peek definition" / hover-doc behavior applied to
governed Arcanum and DomainSpec vocabulary: schema field names, contract keys,
and definition IDs become live references that point at their authoritative
content in place, so the reader never breaks flow to ask "what is this?".

Trigger:

- the user hovers (or the surface detects) a governed token in a schema, doc,
  contract, route trace, or conversation span:
  - a schema/contract field such as `valid_challenge_modes`,
    `confidence_reference`, `resolution_gate`, `instantiates`, or `residue`;
  - a definition ID such as `CAV2-D40`, or a named invariant/axiom handle;
  - a canonical term that has a definitions, inventory, or ontology home.

Popover contents:

- the token and the kind of thing it is (contract field, node property,
  definition ID, invariant/axiom, canonical term);
- the resolved authoritative content: the field's contract row and meaning, or
  the definition body (e.g. `CAV2-D40` -> "challenge_contract binds
  confidence/residue" with its current statement);
- the source surface and authority boundary: canonical definition vs candidate
  vs raw schema field vs deferred/superseded;
- confidence, status, and last-updated when the source carries them;
- actions: open source, copy handle, add to handoff or context pack, park as
  side node, or open the related definition/drift audit — never an edit action.

Owner-safe route:

```text
hovered governed token
  -> reference resolver (definitions | schema/contract | inventory | ontology-vault)
  -> matched authoritative entry, or "unresolved / ambiguous" marker
  -> hover popover (read-only)
  -> optional open, copy, handoff, context-pack, or side-node insert
  -> no authority promotion or content mutation
```

Guardrail:

- Resolution is read-only. The popover points at content; it never edits the
  definition, schema, or contract it resolves.
- A token with no authoritative home is reported `unresolved`, and a token that
  matches more than one home is reported `ambiguous` with the candidates listed —
  the popover must not fabricate a definition or silently pick one source.
- The popover must keep the authority boundary visible: a canonical definition, a
  candidate condensation, and a bare schema field are distinct and cannot collapse
  into one generic "reference" badge.
- This pattern overlaps DomainSpec's knowledge-graph "definition pointers" /
  "concept detail focus" (see `knowledge-graph-visualization/SPEC.md`); the hover
  popover is the inline, no-navigation analog and should reuse that pointer model
  rather than inventing a second resolution path.

### 12. Self-Assembling Ergonomics Action

This is the meta-pattern: a command and visible button that runs the opportunity
map on itself. It **suggests** its own next ergonomics improvement, **assembles** it
as candidate artifacts, **tests** it against a pre-registered criterion, then
**notifies** the user with a bounded test to run and approve. Detail and draft
contract: [self-assembling-ergonomics/](self-assembling-ergonomics/README.md).

The load-bearing rule: *assembled and green is not shipped.* The loop may suggest,
author, build, and test autonomously, but it may not promote, install, or mutate any
canonical capability or runtime until the user runs the delivered test and approves.

Trigger:

- the surface detects a high-value opportunity (a map entry plus observed friction
  telemetry) and offers to build it;
- the user explicitly taps "Build this" on a scoped candidate.

Loop:

```text
suggest (map + friction telemetry)
  -> user one-tap "Build this" (scoped consent)
  -> assemble: invoke define/design/plan in an isolated candidate space
  -> owner-lifecycle drafts (spellcraft | sigil-development) — drafts only
  -> test: pre-register acceptance criterion, then run (experiment-harness)
  -> notify: push notification with verdict + a bounded test the user runs
  -> user tests and approves -> governed promotion through the real owner
                       or rejects -> residue ledger, iterate or drop
  -> nothing canonical or runtime mutates before approval
```

Guardrail:

- The "suggest" step must cite a real map entry or real friction evidence; it cannot
  invent an opportunity.
- Assembly stays in an isolated candidate space and never edits `arcanum/` canonical
  capabilities or runtime.
- The acceptance criterion is frozen before the run, so "it passed" can never be
  retrofitted to the result.
- The notification says "ready for your test + approval," never "done" or "shipped."
- Rejection and FALSIFIED are valid outcomes that leave residue and iterate — never a
  silent retry-until-green.
- Promotion routes through the owner that owns the target lifecycle, with a receipt;
  this loop is author and tester, not owner.

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

Treat Connective as the flagship proof after the control-panel substrate is clear:

1. Import one Craft scope with several pending nodes.
2. Collect an opt-in human indicator snapshot.
3. Attach one user-executed test result.
4. Rank the next execution lanes and explain the recommendation.

That proof should show the product's full promise without building a full task
manager runtime yet.

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
- Cached knowledge result that hides stale, missing, or candidate-only status.
- Knowledge popup that treats inventory or ontology read models as canonical
  definitions.
- Handoff memo window that turns an addressed memo into an unowned task list.
- Reply action that writes as if it came from a human teammate.
- Craft panel that reports only aggregate counts instead of pending by node.
- Craft panel that edits `.craft/ledger.yml` authority directly or closes blockers
  without a governed owner-route receipt.
- Connective recommendation that invents human indicators or treats them as
  surveillance data.
- Connective ranking that always chooses low-load comfort work over domain-critical
  work, or forces high-load work without showing the attention risk.
- Generic "run agent" button with no bounded route menu.
- Reusable spell or sigil creation from one anecdote.
- Self-assembling action that promotes its own build without the user test and
  approval gate.
- "Suggest" step that fabricates an opportunity with no map entry or friction
  evidence behind it.
- Self-test that writes its own success criterion after seeing the result, or that
  silently retries until green.
- Self-assembly that edits `arcanum/` canonical capabilities or runtime instead of an
  isolated candidate space.
- Notification that reports "done" or "shipped" instead of "ready for your test and
  approval."
