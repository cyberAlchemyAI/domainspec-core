# Plan validation

## Outcome

The authored Plan contract is complete and deterministic enough to hand to the
readiness gate. Runtime admission remains blocked by design: no SWU has a frozen
material package, no SWU is selected, and no Task Session may begin.

## Validation evidence

- Define result: `pass`.
- Design result: `pass`; the denominator and selection replays are byte-identical.
- Execution dispatch: `pass` under `dispatch-spec` validation.
- JSON and JSON Schema artifacts: syntactically valid.
- Work Pack Readiness Audit, first pass: `block` with fourteen findings.
  - Five command working directories were not repository-relative.
  - Three fragment-bearing source selectors were not exact filesystem paths.
  - The terminal receipt `unit_id` constraint omitted an explicit string type.
  - Five SWUs intentionally lacked material-package evidence.
- Work Pack Readiness Audit, second pass:
  - `plan_contract_status`: `pass`
  - `receipt_semantics_status`: `pass`
  - `runtime_admission_status`: `block`
  - remaining findings: exactly five, one `material_package is null` blocker for
    each of `SWU-AKV-QRY-001` through `SWU-AKV-QRY-005`

The authoritative second-pass evidence is in
`readiness/results-r2/work-pack-readiness-report.json` and its Markdown view.

## Execution boundary

This validation ran authoring validators and the readiness audit only. It did not
run any SWU validation command, create the candidate query-contract directory,
modify an ontology, select an SWU, or allocate a Task Session.

## Next valid transition

Prepare and freeze the current material package for `SWU-AKV-QRY-001`, update the
immutable audit frontier through the package owner, and rerun the Work Pack
Readiness Audit. Only a runtime-admission `pass`, followed by explicit selection of
that SWU, may route into `task-session`.
