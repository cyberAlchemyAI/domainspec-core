# SWU-GSP-005 Validation

- Material package: `pass`
- Mutation admission: `admit`
- Exact applied material parity: `4/4`
- TypeScript no-emit check: `pass`
- Full unit/slice suite: `71/71 pass`
- First focused browser run: `5/6`; the mobile witness incorrectly required
  the action recap to start above the fold after proving the preview cards had
  stacked.
- Rework: scroll the recap into view before asserting inspectability; no
  product source changed.
- Final focused browser run: `6/6 pass`
- Full Playwright regression: `21/21 pass`

Accept and Revert buttons remain disabled until an actor-neutral checkbox is
set. Their POST routes independently require a live action, candidate/revision
identity, target state, and `acknowledged=true`; absent context returns 428 and
stale context returns 409. Export has no browser action. Annotation is
unavailable without resolved content and its form remains disabled until a
real `data-od-id` target is selected. At 390px, before/after cards stack with
no horizontal document overflow.
