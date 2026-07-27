# Explorer Returns — Akashic Contract Architecture

Dispatch: `2026-07-26-akashic-contract-architecture`
Transcript owner: parent strategist
Status: verbatim substantive explorer returns

The following sections preserve the explorers' returns for downstream
synthesis. They are research inputs, not accepted findings or Design authority.

## Agent 1 — Abramsky, Samson

## Structural/formal return — Abramsky lane

### 1. Exact current contract inventory

The target currently contains an authored candidate Define/Design contract, not an implemented contract:

- `akashic-content/v0`: proposed closed discriminated `SourceRecord | ClaimRecord` file format.
- `AuthorSource` / `AuthorClaim`: proposed contributor-attributed authoring operations.
- `ValidateRecordSet`: proposed closed-shape plus deterministic cross-record validation.
- Identity/reuse law: proposed rejection of duplicate identity only at the same declared resource level and scope.
- Evidence-reference law: proposed embedded `ClaimRecord.evidence[] → SourceRecord` references with exact selectors; raw `supported_by` and generic `derived_from` are forbidden.
- Rights/time/authority laws: proposed rights-basis and timestamp predicates plus a hard ceiling preventing authored or generated truth/review/publication/permission/promotion states.
- Validation facts/receipts: proposed version-and-digest-bound conformance facts with ordered diagnostics.
- `CompileInventory`: proposed one-origin deterministic authored-record projection and selector index.
- `CheckProjectionParity`: proposed rebuild comparison rejecting stale or hand-edited generated output.
- `GetRecord`, `SelectContent`, `ReverseSourceLookup`, `ExplainProjection`: proposed read-only retrieval contracts.
- Interface versions: candidate schema, predicate, generator, projection, and selector versions.
- Planned witness bank: Design-only `VC-*` fixtures; none executed.

Status boundary:

- **Current:** only the markdown/JSON Define and Design artifacts, including scope and planned-witness manifests.
- **Proposed Phase 0:** all contracts above.
- **Deferred:** context packets/PR controls/skills (Phase 1); first-class `EvidenceAssertion`, excerpts, synthesis, tower records (Phase 2); concepts/categories/collections/semantic projection (Phase 3); RDF/SHACL or Olog substrate comparison (Phase 4).
- **Missing/blocking:** schemas, validator, diagnostic registry, canonical serializer, generators, selectors, fixtures, receipts, runtime proof, and genuine owner bindings.
- **Killed:** raw `supported_by`, generic `derived_from`, stored inverses, generic `is_part_of`, self-authored authority/lifecycle state, automated truth/publication/promotion.

The prior research remains public and useful but explicitly records dissent/loop-ceiling, no runtime witness, and unbound owners. It is source input, not acceptance authority.

### 2. Candidate contract matrix

| ID / family | Phase; producer → consumer | Bound input → output | Invariant; deterministic diagnostic/residue | Authority effect; version/compatibility owner | Status; smallest + / single-fault − | Exact selectors; external source |
|---|---|---|---|---|---|---|
| `AK-REC-v0` closed record envelope | P0; contributor → shape validator/readers | UTF-8 structured file, `akashic-content/v0`, attribution, kind payload → one `SourceRecord` or `ClaimRecord` | Exactly one kind-specific closed payload; reject unknown field, multiple/wrong payload, missing evidence, nested attribution | Attribution only; schema/validator owner unbound; schema version explicit, no predecessor promise | Proposed/blocked; + one valid source and one valid evidence-bearing claim; − add one unknown property (`VC-SHAPE-NEG-UNKNOWN-001`) | `SPEC.md` Capabilities/Domain Concepts; `interfaces.md` Authored File; `VALIDATION-CONTRACTS.md#VC-SHAPE`; [JSON Schema Core 2020-12](https://json-schema.org/draft/2020-12/json-schema-core), [Validation](https://json-schema.org/draft/2020-12/json-schema-validation) |
| `AK-ID-v0` source identity/reuse | P0; source author → cross-record validator | resource level, scope, typed basis, record set → identity index / diagnostic | One identity per same bound level+scope; byte digest cannot prove work identity; `VC-IDENTITY-NEG-DUPLICATE-001` or `...DIGEST-001` | Conformance only; source-identity owner unbound; compatibility must later state identity preservation | Proposed/blocked; + A1/A2 reuse one Source A; − second SourceRecord claims same bound identity at same level/scope | `SPEC.md` AK-C1/AK-C3; `operations.md#ValidateRecordSet`; `VALIDATION-CONTRACTS.md#VC-IDENTITY`; local policy, no external spec claimed |
| `AK-EVID-v0` embedded evidence reference | P0; claim author → reference validator/projector/query | claim, source IDs, exact selectors, relation, interpretation, basis → validated directed references | `ClaimRecord → SourceRecord`, `1..n`, non-transitive, no stored inverse; reject dangling/wrong-kind/missing selector/raw killed edge | Contributor assertion only; schema/content owners unbound; incompatible first-class evidence requires later version | Proposed/blocked; + A1 selector 1 and A2 selector 2 resolve to Source A; − change one source ID to unknown | `SPEC.md` AK-C2; `operations.md#AuthorClaim/#ValidateRecordSet`; `VALIDATION-CONTRACTS.md#VC-REFERENCE`; `findings.md#ClaimRecord-with-embedded-attributable-evidence` |
| `AK-RTA-v0` rights, time, authority separation | P0; record author → validators/receipt writer | rights state+basis, timestamps, fields → pass/fail fact | asserted license/permission needs basis; update ≥ creation; no self-authored truth/review/publication/acceptance/promotion/permission | No legal permission or owner decision; rights and governance owners unbound | Proposed/blocked; + `rights=unknown` without invented permission; − asserted permission with basis removed | `SPEC.md` AK-C3/Claim Ceiling; `operations.md`; `mappings.md#Prohibited-Mappings`; `VALIDATION-CONTRACTS.md#VC-RIGHTS/#VC-PHASE-BOUNDARY` |
| `AK-VAL-v0` validation/diagnostics | P0; shape+cross validators → projector/test harness | exact paths+bytes, schema/predicate versions → ordered diagnostics, input digest, validation facts | Stable precedence: path, shape/kind, forbidden, time/rights, ID/identity, endpoint/reference, selector/relation, parity; residue `OWNER_UNRESOLVED` is blocking | Conformance for named bytes only; schema/validator owns future diagnostic registry | Proposed/blocked; + complete A/B record set passes; − one fixture violates one predicate and returns expected ID+selector | `operations.md#ValidateRecordSet/#Failure-Ordering`; `ARCHITECTURE.md` validation components; `VALIDATION-CONTRACTS.md#Fixture-Discipline`; JSON Schema defines standardized output structures but local diagnostic IDs/precedence remain Akashic-owned: [Core output section/schema](https://json-schema.org/draft/2020-12/json-schema-core#section-12) |
| `AK-PROJ-v0` Inventory projection | P0; projector → selector engine/readers | validation-passing exact record set + generator/projection versions → one entry/origin per authored record, selector index, input/output digests | Pure, identity-preserving, stable-ID order, no upstream write, no minted status/confidence/meaning/authority | Non-authority derivation; retrieval/projection owner unbound; projection version explicit | Proposed/blocked; + five authored records produce five explained entries; − projector attempts authored-path mutation | `operations.md#CompileInventory`; `mappings.md`; `ARCHITECTURE.md#Inventory-Projector`; `VALIDATION-CONTRACTS.md#VC-PROJECTION` |
| `AK-PARITY-v0` byte determinism/parity | P0; projector/parity checker → test harness/generated store | same authored bytes+versions or rebuilt output → canonical bytes/digests/parity verdict | Identical bound inputs produce byte-identical output; stale/hand edit rejected; incomplete build discarded before atomic replacement | Operation fact only; retrieval/projection owner must bind serializer and digest policy | Proposed but **underspecified**; + repeat build exact-byte equality; − flip one projected byte in generated entry | `operations.md#CheckProjectionParity`; `ARCHITECTURE.md` Recovery/Persistence; `VALIDATION-CONTRACTS.md#VC-PROJECTION`; JCS supplies a concrete canonical JSON option but is Informational and not selected locally: [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html) |
| `AK-QUERY-v0` selector/origin queries | P0; Inventory+selector engine → curator/agent/test harness | versioned finite selector or record/entry/source ID → stable matches, not-found, reverse lookup, origin explanation | A1/A2 selected and B1 excluded; stable order; each output exposes attribution, exact selectors, rights, projection origin, and separate receipt state; deterministic invalid-selector/not-found residue required but IDs absent | Read-only, no acceptance/publication truth; retrieval owner unbound; selector version explicit | Proposed/blocked; + composite selector returns A1/A2 only; − remove exact origin or return an authority field | `queries.md`; `interfaces.md#Selector-Interface`; `mappings.md#Record-Set-to-Selector-Index`; `VALIDATION-CONTRACTS.md#VC-SELECTOR` |
| `AK-VERSION-v0` version/compatibility/admission | P0 boundary, later versions; future owners → validators/readers/migrators | schema/predicate/selector/generator/projection versions + proposed successor contract → accept/reject/migrate decision | P0 promises no predecessor compatibility; successor must state identity preservation, migration, and projection parity before reading/rewriting records; mechanism admission requires distinct behavior+witness | Owner decision only; owners currently unbound; deterministic diagnostic absent | **Missing as executable contract**; + declared supported tuple reads without reinterpretation; − one unsupported/mixed version fails before processing | `interfaces.md#Compatibility-Boundary`; `ARCHITECTURE.md#Integration-and-Versioning-Extension/#Decision-Flow-View`; JSON Schema `$schema` identifies dialect, and implementations must switch modes or error on unsupported referenced dialects: [Core §8.1.1](https://json-schema.org/draft/2020-12/json-schema-core#section-8.1.1), [2020-12 release notes](https://json-schema.org/draft/2020-12/release-notes) |

External verification consequences:

- JSON Schema 2020-12 can express the closed discriminated shape using `oneOf` and closure using `unevaluatedProperties`; `format` is annotation-only under the default dialect, so an RFC 3339/BCP-47-shaped string does **not** become a fail-closed assertion unless the local dialect/validator explicitly enables or implements assertion behavior.
- JSON Schema does not supply Akashic’s cross-record identity, reference, rights, ordering, or authority laws; these remain local validator contracts.
- “Byte-stable” is not established merely by JSON Schema or stable key insertion. A concrete canonical serialization contract is still missing. RFC 8785 is one candidate, with constraints including I-JSON, duplicate-property rejection, deterministic recursive property sorting, and exact number/string serialization.
- The local diagnostic registry is explicitly future-owned. JSON Schema output vocabulary can structure schema/instance locations, but cannot by itself establish Akashic diagnostic IDs or precedence.

### 3. Facts, inferences, open questions

**Source-backed facts**

- Local artifacts label themselves candidate/authored-complete, with runtime evidence “none.”
- `PLANNED-WITNESSES.json` marks every witness `design-contract-authored`; execution owners are role placeholders.
- `DESIGN-SCOPE-MANIFEST.json` has `compatibility_boundaries: []`, while prose says a successor must state identity preservation, migration, and parity.
- The prior findings say the research dispatch ended in dissent/loop-ceiling and owner bindings remain unbound.
- JSON Schema’s `$schema` identifies a dialect; `oneOf` requires exactly one matching subschema; `unevaluatedProperties` can close composed schemas; default 2020-12 `format` behavior is annotation rather than assertion.
- RFC 8785 specifies a repeatable JSON canonical form but is Informational, not an Internet Standards Track specification.

**Inferences**

- The strongest audited Design delta is not a new semantic model. It is to make already-required observable boundaries explicit: serialization profile, diagnostic registry, supported version tuple, unsupported-version failure, and owner/admission contract.
- `AK-PARITY-v0` cannot currently sustain “byte-identical” interoperably because no canonical serializer, newline/encoding convention, digest algorithm, duplicate-key rule, or receipt byte format is selected.
- `AK-VERSION-v0` is prose-level only; absent an accepted-version matrix and deterministic incompatible-version residue, consumers can diverge before validation.
- A central catalogue is useful only if it is generated/validated from normative contract definitions; a hand-maintained summary would duplicate authority and add drift without behavior.

**Open questions**

- Which exact serialization profile, digest algorithm, UTF-8/newline rule, and duplicate-key behavior bind authored and generated bytes?
- Is `format` assertion required for timestamps/language tags, or are these local cross-record/string predicates?
- What are the exact diagnostic IDs and machine output schema for unreadable input, unsupported version, invalid selector, not-found, and owner-unresolved?
- What exact version tuple combinations are supported, and does a mismatch reject before reading any record?
- Who owns schema/validator, identity, rights, content review, projection/selector, compatibility, and migration admission?
- Is a future migration allowed to rewrite authored IDs? Current prose implies this must be decided, not assumed.
- The manifest’s `unknowns: []` is inconsistent with its own unbound-owner and compatibility residue; whether that field means “no uncaptured unknowns” or “no unknowns” needs clarification.

### 4. Do catalogue, compatibility, deprecation, or migration admission add distinct behavior?

- **Central contract catalogue:** conditionally yes. It adds distinct behavior only if it is the machine-validated registry mapping contract ID/version to producer, consumer, schema/dialect, diagnostic namespace, owner, authority ceiling, and lifecycle status, and validation fails on an unregistered/multiply-owned contract. A prose index alone adds no behavior.
- **Compatibility matrix:** yes, now. It determines whether a concrete `(schema, predicate, generator, projection, selector)` tuple is accepted or rejected before processing. This closes an observable failure boundary currently absent from the manifest.
- **Deprecation rule:** not yet as a standalone lifecycle. With no predecessor and no admitted successor, it adds no present P0 behavior. Preserve a rule that no version may be deprecated until a successor, migration witness, owner, and rejection/effective-date policy exist.
- **Migration admission:** yes as a fail-closed gate, but no migrator should be designed yet. Admission adds distinct behavior by forbidding a new version from reading or rewriting stored records until identity preservation, lossy-field handling, projection parity, rollback, and single-fault failure witnesses pass under a bound owner.

Recommended audited public-safe Design delta: add only the catalogue/compatibility/admission contracts and witnesses above, plus canonical-byte and diagnostic-output bindings. Do not add implementation claims, semantic machinery, owner names, or migration code.

## Agent 2 — Peirce, Charles Sanders

## Provenance / knowledge-library lane result

The public target already has a coherent Phase-0 provenance architecture, but it is Design authority only: no schema, validator, records, generator, owner binding, executed fixtures, workflow receipts, publication gate, or ontology admission exists. The defensible Design delta is therefore mainly sharper naming and explicit future seams—not promotion of new runtime or semantic machinery.

### 1. Contract matrix

| ID / family | Phase | Producer → consumer | Bound inputs → outputs | Invariant | Failure / residue | Authority effect | Version owner | Status | Witnesses | Local selector / primary provenance |
|---|---|---|---|---|---|---|---|---|---|---|
| `AK-PROV-01 / authored-source-description` | 0 | contributor → validator, reader | contributor identity/time, resource level, identity scope, typed basis, locator, source parties/dates, rights state → `SourceRecord` | Describes exactly one resource at one declared identity level; digest equality is only byte-level evidence; local record creation time is not source publication time | Reject unknown fields, identity-level collapse, duplicate same-scope identity, unsupported rights assertion; unresolved cross-host/work normalization remains residue | Establishes only what the contributor recorded about the source | schema/validator + source-identity + rights owners; all currently unbound | **Present as authored Design contract; unimplemented** | Positive: distinct A/B sources, A reused by two claims. Negative: duplicate identity; digest claimed as work identity; permission without basis | `define/SPEC.md#AK-C1`, `design/VALIDATION-CONTRACTS.md#VC-IDENTITY`, `#VC-RIGHTS`; [DOI Handbook](https://www.doi.org/doi-handbook/html/), [IFLA LRM 2024](https://repository.ifla.org/items/214c74cb-c075-4428-a138-39f8d06c55aa), [DCMI Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) |
| `AK-PROV-02 / authored-claim-and-evidence-value` | 0 | contributor → validator, selector consumer | proposition + one or more `{source_id, selector, relation, interpretation, basis}` values under record-level attribution → `ClaimRecord` | One contributor-attributed proposition; evidence denotes the contributor’s claimed bearing of an exact source segment, not source truth or accepted interpretation; no nested duplicate `asserted_by` | Reject no evidence, dangling/wrong-kind source, missing selector, raw `supported_by`, generic `derived_from`, nested attribution | Attribution only; no truth, acceptance, review, or permission | schema/validator + content/domain owners; unbound | **Present as authored Design contract; unimplemented** | Positive: A1/A2 use different selectors over Source A; B1 uses Source B. Negatives: missing selector, wrong endpoint, killed edge | `define/SPEC.md#AK-C2`, `design/VALIDATION-CONTRACTS.md#VC-REFERENCE`; [W3C Web Annotation Data Model](https://www.w3.org/TR/annotation-model/) |
| `AK-PROV-03 / source-segment-selection` | 0 | claim author → validator/query | source identity plus exact selector → selected source segment exposed beside result | Selector identifies a segment of a named source; source, selector, selected state, and interpretation remain distinct | Missing/unresolvable selector rejects; changing sources may require a future state/digest binding; current selector grammar is unspecified | None beyond recording and reproducibly locating the contributor’s selected target | selector grammar + source-identity owners; unbound | **Present in principle; selector types/state binding missing** | Current planned selectors discriminate A1/A2/B1; no stale-source or selector-recovery witness yet | `define/SPEC.md#AK-C2`, `design/ARCHITECTURE.md#Selector-Engine`, `design/VALIDATION-CONTRACTS.md#VC-REFERENCE`; [W3C Web Annotation selectors and states](https://www.w3.org/TR/annotation-model/#selectors) |
| `AK-PROV-04 / validation-fact` | 0 | validators → projector, human/test harness | exact input paths/digest, validator and predicate-profile versions → verdict + ordered diagnostics + emitted time | Fact is immutable and byte/predicate-bound; a pass means only that named predicates passed | Stable rejection without input mutation; owner-unresolved blocks implementation; execution receipt is missing | Conformance fact only; never assessment, truth, review, permission, publication, or promotion | schema/validator owner; unbound | **Present as event/receipt Design; not executed** | Planned `VC-SHAPE`, `VC-IDENTITY`, `VC-REFERENCE`, `VC-RIGHTS`; single-fault negatives | `define/events.md#RecordSetValidated`, `define/states.md#Derived-Processing-States`, `design/VALIDATION-CONTRACTS.md`; [W3C PROV-O Entity/Activity/Agent model](https://www.w3.org/TR/prov-o/) supports keeping generated activity facts distinct from entities and responsible agents |
| `AK-PROV-05 / inventory-projection-provenance` | 0 | projector → selector engine, reader | validated exact `RecordSet`, generator/projection versions, authored origins/digests → one entry per authored record + reverse selector index + projection receipt | Exactly one authored origin per entry; deterministic bytes for identical bound inputs; no upstream writes; read model mints no identity, meaning, confidence, or status | Stale/hand-edited projection fails parity; incomplete build discarded; last complete root retained; runtime generator absent | No independent authority; deterministic retrieval does not confer authority | retrieval/projection owner; unbound | **Present as Design contract; unimplemented** | Positive: byte-identical rebuild; input change changes digest. Negatives: stale, hand-edit, upstream write | `define/SPEC.md#AK-C4`, `design/ARCHITECTURE.md#Inventory-Projector`, `design/VALIDATION-CONTRACTS.md#VC-PROJECTION`; [W3C PROV-O](https://www.w3.org/TR/prov-o/) |
| `AK-PROV-06 / bounded-retrieval-result` | 0 | selector engine → human/agent | versioned selector over complete projection → stable ordered records with source selector, contributor attribution, rights state, separate receipt state, origin explanation | Retrieval explanation stays beside returned content; no ranking, inference, graph traversal, or hidden authority field | Stable error or stable ordered result; useful ranking/cross-host normalization remain unclaimed | Read-only retrieval fact, not acceptance or meaning | retrieval/projection owner; unbound | **Present as Design contract; unimplemented** | `VC-SELECTOR-DISCRIMINATION`, attribution, and one-origin positives; no retrieval-quality claim | `define/SPEC.md#AK-C5`, `design/ARCHITECTURE.md#Selector-Engine`, `design/VALIDATION-CONTRACTS.md#VC-SELECTOR` |
| `AK-PROV-07 / rights-description-and-basis` | 0 | contributor → rights validator/reviewer | `unknown`, asserted license, or rights statement plus basis reference where asserted → descriptive rights state | Rights information, rights basis, and legal permission are separate; `unknown` invents nothing; external-resource rights metadata can be non-authoritative hints | Unsupported asserted permission rejects; excerpt/reuse policy and rights owner are unresolved | Records a rights description; never grants permission or legal advice | rights/licensing owner; unbound | **Present narrowly; permission decision missing; excerpt policy deferred** | Positive: unknown; asserted license with basis. Negative: permission without basis | `design/VALIDATION-CONTRACTS.md#VC-RIGHTS`, `define/SPEC.md#AK-C1`; [DataCite Rights 4.7](https://datacite-metadata-schema.readthedocs.io/en/4.7/properties/rights/), [RightsStatements.org FAQ](https://rightsstatements.org/en/documentation/faq.html), [Web Annotation external-resource metadata warning](https://www.w3.org/TR/annotation-model/#external-web-resources) |
| `AK-LIFE-01 / assessment` | 1+ | named assessor/reviewer → bound owner or reader | subject, assessor, scope, basis/selectors, assessment kind, time/version → scoped attributable judgment | Assessment is about a named subject under a declared basis and remains distinct from validation and owner decision | No assessor identity/scope/basis means no assessment fact; disagreements remain multiple attributable assessments | Establishes only that assessor’s judgment | content/domain, rights, safety, or source-identity assessment owners; unbound | **Implied in research and authority map; deliberately absent from Phase 0; should remain deferred** | Needed positive: two assessors may disagree without overwriting claim. Negative: validator pass treated as assessment | `findings.md#Authority-and-non-authority-map`, `design/ARCHITECTURE.md#Authority-and-Trust-Extension`; [W3C Web Annotation motivations](https://www.w3.org/TR/annotation-model/#motivation-and-purpose) provides a useful precedent for preserving annotation purpose |
| `AK-LIFE-02 / owner-decision-and-publication-effect` | 1+ | genuinely bound owner → publication/admission consumer | exact subject/version, decision kind, owner binding, policy basis, state, receipt, effective time, revocation → decision-kind-specific effect | Review, acceptance, publication, permission, and ontology admission are separate decision kinds; merge is not publication; publication is not truth; revocation is explicit | `OWNER_UNRESOLVED`; missing decision kind/policy/receipt; invented lifecycle field rejected | Only the exact effect authorized by the bound decision kind; never universal truth | governance/publication/ontology/rights owner as applicable; none bound | **Boundary present; actual contract missing and correctly deferred** | Future positives must demonstrate effects differ by decision kind. Negatives: merge→publish, publish→true, reviewer→owner, generated→promoted | `define/states.md#Forbidden-Collapse`, `define/events.md#Non-Events`, `design/ARCHITECTURE.md#Authority-and-Trust-Extension` |
| `AK-SEM-01 / ontology-candidate-and-promotion` | 3 | selected source-backed claims + explicit owner gate → later graph/ontology projection | authored record IDs, candidate relation and endpoint/algebra contract, validation/assessment evidence, owner decision → candidate node/edge; separately, promoted meaning if admitted | Candidate has exactly one authored origin; projection cannot mint semantic identity/status; concepts, schemes, collections, hierarchy, relatedness, and admission remain non-collapsed | Defer without distinct consumer, owner, positive/negative witness, and discriminating behavior; reject strong `proves`, `equivalent_to`, `specializes`, `causes` relations in v1 | Candidate/projection: none. Promotion: only a future bound ontology-owner decision | semantic/ontology owner; missing | **Explicitly deferred; no current ontology contract or promotion** | Needed: direct-record selector cannot satisfy a real semantic query; removal/change produces distinct retrieval behavior. Negative: Inventory entry treated as concept; collection as hierarchy; validation as admission | `findings.md#Category-tag-concept-scheme-and-collection`, `#Candidate-allowed-relations`, `design/ARCHITECTURE.md#Later-mechanism-admission`; [W3C SKOS Reference](https://www.w3.org/TR/skos-reference/) |
| `AK-VERS-01 / contract-version-migration` | future | version owner/migrator → record reader/projector | old/new schema, predicate, selector, generator, projection versions + identity-preservation rule + migration receipt → migrated records/projections | Each interface carries a version; future revisions must say whether identity is preserved or superseded and prove projection parity before rewrite | No compatibility promise exists; ambiguous identity preservation blocks migration | Technical transformation fact only | each named interface owner; unbound | **Version fields present; migration contract missing and correctly deferred** | Future positives: identity-preserving and superseding migrations are distinguishable. Negatives: silent rewrite; projection parity assumed | `define/interfaces.md#Compatibility-Boundary`, `design/ARCHITECTURE.md#Integration-and-Versioning-Extension`; [DataCite relation-type distinctions](https://datacite-metadata-schema.readthedocs.io/en/4.7/appendices/appendix-1/relationType/) |

### 2. Strict non-collapse map

```text
authored fact
  = “contributor C recorded field/value V in record R at time T”
  ≠ the external world is as V states

source description
  = contributor-authored metadata identifying/describing resource S
  ≠ S itself
  ≠ a claim about S’s subject matter
  ≠ permission to reuse S

claim
  = contributor-attributed proposition P
  ≠ source wording
  ≠ accepted interpretation
  ≠ truth

evidence selector
  = a typed locator for segment X of source S, optionally bound to a source state
  ≠ P
  ≠ proof that X supports P
  ≠ the interpretation of X

validation fact
  = validator V evaluated predicates Q over exact bytes D and returned result R
  ≠ assessment
  ≠ owner decision
  ≠ review, truth, permission, publication, or promotion

assessment
  = assessor A’s scoped judgment J about subject U on basis B
  ≠ validation
  ≠ universal truth
  ≠ owner authorization

owner decision
  = bound owner O applied policy K and issued decision kind D over exact subject/version U
  ≠ the owner’s assessment unless separately recorded
  ≠ every possible downstream effect

publication effect
  = only the publish/unpublish effect named by a valid publication decision
  ≠ merge
  ≠ acceptance as true
  ≠ rights permission
  ≠ ontology admission

Inventory projection
  = deterministic generated view G over named authored inputs and versions
  ≠ authored fact
  ≠ new identity or meaning
  ≠ confidence, assessment, owner decision, or authority

ontology candidate
  = proposed semantic node/relation grounded in selected authored records,
    with explicit endpoint/algebra and provenance
  ≠ Inventory entry
  ≠ canonical concept
  ≠ admitted relation
  ≠ promoted meaning

promoted meaning
  = exact semantic effect of a future bound ontology-owner admission decision,
    under a versioned scheme and policy
  ≠ truth
  ≠ permission
  ≠ publication
  ≠ generic production authorization
```

The critical lifecycle order is not a conveyor belt where each stage upgrades the previous one. It is a set of joins across separate namespaces:

```text
authored records
  ├── validation facts
  ├── generated retrieval projections
  ├── later assessments
  └── later owner decisions
          ├── publication effect
          ├── rights/use effect
          └── ontology-admission effect
```

No arrow above is automatic. In particular:

- source selection does not entail evidential support;
- validator pass does not entail positive assessment;
- assessment does not entail owner decision;
- merge receipt does not entail publication;
- publication does not entail truth, permission, or ontology admission;
- deterministic Inventory retrieval does not entail semantic authority;
- ontology candidacy does not entail promoted meaning.

### 3. Source-backed facts

1. W3C Web Annotation separates an Annotation from its Body, Target, Specific Resource, Selector, State, and Motivation. It also explicitly warns that metadata stated about external Body/Target resources—including rights and creator information—are client hints, not authoritative information. This strongly supports Akashic’s separation of source description, source segment, interpretation, and authority. [Primary source](https://www.w3.org/TR/annotation-model/)

2. PROV-O’s starting model separates Entities, Activities, and responsible Agents, and its more specific derivation predicates distinguish quotation, revision, and primary-source relationships. This supports typed validation/projection activity receipts and argues against a generic `derived_from` field. It does not require Akashic to adopt RDF or PROV-O in Phase 0. [Primary source](https://www.w3.org/TR/prov-o/)

3. DCMI says its terms may inform non-RDF JSON or relational application profiles, while domain/range semantics may be treated as usage guidance outside RDF. Thus a versioned local profile is legitimate, but use of similarly named fields is not itself a DCMI-conformance claim. [Primary source](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)

4. DOI identifies a referent independently of the current resolution URL; DOI records and locations can change while the DOI/referent mapping persists, and persistence depends on organizational policies and maintenance. Therefore DOI, URL, observed representation, and captured-byte digest must not be collapsed. [Primary source](https://www.doi.org/doi-handbook/html/)

5. IFLA LRM distinguishes Work, Expression, Manifestation, and Item. Akashic’s current `work | edition | manifestation | captured_bytes` enumeration is a local policy vocabulary, not IFLA-LRM terminology and not yet a proved crosswalk. [Primary source](https://repository.ifla.org/items/214c74cb-c075-4428-a138-39f8d06c55aa)

6. DataCite distinguishes rights text, rights URI, identifier, identifier scheme, and scheme URI; it also defines distinct version, citation, metadata, part/whole, review, derivation, and reference relations. This supports keeping rights assertions basis-bound and relation-specific, but does not authorize adopting those relations without local consumers and invariants. [Rights](https://datacite-metadata-schema.readthedocs.io/en/4.7/properties/rights/), [relation types](https://datacite-metadata-schema.readthedocs.io/en/4.7/appendices/appendix-1/relationType/)

7. SKOS distinguishes concepts, schemes, labels, collections, associative relations, and hierarchy. A collection is not thereby a concept, and `related` is not hierarchy. This supports the current Phase-3 deferral. [Primary source](https://www.w3.org/TR/skos-reference/)

### 4. Bounded inferences for the Design delta

- Add a public-safe term such as **source description** or **source-description fact** so `SourceRecord` is not casually described as “the source fact.” Its only authored fact is that a named contributor recorded the description.
- Specify a minimal selector profile before implementation: selector type, source-state binding or explicit absence, normalization rules, resolution result, and diagnostic behavior. Exact free-form selector strings are not yet a reproducible provenance contract.
- Keep `EvidenceValue` embedded in Phase 0. Promote it to a first-class assertion only when independent authorship, conflicting interpretations, independent review, or lifecycle produces a discriminating witness.
- Treat validation/projection receipts as provenance of repository operations, not provenance of the underlying external proposition.
- Preserve rights description, legal assessment, and permission decision as three different contracts.
- Preserve assessment as a later attributable record distinct from the future owner decision.
- Do not introduce PROV-O, PREMIS, Web Annotation JSON-LD, RDF, or DataCite schemas into Phase 0. Their distinctions are useful design precedents; current consumers do not require their runtime substrates.
- Ontology population, if later admitted, should consume selected source-backed claim records plus explicit assessments and owner decisions. It must never consume Inventory entries as if retrieval projection were semantic admission.

### 5. Open questions / blocking residue

1. What exact resources do the four identity levels denote, and is `edition` meant to approximate an Expression, a Manifestation, or a repository-local bibliographic unit? The current list is usable only after a source-identity owner binds it.
2. Which selector types are permitted for HTML, PDF, audiovisual, repository files, and captured bytes? How is source drift detected?
3. Does Phase 0 require a captured representation digest whenever a selector targets mutable network content, or is unresolved mutability surfaced as residue?
4. Which rights assertions qualify as a sufficient “basis reference,” and which uses require a separate permission decision?
5. What stable contributor identity namespace is allowed, and how are corrections, renames, or compromised identities represented without rewriting provenance?
6. Are validation facts append-only event records, reproducible receipt files, or both? What is their retention and supersession rule?
7. What makes a validation/projection version authoritative for one run when technical owners are unbound?
8. Which future decision kinds exist—review acceptance, publication, reuse permission, ontology admission, production authorization—and who owns each independently?
9. What revocation semantics apply to publication and ontology admission, and how do projections expose revoked/superseded decisions without rewriting authored history?
10. Which concrete query is impossible or materially unsafe with direct record references and selectors, thereby earning a first-class evidence assertion or ontology layer?

The lane conclusion is conservative: the Phase-0 provenance core is already well bounded, but its positive status is “authored Design contract with planned witnesses,” not implemented, accepted, publication-ready, or ontology-ready.

## Agent 3 — Ashby, W. Ross

Operational contract research — read-only, no files edited.

AUDIT BASELINE

Source fact: target README says implementation is blocked on named owners, runtime evidence is none, and Phase-1 workflow is proposed/not implemented (`projects/akashic-records/README.md#current-status`, `#how-agents-would-participate`). Define explicitly excludes Phase-1 packet/agent PR skills (`development/phase-0-content-contract/define/SPEC.md#non-goals-and-deferred-surfaces`). Architecture places GitHub controls, skills, packets, publication decisions, PR review/merge, and trusted post-merge regeneration outside Phase 0 (`design/ARCHITECTURE.md#context-view`, `#candidate-authoring-and-projection`). Validation has only planned Design evidence and explicitly reserves `PACKET_STALE_OR_INCOMPLETE` and `FORBIDDEN_CONTROL_PLANE_DIFF` for Phase 1 (`design/VALIDATION-CONTRACTS.md#vc-phase-boundary`; findings `#smallest-positive-negative-witness-ladder`). Tree inspection confirms no `.github/**`, schemas, validators, records, skills, generated runtime, receipt implementation, or context-packet implementation. Therefore every contract below is a proposed Design delta, not deployed behavior or configured GitHub policy.

STATE TERMS: CURRENT = authored proposal/evidence boundary exists locally, not executable; PROPOSED = Phase-1 Design delta; DEFERRED = deliberately later; MISSING = required schema/producer/witness/owner is absent.

1) MINIMUM PHASE-1 TASK / TYPED INTAKE ISSUE — outside Phase 0; PROPOSED, implementation MISSING.
Producer: requester/triager under a future issue template. Consumer: trusted packet builder, capability selector, `add-content`, reviewers. Minimum payload: contract version; repository/base ref; stable issue ID; bounded objective; proposed source identities plus exact selectors; proposed claim(s); rights basis or explicit unknown; uncertainty/exclusions; permitted cohort; target paths + mutation allowlist; requested review classes; completion/close criteria. Preconditions: real issue identity; bounded cohort (reject whole-corpus intake); base ref resolvable; no invented owner assignment. Postconditions: immutable task snapshot/digest available to packet generation; triage outcome attributable. Authority effect: records request/triage only—no truth, permission, acceptance, owner binding, or merge authorization. Threat boundary: issue text/source material untrusted; injection instructions remain quoted data; stale base, ambiguous source/selector, unbounded scope, or control-plane mutations fail closed. Versioning: `task_contract_version` plus issue revision/update time and base SHA; any material edit changes task digest and invalidates dependent packet. Positive witness: one issue with one small coherent cohort and complete selectors/allowlist yields a packet request. Negative: “ingest this corpus” or target `.github/**` yields `TASK_UNBOUNDED` / `FORBIDDEN_CONTROL_PLANE_TARGET`. Local selectors: findings `#candidate-github-issue-to-pr-flow`; research `#1-issue-source-intake`, `#skill-contract-add-content`, `#threat-cases`. Official GitHub issue-to-PR linkage background: https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/merging-a-pull-request (mechanism only).

2) TRUSTED BASE-POLICY PACKET — outside Phase 0; PROPOSED, generator/owners MISSING.
Producer: repository-owned, base-ref-pinned read-only policy resolver running from trusted configuration. Consumer: context-packet builder, candidate validator, reviewer, owner-decision evaluator. Payload: repository ID; base ref/SHA; policy packet version/digest; schema/predicate/rights/selector/generator versions; allowed paths; forbidden control paths; required check names + expected producing App identities; review/ruleset requirements; bypass policy; policy-source paths/digests. Preconditions: policy is read from named base commit, not PR head or issue prose; accountable ruleset/governance owner bound; actual remote rules queried if claiming enforcement. Postcondition: immutable base-policy digest against which candidate/receipt claims can be verified. Authority effect: describes policy/config snapshot; does not prove controls actually blocked a change unless paired with observed run/remote facts. Threat: malicious head-branch lookalikes, same-name status laundering, base drift, bypass omission. Versioning: content-addressed by base SHA + canonical bytes; no compatibility inference across policy versions. Positive: candidate check uses exact required check emitted by expected App and base-owned schema. Negative: head adds same-named check or edits validator; `POLICY_SOURCE_UNTRUSTED` / `FORBIDDEN_CONTROL_PLANE_DIFF`. Local: findings `#candidate-github-issue-to-pr-flow`, `#capability-pool-and-context-packets`; research lines/anchors `#operating-model-source-intake-through-merge`, `#machine-checkable-checks`, `#threat-cases`. GitHub facts: rulesets can require reviews, latest-push approval, conversation resolution, status checks and select expected App source, but configuration must be established in the actual repo: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets . CODEOWNERS alone requests/permits qualifying owner approval; multiple listed owners do not mean all must approve, and CODEOWNERS itself should be protected: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners .

3) CONTENT CANDIDATE — bridges Phase 1 into the Phase-0 authored-record contract; authored SourceRecord/ClaimRecord SHAPES are CURRENT Design-only Phase 0, while candidate manifest/PR envelope is PROPOSED Phase 1 and MISSING.
Producer: contributor or `add-content` on unprivileged branch. Consumer: Phase-0 shape/cross-record validators, PR checks, `review-content`, owners. Payload: candidate ID; task/issue ID; base-policy digest; packet digest; head/base SHAs; changed-record manifest/path/digest; candidate SourceRecords/ClaimRecords using `akashic-content/v0`; source-selector table; uncertainty/exclusions; generator outputs only if repository-owned generator used. Preconditions: trusted packet fresh; paths allowlisted; source identity/selectors resolvable; asserted rights have basis; author cannot edit controls/approve/merge. Postconditions: deterministic diff and manifest bound to head SHA; validation can evaluate exact bytes. Authority: contributor attribution only. Threats: source hallucination, license misuse, prompt injection, schema gaming, stronger-than-source claim, generated hand edit. Versioning: record schema version plus candidate envelope version; material head push invalidates reports/reviews tied to old SHA. Positive: two sources/three claims planned Phase-0 witness carried in an allowed PR with exact selectors. Negative: raw `supported_by`, self-authored approval, missing selector, stale packet, or control-plane edit. Local: `define/SPEC.md#required-positive-witness`, `#required-single-fault-negatives`; `design/VALIDATION-CONTRACTS.md#vc-shape` through `#vc-projection`; findings `#candidate-skill-contracts`; research `#skill-contract-add-content`.

4) VALIDATION REPORT / RECEIPT — Phase-0 validation/projection receipt semantics are CURRENT Design-only; PR/scope/policy report is PROPOSED Phase 1; executable producer MISSING.
Producer: deterministic base-policy-bound validator/check suite. Consumer: reviewer, owner-decision gate, merge receipt, post-merge regenerator. Payload: receipt schema; candidate/task/policy/packet digests; head/base SHA; check ID + predicate version; tool/workflow identity; expected producer identity; exact input selector/digests; ordered diagnostics; result; output/artifact digest; invocation/run URL/time. Preconditions: candidate manifest digest matches head; verifier uses base-owned policy; dependencies resolved; no check-name-only trust. Postconditions: immutable fact “predicate P version V returned R for bytes D”; failure blocks only if actual repo rule says so. Authority: conformance fact only, never truth/fair interpretation/permission/approval. Threat: green-check laundering, unreproducible or mutable artifacts, skipped/neutral semantics accidentally accepted, check replay on new head. Versioning: predicate/tool/receipt versions explicit; report superseded—not rewritten—on new head. Positive: exact input + version rerun returns same diagnostics/output. Negative: same check name from wrong App or report head SHA mismatch => invalid receipt. Local: `define/SPEC.md` `ak.ValidationFact`; `design/ARCHITECTURE.md#receipt-writer`; `VALIDATION-CONTRACTS.md`; findings authority table. GitHub required checks may accept successful/skipped/neutral and can be restricted to an expected App—local policy must choose semantics: https://docs.github.com/en/repositories/configuring-branches-and-merges/managing-protected-branches/about-protected-branches .

5) REVIEW FINDING — outside Phase 0; PROPOSED, skill/report schema MISSING.
Producer: distinct `review-content` agent or human reviewer; consumer: candidate author, bound owners, owner-decision gate. Payload: finding ID/version; reviewer identity + capability/profile version (content-free); packet/policy/head digests; class (`provenance`, claim support, interpretation, licensing, safety, schema/relation, scope/parity); severity; affected selector/record/path; evidence/basis; required action; merge-blocking recommendation; status/supersession. Preconditions: not self-review; source accessible; exact candidate revision; reviewer does not rely on head-branch instructions for enforcement. Postconditions: attributable assessment, unresolved blockers preserved; repairs occur in later author commit and force revalidation/re-review. Authority: assessment only, not CODEOWNER approval or owner decision. Threat: self-review, inaccessible source, ambiguous rights/multiple defensible readings, finding self-resolution, stale review after push. Versioning: append-only/superseding per head SHA; closure by separately attributable response/owner decision. Positive: rights ambiguity finding blocks pending owner. Negative: reviewer authors candidate then marks own blocker resolved. Local: findings `#candidate-skill-contracts`; research `#skill-contract-review-content`, `#target-local-agent-strategy`. GitHub review states/configurable stale/latest-push rules are mechanisms, not proof configured: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews and ruleset URL above.

6) OWNER DECISION — outside Phase 0; PROPOSED and governance/publication owner UNBOUND/MISSING. DecisionRecords generally later; minimum merge-scope decision needed for Phase 1 must not become a broad publication/truth record.
Producer: explicitly bound human/team for a declared decision kind. Consumer: merge gate/receipt builder and later read model. Payload: decision ID/schema; subject (PR/candidate/finding); narrow decision kind (`allow_merge_for_policy_version`, rights disposition, claim-language disposition, etc.); bound owner identity/binding evidence; policy basis/digest; reviewed head SHA; state/effect; conditions; decided/effective time; expiry/revocation/supersedes; supporting receipts/findings. Preconditions: owner binding exists independently; all required subjects on exact head; no unresolved mandatory finding unless decision kind explicitly adjudicates it; separation from latest pusher if policy requires. Postcondition: only declared effect becomes effective. Authority: decision-kind-specific governance effect; never universal truth, source correctness, legal advice, publication, or every-use permission. Threat: invented owner, overloaded approval, stale-head approval, one owner standing in for distinct domains, contributor assertion masquerading as decision. Versioning: append-only, revocable/superseding; no mutation of history. Positive: bound rights owner resolves one stated rights question for exact candidate revision. Negative: role label `rights owner` with no actual binding => `OWNER_UNRESOLVED`. Local: findings authority table and `#unresolved-dissent-and-owner-bindings`; `ARCHITECTURE.md#authority-and-trust-extension`. GitHub CODEOWNERS identifies responsible users/teams but cannot prove expertise or independent multi-domain approval (CODEOWNERS URL above).

7) MERGE RECEIPT — outside Phase 0; PROPOSED, producer/schema MISSING.
Producer: trusted observer of GitHub repository action plus policy evidence; consumer: regeneration workflow, closeout, Inventory consumers. Payload: repository; issue/PR; base branch; pre-merge base SHA; reviewed head SHA; resulting base/merge commit SHA; merge method; actor/time; merged/closed state; exact check run IDs/producers/results; reviews and reviewed revision; unresolved-thread state; applicable ruleset/policy digest; bypass/indirect-merge indicators; changed-record digests. Preconditions: query actual remote event/state and verify resulting commit reachability; do not infer compliance from `merged=true`; expected-producer checks/reviews evaluated against policy snapshot. Postcondition: records repository action and observed policy facts; triggers regeneration only for exact merged base revision. Authority: merge fact, not semantic correctness/publication/acceptance. Threat: indirect merge, admin bypass, rebase/squash SHA confusion, stale reviews/checks, webhook replay. Versioning: receipt schema plus GitHub API version; append-only; correction receipt if observation wrong. Positive: PR merged through configured path, resulting base SHA verified, required evidence linked. Negative: head becomes reachable indirectly; GitHub says PR may be marked merged even when that PR’s protections were unsatisfied, so receipt must flag `indirect_merge`: https://docs.github.com/en/pull-requests/reference/pull-request-merges . Local: findings authority table and `#candidate-github-issue-to-pr-flow`; research `#observability-and-closeout`.

8) REGENERATION RECEIPT — Phase-0 projection receipt semantics CURRENT Design-only; trusted post-merge use is outside Phase 0, PROPOSED/MISSING.
Producer: trusted post-merge projector from merged base bytes, ideally isolated from candidate branch control. Consumer: retrieval publication step, closeout, context-packet builder. Payload: receipt/schema version; merge receipt digest; repository/base SHA; exact authored RecordSet paths/digests; schema/predicate/generator/projection/selector versions; resolved dependencies; output root/digest; parity result; invocation identity/time; attestation reference/signing identity if used. Preconditions: valid merge receipt; merged records pass validation; isolated temp build; one logical writer; generated root not hand-authored. Postconditions: identical bound inputs/versions reproduce byte-identical Inventory; complete receipt written last; failed parity does not replace last complete root. Authority: provenance/reproducibility fact only. Threat: build from unmerged head, mutable dependencies, partial replacement, stale generated bytes, attestation signature/signer not verified. Versioning: generator/projection versions explicit; content-addressed output; compatibility/migration declared before rewrite. Positive: clean rebuild matches output digest then atomic replacement. Negative: hand edit/stale output fails parity and old complete root remains. Local: `ARCHITECTURE.md#inventory-projector`, `#candidate-authoring-and-projection`, `#persistence-and-concurrency-extension`; `VALIDATION-CONTRACTS.md#vc-projection`. Primary provenance facts: in-toto Statement binds subject by digest and predicate by URI: https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md ; SLSA defines provenance as builder/run/build-definition metadata, not truth: https://slsa.dev/spec/v1.2/provenance ; GitHub attestations can bind SHA256 subject digest to workflow provenance but verification must validate signature/time/signer: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations and https://docs.github.com/en/rest/users/attestations .

9) DIGEST-BOUND CONTEXT PACKET — outside Phase 0; Phase-1 PROPOSED/MISSING. Persistent capability registry remains DEFERRED until multiple dispatch paths show need; capability profiles MUST remain content-free.
Producer: trusted selector/packet builder consuming merged Inventory and trusted base policy. Consumer: exactly one bounded agent task/reviewer; return/receipt verifier. Payload: packet schema/version/id/digest; task/issue snapshot digest; base-policy digest; merged base SHA + regeneration receipt digest; selected Inventory handles/authored IDs and projection digests; exact external source selectors; selection rationale; explicit omissions/nearby conflicts; allowed target paths/mutation scope; required checks/review classes; capability profile ID/version (reference only); expiry/freshness rule; non-authority notice. Preconditions: Inventory derived from merged bytes; all handles resolve to one authored origin; task/policy/Inventory dependencies digest-bound; packet does not store owner approval or become agent memory. Postconditions: consumer can reproduce selection and prove exactly what was supplied/omitted; return binds same packet/profile versions. Authority: non-authority read model; cannot approve claims, confer identity/status, or authorize production. Threat: stale/partial packet, omitted conflicting evidence, issue prose injected verbatim as policy, content copied into capability registry, overscoped agent mutation. Versioning: canonical serialization + digest; any dependency change creates new packet; stale packet fails, never silently refreshes. Positive: one task packet selects only needed handles/selectors and reproduces byte-for-byte. Negative: changed policy/Inventory digest or omitted declared dependency => `PACKET_STALE_OR_INCOMPLETE`. Local: findings `#capability-pool-and-context-packets`, `#smallest-positive-negative-witness-ladder`; research `#2-trusted-context-packet`, `#target-local-agent-strategy`; `define/glossary.md` Content packet. in-toto digest-binding is a suitable structural precedent, not automatic semantic suitability (Statement URL above).

CROSS-CONTRACT MINIMUM FLOW (inference, proposed): TaskSnapshot -> BasePolicyPacket + merged Inventory/regeneration receipt -> ContextPacket -> ContentCandidate -> ValidationReport + ReviewFindings -> OwnerDecision(s) -> MergeReceipt -> RegenerationReceipt -> new ContextPackets. Every arrow carries digest/version references; no downstream generated/report surface writes authority upstream.

DEFERRED / EXCLUDED: persistent capability registry until multiple routes witness selection need; Research Tower/Excerpt/Synthesis/EvidenceAssertion Phase 2; category/concept/graph Phase 3; RDF/SHACL/Olog later. Content-bearing agent profiles are KILLED, not deferred. GitHub artifact attestation is optional hardening, not a substitute for the domain-specific regeneration receipt or owner decision.

SOURCE FACTS VS INFERENCE VS OPEN QUESTIONS

Source facts are the local status/boundaries and current official platform/standard behaviors cited above. Contract field lists and diagnostic names beyond the two locally named Phase-1 predicates are bounded design inferences, not existing schemas. Open owner questions: actual named schema, identity, domain, rights, retrieval, governance, and ruleset owners; decision kinds; public/private publication boundary; content root/ID/date/deletion policies; ruleset/plan/visibility/bypass state; check producer identities and status semantics; merge method; packet canonicalization/expiry/omission policy; whether to use in-toto/SLSA/GitHub attestations; first staging cohort/reviewers; retention of source bytes/excerpts. No current evidence permits claiming any GitHub control is configured.
