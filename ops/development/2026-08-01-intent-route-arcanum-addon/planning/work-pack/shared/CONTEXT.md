# Shared context

## Invariants

- Public Arcanum is a separate public authority; private prose and code do not
  cross by convenience.
- The existing private resolver is tested precedent, not canonical source.
- Bootstrap projects accepted sigils; it does not resolve or accept them.
- The route catalog is a read-only digest-bound projection, not a registry.
- Resolver and adapters have zero authority and no independent persistence.
- Human confirmation reuses existing Dispatch/group/seat ownership.
- Augmentor captures/presents; orchestrator binds/launches only after retained
  gates; CAV2/ACI remains private.

## Decision mentality

The runtime profile at `.arcanum/profiles/decision-profile.yml` requires
strictest-safe, default-deny unknowns, propose-then-promote, smallest reliable
slices, named owner lanes, local/static validation first, and durable explicit
approval for mutation.

