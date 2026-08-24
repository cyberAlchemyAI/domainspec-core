# TASK-OVSS-05 — Admission, Migration, Rollback, And Privacy

- Layer/slice: L2; S-005
- Wave: W2
- Objective: prove package-source owner decisions and reversible identity-preserving migration without private leakage.
- Sources: Stage 06 sections 3.10–3.11; Stage 08 R5/R6/R8
- Dependencies: W1 pass and explicit package-owner decisions
- Proposed write scope: `arcanum/arcana/ontology-vault/development/semantic-source-spine/src/governance/`; `arcanum/arcana/ontology-vault/development/semantic-source-spine/fixtures/migration/`; `arcanum/arcana/ontology-vault/development/semantic-source-spine/fixtures/private-boundary/`
- Current gate: blocked

## SWU-OVSS-009 — Owner transition proof

- Primary behavior: resolve immutable admission events and execute copy/verify migration with total identity map and retained rollback bytes.
- Acceptance boundary: exact admission/supersession/rollback succeeds; automatic admission, partial cutover, unresolved split/merge, overwritten rollback, and private leakage fail.
- Split analysis: admission resolver, migration engine, and leakage validator can pass independently. This SWU is task-shaped and must split before mutation-capable admission.
- Dependencies: W1 and owner-approved event/storage boundaries.
- Source anchors: Stage 08 R5/R6/R8 and T7–T10.
- Write scope: governance/migration/private-boundary candidate source and fixtures.
- Done: not eligible until split; later child SWUs need individual commands and receipts.
- Validation: blocked pending Plan refresh.
- Execution owner: Ontology Vault package owner plus Sigil Development.
- Handoff: migration tools propose; only owner events cut over.

## Synchronization

Private adopter material may be used only in private runs or synthetic/redacted
fixtures. Public schema/fixture/output scans must inspect all bytes and paths.
