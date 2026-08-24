# Invoke Plan Validation

## Candidate package checks

- Design scope extractor: `pass`, receipt digest
  `25f969db6ab04949465a5ceaae09571fad9362fbc53239d5c3bd992c82dcff00`.
- Design selection validator: `pass`, `design-validator-pass`, fixed point,
  result digest
  `632574d620b42e6c6b3b3cda4d217b0bad35c2ee432a798ec9257e00968293a4`.
- Plan Markdown files: 19.
- Missing relative Markdown links: 0.
- Required Work Pack control fields: present.
- SWU IDs `SWU-WCP-001` through `SWU-WCP-008`: present.
- Template placeholders/TODO markers: none.

## Invoke validator baseline controls

All passed on 2026-08-04:

1. `run-validation-fixtures.sh`
2. `run-design-selection-fixtures.sh`
3. `run-distill-evidence-schema-fixtures.sh`
4. `run-distill-runtime-event-fixtures.sh`
5. `run-distill-semantic-fixtures.sh`
6. `run-distill-provenance-fixtures.sh`
7. `run-distill-active-mode-evidence-fixtures.sh`

These controls validate Invoke's machinery, not the candidate Plan's mutation
readiness. Task Session must independently admit the selected SWU.

## Verdict

- Authored Plan: `pass`.
- Selected read-only handoff: `pass`.
- Native mutation readiness: `block` pending exact package provenance.
