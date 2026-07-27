# Shared Execution Context

## Authoritative Planning Chain

`SPEC.md -> ARCHITECTURE.md -> DESIGN-DISTILL.md -> IMPLEMENTATION-LAYERING.md -> WORK-PACK.md`

Use `WORK-PACK.md` for current plan state and `SWU-MANIFEST.json` for machine
identity/dependency lookup. Task files own implementation detail.

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
- `backend/e2e/governed-state-projection.spec.ts`
- `backend/e2e/action-annotation-mobile.spec.ts`
- `backend/e2e/helpers.ts`

## Evidence Boundary

UPW-FIX-001–024 are planned contracts. A Task Session receipt may prove only
the selected SWU and checks it actually ran. It cannot promote human,
cross-browser, certification, release, or production claims.
