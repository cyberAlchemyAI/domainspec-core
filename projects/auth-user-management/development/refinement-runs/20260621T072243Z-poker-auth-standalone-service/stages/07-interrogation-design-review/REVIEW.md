# Interrogation Review: Design

## Mode Result

- Mode: refine-design-review
- Questions asked: 0
- Decisions recorded: 2
- Artifacts updated: none
- Verdict: pass

## Review Findings

### Finding 1: Application dependency normalization is mandatory

Poker Team use cases directly import telemetry, `jsonwebtoken`, `bcrypt`,
`randomUUID`, `new Date()`, and `process.env`. A reusable importable package
must make these dependencies injectable or move them to infrastructure helpers.

Severity: high

Resolution: keep this as a work-pack acceptance gate.

### Finding 2: Role definitions are useful as examples, unsafe as defaults

Poker Team roles include player, coach, manager, admin, and product-specific
permissions. Copying those as defaults would make the reusable service falsely
Poker-specific.

Severity: medium

Resolution: expose role-definition types and seed helpers; consumers provide
role sets.

### Finding 3: Drizzle schema is source evidence but needs package ownership

The Poker Team schema is mixed with players, stats, transactions, onboarding,
and coaches. The standalone package should copy only auth tables/enums and
export them as its own schema object.

Severity: medium

Resolution: execution SWU owns a focused schema extraction.

## Gate Review

| Gate | Result |
| --- | --- |
| Source boundary | pass |
| Drizzle/Postgres default | pass |
| TypeScript runtime | pass |
| No Poker Team product defaults | pass with work-pack guardrail |
| Importable service API | pass with port-normalization guardrail |

## Verdict

pass
