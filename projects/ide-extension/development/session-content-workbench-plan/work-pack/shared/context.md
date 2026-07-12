# Shared Context

## Objective

Build a trusted-local interactive HTML workbench over the completed manual
session bridge. The value loop is publish, display, interact, poll, continue.

## Approved Sources

- `../../session-content-canvas-design/DECISIONS.md`
- `../../session-content-canvas-design/ARCHITECTURE-BUNDLE.md`
- `../../session-content-canvas-design/UX-PLAN.md`
- `../../session-content-workbench-refresh/REFRESH-REPORT.md`
- `../../../SPEC.md`
- `../../../ARCHITECTURE.md`

## Runtime Anchors

- `src/server.mjs`
- `src/kernel/projector.mjs`
- `src/kernel/storage.mjs`
- `src/kernel/schema-validation.mjs`
- `scripts/session-bridge.mjs`
- `public/demo/l0.html`
- current Node and Playwright bridge tests

## Boundary

V0 trusts the local operator, session, and HTML. Correctness, repeatability, and
user value matter; production security claims do not.
