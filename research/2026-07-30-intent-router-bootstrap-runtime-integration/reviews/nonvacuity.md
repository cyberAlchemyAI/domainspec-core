# Non-Vacuity and Runtime Parity Review — Gödel, Kurt

dispatch_id: `2026-07-30-intent-router-bootstrap-runtime-integration`  
step_id: `s3`  
capability_ref: `research`  
capability_target: `dispatch-sheet.json`  
capability_mode: `review`  
wave_id: `review`  
write_scope: `[]`  
status: `BLOCK`  
artifacts: `[]`  
validation: `Read-only review of synthesis.md, research.md, synthesis receipt, three explorer receipts, and exact cited private JSON-port/core test selectors. Current private standalone tests witness only existing core behavior; generated public core/wrappers and orchestrator adapter do not exist.`  
observer_status: `not-invoked-read-only-review`

blockers:

- `no-witness.executable-command-matrix`: The “Exact future validation fixtures” section contains assertions, not exact commands with exact expected exit codes/stdout/stderr for the five required surfaces.
- `no-witness.public-core`: No candidate public core exists, so private tests cannot witness extraction correctness, public/private cleanliness, version/digest binding, or public behavior.
- `no-witness.generated-wrapper-parity`: Neither generated resolver wrapper exists. Shared generation topology and directory presence cannot prove behavior parity.
- `no-witness.orchestrator-adapter`: No thin adapter, selection artifact, catalog owner, normalization owner, transport policy, persistence schema, or launch-gate tests exist.
- `no-witness.negative-coverage`: Current executable JSON-port evidence does not witness the complete required negative matrix.
- `no-witness.expected-output`: Proposed future runner commands lack output schema, exact expected bytes/count, exit code, and stderr contract.
- `no-witness.rollback`: No pinned prior-version rollback fixture or expected restored digest is specified.

residue:

- `private-core-current-witness-only`
- `future-public-extraction`
- `exact-command-contract`
- `exact-output-contract`
- `cross-runtime-behavior-parity`
- `adapter-failure-injection`
- `no-launch-observation-points`
- `durable-rollback-witness`

reroute: `Return to synthesis for a bounded validation-contract repair only; do not implement, generate, install, or promote. After human extraction approval and implementation, execute the contract in disposable fixtures as separate evidence.`  
handoff_note: `Presence is not behavior parity. Keep every proposed command explicitly marked future until its referenced executable and fixture exist. Resolver output remains candidate; authoritative selection belongs only to the retained owner.`

Verdict: typed no-witness `BLOCK`.

The authority terminology is correctly bounded in the synthesis: resolver output is consistently `candidate`, while human selection terminology occurs only downstream. The private name `selected-local` is identified as a compatibility mapper and excluded from automatic public extraction.

## Bounded repairs required

1. Add one exact future command block for the core JSON port. It must name the eventual runner, fixture directory, case IDs, and deterministic contract:
   - exit `0` only when every declared case passes;
   - stdout is exactly one canonical JSON summary or JSONL stream with a declared schema and exact case count;
   - stderr is exactly empty;
   - cases include candidate, ambiguous, no-match, invalid request, malformed JSON transport, malformed catalog, unsupported request/protocol version, and catalog/content digest mismatch;
   - expected disposition/reason codes and `authority_effect: none` are specified per case.
2. Add one exact future command block for the candidate public core:
   - invoke tests from the future canonical public Arcanum sigil path;
   - state an exact machine-readable summary;
   - include a private-identifier/import/path scan with an unambiguous success exit;
   - verify manifest/core/protocol versions and closure/fixture digests against expected values recorded by the fixture.
3. Add separate exact future commands for generated Codex and Claude wrappers:
   - invoke each installed wrapper’s actual entry point;
   - run the identical fixture manifest;
   - capture canonical stdout, stderr, and exit status;
   - compare response bytes and typed failure classifications;
   - define exact admitted wrapper differences;
   - cover disabled integration and pinned prior-version rollback with exact before/after digests.
4. Add an exact future command for the thin orchestrator adapter with a selected test command and exact count. It must inject capability denial, version/digest mismatch, disabled integration, timeout, unavailable executable, nonzero exit, multiple or oversized stdout, stderr-policy violations, and rollback mismatch.
5. Make no-launch assertions observable. For every blocked or failing case, require zero calls to workflow binding, Dispatch opening/appender, journal `dispatch-open`, compatibility fallback, and host spawn.
6. Replace “same failure classification” with a table mapping every case to exact disposition or adapter lifecycle state, exact reason/error code, exit code, stdout shape/limit, stderr rule, and launch-call count.

Until commands reference real executables and expected outputs are frozen, they remain future acceptance design—not current evidence.
