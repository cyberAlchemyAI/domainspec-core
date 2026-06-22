# TASK-AUTH-PRODUCTION-READINESS

## Objective

Harden the TypeScript auth foundation toward production readiness after local package behavior and Body War consumer proof pass.

## Source Contracts

- Savvy auth decision: external IdP + secure app session + app-owned authorization.
- Poker-team auth telemetry and deny-by-default patterns.
- Auth package L0-L2 receipts.

## Smallest Working Units

### SWU-AUTH-008 - Production Readiness Boundary

- Dependencies: `SWU-BW-001`, `SWU-INV-001`.
- Write scope: `projects/auth-user-management/docs/`, package env examples, readiness report artifacts.
- Done criteria: durable store decision, provider-token encryption decision, secret/env contract, runbook, rollback, manual Strava smoke plan, denial matrix status.
- Acceptance evidence: production readiness report reviewed; secret-gated smoke plan documented.
- Execution owner: manual.
- Handoff note: do not require real Strava credentials in normal CI.

## Synchronization

Production readiness can be `flag` with named gaps, but not `pass` while durable storage and token custody remain undefined.
