# Auth Access Control Docs

This folder was extracted from Poker Team's `auth-access-control` DomainSpec
docs and normalized for `@domainspec/auth-user-management`.

Package authority:

- reusable domain concepts, operations, states, mappings, workflows, events,
  capability docs, test spec, and decisions;
- TypeScript application use cases and ports under `src/`;
- Drizzle/Postgres schema and repository factories as the default SQL surface;
- consumer-provided role definitions and permission grants.

Extracted examples:

- Poker Team roles such as player, coach, manager, and admin are examples of
  consumer-provided role definitions, not package defaults.
- HTTP route, UI, browser cookie, CSRF, Strava, and product profile behavior
  belongs in consuming applications or future adapter packages.
- Historical alignment, pipeline, observability, and UI reports are retained as
  source evidence and should not be read as package runtime obligations unless
  restated in the package README or tests.
