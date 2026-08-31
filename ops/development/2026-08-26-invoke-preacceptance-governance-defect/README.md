# Invoke Preacceptance Governance Defect Repair Plan

## Outcome Brief

Invoke currently cannot carry a nonempty, unapproved candidate through its own
preacceptance path, and parts of that path can report misleading evidence. This
  package defines a bounded repair: represent staged candidate bytes without apply
  authority, validate declared structured/text postimages, bind the owner request to
  the exact frozen effect, exercise the real candidate, and collect every still-
  reachable blocker.

- Objective: make the Invoke preacceptance chain truthful before another owner
  request is emitted.
- Result: a proposal-only, source-grounded repair Work Pack with seven atomic repair
  units and an end-to-end regression boundary.
- Why it matters: the same governance mechanics should no longer interrupt Body
  War or another project after candidate bytes have already been prepared.

## Boundary and Next Decision

- Changed: planning artifacts in this private operations folder only.
- Unchanged: Invoke source, generated skill packages, Body War postimages, owner
  acceptance, application, Task Session admission, Git, publication, deployment,
  external effects, geometry, scoring, and privacy decisions.
- Open questions: the exact implementation baseline is not frozen because current
  Invoke files contain unattributed live changes; the lifecycle owner must classify
  those bytes and select a versioned staged-candidate encoding after a complete
  consumer inventory.
- User decision: none for this planning result. Exact repaired bytes will require a
  later owner decision.
- Next action: Spellcraft owns design acceptance, candidate implementation, and
  validation of the Invoke spell repair.

## Start Here

1. [WORK-PACK.md](WORK-PACK.md) — scope, state model, repair units, blockers, and
   authority boundary.
2. [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) — L0-L3 promotion
   decisions.
3. [EXECUTION-PACK.md](EXECUTION-PACK.md) — ordered implementation waves and exact
   stop conditions.
4. [VALIDATION-MATRIX.md](VALIDATION-MATRIX.md) — positive, negative, and
   full-lifecycle regression coverage.
5. [DISTILL-VALIDATION.md](DISTILL-VALIDATION.md) — smallest-unit and recomposition
   review.

## Source Evidence

- `projects/body-war/development/invoke-runs/20260826T132848Z-body-war-continuation-material/PREACCEPTANCE-BLOCKER-RECEIPT.json`
- `arcanum/spells/invoke/schemas/material-package.schema.json`
- `arcanum/spells/invoke/scripts/material_package_validator.py`
- `arcanum/spells/invoke/schemas/preacceptance-closure-manifest-v1.schema.json`
- `arcanum/spells/invoke/schemas/preacceptance-closure-receipt-v1.schema.json`
- `arcanum/spells/invoke/scripts/preacceptance_closure.py`
- `arcanum/spells/invoke/development/preacceptance-closure/test_preacceptance_closure.py`
- `arcanum/framework/GOVERNANCE-FLOW-CONTRACT.md`

The Body War receipt is private trigger evidence. Public Arcanum fixtures must be
synthetic and must not reproduce Body War prose, personal data, or private project
material.
