# TASK-W1-TYPESCRIPT-SCAFFOLD

## Objective

Replace `projects/body-war/app/` with a Body War-owned TypeScript MVP scaffold
after W0 contracts pass.

## Layer And Slice

- Layer: L1.
- Slice: S-001.
- Wave: W1.

## Source Contracts

- `../../SPEC.md`
- `../../DEPLOYMENT-SECURITY.md`
- `../../ARCHITECTURE-AUDIT.md`

## Dependencies

- All W0 SWUs pass.
- Work-pack mutation gate is reopened.

## Smallest Working Units

| SWU | Goal | Write Scope | Done Criteria | Validation |
| --- | --- | --- | --- | --- |
| SWU-BWPT-007 | Scaffold TypeScript app boundary. | `projects/body-war/app/` | TS app has package scripts, strict config, DomainSpec refs, and basic route shell. | Typecheck/start command selected in W0 and passes. |

## Implementation Detail

- Preserve only needed prototype evidence through docs or reference notes; do not
  silently carry local JSON token storage forward.
- Keep domain/application/interface/infrastructure/UI boundaries explicit.
- Add path/source references to DomainSpec architecture methods per
  `ARCHITECTURE-AUDIT.md`.

## Blockers

Blocked until W0 passes.

