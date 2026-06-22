# Distill Validation

Verdict: `pass-for-authoring`, `flag-for-promotion`.

## Validation Target

- Objective: create a candidate public testing-specific router and parent
  receipt contract.
- Delivery boundary: `arcanum/arcana/verification-weaver/`.
- Smallest coherent unit: `tasks/SWU-VW-001.md`.
- Work-pack: `WORK-PACK.md`.
- Handoff: `RUNTIME-HANDOFF.md`.

## Pass Checks

- The unit is small enough to execute in one task-session.
- The unit is large enough to prove route, receipt, fixtures, negative controls,
  and local validation together.
- The unit recomposes into the approved design without registry/runtime
  exposure.
- Owner boundaries are explicit and status-qualified.
- Private evidence is internal-only.

## Flags

- The package is not promotion-ready until synthetic fixture evidence and an
  experiment-harness report exist.
- `ux-evidence-validator` remains seed/not promoted; UX lane receipts may only
  flag or record residue until calibrated harness evidence exists.
- A follow-on `sigil-development` route is required before runtime or registry
  promotion.

## Repair Route

Execute `SWU-VW-001` with Task Session, then route the validated candidate to
`sigil-development` and `experiment-harness`.
