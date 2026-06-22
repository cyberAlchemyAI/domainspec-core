# Subagent Receipts

Status: complete
Join policy: parent synthesis

## Route Choice Reviewer

- Role: `route-choice-reviewer`
- Verdict: no-block for continuing Refine; block immediate app mutation before
  final plan.
- Findings:
  - Keep Strava as the only visible MVP login method.
  - Preserve provider extensibility internally.
  - Keep refinement planning-only before Task Session implementation.
- Residue:
  - Reconcile CTA wording: `Connect Strava` vs `Continue with Strava`.
  - Document hidden provider extensibility.
  - Define exact Studio live-page handoff and validation commands.

## Alternative Comparator

- Role: `alternative-comparator`
- Verdict: no-block for plain static hardening; defer framework migration.
- Ranked route:
  1. Plain HTML/CSS/JS hardening.
  2. Lightweight icon/package support only if accepted as necessary.
  3. Framework/bundler migration deferred.
- Findings:
  - Current package has no frontend bundler or UI component library.
  - Existing Playwright tests already target the static shell.
  - Dynamic template-string rendering in tracks/submissions should be hardened
    before production acceptance.

## Structure Explorer

- Role: `structure-explorer`
- Verdict: no-block for Refine; block production implementation if callback,
  error, preview-evidence, geometry-status, and anonymous login-first states are
  not modeled.
- Missing states:
  - anonymous login-first page;
  - callback success/error/retry;
  - provider disconnected/reconnect;
  - activity loading/empty/provider-error;
  - evidence preview status;
  - per-track geometry status;
  - POST submit errors.
- Required new anchors:
  - `auth.login-first`
  - `auth.callback-status`
  - `auth.error.banner`
  - `auth.reconnect.cta`
  - `profile.privacy-card`
  - `activity.loading`
  - `activity.empty`
  - `activity.error`
  - `track.geometry-status`
  - `evidence.status-chip`
  - `evidence.submission-list`
  - `evidence.submit.error`

## Falsification Reviewer

- Role: `falsification-reviewer`
- Verdict: no-block for planning; block production-readiness acceptance until
  falsification checks exist and pass.
- Required checks:
  - anonymous page is login-first and not internal dashboard;
  - exactly one visible Strava CTA;
  - no alternative login providers in MVP;
  - fake-Strava connected state recomposes into profile/activity/evidence;
  - auth error state is user-safe and retryable;
  - no verified/scoring/control overclaim;
  - Studio selector continuity;
  - mobile at 390x844 and 320x568.
- Required evidence:
  - anonymous desktop/mobile screenshots;
  - connected desktop/mobile screenshots;
  - auth-error screenshot;
  - trace on first failure;
  - selector table from Studio handoff to real app.
