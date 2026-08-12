# TASK-OVSS-02 — Canonicalization And Normalization

- Layer/slice: L0; S-002
- Wave: W0
- Objective: derive stable canonical package and normalized-model bytes without creating a second source.
- Sources: Stage 06 `OV-CANON-JSON/v1` and `NormalizedSemanticModel v1`
- Dependencies: TASK-OVSS-01 complete
- Proposed write scope: `arcanum/arcana/ontology-vault/development/semantic-source-spine/src/canonicalization/`; `arcanum/arcana/ontology-vault/development/semantic-source-spine/src/normalization/`; `arcanum/arcana/ontology-vault/development/semantic-source-spine/fixtures/canonicalization/`; `arcanum/arcana/ontology-vault/development/semantic-source-spine/fixtures/normalization/`
- Current gate: blocked by B-004

## SWU-OVSS-004 — Canonical package bytes

- Primary behavior: compute exact and canonical source digests under the closed framing/profile.
- Acceptance boundary: identical values with formatting/key-order changes preserve canonical digest; duplicate keys, non-NFC, float numbers, set duplicates, or path drift fail.
- Split analysis: parser, canonical serializer, framing, and digest cannot independently satisfy the one canonicalization decision.
- Dependencies: SWU-OVSS-001–003.
- Source anchors: Stage 06 section 3.5.
- Write scope: canonicalization source and fixtures only.
- Done: two-run byte identity and every canonicalization negative have receipts.
- Validation: runtime-specific exact command requires B-004; byte comparisons and hashes are mandatory.
- Execution owner: Sigil Development-owned Task Session route.
- Handoff: no clock, host path, run ID, or silent Unicode rewriting in governed bytes.

## SWU-OVSS-005 — Disposable normalized model

- Primary behavior: flatten valid source records/relations into stable ID order and bind every input/tool digest.
- Acceptance boundary: repeated normalization is byte-identical; unknown/contradiction survive; submitted IR is rejected as source.
- Split analysis: flatten/order/bind/digest produce one independently accepted model artifact.
- Dependencies: SWU-OVSS-004.
- Source anchors: Stage 06 section 3.6.
- Write scope: normalization source and fixtures only.
- Done: model schema, positive fixture, formatting variant, unknown/contradiction fixture, and IR-as-source negative pass.
- Validation: exact command requires B-004.
- Execution owner: Sigil Development-owned Task Session route.
- Handoff: model is reproducible and disposable, never admitted.

## Synchronization

Only candidate development outputs. No source package is admitted and no
ProjectionReceipt is produced by this task.
