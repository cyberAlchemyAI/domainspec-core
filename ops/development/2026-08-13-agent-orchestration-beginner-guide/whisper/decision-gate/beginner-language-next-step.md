---
decision_id: DG-AOG-BEGINNER-LANGUAGE-001
status: resolved
target_scope: beginner-language tournament next step
source_plan: ../beginner-language-tournament-plan.md
source_plan_sha256: 5a4fcc97b199e94de133e5cd8d7ad68276e3a45a5de0453e58145005a805bd65
admissibility_request: beginner-language-next-step.request.json
admissibility_request_digest: 2766bcdb3449d8cec06953e725e08aff70d02a143e856f091c5551f0fdaa5c1c
admissibility_receipt: beginner-language-next-step.receipt.json
---

# Beginner-language tournament next-step decision

## Decision question

Which route should govern the next beginner-language step?

## Admissible options

### `LANG-AUDITION-STAGE` — stage the audition proposal

Prepare and validate only the governed dispatch proposal for Waves 0–2:
baseline extraction, three small independent auditions, and two independent
reviews. Return the exact strategy and action digests for a separate human
confirmation. Do not register or spawn agents, rewrite all seven routes, edit
HTML, promote, publish, or deploy.

Trade-off: this adds a small governance step, but it tests the voice and teaching
movement before spending a full tournament on language that may still be wrong.

### `LANG-PLAN-REVISE` — revise before staging

Keep the current guide and proposed plan unchanged while the operator revises
the audience assumption, vocabulary policy, audition moments, candidate tracks,
review criteria, or wave shape.

Trade-off: this postpones learner-facing improvement, but avoids constructing a
dispatch around a plan the operator does not yet endorse.

### `LANG-TOURNAMENT-STOP` — stop this initiative

End the tournament initiative and retain the current guide and deployed route
as they are.

Trade-off: this avoids further coordination cost, but leaves the reported
beginner-language friction unresolved.

## Structurally rejected shortcut

`LANG-FULL-FANOUT-NOW` is not an admissible preference. The intent is volatile,
the exact audition dispatch has not been validated or confirmed, and Human Gate
A has not selected and frozen a voice direction and term policy. A full
seven-route fan-out would contradict the accepted plan boundary.

## Current decision state

- Selected option: `LANG-AUDITION-STAGE`
- Rationale: the operator selected the exact option ID after receiving the
  expanded trade-offs; no additional rationale was supplied.
- Source of decision: direct operator message `LANG-AUDITION-STAGE`
- Decision timestamp: `2026-08-16T14:42:55Z`
- Result: `PASS`
- Remaining blocker: none at this decision gate
- Consequential mutations performed: none
- Dispatches registered or spawned: none
- Guide or deployment bytes changed: none

The earlier “explain or show more context” turn did not resolve the gate. The
later exact option selection did; downstream dispatch execution still requires
its own confirmation after the complete strategy passes readiness and tension.
