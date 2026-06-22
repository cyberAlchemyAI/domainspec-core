# Interrogation Review: Define

## Mode Result

- Mode: refine-review
- Questions asked: 0
- Decisions recorded: 3
- Artifacts updated: none
- Verdict: pass

## Review Questions Resolved From Evidence

### Is the source boundary correct?

Yes. The user named
`validation/poker-team/backend/src/domain/auth-access-control`, and repository
evidence shows that application use cases, Drizzle repositories, schema, and
tests are adjacent to that domain. The route should copy the whole vertical
slice, not just the domain folder.

### Can the copied code be imported by any service as-is?

No. The application use cases import Poker Team telemetry, JWT and bcrypt
directly, and some values from `process.env`. The reusable package needs ports
for token codec, password service, clock, id generation, telemetry, and
configuration.

### Should bootstrap role definitions be copied as defaults?

Not as authority. `role-definitions.ts` contains Poker Team permissions such as
player-management, player-makeup, and financial-settlement. The reusable
package may include a role-definition type and helper, but consumers must supply
their own default roles.

## Decisions

| Decision | Rationale |
| --- | --- |
| Copy vertical slice rather than domain-only. | Application readiness and tests already exist in Poker Team. |
| Normalize concrete dependencies into ports. | Importable service must not depend on Poker Team infrastructure or process env. |
| Use Drizzle/Postgres repository as production SQL default. | Matches current architecture invariant and Poker Team source implementation. |

## Risks

- If implementation keeps the old `projects/auth-user-management` JSON-store
  shape as production authority, it will conflict with this corrected route.
- If tests are copied without trimming HTTP-layer `buildApp` assertions, the
  standalone package will inherit Poker Team route coupling.
- If JWT/bcrypt remain hard imports inside use cases, future services cannot
  choose transport/security policy cleanly.

## Verdict

pass
