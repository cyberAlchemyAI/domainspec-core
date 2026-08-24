# TASK-OVSS-01 — Source And Protocol Schemas

- Layer/slice: L0; S-001
- Wave: W0
- Objective: make package closure, conditional semantic families, and protocol objects structurally discriminating.
- Source contracts: `../../../stages/06-invoke-design.md` sections 3.1–3.4; `../../../stages/08-distill-repair.md` R1–R2
- Dependencies: B-001 and B-003 resolved before mutation
- Proposed write scope: `arcanum/arcana/ontology-vault/development/semantic-source-spine/schemas/`; `arcanum/arcana/ontology-vault/development/semantic-source-spine/fixtures/schema/`
- Current gate: blocked

## Smallest Working Units

### SWU-OVSS-001 — Closed package inventory

- Primary behavior: accept exactly locally closed declared package modules and reject path/import/reference escape.
- Acceptance boundary: single/multi-module positives pass; undeclared module, `..`, absolute path, symlink, remote ref/context, and digest mismatch each fail distinctly.
- Split analysis: schema and fixtures cannot prove the behavior independently; retain together.
- Dependencies: none after blockers.
- Source anchors: Stage 06 `SemanticPackage v1`; Stage 08 R1.
- Related context: current Ontology Vault schemas are build-from-owned but not this package contract.
- Write scope: package schema plus package-closure fixtures only.
- Done: schema bytes, validator entry, positive/negative fixtures, and result receipt exist.
- Validation: exact command blocked by B-004; later route must parse every JSON and run one isolated case per closure invariant.
- Execution owner: Sigil Development-owned Task Session route.
- Handoff: do not add record semantics, canonicalization, projections, admission, or public root mutation.

### SWU-OVSS-002 — Conditional record/relation/type validation

- Primary behavior: discriminate record families and validate stable IDs plus local relation endpoints under `knowledge-vault` constraints.
- Acceptance boundary: valid family/endpoint cases pass; unknown family, inapplicable axis, duplicate ID, missing/type-invalid endpoint, and forbidden relation fail separately.
- Split analysis: record, relation, and ontology-type constraints jointly own the endpoint/type decision; if validator boundaries become independently releasable, split in Plan refresh.
- Dependencies: SWU-OVSS-001.
- Source anchors: Stage 06 `SemanticRecord v1` and `SemanticRelation v1`; Stage 08 R2.
- Write scope: record, relation, knowledge-vault schemas and their fixtures only.
- Done: conditional families are closed and relation source is standalone only.
- Validation: exact command blocked by B-004; fixture matrix is mandatory.
- Execution owner: Sigil Development-owned Task Session route.
- Handoff: reuse existing axes without making every axis universal.

### SWU-OVSS-003 — Protocol object schemas

- Primary behavior: validate inter-object bindings for normalized model, projection definition/trace/receipt, SourcePatch, admission events, MigrationMap, and MigrationReceipt.
- Acceptance boundary: every protocol object binds the exact subject digests/IDs it claims; self-admission and view writeback shapes are unrepresentable.
- Split analysis: candidate children are projection, patch, admission, and migration schema sets; they can become independent and must be split before execution if one subset is selected alone.
- Dependencies: SWU-OVSS-002.
- Source anchors: Stage 06 sections 3.6–3.11; Stage 08 R3–R8.
- Write scope: protocol schemas and protocol fixtures only.
- Done: positive/negative bindings exist with no authority-collapse field.
- Validation: exact command blocked by B-004.
- Execution owner: Sigil Development-owned Task Session route.
- Handoff: preserve `PromotionRecord` as one-item authority; do not redefine it.

## Synchronization

No public convention or generated skill mirror changes. Completion evidence is
candidate-development schema/fixture receipts only.
