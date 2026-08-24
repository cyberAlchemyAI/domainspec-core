# Context Pack: SWU-WCSB-001

- Mode: Task Session standard context, local Codex runtime.
- Work Pack: `plan/WORK-PACK.md`.
- Selected unit: `SWU-WCSB-001` / `TASK-WCSB-01`.
- Objective: materialize and fixture-prove the deterministic reviewed-source
  build protocol without fetching source, installing dependencies, compiling,
  loading an addon, or reading Craft state.
- Dependencies: Define, Design, Plan, Dispatch, and Distill all pass.
- Material scope: `.gitignore`, the runner, validator, receipt schema, fixture
  shell entrypoint, fixture cases, and fixture driver.
- Validation output: one terminal Task Session receipt after all critical
  commands pass.
- Forbidden effects: network, checkout, npm install, native compilation,
  addon load, Craft, Git mutation, publication, and deployment.
- Closeout owner: `invoke:refresh:apply-approved`, bookkeeping-only, limited to
  the three declared Plan targets.
- Unique successor on pass: `SWU-WCSB-002`; no successor on block.
- Claim ceiling: runner/validator implementation and deterministic fixture
  proof only.

Every done criterion and validation command is acceptance-critical. There is
no unresolved multi-option decision in this unit.

