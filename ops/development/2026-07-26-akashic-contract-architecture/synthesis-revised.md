# Revised Synthesis — Akashic Contract Architecture

Dispatch: `2026-07-26-akashic-contract-architecture`  
Stage: synthesizer-reviewer zig-zag, revision 1 of 1  
Status: research synthesis candidate; not public Design authority

## Direct answer and evidence boundary

The public Design self-identifies as an `authored-complete candidate`, but the
evidence sustains a narrower operational statement: it is owner-blocked,
unaccepted, unimplemented, and contract-incomplete at the selector,
serialization, diagnostic-output, and supported-version-tuple seams. Its
fixtures are planned Design witnesses and none has executed. This synthesis
therefore distinguishes four states for every Phase-0 surface:

1. **current boundary or requirement** — already stated in the public
   Define/Design;
2. **missing normative profile** — behavior required by the boundary but no
   rule is selected;
3. **planned witness** — a named Design fixture, not an execution result;
4. **no execution** — no schema, validator, generator, selector, fixture run,
   or receipt establishes runtime behavior.

The target's status and claim boundary are explicit in
`design/ARCHITECTURE.md` (header, Design Objective, Validation Extension) and
`design/DESIGN-TRANSPORT.md#Claim-Boundary`. Abramsky §1 and Peirce's opening
inventory confirm the same limitation; Ashby's Audit Baseline confirms that
the Phase-1 workflow is proposed rather than configured.

External standards below are structural precedents only. Local contract
ownership remains with the currently described ownership roles, and no owner
is bound. JSON Schema does not own Akashic's cross-record laws, diagnostic
registry, tuple registry, receipts, migration, or deprecation. Web Annotation
does not select an Akashic selector grammar or state policy. RFC 8785 does not
select Akashic's digest, source-file byte domain, newline policy, or receipt
format. GitHub documentation describes configurable mechanisms, not current
repository configuration or human expertise. PROV-O, in-toto, SLSA, SKOS, and
Olog do not confer semantic correctness, authorization, or admission.
[Abramsky §§2–4; Peirce §§3–4; Ashby contracts 2, 4, 7–9; Popper corrections
1–11]

## 1. Phase-labelled contract catalogue

The IDs below are synthesis handles, not proposed public contract identities.
Public Design should retain existing surface names such as `SourceRecord`,
`ClaimRecord`, `ValidationFact`, `CompileInventory`, and `SelectContent`.

### Phase 0 — current public boundaries

| Surface | Producer → consumer | Current boundary or requirement | Missing normative profile | Planned witness | Execution |
|---|---|---|---|---|---|
| `SourceRecord` | contributor → shape/cross-record validator and reader | Closed contributor-authored description of exactly one resource at one declared level/scope; the record is not the source, and a captured-byte digest is not work identity. | Exact identity normalization and equality policy; accountable schema, source-identity, and rights owners. | `VC-SHAPE-POS-001`, `VC-IDENTITY-POS-DISTINCT-001`, duplicate and digest negatives. | None. [Abramsky `AK-REC-v0`, `AK-ID-v0`; Peirce `AK-PROV-01`; `design/ARCHITECTURE.md#Record-Store/#Cross-Record-Validator`; `design/VALIDATION-CONTRACTS.md#VC-SHAPE/#VC-IDENTITY`] |
| `ClaimRecord` with embedded `EvidenceValue` | contributor → shape/reference validator, projector, query | One attributed proposition with one-or-more embedded evidence values. Each value carries a source reference, `SourceSelector`, relation, interpretation, and basis. `EvidenceValue` is not a Phase-0 record kind or assessment. | Exact selector and relation profiles; content/domain owner. | Shape positives; A1/A2/B1 reference positives; missing/dangling/wrong-kind/killed-edge negatives. | None. [Abramsky `AK-EVID-v0`; Peirce `AK-PROV-02`; `design/GLOSSARY-CONSISTENCY.md`; `design/VALIDATION-CONTRACTS.md#VC-REFERENCE`] |
| `SourceSelector` and `SelectedSourceSegment` | claim author → reference validator and selector resolver | They are distinct: a selector is a typed locator expression; a selected segment is the resolver's result against a named source state. Neither is the claim, interpretation, or proof of support. Web Annotation supplies a separation precedent, not the local grammar. | Supported selector types, normalization, source-state mode, resolution input/output, and four outcomes: unsupported expression type, invalid expression, not found/successful empty, and state mismatch. No state-binding rule is selected. | Existing missing-selector negative only. State-drift and expression-validity witnesses are deferred until a profile is selected. | None. [Peirce `AK-PROV-03`, §§3–5; [W3C Web Annotation selectors and states](https://www.w3.org/TR/annotation-model/#selectors); `design/ARCHITECTURE.md#Selector-Engine`; Sattler selector/query corrections] |
| rights, time, and authority ceiling | contributor → validators | Asserted rights state requires basis; `unknown` invents no permission; update cannot precede creation; authored/generated fields cannot self-assign truth, review, acceptance, publication, permission, or promotion. | Rights-basis and excerpt policy; rights owner. | `VC-RIGHTS-*`, shape time/lifecycle negatives, `VC-PHASE0-NO-AUTHORITY-001`. | None. [Abramsky `AK-RTA-v0`; Peirce `AK-PROV-07`; `design/VALIDATION-CONTRACTS.md#VC-RIGHTS/#VC-PHASE-BOUNDARY`] |
| `ValidationFact` | shape/cross-record validator → projector and test/human consumer | Predicate result over exact bound inputs and named predicate/schema versions; it establishes conformance only. Diagnostic precedence is required to be stable. | Closed fact fields, complete diagnostic registry, deterministic precedence between all failure classes, and representation of the diagnostic array. | Current `VC-SHAPE`, `VC-IDENTITY`, `VC-REFERENCE`, `VC-RIGHTS`; no executed fact. | None. [Abramsky `AK-VAL-v0`; Peirce `AK-PROV-04`; `design/ARCHITECTURE.md#Receipt-Writer`; `design/VALIDATION-CONTRACTS.md#Fixture-Discipline`] |
| `ValidationReceipt` | receipt writer → projector, harness, later report builder | Immutable serialized envelope containing one or more `ValidationFact` values plus input selectors/digests, producer/tool versions, and emission provenance. A receipt does not strengthen the facts it encloses. | Receipt schema and canonical serialization. JSON Schema output structures are precedent for locations/output shape only. | No separate current receipt fixture. Candidate diagnostic witness: exact bytes and tuple produce pass with ordered empty diagnostics; changing one predicate yields its single ordered diagnostic. | None. [Abramsky `AK-VAL-v0`, §3; [JSON Schema output](https://json-schema.org/draft/2020-12/json-schema-core#section-12); Quine naming hierarchy; Sattler diagnostic correction] |
| Inventory projection | projector → selector engine and readers | A validation-passing exact RecordSet produces exactly one generated entry per authored origin, stable-ID order, and reverse lookup; no upstream writes and no minted identity, meaning, confidence, status, or authority. | Generator/projection implementation and owners. | `VC-PROJECTION-*`; `PLANNED-WITNESSES.json` determinism/parity witnesses. | None. [Abramsky `AK-PROJ-v0`; Peirce `AK-PROV-05`; `design/ARCHITECTURE.md#Inventory-Projector`; `design/VALIDATION-CONTRACTS.md#VC-PROJECTION`] |
| `ProjectionReceipt` and parity | projector/parity checker → generated-store consumer and harness | Receipt is the operation envelope for projection; identical selected inputs and versions are required to produce identical output bytes; stale/hand-edited/incomplete output must not replace the last complete root. | Authored-input byte domain, generated byte serialization, UTF-8/newline rules, duplicate-key behavior, digest algorithm, and receipt format. Until selected, “byte-identical” is a local Design requirement, not interoperable behavior. RFC 8785 is only an Informational candidate for generated JSON canonicalization. | Current determinism, input-change, stale, hand-edit and upstream-write fixtures are planned. | None. [Abramsky `AK-PARITY-v0`, §§2–3; `design/ARCHITECTURE.md#Persistence-and-Concurrency-Extension`; `design/VALIDATION-CONTRACTS.md#VC-PROJECTION`; [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html)] |
| bounded query result | selector engine → curator, agent, harness | Versioned finite selector over a complete projection returns stable ordered results or a typed outcome, preserving attribution, source selector, rights, receipt boundary, and exactly one authored origin; it does not rank, infer, traverse a semantic graph, or establish authority. | Query expression grammar and typed outcomes: unsupported, invalid, not found, successful empty, and successful non-empty. | Current A1/A2-versus-B1 discrimination, attribution, and origin witnesses. Expression-validity witness awaits the selector profile. | None. [Abramsky `AK-QUERY-v0`; Peirce `AK-PROV-06`; `design/ARCHITECTURE.md#Selector-Engine`; `design/VALIDATION-CONTRACTS.md#VC-SELECTOR`] |
| supported interface tuple | tuple registry → validator, reader, projector, selector resolver | Each interface already carries schema, predicate, selector, generator, or projection version, and Phase 0 promises no predecessor compatibility. A supported-tuple lookup is the present missing compatibility seam, separate from future migration. | Registry entries and owner; exact lookup input/output; `UNSUPPORTED_CONTRACT_TUPLE` is only a candidate label. Required behavior: exactly one processor binding permits processing; zero or multiple bindings reject before record parse/projection. JSON Schema dialect identification is precedent only. | New planned `VC-VERSION` may use one supported tuple; changing only selector version changes lookup cardinality from one to zero. | None. [Abramsky `AK-VERSION-v0`, §§2–4; `design/ARCHITECTURE.md#Integration-and-Versioning-Extension`; [JSON Schema dialect identification](https://json-schema.org/draft/2020-12/json-schema-core#section-8.1.1); Sattler tuple correction] |

### Phase 1 — external/deferred, non-normative interface stubs

The Phase-0 Design already names GitHub controls, context packets, review,
merge, and post-merge generation as external. It should retain only this
high-level seam. The detailed fields below are research candidates for a
separate future Phase-1 Design; they are not normative additions to Phase 0,
not configured controls, and not implementation claims. [Popper classification
corrections; Quine correction 3; `design/ARCHITECTURE.md#Context-View` and
`#Candidate-Authoring-and-Projection`]

| Future stub | Producer → consumer | Minimum distinct behavior and authority ceiling | Status |
|---|---|---|---|
| bounded task snapshot | requester/triager → packet builder/contributor/reviewer | Binds exact task revision, base ref, objective, cohort, selectors, path scope, review classes and closure criteria; request/triage fact only. | External/deferred; detailed envelope build-from-owned. [Ashby contract 1] |
| base-policy snapshot | resolver whose base ref, policy paths, bytes, producer identity, tool/version and verification result satisfy named predicates → packet builder/validator/reviewer | Binds base SHA, policy digest, allowed/forbidden paths, expected check producers and review rules; describes a policy snapshot, not enforcement. GitHub mechanisms are configurable precedents only. | External/deferred. [Ashby contract 2; [GitHub ruleset rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets); [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)] |
| `ContextPacket` with `CapabilityProfileRef` | packet builder satisfying dependency-resolution/freshness predicates → one bounded agent/reviewer | Packet binds task/policy/base/projection/source-selection digests, omissions, allowed paths and expiry. `CapabilityProfileRef` is content-free routing identity only; packet content and selected handles cannot mutate or establish capability. | External/deferred; freshness algorithm unresolved. [Ashby contract 9; Quine corrections 7–8] |
| content candidate | contributor → Phase-0 validators and reviewers | Exact candidate revision/diff and record bytes bind to task/policy/packet; contribution attribution only. | External/deferred bridge to Phase 0. [Ashby contract 3] |
| `ValidationReport` | Phase-1 report builder → reviewer and decision gate | Aggregates `ValidationReceipt` values for exactly one candidate revision and policy snapshot; it is not itself a fact, review, or authorization. | External/deferred. [Ashby contract 4; Quine naming hierarchy] |
| assessment/review finding | independent reviewer/assessor → author and typed decision owner | Attributable judgment over exact subject/revision, class, basis and selectors; distinct from `EvidenceValue`, validation, and authorization. | External/deferred. [Peirce `AK-LIFE-01`; Ashby contract 5] |
| typed decision | independently bound owner → exact effect consumer | Closed `decision_kind`; merge authorization, rights disposition, publication, and ontology admission remain separate. Owner resolution must yield exactly one valid binding for kind/subject/policy; a role label yields zero. | External/deferred; currently described ownership roles, no bound owners. [Peirce `AK-LIFE-02`; Ashby contract 6; Quine corrections 5, 14] |
| `MergeReceipt` | remote repository observer satisfying repository/ref/event/API-version and verification predicates → regenerator/closeout | Joins merge authorization and observed repository facts, but is produced independently of the authorization. It records repository action, policy evidence, bypass/indirect merge and resulting commit; no semantic or publication effect. | External/deferred; GitHub merge behavior is precedent only. [Ashby contract 7; [GitHub pull-request merges](https://docs.github.com/en/pull-requests/reference/pull-request-merges); Quine correction 6] |
| `RegenerationReceipt` | post-merge projector satisfying base-reachability, producer/tool-version, policy-digest and parity predicates → retrieval/packet builder | Operation receipt over merged authored bytes and generated output; distinct from `ProjectionReceipt` by its merge/base-policy binding. | External/deferred. in-toto and SLSA are digest/provenance precedents only. [Ashby contract 8; [in-toto Statement](https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md); [SLSA provenance](https://slsa.dev/spec/v1.2/provenance)] |

### Phase 2 and later

| Surface | Required separation | Admission status |
|---|---|---|
| first-class evidence record | Separately authored evidence proposition/value with its own lifecycle; not an assessment. It is earned only by independent authorship, conflicting interpretations, review, reuse, or lifecycle that embedded `EvidenceValue` cannot represent. | Deferred to Phase 2. Phase-0 duplicate is **KILL**: keep embedded `EvidenceValue`. [Peirce §4; Quine corrections 10 and surviving KILLs] |
| assessment record | Attributable scoped judgment with assessor, subject, basis, selectors, kind, version and time; not validation or evidence. | Deferred to Phase 1/2 consumer. [Peirce `AK-LIFE-01`] |
| `OntologyCandidate` | Separately identified derived candidate that references authored origins; it never reuses authored record identity. Candidate derivation is not ontology admission. | Deferred to Phase 3 until a named query fails under direct references and succeeds under a typed candidate. [Peirce `AK-SEM-01`; Quine correction 9; Sattler graph correction] |
| ontology admission | Typed decision by a genuinely bound ontology owner over an exact candidate/scheme/policy/version; only its declared semantic effect is produced. | Deferred; no owner/query/policy/witness. SKOS is a structural distinction precedent only. [Peirce §§2–4; [SKOS Reference](https://www.w3.org/TR/skos-reference/)] |
| RDF/SHACL or Olog substrate | Technical substrate, separate from semantic admission. Olog eligibility additionally requires repeated total functional arrows, instance path equations and a mapping need. | Deferred/excluded from Phase 0, not killed merely for absent witness. Olog witness waits for a real arrow/path pair. [Abramsky §1; `design/ARCHITECTURE.md#Decision-Flow-View`; Sattler and Quine corrections] |
| deprecation and migration | Future transition policy over a concrete old/new tuple pair, separate from present supported-tuple rejection. Must state identity preservation/supersession, loss, selector behavior, parity, rollback and receipt. | Deferred until a successor pair and owner exist. Missing-identity, lossy-field, parity and rollback witnesses are not Phase-0 fixtures. [Abramsky §§3–4; Peirce `AK-VERS-01`; Sattler migration correction; Quine correction 11] |

### Killed duplicates and preserved deferrals

**KILL because duplicate or collapsed:**

- a Phase-0 first-class `EvidenceAssertion`: merge current behavior into
  embedded `EvidenceValue`;
- content-bearing capability profiles: use a content-free
  `CapabilityProfileRef` plus a separate digest-bound `ContextPacket`;
- prose-only `CONTRACT-CATALOG.md`: fold useful summary into current
  Architecture and Validation Contracts;
- raw `supported_by`, generic `derived_from`, generic `is_part_of`, and stored
  authored inverses: retain typed embedded relations and generated inverse
  views;
- self-authored review, acceptance, publication, permission, truth, promotion,
  or other owner-effect fields: keep later assessment and typed decision
  contracts separate.

**DEFER, not KILL solely for absent witness:** deprecation, migration,
RDF/SHACL, Olog, semantic graph projection, and ontology admission.
[Abramsky §1 and §4; Peirce §4; Quine surviving KILLs and final instruction]

## 2. Producer-consumer dependency map

```text
Phase 0

Contributor
  ├─ SourceRecord ─┐
  └─ ClaimRecord
       └─ embedded EvidenceValue
            ├─ SourceSelector
            └─ contributor interpretation/basis
                    │
                    v
              Shape Validator
                    │
                    v
          Cross-Record Validator
                    │
          ValidationFact(s)
                    │
          ValidationReceipt
                    │
                    v
           Inventory Projector
              ├─ Generated Inventory
              └─ ProjectionReceipt
                    │
              Parity Checker
                    │
                    v
             Selector Engine
              ├─ SelectedSourceSegment
              └─ bounded attributed query result

External Phase-1 seam, non-normative here

TaskSnapshot + BasePolicySnapshot + prior RegenerationReceipt
  → ContextPacket(CapabilityProfileRef only)
  → ContentCandidate
  → ValidationReport(ValidationReceipts) + ReviewFindings
  → typed merge authorization / rights disposition / publication decision
  → independent remote MergeReceipt
  → RegenerationReceipt
  → later fresh ContextPackets

Later semantic seam

authored origins + selected claims + separate assessment
  → separately identified OntologyCandidate
  → typed ontology-admission decision
  → exact admitted effect under one scheme/policy
```

Every edge must bind exact identities, versions and/or digests before it can
support reproducibility. No downstream generated surface writes authority or
identity upstream. The Phase-1 nouns are interface stubs, not Phase-0
normative records. [Abramsky contract matrix; Peirce §2; Ashby cross-contract
flow; `design/ARCHITECTURE.md#Dependency-and-Interface-View`]

## 3. Lifecycle and authority non-collapse

| Surface | What it can establish | What it cannot establish |
|---|---|---|
| authored fact | contributor recorded value V in record R | external truth |
| source description | contributor's identification/description of resource S | S itself, claim support, reuse permission |
| `EvidenceValue` | contributor's claim-local relation, interpretation, basis and source reference | independent evidence record, assessment, proof |
| `SourceSelector` | locator expression | selected bytes/segment, interpretation, evidential support |
| `SelectedSourceSegment` | resolver result against named source/state under a profile | claim, proof, accepted interpretation |
| `ValidationFact` | predicate outcome over bound inputs/version | assessment, review, decision |
| `ValidationReceipt` | immutable operation/provenance envelope for facts | stronger facts or authority |
| Inventory/query result | deterministic attributed read view | authored identity, confidence, meaning, acceptance |
| `ValidationReport` | Phase-1 aggregation for one candidate revision | new conformance fact, review, authorization |
| assessment/review finding | assessor's scoped attributable judgment | validator result, universal truth, owner effect |
| typed decision | exact effect of one closed decision kind by one resolved owner | every downstream effect |
| `MergeReceipt` | independently observed repository action and joined policy evidence | merge authorization, publication, semantic correctness |
| publication effect | publish/unpublish effect of a publication decision | truth, rights permission, ontology admission |
| `OntologyCandidate` | separately identified derived semantic proposal with authored-origin references | authored record identity, admitted meaning |
| ontology admission | exact admitted effect under one scheme/policy/version | truth, permission, publication, general production authorization |

There is no automatic conveyor: selector resolution does not entail evidential
support; validation does not entail assessment; assessment does not entail a
typed decision; merge authorization does not entail an observed merge; merge
does not entail publication; publication does not entail truth, permission, or
ontology admission. [Peirce §2; Ashby contracts 4–8;
`design/ARCHITECTURE.md#Authority-and-Trust-Extension`]

## 4. Version and compatibility candidate

### Present Phase-0 seam

The Design already requires explicit schema, predicate, selector, generator,
and projection versions and promises no predecessor compatibility. Clarify a
single fail-closed lookup:

```text
lookup(schema_version,
       predicate_version,
       selector_version,
       generator_version,
       projection_version)
  -> exactly one processor binding: processing may begin
  -> zero bindings: reject before parse/project
  -> more than one binding: reject ambiguous registry
```

The registry contents, processor-binding representation, local diagnostics,
and accountable owner remain unresolved. Changing only the selector version
must be sufficient to move a witness from one binding to zero. JSON Schema's
`$schema` handling only precedents explicit dialect selection or failure; it
does not own this five-part tuple. [Abramsky `AK-VERSION-v0`; [JSON Schema Core
§8.1.1](https://json-schema.org/draft/2020-12/json-schema-core#section-8.1.1);
Sattler supported-tuple correction]

### Directional compatibility, deprecation, and migration

These remain future policy, not present Phase-0 contracts. A future owner must
separately declare reader compatibility, writer compatibility, identity
preservation or supersession, selector behavior, projection parity, loss,
rollback, effective date, and receipt behavior for one concrete old/new pair.
No version is deprecated and no migration witness is added before such a pair,
policy, owner, and consumer exist. A migration operation fact cannot approve
content or meaning. [Abramsky §4; Peirce `AK-VERS-01`; Sattler
`VC-MIGRATION-ADMISSION` correction]

## 5. Smallest positive and single-fault negative witnesses

| Boundary | Smallest positive | Single changed fact and expected observation | Current status |
|---|---|---|---|
| closed record | one valid `SourceRecord`; one valid evidence-bearing `ClaimRecord` | add one unknown field → shape rejection | Planned in `VC-SHAPE`; no run. |
| identity reuse | A1 and A2 reuse one Source A at same level/scope | add a second SourceRecord with same bound identity → duplicate rejection | Planned in `VC-IDENTITY`; no run. |
| evidence endpoint | A1 selector points to Source A | change only source ID to unknown → dangling rejection | Planned in `VC-REFERENCE`; no run. |
| rights basis | asserted license has basis, or rights is `unknown` | remove only asserted basis → rights rejection | Planned in `VC-RIGHTS`; no run. |
| selector profile | one supported type, normalization rule, and declared state mode resolves one segment | change only bound source-state digest → state mismatch | **Deferred until profile/state policy selected.** Preserve typed zeroes: unsupported, invalid, not found/empty, state mismatch. |
| diagnostic fact/receipt | exact bytes and predicate tuple yield pass with ordered empty diagnostic array | change one predicate true→false → one diagnostic at its selected precedence | **Add Design field/precedence contract;** serialization unresolved; no run. |
| canonical output bytes | same selected input-byte domain and version tuple yields same output stream/digest | flip one generated byte → parity mismatch | Existing planned parity witness, but **profile unresolved**; no interoperable-byte claim. |
| bounded query | supported expression returns A1/A2 in stable order and excludes B1 | change only expression validity under the selected grammar → invalid-expression outcome | Existing discrimination witness; expression negative deferred until grammar selected. |
| supported tuple | exact tuple lookup returns one processor binding | change only selector version → lookup cardinality one→zero and reject before parse/project | **Add planned `VC-VERSION`;** registry unresolved; no run. |
| typed owner resolution | independent binding resolves exactly one owner for one kind/subject/policy | replace binding evidence with role label → zero bindings/`OWNER_UNRESOLVED` | Future Phase-1/owner contract; no current owner. |
| context freshness | explicit algorithm reproduces packet from all dependency digests | change only policy digest → stale packet | Deferred until freshness algorithm selected. |
| migration | concrete old/new pair declares identity/loss/parity/rollback/receipt | remove one identity disposition → admission rejection | Deferred until pair/policy exists. |
| graph admission | named query fails under direct references and succeeds under a typed candidate | remove one endpoint/algebra element → query invariant fails | Deferred until real query/candidate exists. |
| Olog admission | real repeated total arrows and path equation satisfy required mapping | make one arrow partial or paths unequal → admission fails | Deferred until real arrow/path pair exists. |

Existing fixture names and claims come from
`design/VALIDATION-CONTRACTS.md` and `design/PLANNED-WITNESSES.json`. Candidate
failure labels outside those files are Design inferences and must not be
presented as current registry entries. [Popper correction 10]

## 6. Candidate verdicts

| Candidate | Local owner surface | External precedent boundary | Witness status | Verdict |
|---|---|---|---|---|
| source-description wording | currently described schema/source-identity/content roles; no bound owners | Web Annotation/DOI distinctions only | current glossary/authority distinction | **MERGE clarification into existing Record Store/authority prose; not a new contract** |
| selector profile | retrieval/projection and source-identity roles; unbound | Web Annotation separates Selector/State but selects no grammar | missing profile; current selector fixtures insufficient for state | **BUILD-FROM-OWNED seam; unresolved** |
| canonical bytes | retrieval/projection role; unbound | RFC 8785 is an Informational generated-JSON candidate only | parity planned; byte profile absent | **BUILD-FROM-OWNED seam; unresolved** |
| diagnostic fact/receipt fields and precedence | schema/validator role; unbound | JSON Schema output structures only | add discriminating planned fact witness | **BUILD-FROM-OWNED clarification** |
| supported tuple lookup | interface roles; unbound | JSON Schema dialect selection/failure only | one→zero binding witness defined | **BUILD-FROM-OWNED clarification** |
| deprecation/migration | future compatibility/migration owner; none bound | no external source supplies local policy | no old/new pair | **DEFER** |
| repeated authority explanation | existing Design authority section | PROV-O structural separation only | no distinct producer/consumer | **FOLD into existing section; no new contract** |
| high-level Phase-1 seam | future governance/retrieval/ruleset roles; none bound | GitHub mechanisms only | already publicly proposed | **KEEP existing external seam** |
| detailed Phase-1 envelopes/receipts | future roles; none bound | GitHub/in-toto/SLSA structural precedents only | no configuration/execution | **DEFER to separate Phase-1 Design** |
| first-class Phase-0 evidence record | content/domain role; unbound | none needed | embedded `EvidenceValue` satisfies current consumer | **KILL duplicate; defer future record until distinct lifecycle witness** |
| content-bearing capability profile | future routing role | none | collapses routing identity and task content | **KILL; use `CapabilityProfileRef` + separate packet** |
| prose-only contract catalogue | no distinct owner/consumer | none | no failure behavior | **KILL; fold summary into current files** |
| semantic graph / ontology admission | future ontology role; missing | SKOS distinctions only | no real query failure/admission policy | **DEFER, not KILL** |
| RDF/SHACL/Olog substrate | future semantic/runtime roles | structural traditions only | no real substrate witness | **DEFER/exclude from Phase 0, not KILL** |

## 7. Exact public Design deltas

Only the following bounded edits are recommended. They preserve the public
status as authored candidate, keep Phase 1 non-normative, and do not select
unowned rules.

### `design/ARCHITECTURE.md`

1. **Header / Design Objective:** after the current status, add:
   “The artifact self-identifies as authored-complete. It remains
   owner-blocked, unaccepted, unimplemented, and incomplete where this document
   explicitly leaves selector, serialization, diagnostic-output, and supported
   version-tuple profiles unresolved. Planned witnesses are not executed
   evidence.”

2. **Record Store:** fold in one sentence rather than a new section:
   “A `SourceRecord` is a contributor-authored source description, not the
   source resource or an externally true source fact.”

3. **Selector Engine:** distinguish:
   - `EvidenceValue`: claim-local relation, interpretation, basis, and source
     reference;
   - `SourceSelector`: locator expression;
   - `SelectedSourceSegment`: resolver result against a named source/state.

   Then state that supported selector types, normalization, source-state mode,
   resolution behavior, and the distinction among unsupported, invalid, not
   found/successful empty, and state mismatch remain unresolved owner
   decisions. Do not require state binding or add a state witness yet. Web
   Annotation may be cited only as a separation precedent:
   [W3C Web Annotation selectors and
   states](https://www.w3.org/TR/annotation-model/#selectors).

4. **Receipt Writer:** establish the naming hierarchy:
   - `ValidationFact`: predicate result over bound inputs;
   - `ValidationReceipt`: immutable serialized envelope for facts and operation
     provenance;
   - `ProjectionReceipt`: projection operation envelope;
   - future `ValidationReport`: Phase-1 aggregation for one candidate revision;
   - future `RegenerationReceipt`: post-merge operation envelope.

   State that receipt serialization is unresolved and never strengthens the
   authority of enclosed facts.

5. **Persistence and Concurrency Extension:** qualify byte determinism:
   “Identical inputs and versions are required to produce identical generated
   bytes under one selected byte profile. The authored-input byte domain,
   generated serialization, UTF-8/newline policy, duplicate-key handling,
   digest algorithm, and receipt format are not yet selected; interoperable
   byte determinism is therefore not established.” RFC 8785 may be named only
   as an Informational candidate for generated JSON:
   [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html).

6. **Integration and Versioning Extension:** replace the current final
   sentence with two paragraphs:
   - present seam: exact five-part tuple lookup must resolve to one processor;
     zero or multiple bindings reject before parse/project; registry,
     diagnostics, processor representation, and owner remain unresolved;
   - future seam: compatibility directions, deprecation, and migration are
     deferred until a concrete successor pair declares identity, loss,
     selector behavior, parity, rollback, receipt, owner, and witnesses.

   JSON Schema may be cited for explicit dialect identification/failure only:
   [JSON Schema Core
   §8.1.1](https://json-schema.org/draft/2020-12/json-schema-core#section-8.1.1).

7. **Authority and Trust Extension:** expand the existing table, not a new
   parallel authority section, with `assessment`, typed decision, future
   `ValidationReport`, independently observed `MergeReceipt`, publication
   effect, `OntologyCandidate`, and ontology admission. Use “currently
   described ownership roles; no bound owners.” Replace every adjectival
   “trusted” construction with named predicates over base ref, producer
   identity, tool/version, policy digest, and verification result.

8. **Context and Dependency views:** retain the already-present high-level
   Phase-1 seam only. It may name:
   `TaskSnapshot + BasePolicySnapshot → ContextPacket → ContentCandidate →
   ValidationReport + ReviewFinding → typed decision → independently observed
   MergeReceipt → RegenerationReceipt`.
   Label every noun external/deferred and non-normative. Define
   `CapabilityProfileRef` as content-free routing identity. Move all detailed
   envelope fields and GitHub rules to a future Phase-1 Design.

9. **Later mechanism admission:** clarify that an `OntologyCandidate` receives
   a separate derived identity and references authored origins; it never reuses
   authored identity. Candidate derivation and typed ontology admission are
   separate. Defer graph and Olog witnesses until a real failed query and real
   arrow/path pair exist.

### `design/VALIDATION-CONTRACTS.md`

1. Add a short **Contract state legend** distinguishing current boundary,
   missing normative profile, planned witness, and no execution.

2. Add **VC-DIAGNOSTIC** as planned Design evidence:
   - positive: exact bound bytes and predicate tuple yield pass and an ordered
     empty diagnostic array;
   - negative: change exactly one predicate true→false and receive exactly its
     diagnostic at the selected precedence.

   Require fact fields for bound inputs/digests, schema/predicate versions,
   verdict, ordered diagnostics, producer/tool version, and emission
   provenance. Keep receipt serialization and concrete diagnostic registry
   unresolved.

3. Add **VC-VERSION** as planned Design evidence:
   - positive: exact `(schema, predicate, selector, generator, projection)`
     lookup returns one processor binding;
   - negative: change only selector version and lookup returns zero, rejecting
     before record parsing/projection;
   - ambiguity: multiple bindings reject.

   State that registry contents and diagnostic labels remain unresolved.

4. Revise **VC-PROJECTION** preamble to say its byte witnesses become
   executable only after a byte profile selects the input domain,
   serialization, encoding/newline, duplicate-key and digest rules. Do not add
   a separate `VC-SERIALIZATION` group yet.

5. Revise **VC-SELECTOR** preamble to separate unsupported, invalid, not found,
   successful empty, successful non-empty, and state mismatch as required
   future outcome classes. Do not add `VC-SELECTOR-STATE` until a state policy
   is selected.

6. Extend **VC-PHASE-BOUNDARY** with typed negatives showing that no Phase-0
   output is an assessment, `ValidationReport`, merge authorization,
   `MergeReceipt`, publication effect, `OntologyCandidate`, or ontology
   admission.

7. Do not add `VC-MIGRATION-ADMISSION`, graph, or Olog fixtures until their
   real old/new pair, policy, failed query, or arrow/path objects exist.

### `CONTRACT-CATALOG.md`

Do **not** create it. A prose catalogue has no distinct consumer or validation
purpose and would duplicate the Architecture and Validation Contracts. A
future machine registry earns a distinct artifact only when processors consume
it and validation rejects zero/multiple processor bindings or
unregistered/multiply-owned contracts. [Abramsky §4; Quine surviving KILLs]

## 8. Reviewer-response matrix

| Reviewer requirement | Revision response |
|---|---|
| Separate local owners from precedent; roles are unbound | Every catalogue/verdict row names the local role separately and says no owner is bound; the opening narrows each external source. |
| Classify source-description/high-level P1 as already public; details build-from-owned | Source-description is folded into existing Record Store wording; the P1 seam is retained as already proposed while detailed envelopes are deferred. |
| Narrow JSON Schema, Web Annotation, RFC 8785, GitHub, PROV-O/in-toto/SLSA/SKOS claims | Each source is explicitly a structural precedent with the exact local choices it does not supply. |
| New fields/diagnostics are inferences; exclude non-public evidence from public text | Candidate labels are marked unresolved; exact public deltas cite only public selectors and primary URLs. |
| Selector positive/negative must be discriminating | Required types/normalization/state mode and typed outcomes are stated; the state witness is deferred until policy selection. |
| Fact/receipt diagnostic boundary and precedence | `ValidationFact`, `ValidationReceipt`, fields, empty-array positive and one-predicate negative are specified; serialization remains unresolved. |
| Canonical bytes cannot be claimed before profile selection | Byte domain, serialization, encoding/newline, duplicates and digest are listed unresolved; current parity is a planned requirement only. |
| Query outcomes must not collapse | Unsupported, invalid, not found, successful empty/non-empty, and state mismatch are separated. |
| Supported tuple must have one→zero lookup witness | The present five-part registry lookup and selector-version single-fault negative are explicit; rejection occurs before processing. |
| Migration witness deferred until successor pair | Migration/deprecation are separated from current tuple lookup and deferred with their future admission fields. |
| Owner decision needs independent binding witness | Typed decisions require exactly one independent binding; replacing evidence with a role label yields zero/`OWNER_UNRESOLVED`. |
| Packet freshness only after algorithm exists | Phase-1 packet is a stub and freshness witness is deferred until an explicit algorithm. |
| Graph/Olog witnesses require real query/arrows | Both witnesses are deferred; authority-collapse negatives are not used as need evidence. |
| Status must separate authored claim, completeness, witnesses and execution | The direct answer and Phase-0 catalogue use the four-state classification explicitly. |
| Phase-1 must remain external/non-normative in Phase-0 Design | Phase-1 has one compact seam only; detailed normative contracts are routed to a future artifact. |
| Establish naming hierarchy | `ValidationFact`, `ValidationReceipt`, `ValidationReport`, `ProjectionReceipt`, and `RegenerationReceipt` are defined and non-collapsed. |
| Typed decisions and independent merge observation | Four decision kinds are separated; `MergeReceipt` is produced by a remote observer and joins authorization as input. |
| Replace adjectival trust with predicates | Base ref, producer identity, tool/version, policy digest and verification result are named predicates throughout. |
| Keep capability routing identity content-free | `CapabilityProfileRef` is routing identity only; task content and selected handles remain in `ContextPacket`. |
| Candidate and admission; authored and derived identity | `OntologyCandidate` has separate derived identity referencing authored origins; ontology admission is a typed later decision. |
| Evidence, selector, selected segment, and assessment must not collapse | All four are separate in the catalogue, dependency map, and authority map. |
| Do not publish competing synthesis IDs | Synthesis IDs are explicitly temporary handles; public names retain existing operation/surface vocabulary. |
| Preserve KILL versus DEFER distinctions | Duplicate/collapsed constructs are KILL; deprecation, migration, semantic graph, RDF/SHACL, Olog and ontology admission remain deferred. |

## Concrete next action

The public Design owner may admit only the bounded edits in §7 after confirming
that selector, byte, diagnostic, and tuple choices remain explicitly unresolved
and that the extra Phase-1 terms are non-normative external seams. No schema,
validator, fixture execution, GitHub configuration, migration, graph,
ontology, implementation, publication, or owner binding follows from this
synthesis.
