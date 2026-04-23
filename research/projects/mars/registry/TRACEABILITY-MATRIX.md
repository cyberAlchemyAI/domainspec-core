# MARS Traceability Matrix

| Claim | MARS Experiments | Upstream Dependencies | Result Artifact |
|---|---|---|---|
| MARS-C1 | MARS-01, MARS-05 | domainspec C1 evidence | results/MARS-EVIDENCE-STATUS.md |
| MARS-C2 | MARS-01, MARS-02 | dep-mars-c2-baseline + domainspec E11 planned | results/MARS-EVIDENCE-STATUS.md |
| MARS-C3 | MARS-03, MARS-04 | domainspec C3 experiments | results/MARS-EVIDENCE-STATUS.md |
| MARS-C4 | MARS-06, MARS-07 | domainspec C4 experiments | results/MARS-EVIDENCE-STATUS.md |

## Active Full-Closure Queue (2026-04-23)

| Sequence | claim_id | experiment_id | gate_id | Status |
| --- | --- | --- | --- | --- |
| 1 | MARS-C2 (primary), MARS-C1 (secondary) | E11 | D4 + G4 | in progress (manual packet started; strict hold) |
| 2 | MARS-C3, MARS-C4 | E7 | G1 (longitudinal capture start) | in progress |
| 3 | MARS-C3 | E4 | G1-G4 | queued |
| 4 | MARS-C3 | E5 | G1-G4 | queued |
| 5 | MARS-C4 | E8 | G1-G4 | queued (depends on E7 accumulation) |
| 6 | MARS-C2 | E1, E2, E3 | G1-G4 | queued |
| 7 | MARS-C1, MARS-C2 | E10 | G1-G4 | queued |

Execution reference:
- `runbooks/DOMAINSPEC-FULL-CLOSURE-PLAN-2026-04-23.md`
