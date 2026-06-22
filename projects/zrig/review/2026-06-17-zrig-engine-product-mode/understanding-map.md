# Z-Rig Engine / Product-Mode Understanding Map

Dispatch: `2026-06-17-zrig-engine-product-mode-review`

## What Z-Rig Is Trying To Be

Z-Rig Turbo v5.5.3 is a governed multi-agent orchestration engine. Its product promise is not just "run several agents"; it is a mode-aware pipeline where the orchestrator owns state transitions, assigns seats, enforces gates, routes failures, preserves audit residue, and, in later waves, can deploy and monitor the result.

The review found a coherent product shape:

- `MICRO`: small bounded tasks.
- `STANDARD`: primary pipeline from provider probing through build, verify, review, deploy, sentinel, and writeback.
- `FULL`: additive high-stakes path with extra verification/adversarial waves.
- `AUTO`: implemented and documented as classifier-driven mode selection, but not present in the extracted PDF mode enum.

## Engine Flow

The core CLI exposes three operator commands:

- `validate`: load and structurally validate run config and task JSON.
- `classify`: run mode selection.
- `run`: execute the pipeline, defaulting to a stub executor unless `--live` is supplied.

In the current example path:

1. `validate` succeeds for `examples/run_config.json` and `examples/task_description.json`.
2. `classify` selects `STANDARD`.
3. Dry-run executes the standard wave sequence with the default stub executor.
4. The pipeline reports completed success, with `W5.5` and `W8.5` skipped on clean-run.

The standard dry-run shape is useful for state-machine smoke testing, but it is not product-mode proof of live governed execution.

## Authority Boundaries

### Spec Boundary

The extracted PDF establishes the strongest product authority seen in this review:

- PDF page 4 frames the mode lattice as `MICRO · STANDARD · FULL`.
- PDF page 8 lists run config mode enum values as `MICRO`, `STANDARD`, and `FULL`.
- PDF page 126 says the orchestrator decides what happens next and must reject invalid transitions.
- PDF page 128 requires each run to execute inside a dedicated filesystem namespace.
- PDF page 132 gives concrete later gate conditions, including `G4`, `G5`, `G10`, and `G11`.

When code or QuickStart expands beyond that PDF, the expansion should either be promoted into the spec or clearly marked as an implementation extension.

### Orchestrator State Boundary

The orchestrator is supposed to be the execution-state authority. The code partly supports that with manifests, wave records, gates, routing, and run summaries. The weak spots are state that is either:

- checked too generically, as with unimplemented gates;
- counted in a local seat scope, as with failover caps;
- accepted from bridge output, as with model/family identity;
- written non-fatally, as with residue persistence.

Product-mode behavior should keep these under trusted orchestrator control.

### Gate Boundary

The key risk is gate fallback. The current code maps later product waves to gate IDs, but only a subset have specific evaluators. Missing evaluators use a generic gate that checks registry integrity, timeout, and output presence. That means a syntactically non-empty but semantically failed deploy or sentinel output can pass.

The gate model is strong enough to carry Z-Rig, but product/live modes need a fail-closed policy for missing or generic evaluators.

### Bridge Boundary

The live bridge protocol writes dispatch requests and reads output manifests. That gives Z-Rig a workable external-agent integration path, but the bridge is a trust boundary:

- operator docs need the request/output contract;
- bridge-reported identity must not override trusted seat identity;
- missing runtime dependencies must be declared;
- blocked live imports should not be discovered only at run time.

### Deploy And Sentinel Boundary

Deploy and sentinel are side-effectful product surfaces. The implementation has modules for deployment, integration, and sentinel checks, but direct W10/W11 execution depends on top-level context keys not supplied by the normal pipeline context. The CLI also lacks explicit deploy/monitor validation commands.

Until this is fixed, Z-Rig can describe deploy/sentinel waves, but cannot cleanly prove an operator-reachable product path for them.

### Audit, Residue, And Metrics Boundary

Residue and metrics are the engine's memory and improvement substrate. Today:

- residue write construction is schema-incompatible and non-fatal;
- metrics triggers exist but are not wired into pipeline completion;
- dry-run can complete while residue persistence fails.

For demo mode, warning may be acceptable. For product/live mode, failed residue or unwired metrics should either degrade assurance explicitly or fail closed according to policy.

## Mental Model For Reviewers

Use three evidence classes:

1. Spec evidence: PDF mode lattice, gate tables, execution-state invariants, namespace requirements.
2. Engine evidence: source code paths, gate registrations, pipeline context, manifests, dispatch, routing, deploy/sentinel modules.
3. Runtime evidence: safe CLI outputs and focused local reproductions.

Do not collapse these classes. A dry-run completion proves that the state machine can traverse a stubbed path. It does not prove that live bridge, deploy, sentinel, identity, residue, or side effects satisfy product-mode promises.

## Current Product-Mode Assessment

Z-Rig is promising and structurally legible, but not yet product-mode trustworthy. The architecture has the right named parts; the current implementation lets too many of those parts report success through fallback, underdocumented, or non-authoritative paths.

The fastest path to a credible product mode is:

1. Close the generic-gate gap.
2. Make live bridge identity and manifest contracts explicit.
3. Make deploy/sentinel reachable and fail-closed.
4. Fix residue persistence and declared dependencies.
5. Reconcile PDF, QuickStart, and code around `AUTO`.

Once those are fixed, the existing CLI, manifest, wave, and gate skeleton can become a useful governed agent pipeline rather than only a convincing dry-run harness.
