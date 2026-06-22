# Activity Import Receipt

Status: `template`
Scope: TROQAR / Body War L0 Strava activity summaries

This receipt shape records that activity summaries were imported through the
server-owned Strava connection without exposing provider tokens, raw private
payloads, maps, notes, or route-geometry claims.

## Public-Safe Receipt Shape

```json
{
  "source": "strava",
  "principal_id": "strava:<redacted-or-owned-id>",
  "imported_at": "2026-06-21T00:00:00.000Z",
  "summary_count": 0,
  "redaction": {
    "provider_tokens": "server_only",
    "raw_private_payload": "omitted",
    "maps": "omitted",
    "notes": "omitted"
  },
  "consent": {
    "friend_fixture": "required_before_real_friend_activity"
  },
  "authority": {
    "activity_summary": "imported",
    "route_geometry": "not_claimed",
    "scoring": "not_claimed"
  }
}
```

## Allowed Activity Summary Fields

- `id`
- `name`
- `distance`
- `moving_time`
- `elapsed_time`
- `total_elevation_gain`
- `type`
- `sport_type`
- `start_date`
- `average_speed`

## Forbidden Tracked Fields

- Strava access tokens.
- Strava refresh tokens.
- OAuth authorization codes.
- Raw provider payloads.
- Private activity notes.
- Map/polyline data.
- Friend activity data without consent.

## Closure Rule

A receipt can support "activity import works" only. It cannot close route
geometry, scoring, leaderboard, challenge, or public verification claims.
