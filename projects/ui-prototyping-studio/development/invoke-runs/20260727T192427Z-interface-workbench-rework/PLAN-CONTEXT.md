# Invoke Plan Context

## Objective

Remediate the current medium-complexity interface-workbench Plan against the
verified change requests in `plan-distill-review/findings.md` without reopening
approved Design or executing product work.

## Approved Inputs

- `ARCHITECTURE.md`, `UX-PLAN.md`, `WITNESS-CONTRACTS.md`
- `DESIGN-DISTILL.md`, `DESIGN-SELECTION-RESULT.json`
- prior review: `plan-distill-review/findings.md`
- current source anchors under `backend/src` and `backend/e2e`

Design remains `design-validator-pass`. All UPW witnesses remain planned and
unexecuted. Invoke Plan did not edit upstream Design artifacts.

## Remediation Boundary

Included:

- exhaustive exact mutation scopes and preflight bindings;
- authoritative token/equality/retry/exhaustion for coherent snapshot reads;
- current-route-only SWU-003 and later reusable route admission;
- pure context planning before atomic commit;
- 19-SWU decomposition;
- exact 008–013 acceptance selectors/mutants/receipts;
- inverse primary assertion ownership;
- semantic versus serialization edges;
- exact per-SWU closeout targets/permissions and W5 report contract.

Excluded:

- product source mutation or test execution;
- upstream Design changes;
- SWU selection or Task Session admission;
- human study, cross-browser, certification, release, deployment, or production
  claims.

## Complexity And Output

- Complexity: medium.
- Output: split work-pack.
- Canonical machine artifacts:
  `SWU-MANIFEST.json`, `SWU-SCOPE-INVENTORY.json`,
  `SWU-ACCEPTANCE-MATRIX.json`, `CLOSEOUT-SYNC-INVENTORY.json`.
- Fresh governed Plan Distill has now run over the remediated literal bytes and
  returned BLOCK. Verified repairs are in
  `plan-redistill-review/findings.md`.

## Current Admission

- Plan authoring repair: mechanically complete but semantically blocked.
- Plan Distill: BLOCK on task-shaped 016, 017, and 019 plus non-executable
  closeout/W5 contracts; two bounded precision repairs also remain.
- Selected SWU: none.
- Task Session: blocked.
- Next owner: deferred Invoke Plan remediation after explicit authorization.
