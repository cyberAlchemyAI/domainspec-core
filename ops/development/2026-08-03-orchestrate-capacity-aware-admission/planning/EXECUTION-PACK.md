# Execution Pack: Capacity-Aware Orchestrate Admission

## Control

| Field | Value |
| --- | --- |
| planningGateStatus | pass for SWU-OCA-001 Task Session preflight only |
| complexity | high |
| baselineWave | W0 |
| activePlanRef | `work-pack/waves/W1-L0-ADMISSION.md` |
| workPackManifest | `WORK-PACK.md` |
| layeringArtifact | `IMPLEMENTATION-LAYERING.md` |
| specRef | `../define/SPEC.md` |
| activeLayerWindow | L0 |
| readinessProfile | pilot |

## Wave order

```text
W0 baseline and owner preflight
  -> W1 SWU-OCA-001 whole-wave admission
  -> W2 SWU-OCA-002 failed-spawn evidence
  -> G-L0
  -> W3 SWU-OCA-003 Codex provider ceiling
  -> W4 SWU-OCA-004 route options
  -> W5 SWU-OCA-005 generated parity
  -> G-L1
  -> W6 read-only integrated verification
```

There is no parallel implementation wave. Canonical SWUs overlap in
`SKILL.md`, coordinator, and validation surfaces, so sequential receipts are
required. Later host reservation/release and consumer adoption are not in this
execution pack.

## Gates

| Gate | Required evidence | On failure |
| --- | --- | --- |
| G-W0 | clean target-path baseline, unrelated-dirty-work classification, submodule on `main`, context pack, material package, closeout binding | block before mutation |
| G-OCA-001 | sufficient plus missing, malformed, stale, cross-host/run/wave, advisory, unknown, insufficient, reservation-required, omitted-policy, and mixed-version cases; zero-action/attempt invariant; v0.1 compatibility regressions | repair OCA-001 |
| G-L0 | OCA-001 and OCA-002 terminal receipts; canonical causal stream pass | do not start provider work |
| G-OCA-003 | current Codex profile returns exact supported ceiling; inventory-only case remains advisory/unknown | retain conservative block |
| G-OCA-004 | no route option becomes approved execution bytes; infeasible capabilities omitted | repair projection |
| G-OCA-005 | all manifest-declared generated packages match canonical source/support | repair generation only |
| G-L1 | all five SWU receipts plus read-only verification | stop before lease/release or consumer work |

## Parallelization boundary

None inside the active pack. Validation commands may run concurrently only
when they write to separate temporary directories and do not mutate snapshots.
The current host-capacity defect is itself a reason not to create a parallel
implementation dispatch before OCA-001 exists.

## Stop conditions

- target Orchestrate files have unrelated live changes;
- implementation would hard-code or infer a host limit;
- a blocked path emits any action document or native spawn attempt;
- route projection silently changes approved topology;
- public files receive private incident, account, or consumer data;
- generated files are edited without canonical change and regeneration;
- a mutation-capable SWU lacks current material or closeout binding;
- user requests commit, push, publication, or deployment without a separate
  authorized route.
