# Specialist Return: Semantic Source Schema Architect

## 1. Source selectors and observed facts

### Observed source facts

- `REFINE-SEED-PROPOSAL.md` — **Fixed Direction And Claim Ceiling**, **Candidate Layer Model To Test**, **Required Invariants**
  - The confirmed direction is one owner-admitted machine semantic source followed by validation, deterministic normalization, and derived views.
  - Parsing, schema validity, normalization, and projection do not confer authority or promotion.
  - Stable IDs must not depend on file position or presentation order.
  - Unknown, contradictory, unsupported, and deferred states must remain typed.
  - Migration must preserve IDs or emit explicit identity maps.
- `REFINE-SEED-PROPOSAL.md` — **Candidate Schema Suite**, **Representation Alternatives**
  - The seed proposes modular package, record, relation, evidence, governance, projection, and ontology-type constraints.
  - Closed JSON, locally constrained JSON-LD, and typed authoring compiled to canonical JSON are explicitly open alternatives.
- `stages/01-context-pack.json` — obligations `O1`–`O9`, gaps `G1`–`G3`
  - Existing entry, lifecycle, confidence, relation, and `PromotionRecord` work is build-from-owned.
  - Representation selection, projection contract, and migration contract are deferred research gaps.
  - Canonical Ontology Vault sources outrank development candidates and private pressure evidence.
- `stages/02-invoke-define.md` — **Inputs**, **Outputs**, **Functional Requirements**, **Definition-Scope Distill Sanity**
  - The smallest previously identified unit is the semantic-source spine, not one universal schema.
  - `NormalizedSemanticModel` is derived and must not be independently authored.
  - Schema modules must be closed and digest-bound.
  - Owner admission and `PromotionRecord` decisions remain separate.
- `stages/03-interrogation.md` — **Fixed Decisions**, research question `R1`
  - Source/view direction is fixed.
  - Representation, canonicalization, rich-text storage, migration, and `AdmissionRecord` overlap remain unresolved evidence questions.
- `arcanum/arcana/ontology-vault/SKILL.md` — **ontology-type-arguments**, **Step 5**, **quality-bar**
  - The selected job is `knowledge-vault`; no branch scope is implied.
  - Convention changes require current/proposed rules, rationale, migration impact, affected files, and rollback.
  - Delegated findings are evidence, not authority.
- `catalogs/ontology-types.json` — `knowledge-vault`
  - The cataloged focus includes knowledge roles, maturity, evidence and commitment confidence, premises, delegated evidence, and conventions.
- `GOVERNED-CANDIDATE-BUNDLE.md` — **Published Candidate Boundaries**, **Current Candidate Model**
  - `promotion_record` is canonical only as the Ontology Vault governance decision record-kind.
  - The full entry schema, JSON Schema, profiles, and templates remain candidate or deferred.
  - Existing axes are `record_kind`, `lifecycle_status`, `claim_role`, `governance_outcome`, and `bridge_outcome`.
- `BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md` — **Entry Schema**, **Relation Schema**, validations `V4`, `V8`, `V9`, `V11`–`V13`
  - The candidate already supplies entry fields, embedded edges, evidence pointers, split confidence, governance state, typed unknown/contradiction outcomes, endpoint targets, and promotion constraints.
  - Embedded relations and standalone bridge entries have distinct existing uses.
  - The full schema remains non-canonical.

### Inference boundary

The package shape, canonicalization algorithm, compatibility states, digest domains, and representation recommendation below are specialist proposals. They are not observed current conventions.

## 2. Candidate recommendation

Select **closed JSON as the v1 admitted authored representation**.

The smallest closed source is:

```text
SemanticPackage
├── manifest.json
├── records/*.json
└── projections/*.json       optional declarations, still source
```

All paths are package-relative. V1 permits no remote schema, context, import, or semantic endpoint resolution. External evidence remains an opaque, typed evidence reference, not a graph endpoint.

### `SemanticPackage` manifest

Minimum candidate fields:

```text
format_id
package_id
package_version
namespace
ontology_type
owner_ref
source_posture
schema_suite { suite_id, version, digest }
canonicalization_profile { profile_id, version, digest }
compatibility { reader_state, target_schema_version }
modules[] {
  module_id,
  path,
  media_type,
  schema_ref,
  exact_bytes_digest
}
projection_definition_refs[]
```

Rules:

- `package_id`, module IDs, record IDs, and relation IDs are explicit owner-assigned identities.
- IDs do not contain file offsets, array positions, titles, or content digests.
- Module paths are normalized, unique, local, and exhaustively listed.
- Every semantic record occurs in exactly one listed module.
- Cross-module record IDs are globally unique in the package.
- Every relation endpoint resolves to exactly one record in the closed package.
- External semantic relations are deferred from v1; introducing pinned package dependencies requires a later compatibility design.

### Smallest `SchemaSuite`

Use five composed schemas, not the seed’s seven independently versioned schemas:

1. `semantic-package.schema`
2. `semantic-record.schema`
3. `semantic-relation.schema`
4. `semantic-projection-definition.schema`
5. exactly one ontology-type constraint module, initially `knowledge-vault.schema`

Keep evidence and governance as named `$defs` within `semantic-record.schema` for v1. Current evidence and governance fields are record-owned and do not yet prove an independently identified module lifecycle. Split them later only if cross-record reuse, independent versioning, or fixtures demonstrate distinct ownership.

Reuse the existing candidate record fields and axis separation. Add only:

- explicit `relation_id` to each embedded edge;
- `display_order`, where presentation order is intentional;
- namespaced extensions declared by the manifest and validated by digest-bound local schemas.

Unknown and residue use existing axes rather than a new truth field:

- unsupported/unknown evidence: `confidence.evidence: unknown` plus a promotion blocker;
- contradiction: preserved claim, counterevidence, `lifecycle_status: contradicted`, and typed contradiction role/outcome;
- deferred work: `lifecycle_status: deferred` plus owner-routed blocker;
- absence never synthesizes a positive value.

### Canonicalization and normalization

Canonicalization input is the exact manifest and every listed module byte sequence.

Validation rejects:

- non-UTF-8 input;
- duplicate JSON keys;
- non-integer JSON numbers—decimals must use canonical strings;
- undeclared files or module references;
- remote references;
- unknown properties outside declared namespaced extensions;
- duplicate IDs or unresolved endpoints.

Produce three distinct digest domains:

1. `exact_source_digest`: SHA-256 over path-length/path/byte-length/exact-byte frames in normalized path order.
2. `canonical_source_digest`: SHA-256 over canonical JSON values, ignoring source indentation and object-key order.
3. `normalized_model_digest`: SHA-256 over normalized-model bytes, bound additionally to schema-suite digest, canonicalization-profile digest, and normalizer identity/version.

Canonical JSON rules:

- UTF-8, no BOM;
- lexicographically sorted object keys;
- minimal JSON escaping and no insignificant whitespace;
- source strings must already satisfy the declared Unicode normalization rule;
- set-like arrays sort by schema-declared stable keys;
- sequence-like arrays preserve explicit semantic order;
- display order is represented as data and never used for identity.

The derived `NormalizedSemanticModel` flattens records by stable ID and relations by `relation_id`, with deterministic ordering. It is reproducible and disposable; editing or admitting it as source is invalid.

### Compatibility

Use explicit states:

- `exact`: schema-suite ID, version, and digest match;
- `read-compatible`: the reader accepts the source version, but normalization targets one exact declared version;
- `migration-required`: identity-preserving `MigrationMap` required before normalization;
- `unsupported`: fail closed.

A version range alone is insufficient for reproducibility; every accepted execution still binds the exact schema-suite digest. Major-version movement is never implicit. Split, merge, retirement, or ID replacement requires a queryable identity map and rollback evidence.

### Build-from-owned boundary

Build from owned:

- current record kinds;
- current lifecycle/role/outcome axis separation;
- current confidence split;
- current evidence, governance, and embedded-edge shapes;
- canonical `promotion_record` semantics;
- cataloged ontology-type IDs.

New candidate work:

- package manifest;
- closure rules;
- relation IDs;
- canonicalization profile;
- suite composition/digest;
- normalized IR;
- compatibility and migration contracts.

## 3. Representation comparison

| Rubric | Closed JSON | Constrained JSON-LD | Typed authoring → JSON |
|---|---|---|---|
| Local closure | Strong; local refs can be prohibited directly | Conditional; contexts and vocabularies must be vendored and frozen | Strong only if grammar, compiler, imports, and output schema are all pinned |
| Canonicalization | Small, explicit byte/value contract | Harder because compaction, expansion, contexts, and graph normalization add choices | Deterministic only through another compiler contract |
| Stable IDs | Explicit owner-assigned IDs | Native identifier support, but does not solve owner identity policy | Explicit IDs possible |
| Schema composition | Straightforward closed modules | Powerful but requires two interacting constraint/graph regimes | Good, but grammar and JSON schema can drift |
| Graph semantics | Adequate through typed relations | Strongest native graph representation | Depends on compiled AST |
| Semantic diff | Good after canonical semantic diffing | Weak-to-moderate because equivalent graph spellings may differ | Best authoring diff if the language is carefully designed |
| Portability | Highest with ordinary JSON tooling | Moderate; specialized tooling and local-context discipline required | Lowest initially; consumers require the compiler or canonical output |
| Migration | Direct record-to-record mapping | Adds vocabulary/context migration | Must migrate both authoring syntax and canonical target |

Recommendation: closed JSON is the smallest v1 contract. JSON-LD is better treated as a derived graph projection. Typed YAML or a small language can later become a schema-guided source-patch frontend, but admitting it now introduces a second compiler and source-identity problem before authoring evidence proves the cost necessary.

## 4. Finite positive and negative witnesses

### Positive

1. Single-module package validates and two normalizations produce byte-identical IR.
2. Whitespace and object-key reordering change `exact_source_digest` but preserve `canonical_source_digest` and IR digest.
3. Multi-module records with a typed cross-module relation resolve and normalize in stable-ID order.
4. Changing `display_order` changes presentation semantics without changing record identity.
5. Unsupported evidence remains `confidence.evidence: unknown`; normalization does not promote it.
6. A total migration preserves IDs and produces `migration-required → exact`.
7. A promoted entry still requires the existing owner/evidence conditions; package validity alone has no promotion effect.

### Negative

1. Duplicate record ID across modules: reject.
2. Relation endpoint absent from the package: reject.
3. Relation endpoint exists but violates the relation’s allowed endpoint profile: reject.
4. Undeclared module or remote reference/context: reject.
5. Duplicate JSON key or forbidden numeric form: reject.
6. Schema-suite version matches but digest differs: reject.
7. Normalized IR is submitted as authored source: reject.
8. Content-hash-derived record ID changes after wording correction: migration/identity failure.
9. Schema-valid package without owner admission: structurally valid, but not admitted or authoritative.
10. Projection contains a semantic relation absent from normalized IR: projection failure, not new knowledge.
11. Minor-version reader silently accepts a changed enum or normalization rule without exact digest binding: compatibility failure.
12. Missing evidence is interpreted as support: semantic validation failure; retain unknown.

## 5. Rejected alternatives

- **JSON-LD as v1 authored source:** rejected because graph expressiveness does not compensate for the added closure, context, canonicalization, and semantic-diff ambiguity. It remains a strong derived projection.
- **Typed YAML or custom DSL as v1 admitted source:** rejected because it adds grammar/compiler authority and two migration surfaces. Reconsider after authoring witnesses demonstrate closed JSON plus schema-guided tooling is inadequate.
- **One universal mega-schema:** rejected because package closure, record semantics, relations, projections, and ontology-type constraints have different evolution pressures.
- **Independently authored normalized IR:** rejected as a second source of truth.
- **Content-addressed semantic IDs:** rejected because ordinary claim correction would destroy continuity. Content digests bind versions; they do not name enduring entities.
- **Implicit external endpoint resolution:** rejected because it breaks local closure and reproducibility.
- **Separate evidence and governance schema packages in v1:** deferred because current sources show record-owned fields, not independently governed object lifecycles.

## 6. Claim ceiling

This is a read-only specialist recommendation from the confirmed candidate-local research run. It does not establish a canonical schema, public convention, implementation, migration approval, owner admission, promotion, generated-package synchronization, release, or RWO gate decision. Existing candidate validation proves only the earlier branch-aware bundle, not this proposed semantic-package spine.

## 7. Residue and reroute

- Projection authoring specialist: confirm whether closed JSON can support humane long-form authoring, source patches, display order, and semantic diffs.
- Governance/migration specialist: decide `AdmissionRecord` non-vacuity, owner movements, rollback, compatibility, and private-profile boundaries.
- Parent synthesis: join all three receipts and preserve disagreements.
- Ontology Vault `convention-update`: formulate any consolidated candidate rule with migration and rollback.
- Sigil Development plus owner approval: required before public source mutation.
- Implementation Layering/Task Session: later compiler, schema, fixtures, and deterministic test execution.
- The paused RWO identity gate remains untouched.

Status: **pass**. Blockers: none for specialist research; representation admission, exact schema promotion, `AdmissionRecord`, migration ownership, and public mutation remain intentionally unresolved owner decisions.
