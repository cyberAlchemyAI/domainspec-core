# S04 - Research Decision

Owner: `refine`
Mode: `no-research`
Verdict: `pass`

## Decision

Use `no-research` for this refine run.

## Rationale

The user asked to import and use the local DomainSpec architecture, and the repo already contains two local auth references:

- `validation/poker-team` for TypeScript auth access-control patterns,
- `projects/savvy_legal-studio-ai` for browser cookie/session and security boundary lessons.

External research is not needed to choose the implementation architecture. If production IdP vendor selection, Strava API edge behavior, or cookie deployment policy needs verification later, that should be a bounded follow-up research pass.

## Route Decision

Selected route: `domainspec-typescript-migration`

Rejected:

- `direct-python-patch`, because it preserves the wrong implementation language.
- `policy-only`, because it leaves the wrong auth code in place.

## Research Decision Receipt

- Research mode: `no-research`
- External calls: none
- Blocking gaps: none
- Deferred bounded research candidates: IdP vendor setup, production secret storage, Strava rate-limit/runtime operations.
