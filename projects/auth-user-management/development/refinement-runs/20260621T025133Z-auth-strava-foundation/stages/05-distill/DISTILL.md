# Distill - Smallest Coherent Unit

## Selected Unit

Reusable Auth Core + Browser Session Adapter + Strava Provider Link.

This unit is coherent because Body War cannot safely connect to Strava without
server-owned identity, session continuity, provider account ownership, token
custody, and redacted audit. It is still small enough to avoid track geometry,
scoring, disputes, anti-cheat, and broader game mechanics.

## Chosen Decisions

- `DEC-AUTH-TRANSPORT-001`: choose
  `hybrid-cookie-for-browser-bearer-for-service-api`.
- `DEC-AUTH-STRAVA-SCOPE-001`: choose
  `link-identity-and-import-recent-activity-summaries`.

## Rejected Units

| Rejected unit | Reason |
|---|---|
| Body War direct Strava implementation | Creates one-off auth and makes reuse harder. |
| Full game MVP | Pulls in track geometry, scoring, and disputes before auth is safe. |
| Bearer-only foundation | Poker-team proves bearer, but Body War/Savvy browser flows need cookie/CSRF safety. |
| Cookie-only foundation | Useful for browser flows but weaker for future service/API consumers and token introspection. |
| Strava identity-only link | Too small for Body War; it does not prove activity import. |
| Refreshable all-activity access by default | Too broad for first consent surface; `activity:read_all` should be opt-in escalation. |

## Residue

Implementation still needs a task-session route. This refine run selects the
unit and plan; it does not implement runtime code.
