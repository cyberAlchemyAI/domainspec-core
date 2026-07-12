# SWU-IDEAD-007 Evidence

```yaml
swu_id: SWU-IDEAD-007
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: projects/ide-extension/development/l0-human-approval-desk-plan/work-pack/evidence/SWU-IDEAD-007.md
files_touched:
  - src/kernel/artifacts.mjs
  - src/envelopes/dry-run-envelope.mjs
  - src/kernel/projector.mjs
  - src/server.mjs
  - schemas/receipt.schema.json
  - tests/fixtures/schemas/receipt.valid.json
  - tests/fixtures/schemas/receipt.invalid-missing.json
  - tests/fixtures/schemas/receipt.invalid-type.json
  - tests/l0-artifact-evidence.test.mjs
  - tests/l0-persistence-recovery.test.mjs
  - package.json
validation:
  - npm run test:artifacts
  - npm run test:persistence
  - npm run test:adversarial
  - node --test --test-concurrency=1 tests/*.test.mjs
  - npm run validate:schemas
  - npm audit --audit-level=high
  - git diff --check
blockers: []
residue: []
reroute: SWU-IDEAD-008
handoff_note: Receipt responses expose before, after, and receipt artifact refs; every committed ref is contained, resolvable, and bound to the same run, envelope, approval, grants, and disposition.
```

## Stable Evidence API

- `evidenceArtifactIds({ run_id, approval_id })` derives deterministic before, after, and receipt artifact IDs from bound records.
- `writeArtifactRef()` uses exclusive `wx` creation, flushes the file handle, and refuses overwrite with `artifact_exists`.
- `resolveArtifactRef()` confines JSON refs to the configured artifact directory.
- `readArtifactRef()` rejects missing, malformed, non-regular, and symbolic-link artifact targets.
- `validateArtifactRef()` compares loaded artifact fields with expected bindings.
- `validateEvidenceRefs()` resolves source evidence inside a configured real filesystem root and rejects lexical or symbolic-link escape.
- Approval responses retain `artifact_ref` for compatibility and add `artifact_refs.before`, `artifact_refs.after`, and `artifact_refs.receipt` for UI consumption.

## Receipt Bindings

Every passed L0 receipt now binds:

- `receipt_id`, `run_id`, `envelope_id`, and `approval_id`;
- normalized `requested_grants`;
- `disposition: approved`, stage, and status;
- resolvable `before_ref` and `after_ref`;
- source-backed `evidence_refs`;
- `created_at`.

The before artifact contains pending envelope and approval records. The after artifact contains the proposed passed envelope and consumed approval. The receipt artifact contains the exact schema-validated receipt payload. All three files are re-read and binding-validated before the single authoritative `receipt.appended` event commits.

If source evidence or event append fails, no receipt becomes authoritative and existing files remain visible as orphan residue. Rejection writes neither a passed receipt nor evidence artifacts.

## Validation Results

| Command | Result |
| --- | --- |
| `npm run test:artifacts` | pass: 6/6 hostile and integration cases |
| `npm run test:persistence` | pass: 6/6, including three-orphan append interruption |
| `npm run test:adversarial` | pass: 8/8; AR-CAND-007 is green |
| all Node tests | pass: 48/48 |
| `npm run validate:schemas` | pass: 7 schemas, 6 manifests, 21 fixtures |
| `npm audit --audit-level=high` | pass: 0 vulnerabilities |
| syntax checks and `git diff --check` | pass |

No subagents or external runtime adapters were used. No experiment harness applies to this product SWU. This evidence does not claim cryptographic chaining, signatures, or generic tamper evidence.
