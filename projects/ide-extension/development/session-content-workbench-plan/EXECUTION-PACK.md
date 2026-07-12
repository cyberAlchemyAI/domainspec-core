# Execution Pack: Session Content Workbench

## Control

| Field | Value |
| --- | --- |
| planningGateStatus | pass |
| complexity | medium |
| baselineWave | W0 |
| activePlanRef | [WORK-PACK.md](WORK-PACK.md) |
| layeringArtifact | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) |
| readinessProfile | trusted-local-value-v0 |

## Wave Schedule

| Wave | Outcome | SWUs | Entry gate | Exit gate |
| --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0.md) | Contract and replay baseline. | 001-002 | refreshed design pass | schema/replay pass |
| [W1](work-pack/waves/W1.md) | Manual publish and display. | 003-004 | W0 pass | existing presentation usable |
| [W2](work-pack/waves/W2.md) | Automatic complete-revision updates. | 005 | W1 pass | reconnect/restart/degraded proof |
| [W3](work-pack/waves/W3.md) | Generic interaction and automated value surfaces. | 006-007 | W2 pass | Decision/Craft browser round trip |
| [W4](work-pack/waves/W4.md) | Real Codex value witnesses and closure. | 008-009 | W3 pass | retained evidence and review |

## Dependency Spine

```text
001 -> 002 -> 003 -> 004 -> 005 -> 006 -> 007 -> 008 -> 009
```

## Merge Rules

- Default execution is sequential because projector, server, CLI, and the
  single-file workbench overlap across layers.
- Every SWU consumes the previous Task Session result and reruns its focused
  regression surface.
- Status synchronization occurs only after evidence exists.
- No source mutation occurs from Invoke or from a later witness-only SWU.

## Stop Conditions

- Existing bridge history fails replay.
- Manual presentation display needs automatic transport to pass.
- A partial or hash-mismatched file is treated as a published revision.
- The browser or HTML page bypasses the kernel interaction endpoint.
- Value witnesses require security, remote access, or specialized skill APIs.
- A live witness is unavailable and someone proposes simulated success.
