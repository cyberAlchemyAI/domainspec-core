# Spell Candidate: IDE Assisted Arcanum Routing

Status: candidate
Scope: project-local proposal
Canonical ID: `ide-assisted-arcanum-routing`
Lifecycle owner if pursued: `spellcraft`

## Purpose

Compose Necronomicon, Dispatch Spec, Definitions Governance, Spellcraft, Sigil
Development, Task Session, and Observability into an IDE-facing workflow that
turns conversation spans into bounded actions with clear owners, gates,
handoffs, and receipts.

The spell would not implement an IDE plugin by itself. It would define the
Arcanum-side workflow contract that a host extension, command palette, or rules
package can project.

## Trigger Conditions

- A conversation span looks like a candidate definition.
- A side note appears during an active interaction.
- The active interaction becomes handoff-ready.
- The user asks to dispatch a subagent or the route has role-bound fanout
  pressure.
- A repeated workflow suggests a composed spell or sigil maintenance path.
- The IDE needs to show a bounded route menu instead of an unbounded tool list.

## Required Sigils And Spells

| Capability | Role |
| --- | --- |
| `necronomicon` | Own active interaction state, side notes, candidate classification, route memory, checkpoints, and handoffs. |
| `dispatch-spec` | Validate action route shape, route menus, subagent strategy, gates, and observability grouping. |
| `definitions-governance` | Own candidate definition packets and any later canonical definition updates. |
| `spellcraft` | Own reusable workflow composition if the action sequence becomes a spell. |
| `sigil-development` | Own changes to one sigil's behavior contract. |
| `task-session` | Own bounded execution after a route becomes an approved task or SWU. |
| `decision-gate` | Resolve consequential alternatives before mutation. |
| `signal-observer` | Record usage, route misses, output drift, and follow-up signals. |

Optional:

- `inventory` for source-backed knowledge candidates;
- `ontology-harness` for ontology or premise candidates;
- `discipline-governance` for recurring cross-capability practices;
- `x-ray` for visual explanation of a route, artifact, or active graph;
- `context-builder` for compact evidence packs.

## Shared State

| State | Meaning | Authority |
| --- | --- | --- |
| `conversation_span` | Text range or chat turn that triggered an action. | Host/IDE runtime |
| `action_candidate` | Classified action card with owner, confidence, and route. | Spell frame, non-authoritative |
| `route_menu` | Bounded 3-7 option menu. | `dispatch-spec` |
| `handoff_draft` | Suggested destination, summary, refs, gaps, and next prompt. | Owning handoff capability |
| `side_node` | Non-interrupting note, fact candidate, research seed, contradiction, or reminder. | Necronomicon |
| `subagent_preview` | Role cards, join policy, permission, and receipt requirements. | `dispatch-spec` plus active owner |
| `receipt` | Execution, handoff, validation, or blocked proof. | Producing capability |

## Execution Phases

| Phase | Owner | Input | Output | Gate | Failure Policy |
| --- | --- | --- | --- | --- | --- |
| 1. Detect action span | Host adapter plus Necronomicon | conversation span | action candidate frame | source span is available | show no action or ask user to select span |
| 2. Classify authority | Necronomicon | action candidate | candidate class and owner | owner can be named | route to fallback-discover or ask one question |
| 3. Validate route menu | Dispatch Spec | candidate class and owner | bounded route menu | dispatch shape validates | block unsafe action |
| 4. Present action card | Host adapter | route menu | button or popup | user selection is explicit | keep as parked candidate |
| 5. Compose handoff or preview | Owning capability | selected action | handoff draft or subagent preview | required refs and gaps are named | flag missing evidence |
| 6. Execute only if approved | Task Session or owner | approved route | receipt or blocked reason | permission and owner gate pass | write handoff instead of executing |
| 7. Capture outcome | Signal Observer plus Necronomicon | receipt | route ledger, checkpoint, side node update | telemetry path available or gap reported | preserve primary result and report observability gap |

## Action Card Contract

```yaml
action_id: <stable-id>
span_ref: <conversation-span-or-artifact-handle>
detected_kind: definition_candidate | side_node | handoff | route_menu | subagent_preview | maintenance_nudge
label: <short button label>
summary: <why this action is suggested>
owner: <capability-id>
authority: candidate | handoff | execution | promotion
confidence: high | medium | low | block
route_ref: <dispatch-id-or-none>
destination_suggestion: <path-or-capability-or-none>
preview_fields:
  - <field name>
buttons:
  - label: <verb>
    effect: <candidate | handoff | execute_after_approval | dismiss>
disabled_reason: <reason-or-none>
```

## Handoff Composer Contract

Required fields:

- destination capability or folder;
- source refs and artifact handles;
- concise summary;
- owner-safe next prompt;
- open gaps and blocked fields;
- validation checks;
- privacy or public/private boundary notes;
- whether execution is authorized.

## Gates

- Candidate definitions route through `definitions-governance`.
- Ontology or premise candidates route through `ontology-harness` or
  `ontology-vault`.
- Subagents require explicit user approval and closeout receipts.
- Reusable spell creation requires Spellcraft.
- Sigil behavior changes require Sigil Development.
- Canonical Arcanum mutations require their owning lifecycle and validation.
- Host-specific plugin work requires a separate implementation plan and browser
  or IDE evidence.

## Failure Policy

- If the owner cannot be determined, show a route menu or ask one focused
  question.
- If a route validates but execution is not approved, write a handoff draft.
- If a subagent cannot spawn, record a blocked subagent lifecycle entry and let
  the parent decide whether a non-subagent fallback is allowed.
- If observability is unavailable, preserve the primary result and report the
  telemetry gap.

## Observability

Meaningful executions should record:

- action kind;
- selected route;
- owner capability;
- whether a handoff or execution occurred;
- subagent strategy and authorization state;
- files changed;
- receipts produced;
- blocked fields;
- user dismissals or corrections;
- follow-up owner.

## Next Step

Use Spellcraft `design` only after the user approves turning this project
proposal into a local spell artifact under `.arcanum/spells/` or a reusable
library spell under `arcanum/spells/`.
