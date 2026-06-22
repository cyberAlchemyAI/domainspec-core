# Distill Repair

## Repairs Applied

1. Closed the transport ambiguity by selecting
   `hybrid-cookie-for-browser-bearer-for-service-api`.
2. Closed the Strava scope ambiguity by selecting
   `link-identity-and-import-recent-activity-summaries`.
3. Added official Strava documentation check for scope currentness.
4. Kept implementation out of the refine run.
5. Preserved private source boundaries.
6. Separated Body War first-consumer work from reusable foundation work.

## Repaired Acceptance Surface

- Core auth tests come from poker-team's P0 auth obligations.
- Browser guard tests come from Savvy's forged auth, CSRF, permission, and
  resource-scope tests.
- Provider tests come from Body War's Strava work-pack plus official scope
  currentness.

## Residue

- Implementation task-session must choose actual persistence technology.
- Implementation task-session must define environment variables, migrations,
  and deployment secret policy.
- Body War still has active real-activity evidence blocker until one consenting
  activity imports and submits without token leakage.

## Verdict

Pass. The plan is actionable without dragging track/game work into the first
slice.
