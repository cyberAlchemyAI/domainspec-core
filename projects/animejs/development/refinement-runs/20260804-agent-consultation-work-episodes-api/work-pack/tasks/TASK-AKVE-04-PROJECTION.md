# TASK-AKVE-04: Reducer and Isolated Overlay

- Layer/wave: L1 / W1.
- Lifecycle owner: `animejs-vault-candidate-owner`.

## SWU-AKVE-005: Deterministic version-keyed reducer

- Primary behavior: replay one exact episode journal into canonical snapshot
  bytes keyed by reducer version and last-event digest.
- Dependency: SWU-AKVE-004.
- Inputs: ordered event bytes and reducer version.
- Outputs: immutable snapshot, snapshot digest, migration receipt, or quarantine diagnostic.
- Algorithm:
  1. verify schema, episode identity, contiguous revision, exact input order,
     prior-event chain, event digest, and frozen opening graph policy;
  2. replay from empty state through the pure transition application table;
  3. reject gap, fork, shuffle, impossible transition, or trailing corruption;
  4. canonicalize the state and hash the exact bytes;
  5. key output by reducer version plus last-event digest;
  6. on version change, retain old bytes and emit a migration receipt.
- Edge cases: TS-22 through TS-26, empty journal, single open, truncated tail,
  and evidence later marked revoked without rewriting history.
- Split analysis: verification, replay, and hashing are implementation steps of
  one accepted deterministic-state behavior.
- Exact write scope:
  - `projects/animejs/ontology/agent-knowledge-vault/operational/src/reducer.mjs`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/fixtures/reducer-cases.json`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/tests/reducer.test.mjs`
- Done: identical input/version yields byte-identical output; corrupt input
  never yields a current snapshot; upgrades preserve prior snapshots.
- Validation: `node --test projects/animejs/ontology/agent-knowledge-vault/operational/tests/reducer.test.mjs`.
- Execution owner recommendation: `subagent`, with `local-fallback` allowed.

### Closeout synchronization

- Target inventory: exactly the three write-scope paths.
- Baseline binding: all three absent at Plan time; bind SWU-004 journal and
  canonical-JSON digests from its owner receipt.
- Admitted deltas: create three files only.
- Owner validation: targeted command twice with equal snapshot bytes/digests.
- Terminal receipt: `../../task-sessions/SWU-AKVE-005/terminal-receipt.json`.
- Owner receipt: `../../task-sessions/SWU-AKVE-005/owner-closeout.json`.
- Continuation receipt: `../../task-sessions/SWU-AKVE-005/continuation-router.json`.
- Successor policy: route only 006 after pass; otherwise stop.

## SWU-AKVE-006: Episode overlay and projection compiler

- Primary behavior: compile reducer snapshots into an allowlisted, isolated
  operational episode overlay without mutating canonical graph material.
- Dependency: SWU-AKVE-005.
- Inputs: current snapshots, evidence eligibility overlays, projection
  manifest/allowlist, and unchanged canonical vault digest.
- Outputs: episode-only overlay records, neutral projection bytes/digest,
  leakage report, and current/pending/failed/corrupt/quarantined status.
- Algorithm:
  1. accept only five overlay record kinds from the API contract;
  2. strip all canonical node/relation IDs and forbidden field classes;
  3. render supersession as overlay-only reference and revoked evidence as
     derived unconfirmed eligibility;
  4. compile allowed views in stable order and hash canonical bytes;
  5. compare canonical vault files/digest before/after and require zero delta;
  6. quarantine only affected episodes on reducer/projection corruption.
- Edge cases: TS-05, TS-16, TS-21, TS-27 through TS-30, and unaffected records
  during one episode quarantine.
- Split analysis: overlay formation and projection compilation share the
  single-derived-writer/no-canonical-write acceptance boundary.
- Exact write scope:
  - `projects/animejs/ontology/agent-knowledge-vault/operational/src/overlay.mjs`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/src/projection.mjs`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/fixtures/overlay-cases.json`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/tests/projection.test.mjs`
- Done: deterministic projection passes; forbidden kinds/fields fail; current
  nodes, relations, sources, and views have byte-for-byte zero delta; closing
  an episode creates zero Lessons.
- Validation: `node --test projects/animejs/ontology/agent-knowledge-vault/operational/tests/projection.test.mjs`.
- Execution owner recommendation: `subagent`, with `local-fallback` allowed.

### Closeout synchronization

- Target inventory: exactly the four write-scope paths.
- Baseline binding: all four absent; bind SWU-001 allowlist and SWU-005 reducer
  digests, plus current canonical vault graph digest, at admission.
- Admitted deltas: create four operational files only; canonical vault delta
  must be zero.
- Owner validation: targeted command and scoped SHA-256 before/after inventory
  of `nodes/`, `relations/`, `sources/`, and existing `views/`.
- Terminal receipt: `../../task-sessions/SWU-AKVE-006/terminal-receipt.json`.
- Owner receipt: `../../task-sessions/SWU-AKVE-006/owner-closeout.json`.
- Continuation receipt: `../../task-sessions/SWU-AKVE-006/continuation-router.json`.
- Successor policy: route only 007 after pass; otherwise stop.

