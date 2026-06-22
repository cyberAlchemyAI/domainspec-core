# Z-Rig Engine And Product Mode Review Strategy

Status: proposed; check-tension gate passed; not confirmed; not registered; not executed.

This strategy uses `domainspec-subagents-strategy` for a governed review dispatch over
`projects/zrig`. It is intentionally pre-runtime: no row has been appended to
`telemetry/agents/subagents-dispatch.yaml`, and no Z-Rig review agents have been launched.
Execution requires an explicit human confirmation of the frozen sheet below.

## Why Dispatch

Principle-1 triggers are present:

- Synthesis: the review must combine the PDF specification, QuickStart, Python engine,
  examples, tests, and product-mode/operator claims.
- Context protection: raw code/spec/test output would be larger than the parent should
  carry.
- Isolation: review attacks should be discardable and independently checked before they
  become change requests.
- Parallelism: fidelity, mechanics, operability, and abuse/gaming lenses can run
  concurrently.

The route is `dispatch_type: review`, not `research`, because the target artifacts already
exist and the deliverable is verified change requests.

## Evidence Boundary

Initial local evidence used to scope the sheet:

- `projects/zrig/Z-RIG-TURBO-V5.5.3-SPECIFICATION.pdf` is present as a 139-page PDF. This
  environment did not have `pdftotext`; spec-vs-code claims must therefore quote extracted
  PDF evidence during execution before they are accepted.
- `projects/zrig/z-rig-turbo-v5.5.3-engine.tar.gz` and the extracted
  `z-rig-orchestrator/` source are present.
- `QUICKSTART.md` claims the product is a multi-model orchestration pipeline and gives
  product stats, modes, run commands, wave sequence, gates, failure routing, and key files.
- `src/zrig/manifest.py` defines STANDARD, MICRO, and FULL wave sequences.
- `src/zrig/config.py` defines `AUTO`, `MICRO`, `STANDARD`, and `FULL` modes.
- `src/zrig/live_executor.py` and `src/zrig/openclaw_bridge.py` define the `--live`
  OpenClaw bridge path.
- Tests cover AUTO mode selection, FULL-mode seat/wave additions, family diversity,
  deployment, pipeline integration, dispatch, and summary behavior.

## Required Outputs

All dispatch outputs land in:

`projects/zrig/review/2026-06-17-zrig-engine-product-mode/`

Required by the review type:

- `attacks.md`: collected attacker and verifier returns, verbatim.
- `findings.md`: cited change requests; every surviving finding quotes or cites the
  artifact evidence and every refuted finding is dropped.

Additional requested understanding artifact:

- `understanding-map.md`: a concise map of engine concepts, product-mode surfaces, and
  source/test anchors. It must cite `attacks.md`, `findings.md`, or direct file evidence.

## Proposed Dispatch Row

The following JSON is the schema-clean row to register only after explicit confirmation.
It deliberately excludes the human-facing pairwise tension evidence below because the
appender rejects unknown keys.

```json
{
  "dispatch_id": "2026-06-17-zrig-engine-product-mode-review",
  "schema_version": "0.6.0",
  "dispatch_type": "review",
  "goal": "Understand and review the Z-Rig Turbo v5.5.3 engine and product mode, producing a cited understanding map plus verified change requests for any engine/product-mode gaps.",
  "context": "Target corpus is projects/zrig, including Z-RIG-TURBO-V5.5.3-SPECIFICATION.pdf, z-rig-turbo-v5.5.3-engine/z-rig-orchestrator, QUICKSTART.md, src/zrig, examples, and tests. The engine presents MICRO/STANDARD/FULL/AUTO modes, dry-run and --live OpenClaw bridge execution, gated pipeline waves, deployment, sentinel monitoring, residue, and failure routing. Review is read-only over engine/spec artifacts; outputs land in projects/zrig/review/2026-06-17-zrig-engine-product-mode/.",
  "max_loops": 1,
  "final_approver": "Brandenburg, Martin",
  "anti_bias_global": "Product promise vs executable engine reality across spec, code, tests, and operator path.",
  "working_folder": "projects/zrig/review/2026-06-17-zrig-engine-product-mode/",
  "groups": [
    {
      "group_id": "attackers",
      "n": 4,
      "robot_talks": true,
      "layers": 1,
      "anti_bias": "attack-vector (fidelity/governance vs mechanics/correctness vs operability vs abuse/gaming)",
      "agents": [
        {
          "agent_name": "Turing, Alan",
          "role": "explorer",
          "model": "gpt-5.5",
          "token_budget": 1800,
          "angle": "fidelity/governance lens: attack contradictions between the PDF/QuickStart product promise and the implemented engine boundaries.",
          "initial_prompt": "Review Z-Rig read-only from the fidelity/governance lens. Target corpus: projects/zrig/Z-RIG-TURBO-V5.5.3-SPECIFICATION.pdf, QUICKSTART.md, and z-rig-orchestrator source/tests. Extract or quote exact spec/doc evidence before making any spec-vs-code claim. Attack contradictions between product promise, documented modes, waves, gates, live bridge, deployment, sentinel behavior, and implemented boundaries. Return candidate findings with file/page/line evidence, severity, and proposed fix. Also return a concise concept map slice for understanding-map.md. Budget about 1800 tokens."
        },
        {
          "agent_name": "Ashby, W. Ross",
          "role": "explorer",
          "model": "gpt-5.5",
          "token_budget": 1800,
          "angle": "mechanics/correctness lens: attack state-machine, gate, mode-selection, manifest, retry, timeout, and failure-routing behavior against tests and code.",
          "initial_prompt": "Review Z-Rig read-only from the mechanics/correctness lens. Trace src/zrig/pipeline.py, gates.py, classifier.py, manifest.py, config.py, dispatch.py, families.py, and tests. Attack state transitions, mode selection, wave ordering, gate predicates, retry bounds, timeout routing, manifest checkpointing, family diversity, and failure routing. Run only safe local checks if useful, such as pytest or CLI dry-run/classify; do not use --live. Return candidate findings with exact file/line/test evidence, severity, proposed fix, and a concept map slice. Budget about 1800 tokens."
        },
        {
          "agent_name": "van Lamsweerde, Axel",
          "role": "explorer",
          "model": "gpt-5.5",
          "token_budget": 1800,
          "angle": "operability lens: attack whether a fresh operator can run dry-run, classify, --live bridge, deployment, sentinel, and artifact paths end to end without inventing steps.",
          "initial_prompt": "Review Z-Rig read-only from the operability lens. Attack QUICKSTART.md, CLI entry points, examples, pyproject, live_executor.py, openclaw_bridge.py, deploy_adapter.py, deploy_config_schema.py, sentinel_monitor.py, run_summary.py, and generated artifact paths. Ask whether a fresh operator can validate configs, classify, dry-run, understand --live bridge requirements, inspect outputs, deploy, and monitor without hidden assumptions. Do not perform real deployment or --live dispatch; use blocked-run notes when runtime prerequisites are missing. Return candidate findings with exact evidence, severity, proposed fix, and a concept map slice. Budget about 1800 tokens."
        },
        {
          "agent_name": "Rittel, Horst",
          "role": "explorer",
          "model": "gpt-5.5",
          "token_budget": 1800,
          "angle": "abuse/gaming lens: attack ways configs, gates, provider diversity, failover, deployment, and bridge artifacts can satisfy the letter while defeating product intent.",
          "initial_prompt": "Review Z-Rig read-only from the abuse/gaming lens. Attack config and task schema assumptions, gate pass conditions, family diversity and failover, generated bridge files, deployment config validation, sentinel assumptions, ignored/generated files, and residue/metrics. Look for ways a run could satisfy a mechanical predicate while undermining product intent, safety, independence, or auditability. Do not modify source. Return candidate findings with exact evidence, severity, proposed fix, and a concept map slice. Budget about 1800 tokens."
        }
      ]
    },
    {
      "group_id": "synthesizer",
      "n": 1,
      "agents": [
        {
          "agent_name": "Shannon, Claude",
          "role": "writer",
          "model": "gpt-5.5",
          "token_budget": 3200,
          "initial_prompt": "Synthesize the attacker returns into attacks.md, findings.md, and understanding-map.md. Preserve each attacker's initial and final positions because the attacker group uses robot_talks. Deduplicate candidate findings, keep severity grounded, and cite the exact attacker return plus direct artifact evidence for every load-bearing claim. Separate verified product understanding from change requests. Prepare the draft for verifier zig-zag; do not soften or retain findings that lack proof. Budget about 3200 tokens."
        }
      ]
    },
    {
      "group_id": "verifiers",
      "n": 2,
      "robot_talks": true,
      "layers": 1,
      "anti_bias": "attack-vector (source-evidence refutation vs executable-reproduction refutation)",
      "agents": [
        {
          "agent_name": "Tetlock, Philip",
          "role": "skeptic",
          "model": "gpt-5.5",
          "token_budget": 2200,
          "angle": "source-evidence refutation gate: drop any finding lacking exact quoted evidence from spec, docs, code, or tests.",
          "initial_prompt": "Verify the synthesized findings from the source-evidence refutation gate. Drop any finding lacking exact quoted or line/page-grounded evidence from spec, docs, code, examples, or tests. Check that PDF-derived claims include extracted/quoted spec evidence. Return which findings survive, which are refuted, and the exact reason. Budget about 2200 tokens."
        },
        {
          "agent_name": "Schön, Donald",
          "role": "skeptic",
          "model": "gpt-5.5",
          "token_budget": 2200,
          "angle": "executable-reproduction refutation gate: drop or downgrade any behavior finding not reproduced by pytest, CLI dry-run/classify, or a reasoned blocked-run note.",
          "initial_prompt": "Verify the synthesized findings from the executable-reproduction refutation gate. For behavior claims, run safe local checks when possible: pytest, zrig validate, zrig classify, and dry-run zrig run with examples. Do not use --live and do not deploy. If a claim depends on OpenClaw, deployment, sentinel, or external runtime, produce a blocked-run note instead of pretending it was reproduced. Return surviving and refuted findings with exact command evidence or blocked-run reason. Budget about 2200 tokens."
        }
      ]
    },
    {
      "group_id": "coverage_approver",
      "n": 1,
      "agents": [
        {
          "agent_name": "Brandenburg, Martin",
          "role": "auditor",
          "model": "gpt-5.4",
          "token_budget": 1600,
          "initial_prompt": "Final approval audit. Check that every declared target class was attacked: PDF/spec, QuickStart/operator docs, config/schema, mode classifier, manifest/wave sequences, pipeline/failure routing, gates, dispatch/family diversity/failover, live OpenClaw bridge, deployment/sentinel, residue/metrics, examples, and tests. Check that every surviving finding is cited and every refuted finding was dropped. Recommend ACCEPT or REJECT for the change-request list and understanding map. Budget about 1600 tokens."
        }
      ]
    }
  ],
  "connections": [
    {
      "from": "attackers",
      "to": "synthesizer",
      "type": "sequential"
    },
    {
      "from": "synthesizer",
      "to": "verifiers",
      "type": "zig-zag",
      "loop_cap": 2
    },
    {
      "from": "synthesizer",
      "to": "attackers",
      "type": "feedback",
      "loop_cap": 1
    },
    {
      "from": "verifiers",
      "to": "coverage_approver",
      "type": "sequential"
    }
  ]
}
```

## Tension Evidence

The check-tension gate passed with two independent agents:

- Checker agent `019ed349-6a69-7ed1-99bb-4cd7c214eb8c`: PASS.
- Reviewer agent `019ed349-bb70-7821-882f-e5cfd6b2bff2`: PASS.

Pairwise predicted disagreement evidence for `attackers`:

- Turing runs spec-and-doc fidelity, Ashby runs executable mechanics on the attack-vector
  axis; a bias in Turing toward stated promises would be exposed by Ashby's code/test trace.
- Turing runs spec-and-doc fidelity, van Lamsweerde runs operator execution path on the
  attack-vector axis; a bias in Turing toward conceptual completeness would be exposed by
  missing run steps.
- Turing runs spec-and-doc fidelity, Rittel runs abuse/gaming on the attack-vector axis; a
  bias in Turing toward nominal compliance would be exposed by adversarial bypasses.
- Ashby runs executable mechanics, van Lamsweerde runs operator execution path on the
  attack-vector axis; a bias in Ashby toward internal correctness would be exposed by
  unusable product workflow.
- Ashby runs executable mechanics, Rittel runs abuse/gaming on the attack-vector axis; a
  bias in Ashby toward happy-path tests would be exposed by adversarial config/gate cases.
- van Lamsweerde runs operator execution path, Rittel runs abuse/gaming on the attack-vector
  axis; a bias in van Lamsweerde toward documented flows would be exposed by hostile or
  ambiguous usage.

Pairwise predicted disagreement evidence for `verifiers`:

- Tetlock runs source-evidence refutation, Schon runs executable-reproduction refutation on
  the attack-vector axis; a bias in Tetlock toward textual proof would be exposed by
  runnable behavior, while a bias in Schon toward runtime-only proof would be exposed by
  exact source/spec text.

## Execution Plan After Confirmation

1. Freeze this sheet exactly or revise and re-run check-tension.
2. Write the JSON row to `.register-dispatch.tmp.json`.
3. Register with:

   ```sh
   node implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/register-dispatch/append-dispatch.cjs .register-dispatch.tmp.json
   ```

4. Delete `.register-dispatch.tmp.json`.
5. Launch `attackers` in parallel. Because `robot_talks: true`, preserve initial and final
   positions for the synthesizer.
6. Launch `synthesizer`; then run the `synthesizer` to `verifiers` zig-zag with
   `loop_cap: 2`.
7. Fire the feedback edge only if the synthesizer or verifiers identify missing material
   that the attackers must gather.
8. Launch `coverage_approver`.
9. Parent verifies any claimed file writes or checks before accepting completion.
10. Append a close row with `exit_reason` and `agents_spawned`.

Expected close shape if resolved on the first loop:

```json
{
  "close_of": "2026-06-17-zrig-engine-product-mode-review",
  "exit_reason": "resolved",
  "agents_spawned": {
    "total": 8,
    "tree": {
      "explorer": 4,
      "writer": 1,
      "skeptic": 2,
      "auditor": 1,
      "helpers": 0
    },
    "loops_used": 1
  }
}
```

## Suggested Verification Surface

These are review-time checks, not checks already run by this strategy pass:

```sh
cd projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m zrig validate --config examples/run_config.json --task examples/task_description.json
PYTHONPATH=src python3 -m zrig classify --config examples/run_config.json --task examples/task_description.json
PYTHONPATH=src python3 -m zrig run --config examples/run_config.json --task examples/task_description.json --output-dir /tmp/zrig-review-dry-run
```

Do not run `--live`, deployment, or sentinel network checks during review unless the human
explicitly provides the OpenClaw/deployment runtime and confirms that side-effect boundary.
