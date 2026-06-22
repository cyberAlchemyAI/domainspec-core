# Refine Result - Online Auth/Profile VPS Slice

Status: `flag`

The confirmed Refine loop has executed. It produced a non-executed but
implementation-ready route for the Body War/TROQAR online auth/profile/VPS
slice.

Primary artifacts:

- `projects/body-war/docs/features/troqar-product-architecture/ONLINE-AUTH-PROFILE-INFRA.md`
- `projects/body-war/development/refinement-runs/20260621T043947Z-online-auth-profile-vps-refine/INFRA-DEFINITION-EXTRACTION.md`
- `projects/body-war/development/refinement-runs/20260621T043947Z-online-auth-profile-vps-refine/stages/S01-CONTEXT-BUILDER.md`
- `projects/body-war/development/refinement-runs/20260621T043947Z-online-auth-profile-vps-refine/stages/S02-INVOKE-DEFINE.md`
- `projects/body-war/development/refinement-runs/20260621T043947Z-online-auth-profile-vps-refine/stages/S06-INVOKE-DESIGN.md`
- `projects/body-war/development/refinement-runs/20260621T043947Z-online-auth-profile-vps-refine/stages/S09-INVOKE-PLAN.md`
- `projects/body-war/development/refinement-runs/20260621T043947Z-online-auth-profile-vps-refine/stages/S10-FINAL-INTERROGATION.md`

Dispatch validation status: `VALIDATION=pass`.

## Final Synthesis

- The new L0 priority is the Online Identity Loop: HTTPS app, secure browser
  session, Strava connect, minimal profile, safe Strava profile link, redacted
  activity summaries, and deployment receipt.
- `projects/auth-user-management/` should be the reusable TypeScript auth and
  Strava integration package, not a one-off Body War copy.
- DomainSpec provides the infra constitution; poker-team provides structural
  Single VPS evidence; Body War must own its own infra artifacts.
- Production token custody requires PostgreSQL or equivalent durable
  server-side storage before public Strava validation.
- The friend's Taquaral activity is a future validation fixture only after
  consent and redacted import receipts.
- Track geometry, scoring, social, rankings, and economy remain intentionally
  deferred.

## Implementation Plan

The refined work-pack is `WP-BWO-ONLINE-AUTH-PROFILE-VPS`.

Recommended first Task Session:

`SWU-BWO-001`: author `projects/body-war/docs/INFRA-ARCHITECTURE.md` from the
online slice definition, DomainSpec infra template, poker-team infra reference,
and infra-spec strategy.

Then proceed through:

1. Body War compose/Caddy/env secret inventory.
2. Postgres-backed auth/profile/provider store.
3. `/api/profile` and `/profile`.
4. Strava link and redacted activity summaries.
5. VPS deployment receipt.

## Open Flags

- canonical domain and app origin,
- VPS access/deploy user,
- Strava production redirect URI,
- Postgres store adapter,
- friend consent receipt,
- monitoring depth,
- Taquaral geometry authority.

These flags do not block implementation, but they block any claim that the app
is production-ready online.
