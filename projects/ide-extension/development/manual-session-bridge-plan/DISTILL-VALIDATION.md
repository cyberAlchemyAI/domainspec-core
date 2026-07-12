# Distill Validation: Manual Session Bridge Plan

## Control

| Field | Value |
| --- | --- |
| Mode | Validate |
| Verdict | pass |
| Scope | Active L0 plan only |
| First executable unit | `SWU-MSB-001` |
| Role path | Local Proposer/Balancer; no subagents |

## Smallest Coherent Unit

`SWU-MSB-001` is the smallest safe first mutation because all later behavior
depends on one unambiguous v2 contract oracle. Splitting spec, grants, receipt
branches, and fixtures would permit source behavior against a partly defined
authority model. Combining replay or endpoints into 001 would make the first
unit too broad and would weaken the v1 non-regression gate.

## Role Conversation Trace

- Proposer: begin with target/claim endpoints to reproduce the manual poll quickly.
- Balancer objection, evidence validity: current approval terminalizes as a v1
  execution receipt, so endpoint code would encode a known false lifecycle.
- Reconciliation: 001 defines the v2 contract, then 002 proves replay before W1.
- Proposer: let the session claim the oldest approved proposal.
- Balancer objection, human intent: approval is not target selection and could
  execute the wrong private request.
- Reconciliation: singleton `ready_for_poll` remains an operator-owned gate.
- Proposer: add automatic retry after interruption.
- Balancer objection, duplicate execution: timers/leases are L1 and the session
  is unattested.
- Reconciliation: preserve explicit operator release/requeue for read-only L0.

## Recomposition Proof

1. 001-002 establish a versioned contract and stable replay substrate.
2. 003-005 implement the complete kernel authority path from authorization to
   terminal execution receipt.
3. 006-008 expose the same path to the active session and human workbench without
   changing authority ownership.
4. 009-011 prove deterministic hostility/restart behavior, real browser usability,
   and one actual blind manual execution.
5. `TASK-VERIFY-READINESS` only audits and synchronizes the resulting evidence.

Removing any group leaves the product contract ambiguous, the execution
unbound, the human flow unusable, or the proof simulated.

## Validation Matrix

| Check | Verdict | Evidence |
| --- | --- | --- |
| Executable first unit | pass | 001 has inputs, exact write scope, rules, edge cases, done criteria, validation, result, and handoff. |
| One parent per SWU | pass | Eleven manifest IDs are expanded once across five implementation tasks. |
| Task coverage | pass | Five implementation tasks have SWUs; the `VERIFY` task has an explicit closure exemption. |
| Recomposition | pass | Four groups above close the approved prepare-to-receipt loop. |
| Hidden gaps | pass | v1 replay, receipt timing, secrecy, singleton target, interruption, assurance, and live witness are explicit. |
| Deferred complexity | pass | Leases, authentication, mutation, workers, providers, VSCodium, browser control, and remote adapters remain L1-L3. |
| Evidence validity | pass | Fake claimant is the automated oracle; Playwright and one real witness are separate gates. |
| Navigation | pass | Work-pack selects 001 and names the exact Task Session route. |

## Frame Expiry

Replan if the approved decisions change, `SPEC.md` changes L0 authority, another
implementation replaces event/storage semantics, or v1 replay evidence shows an
unmodeled historical shape. Ordinary implementation findings become task residue;
they do not expire the plan unless they cross one of those boundaries.

## Verdict

Pass. The plan is execution-ready at `SWU-MSB-001`; this verdict validates plan
structure and recomposition, not runtime completion.
