# Execution Pack: High-Attention, Low-Parameter Experiment Protocol

## Purpose

Cross-task choreography for the high-complexity plan. Task and SWU definitions
remain authoritative in [WORK-PACK.md](WORK-PACK.md) and `work-pack/tasks/`.

## Planning Control Fields

| Field | Value |
| --- | --- |
| planningGateStatus | block |
| complexity | high |
| baselineWave | W0 |
| activePlanRef | [W0 foundation](work-pack/waves/W0-foundation.md) |
| workPackManifest | [WORK-PACK.md](WORK-PACK.md) |
| layeringArtifact | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) |
| specRef | [SPEC.md](SPEC.md) |
| activeLayerWindow | L0 |
| readinessProfile | pilot |

## Wave Choreography

| Wave | Layer question | Tasks/SWUs | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0-foundation.md) | Is the intended claim and machine contract explicit? | DECISIONS 001–005; CONTRACTS 006 | User authorizes decision process. | Approved decisions and passing schema fixtures. |
| [W1](work-pack/waves/W1-offline-witness.md) | Does fixture-to-score semantics close deterministically? | FIXTURES 007–008; WITNESS 010 | W0 pass. | Byte-identical offline witness. |
| [W2](work-pack/waves/W2-measurement-smoke.md) | Can one exact stack measure short/long cells reliably? | ADMISSION 009; MEASURE 011 | W1 pass plus resource authorization. | Capacity and repeat smoke receipts. |
| [W3](work-pack/waves/W3-decision-pilot.md) | Does the paired experiment produce a decision-bearing result? | MEASURE 012; ANALYZE 013–014 | W2 pass and frozen inference matrix. | Analysis, frontier, phase decision. |
| [W4](work-pack/waves/W4-closeout-extension.md) | Is the result aligned, publishable, and worth one extension? | VERIFY exemption | W3 phase decision. | Audit closeout or explicit stop. |

## Parallelization Boundaries

- W0 decisions are sequential from SWU 001; schema scaffolding may not freeze
  decision-dependent enums before approvals.
- In W1, generator/provenance work precedes renderer/scorer integration.
- W2 admission probes are local/hardware-bound and must not share a GPU with
  uncontrolled workloads.
- W3 matrix shards may execute in parallel only with immutable inputs,
  disjoint output paths, identical admitted stack, and parent join validation.
- Analysis starts only after the eligibility ledger closes required pairs.

## Receipt Contract

Every bounded execution returns:

```yaml
swu_id: SWU-HALP-NNN
result: pass | flag | block | interrupted
capability_ref: task-session | experiment-harness | decision-gate
receipt_kind: native-stage | subagent | local-fallback | blocked
receipt_artifact: path-or-none
files_touched: []
validation: []
blockers: []
residue: []
reroute: owner-or-none
handoff_note: concise parent synchronization note
```

## Stop Conditions

- Any decision, schema, determinism, compatibility, capacity, or telemetry gate
  failure stops its dependent wave.
- No available long-bin admitted cell stops the primary long-context study.
- No remaining cell capable of changing feasibility, Pareto membership,
  normalization order, or mechanism explanation stops that arm.
- A typed failure creates residue and a repair/stop decision; it is not erased.
