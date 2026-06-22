# Friend Activity Consent Template

Status: `blank-template`
Scope: Private Taquaral Strava validation fixture

This is a template only. Do not fill it with private details in a tracked file
unless the participant explicitly agrees to that storage boundary.

## Consent Record

| Field | Value |
| --- | --- |
| Participant name or private alias | `<private>` |
| Consent date | `<YYYY-MM-DD>` |
| Allowed use | Validate TROQAR Strava connection and redacted activity-summary import. |
| Disallowed use | Public route proof, scoring, leaderboard ranking, marketing, or raw activity publication. |
| Data allowed in tracked artifacts | Redacted receipt only. |
| Data not allowed in tracked artifacts | Tokens, OAuth codes, raw activity payload, maps, notes, private URLs, exact private profile data. |
| Revocation path | Remove validation fixture and mark receipts revoked. |

## Required Confirmation

The participant should explicitly confirm:

```text
I consent to using one of my Strava activities only to validate the TROQAR
connection and redacted activity-summary import flow. I do not consent to this
activity being used as public route proof, scoring authority, or leaderboard
evidence.
```

## Receipt Rule

After consent, record only a redacted activity import receipt. Keep any private
identity mapping or raw evidence outside tracked repository artifacts unless the
participant explicitly approves that storage boundary.
