# Execution Pack: Minto Pyramid experiment L0

Status: proposal-only; no wave is admitted or running.

## Planning controls

| Field | Value |
|---|---|
| workPackManifest | `WORK-PACK.md` |
| layeringArtifact | `IMPLEMENTATION-LAYERING.md` |
| complexity | medium |
| planningGateStatus | pass-ready-for-exact-acceptance; execution blocked |
| baselineWave | W0 |
| activeLayerWindow | L0 |
| readinessProfile | pilot |

## Wave board

| Wave | Layer question | SWU | Entry gate | Exit evidence | Parallelism |
|---|---|---|---|---|---|
| [W0 — Case](work-pack/waves/W0-CASE.md) | Can the exact controlled case be authored without semantic or scope drift? | SWU-MPX-001 | exact plan acceptance and fresh selection | case artifact plus passing Task Session and Invoke closeout receipts | none |
| [W1 — Mechanics](work-pack/waves/W1-MECHANICS.md) | Do all declared structural mechanics close over the exact case? | SWU-MPX-002 | W0 joined closeout | mechanics receipt plus passing Task Session and Invoke closeout receipts | none |
| [W2 — Review](work-pack/waves/W2-REVIEW.md) | Does a precommitted role-label-blind human review support a bounded non-vacuity verdict while preserving the boundary case? | SWU-MPX-003 | W1 joined closeout and explicit human participation | exact commitment, packet, response, reveal/witness, Task Session receipt, and terminal Invoke closeout | none |

## Choreography

The frontier is strictly sequential. No wave may begin from task order alone: it consumes the exact joined closeout receipt and actual predecessor bytes. Task Session and Invoke write scopes are disjoint. W2 stops for a human semantic choice; automatic execution cannot fabricate or bypass it, and interruption after commitment restarts W2 with a fresh attempt.

## Completion boundary

Completion means all three unit and owner receipts join and the final witness artifact is structurally valid. It does not mean integration, reader efficacy, promotion, publication, deployment, or production readiness.
