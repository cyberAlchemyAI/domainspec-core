---
decision_id: DG-AOG-LANG-ACTION-BINDING-002
status: resolved
selected_option: LANG-HOST-DEFAULT-AUDITION
resolved_at: 2026-08-16T15:35:01Z
decision_source: user-selected exact option and approved implementation
target_scope: language-audition action binding before dispatch confirmation
source_sheet: ../language-tournament/audition/dispatch-sheet.json
source_sheet_sha256: 67e5fe082c718111fb0ca7569fed3c06789fcb406675cb51ceebf0ee23497f4d
source_route: ../language-tournament/audition/DISPATCH-ROUTE.json
source_route_sha256: 5beb4797222828e7f319b9d27dc99960f46f16588b68556bf7aa9dda8b4a8b4e
source_audit: ../language-tournament/audition/ACTION-BINDING-AUDIT.json
admissibility_request: language-audition-action-binding.request.json
admissibility_request_digest: 4506c154d8e947a269db170739d4ea2499574c6a00dff7a3dd11d2f943d6be06
admissibility_receipt: language-audition-action-binding.receipt.json
---

# Language-audition action-binding decision

## Decision question

How should the proposal close the gap between the human-reviewed agent sheet and
the smaller field set persisted by the current Orchestrate native action?

## Why This Blocks Confirmation

The sheet materially selects nine identities, models, token budgets, angles,
and exact prompts. The current native action persists role, capability, target,
mode, policies, scopes, and references. The route now points every role at an
exact sheet selector, so the persona, angle, and prompt are available as an
indirect input, but they are not separately action-validated. Model and token
budget are not carried at all, and the host exposes no enforceable token-budget
parameter. Structural route validation therefore passes while exact execution
fidelity remains blocked.

## Admissible Options

### `LANG-HOST-DEFAULT-AUDITION` — revise around honest host defaults

Revise the material sheet before confirmation: stop promising the Luna/Terra/Sol
split, label model selection as inherited host-default behavior, label token
budgets as advisory self-limits, bind each persona/angle/prompt through the
exact sheet digest and row selector, and add a proposal-local selector-binding
check. Then rerun schema `0.8.0` readiness, both exact-digest tension checks,
material projection, route validation, and the confirmation gate.

Benefit: smallest route back to the language audition; preserves the actual
methodology diversity that matters for this editorial experiment.

Cost/risk: the run will not test whether different model families improve the
candidate spread, and token budgets remain advisory rather than host-enforced.

Choose when: the teaching-method contrast matters more than model routing.

Downstream impact: proposal files and digests change; no registration, spawn,
HTML mutation, publication, or deployment occurs until a later confirmation.

Recommendation: choose this option. The experiment is about language movement,
not model benchmarking, so honest host defaults remove a false precision without
weakening the three candidate methodologies or the two independent review axes.

### `LANG-ORCHESTRATE-BINDING-WORKPACK` — repair the runtime contract first

Defer the audition and prepare a separate public Arcanum Work Pack that versions
the action schema, coordinator, driver, host profile, and fixtures so identity,
model, angle, prompt, and advisory budget are explicit persisted fields. Model
must be passed to `collaboration.spawn_agent`; token budget must remain advisory
unless the host gains a real enforcement mechanism.

Benefit: creates a reusable exact binding for future governed dispatches.

Cost/risk: materially larger scope, public Arcanum source and generated-package
work, regression testing, and a separate implementation/owner gate before the
language audition can resume.

Choose when: heterogeneous model routing is part of the experiment's claim, or
the runtime contract should be repaired before any new governed dispatch.

Downstream impact: the guide remains unchanged while a separately authorized
runtime Work Pack is designed and, only after another gate, implemented.

### `LANG-AUDITION-HOLD` — stop at the blocked proposal

Keep the current proposal, static audit, and gate evidence as-is. Do not revise
the sheet or runtime.

Benefit: no further scope or coordination cost.

Cost/risk: the beginner-language tournament does not run and the reported
terminology friction remains unresolved.

Choose when: neither proposal revision nor runtime repair should proceed now.

Downstream impact: guide, deployment, ledger, actions, and target-agent state
remain unchanged.

## Structurally Rejected Shortcut

`LANG-CONFIRM-CURRENT-ROUTE` is inadmissible. Human confirmation cannot fill a
missing persisted action contract, and executing it would overstate fidelity to
the reviewed material strategy.

## Current Decision State

- Selected option: `LANG-HOST-DEFAULT-AUDITION`
- Result: `PASS`
- Rationale: the experiment compares teaching movements rather than model
  families, so honest host inheritance removes unsupported routing precision
  while preserving the three methodology and two review axes.
- Remaining blocker: none at this decision gate; the revised material proposal
  must still pass its fresh readiness, tension, selector-binding, route, and
  post-validation human-confirmation gates.
- Consequential mutations after the blocker: none
- Dispatches registered or target agents spawned: none
- Guide or deployment bytes changed: none

The selected option authorizes revision of the proposal and its gate evidence.
It does not pre-confirm unvalidated future bytes, register the dispatch, spawn
target agents, edit the guide, or deploy a derivative.
