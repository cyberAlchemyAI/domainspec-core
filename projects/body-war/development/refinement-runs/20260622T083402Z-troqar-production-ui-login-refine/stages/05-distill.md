# Stage 05 - Distill

Status: pass
Capability handle: `distill`
Mode: `standard`
Receipt kind: parent-native-stage-artifact

## Coherent Unit

Selected unit: `TROQAR production login-first shell`.

This is the smallest coherent production-ready unit because it contains the
anonymous first impression, login action, connected runner state, and browser
validation surface without requiring track gameplay, maps, real deploy, or new
auth providers.

## Rejected Larger Units

| Candidate | Rejected Because |
| --- | --- |
| Full TROQAR app shell with maps/routes/challenges/community | Pulls in deferred game and track surfaces. |
| Full auth/account management redesign | Shared auth package is outside this UI surface. |
| React/Vite frontend migration | Migration is not needed to prove first production UI unless static surface fails. |

## Rejected Smaller Units

| Candidate | Rejected Because |
| --- | --- |
| Only fix anonymous error copy | Too small; does not address production readiness. |
| Only style the existing panels | Leaves the anonymous first page structurally wrong. |
| Only add Playwright screenshots | Tests evidence, but no product/UI decision. |
