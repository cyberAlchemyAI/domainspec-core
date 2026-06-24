# SPEC - Craft Control Panel

Status: draft strategy artifact; no runtime implementation
Date: 2026-06-23
Owner if pursued: IDE Ergonomics host-surface owner plus Craft/route owners
Builds on: [README.md](README.md)

## 1. Problem

Craft makes project state durable, but the user still has to translate ledger rows
into the next interaction manually. A ledger may already say there are open
decisions, active gaps, refined blockers, pending artifacts, and a next move, but
the IDE does not yet show those as actionable choices.

This creates friction:

- pending work is hidden in files or summarized only as counts;
- the user cannot quickly tell whether the next move needs Interrogation,
  Decision Gate, Refine, execution, or deferral;
- decision questions are not presented with the interactive UX users expect from
  AI chat editors;
- agents can start work from a stale or broad summary instead of the owning Craft
  scope.

## 2. Primitive

`craft-control-panel` is a read-first IDE primitive with three linked parts:

1. `craft_state_export` - a panel-safe projection of the current Craft ledger,
   index, and human view.
2. `craft_route_option_set` - route choices for one selected node, row, or next
   move.
3. `interactive_route_question` - a one-question UX for choosing the next owner
   route.

The primitive is a control surface over Craft state. It is not itself Craft, and it
is not the owner of Interrogation, Decision Gate, or Refine artifacts.

## 3. Source Surfaces

Initial source surfaces:

| Surface | Role |
| --- | --- |
| `.craft/ledger.yml` | Source of truth for Craft state. |
| `.craft/index.json` | Optional generated machine index for lookup. |
| `CRAFT.md` | Generated human view with linked summary and quick links. |
| `.craft/artifacts/` | Supporting decisions, receipts, handoffs, and evidence. |
| repository-wide ledger discovery | Finds multiple scoped Craft spaces before reporting all status. |

The panel must support scoped ledgers. A repository can contain many `.craft`
spaces; the panel must show which scope owns the selected work.

## 4. State Export Model

```yaml
craft_state_export:
  export_id: <stable-host-id>
  workspace_root: <repo-path>
  scope_path: <repo-relative-path>
  ledger_path: <repo-relative-path-to-.craft/ledger.yml>
  human_view_path: <repo-relative-path-or-null>
  exported_at: <timestamp>
  source_hashes:
    ledger: <hash-or-mtime>
    index: <hash-or-mtime-or-null>
    human_view: <hash-or-mtime-or-null>
  readiness:
    stage: <define|design|build|validate|unknown>
    gate: pass | flag | block | unknown
  pending_by_node:
    - context_id: <id>
      title: <title>
      gate: pass | flag | block | unknown
      active_blockers: []
      blocking_decisions: []
      open_decisions: []
      active_gaps: []
      pending_artifacts: []
      recomposition_residue: []
      next_move: <text-or-null>
  selected_item:
    kind: context | blocker | decision | gap | definition | artifact | recomposition | next_move
    id: <stable-id-or-null>
    summary: <short summary>
    source_selector: <path-or-row-id>
```

Export rules:

- Export is read-only.
- Export must show pending work by node, not only aggregate counts.
- Export must mark stale state when source hashes differ from the last refresh.
- Export may summarize but must keep links to ledger row IDs and source paths.

## 5. Route Option Set

```yaml
craft_route_option_set:
  selected_item_id: <row-id-or-context-id>
  recommended_option: <option-id>
  options:
    - option_id: ask_interrogation
      label: Ask one question
      owner: interrogation
      when_to_choose: <short condition>
      effect: draft_interview_question
      requires_confirmation: true
    - option_id: open_decision_gate
      label: Resolve decision
      owner: decision-gate
      when_to_choose: <short condition>
      effect: decision_record
      requires_confirmation: true
    - option_id: start_refine
      label: Refine target
      owner: refine
      when_to_choose: <short condition>
      effect: strategy_proposal
      requires_confirmation: true
    - option_id: export_state
      label: Refresh/export state
      owner: craft
      effect: read_model_refresh
      requires_confirmation: false
    - option_id: defer
      label: Keep visible
      owner: craft
      effect: no_mutation
      requires_confirmation: false
    - option_id: explain_more
      label: Explain / more context
      owner: control-panel
      effect: expand_tradeoffs
      requires_confirmation: false
```

Routing heuristics:

- Use `interrogation` when the selected item needs one owner-bound or
  evidence-backed question before route choice.
- Use `decision-gate` when more than one consequential option exists and work
  should stop until the decision is explicit.
- Use `refine` when the target is vague, design-shaped, or needs a non-executed
  strategy proposal before implementation.
- Use `craft` export when state may be stale or the user only wants status.
- Use `defer` when the item should stay visible without mutation.

## 6. Interactive Question Contract

```yaml
interactive_route_question:
  question_id: <stable-host-id>
  selected_item: <row-id-or-context-id>
  prompt: <single focused question>
  context: <why the question matters>
  recommended_option: <option-id-or-null>
  options:
    - <route option>
  explain_more_available: true
  unresolved_risk_if_unanswered: <short risk>
  selected_option: <option-id-or-null>
  result:
    status: unanswered | selected | deferred | blocked
    next_owner: <capability-or-none>
    artifact_or_receipt: <path-or-null>
```

Question rules:

- Ask one question at a time.
- Include a recommended option only when the source evidence supports it.
- Always include `Explain / more context` for consequential choices.
- Selecting `Explain / more context` does not choose a route; it expands
  trade-offs and re-presents the same real options.
- Selecting `Refine` opens a strategy proposal first, not an immediate run.
- Selecting `Decision Gate` persists a decision record only after the user chooses
  a real option.

## 7. Interaction States

| State | Meaning | UI behavior |
| --- | --- | --- |
| `discovering` | Finding Craft scopes. | Show ledgers found and ask scope only if ambiguous. |
| `exported` | State model is current. | Show pending by node and quick actions. |
| `stale` | Source ledger/index changed since export. | Badge state and offer refresh. |
| `item-selected` | One row or next move is focused. | Show route option set. |
| `question-open` | One interactive route question is active. | Show route options and explain-more action. |
| `route-selected` | User picked an owner route. | Show required confirmation and expected artifact/receipt. |
| `handoff-written` | Selected route needs a future run. | Link handoff or strategy proposal. |
| `receipt-returned` | Owner capability produced proof. | Offer governed Craft update or closeout. |

## 8. Owner-Safe Actions

| Action | Allowed effect | Boundary |
| --- | --- | --- |
| `export_state` | Refresh a read model from Craft sources. | Does not mutate ledger. |
| `ask_interrogation` | Ask one evidence-backed question. | No invented answers; update only after user answer. |
| `open_decision_gate` | Present options with trade-offs. | No consequential mutation while gate is unresolved. |
| `start_refine` | Create or preview a Refine strategy proposal. | No runtime-backed stages before confirmation. |
| `record_receipt` | Attach owner-route result to panel state. | Craft ledger updates require a governed write path. |
| `defer` | Keep item visible. | No mutation. |

Disallowed effects:

- writing directly to `.craft/ledger.yml` from the panel without a governed Craft
  update path;
- closing raw blockers directly;
- selecting a route on the user's behalf for a consequential decision;
- hiding stale exports;
- treating a route proposal, dispatch validation, or strategy preview as execution
  proof;
- collapsing multiple Craft scopes into one undifferentiated dashboard.

## 9. Pass Conditions

A static proof over fixture ledgers passes when a reader can answer:

- which Craft scope owns the work;
- whether the panel export is fresh or stale;
- what is pending by node;
- which row or next move is selected;
- why the recommended route is Interrogation, Decision Gate, Refine, export, or
  defer;
- what question the user is being asked;
- what will happen if the user selects each option;
- what will not happen automatically.

The proof fails if:

- pending work appears only as aggregate counts;
- the panel edits ledger authority directly;
- a decision gate has no explain-more route;
- Refine starts runtime-backed stages without a strategy confirmation;
- Interrogation asks a question that is not tied to a selected row or artifact;
- multiple scoped Craft ledgers are mixed without showing scope ownership.
