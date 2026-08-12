# Stage 06: Invoke Redefine / Design — Exact Candidate Model

## Invoke Result

- Mode: `design`
- Spell: `invoke`
- Capability: `invoke`
- Phase status: `flag`
- Design evidence state: `authored-complete`
- Evidence ceiling: candidate architecture only; no DesignScopeManifest/denominator/fixed-point validator receipt
- Plan evidence: pending
- Template/profile selection: DomainSpec six-view architecture baseline plus sigil-design companion
- Human semantic surface: present; a formal UX companion remains a downstream design-validation requirement
- Public mutation: none
- Authority effect: none
- Recommended next route inside Refine: `refine-design-review`

The flag does not mean the candidate is vague. It means an exact candidate is
authored while its schemas, fixtures, validator, and independent design
selection receipt do not yet exist.

## 1. Context View

### Problem

Ontology Vault currently has useful ontology-type, lifecycle, confidence,
relation, governance, and PromotionRecord work, but no reusable contract that
makes one machine package the source and every readable/operational view a
verifiable projection. Human documents can therefore drift toward parallel
truth, while a machine-first replacement could become hostile to authors or
collapse structural validity into authority.

### Selected outcome

```text
owner-authored closed JSON SemanticPackage
  -> SchemaSuite validation
  -> OV-CANON-JSON/v1
  -> deterministic NormalizedSemanticModel
  -> declared ProjectionCompiler
  -> HumanView | GraphView | QueryView
  -> ProjectionReceipt + ProjectionTrace

human correction
  -> SourcePatch against exact base digest
  -> owner-reviewed candidate source version

owner admission
  -> external immutable AdmissionRecord

claim/relation promotion
  -> existing one-primary-claim PromotionRecord boundary
```

### Actors and owners

| Actor/owner | Owns | Does not own |
|---|---|---|
| Ontology author | Draft source content and SourcePatch proposals | Admission, promotion, public convention mutation |
| Package owner | Source-version acceptance and AdmissionRecord | Automatic truth or promotion of contained claims |
| SchemaSuite validator | Structural/cross-field evidence | Truth, owner decision, normalization authority |
| Normalizer | Reproducible disposable IR | Authored source or semantic decision |
| Projection compiler | Declared read models | New semantic claims or writeback |
| Reviewer | Semantic review and correction proposals | Direct generated-view mutation |
| Claim/relation review owner | PromotionRecord decision for one primary item | Whole-package admission |
| Ontology Vault lifecycle owner | Reusable public convention | Private adopter meaning |
| Sigil Development | Later capability lifecycle mutation and validation | Automatic owner approval or promotion |
| Inventory | Discovery handles and projection precedent | Authority or public convention validation |

## 2. High-Level Structure View

```text
SOURCE PLANE                    DERIVED PLANE
┌──────────────────────┐       ┌──────────────────────────┐
│ SemanticPackage      │       │ NormalizedSemanticModel  │
│ manifest + modules   │──────▶│ stable records/relations │
└──────────┬───────────┘       └────────────┬─────────────┘
           │                                │
┌──────────▼───────────┐       ┌────────────▼─────────────┐
│ SchemaSuite          │       │ ProjectionCompiler       │
│ core + type module   │       │ definition + template    │
└──────────────────────┘       └──────┬─────────┬─────────┘
                                      │         │
                              ┌───────▼───┐ ┌───▼─────────┐
                              │ HumanView│ │Graph/QueryView│
                              └───────┬───┘ └───┬─────────┘
                                      └────┬────┘
                                           ▼
                                  ProjectionReceipt
                                  + ProjectionTrace

PROPOSAL PLANE                   GOVERNANCE PLANE
┌──────────────────────┐        ┌──────────────────────────┐
│ SourcePatch          │        │ AdmissionRecord          │
│ base digest + ops    │        │ package-version decision │
└──────────────────────┘        └──────────────────────────┘
┌──────────────────────┐        ┌──────────────────────────┐
│ MigrationMap/Receipt │        │ PromotionRecord          │
│ copy/verify/rollback │        │ one claim/relation       │
└──────────────────────┘        └──────────────────────────┘
```

Only the Source Plane is authored ontology source. Derived artifacts are
reproducible read models. Proposal artifacts ask for source changes. Governance
records bind owner decisions and never arise automatically from compilation.

## 3. Low-Level Component View

### 3.1 SemanticPackage v1

Physical layout:

```text
<package>/
  manifest.json
  records/*.json
  relations/*.json
  projections/*.json
```

All referenced paths are normalized package-relative paths. `..`, absolute
paths, symlinks, remote imports, remote contexts, undeclared modules, and
implicit semantic endpoints are rejected.

#### Manifest fields

| Field | Type | Rule |
|---|---|---|
| `format_id` | const | `arcanum.ontology-vault.semantic-package/v1` |
| `package_id` | stable ID | Owner assigned; never title, position, or content hash derived |
| `package_version` | version | Identifies this authored version; compatibility still binds digests |
| `namespace` | stable string | Closed local namespace for semantic IDs |
| `ontology_type` | catalog ID | Exactly one primary type; v1 proof uses `knowledge-vault` |
| `owner_ref` | owner handle | Names proposed package owner; does not self-admit |
| `source_posture` | enum | `draft` or `candidate`; `admitted` is forbidden here |
| `schema_suite` | ref tuple | Suite ID, version, and exact aggregate digest |
| `canonicalization_profile` | ref tuple | `OV-CANON-JSON/v1`, version, implementation-neutral digest |
| `modules[]` | closed inventory | Module ID, normalized path, kind, schema ref, exact bytes digest |
| `projection_definition_refs[]` | stable refs | Optional authored projection declarations |
| `extension_schema_refs[]` | local digest refs | Optional namespaced profiles; no undeclared keys |

Closure rules:

- every semantic record and relation occurs in exactly one declared module;
- IDs are globally unique within the package namespace;
- every relation endpoint resolves to exactly one local record;
- the manifest lists every semantic and projection module exactly once;
- external evidence may be referenced as opaque typed evidence, but external
  semantic graph endpoints are deferred from v1;
- source validity never implies an AdmissionRecord or PromotionRecord result.

### 3.2 Source SchemaSuite v1

| Schema | Owns | Does not own |
|---|---|---|
| `semantic-package.schema.json` | manifest, module closure inputs, suite/profile refs | records, admission |
| `semantic-record.schema.json` | record shape, lifecycle/confidence axes, content, evidence/governance `$defs` | package admission |
| `semantic-relation.schema.json` | relation identity, endpoints, type, direction, lifecycle, evidence | external endpoint resolution |
| `semantic-projection-definition.schema.json` | bounded projection declaration | execution receipt or output authority |
| `knowledge-vault.schema.json` | selected type constraints and allowed record/relation combinations | other ontology types |

Evidence and governance stay `$defs` inside the record schema for v1. A later
split requires observed cross-record reuse or independent lifecycle/versioning.

Supporting protocol/governance schemas are outside the source suite:

- `normalized-semantic-model.schema.json`
- `projection-receipt.schema.json`
- `projection-trace.schema.json`
- `source-patch.schema.json`
- `admission-record.schema.json`
- `migration-map.schema.json`
- `migration-receipt.schema.json`

### 3.3 SemanticRecord v1

Required core:

- `record_id`, `record_kind`, `title`
- `lifecycle_status`, `claim_role`, `governance_outcome`
- `confidence.evidence`, `confidence.commitment`, and rationale
- typed `content` with `claim`, `definition`, `purpose`, rationale blocks,
  examples, non-examples, and notes where applicable
- evidence references with immutable identity, selector, role, proof posture,
  provenance, and counterevidence
- typed blockers/residue
- optional namespaced extensions declared by the manifest

Long-form content uses stable blocks:

```json
{
  "format": "plain-text/v1",
  "blocks": [
    {"block_id": "rationale-source-view-split", "text": "..."}
  ]
}
```

V1 uses plain text plus explicit lists/blocks. A rich-text or CommonMark subset
requires a later parser/rendering profile and fixtures. Block IDs are patch and
projection anchors; array position is not identity.

Typed absence:

- unsupported evidence: `confidence.evidence = "unknown"` plus a blocker;
- contradiction: preserve claim and counterevidence with the existing
  contradicted lifecycle/governance vocabulary;
- deferred: explicit lifecycle state plus owner-routed blocker;
- missing fields never synthesize positive support.

### 3.4 SemanticRelation v1

Required:

- `relation_id`, `relation_type`, `from_id`, `to_id`, `direction`
- evidence refs and confidence where the type requires them
- lifecycle state, branch/profile constraints, and optional cycle policy

Validation rejects missing endpoints, type-disallowed endpoint kinds, duplicate
IDs, forbidden cycles, and relations not permitted by the selected ontology
type module. Presentation order cannot create relation identity.

### 3.5 OV-CANON-JSON/v1

Input: exact `manifest.json` plus every declared module byte sequence.

Validation before canonicalization rejects non-UTF-8, BOM, duplicate keys,
non-NFC strings, unknown properties outside declared extensions, non-integer
JSON numbers, undeclared paths, path traversal, remote refs, duplicate IDs, and
unresolved endpoints. Decimal quantities use schema-constrained canonical
strings rather than implementation-dependent JSON floats.

Canonical value rules:

1. Parse with duplicate-key rejection.
2. Require strings already normalized to Unicode NFC; do not silently rewrite.
3. Sort object keys by Unicode code point.
4. Serialize UTF-8 with minimal JSON escaping and no insignificant whitespace.
5. Preserve schema-declared sequence arrays.
6. Sort schema-declared set arrays by their explicit stable key and reject
   duplicate keys.
7. Represent display order as explicit data; display order never creates ID.
8. Serialize without clock, run ID, host path, or final newline variability.

Canonical package framing:

```text
bytes("OV-PACKAGE-CANON/v1\0")
for each canonical path in normalized-path order:
  u32be(path_byte_length) || path_utf8 ||
  u64be(canonical_content_byte_length) || canonical_content_bytes
```

Digest domains:

| Digest | Binds |
|---|---|
| `exact_source_digest` | Same framing over exact declared source bytes |
| `canonical_source_digest` | Canonical framed semantic package bytes |
| `schema_suite_digest` | Ordered schema IDs, versions, paths, and exact bytes digests |
| `normalized_model_digest` | Normalized model bytes plus source, suite, profile, and normalizer identities |
| `projection_definition_digest` | Exact canonical ProjectionDefinition |
| `compiler_digest` | Projector executable/source artifact identified by the owner contract |
| `template_digest` | Exact non-semantic template bytes |
| `projection_trace_digest` | Emission provenance map |
| `output_digest` | Exact generated output bytes |

No aggregate “build digest” replaces these domains.

### 3.6 NormalizedSemanticModel v1

The model contains:

- package identity and all input digests;
- records keyed and emitted in `record_id` order;
- relations keyed and emitted in `relation_id` order;
- explicit display-order fields retained as values;
- preserved unknown, contradiction, blockers, and residue;
- no runtime timestamps or host paths in governed bytes.

It is deterministic, content-addressed, reproducible, and disposable. Editing,
admitting, or treating it as a fallback source is invalid.

### 3.7 ProjectionDefinition v1

Required fields:

- `projection_id`, schema version, `projection_kind`
- `audience`, `purpose`
- compatible exact normalized-model schema
- `renderer_id`, `renderer_version`, renderer digest
- record/relation selection and filters
- stable ordering keys and deterministic tie-breakers
- field mapping to sections/nodes/edges/query columns
- `template_id` and template digest
- unknown, contradiction, omission, reference, escaping, and serialization policies
- output format/media type and package-relative target
- `invented_claim_policy: "reject"`
- `writeback_posture: "forbidden"`
- generated/non-authority banner requirements

V1 graph projections may copy typed source relations but may not infer new
semantic edges. Inference rules require a later explicitly owned contract.

### 3.8 ProjectionTrace and ProjectionReceipt v1

Every semantic emission records:

- `emission_id`
- output selector or stable anchor
- source record/field/block/relation selectors
- `emission_kind: semantic | structural`
- emitted text/value digest

Structural headings and layout may originate in a template. A semantic emission
must trace to normalized source selectors. An untraced semantic emission or a
source state rewritten as a stronger state is an invented-claim failure.

Receipt fields:

- receipt/schema ID and result
- package ID/version; exact and canonical source digests
- suite module refs/digests and aggregate digest
- canonicalization and normalizer identities/digests
- normalized-model digest
- projection definition, compiler, and template identities/digests
- resolved selection, ordering, filters, and output profile
- trace digest
- output path, media type, byte size, and digest
- warnings, omissions, unknowns, contradictions, diagnostics
- invented-claim, writeback-posture, and reproducibility results

Operational `run_id`, `started_at`, and `finished_at` may live in a receipt
envelope but are excluded from governed deterministic output bytes.

### 3.9 SourcePatch v1

Required envelope:

- `patch_id`, author, rationale
- package ID/version and `base_canonical_source_digest`
- ordered operations
- expected candidate version
- validation posture and unresolved conflicts

Closed operations:

- `add_record`, `remove_record`, `replace_field`
- `add_relation`, `remove_relation`
- `replace_content_block`
- `reorder_display`

Every operation uses a stable semantic selector and an old-value/precondition
digest. Applying a patch creates a candidate source version. It never produces
admission or promotion. A generated-view selection can draft a patch only when
its receipt and trace resolve to an exact source selector.

### 3.10 AdmissionRecord and PromotionRecord

`AdmissionRecord` is external to the package it binds. Required fields:

- `admission_id`, immutable record version
- package ID/version
- exact and canonical source digests
- schema-suite and canonicalization-profile digests
- named package owner and admission scope
- decision: `admit | reject | revoke | supersede`
- compatibility state and supporting receipt refs
- rationale, gate result, decided-at time
- previous admission and exact rollback target

Only the package owner can issue it. Validators, normalizers, compilers, and
migration tools cannot. It does not assert every contained claim is true or
promoted.

`PromotionRecord` retains its existing one-primary-claim or one-primary-relation
boundary. It may reference an admitted package/record identity, but cannot admit
the package or aggregate unrelated claims.

### 3.11 Compatibility and migration

Closed compatibility states:

- `exact`
- `read-compatible`
- `migration-required`
- `partial-with-residue`
- `incompatible`
- `unknown`

`read-compatible` permits explicitly bounded inspection/preview but not new
admission. Admission targets exact suite/profile digests; migration must
materialize and verify that exact target.

`MigrationMap` binds old/new package and schema versions/digests and classifies
every old identity as `preserved`, `renamed`, `split`, `merged`, `retired`, or
`unresolved`. Split/merge never implies identity automatically. `MigrationReceipt`
binds tool/version/digest, inputs, candidate outputs, validation, residue,
pre-migration snapshot, and rollback target. Migration is copy-and-verify; only
the adopter/package owner can cut over. Partial or unknown residue blocks cutover.

## 4. Workflow Process View

### Author and review workflow

1. Load the exact admitted or draft package plus SchemaSuite.
2. Derive a field catalog from the schemas. An optional tool-owned
   `AuthoringProfile` may control labels/layout but cannot change semantics.
3. A form/editor creates a SourcePatch against the exact base digest.
4. Apply the patch into an isolated draft candidate.
5. Validate closure, schemas, cross-field rules, and stable IDs.
6. Canonicalize and normalize.
7. Compile preview HumanView/GraphView and receipts.
8. Show a semantic diff keyed by record/relation/block ID; show formatting-only
   changes separately.
9. Reviewer accepts, rejects, or revises the patch. Invalid drafts and diagnostics
   remain recoverable; the last admitted source is untouched.
10. Package owner may issue an AdmissionRecord for the exact candidate bytes.
11. Claim/relation promotion, when needed, uses separate PromotionRecords.

### Generated-view correction

1. Resolve the selected output fragment through ProjectionTrace.
2. Confirm receipt digests match current package/compiler/template/output.
3. Draft a SourcePatch with exact selector and precondition.
4. Return to the ordinary owner review flow.

Direct view writeback is never a workflow branch.

### Migration workflow

1. Retain exact prior admitted bytes and AdmissionRecord.
2. Compute a total MigrationMap into a separate candidate directory.
3. Validate IDs, schemas, relations, projections, private-boundary fixtures, and
   rollback target.
4. Keep partial output as typed residue if any identity is unresolved.
5. Package owner decides cutover by issuing a new AdmissionRecord.
6. Rollback re-admits the retained prior bytes; it does not reconstruct them.

## 5. Decision Flow View

```text
Package bytes present?
  no  -> block
  yes -> exact declared module closure?
           no  -> invalid draft, preserve diagnostics
           yes -> source schemas and cross-field rules pass?
                    no  -> invalid draft, no governed projection
                    yes -> canonicalize and normalize reproducibly?
                             no  -> compiler/canonicalization block
                             yes -> projection definition exact and local?
                                      no  -> projection block
                                      yes -> output reproducible and every
                                             semantic emission traceable?
                                               no  -> invented/drift block
                                               yes -> derived view valid

Derived view valid?
  yes -> evidence only
  owner AdmissionRecord for exact package exists?
    no  -> package remains non-admitted
    yes -> package is admitted for that scope only

Claim/relation use requested?
  -> evaluate its own lifecycle/evidence/PromotionRecord owner gate
```

No branch converts validation, normalization, or projection success into an
owner decision.

## 6. Dependency And Interface View

| Producer | Interface | Consumer | Gate |
|---|---|---|---|
| Ontology authoring tool | SourcePatch v1 | Package owner/draft applier | Exact base digest and preconditions |
| SemanticPackage | Package v1 | SchemaSuite validator | Closed local module inventory |
| SchemaSuite validator | Validation report | Normalizer and reviewer | Structural pass only; no authority |
| Canonicalizer | canonical source bytes/digest | Normalizer, AdmissionRecord | Profile and suite digest exact |
| Normalizer | NormalizedSemanticModel | Projectors/query tools | Disposable, source-bound IR |
| Projection compiler | View, Trace, Receipt | Readers/reviewers/tools | Reproducible; no invented emissions |
| Reader correction UI | source selector proposal | SourcePatch builder | Current receipt/trace required |
| Migration tool | candidate package, Map, Receipt | Adopter/package owner | Copy-and-verify; residue closed |
| Package owner | AdmissionRecord | Package resolver | External immutable owner decision |
| Claim review owner | PromotionRecord | Operational consumers | One primary item and existing lifecycle gates |
| Inventory | source handles | Context selection | Discovery-only, never authority |
| Ontology Vault | public contract candidate | Sigil Development | Later approval before mutation |
| Private adopter/RWO | private profile/package | Its own owner route | No public leakage; paused RWO identity gate untouched |

## Ontology Delta

Candidate node kinds:

| Node kind | Identity/cardinality | Authority posture |
|---|---|---|
| `semantic_package_version` | One node per package ID/version/canonical digest | Source candidate; external admission required |
| `semantic_module` | Exactly one package membership | Authored source component |
| `schema_suite` / `schema_module` | One exact suite per package version; five source modules in v1 | Structural contract only |
| `semantic_record` | Stable owner ID, exactly one source module | Meaning-bearing source record |
| `semantic_relation` | Stable relation ID, exactly two resolved endpoints | Meaning-bearing source relation |
| `projection_definition` | Stable ID, source-owned declaration | Declares a read model, no authority |
| `normalized_model` | Exactly one source/package/suite/normalizer binding | Derived disposable IR |
| `derived_view` | Exactly one model and definition per output | Non-authority projection |
| `projection_receipt` / `projection_trace` | Exactly one execution/output binding | Execution evidence only |
| `source_patch` | Exactly one base package digest | Proposal only |
| `admission_record` | Exactly one package version/digest and owner decision | Package-source authority for stated scope |
| `promotion_record` | Exactly one primary claim or relation | Item lifecycle authority only |
| `migration_map` / `migration_receipt` | Exactly one old/new transition | Migration evidence; owner cutover separate |
| `authoring_profile` | Tool-owned schema/UI profile | Non-semantic ergonomics configuration |

Candidate relation kinds:

| Relation | Domain -> range | Cardinality/invariant |
|---|---|---|
| `includes_module` | package -> module | one-or-more; module has one package |
| `constrained_by_suite` | package -> suite | exactly one exact digest |
| `contains_record` | module -> record | record has exactly one source module |
| `contains_relation` | module -> relation | relation has exactly one source module |
| `from_endpoint` / `to_endpoint` | relation -> record | exactly one each; local and type-valid |
| `declares_projection` | package -> definition | zero-or-more stable refs |
| `normalizes_to` | package version -> normalized model | derived; model cannot reverse-own source |
| `projects_to` | model -> derived view | view also requires exactly one definition |
| `evidenced_by_projection_receipt` | view -> receipt | one receipt per governed execution |
| `traced_by` | view -> projection trace | semantic emissions must be covered |
| `proposes_patch_to` | patch -> package version | exactly one base digest; no write authority |
| `admits_package_version` | admission record -> package version | one exact digest and scope |
| `promotes_item` | promotion record -> record/relation | exactly one primary target |
| `migrates_from` / `migrates_to` | map -> package version | one old and one candidate target |
| `supersedes_admission` | admission -> admission | acyclic immutable chain |

Prohibited relations:

- normalized model `is_source_for` package;
- derived view `writes_back_to` package;
- validation receipt `admits` or `promotes` anything;
- package `self_admits`;
- package-level PromotionRecord targets every contained item;
- public schema `imports_private_profile_semantics`;
- this candidate `resolves` the paused RWO ontology identity decision.

## Candidate Queries

1. Which derived views are stale for the current admitted package digest?
2. Which semantic emissions have no source selector in their trace?
3. Which package versions are structurally valid but lack an AdmissionRecord?
4. Which promoted items do not belong to an admitted package version?
5. Which relation endpoints are missing or type-invalid?
6. Which migrations contain split, merge, retired, or unresolved identities?
7. Which private extension namespaces occur in reusable public schema/fixture paths?
8. Which source patches target a stale base digest?

## Planned Witness Contract

Positive:

- single- and multi-module packages normalize deterministically;
- Markdown and graph/query outputs share source/model digests but have distinct
  definition/output digests;
- formatting-only JSON changes alter exact-source but not canonical-source digest;
- view correction maps to a SourcePatch selector;
- total ID-preserving migration can be verified and rolled back.

Negative:

- duplicate IDs, missing/type-invalid endpoints, undeclared modules, remote refs;
- source/suite/compiler/template drift;
- timestamp or nondeterministic order in governed output;
- invented promotion/support claim in a view;
- direct view writeback;
- schema-valid package without owner admission;
- automatic AdmissionRecord after compilation;
- partial migration cutover;
- private vocabulary leakage into public schema/fixture;
- normalized IR submitted as source;
- RWO gate inference from this result.

All witnesses are planned and unexecuted.

## Design Decisions And Rejected Alternatives

| Decision | Selected | Rejected/deferred |
|---|---|---|
| Source representation | Closed JSON v1 | JSON-LD source rejected; strict YAML deferred pending authoring evidence |
| Human authoring | Schema-guided forms/editors -> SourcePatch | Hand-maintained parallel Markdown or direct view writeback |
| Schema composition | Five source schemas plus separate protocol schemas | One mega-schema; seven independently versioned v1 source schemas |
| Admission | External immutable AdmissionRecord | Mutable package flag; package-level PromotionRecord |
| IR | Deterministic disposable model | Independently authored or admitted IR |
| Graph | Derived projection | Remote/context-driven source graph |
| IDs | Owner-assigned stable IDs | Position-, title-, or content-hash-derived IDs |
| Migration | Copy, total map, verify, owner cutover, rollback | Destructive in-place or partial warning-based cutover |

## Risks And Open Design-Validation Gaps

- JSON form/editor usability is designed but not witnessed with natural users.
- `plain-text/v1` may be too weak for rich explanation; widening it needs its own parser/profile evidence.
- Projection non-invention requires a real trace validator, not receipt prose.
- Schema annotations for set/sequence arrays and form generation require exact bytes and fixtures.
- AdmissionRecord storage/resolution owner is conceptually separated but not implemented.
- No DesignScopeManifest, denominator extraction, selection fixed-point receipt,
  formal UX plan, or executed witness currently exists.

## Distill Design-Unit Check

The coherent design unit is the source-to-view-to-patch kernel. It cannot split
before the HumanView because that loses the user outcome, and it cannot split
before SourcePatch because generated-view correction would remain undefined.
Admission implementation, graph/query parity, migration, and lifecycle
integration remain later layers. Verdict: `pass` for candidate unit selection;
design evidence remains `authored-complete` only.

## Claim Ceiling

This artifact is an exact candidate architecture in a private refinement run.
It is not a public Ontology Vault convention, canonical schema, generated skill
update, implemented compiler, validated UX, admitted ontology, promoted meaning,
migration approval, release, deployment, production proof, or RWO decision.
