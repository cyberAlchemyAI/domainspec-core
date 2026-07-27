# Findings — Akashic Contract Architecture

Dispatch: `2026-07-26-akashic-contract-architecture`  
Evidence state: research candidate awaiting registered audit  
Authority: research only; not Design acceptance, implementation, publication,
promotion, or owner binding

## Direct answer

Akashic Records can become a dependable library for people and agents by
keeping two promises separate:

1. **Phase 0:** contributors describe sources and make attributed claims;
   deterministic checks and a generated Inventory make those records findable
   without turning retrieval into truth or approval.
2. **Phase 1:** agents propose bounded changes; validation, review, typed human
   decisions, merge observation, and post-merge regeneration remain different
   facts.

The Phase-0 promise is coherent but exists only as Design. The public
Architecture self-identifies as an `authored-complete candidate`, says runtime
evidence is `none`, and leaves technical owners unbound. Validation fixtures
are planned and unexecuted. Research found four contract seams that should be
made explicit before implementation: selector behavior, canonical bytes,
diagnostic output, and supported version tuples.
[Architecture](../../../projects/akashic-records/development/phase-0-content-contract/design/ARCHITECTURE.md)
[Validation Contracts](../../../projects/akashic-records/development/phase-0-content-contract/design/VALIDATION-CONTRACTS.md)
[Reviewed synthesis](./synthesis-revised.md)

Private Inventory served only as a non-authority preflight lead. Claims here
were re-grounded in public Akashic artifacts, preserved explorer evidence, or
primary sources. “Current” below means an authored boundary, not deployed
behavior.

## Current contract inventory

| Surface | Producer → consumer | Current promise | Missing profile or binding |
| --- | --- | --- | --- |
| `SourceRecord` | contributor → validator/reader | Closed contributor-authored description of one resource at one declared level/scope; not the resource or an externally true fact. | Identity equality/normalization; schema, identity, rights owners. |
| `ClaimRecord` + embedded `EvidenceValue` | contributor → validator/projector/query | Attributed proposition with source reference, selector, relation, interpretation, and basis. | Selector/relation profiles; content owner. |
| validation fact/receipt | validators/writer → projector/harness | Conformance over exact inputs and versions; no assessment or approval. | Fact/receipt fields, diagnostic registry/precedence, serialization. |
| Inventory projection/parity | validated records → selector/readers | One deterministic entry per authored origin; no upstream write or minted identity/authority. | Generator, canonical byte profile, parity execution, owner. |
| bounded selector query | Inventory → person/agent/harness | Stable attributed results with selectors, rights, receipt state, and origin; no ranking/inference. | Grammar, normalization, state policy, typed outcomes. |
| version boundary | tuple registry → processors | Schema, predicate, selector, generator, and projection versions are explicit; no predecessor compatibility is promised. | Supported-tuple registry, processor binding, diagnostic, owner. |

These boundaries are already distributed across the
[Architecture](../../../projects/akashic-records/development/phase-0-content-contract/design/ARCHITECTURE.md)
and
[Validation Contracts](../../../projects/akashic-records/development/phase-0-content-contract/design/VALIDATION-CONTRACTS.md);
the exact gap analysis is in the [explorer record](./research.md).

## Missing, deferred, and killed

| Disposition | Candidate | Reason |
| --- | --- | --- |
| **Missing Phase-0 profile** | selector grammar/state/outcomes | `EvidenceValue`, locator expression, selected segment, and interpretation must remain distinct. Web Annotation is a separation precedent, not Akashic policy. [W3C](https://www.w3.org/TR/annotation-model/#selectors) |
| **Missing Phase-0 profile** | canonical bytes | Byte domain, serialization, encoding/newline, duplicate-key, digest, and receipt rules are unselected. RFC 8785 is only an Informational JSON candidate. [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html) |
| **Missing Phase-0 profile** | diagnostics | JSON Schema precedents output structure, not local IDs, precedence, receipts, or authority. [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-core#section-12) |
| **Missing Phase-0 profile** | supported five-part tuple | Processing needs an exactly-one lookup before parse/project; dialect identification is only a precedent. [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-core#section-8.1.1) |
| **Missing binding** | all technical/governance owners | Current role labels are responsibilities, not assigned people or teams. |
| **Deferred** | detailed agent/PR contracts | Phase 1 requires a separate future Design; no GitHub control is proved configured. |
| **Deferred** | migration/deprecation | No predecessor/successor pair, owner, loss policy, or witness exists. |
| **Deferred** | graph, ontology, RDF/SHACL, Olog | No failed direct-reference query, admission policy, graph witness, or arrow/path witness earns them. |
| **Killed as duplicate** | Phase-0 first-class evidence record; prose-only contract catalogue | Embedded `EvidenceValue` serves the current consumer; a prose catalogue adds drift but no rejection behavior. |
| **Killed as collapse** | content-bearing capability profile; self-authored authority fields | Separate content-free routing identity from context; separate authored contribution from assessment and typed decisions. |
| **Killed as ambiguous** | raw `supported_by`, generic `derived_from`/`is_part_of`, stored authored inverses | Keep typed embedded relations and generated inverse views. |

KILL means duplicate or lifecycle collapse. Lack of a witness alone means
DEFER, especially for semantic machinery. [Reviewer gates](./reviews.md)

## Phase map

```text
Phase 0: SourceRecord + ClaimRecord(EvidenceValue)
  → validation facts/receipts → Inventory projection → bounded query

Phase 1, external and non-normative here:
  TaskSnapshot + BasePolicySnapshot → ContextPacket → ContentCandidate
  → ValidationReport + ReviewFinding → typed decision
  → independent MergeReceipt → RegenerationReceipt

Phase 2: first-class evidence/assessment only when distinct lifecycle earns it
Phase 3: separate OntologyCandidate → separate ontology-admission decision
Phase 4: graph/RDF/SHACL/Olog only after discriminating real witnesses
```

This retains the public
[Phase-0 boundary](../../../projects/akashic-records/development/phase-0-content-contract/design/ARCHITECTURE.md)
rather than importing future records or controls.

## Agent contribution contracts

These are future Phase-1 interface stubs, not current schemas or controls.

| Stub | Producer → consumer | Minimum binding | Authority ceiling |
| --- | --- | --- | --- |
| bounded task | requester/triager → packet builder/agent/reviewer | task revision, base ref, cohort, selectors, path scope, review/closure criteria | request/triage fact |
| base-policy snapshot | verified base resolver → packet builder/validator | base SHA, policy digest, allowed paths, expected check producers/reviews | policy description, not enforcement |
| `ContextPacket` + `CapabilityProfileRef` | reproducible builder → one bounded agent | task/policy/base/projection/source digests, omissions, scope, expiry; profile ref is content-free | context/routing only |
| content candidate | agent/contributor → validators/reviewers | exact revision/diff, record manifest, task/policy/packet digests | attribution only |
| `ValidationReport` | report builder → reviewer/decision gate | receipts for one candidate revision/policy | aggregation, not fact or approval |
| review finding | independent reviewer → author/typed owner | revision, class, basis, selector, severity, action | scoped assessment only |
| typed decision | independently resolved owner → exact effect consumer | closed kind, subject, binding evidence, policy, conditions | only the named effect |
| `MergeReceipt` | verified remote observer → regenerator/closeout | event/resulting commit, checks/reviews, policy, bypass/indirect merge | repository action only |
| `RegenerationReceipt` | verified post-merge projector → retrieval/packet builder | merged base, exact inputs/versions, output digest, parity, producer | reproducibility only |

GitHub rulesets and CODEOWNERS are configurable mechanisms, not evidence that
Akashic has configured controls or bound qualified owners.
[Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
[CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
A remote receipt must also handle indirect-merge behavior.
[Pull-request merges](https://docs.github.com/en/pull-requests/reference/pull-request-merges)
[Operational explorer evidence](./research.md)

## Authority non-collapse

| Surface | May establish | Must not establish |
| --- | --- | --- |
| source description / claim | what a contributor recorded | external truth or permission |
| `EvidenceValue` / selector / selected segment | relation and locator; resolution under a profile | proof, accepted interpretation, or assessment |
| `ValidationFact` / `ValidationReceipt` | predicate result; immutable operation envelope | review, decision, or stronger authority |
| Inventory/query result | reproducible attributed read view | identity, confidence, meaning, acceptance |
| review finding | scoped assessor judgment | validator result or owner effect |
| typed decision | one exact effect by one bound owner | every downstream effect |
| `MergeReceipt` | observed repository action | authorization, publication, correctness |
| `OntologyCandidate` / admission | derived proposal; exact admitted semantic effect | authored identity, truth, permission, publication |

Selection does not prove support; validation does not become assessment;
assessment does not become decision; merge does not become publication;
publication does not become truth, permission, or ontology admission. PROV-O
supports keeping entities, activities, and agents distinct, but neither
requires RDF adoption nor confers authority.
[PROV-O](https://www.w3.org/TR/prov-o/)
[Provenance explorer evidence](./research.md)

## Compatibility, version, and migration policy

The present Phase-0 seam is fail-closed:

```text
lookup(schema, predicate, selector, generator, projection)
  → exactly one processor: processing may begin
  → zero processors: reject before parse/project
  → multiple processors: reject ambiguous registry
```

Registry contents, processor representation, diagnostic labels, and owner are
unresolved. The smallest witness changes only selector version and observes
lookup cardinality move from one to zero.

Compatibility is directional: future policy must separately state old-reader/
new-record, new-reader/old-record, and writer behavior. Migration remains
deferred until one old/new pair declares identity preservation or
supersession, loss, selector behavior, parity, rollback, effective date,
receipt behavior, owner, and witnesses. A migration receipt proves an
operation, not content correctness or semantic approval.
[Version synthesis](./synthesis-revised.md)

## Positive and single-fault-negative witness plan

All witnesses are planned; none has executed.

| Boundary | Positive | Change one fact → expected negative |
| --- | --- | --- |
| closed record | valid source and evidence-bearing claim | add unknown field → shape rejection |
| identity | A1/A2 reuse Source A | duplicate same-scope identity → rejection |
| evidence | A1 selector resolves to Source A | source ID becomes unknown → dangling rejection |
| rights | asserted license has basis or state is unknown | remove asserted basis → rejection |
| selector | supported expression resolves one segment | change state digest → mismatch; deferred until profile |
| diagnostic | bound tuple passes with ordered empty diagnostics | one predicate false → its one ordered diagnostic |
| bytes | same selected inputs/tuple yield same digest | flip generated byte → parity mismatch; profile unresolved |
| query | expression returns A1/A2, excludes B1 | make expression invalid → typed invalid result |
| version | tuple yields one processor | change selector version → zero; reject before processing |
| owner | evidence resolves one owner | replace evidence with role label → zero bindings |
| packet/migration/graph/Olog | real algorithm, pair, query, or arrows pass | change one dependency, identity disposition, endpoint, or path → fail; all deferred |

Existing names are in the
[Validation Contracts](../../../projects/akashic-records/development/phase-0-content-contract/design/VALIDATION-CONTRACTS.md).
New diagnostic labels remain inferences until publicly admitted.

## Five-column verdict matrix

“Owner” is a responsibility, not a bound person. “Witnessed” reports current
evidence, not execution.

| Candidate | Owner | Witnessed | Sound | Verdict |
| --- | --- | --- | --- | --- |
| source-description wording | schema/identity/content; unbound | current distinction | yes if folded | **MERGE clarification** |
| selector profile | retrieval/identity; unbound | profile absent | yes if locator/result/interpretation stay separate | **BUILD; unresolved** |
| canonical bytes | retrieval/projection; unbound | parity planned; profile absent | yes | **BUILD; unresolved** |
| diagnostic fact/receipt | schema/validator; unbound | discriminating pair planned | yes with fact/receipt split | **BUILD clarification** |
| supported tuple | interface roles; unbound | one-to-zero pair planned | yes if separate from migration | **BUILD clarification** |
| migration/deprecation | future compatibility; unbound | no version pair | yes in principle | **DEFER** |
| high-level Phase 1 | future roles; unbound | proposed, not executed | yes if external | **KEEP seam** |
| detailed Phase 1 | future roles; unbound | none | yes as future lifecycle | **DEFER** |
| Phase-0 evidence record | content; unbound | embedded value suffices | duplicate | **KILL** |
| content-bearing capability profile | routing; unbound | none | collapses context/routing | **KILL; split** |
| prose catalogue | no distinct consumer | none | duplicate | **KILL; fold** |
| graph/ontology | ontology; unbound | no query/policy | sound only with candidate/admission split | **DEFER** |
| RDF/SHACL/Olog | semantic/runtime; unbound | no substrate witness | undecided | **DEFER / exclude P0** |

[Reviewer corrections](./reviews.md)
[Revised synthesis](./synthesis-revised.md)

## Proposed public-safe Design delta

For `design/ARCHITECTURE.md`:

1. Clarify that “authored-complete” is self-description while the Design is
   owner-blocked, unaccepted, unimplemented, and profile-incomplete.
2. Call `SourceRecord` a contributor-authored source description.
3. Distinguish `EvidenceValue`, `SourceSelector`, and
   `SelectedSourceSegment`; list selector rules/outcomes as unresolved.
4. Define `ValidationFact`, `ValidationReceipt`, and `ProjectionReceipt`;
   mention future `ValidationReport`/`RegenerationReceipt` only in the external
   Phase-1 seam.
5. Qualify byte determinism with every unresolved byte-profile choice.
6. Add exactly-one supported-tuple lookup; keep migration/deprecation deferred.
7. Extend the existing authority table with typed decisions, independent merge
   observation, and separately identified ontology candidates.
8. Keep one compact Phase-1 flow external, deferred, and non-normative; keep
   `CapabilityProfileRef` content-free.
9. Defer graph/Olog witnesses until real query and arrow/path cases exist.

For `design/VALIDATION-CONTRACTS.md`:

1. Add the legend: current boundary, missing profile, planned witness, no
   execution.
2. Add planned `VC-DIAGNOSTIC` with bound fields, ordered-empty positive, and
   one-predicate/one-diagnostic negative; registry/serialization unresolved.
3. Add planned `VC-VERSION` with exactly-one, zero, and ambiguous lookups.
4. Qualify byte witnesses until a profile is selected; do not add
   `VC-SERIALIZATION`.
5. List selector outcomes but defer `VC-SELECTOR-STATE`.
6. Add typed negatives preventing Phase-0 outputs from becoming assessment,
   report, authorization, merge, publication, ontology candidate, or admission.
7. Defer migration, graph, and Olog fixtures until real objects exist.

Do not create `CONTRACT-CATALOG.md`. Public-ready text must cite public
artifacts or primary sources, never private Inventory, dispatch, telemetry, or
owner paths.

## Unresolved owners and dissent

No people or teams are bound for schema/validation, source identity, content,
rights, retrieval/bytes, compatibility, or later governance/ontology. Exact
selector, byte, diagnostic, tuple, and owner-resolution policies remain open.

The explorer tension is resolved as follows:

- a prose catalogue is killed; a machine registry may return only when real
  processors consume it and zero/multiple lookup changes behavior;
- present tuple rejection is added, while migration waits for a real pair;
- graph, RDF/SHACL, Olog, and ontology are deferred—not killed—because missing
  witnesses do not by themselves prove collapse.

External standards remain precedents, not local policy owners. No finding
authorizes implementation, acceptance, publication, promotion, or ownership.

## Concrete next action

The public Design owner may integrate only the bounded Architecture and
Validation edits above, preserving unresolved labels and the external
Phase-1 boundary. The next gate is to bind accountable owners and select the
four Phase-0 profiles—selector, bytes, diagnostics, and supported tuple—before
turning planned witnesses into executable tests.

