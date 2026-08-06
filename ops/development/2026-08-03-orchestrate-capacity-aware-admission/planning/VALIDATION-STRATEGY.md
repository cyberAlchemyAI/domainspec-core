# Validation Strategy

## Evidence states

- Design fixtures: authored, unexecuted contracts.
- Plan checks: authoring/shape evidence only.
- Future SWU receipts: implementation evidence for exact target bytes.
- Live host capacity, reservation, release, and user experience remain
  separately evidenced.

## Per-SWU validation

### SWU-OCA-001

- authoritative sufficient evidence -> exact full action set;
- missing, malformed, stale, cross-host/run/wave, advisory, unknown, and
  insufficient evidence -> zero action documents and zero spawn attempts;
- reservation-required -> typed unsupported block and zero actions in the
  active snapshot-only contract;
- capacity evaluator output validates against its versioned schema;
- `legacy_v0_1` is available only through the separately named compatibility
  entrypoint and declared v0.1 fixtures; it is never a governed-execution
  default or fallback;
- `strict_whole_wave_v0_2` requires policy, evidence, expected host, and injected
  evaluation time together; missing, omitted, unknown, or mixed-version inputs
  block without downgrade.

### SWU-OCA-002

- `action_attempted -> host_spawn_failed ->
  pre_agent_failure_receipt_admitted -> gate_block` validates;
- a null-agent failure receipt cannot gate-pass;
- fabricated agent ID, missing failure event, duplicate receipt, and dependent
  action before block fail;
- current success, timeout, interrupt, and partial-wave cleanup tests pass.

### SWU-OCA-003

- authoritative provider evidence is admitted only with exact scope/freshness;
- `list_agents`-style inventory without a total remains advisory or unknown;
- retained completion never maps to released/reusable without host proof;
- provider unsupported returns a typed block, not a missing-field crash;
- preflight performs no spawn/wait/interrupt call.

### SWU-OCA-004

- smaller, serial, inline, fresh-session, queue, defer, and cancel options appear
  only when their owner capability is available and semantics remain valid;
- material topology/session changes set validation and renewed-confirmation
  requirements;
- projection emits no dispatch registration, action, or owner call;
- private provider details do not cross the neutral schema.

### SWU-OCA-005

- generate Codex, repo-local, and Claude Orchestrate packages in a temporary
  target from canonical Arcanum;
- sync only the three exact Orchestrate package directories after reviewing the
  diff;
- run bootstrap-generation parity;
- prove tests and caches are excluded and support paths are byte-equal.

## Exact regression commands

```bash
python3 arcanum/runtime/orchestrate/tests/test_compile_actions.py
python3 arcanum/runtime/orchestrate/tests/test_reduce_receipts.py
python3 arcanum/runtime/orchestrate/tests/preflight/test_preflight_contract.py
python3 arcanum/runtime/orchestrate/tests/native-spawn/test_native_spawn_contract.py
python3 arcanum/runtime/orchestrate/tests/native-join/test_native_join_contract.py
python3 arcanum/runtime/orchestrate/tests/partial-wave/test_partial_wave_recovery.py
python3 arcanum/runtime/orchestrate/tests/evidence-order/test_evidence_order.py
python3 arcanum/runtime/orchestrate/tests/receipt-admission/test_receipt_admission_matrix.py
python3 arcanum/runtime/orchestrate/tests/bootstrap-generation/test_bootstrap_generation.py
```

New test paths are added by the owning SWUs and then included explicitly. Do
not rely on top-level unittest discovery; nested non-package test directories
are not recursively discovered.

## Boundary checks

```bash
git diff --check -- arcanum/runtime/orchestrate .agents/skills/orchestrate .arcanum/runtime/orchestrate .claude/skills/orchestrate ops/development/2026-08-03-orchestrate-capacity-aware-admission
rg -n "pre-task-session-readiness-gap|agent thread limit reached|/home/vrondelli|quota|account tier" arcanum/runtime/orchestrate
```

The marker scan expects no private incident/path detail in public canonical
source. Generic fixture language such as `capacity_exhausted` is permitted.

## Live canary boundary

No live native spawn is required for OCA-001..OCA-005 acceptance. A later L2
canary that reserves or spawns agents requires a new validated, capacity-safe,
user-approved dispatch and host-owner receipt.
