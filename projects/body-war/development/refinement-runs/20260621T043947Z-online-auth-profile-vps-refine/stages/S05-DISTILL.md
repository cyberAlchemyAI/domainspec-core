# S05 Distill - Smallest Coherent Unit

Status: `pass`
Capability: `distill`
Input: `stages/S04-RESEARCH-DECISION.md`

## Smallest Coherent Unit

The smallest useful unit is the Online Identity Loop:

1. A runner reaches the app over HTTPS.
2. The server establishes a secure browser session.
3. The runner connects Strava through OAuth.
4. The profile page shows identity, connection state, privacy state, and a safe
   link to the connected Strava profile.
5. The app imports and displays redacted activity summaries.
6. A deployment receipt proves health, login, Strava connect, profile, activity,
   CSRF, and secret-redaction checks.

## Why This Unit Holds Together

- Login without profile is not product-visible enough.
- Profile without Strava is not the desired TROQAR identity flow.
- Strava without durable token custody is not production-ready.
- VPS deployment without a receipt is not operationally meaningful.
- Activity summaries without consent and redaction are not safe validation
  evidence.

## What It Enables Later

This unit composes into later Body War/TROQAR work:

- activity evidence can feed future run proof,
- profile identity can feed scoring and social presence,
- deployment receipts can feed operational governance,
- Strava summaries can support Taquaral validation once route geometry is ready.

## What It Does Not Do

This unit does not:

- define the Taquaral track geometry,
- validate a run against a track,
- score a runner,
- publish leaderboards,
- create challenges,
- implement economy,
- provide admin/operator content management.

## Distilled Risk

The dominant risk is false closure: shipping "connected to Strava" while tokens,
sessions, consent, and deployment proof are still local-pilot quality. The plan
must put durable storage and receipts before any production claim.

## Handoff

Proceed to Invoke Design around this single loop.
