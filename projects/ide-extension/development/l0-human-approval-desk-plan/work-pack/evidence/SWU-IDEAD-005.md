# SWU-IDEAD-005 Evidence

```yaml
swu_id: SWU-IDEAD-005
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: projects/ide-extension/development/l0-human-approval-desk-plan/work-pack/evidence/SWU-IDEAD-005.md
validation:
  - npm run validate:schemas
  - npm run test:schemas
  - npm run test:runtime-schemas
  - node --test --test-concurrency=1 tests/l0-lifecycle.test.mjs tests/l0-grants-disposition.test.mjs tests/l0-smoke.test.mjs
  - npm run test:adversarial
blockers: []
residue:
  - AR-CAND-007 remains red and is owned by SWU-IDEAD-007.
reroute: SWU-IDEAD-006
handoff_note: Runtime ingress and emitted records now validate before durable writes; server readiness rejects invalid shipped manifests.
```

## Boundary Evidence

- Seven Draft 2020-12 schemas compile through the shared cached Ajv adapter.
- Six shipped module manifests and twenty-one valid/hostile fixtures pass the executable validation contract.
- Malformed prepare, approve, and reject payloads return `400 invalid_request` without state, event, receipt, or artifact writes.
- Closed-grant policy runs after request-shape validation and rejects unknown grants before envelope creation.
- Prepared, consumed, and rejected envelope/approval records validate before state or event persistence.
- Approval receipts validate before before-state or receipt artifacts are written.
- A tampered emitted approval fails closed with the workbench preserved byte-for-byte, one existing event, and no artifact directory.
- Server readiness rejects a schema-invalid shipped manifest before the HTTP server listens.

## Validation Results

| Command | Result |
| --- | --- |
| `npm run validate:schemas` | pass: 7 schemas, 6 manifests, 21 fixtures |
| `npm run test:schemas` | pass: 6/6 |
| `npm run test:runtime-schemas` | pass: 6/6 |
| focused lifecycle, grant/disposition, and smoke tests | pass: 16/16 |
| `npm run test:adversarial` | flag: 7/8 pass; AR-CAND-008 passes; expected AR-CAND-007 remains red |

No subagents or external runtime adapters were used. No experiment harness applies to this product SWU.
