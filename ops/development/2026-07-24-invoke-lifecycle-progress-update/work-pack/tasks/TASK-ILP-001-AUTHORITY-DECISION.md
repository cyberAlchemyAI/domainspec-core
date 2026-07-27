# TASK-ILP-001: Transition Authority and Source Placement

## Objective

Ratify one legitimate transition-admission owner and exact public source
placement before any protocol code is written.

- Layer/slice/wave: L0 / S0 / W0
- Lifecycle owner: Spellcraft plus Arcanum governance
- Dependencies: none
- Blocker: `ILP-G01`
- Source contracts: `../../DEFINE.md`, `../../DESIGN.md`,
  `../shared/DECISIONS.md`, `../../LIFECYCLE-HANDOFF.md`
- Write scope: one new private decision receipt under
  `work-pack/session-evidence/SWU-ILP-001/`; no public or generated source

## Implementation detail

The owner must evaluate, not merely name, the authority model:

1. Identify the existing owner that can admit cross-capability lifecycle edges.
2. Prove that this owner does not create a second mutable current-state
   authority.
3. Name the exact public canonical paths for epoch, local-contract, readiness,
   change-impact, and transition schemas/validators.
4. List capabilities allowed to submit evidence.
5. List surfaces explicitly unable to admit transitions: Invoke Plan, Invoke
   Refresh, Task Session execution, validators, Inventory, observability,
   projections, status files, and cursors unless the selected owner is one of
   those under an explicit existing authority contract.
6. State whether a new definition/constitution decision is required.
7. Return `block` if two owners remain plausible or if source ownership and
   transition authority conflict.

## Smallest Working Unit

### SWU-ILP-001

- Primary decision: select transition-admission owner and source placement.
- Acceptance boundary: one receipt answers all seven steps with no competing
  owner or ambiguous path.
- Candidate children: owner selection; path selection; exclusions.
- Retained rationale: none can authorize implementation independently; a
  partial decision preserves the authority gap.
- Execution owner: `manual` through Spellcraft lifecycle assessment.
- Done criteria:
  - one owner named;
  - exact canonical paths named;
  - evidence submitters and excluded authority surfaces named;
  - public/private and promotion boundaries stated;
  - next route returned.
- Validation:
  - review against `../../DESIGN.md` authority table;
  - review against repository public/private boundary;
  - review that no new current-state projection is introduced.
- Handoff: use `../../LIFECYCLE-HANDOFF.md`; return its exact receipt shape.

## Synchronization

No Task Session closeout applies because the unit is non-mutating. A passing
receipt is source evidence for an Invoke `plan_repair` that resolves `ILP-G01`
and selects SWU-ILP-002. No execution epoch exists to reuse or supersede.

## Completion evidence

`work-pack/session-evidence/SWU-ILP-001/decision-receipt.json`

