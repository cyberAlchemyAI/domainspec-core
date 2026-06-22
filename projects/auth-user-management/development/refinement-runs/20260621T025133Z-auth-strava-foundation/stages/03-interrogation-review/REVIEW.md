# Interrogation Review

## Review Questions

1. Is the target a one-off Body War implementation or a reusable auth
   foundation?
2. Does poker-team cover the reusable auth spine?
3. Does Savvy cover browser-session safety?
4. Does Strava require a first provider adapter decision before implementation?
5. Does any track/game work belong in this slice?

## Answers

1. Reusable foundation first. Body War is the first consumer.
2. Yes, with exclusions. Poker-team covers the auth spine but not browser
   cookie/CSRF transport and not generic roles.
3. Yes, with exclusions. Savvy covers server-owned browser session guards and
   tests but must not transfer mock/client-session auth.
4. Yes. Strava scope and provider token custody must be explicit before code.
5. No. Track geometry, scoring, disputes, and game mechanics stay deferred.

## Risks

- Copying poker-team too literally would leak poker roles and product
  permissions into a reusable foundation.
- Copying Savvy too literally would preserve mock login and client-carried
  session authority.
- Implementing Strava directly in Body War would make later extraction harder.

## Verdict

Pass for review. The remaining decisions are design decisions, not blockers for
continuing the refine loop.
