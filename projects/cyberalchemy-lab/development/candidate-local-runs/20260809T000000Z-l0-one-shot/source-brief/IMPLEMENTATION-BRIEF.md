# CyberAlchemy Lab L0 — Implementation Source Brief

## Scope

This is a source-derived implementation brief for SWU-CAL-002 through SWU-CAL-010. It does not alter the package or decide unresolved research/authority questions. Existing SWU-CAL-001 supplies `cal-canonical-json-v1` and must be imported rather than reimplemented.

## Existing foundation (SWU-CAL-001)

- `schemas/canonical-json-profile.json`: profile `cal-canonical-json-v1`, schema `1.0.0`, SHA-256 digests over `profile_id`, profile schema version, value schema version, and canonical UTF-8 bytes separated by NUL.
- Valid values: null, boolean, string, array, plain object, and JavaScript safe integer. Object keys are printable ASCII, decoded-unique, and raw-ASCII sorted; arrays preserve order; strings use `JSON.stringify` escaping; output has no insignificant whitespace.
- Raw parsing rejects decoded duplicate keys before `JSON.parse`; it rejects fraction/exponent forms, negative zero, and unsafe integers. Direct values reject symbols, accessors, non-plain objects, sparse arrays, unsupported types, and cycles.
- Existing error vocabulary: `CAL_JSON_INPUT_NOT_TEXT`, `CAL_JSON_SYNTAX_INVALID`, `CAL_JSON_KEY_NOT_PRINTABLE_ASCII`, `CAL_JSON_DUPLICATE_KEY`, `CAL_JSON_NEGATIVE_ZERO`, `CAL_JSON_NUMBER_FORM_FORBIDDEN`, `CAL_JSON_UNSAFE_INTEGER`, `CAL_JSON_UNSUPPORTED_VALUE`, `CAL_JSON_CYCLE`, `CAL_JSON_SCHEMA_VERSION_REQUIRED`.

## SWU map and owned files

| SWU | Requirement | Product files |
| --- | --- | --- |
| 002 | Closed record/graph contract | `schemas/lab-records.schema.json`, `ontology/relation-registry.json`, `tests/record-contract.test.mjs` |
| 003 | Projection shape plus privacy contract | `schemas/projection.schema.json`, `privacy/privacy-policy.json`, `projection/projection-contract.json`, `tests/projection-contract.test.mjs` |
| 004 | Candidate Research Tower navigation spine | seven top-level package prose files below |
| 005 | Unselected decision, definition binding, open residue, blocked promotion, not-run validation controls | `residue/residue-items.json`, `decisions/representative-tower.md`, `definitions/definition-bindings.json`, `promotions/blocked-promotion.json`, `validation/expected-validation-records.json`, `tests/package-structure.test.mjs` |
| 006 | One complete synthetic seven-file tower and valid input graph | toy source tree, six graph JSON files, `fixtures/valid/synthetic-one-tower.json`, `tests/fixture-contract.test.mjs` |
| 007 | Deterministic, privacy-filtered projection compiler | `tools/compile-projection.mjs`, `tests/compile-projection.test.mjs` |
| 008 | Fifteen single-fault fail-closed mutants | `fixtures/invalid/mutant-matrix.json`, `tests/negative-mutants.test.mjs` |
| 009 | Ordered package snapshot and verifier | `tools/build-package-snapshot.mjs`, `PACKAGE-SNAPSHOT.json`, `tests/package-snapshot.test.mjs` |
| 010 | Isolated synthetic witness | `development/witness-runs/l0-synthetic-001/{INPUT-LOCK.json,projection.json,validation-records.json,RESULT.md}` |

Every SWU’s historical execution-receipt target is omitted from this candidate-local build brief; the user explicitly deferred lifecycle bookkeeping.

## Closed records and common invariants

All record kinds carry: `schema_version`, stable logical `id`, `record_snapshot_id`, `status`, `privacy_class`, `provenance`, `authority_effect: "none"`, and `fixture_class`.

| Kind | Required distinguishing fields | Invariant |
| --- | --- | --- |
| `SourceSnapshot` | `logical_source_id`, `content_digest`, `byte_size`, `media_type`, `locator`, `capture_context`, `owner`, revision relations | ID binds logical source and digest; equal bytes never merge logical sources. |
| `TowerPackageSnapshot` | `tower_logical_id`, complete ordered artifact manifest, source bindings, `manifest_digest` | Manifest ordering changes identity. |
| `Claim` | proposition, scope, owner, status, claim ceiling | Exactly one falsifiable proposition. |
| `EvidenceAnchor` | immutable source snapshot, byte-range selector, selected-byte digest, role | Must resolve once against exact source bytes. |
| `DefinitionReference` | governed term ID, owner path, selector/digest, binding status | References rather than redefines the term. |
| `ResidueItem` | question/failure, scope, owner, status, blocked claims/gates | Open residue cannot project as cleared. |
| `OntologyCandidate` | proposed meaning, scope, evidence ceiling, review state, contradiction path | Candidate/non-authority state remains constant. |
| `ValidationRecord` | validator/profile/version, exact inputs, command, environment, result, violations, time | Proves named check only; compiler cannot self-pass. |
| `PromotionRecord` | one primary candidate, evidence, owner, gate result, scope, contradiction, expiry, rollback, decision ref | Synthetic L0 requires `gate_result: "block"`. |
| `Relation` | kind, from/to IDs, direction, provenance, status | Must be admitted by closed registry/endpoints. |

Closed `fixture_class` values: `synthetic-contract-fixture`, `mechanics-only-private-provisional`, `owner-selected-real-tower`. L0 data uses the first; none of these make the fixture representative.

## Relation registry

| Kind | Endpoints | Rule |
| --- | --- | --- |
| `package_contains` | `TowerPackageSnapshot` -> any package record | One-to-one-or-more; acyclic. |
| `anchored_by` | `Claim` or `OntologyCandidate` -> `EvidenceAnchor` | One-or-more; acyclic. |
| `supports` | `EvidenceAnchor` -> `Claim` or `OntologyCandidate` | Many-to-many; acyclic in L0. |
| `references_definition` | `OntologyCandidate` -> `DefinitionReference` | One-or-more; acyclic. |
| `derived_from` | projection record -> every used input snapshot/record ID | One-or-more; acyclic; compiler-created only. |
| `blocked_by` | `PromotionRecord` or candidate -> open `ResidueItem`, contradiction, or failed `ValidationRecord` | One-or-more while blocked; acyclic. |
| `contradicts` | `Claim` -> `Claim` | Explicit symmetric pair, scoped status, no cycle beyond that pair. |

Unknown kinds/endpoint combinations, dangling endpoints, ID collisions, inferred equality, unanchored claims/candidates, unblocked promotion, and extra contradiction cycles must fail. Output-only relation sort is `(kind, from_id, to_id, relation_id)` and must not merge logically distinct duplicate relationships.

## Projection and privacy contract

- Projection is disposable and outside the candidate package. It carries formula inputs; records sorted `(kind,id)`; relations in registry order then IDs; forward/reverse adjacency; privacy decisions; invalid/stale state; and `authority_effect: none`.
- Revision is SHA-256 over canonical `{projection_schema_version,tower_snapshot_id,input_record_snapshot_ids_sorted,relation_registry_digest,projection_rules_digest,generator_contract_digest,privacy_policy_digest}` using the existing profile.
- Reserved consumer fields: projection schema/revision, tower snapshot ID, generator/privacy digests, fixture class, records/relations/adjacency, source digest/selector/owner/privacy class/claim ceiling, contradiction/residue state, invalid/stale state, authority effect.
- Privacy is a field allow/deny policy by privacy class. Before atomic rename, recursively reject unknown projection keys, denied keys at any depth, exact denied locators/content values, and configured byte-pattern sentinels. Require every record’s privacy class and applied policy digest; validate again after filtering. Failed runs must preserve a prior valid output.
- Static seam only: no `POST`, publication, or effectful transport token in the reserved consumer contract. No server, adapter, IDE, or browser implementation is in L0.

## Synthetic fixture

The toy source tree is exactly these seven authored files:

1. `fixtures/source/toy-tower/README.md`
2. `fixtures/source/toy-tower/TOWER.md`
3. `fixtures/source/toy-tower/levels/L0-corpus.md`
4. `fixtures/source/toy-tower/levels/L1-residue-map.md`
5. `fixtures/source/toy-tower/levels/L2-closure-plan.md`
6. `fixtures/source/toy-tower/gates/closure-gates.md`
7. `fixtures/source/toy-tower/residue/open-residue.md`

Exact graph cardinality: 1 `TowerPackageSnapshot`; 7 `SourceSnapshot`; 1 `Claim` sourced from toy `L0-corpus.md`; 1 external `DefinitionReference`; 1 open `ResidueItem`; 2 `EvidenceAnchor` records (toy claim and external definition); 1 candidate `OntologyCandidate`; 1 blocked `PromotionRecord`; and only closure-required input relations (`package_contains`, `anchored_by`, `supports`, `references_definition`, `blocked_by`). The compiler alone adds `derived_from` projection edges. All instances are `synthetic-contract-fixture`, `authority_effect:none`.

The external DefinitionReference is fixed to `development/research/2026-08-07-foundation/findings.md`, digest `07a29e2fc62f92b6eb2d28c197b19c2ccc036a9952b75474f52c5ac9a44de11d`, its Research Tower definition/non-goals selector, and status `accepted-research-definition-reference`.

All byte selectors use `utf8-byte-range-v1`: `{kind,start_byte,end_byte_exclusive,selected_bytes_sha256}` with `start_byte < end_byte_exclusive <= byte_size`, raw bytes, matching slice digest, and no Unicode/newline normalization.

## Compiler and negative matrix

Compiler input: exact allowlisted fixture/input, source bytes, records/relations, package snapshot, relation registry, projection/privacy contracts, and the existing canonical JSON tool. It recomputes digests/sizes/IDs/self-binding, resolves anchors, validates record/graph/gate state, filters/scans privacy, builds adjacency, computes revision, canonicalizes, writes temporary output and atomically renames only on success. It may emit diagnostics/build lock but never a passing `ValidationRecord`.

| ID | Primary mutant | Required code |
| --- | --- | --- |
| M01 | Source byte changes while digest remains | `CAL_SOURCE_DIGEST_MISMATCH` |
| M02 | Anchor out of bounds or wrong slice digest | `CAL_SELECTOR_INVALID` |
| M03 | Distinct logical source reuses source snapshot ID, or inferred `same_as` | `CAL_IDENTITY_COLLAPSE` |
| M04 | Reordered manifest with old tower ID | `CAL_TOWER_SNAPSHOT_STALE` |
| M05 | Absent relation endpoint | `CAL_RELATION_DANGLING` |
| M06 | Unknown record/relation kind | `CAL_KIND_UNSUPPORTED` |
| M07 | Denied private locator/content/sentinel in final output | `CAL_PRIVACY_EXPOSURE` |
| M08 | Changed input/rule/generator/privacy binding with old revision | `CAL_PROJECTION_STALE` |
| M09 | ValidationRecord missing/mismatching input set, profile, or command | `CAL_VALIDATION_UNBOUND` |
| M10 | Open residue/contradiction rendered cleared | `CAL_RESIDUE_STATE_MISMATCH` |
| M11 | Changed authority effect/promotion gate/status or projection asserts promotion | `CAL_AUTHORITY_EFFECT_FORBIDDEN` |
| M12 | `POST`, publication, or effectful reserved transport | `CAL_TRANSPORT_EFFECT_FORBIDDEN` (static only) |
| M13 | Tower absent from exact allowlist/input lock | `CAL_TOWER_NOT_ALLOWLISTED` |
| M14 | Invalid normalized self digest | `CAL_PACKAGE_MANIFEST_STALE` |
| M15 | Compiler identity as passing validator | `CAL_VALIDATOR_NOT_INDEPENDENT` |

Every mutant is a single committed delta from the valid fixture, executes once, expects the exact code, and proves the previous valid output bytes are unchanged.

## Package snapshot

`PACKAGE-SNAPSHOT.json` lists every authored package file in declared order and no witness output. Its `normalized-self-v1` verification sets the manifest entry’s `content_digest` to 64 zeroes and root `manifest_self_digest` + `tower_snapshot_id` to 64 zeroes, canonicalizes/hashes, materializes `manifest_self_digest`, then calculates and materializes `tower_snapshot_id` from schema, tower ID, ordered artifacts (with manifest self digest), source bindings, definition binding digest, and privacy policy digest. Check must reject extras, omissions, duplicates, symlink escape, filesystem-order dependence, and stale fields.

## Witness run and final commands

`development/witness-runs/l0-synthetic-001/` contains only `INPUT-LOCK.json`, `projection.json`, `validation-records.json`, and `RESULT.md`. Lock package/tool/test/Node/command/environment/privacy/rule digests; compile twice to isolated outputs and compare bytes; then materialize the one accepted projection. An independent identity issues immutable validation records and `RESULT.md` must state mechanics-only evidence, `authority_effect:none`, and deny real-source, representative, IDE, authority, effect, readiness, promotion, publication, deployment, and release claims.

```text
node --test projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/record-contract.test.mjs
node --test projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/projection-contract.test.mjs
node --test projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/package-structure.test.mjs
node --test projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/fixture-contract.test.mjs
node --test projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/compile-projection.test.mjs
node --test projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/negative-mutants.test.mjs
node --test projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/package-snapshot.test.mjs
node --test projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/*.test.mjs
node projects/cyberalchemy-lab/research/tower-evidence-navigator/tools/build-package-snapshot.mjs --check
python3 -m json.tool <each emitted JSON>
```

## Evidence and ambiguities

1. The plans require a strict schema and stable compiler failures but do not prescribe a JSON Schema dialect, a single universal record envelope shape, or exact JSON key names beyond named required fields. Choose a self-consistent dependency-free format and lock it in tests.
2. The plans require source snapshot IDs to bind logical ID/digest but do not prescribe the exact ID preimage. Use an explicit canonical formula and test equal bytes with different logical IDs.
3. Relation cardinalities are semantic; they do not supply a generic graph API. Implement a narrow validator tied to the fixture and registry.
4. Privacy classes, allowed fields, denied keys, sentinels, and schema field sets are deliberately delegated to SWU-CAL-003. Define them minimally, then use M07 to lock behavior.
5. The package manifest’s exact allowlisted file order is not enumerated. The snapshot builder must own an explicit list covering every authored package file at final L0, excluding only witness output.
6. `ValidationRecord` has required concepts but no immutable storage encoding. Use a stable record collection that binds command, inputs, environment, validator identity, result, violations, and time; ensure M09/M15 validate it.
7. `INPUT-LOCK.json` is required before compilation but its exact source fields are only listed conceptually. Include all named inputs and their digests plus output command/version context; use it to implement M13.
8. Stage 06 says compiler computes definition/privacy/generator contract digests; the plans do not define all file-to-digest mappings. Document them inside the projection contract and test their inclusion in revision.

## Evidence sources

- `stages/06-invoke-design/ARCHITECTURE.md`
- `stages/08-distill-repair.md` (superseding canonicalization, fixture, privacy, mutant details)
- `work-pack/tasks/TASK-CAL-{CONTRACTS,PACKAGE,COMPILER,SNAPSHOT,WITNESS}.md`
- Existing SWU-CAL-001 canonical profile/module/tests
