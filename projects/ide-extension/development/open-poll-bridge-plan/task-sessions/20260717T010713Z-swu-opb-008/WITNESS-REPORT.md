---
module: ide-extension-open-poll-bridge
swuId: SWU-OPB-008
status: pass
createdAt: 2026-07-17T01:07:13Z
---

# Open Poll Browser Witness Report

## Claim Under Test

The browser workbench presents one request as open availability, a session claims
it as `openrouter.local-session`, and the visible terminal receipt remains bound
to that claimant.

## Evidence

- PASS: `npm --prefix projects/ide-extension run test:workbench`
  - 6 Node UI tests passed.
- PASS: `npm exec -- playwright test tests/e2e/manual-session-bridge.spec.mjs`
  from `projects/ide-extension`
  - desktop Chromium passed.
  - mobile Chromium passed.
- PASS: scoped `git diff --check`.

## Witness Assertions

- Ready polling uses `/api/bridge/requests/ready` without `agent_ref`.
- Browser status says `Available to poll`.
- The first and second Playwright claims use `openrouter.local-session`.
- Bridge detail displays `Claimant`.
- The terminal execution receipt carries `openrouter.local-session`.

## Result

PASS. The workbench path visibly supports open singleton availability and
claim-bound non-Codex identity.
