# Execution Pack: Craft Consultation API

## Planning control fields

| Field | Value |
| --- | --- |
| planningGateStatus | block |
| complexity | medium |
| baselineWave | W0 |
| activePlanRef | `WORK-PACK.md` |
| workPackManifest | `WORK-PACK.md` |
| layeringArtifact | `IMPLEMENTATION-LAYERING.md` |
| specRef | `API-CONTRACT.md`, `DATA-MODEL.md`, `SECURITY-BOUNDARY.md` |
| activeLayerWindow | L0 |
| lastPlannedAt | 2026-08-05T20:58:03Z |
| readinessProfile | pilot |

## Waves

| Wave | Goal | Included units | Entry | Exit |
| --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0.md) | Resolve owners and capture immutable baselines | decision/baseline only | new authorization | approved root/ports and exact digests |
| [W1](work-pack/waves/W1.md) | Build 0.15.9 snapshot, then test fresh-process reopen | SWU-CAPI-000 -> SWU-CAPI-001 | W0 | two passing/failing immutable experiment receipts |
| [W2](work-pack/waves/W2.md) | Pin the accepted runtime and build pure L0 foundations | 002 -> 003; 004 -> 005, with disjoint branches | W1, root approval, exact 0.15.9 dependency gate | dependency/verifier/invalidation/schema/security suites pass |
| [W3](work-pack/waves/W3.md) | Expose authorized L0 | 006 -> 007 | W2 | complete L0 HTTP suite and no-writer proof |
| [W4](work-pack/waves/W4.md) | Add conditional 0.3.0 rows | 008 -> 009 | W3 | adapter and row route suites pass |
| [W5](work-pack/waves/W5.md) | Verify closure | TASK-VERIFY | all admitted waves | evidence ceiling and residue audited |

No wave is admitted while `WORK-PACK.md` has an empty allowed-route projection.
Each mutation SWU runs in a separate Task Session, joins its owner refresh, and
stops on acceptance-critical failure. Parallel work is permitted only for the
disjoint runtime and contract branches in W2; shared-path SWUs stay sequential.

## Closure obligations

- Source ledgers, prior WaveDB store, and experiment inputs remain byte-unchanged.
- The API dependency surface may bind 0.15.9 only after both W1 receipts pass;
  the pin must match the verified tarball SRI/SHA-256 and native-addon identity.
- Every completed SWU has its exact baseline, terminal receipt, validation, and
  Invoke Refresh receipt.
- Closure does not imply deployment, production, publication, promotion,
  replacement, recovery, or source authority.
