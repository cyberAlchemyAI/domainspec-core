# Phase 01-01 Drift Matrix

| Drift ID | Requirement | Source of Truth | Target Doc/Asset | Gap Description | Planned Plan ID |
|---|---|---|---|---|---|
| DR-001 | DOC-01 | implementation/domainspec/copilot/skills | implementation/domainspec/README.md | Skills table omits shipped advanced skills (`domainspec-reflect`, `domainspec-signal-observer`, `domainspec-ui-phase-bridge`, `domainspec-ui-audit-bridge`). | 01-02 |
| DR-002 | DOC-01 | implementation/domainspec/templates | implementation/domainspec/README.md | Templates table omits shipped templates (`agent-runner.md`, `PIPELINE-REPORT.md`, `SIGNAL-SCHEMA.md`, `OBSERVABILITY-REPORT.md`, `use-case.md`, `setup.sh`). | 01-02 |
| DR-003 | DOC-01 | implementation/domainspec/CHANGELOG.md | implementation/domainspec/README.md | Reference table shows stale current version (`v1.8.1`) instead of changelog head (`1.8.2`). | 01-02 |
| DR-004 | DOC-02 | implementation/domainspec/README.md | implementation/README.md | Mirror must remain synchronized after canonical README corrections. | 01-02 |
| DR-005 | DOC-03 | implementation/domainspec/copilot/skills | implementation/domainspec/copilot/README.md | Command list does not include full shipped command set (infra, OTel, layering, pilot-readiness, reflect, signal-observer, UI bridge variants). | 01-03 |
| DR-006 | DOC-03 | implementation/domainspec/copilot/agents | implementation/domainspec/copilot/README.md | Agent list omits shipped copilot agents (`domainspec-infra-architect`, `domainspec-otel-instrumenter`, `domainspec-otel-verifier`, `domainspec-ui-architect`). | 01-03 |
| DR-007 | DOC-04 | implementation/domainspec/copilot/install.sh | implementation/domainspec/copilot/INSTALL.md | INSTALL guidance requires explicit public/internal command taxonomy and post-install validation aligned with installer behavior. | 01-03 |
| DR-008 | PKG-01 | implementation/domainspec/.github/skills/domainspec-plan-phase-bridge, implementation/domainspec/.github/skills/domainspec-execute-phase-bridge | implementation/domainspec/copilot/skills | Bridge skills referenced by shipped agents are absent from distributable copilot skill pack. | 01-04 |
| DR-009 | GOV-01 | Requirement for deterministic drift prevention | implementation/domainspec/tools | No deterministic docs-versus-assets sync check script exists to prevent regression. | 01-04 |

## Requirement Coverage Map

| Requirement | Drift IDs | Planned Plan IDs |
|---|---|---|
| DOC-01 | DR-001, DR-002, DR-003 | 01-02 |
| DOC-02 | DR-004 | 01-02 |
| DOC-03 | DR-005, DR-006 | 01-03 |
| DOC-04 | DR-007 | 01-03 |
| PKG-01 | DR-008 | 01-04 |
| GOV-01 | DR-009 | 01-04 |
