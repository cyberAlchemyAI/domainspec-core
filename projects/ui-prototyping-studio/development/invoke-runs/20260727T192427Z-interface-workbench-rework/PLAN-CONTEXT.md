# Invoke Plan Context

## Objective

Convert the passing interface-workbench Design into a non-mutating,
medium-complexity split work-pack whose SWUs can be executed one at a time
without reopening product or architecture discovery.

## Approved Design References

- [Define specification](SPEC.md)
- [Architecture](ARCHITECTURE.md)
- [UX Plan](UX-PLAN.md)
- [Witness contracts](WITNESS-CONTRACTS.md)
- [Validation strategy](VALIDATION-STRATEGY.md)
- [Design Distill](DESIGN-DISTILL.md)
- [Design transport](DESIGN-TRANSPORT.md)
- [Selection result](DESIGN-SELECTION-RESULT.json)

Design evidence state is `design-validator-pass`. Plan evidence begins at
`plan-evidence-pending`; all UPW-FIX witnesses remain unexecuted.

## Delivery Boundary

Included:

- coherent projection snapshot and same-snapshot compatibility fields;
- deterministic whole/region versioning;
- stable no-build browser shell and inert polling;
- action-aware trailing refresh;
- recoverable keyed commit;
- identity-bound local context;
- the six target workbench regions;
- responsive, copy, bounded accessibility, security, and regression evidence.

Excluded:

- framework migration;
- streaming/push transport;
- a new durable draft or browser-state store;
- lifecycle/state vocabulary changes;
- reopening the completed governed-state-projection frontier;
- human study execution;
- cross-browser generalization;
- accessibility certification;
- release, deployment, or production claims.

## Constraints

- Preserve current application/store authority and action gates.
- Keep runtime no-build, loopback-only, and Node/TypeScript.
- Use safe DOM sinks and sandboxed/allowlisted frame routes.
- Run checked-in `tsc`, `tsx`, and Playwright binaries when Corepack/pnpm is
  unavailable.
- Serialize SWUs with overlapping `studio.ts` or workbench-shell write scopes.
- Invoke authors only; Task Session owns one selected SWU.

## Complexity

`medium`

The plan exceeds five tasks and requires a split work-pack, explicit waves,
task-local implementation detail, SWUs, execution choreography, and automatic
Plan Distill. It has no cross-repository or irreversible migration risk, so it
is not high complexity.

## Current Admission

- Design admission: pass
- Plan authoring: allowed
- Plan Distill: pending governed validation
- Work-pack execution gate: blocked pending Plan Distill and explicit SWU
  selection
- Selected SWU: `none`
