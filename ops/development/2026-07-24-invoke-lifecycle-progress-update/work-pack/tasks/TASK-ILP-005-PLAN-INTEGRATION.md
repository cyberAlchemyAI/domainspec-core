# TASK-ILP-005: Invoke Plan Epoch and Route Gate

## Objective

Make Invoke Plan emit separate authored-validity and handoff-readiness results,
author an immutable epoch candidate for one selected SWU, and never route
mutation execution unless readiness is admitted as ready.

- Layer/slice/wave: L2 / S2 / W2
- Lifecycle owner: Spellcraft
- Dependencies: SWU-ILP-002, 003, and 004
- Source contracts: current `arcanum/spells/invoke/plan.md`,
  `../../DESIGN.md`
- Write scope:
  - `arcanum/spells/invoke/plan.md`
  - `arcanum/spells/invoke/README.md`
  - owner-approved Invoke mode schemas/fixtures
  - generated Invoke mirrors only through canonical synchronization

## Algorithm

1. Complete normal Plan artifact validation and Distill.
2. Resolve zero or one selected SWU; more than one blocks epoch issuance.
3. If no mutation unit is selected, report handoff `not-needed`/`gated` without
   an epoch.
4. Build and independently validate the epoch candidate for the selected unit.
5. Invoke the mode producer and readiness validator.
6. Submit epoch/readiness transition evidence to the ratified owner.
7. Report authored validity and handoff readiness independently.
8. Emit a Task Session route only when the current owner receipt admits
   `handoff_ready`.
9. Treat old plans without these artifacts as `legacy_unadmitted`.

## Smallest Working Unit

### SWU-ILP-005

- Primary behavior: decide Plan's mutation-execution route.
- Acceptance boundary: the real Plan output and route matrix.
- Candidate children: output fields; epoch construction call; readiness call;
  route gate.
- Retained rationale: partial integration leaves a bypass where an authored
  pass can still route execution.
- Execution owner: `local-fallback` through Spellcraft.
- Done criteria:
  - authored pass + ready routes exactly one epoch/SWU;
  - authored pass + gated/blocked never routes Task Session;
  - authored failure never manufactures readiness;
  - no selected unit creates no mutation epoch;
  - plan repair of any control field requires successor.
- Validation:
  `python3 arcanum/spells/invoke/development/run-lifecycle-progress-fixtures.py --group plan-route`
- Handoff context: W1 receipts, current Plan fixtures, artifact boundary
  contract.

## Closeout

Use `../shared/CLOSEOUT-CONTRACT.md`. Canonical-first/generated-second parity is
mandatory. A generated mirror cannot be used as the source.

