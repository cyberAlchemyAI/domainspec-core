# TASK-WCSB-01: deterministic source-build runner

## Execution status

- Status: `completed-pass`.
- Terminal receipt:
  `../../../execution/task-sessions/SWU-WCSB-001/terminal-receipt.json`.
- Evidence: seven exact material targets, one positive fixture, nine stable
  negative controls, static no-effect scan, and scoped whitespace pass.
- Closeout decision: select `SWU-WCSB-002`; this task does not itself perform
  the source checkout or native build.

## Objective and mapping

- Slice: S-WCSB-01.
- Layer/wave: L0 / W0.
- Objective: implement a fail-closed standard-library runner, receipt schema,
  validator, and deterministic fixtures without fetching source, installing
  dependencies, compiling, or loading WaveDB.

## Source contracts

- `../../../design/ARCHITECTURE.md#view-3-low-level-components`
- `../../../design/SOURCE-CONTRACTS.md`
- `../shared/context.md`
- `../../PLAN.md#implementation-decisions`

## SWU-WCSB-001

- Primary behavior: encode and fixture-prove the complete source-build protocol.
- Dependencies: Define pass, Design `design-validator-pass`, Plan/Dispatch/
  Distill pass.
- Selected: yes.
- Write scope:
  - `experiment/source-build/.gitignore`;
  - `experiment/source-build/runtime/run_source_build.py`;
  - `experiment/source-build/runtime/validate_source_build.py`;
  - `experiment/source-build/runtime/source-build-receipt.schema.json`;
  - `experiment/source-build/runtime/tests/run-fixtures.sh`;
  - `experiment/source-build/runtime/tests/fixtures/**`;
  - `experiment/source-build/execution/task-sessions/SWU-WCSB-001/**`.
- Forbidden effects: network access, source checkout, npm dependency
  materialization, lifecycle scripts, native build, addon load, Craft access,
  Git mutation, publication, deployment.

## Implementation detail

### Runner inputs

- repository root and source-build root;
- exact source URL and root commit;
- expected root build-file hashes and recursive gitlink policy;
- attempt ID and absent work-root target;
- expected Node/npm/toolchain identities and OpenSSL mode;
- output evidence directory.

### Runner algorithm

1. Parse explicit arguments and reject unknown/missing inputs.
2. Normalize every workspace path under `source-build/`; reject traversal,
   symlink escape, existing attempt target, or forbidden target.
3. Execute only a closed command table for Git source resolution, recursive
   submodules, hashing, `npm ci --ignore-scripts`, copy sources, build, direct
   Mocha tests, and canary.
4. Capture command, cwd, start/end time, exit code, and bounded stdout/stderr to
   attempt logs without recording environment dumps.
5. Stop on first failed command or identity check; emit a block receipt with a
   stable failure code and no addon handoff.
6. Write source, dependency, generated-source, build, and test manifests using
   canonical JSON and atomic replace inside the evidence directory.
7. Run the independent validator; write the terminal receipt last only when
   every acceptance field passes.

### Validator rules

- validate the receipt schema and supported schema version;
- require exact attempt/source/lock/toolchain identities;
- require all acceptance stages present exactly once and pass;
- verify every named evidence file and addon hash from live bytes;
- reject any forbidden effect, unclassified residue, missing log, missing
  output, extra/missing stage, or claim above the source-build ceiling;
- return stable diagnostics and nonzero exit on failure.

### Fixture matrix

- complete pass receipt;
- wrong source commit;
- missing recursive submodule record;
- lockfile drift;
- lifecycle scripts not disabled;
- missing addon;
- addon hash mismatch;
- failed upstream test;
- forbidden Craft effect;
- inflated npm/publication/cross-platform claim.

## Split analysis

Candidate children are runner, schema, validator, and fixtures. The runner is
unsafe without the validator/schema, while the validator has no meaningful
acceptance without positive and negative fixtures. They form one independently
reviewable protocol artifact and cannot pass safely in isolation.

## Done criteria and validation

- all declared material files exist and contain no placeholders;
- Python parses and `--help` succeeds for runner and validator;
- schema parses and requires all acceptance-critical fields;
- fixture suite accepts only the complete pass fixture and rejects every
  negative fixture with its expected stable code;
- static scan proves the fixture run performed no network/native/Craft effect;
- terminal Task Session receipt and joined Invoke Refresh owner receipt exist.

Validation commands:

```bash
python3 -m py_compile runtime/run_source_build.py runtime/validate_source_build.py
python3 runtime/run_source_build.py --help
python3 runtime/validate_source_build.py --help
bash runtime/tests/run-fixtures.sh
git diff --check -- source-build/.gitignore source-build/runtime
```

Execution owner: Task Session local. Expected result shape is the Task Session
contract with exact files, commands, validation, blockers, residue, and next
route. Successor is SWU-WCSB-002 only after joined closeout.
