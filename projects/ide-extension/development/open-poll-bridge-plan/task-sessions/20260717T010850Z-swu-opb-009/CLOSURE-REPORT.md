---
module: ide-extension-open-poll-bridge
swuId: SWU-OPB-009
status: pass
createdAt: 2026-07-17T01:08:50Z
---

# Open Poll Bridge Closure Report

## Readiness Claim

PASS. The L0 bridge now supports open singleton availability with
claim-bound non-Codex identity.

## Evidence Matrix

| Claim | Evidence |
| --- | --- |
| Ready is open availability, not a selector. | `SWU-OPB-003`; ready endpoint accepts no query and ignores `agent_ref`; bridge suite passed. |
| Claim binds non-Codex identity. | `SWU-OPB-004`; claim/result tests use `openrouter.local-session`; bridge suite passed. |
| Result receipt preserves stored claim identity. | `SWU-OPB-002`, `SWU-OPB-004`, `SWU-OPB-007`; projector and witness assert receipt/claim identity. |
| Race loser secrecy is preserved. | `SWU-OPB-004`, `SWU-OPB-007`; ten-claim race has one winner and no payload leaks. |
| Workbench teaches availability/claimed model. | `SWU-OPB-006`, `SWU-OPB-008`; UI and Playwright tests passed. |
| Browser witness proves desktop/mobile path. | `SWU-OPB-008`; focused Playwright spec passed for desktop and mobile Chromium. |

## Final Validation

- PASS: `npm --prefix projects/ide-extension run validate:schemas`
  - 21 runtime schemas, 6 module manifests, 81 schema fixtures.
- PASS: `npm --prefix projects/ide-extension run test:bridge`
  - 68 tests passed.
- PASS: `npm --prefix projects/ide-extension run test:workbench`
  - 6 tests passed.
- PASS: `npm exec -- playwright test tests/e2e/manual-session-bridge.spec.mjs`
  from `projects/ide-extension`
  - 2 Chromium projects passed.
- PASS: `git diff --check -- projects/ide-extension .arcanum/observability`.

## Residue

- L1/L3 deferred: queue, leases, background workers, authenticated session
  registry, provider routing, mutation executors, and IDE/browser control.
- Local debug `/api/state` still exposes richer state than the poll contract;
  the public poll surface remained narrower in witness tests.

## Next Route

Use the bridge in the workbench, or open a new governed plan for automatic
polling/lease behavior.
