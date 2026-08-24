# Craft Consultation API Decisions

## DG-CAPI-NEXT-UNIT-20260805

- status: `resolved-pass`
- classification: `blocker`
- question: Which outcome should govern the next bounded Craft API step?
- selected option: `CAPI-NEXT-000`
- source of decision: `direct user response "1", mapped to the presented option CAPI-NEXT-000`
- opened at: `2026-08-05T21:28:05Z`
- resolved at: `2026-08-05T21:59:10.723Z`
- admissibility request: `decision-gates/20260805T212805Z-select-next-unit/option-admissibility-request.json`
- admissibility receipt: `decision-gates/20260805T212805Z-select-next-unit/option-admissibility-receipt.json`
- request digest: `9b75676455cb72934a8b79999a69c5fa34a5b1f3a5a38388c8822bd4cce6a2ab`
- decision result: `decision-gates/20260805T212805Z-select-next-unit/decision-result.json`

### Admissible options

#### CAPI-NEXT-000 — Select SWU-CAPI-000

- kind: `action`
- benefit: creates the missing immutable WaveDB `0.15.9` Craft snapshot and closes the first runtime evidence gap.
- cost or risk: writes only the declared isolated derived-snapshot and execution-evidence scopes; it may block if the current source inventory is no longer exactly 27 ledgers and 55 records.
- choose when: the owner wants to continue toward the API through the narrowest admitted predecessor.
- downstream impact: records owner selection only; a separate Task Session must still admit and execute `SWU-CAPI-000`. No successor starts automatically.
- reversibility: the selection can be superseded before execution; any later immutable attempt remains evidence rather than canonical Craft authority.
- hazard: `authority`
- owning gate: `craft-consultation-api-plan-owner`

#### CAPI-DEFER — Defer selection

- kind: `defer`
- benefit: preserves all evidence and avoids runtime work until the owner is ready.
- cost or risk: the Craft API remains blocked and the `0.15.9` snapshot gap stays open.
- choose when: timing, ownership, or scope needs more consideration.
- downstream impact: `allowedRoutes=[]` and `selectedUnit=null` remain unchanged.
- reversibility: fully reversible through a later Decision Gate.
- hazard: `reversible`

#### CAPI-STOP — Stop this effort

- kind: `stop`
- benefit: ends the current continuation path without additional mutation or runtime cost.
- cost or risk: no Craft API will be constructed from this Work Pack unless a later owner explicitly reopens it.
- choose when: the API direction is no longer desired.
- downstream impact: no Task Session is admitted; existing plans and receipts remain historical evidence.
- reversibility: a later owner may open a new governed decision, but this run remains stopped.
- hazard: `reversible`

### Structurally rejected next units

`SWU-CAPI-001` through `SWU-CAPI-009` were not presented because their declared predecessors, runtime evidence, owner gates, or L0-before-L1 conditions are incomplete. Exact reasons are preserved in the admissibility receipt.

### Remaining blockers

- Invoke Refresh must synchronize the selected unit and exact allowed route into the Work Pack before execution admission.
- A separate Task Session must admit `SWU-CAPI-000`; this decision does not execute it.
- `CAPI-B003` remains open until that Task Session creates and validates the new immutable `0.15.9` snapshot.
- `CAPI-B002` authentication/session and secret-provider ownership before the affected later API units
- `CAPI-B004` deployment evidence remains deferred outside the active L0 window

### Assumptions

- The target is the next bounded unit named by the current refresh handoff.
- Selecting a unit is not consent to execute it and does not satisfy Task Session admission.

### Resolution

The owner selected `CAPI-NEXT-000`. This resolves the next-unit choice and binds
the continuation to `SWU-CAPI-000` only. The Work Pack remains unchanged and
blocked: `selectedUnit=null`, `allowedRoutes=[]`, and no Task Session authority
has been granted. The next authorized lifecycle action is a separately requested
Invoke Refresh that materializes the selection without widening its scope.
