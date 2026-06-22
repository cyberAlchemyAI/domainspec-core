# Research Decision

Status: pass
Owner: `refine`
Mode: `research-if-gap-appears`

## Decision

No external research is active for this run.

## Reason

The current question is not "what poker libraries exist?" or "what external protocols should we copy?" That research already informed the prior mechanics dispatch. The current question is whether the local spec, architecture, and plan are precise enough to hand to `task-session`.

## Trigger Policy

External research remains blocked unless a later stage names a specific external-context gap, such as:

- A selected Hold'em engine API contract is needed.
- A formal Kuhn or Leduc rules reference is needed to settle fixture semantics.
- A CLI protocol compatibility claim needs comparison to an external standard.

If any named gap appears, bounded research requires explicit operator confirmation before it runs.
