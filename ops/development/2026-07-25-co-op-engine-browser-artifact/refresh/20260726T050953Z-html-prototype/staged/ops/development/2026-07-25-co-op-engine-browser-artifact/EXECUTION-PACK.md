# Execution Pack: Co-Op Engine L0 Serial Proofs

## Control

| Field | Value |
| --- | --- |
| planningGateStatus | pass |
| complexity | medium |
| baselineWave | W0 |
| activePlanRef | `WORK-PACK.md` |
| workPackManifest | `WORK-PACK.md` |
| layeringArtifact | `IMPLEMENTATION-LAYERING.md` |
| activeLayerWindow | L0 |
| readinessProfile | pilot |

## Wave Choreography

```text
W0 strict source/runtime/scope baseline
  -> W1 SWU-COOP-001 mutation and validation
  -> closeout refresh for declared targets only
  -> stop

Dormant candidate:
explicit SWU-COOP-002 selection + fresh strict pack
  -> W2 one-file HTML content/IA prototype
  -> closeout refresh
  -> stop; no automatic L1 work
```

| Wave | Layer question | Task/SWU | Entry | Exit evidence | Parallelism |
| --- | --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0.md) | Are exact inputs and boundaries reproducible? | closure-only baseline | Plan pass | validated strict packs and absence baseline | none |
| [W1](work-pack/waves/W1.md) | Can one record fail closed under current policy? | TASK-COOP-L0-CONTRACT / `SWU-COOP-001` | W0 pass | source receipt plus contract-test evidence | none |
| [W2](work-pack/waves/W2.md) | Can the complete portfolio and meeting route cohere in one static browser document? | TASK-COOP-L0-HTML-PROTOTYPE / `SWU-COOP-002` | W1 terminal pass and closeout; later explicit selection and fresh strict pack | browser structure/responsive/network/screenshot source receipt | none |

## Gate Rules

- W1 cannot begin from broad repository exploration; use strict packs first.
- Only `SWU-COOP-001` is mutation-capable.
- `SWU-COOP-002` is planned but remains dormant until a later explicit
  selection and new strict pack.
- Scope expansion, missing Node behavior, contradictory source truth, or a test
  that cannot distinguish a seeded failure stops the run.
- Successful source validation routes to closeout synchronization, not L1.
- Successful `SWU-COOP-001` closeout does not automatically open W2.
- No deployment or public state change exists in this execution pack.
