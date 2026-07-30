# Traceability And Recomposition

| Finding | Spec | Implementation SWUs | Acceptance SWUs |
| --- | --- | --- | --- |
| CR-1 bounded scenes | `CAP-OFSP-01`, `AC-001/002` | 001, 005, 006, 010, 017 | 014, 015, 016, 022, 023 |
| CR-2 keyboard/focus | `CAP-OFSP-04`, `AC-004/007` | 007, 008, 011, 012, 013, 021 | 015, 016, 023 |
| CR-3 relation/pivot | `CAP-OFSP-02/03`, `AC-003/004` | 005, 008, 010, 012 | 014, 015, 016, 023 |
| CR-4 tour state | `CAP-OFSP-05`, `AC-005` | 018, 019 | 022, 023 |
| CR-5 source vocabulary/non-color | `CAP-OFSP-06`, `AC-006/007` | 005, 020, 021 | 022, 023 |
| Native ownership/build gap | integration/versioning | 002, 003, 004, ordered patches | 014, 022 |
| Degraded truthfulness | error contract | 024, 025 | VERIFY + audits |
| Evidence/claim ceiling | `CAP-OFSP-07`, `AC-008` | receipt schema, 015 | 016, 023, closure audits, 026 |

## Layer Recomposition

```text
L0 =
  001 oracle
  + 002-004 admitted tooling
  + 005-008 projection/state
  + 009-013 native scene/landmark/control/focus-motion
  + 014 verified build
  + 015 validator
  + 016 browser attempt

L1 = L0
  + 017 one-hop
  + 018 pure tour state
  + 019 tour bridge
  + 020 source literals
  + 021 forced-colors redundancy
  + 022 verified build
  + 023 browser regression

L2 = L1
  + 024 pure degraded policy
  + 025 rendered recovery
  + VERIFY
  + AUDIT-ALIGNMENT
  + AUDIT-LAYERING

L3 = L2 + 026 reproducible local handoff
```

This recomposition ends at a local structural prototype. It does not recompose
into ontology promotion, upstream acceptance, release, deployment, production,
or human comprehension.

