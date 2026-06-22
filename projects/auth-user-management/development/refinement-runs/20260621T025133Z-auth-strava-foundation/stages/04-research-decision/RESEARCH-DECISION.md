# Research Decision

## Mode

`research-if-gap-appears`

## Triggered Gap

The Strava provider lane raised a current-provider-scope gap. Local Body War
evidence names `read,activity:read`, but the route needed a current official
check before recommending a provider scope.

## External Sources Checked

- Official Strava Authentication docs:
  `https://developers.strava.com/docs/authentication/`
- Official Strava API reference:
  `https://developers.strava.com/docs/reference/`
- Official Strava API changelog:
  `https://developers.strava.com/docs/changelog/`

## Findings

- Strava tells applications to request only the scopes required for normal
  function.
- `activity:read` covers activities visible to Everyone and Followers,
  excluding privacy-zone data.
- `activity:read_all` adds access to Only You activities and privacy-zone data.
- The API reference uses `activity:read` for Everyone and Followers activities
  and `activity:read_all` for Only Me activity access.
- The 2026-04-23 changelog says authentication responses return a
  space-delimited `scope` field.

## Decision

Use local-first planning with a bounded official-doc check only for Strava
scope currentness. No broader external research was performed.

## Resulting Constraint

Default the first Body War Strava adapter to `read,activity:read`. Permit
`activity:read_all` only as an explicit escalation when the consenting athlete
needs private or Only Me activity import.
