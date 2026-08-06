# Validation contracts

The normative future matrix is digest-bound to:

```text
research/2026-07-30-intent-router-bootstrap-runtime-integration/acceptance-contract-addendum.md
sha256 ae914daf71331ddc787d8b562d78ceddabd10ad2526b568de07ecd92f2707e94
```

It declares 78 logical cases:

| Surface | Cases | Required result |
|---|---:|---|
| JSON port | 13 | exact document count, bytes, exits, schemas, reasons |
| public core and scans | 8 | core pass, private-content/import pass, zero-authority and version/digest bindings |
| Codex wrapper | 15 | isolated generated-package behavior and rollback |
| Claude wrapper | 15 | corresponding behavior plus per-case Codex byte equality |
| orchestrator adapter | 27 | strict transport and zero-authority consumer boundary |

All commands require zero runner stderr. The adapter timeout is 5000 ms,
injected delay is 5001 ms, request ceiling is 262144 bytes, target stdout
ceiling is 1048576 bytes, and target stderr ceiling is zero.

## Evidence ladder

1. static candidate scan;
2. core/schema/fixture unit and metamorphic tests;
3. real Node and shared-Chromium portable witness;
4. selective generated-package parity in isolated roots;
5. disposable consumer install/disable/rollback;
6. independent orchestrator and private-admission witnesses.

Later evidence cannot backfill an earlier failed gate. Browser evidence proves
only the tested portable cases; it is not product acceptance.

