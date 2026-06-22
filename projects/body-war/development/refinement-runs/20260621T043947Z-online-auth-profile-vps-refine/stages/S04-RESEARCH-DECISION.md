# S04 Research Decision

Status: `pass`
Mode: `no-research`

## Decision

Do not perform external research in this Refine run.

## Rationale

The user asked to ground the refinement in local DomainSpec, poker-team, and
infra-spec strategy sources. Those local sources already provide enough
authority for the next non-mutating plan:

- DomainSpec defines the infrastructure constitution, presets, validation
  expectations, and artifact shape.
- poker-team gives a concrete Single VPS reference with compose, Caddy,
  cloud-init, Pulumi TypeScript, and auth domain examples.
- `infra-spec-research-strategy.md` supplies the vocabulary for runtime
  instances, state namespaces, evidence substrate, operational proof status,
  and residue.
- Body War and `auth-user-management` already define the TypeScript runtime
  direction, browser-session security, and Strava provider integration.

## External Research Triggers Later

External research may be useful later only if one of these decisions becomes
unclear during implementation:

- final VPS hardening requirements for the selected hosting provider,
- production OAuth policy changes from Strava,
- legal/privacy language for friend activity consent,
- provider-specific DNS or TLS constraints.

## Handoff

Proceed to Distill and reduce the feature into the smallest executable unit.
