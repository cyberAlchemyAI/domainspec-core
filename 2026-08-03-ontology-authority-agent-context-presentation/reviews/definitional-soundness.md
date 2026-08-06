# Definitional soundness review

## Verdict: block

The synthesis correctly separates confidence from commitment, lifecycle from authority, and candidate-local validation from runtime or release. It also bounds “world model” against complete-world truth.

Five load-bearing repairs are required before evidence closure.

### 1. Mark the opening as author voice, not a canonical definition

“Approved definition” can be misheard as CAV2-governed terminology. Approval here is voice approval only.

Replace the moment label:

> Author’s approved opening

Use this spoken bridge:

> Ontologies are knowledge spaces: bounded models of the part of a world a domain cares about. They contain selected concepts and typed relations—including interactions where those are evidenced—and carry time, confidence, provenance, lifecycle, and rules for use. That is my accessible framing; CyberAlchemy v2 adds the governed meaning contract. Neither framing makes an ontology a complete truth model or an authority owner.

Binding: `dispatch-sheet.json#/context`; `live-presentation-language-audition.md#/Opening`; `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md:873-967`.

### 2. Do not make ontology, context, retrieval, or authority into runtime actors

These lines collapse artifacts with processes:

- “Inventory or retrieval finds source-backed evidence.”
- “Ontology interprets selected evidence.”
- “Context packages the task-relevant slice.”
- “Authority governs reliance and action.”
- “Memory retains candidates; context selects … ontology interprets it.”

Replace the shorthand with:

> Find candidate evidence. Type meaning. Bound context. Gate use.

Replace the speaker-notes chain with:

> owned source or event → Inventory or retrieval makes candidate evidence and selectors findable → explicit evidence selection → ontology-governed typed meaning, relations, time, confidence, and provenance → a context builder packages a bounded task view with warnings → a named authority owner permits or denies reliance → a separate workflow or runtime acts, asks, or stops

Replace the memory/context line with:

> Memory may retain candidate material. A context builder selects a task-scoped packet. The ontology supplies the typed meaning and use contract for interpreting that packet. A named authority owner decides permitted reliance. A workflow or runtime separately attempts any authorized action and must produce its own evidence.

Also replace the audition’s “Ontology gives that material structure, context, and limits” with:

> Memory gives the agent material. An ontology supplies the meaning contract for interpreting selected material; a context builder packages the task-scoped subset with its warnings.

Binding: CAV2-D19 operational interpretation and boundary at `DEFINITIONS.md:921-967`; authority lifecycle non-collapse at `:1321-1348` and `:1379-1404`.

### 3. State the glossary, taxonomy, database, and graph boundary positively

The forbidden-collapse list is necessary but insufficient because an ontology can contain or use these structures.

Add:

> An ontology can include a glossary and taxonomy and can be represented in a database or graph. None of those structures alone supplies the governed meaning contract.

Binding: `DEFINITIONS.md:897-919` and `:934-967`.

### 4. Repair the authority ladder

The current ladder jumps from a promotion gate directly to a governed projection, collapsing governed ontology authority with its read model.

Replace it with:

> source selector → Inventory evidence card or EvidenceSet → ontology candidate → owner-gated PromotionRecord → governed ontology node or artifact → projection or generated read model

Add:

> Each arrow is an owned review or handoff, not automatic ingestion. A projection does not stand in for promoted ontology authority.

Binding: `.arcanum/inventory/entries/ontology-population-from-inventory-synthesis.md:31-92` and `:109-138`; `cyberAlchemy-v2/ontology/README.md:6-31`.

### 5. Do not present Augmentor sequences as literal relation directions

`SourceRecord → DisposableSemanticIndex → ContextSnapshot` is an ordered grounding sequence, not the direction of the typed edges. The evolution chain also omits `SourceRecord` and makes review appear to generate a candidate.

Either label the first chain explicitly as “grounding order—not literal edge direction,” or show the actual semantics:

> DisposableSemanticIndex —derived_from→ SourceRecord  
> ContextSnapshot —uses_bounded_projection→ DisposableSemanticIndex  
> SourceRecord —supports context composition→ ContextSnapshot

Replace the evolution diagram with:

> MemoryIntakeRequest —requests_provider_review→ SourceRecord  
> provider disposition + Inventory-validated handoff required  
> SourceRecord —supports_candidate→ OntologyCandidate  
> OntologyCandidate —requests_promotion_gate→ AuthorityDecision

Visually render the final edge as a request into an owner-controlled external gate, not as production of a decision. Keep `authority_effect: none` visible.

Binding: `views/knowledge.json#/sequences/AUG-KNOW-GROUNDING`; `#/sequences/AUG-KNOW-EVOLUTION`; relation IDs `aug.relation.index_derives_from_source`, `aug.relation.context_uses_bounded_index_projection`, `aug.relation.source_supports_context`, `aug.relation.intake_requests_provider_review`, `aug.relation.source_supports_candidate`, and `aug.relation.candidate_requests_named_owner`; `profile.json#/authority_effect` and `#/release_admission`.

After these exact repairs, the package is definitionally sound without changing its intended voice, timing, repository examples, or Augmentor claim ceiling.
