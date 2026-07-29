# Shared Execution Context

## Authoritative Planning Chain

`SPEC.md -> ARCHITECTURE.md -> DESIGN-DISTILL.md -> IMPLEMENTATION-LAYERING.md -> WORK-PACK.md`

Use `WORK-PACK.md` for current plan state, `SWU-MANIFEST.json` for machine
identity/dependency lookup, `SWU-SCOPE-INVENTORY.json` for exact mutation
authority, `SWU-ACCEPTANCE-MATRIX.json` for assertion ownership, and
`CLOSEOUT-SYNC-INVENTORY.json` for receipt synchronization. Task files own
implementation detail.

## Runtime Anchors

- `backend/src/cli/studio.ts`
  - `renderPage`
  - `renderedSignature`
  - `pollScript`
  - `actScript`
  - `/state`
- `backend/src/modules/ui-prototyping-studio/application/governed-state-projection.ts`
  - `GovernedStateProjection`
  - `buildGovernedStateProjection`
- `backend/src/modules/ui-prototyping-studio/application/governed-state-projection.test.ts`
- `backend/src/modules/ui-prototyping-studio/application/ports.ts`
- `backend/src/modules/ui-prototyping-studio/application/session-store.ts`
- `backend/src/modules/ui-prototyping-studio/infrastructure/file-studio-session-store.ts`
- `backend/e2e/governed-state-projection.spec.ts`
- `backend/e2e/action-annotation-mobile.spec.ts`
- `backend/e2e/helpers.ts`

## Evidence Boundary

UPW-FIX-001–024 and `SWU-ACCEPTANCE-MATRIX.json` are planned contracts. A Task
Session receipt may prove only the selected SWU and checks it actually ran. It
cannot promote human,
cross-browser, certification, release, or production claims.
