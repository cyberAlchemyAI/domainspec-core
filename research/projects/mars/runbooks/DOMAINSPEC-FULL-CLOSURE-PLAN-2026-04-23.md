# DomainSpec Full-Closure Orchestration Plan (2026-04-23)

Locked methodology choices:
- 1C completion scope (full closure C1-C4)
- 2A orchestration mode (gsd-phase / wave-based)
- 3B immediate sequencing (E11 D4 + E7 in parallel)
- 4A strict evidence updates (no provisional claim upgrades)
- 5A broad-source depth

## Wave Plan (Dependency-Ordered)

| Wave | Task ID | Task | claim_id | experiment_id | gate_id | Depends On |
| --- | --- | --- | --- | --- | --- | --- |
| W0 | FC-T1 | Publish full-closure orchestration map | MARS-C1..MARS-C4 | cross-experiment | G1 | none |
| W1A | FC-T2 | Start E11 D4 manual package and adjudication track | MARS-C2 (primary), MARS-C1 (secondary) | E11 | D4, G4 | FC-T1 |
| W1B | FC-T3 | Start E7 longitudinal instrumentation baseline | MARS-C3, MARS-C4 | E7 | G1 | FC-T1 |
| W2 | FC-T4 | Execute E4 governance attenuation baseline | MARS-C3 | E4 | G1-G4 | FC-T3 |
| W3 | FC-T5 | Execute E5 observer/executor intervention study | MARS-C3 | E5 | G1-G4 | FC-T4 |
| W4 | FC-T6 | Execute E8 meta-health convergence using E7 accumulation | MARS-C4 | E8 | G1-G4 | FC-T3 |
| W5 | FC-T7 | Execute E1 determinism then E2/E3 hardening sequence | MARS-C2 | E1, E2, E3 | G1-G4 | FC-T2 |
| W6 | FC-T8 | Run E10 external productivity study | MARS-C1, MARS-C2 | E10 | G1-G4 | FC-T4, FC-T7 |
| W7 | FC-T9 | Final strict evidence adjudication and status updates | MARS-C1..MARS-C4 | E1-E11 | D4 + G1-G4 | FC-T2..FC-T8 |

## Strict Evidence Rule

No status changes are allowed in `research/projects/mars/results/MARS-EVIDENCE-STATUS.md` until experiment-level rerun, adjudication, and gate packet checks are complete for the relevant claim update.

## Verification Commands

Repository-level:

```bash
./tools/check_research_structure.sh
./tools/check_github_drift.sh
```

Experiment-level:
- Run gate command blocks in each experiment `protocol.md`.
- Keep a decision packet per experiment under `experiments/<exp>/results/`.
