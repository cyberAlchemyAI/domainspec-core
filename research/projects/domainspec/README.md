# DomainSpec Research Project

DomainSpec is the core evidence program that validates whether typed domain modeling plus deterministic derivation and governance signals can produce reproducible software engineering outcomes.

This project is self-contained under `research/projects/domainspec` and follows canonical-only paths.

## What This Project Is About

DomainSpec answers the central framework claims C1-C4 through controlled experiments (E1-E10), append-only run data, and claim-level traceability into the paper.

The program focuses on:

- deterministic derivation and test obligations
- governance attenuation and intervention effectiveness
- vocabulary sufficiency across multiple domains
- signal-driven meta-governance convergence

## Current Snapshot (2026-04-21)

- Status: active, evidence-building
- Version: 0.1.0
- Owner: domainspec-research-scientist
- Latest run state: E6 and E9 completed and analyzed; remaining experiments pending

## Completeness Dashboard

### Weighted Completeness

- Structural completeness (40% weight): 100%
- Empirical completeness (40% weight): 45%
- Publication completeness (20% weight): 40%
- Overall weighted completeness: 66%

Scoring note:
- Structural = required project contract and canonical governance artifacts present.
- Empirical = sources, inventory, data capture, integrity checks, analysis outputs, evidence updates.
- Publication = paper-facing synthesis and retrospective artifacts.

### Artifact Lane Status

| Lane | Expected Outcome | Current State | Status |
|---|---|---|---|
| Project contract | PROJECT, claims, dependencies, registry, telemetry schema | Present | complete |
| Governance definitions | experiment index and protocol specs (E1-E10) | Present | complete |
| Execution evidence | experiment specs, live data files, analysis outputs | E6 and E9 have data/results; most experiments still pending | in progress |
| Source and inventory | source selection and inventory coverage for active experiments | Source catalog and inventory entries exist, but not complete for all scheduled runs | in progress |
| Claim adjudication | claim-level status updates from experiment evidence | C2 partially supported; C1/C3/C4 still insufficient | in progress |
| Publication | paper updates and retrospective outputs | Paper exists but evidence integration remains partial | in progress |
| Exports | reusable published claim/method artifacts | Claims and methods exports published | complete |

## Experiment Progress

- Total indexed experiments: 10
- Completed with analysis: 2 (E6, E9)
- Not started: 8 (E1, E2, E3, E4, E5, E7, E8, E10)

High-signal completed work:
- E6: vocabulary sufficiency across 18 domains with high coverage
- E9: cross-feature composition stress test with explicit ontology extension proposals

## What Is Missing Right Now

1. Execute E1, E2, and E3 to directly strengthen deterministic derivation evidence for C2.
2. Execute E4, E5, E7, and E8 to establish strong evidence for C1, C3, and C4.
3. Run E10 to establish productivity evidence currently listed as missing in threats/future work.
4. Standardize per-experiment source and inventory artifacts for every pending run, not only E6/E9.
5. Integrate completed evidence deltas into the paper narrative and claim-strength framing.

## Claim Coverage Summary

Current claim snapshot (`claims/CLAIMS.md`):

- C2: partially supported (backed by E6 and E9)
- C1: insufficient evidence
- C3: insufficient evidence
- C4: insufficient evidence

Interpretation:
- DomainSpec has a solid structural and analytical base.
- Empirical closure still depends on finishing the remaining high-priority experiments.

## Canonical File Map

- Project manifest: `PROJECT.yaml`
- Experiment index: `experiments/EXPERIMENTS.md`
- Claims: `claims/CLAIMS.md`
- Dependencies: `deps/DEPENDENCIES.yaml`
- Artifact index: `registry/ARTIFACT-INDEX.md`
- Traceability matrix: `registry/TRACEABILITY-MATRIX.md`
- Paper: `papers/domainspec-paper.md`
- Evidence outputs: `results/*.md` and `data/*.jsonl`

## Dependency Policy

All upstream dependencies must be declared in `deps/DEPENDENCIES.yaml`.
Cross-project consumption is allowed only through declared dependency contracts and published exports.
