# MARS Research Project

MARS is the research-orchestration project that defines and validates a gated, reproducible lifecycle for experiment design, execution, evidence adjudication, and paper integration.

This project is self-contained under `research/projects/mars` and follows canonical-only paths (no compatibility aliases).

## What This Project Is About

MARS exists to answer one core question:

Can we run research programs with deterministic governance gates, explicit dependency contracts, and traceable evidence updates so claim quality improves over time?

The project operationalizes this through:

- 12-stage pipeline orchestration (`definitions/MARS-PIPELINE.md`)
- hard governance gates G1-G4
- claim-level evidence tracking (`results/MARS-EVIDENCE-STATUS.md`)
- explicit dependency contracts (`deps/DEPENDENCIES.yaml`)

## Interview Capacities

MARS now includes interview-first research scoping for both greenfield and brownfield contexts.

Primary command:

```
@mars-research-interviewer mars-research-interview [greenfield|brownfield|auto] [topic-or-project]
```

What this adds:

- Research-scope discovery before protocol design
- Brownfield evidence inspection (claims, protocols, results, data) before questioning
- Counterargument-first framing for hypotheses and propositions
- Experiment candidate generation with disconfirming outcomes and gate-readiness cues

Default output artifact set:

- `PROJECT-OVERVIEW.md`
- `definitions/INITIAL-DEFINITIONS.md`
- `claims/HYPOTHESES.md`
- `experiments/EXPERIMENT-CANDIDATES.md`

Template sources:

- `templates/project-overview-template.md`
- `templates/initial-definitions-template.md`
- `templates/hypotheses-template.md`
- `templates/experiment-candidates-template.md`

Asset paths:

- Agent: `.github/agents/mars-research-interviewer.agent.md`
- Skill: `.github/skills/mars-research-interview/SKILL.md`

## Current Snapshot (2026-04-21)

- Status: active, bootstrap stage
- Version: 0.1.0
- Owner: mars-research-scientist
- Latest run state: tabletop dry run completed, live execution not yet completed

## Completeness Dashboard

### Weighted Completeness

- Structural completeness (40% weight): 100%
- Empirical completeness (40% weight): 20%
- Publication completeness (20% weight): 0%
- Overall weighted completeness: 48%

Scoring note:
- Structural = required project contract and canonical governance artifacts present.
- Empirical = live sourcing, inventory, data capture, integrity audit, and evidence updates.
- Publication = paper-facing synthesis and retrospective artifacts.

### Artifact Lane Status

| Lane | Expected Outcome | Current State | Status |
|---|---|---|---|
| Project contract | PROJECT, claims, dependencies, registry, telemetry schema | Present | complete |
| Governance definitions | pipeline + gate policies + protocol checklist | Present | complete |
| Execution evidence | experiment specs, live data files, integrity/analysis outputs | Dry run exists; no live JSONL data yet | in progress |
| Source and inventory | source selection artifacts and inventory coverage | `sources/` and `inventory/` not populated | missing |
| Claim adjudication | claim evidence updates from completed analyses | Evidence file exists, mostly insufficient/partial support | in progress |
| Publication | paper updates and retrospective outputs | `papers/` empty | missing |
| Exports | reusable methods/claim exports for downstream consumers | Present | complete |

## Gate Readiness

From the latest dry run (`experiments/MARS-DRY-RUN-E1-foundation/protocol.md`):

| Gate | Current Decision | Meaning |
|---|---|---|
| G1 Protocol measurable | pass | Protocol quality baseline is acceptable |
| G2 Source quality | pass | Sources are identifiable and pinnable |
| G3 Inventory readiness | pending | Inventory artifacts are not complete |
| G4 Data integrity | pending | No live run data generated yet |

## What Is Missing Right Now

1. Populate `sources/` with source-selection and quality-gate artifacts for the next live run.
2. Populate `inventory/` with required inventory entries and readiness report.
3. Execute at least one live foundation run and write JSONL outputs under `experiments/<experiment-key>/data/`.
4. Produce integrity and analysis outputs tied to that live run.
5. Update claim evidence statuses from live-run analysis, not just inherited upstream evidence.
6. Create first paper-facing synthesis artifact under `papers/`.

## Claim Coverage Summary

Current evidence baseline (`results/MARS-EVIDENCE-STATUS.md`):

- MARS-C1: weak, insufficient evidence
- MARS-C2: moderate, partially supported
- MARS-C3: insufficient evidence
- MARS-C4: insufficient evidence

Interpretation:
- MARS currently has governance scaffolding and initial traceability.
- It still lacks enough empirical runs to support strong claim adjudication.

## Canonical File Map

- Project manifest: `PROJECT.yaml`
- Pipeline definition: `definitions/MARS-PIPELINE.md`
- Experiment bundle contract: `definitions/EXPERIMENT-BUNDLE-CONTRACT.md`
- Protocol checklist: `protocols/MARS-PROTOCOL-CHECKLIST.md`
- Claims: `claims/CLAIMS.md`
- Dependencies: `deps/DEPENDENCIES.yaml`
- Artifact index: `registry/ARTIFACT-INDEX.md`
- Traceability matrix: `registry/TRACEABILITY-MATRIX.md`
- Evidence status: `results/MARS-EVIDENCE-STATUS.md`

## Experiment Bundle Policy

Each experiment must keep protocol, source selection, run data, and results under its own bundle directory:

- `experiments/<experiment-key>/protocol.md`
- `experiments/<experiment-key>/sources.md`
- `experiments/<experiment-key>/data/*.jsonl`
- `experiments/<experiment-key>/results/*.md`

Governance contract:

- `definitions/EXPERIMENT-BUNDLE-CONTRACT.md`

Migration plan for current flat artifacts:

- `runbooks/EXPERIMENT-BUNDLE-MIGRATION-PLAN.md`

## Dependency Policy

All upstream dependencies must be declared in `deps/DEPENDENCIES.yaml`.
Cross-project consumption is allowed only through declared dependency contracts and published exports.
