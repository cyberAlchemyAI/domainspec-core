# Execution Pack: Arcanum Add-on

## Planning Control Fields

| Field | Value |
| --- | --- |
| planningGateStatus | block |
| complexity | high |
| baselineWave | W0 |
| activePlanRef | `work-pack/waves/W0.md` |
| workPackManifest | `WORK-PACK.md` |
| layeringArtifact | `IMPLEMENTATION-LAYERING.md` |
| specRef | `../define/SPEC.md` |
| activeLayerWindow | L0 |
| selectedSWU | none |
| lastPlannedAt | 2026-07-30T00:00:00-03:00 |
| readinessProfile | pilot |

## Wave Schedule

| Wave | Layer | Tasks | Start gate | Exit evidence |
| --- | --- | --- | --- | --- |
| W0 | L0 | TASK-0 | operator selects GOV-001 after plan/Distill/governance gates | accepted issue/owners plus compatibility receipt |
| W1 | L0 | TASK-1 | W0 receipts pass | valid no-authority catalog, redacted status, deterministic preview, and exact L0 continuation disposition |
| W2 | L1 | TASK-2 | W1 passes, current `L0-DECISION-001=continue`, and owners are bound | exact approval, replay, owner state, reload |
| W3 | L2 | TASK-3 | stable current public operations accepted | real adapters, clarification, result boundaries |
| W4 | L3 | TASK-4 | deterministic L0-L2 pass | degradation plus isolated uninstall/rollback branch receipts, security, and live browser evidence |
| W5 | L3 | TASK-5 | complete evidence bundle | independent readiness route; promotion/release remain separate |

## Execution Rules

- Execute one selected SWU per Task Session.
- Re-run Context Builder at Task Session preflight; do not reuse this planning
  package as an execution context dump.
- Complete the declared owner closeout sync before selecting a successor.
- Later waves cannot start on a partial prior-wave receipt unless the work-pack
  explicitly marks the dependency independent.
- Never parallelize overlapping host route/state writers.
- Strategy and Whisper adapters may be developed independently only after the
  shared adapter contract and accepted Bootstrap compatibility pass.
- Browser validation starts only after deterministic and security gates.
- Uninstall and rollback never run serially on one mutated candidate; they use
  isolated copies of one accepted disabled snapshot and join before security.

## Closure Tasks

- `SWU-ARC-SECURITY-001`, `SWU-ARC-BROWSER-001`, and
  `SWU-ARC-VERIFY-001` are verification/closure SWUs.
- They may not repair runtime code under a verification receipt. A discovered
  defect opens or reopens an owning implementation SWU.
- Readiness, promotion, and release are external owner decisions, not closure
  task side effects.
