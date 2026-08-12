# Stage 04: Research Decision And Joined Specialist Synthesis

## Research Decision

- Policy: `research-if-gap-appears`
- Local named gaps: representation, canonicalization, projection receipts, authoring, admission, and migration
- Selected research: confirmed local read-only specialist wave
- External research: not triggered and not authorized
- Dispatch: `2026-08-06-ontology-vault-semantic-source-specialists`
- Native run: `20260806T215110Z-ontology-vault-semantic-source`
- Join policy: all
- Joined receipts: 3 of 3
- Deterministic gate: `g-specialist-wave = gate_pass`
- Ledger exit: `resolved`
- Verdict: `pass`

## Joined Evidence

| Role | Return | Status | Load-bearing contribution |
|---|---|---|---|
| semantic-source-schema-architect | `delegated-research/returns/semantic-source-schema-architect.md` | pass | Closed local package, five source schemas, stable identity, three digest domains, and fail-closed compatibility. |
| projection-authoring-architect | `delegated-research/returns/projection-authoring-architect.md` | pass | Complete human author journey, typed content blocks, semantic diffs, SourcePatch correction, ProjectionDefinition, and ProjectionReceipt fields. |
| governance-migration-adversary | `delegated-research/returns/governance-migration-adversary.md` | pass | Distinct package AdmissionRecord, owner table, copy-and-verify migration, rollback, public/private isolation, and authority negatives. |

These returns are admitted only as private refinement evidence. They do not
change the public Ontology Vault convention.

## Preserved Disagreements

### Authored representation

- Schema and governance lenses prefer closed JSON because it has the smallest
  closure, canonicalization, portability, and migration surface.
- The authoring lens prefers a strict YAML subset because long-form prose and
  review are easier.
- Both reject JSON-LD as the v1 authored source because locally frozen contexts,
  graph normalization, aliasing, and semantic diffs add unproven complexity.

### Schema suite granularity

- The seed proposed seven source schemas.
- The schema specialist found only five independently evolving source modules
  are earned in v1. Evidence and governance remain `$defs` in the record schema.
- Admission, migration, patch, and execution receipts are protocol/governance
  contracts outside the source SchemaSuite because they bind or transform a
  package rather than constitute its authored semantics.

## Parent Synthesis Decisions

### D1 — Closed JSON is the v1 admitted source encoding

Select closed JSON for the candidate v1 source package. The decision is not
that humans should hand-maintain JSON. It is that only one exact encoding is
eligible for package admission. Schema-guided forms, editors, and commands
produce typed `SourcePatch` operations against that source.

Strict typed YAML remains a rejected-for-v1 alternative, not a forbidden
future. It may be reconsidered only if finite authoring evidence shows the
form/patch route cannot retain humane long-form explanation. If later admitted,
YAML must become the sole authored source for that profile; canonical JSON must
remain derived. Two parallel editable sources are never permitted.

### D2 — JSON-LD is a projection, not the v1 source

Graph consumers may receive a locally generated JSON-LD or equivalent
`GraphView`. The projection is digest-bound and cannot become source or import
remote contexts.

### D3 — Use five schemas for the source package

The v1 `SchemaSuite` contains:

1. `semantic-package.schema.json`
2. `semantic-record.schema.json`
3. `semantic-relation.schema.json`
4. `semantic-projection-definition.schema.json`
5. exactly one ontology-type module, initially `knowledge-vault.schema.json`

Evidence and governance definitions remain reusable `$defs` inside
`semantic-record.schema.json` until independent lifecycle evidence earns a
split. Supporting protocol schemas remain separate:
`normalized-semantic-model`, `projection-receipt`, `source-patch`,
`admission-record`, `migration-map`, and `migration-receipt`.

### D4 — AdmissionRecord is distinct and external

`AdmissionRecord` is non-vacuous. It answers whether one exact package version
and digest is the owner-recognized source for a scope. `PromotionRecord` answers
whether one claim or relation may be relied upon at a lifecycle level.

The AdmissionRecord cannot live inside the package bytes it admits because that
would create a digest self-reference. It is an immutable, owner-issued sibling
governance record that binds package ID, version, canonical digest, suite
digest, scope, decision, compatibility posture, and rollback target.

### D5 — SourcePatch is the only correction bridge

A reader may select material in a generated view only because the projection
receipt maps it back to a stable source selector. The resulting correction is a
proposal with a base source digest and preconditions. It cannot directly write
back, admit, or promote anything.

### D6 — Migration is copy, verify, then owner cutover

Migration never overwrites the current admitted source in place. A total
`MigrationMap` classifies every prior identity as preserved, renamed, split,
merged, retired, or unresolved. Any unresolved, split, or merge ambiguity stays
typed residue and blocks cutover until an owner decides it. Rollback points to
retained exact pre-migration bytes.

## Current, Candidate, And Absent

| Concern | Current evidence | Candidate result | Still absent |
|---|---|---|---|
| Record/lifecycle/confidence axes | Existing Ontology Vault candidate work | Reused without collapse | Public adoption of full schema |
| Package source | None admitted | Closed local JSON SemanticPackage | Schema bytes and validators |
| Normalized model | None admitted | Deterministic disposable IR | Normalizer implementation |
| Human/graph/query views | Non-authority precedents only | ProjectionDefinition plus provenance-bearing outputs | Projectors and finite output fixtures |
| Admission | PromotionRecord exists for claims/relations | Separate external AdmissionRecord | Owner-approved schema and admission ledger |
| Authoring | No reusable contract | Schema-guided form/editor -> SourcePatch | Form generator, diff engine, patch applier |
| Migration | Required but absent | Total MigrationMap, receipt, copy-and-verify rollback | Migrator and legacy fixtures |

## Claim Ceiling And Reroute

This stage selects a candidate model for the remaining private Refine stages.
It does not establish canonical schemas, implementation, runtime behavior,
owner admission, public convention mutation, ontology promotion, migration, or
resolution of the paused RWO identity gate. Any public update must later route
through Ontology Vault convention-update and Sigil Development with explicit
owner approval.
