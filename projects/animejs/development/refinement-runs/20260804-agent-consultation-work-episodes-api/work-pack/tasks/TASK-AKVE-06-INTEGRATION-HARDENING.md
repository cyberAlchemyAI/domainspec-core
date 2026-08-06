# TASK-AKVE-06: Capability Integration and Hardening

- Layer/wave: L2 / W3.
- Lifecycle owner: `animejs-vault-candidate-owner`.

## SWU-AKVE-009: Disjoint capability adapters

- Primary behavior: bind four exact host capability audiences before parsing
  target identifiers or dispatching service operations.
- Dependency: SWU-AKVE-008.
- Inputs: invocation descriptor, opaque host context, closed request body, and
  four service ports.
- Outputs: authorized service result or opaque denial with zero side effects.
- Algorithm:
  1. select adapter by trusted invocation descriptor, never body operation;
  2. require the exact audience and reject generic/mixed/wildcard grants;
  3. inject principal/workspace/vault/policy/request context after body parsing
     rejects spoofed copies;
  4. authorize before target lookup and normalize denied results;
  5. route consultation, append, receipt recovery, or project read only to its
     named port; record separate audit dimensions.
- Edge cases: TS-07/08, cross-capability body reuse, foreign recovery handle,
  unknown adapter, body-directed privilege, and target-existence probes.
- Split analysis: per-route adapters are plausible children, but only the full
  capability matrix proves non-substitutability and opaque denial.
- Exact write scope:
  - `projects/animejs/ontology/agent-knowledge-vault/operational/src/capability-adapters.mjs`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/fixtures/capability-cases.json`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/tests/security.test.mjs`
- Done: the complete route/audience matrix passes and every denial has zero
  journal/projection delta and no target-derived metadata.
- Validation: `node --test projects/animejs/ontology/agent-knowledge-vault/operational/tests/security.test.mjs`.
- Execution owner recommendation: `subagent`, with `local-fallback` allowed.

### Closeout synchronization

- Target inventory: exactly the three write-scope paths.
- Baseline binding: all three absent; bind the SWU-007 and SWU-008 service
  interface digests from owner receipts.
- Admitted deltas: create three files only.
- Owner validation: targeted command and explicit zero-delta denial matrix.
- Terminal receipt: `../../task-sessions/SWU-AKVE-009/terminal-receipt.json`.
- Owner receipt: `../../task-sessions/SWU-AKVE-009/owner-closeout.json`.
- Continuation receipt: `../../task-sessions/SWU-AKVE-009/continuation-router.json`.
- Successor policy: route only 010 after pass; otherwise stop.

## SWU-AKVE-010: Aggregate validator and operational guide

- Primary behavior: provide one deterministic local acceptance entrypoint and
  document only the behavior it actually validates.
- Dependency: SWU-AKVE-009.
- Inputs: all contracts, fixtures, source modules, tests, and current canonical
  vault digest.
- Outputs: aggregate JSON receipt plus operational README.
- Algorithm:
  1. validate JSON and cross-contract references;
  2. run all operational tests in a fixed order using isolated temp stores;
  3. map TS-01 through TS-30 to observed assertions;
  4. inventory existing canonical vault files before/after and require zero delta;
  5. run twice, compare deterministic result/digest fields, and write the
     receipt only after all checks pass;
  6. document capability boundaries, commands, evidence ceiling, and exclusions.
- Edge cases: partial suite failure, leftover temp data, nondeterministic digest,
  missing scenario mapping, and accidental readiness/deployment language.
- Split analysis: the validator and README are separable artifacts, but the
  primary behavior is one usable and accurately described acceptance surface.
- Exact write scope:
  - `projects/animejs/ontology/agent-knowledge-vault/operational/scripts/validate.mjs`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/README.md`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/receipts/validation-receipt.json`
- Done: two aggregate runs pass with equal deterministic fields; every toy
  scenario is mapped; README claims no more than candidate-local validation.
- Validation: `node projects/animejs/ontology/agent-knowledge-vault/operational/scripts/validate.mjs --verify-repeat`.
- Execution owner recommendation: `subagent`, with `local-fallback` allowed.

### Closeout synchronization

- Target inventory: exactly the three write-scope paths; the receipt path may
  be rewritten only by the validator from declared inputs.
- Baseline binding: all three absent; bind every prior owner receipt and current
  canonical vault digest at admission.
- Admitted deltas: create three files only; generated receipt must be
  deterministic except declared timestamps kept outside its comparison digest.
- Owner validation: targeted command, JSON validation, scenario coverage 30/30,
  and zero canonical-vault delta.
- Terminal receipt: `../../task-sessions/SWU-AKVE-010/terminal-receipt.json`.
- Owner receipt: `../../task-sessions/SWU-AKVE-010/owner-closeout.json`.
- Continuation receipt: `../../task-sessions/SWU-AKVE-010/continuation-router.json`.
- Successor policy: terminal. Report L2 candidate evidence; do not route into L3.

