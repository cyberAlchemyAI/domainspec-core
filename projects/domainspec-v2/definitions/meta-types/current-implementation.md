# Current Meta-Type Implementation State

Status: owner-admitted, frozen, project-local

The current canonical implementation baseline is
`domainspec-meta-types-current-implemented@3`, with baseline digest
`af97cd70315f509adcdb4b647951a01f8636da08a07f06f7902e803f546d65cb`.
Its immutable manifest is
[`CANONICAL-IMPLEMENTED-BASELINE.v3.json`](../../development/meta-type-instantiation-cli/CANONICAL-IMPLEMENTED-BASELINE.v3.json).

This is the canonical answer to “what DomainSpec meta-type implementation exists now?”:

- all 13 active backend meta-types have one admitted realization in TypeScript, Python, and Rust;
- the baseline therefore contains 39 exact realization rows;
- every row binds a source, provider, and binding path and digest;
- the 11 UI meta-type rows remain frozen supporting context at their existing maturity and are outside the
  first CLI instantiation surface;
- the 31 canonical relationship signatures remain governed by DS-D8;
- the private CLI implements deterministic instantiation and static target conformance for the
  TypeScript, Python, and Rust profiles;
- Workflow Compensation is an admitted forward-recovery Operation role with an intent-only Workflow
  boundary and separate external executor;
- prior form-queue and provider/profile gate findings remain provenance only and do not control this baseline.

Semantic maturity, implementation admission, and target conformance are separate axes. DS-D1 defines what the
meta-types mean. This state records which implementation bytes are selected. Today, target instantiation and static conformance are implemented and admitted for the private three-profile CLI. Runtime observation remains bounded by admitted providers, and the next product unit is the durable compensation dispatcher.

For Operation (`DS-D1.4`), the selected implementation contract includes declared read, write, and effect
sets; guard execution before state mutation; atomic state-and-outbox behavior; explicit failure continuation;
no undeclared reads, writes, or effects; and typed relationships to Rule, Event, and Workflow.

For Workflow Compensation (`domainspec-v2-D36`), the admitted contract uses the states `not-required`,
`requested`, `running`, `completed`, and `failed`. Workflow evaluation emits intent and plan only. A separate
external executor preflights all exact Operation bindings before invocation and preserves deterministic
idempotency. Durable storage, claiming, retry scheduling, and restart recovery are not implemented.

Baselines `@1` and `@2` remain immutable historical evidence. Baseline `@3` admits the current definitions,
realizations, and compensation-contract epoch without rewriting either predecessor. The private CLI and its
static generated-target observer consume `@3` as a separate current-state conformance surface.

Claim ceiling: this state admits a canonical project-local implementation baseline and bounded static
generated-target conformance. It does not prove durable compensation dispatch, publish or release a package,
deploy anything, or establish production readiness.
