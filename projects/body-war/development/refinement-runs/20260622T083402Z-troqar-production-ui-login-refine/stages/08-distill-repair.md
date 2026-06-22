# Stage 08 - Distill Repair

Status: pass
Capability handle: `distill`
Mode: `repair`
Receipt kind: parent-native-stage-artifact

## Repair Applied

The first design draft was too implementation-shaped without enough acceptance
tests. Repair adds a production-readiness gate:

- anonymous state screenshot or layout assertion;
- connected state screenshot or layout assertion;
- no raw auth/backend terms in visible UI;
- no token-like strings in DOM;
- mobile fit at 390px;
- fake-Strava login remains one-click in local mode;
- submit preview has pending/success/failure behavior.

## Repaired Unit

`TROQAR production login-first shell with Studio handoff and Playwright
falsification`.

This unit is still narrow enough for one implementation Task Session but now has
clear failure tests.
