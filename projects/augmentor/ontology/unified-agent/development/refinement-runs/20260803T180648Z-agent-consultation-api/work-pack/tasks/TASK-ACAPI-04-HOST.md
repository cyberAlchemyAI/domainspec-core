# TASK-ACAPI-04: ResonantOS Host Integration

- Layer/slice: L1 / S-003.
- Dependencies: complete L0 receipts plus B-002 and B-003 resolution.
- Write boundary: `../workspace-resonant/2.0.0-alpha` only after its owner admits
  the exact SWU.

## SWU-ACAPI-007: Verified Host Context Adapter

- Primary behavior: inject principal, policy, deadline, and cancellation outside
  model-visible tool arguments.
- Acceptance: forged caller fields are impossible; expired/wrong-audience
  context yields minimal denial.
- Split analysis: principal and policy bindings form one verified execution
  context and cannot be accepted separately.
- Write scope:
  `../workspace-resonant/2.0.0-alpha/src/core/augmentor-consultation/context.ts`,
  `../workspace-resonant/2.0.0-alpha/src/core/augmentor-consultation/tool-adapter.ts`,
  and their targeted test files.
- Validation: `npm test -- src/core/augmentor-consultation/context.test.ts && npm run build`.
- Evidence: `work-pack/results/SWU-ACAPI-007-RESULT.md`.
- Owner: subagent under ResonantOS host owner.

## SWU-ACAPI-008: Answer Policy

- Primary behavior: map typed results to answer, qualify, clarify, or abstain
  without following retrieved instructions.
- Acceptance: total mapping for all variants; QS-02-QS-06 and QS-11-QS-14 pass.
- Split analysis: all modes form one total policy table.
- Write scope:
  `../workspace-resonant/2.0.0-alpha/src/core/augmentor-consultation/answer-policy.ts`
  and
  `../workspace-resonant/2.0.0-alpha/src/core/augmentor-consultation/answer-policy.test.ts`.
- Validation: `npm test -- src/core/augmentor-consultation/answer-policy.test.ts`.
- Evidence: result 008.
- Owner: subagent under answering-agent owner.

## SWU-ACAPI-009: End-to-end Host Witness

- Primary behavior: one host question calls the native tool and produces a
  source-linked answer or correct abstention.
- Acceptance: exact fixture covers supported, denied, stale, conflict, and
  embedded-instruction paths; no new write, route, run, approval, or memory event.
- Split analysis: this is one integration witness; the path has no value when
  divided into unjoined partial tests.
- Write scope:
  `../workspace-resonant/2.0.0-alpha/src/core/augmentor-consultation/integration.test.ts`,
  `../workspace-resonant/2.0.0-alpha/src/core/augmentor-consultation/index.ts`,
  and the exact registration changes in
  `../workspace-resonant/2.0.0-alpha/src/core/runtime.ts` selected by the host
  owner during admission.
- Validation: targeted Vitest, `npm run build`, and host event-counter assertions.
- Evidence: result 009.
