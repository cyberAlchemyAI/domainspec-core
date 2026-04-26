# domainspec-core Copilot Scope

This repository is the research orchestration root for the 3-repo DomainSpec topology.

## Primary scope

- Research design and execution planning
- Experiment traceability and analysis
- Cross-repository governance and drift control

## Out of scope

- Direct ownership of reusable Type A implementation pack assets
- Product feature implementation in poker-team

## Ownership model

- Type A canonical DomainSpec pack: `implementation/domainspec/copilot`
- Type A canonical MARS reusable assets: `implementation/mars`
- Type B research orchestration assets: `domainspec-core/.github`
- Type C project-local overlays: consumer repositories (for example `validation/poker-team/.github`)

## Operational checks

Run this before research phase transitions and release checkpoints:

```bash
./tools/check_github_drift.sh
```

Treat failures as blockers until classified and resolved in `ops/AGENT-SKILL-TRIAGE-MATRIX.md`.
