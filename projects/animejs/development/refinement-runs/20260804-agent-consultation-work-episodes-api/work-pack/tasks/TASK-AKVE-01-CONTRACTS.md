# TASK-AKVE-01: Closed Contracts

- Layer/wave: L0 / W0.
- Design sources: [API contract](../../API-CONTRACT.md),
  [design](../../stages/06-design.md), and
  [toy scenarios](../../stages/08-toy-scenarios.md).
- Lifecycle owner: `animejs-vault-candidate-owner`.

## SWU-AKVE-001: Neutral projection contract

- Primary behavior: mechanically admit only closed neutral-projection records,
  views, and manifest fields; reject leakage before emitting a projection
  digest.
- Inputs: current vault graph digest, host-selected allowed views, compiler
  version, and candidate records.
- Outputs: validated manifest/record bytes or a closed leakage diagnostic.
- Algorithm:
  1. validate closed schemas with unknown fields forbidden;
  2. intersect requested views with host-granted views;
  3. traverse every record field and role-shaped metadata against the allowlist;
  4. canonicalize accepted fields and sort by opaque record ID;
  5. hash allowlist, records, and manifest; emit no digest on a leakage finding.
- Edge cases: private path, owner route, principal/policy, authority/release,
  prompt role, executable content, unknown view, and digest mismatch.
- Split analysis: schema and leakage mutants are plausible children, but neither
  can independently accept the allowlist boundary.
- Exact write scope:
  - `projects/animejs/ontology/agent-knowledge-vault/operational/contracts/neutral-projection-manifest.schema.json`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/contracts/neutral-projection-record.schema.json`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/contracts/projection-allowlist.json`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/fixtures/projection-contract-cases.json`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/tests/contracts.test.mjs`
- Done: positive record/manifest fixtures pass and every forbidden-field mutant
  fails without a projection digest.
- Validation: `node --test --test-name-pattern='neutral projection' projects/animejs/ontology/agent-knowledge-vault/operational/tests/contracts.test.mjs`.
- Execution owner recommendation: `subagent`, with `local-fallback` allowed.
- Expected result shape: standard SWU receipt with files, targeted command,
  leakage-case count, blockers, residue, and successor 002.

### Closeout synchronization

- Target inventory: exactly the five write-scope paths above.
- Baseline binding: all five paths were absent at Plan time; Task Session must
  recapture presence/SHA-256 and block if any is present or any parent path
  resolves outside `operational/`.
- Admitted deltas: create those five regular files only; no existing vault file
  may change.
- Owner validation: the targeted command above plus an inventory diff proving
  zero writes outside the five paths.
- Terminal receipt: `../../task-sessions/SWU-AKVE-001/terminal-receipt.json`.
- Owner receipt: `../../task-sessions/SWU-AKVE-001/owner-closeout.json`.
- Continuation receipt: `../../task-sessions/SWU-AKVE-001/continuation-router.json`.
- Successor policy: route only 002 after all three receipts pass; otherwise stop.

## SWU-AKVE-002: Episode contract language

- Primary behavior: define one closed command/event/result language shared by
  every later component.
- Dependencies: SWU-AKVE-001 terminal receipt.
- Inputs: API contract invariants and closed capability/status/code sets.
- Outputs: strict schemas, code table, and positive/negative fixtures.
- Algorithm:
  1. encode five command operations with no `supersede_episode` spelling;
  2. encode event variants, revision/digest chain, and host-only field boundary;
  3. encode append/read result unions and semantic-effect-none fields;
  4. close outer statuses and diagnostics in one code table;
  5. assert all schema/result/code references are total and unknown fields fail.
- Edge cases: caller identity, inline Task snapshots, caller episode ID on open,
  generic capability token, missing expected revision, and unknown status/code.
- Split analysis: command, event, and result schemas are file-level children,
  but their shared status/digest vocabulary is the independently accepted unit.
- Exact write scope:
  - `projects/animejs/ontology/agent-knowledge-vault/operational/contracts/consultation-request.schema.json`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/contracts/consultation-result.schema.json`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/contracts/episode-command.schema.json`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/contracts/episode-event.schema.json`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/contracts/episode-result.schema.json`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/contracts/status-codes.json`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/fixtures/episode-contract-cases.json`
- Done: all variants are closed, mutually coherent, fixture-backed, and carry
  the frozen context plus semantic-effect-none contract.
- Validation: `node --test --test-name-pattern='episode contract' projects/animejs/ontology/agent-knowledge-vault/operational/tests/contracts.test.mjs`.
- Execution owner recommendation: `subagent`, with `local-fallback` allowed.
- Handoff: do not implement transitions or storage.

### Closeout synchronization

- Target inventory: exactly the seven write-scope paths above plus the existing
  SWU-001 `contracts.test.mjs`, whose admitted delta is test additions only.
- Baseline binding: the seven new paths absent; `contracts.test.mjs` SHA-256
  must equal the SWU-001 owner receipt. Drift blocks.
- Admitted deltas: create seven files and append episode-contract tests only.
- Owner validation: targeted command plus rerun the SWU-001 command.
- Terminal receipt: `../../task-sessions/SWU-AKVE-002/terminal-receipt.json`.
- Owner receipt: `../../task-sessions/SWU-AKVE-002/owner-closeout.json`.
- Continuation receipt: `../../task-sessions/SWU-AKVE-002/continuation-router.json`.
- Successor policy: route only 003 after pass; otherwise stop.

