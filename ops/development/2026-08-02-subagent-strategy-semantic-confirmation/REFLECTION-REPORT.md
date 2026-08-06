# Workflow Reflection Report

- Target: `domainspec-subagents-strategy` / public `subagent-strategy` core
- Trigger: severe confirmation-gap correction
- Decision: targeted update
- Observer: `/root/confirmation_rule_observer` (`Euler`), read-only

## Finding

The current contract uses one SHA-256 value for two different jobs:

1. machine identity for readiness, tension, and registration; and
2. the scope of human authorization.

The first job requires exact bytes. The second requires stable meaning. Treating
them as identical forces a repeated human confirmation when canonicalization or
evidence materialization changes bytes without changing the strategy the human
reviewed.

## Adopted contract

- Exact sheet digest remains the machine identity.
- Human confirmation binds a deterministic material-strategy projection.
- Every byte revision reruns readiness and both independent tension checks.
- A prior confirmation carries only after current machine gates pass and a
  deterministic equivalence check proves the material projection unchanged.
- Material changes and unknown or unprovable equivalence require reconfirmation.

## Material fields

Objective and evidence boundary; dispatch type; lanes and purposes; identities,
roles, angles, prompts, and source scope; outputs; dependency topology and loop
ceilings; final approver; destination; publication/privacy boundary; validation;
and stop conditions.

## Mechanical fields

Whitespace, key ordering, machine digests and evidence handles, derived counts,
schema defaults, and canonical materialization of content already shown to the
human, provided deterministic projection equivalence succeeds.

## Rejected alternatives

- Removing exact digests: weakens machine integrity.
- Treating every delta as subjective: not deterministic or auditable.
- Special-casing only the current incident: not reusable.
- Carrying confirmation when equivalence is unknown: not fail-closed.

## Required regression evidence

- Formatting-only and canonical-materialization changes do not reconfirm.
- Material changes do reconfirm.
- Unknown equivalence fails closed.
- Stale machine digests and tension receipts remain rejected.
