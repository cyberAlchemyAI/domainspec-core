# Private pilot staging

The active VPS staging is described in [VPS access](evidence/VPS-STAGING.md).
Archive migration is removed. Use a recent activity summary (or a labeled mock),
choose or create a suggested track, provide fresh consent, and submit evidence.

## Product construction

Validate the normal activity-to-evidence loop and runner-facing evidence lifecycle.
See REMOVAL-PLAN.md for removal acceptance and NEXT-STEPS.md for the next work.

## Operational support

Keep credentials private. Preserve the original archives and database schema
history as inactive records. The local staging launcher and VPS use separate
isolated databases. A live provider run is optional until a real activity exists.
The app owner performs Strava login and provides consent in the app.

## Open Questions

Public hosting and production readiness remain deferred in README.md. No archive
migration step is needed or supported.
