# Context Pack: SWU-MSB-010

- Task/SWU: `TASK-VALIDATION-WITNESS / SWU-MSB-010`
- Dependency: SWU-MSB-009 automated safety gate complete
- Sources: Playwright skill, current Playwright config/server harness, legacy
  Approval Desk spec, approved bridge browser flow and UI state model
- Runtime: local Chromium through `@playwright/test`; fresh temporary server state

## Boundaries And Decisions

- Run the same complete bridge flow at 1440x900 and 390x844.
- Use browser controls for human-owned actions and request APIs only for the fake
  session claimant/result owner.
- Verify pre-claim secrecy, singleton conflict visibility, recovery, both receipt
  kinds, result evidence, live announcements, responsive geometry, and errors.
- Retain reviewed desktop/mobile screenshots under the work-pack evidence path.
- No production or manual witness state is consumed.

## Gate

- `npm run test:bridge` passed twice, 66/66 each.
- Chromium and Playwright dependencies are installed; `npx` is available.
- Decisions/blockers: none.
- Gate verdict: PASS.
