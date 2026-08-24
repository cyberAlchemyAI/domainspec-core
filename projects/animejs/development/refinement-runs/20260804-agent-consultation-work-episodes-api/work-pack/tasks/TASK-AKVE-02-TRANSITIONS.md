# TASK-AKVE-02: Episode Transition Oracle

- Layer/wave: L0 / W1.
- Dependency: SWU-AKVE-002.
- Lifecycle owner: `animejs-vault-candidate-owner`.

## SWU-AKVE-003: Pure closed transition oracle

- Primary behavior: decide whether one normalized command may produce exactly
  one next event from one immutable episode state.
- Inputs: current reduced state, normalized command, resolved host bindings,
  evidence metadata, and exact expected revision/opening graph digest.
- Outputs: `{accepted,event}` or one closed rejection; no I/O.
- Algorithm:
  1. authorize pre-bound owner/delegation and compare frozen graph/revision;
  2. select the operation-specific transition from a closed table;
  3. enforce attempt ordinal, one outcome, no dangling close, terminal lock,
     evidence producer/target bindings, and witness classification policy;
  4. for open, bind exact Task/Version snapshots and optional overlay-only
     terminal supersession after cycle check;
  5. construct one normalized event payload or a zero-effect rejection.
- Ordering: authorization precedes target-derived diagnostics; concurrency and
  digest checks precede state transition; evidence resolution precedes outcome.
- Edge cases: every TS-15 through TS-21 case, duplicate command spelling,
  missing successful evidence, and post-terminal append.
- Split analysis: operation handlers are plausible children, but the primary
  acceptance is totality and exclusivity of one shared transition table.
- Exact write scope:
  - `projects/animejs/ontology/agent-knowledge-vault/operational/src/transition-oracle.mjs`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/fixtures/transition-cases.json`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/tests/transitions.test.mjs`
- Done: every valid transition produces one schema-valid event; every invalid
  transition produces the exact code and no event.
- Validation: `node --test projects/animejs/ontology/agent-knowledge-vault/operational/tests/transitions.test.mjs`.
- Execution owner recommendation: `subagent`, with `local-fallback` allowed.
- Handoff: pure module only; no filesystem, clock, random ID, resolver, or journal.

### Closeout synchronization

- Target inventory: exactly the three write-scope paths.
- Baseline binding: all three absent at Plan time; recapture absence/SHA-256 and
  bind SWU-002 schema/code digests from its owner receipt.
- Admitted deltas: create three files only.
- Owner validation: targeted command plus schema validation of every emitted
  event fixture.
- Terminal receipt: `../../task-sessions/SWU-AKVE-003/terminal-receipt.json`.
- Owner receipt: `../../task-sessions/SWU-AKVE-003/owner-closeout.json`.
- Continuation receipt: `../../task-sessions/SWU-AKVE-003/continuation-router.json`.
- Successor policy: route only 004 after pass; otherwise stop.

