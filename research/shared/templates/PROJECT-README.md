# <PROJECT_NAME> Research Project

<One-paragraph summary of the project purpose and why it exists.>

## What This Project Is About

<Define the core research question this project answers.>

<Describe the main mechanisms used by the project (for example: claims, protocol, gates, evidence updates, analysis flow).>

## Current Snapshot (YYYY-MM-DD)

- Status: <planning|active|blocked|completed>
- Version: <semantic version>
- Owner: <owner agent or owner role>
- Latest run state: <for example: no live runs yet | dry run complete | N live runs complete>

## Completeness Dashboard

### Weighted Completeness

- Structural completeness (40% weight): <0-100>%
- Empirical completeness (40% weight): <0-100>%
- Publication completeness (20% weight): <0-100>%
- Overall weighted completeness: <0-100>%

Scoring note:
- Structural = required project contract and canonical governance artifacts present.
- Empirical = sources, inventory, data capture, integrity checks, analysis outputs, evidence updates.
- Publication = paper-facing synthesis and retrospective artifacts.

### Artifact Lane Status

| Lane | Expected Outcome | Current State | Status |
|---|---|---|---|
| Project contract | PROJECT, claims, dependencies, registry, telemetry schema | <state> | <complete|in progress|missing> |
| Governance definitions | pipeline/protocol definitions required by this project | <state> | <complete|in progress|missing> |
| Execution evidence | experiment specs, data files, analysis outputs | <state> | <complete|in progress|missing> |
| Source and inventory | source selection + inventory coverage | <state> | <complete|in progress|missing> |
| Claim adjudication | claim-level evidence status updates | <state> | <complete|in progress|missing> |
| Publication | paper updates and retrospective outputs | <state> | <complete|in progress|missing> |
| Exports | reusable published artifacts for dependents | <state> | <complete|in progress|missing> |

## What Is Missing Right Now

1. <highest-priority missing item>
2. <second missing item>
3. <third missing item>
4. <fourth missing item>

## Canonical File Map

- Project manifest: PROJECT.yaml
- Claims: claims/CLAIMS.md
- Dependencies: deps/DEPENDENCIES.yaml
- Artifact index: registry/ARTIFACT-INDEX.md
- Traceability matrix: registry/TRACEABILITY-MATRIX.md
- <project-specific canonical input>: <path>
- <project-specific evidence output>: <path>

## Dependency Policy

All upstream dependencies must be declared in deps/DEPENDENCIES.yaml.
Cross-project consumption is allowed only through declared dependency contracts and published exports.
