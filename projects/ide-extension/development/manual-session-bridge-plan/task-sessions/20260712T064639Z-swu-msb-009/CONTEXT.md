# Context Pack: SWU-MSB-009

- Task/SWU: `TASK-VALIDATION-WITNESS / SWU-MSB-009`
- Dependency: W2 complete
- Sources: Validation And Real Witness task contract, existing bridge-focused,
  adversarial, persistence, artifact, schema-enforcement, and workbench tests
- Runtime: local Codex; no delegation

## Boundaries And Decisions

- Reuse the focused oracles built beside each authority transition; aggregate
  them into one deterministic serial gate instead of duplicating behavior.
- Preserve a checked-in case-to-obligation matrix so coverage claims remain
  inspectable.
- Run the aggregate twice to expose order dependence or race flakiness.
- Browser and real-human evidence remain 010 and 011 respectively.

## Gate

- W2 complete; 88-test full suite passes.
- Required hostile/replay/restart/failure oracles are present and individually
  passing.
- Decisions/blockers: none.
- Gate verdict: PASS.
