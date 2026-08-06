# TASK-AKVE-05: Consultation and Episode Services

- Layer/wave: L2 / W2.
- Lifecycle owner: `animejs-vault-candidate-owner`.

## SWU-AKVE-007: Bounded consultation service

- Primary behavior: turn one authorized bounded query into exactly one tagged
  result over the neutral projection.
- Dependency: SWU-AKVE-006.
- Inputs: host-bound read context, query contract, projection reader, and caps.
- Outputs: ok/abstain/stale/denied/invalid/temporary-failure union.
- Algorithm:
  1. receive pre-authorized view caps and validate unknown fields;
  2. compare expected graph/projection digests before retrieval;
  3. require VersionContext for version-sensitive decisions;
  4. perform bounded lookup/search/context/coverage/decision/episode traversal;
  5. preserve source handles, evidence state, version bounds, explanation path,
     and clearing criteria; enforce result/hop/byte caps;
  6. abstain rather than guess, widen, or fabricate fallback.
- Edge cases: TS-01 through TS-06, ambiguous choice, unsupported performance
  claim, zero admissible evidence, and projection pending/quarantined.
- Split analysis: planning and result formation are one externally reviewable
  consultation behavior governed by shared budgets and status precedence.
- Exact write scope:
  - `projects/animejs/ontology/agent-knowledge-vault/operational/src/consultation-service.mjs`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/fixtures/consultation-cases.json`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/tests/consultation.test.mjs`
- Done: every operation and non-success branch is fixture-backed; no call can
  write the journal or interpret record text as instruction.
- Validation: `node --test projects/animejs/ontology/agent-knowledge-vault/operational/tests/consultation.test.mjs`.
- Execution owner recommendation: `subagent`, with `local-fallback` allowed.

### Closeout synchronization

- Target inventory: exactly the three write-scope paths.
- Baseline binding: all three absent; bind SWU-006 projection interfaces and
  SWU-002 consultation schema digests from owner receipts.
- Admitted deltas: create three files only.
- Owner validation: targeted command plus journal-delta-zero assertion.
- Terminal receipt: `../../task-sessions/SWU-AKVE-007/terminal-receipt.json`.
- Owner receipt: `../../task-sessions/SWU-AKVE-007/owner-closeout.json`.
- Continuation receipt: `../../task-sessions/SWU-AKVE-007/continuation-router.json`.
- Successor policy: route only 008 after pass; otherwise stop.

## SWU-AKVE-008: Episode command service

- Primary behavior: resolve host handles and append one authorized valid event
  with a complete receipt, or append nothing.
- Dependency: SWU-AKVE-007 plus SWU-AKVE-003/004/005 contracts.
- Inputs: host-bound append context, command, Task/Version/Evidence resolver
  ports, transition oracle, journal, and reducer scheduler.
- Outputs: append result/recovery handle and reducer status.
- Algorithm:
  1. reject host-field spoofing and normalize/canonicalize command;
  2. resolve Task/Version exactly once at open and store inert snapshots/digests;
  3. resolve EvidenceHandle producer/target/class/scope before attachment;
  4. invoke the pure transition oracle;
  5. invoke atomic journal append and return its unambiguous result;
  6. schedule reducer without changing the accepted receipt;
  7. apply evidence revocation only to derived eligibility on later reads.
- Edge cases: TS-09 through TS-21, resolver revocation race, reducer pending,
  and committed receipt unavailable.
- Split analysis: handle resolution and command append cannot pass separately
  because resolved immutable bindings are part of the accepted event meaning.
- Exact write scope:
  - `projects/animejs/ontology/agent-knowledge-vault/operational/src/episode-service.mjs`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/fixtures/episode-service-cases.json`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/tests/episode-service.test.mjs`
- Done: all lifecycle, evidence, idempotency, recovery, and semantic-effect
  scenarios pass with exact event deltas.
- Validation: `node --test projects/animejs/ontology/agent-knowledge-vault/operational/tests/episode-service.test.mjs`.
- Execution owner recommendation: `subagent`, with `local-fallback` allowed.

### Closeout synchronization

- Target inventory: exactly the three write-scope paths.
- Baseline binding: all three absent; bind the exact schema, oracle, journal,
  reducer, and projection digests from prior owner receipts.
- Admitted deltas: create three files only; no repository runtime journal data.
- Owner validation: targeted command plus zero Task/canonical-graph/Lesson delta.
- Terminal receipt: `../../task-sessions/SWU-AKVE-008/terminal-receipt.json`.
- Owner receipt: `../../task-sessions/SWU-AKVE-008/owner-closeout.json`.
- Continuation receipt: `../../task-sessions/SWU-AKVE-008/continuation-router.json`.
- Successor policy: route only 009 after pass; otherwise stop.

