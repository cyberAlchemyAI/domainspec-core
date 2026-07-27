# TASK-ILP-008: Legacy Admission and Progress Projection

## Objective

Re-admit old plans without fabricating readiness and expose lifecycle progress
and churn as observational projections of admitted transitions.

- Layer/slice/wave: L3 / S3 / W3
- Lifecycle owners: Spellcraft for migration; Workflow Reflect for
  observational projection
- Dependencies: all W2 receipts
- Source contracts: `../../DESIGN.md`, `../shared/DECISIONS.md`

## SWU-ILP-008A: Legacy admission

- Primary behavior: convert one `legacy_unadmitted` plan into freshly validated
  current evidence or keep it unadmitted.
- Write scope:
  - owner-approved Invoke legacy adapter/schema/fixtures
  - `arcanum/spells/invoke/plan.md` only if the owner contract requires it
- Algorithm:
  1. Mark any plan lacking current epoch/readiness evidence
     `legacy_unadmitted`.
  2. Resolve one selected SWU and reconstruct the declared control graph from
     live artifacts.
  3. Produce a new epoch candidate and current producer/readiness evidence.
  4. Submit new transitions; never backdate or rewrite old receipts.
  5. Block ambiguity, missing paths, or unavailable owners.
- Acceptance boundary: one legacy admission verdict.
- Candidate children: marker; reconstruction; new evidence.
- Retained rationale: migration is valid only as one no-inference admission
  behavior.
- Done criteria: legacy-only evidence never routes; valid fresh revalidation
  creates current receipts; failures preserve history.
- Validation:
  `python3 arcanum/spells/invoke/development/run-lifecycle-progress-fixtures.py --group legacy`
- Execution owner: `local-fallback` through Spellcraft.

## SWU-ILP-008B: Progress and churn projection

- Primary behavior: derive one observational progress event from admitted
  transitions.
- Dependencies: SWU-ILP-008A
- Candidate write scope:
  - owner-approved Invoke observer envelope/schema
  - owner-approved Workflow Reflect signal schema/fixtures
- Algorithm:
  1. Consume admitted transition ID and owner receipt only.
  2. Emit goal, epoch, unit, from/to, mutation-crossed, blocker fingerprint,
     transition kind, owner return count, and progress verdict.
  3. Compute progress denominator and churn key.
  4. Report repeated unchanged key as `churn_blocked`; do not increment
     progress.
  5. Mark the event explicitly non-authoritative.
- Acceptance boundary: one deterministic projection event.
- Candidate children: event fields; denominator; churn.
- Retained rationale: all are one projection of an admitted transition.
- Done criteria: progress count differs from raw run/Refresh count; missing
  transition owner receipt cannot report progress; unchanged churn adds zero.
- Validation: owner-approved observer/Workflow Reflect fixture runner.
- Execution owner: `local-fallback` through owning lifecycle.

## Closeout

Each SWU independently uses `../shared/CLOSEOUT-CONTRACT.md`. Telemetry or
Inventory updates cannot satisfy the transition-owner receipt requirement.

