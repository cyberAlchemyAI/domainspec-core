# Meta-Meta Research Project

Meta-Meta is the generalization program that tests whether DomainSpec-style governance, signal extraction, and multi-agent coordination patterns transfer across domains beyond the original software context.

This project is self-contained under `research/projects/meta-meta` and follows canonical-only paths.

## What This Project Is About

Meta-Meta answers claims CM1-CM4 through experiments E11-E20, focusing on:

- generalized governance signal extraction
- outer-loop intervention effectiveness
- agent specialization driven by performance signals
- multi-agent conversation and cross-domain knowledge transfer

## Current Snapshot (2026-04-21)

- Status: planning
- Version: 0.1.0
- Owner: domainspec-research-scientist
- Latest run state: experiment index defined, no live runs executed yet

## Completeness Dashboard

### Weighted Completeness

- Structural completeness (40% weight): 100%
- Empirical completeness (40% weight): 0%
- Publication completeness (20% weight): 0%
- Overall weighted completeness: 40%

Scoring note:
- Structural = required project contract and canonical governance artifacts present.
- Empirical = sources, inventory, data capture, integrity checks, analysis outputs, evidence updates.
- Publication = paper-facing synthesis and retrospective artifacts.

### Artifact Lane Status

| Lane | Expected Outcome | Current State | Status |
|---|---|---|---|
| Project contract | PROJECT, claims, dependencies, registry, telemetry schema | Present | complete |
| Governance definitions | full experiment protocols and governance details for E11-E20 | Index exists, detailed experiment files not yet implemented | in progress |
| Execution evidence | experiment specs, live data files, analysis outputs | No live run artifacts yet | missing |
| Source and inventory | source selection and inventory coverage for each run | `sources/` and `inventory/` are empty | missing |
| Claim adjudication | claim-level evidence status updates | No evidence status artifact yet | missing |
| Publication | paper updates and retrospective outputs | `papers/` is empty | missing |
| Exports | reusable published artifacts for dependents | Export scaffold exists, no concrete exports yet | in progress |

## Experiment Progress

- Total indexed experiments: 10 (E11-E20)
- Completed with analysis: 0
- Not started: 10

Critical dependency note:
- E11/E17 depend on DomainSpec signal baseline exports declared in `deps/DEPENDENCIES.yaml`.

## What Is Missing Right Now

1. Create detailed protocol files for E11-E20 referenced by `experiments/EXPERIMENTS-META.md`.
2. Populate `sources/` with source discovery and selection artifacts per experiment wave.
3. Populate `inventory/` with structured inventory entries required by the selected protocols.
4. Execute first live run (recommended E11) and generate append-only JSONL under `data/`.
5. Produce first analysis/result artifact and initialize claim evidence status tracking.
6. Publish first concrete export artifact for downstream reuse.

## Claim Coverage Summary

Current state (`claims/CLAIMS.md`):

- CM1: no empirical support yet
- CM2: no empirical support yet
- CM3: no empirical support yet
- CM4: no empirical support yet

Interpretation:
- Meta-Meta has clear claim framing and dependency contracts.
- It is still pre-empirical and needs initial execution evidence.

## Canonical File Map

- Project manifest: `PROJECT.yaml`
- Experiment index: `experiments/EXPERIMENTS-META.md`
- Claims: `claims/CLAIMS.md`
- Dependencies: `deps/DEPENDENCIES.yaml`
- Artifact index: `registry/ARTIFACT-INDEX.md`
- Traceability matrix: `registry/TRACEABILITY-MATRIX.md`
- Telemetry schema: `telemetry/SIGNAL-SCHEMA.md`
- Published exports index: `exports/README.md`

## Dependency Policy

All upstream dependencies must be declared in `deps/DEPENDENCIES.yaml`.
Cross-project consumption is allowed only through declared dependency contracts and published exports.
