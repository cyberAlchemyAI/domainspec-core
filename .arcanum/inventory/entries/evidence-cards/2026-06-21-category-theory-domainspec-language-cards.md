---
tags: [inventory, formalization, category-theory, yoneda, residue, domainspec-language, latent-space, cyberalchemy-v2, evidence-card, open-question]
node_type: evidence-card
is_session: false
layer: architecture
nature: reference
status: candidate
created: 2026-06-21
dispatch_id: 2026-06-21-category-theory-domainspec-language-synthesis
dispatch_type: research
working_folder: .arcanum/inventory/entries/
sources: [domainspec-formalization/GLOSSARY.md, domainspec-formalization/docs/paper.md, domainspec-formalization/docs/domainspec-two-layer-framework.md, domainspec-formalization/lean-formalization/M2Counter.lean, projects/framework-unification/README.md, projects/framework-unification/layers/domainspec-language/]
---

# Evidence Cards - Category Theory for DomainSpec Language

Each card is a candidate Inventory read model derived from a session synthesis
(2026-06-21, conversational, not a registered dispatch). Cards do not promote
definitions, ontology, specification, or implementation authority. The
mathematical claims are source-backed to `domainspec-formalization/`; the
mapping claims onto cyberAlchemy and the DomainSpec language, and the
Vect-enrichment, are marked as inference/synthesis and carry residue. Promotion
requires the named downstream owner.

## `objects-as-categories-l1`

- ID: `objects-as-categories-l1`
- Status: candidate
- Claim or candidate: In the DomainSpec formalization a domain "class" is not a
  bag of fields but an object of a category L1 whose identity is its arrows:
  objects = domain concepts, morphisms = "functional aspects". Each object
  carries a meta-type (entity / operation / constraint / relationship) and an
  edge law E decides which meta-type pairs may have a morphism. This is the
  categorical core the DomainSpec language must encode (artifact-kind = object,
  reference/dependency = morphism, contract = structural commitment of Delta).
- Source refs:
  `domainspec-formalization/GLOSSARY.md:22`,
  `domainspec-formalization/GLOSSARY.md:94`,
  `domainspec-formalization/GLOSSARY.md:96`,
  `domainspec-formalization/GLOSSARY.md:60`
- Authority level: source-backed (math) for the L1 structure; the "language must
  encode this" framing is synthesis
- Promotion owner: DomainSpec language design owner via invoke/refine/task-session
- Trace: `2026-06-21-category-theory-domainspec-language-synthesis`
- Residue: The mapping artifact-kind to object / reference to morphism is a design
  proposal, not yet a chosen language model.

## `yoneda-concept-is-its-arrows`

- ID: `yoneda-concept-is-its-arrows`
- Status: candidate
- Claim or candidate: By the Yoneda lemma an object c of L1 is fully determined
  by y(c) = Hom(c, -), i.e. by all its arrows into everything else. The
  formalization uses this directly: M2 is a representability conjecture, and "b
  maps to G(b) extends uniquely to a functor by the Yoneda lemma". As a language
  design rule: define a concept by its bundle of morphisms, not by a field list;
  representable = losslessly recoverable.
- Source refs:
  `domainspec-formalization/GLOSSARY.md:42`,
  `domainspec-formalization/docs/paper.md:121`,
  `domainspec-formalization/docs/paper.md:255`,
  `domainspec-formalization/docs/domainspec-two-layer-framework.md:190`
- Authority level: source-backed (math); the "design rule" is synthesis
- Promotion owner: DomainSpec language design owner
- Trace: `2026-06-21-category-theory-domainspec-language-synthesis`
- Residue: Whether "concept = its morphisms" becomes a hard language invariant or
  a guideline is undecided.

## `yoneda-incompleteness-hallucination`

- ID: `yoneda-incompleteness-hallucination`
- Status: candidate
- Claim or candidate: The Yoneda embedding y : L1 -> Set^(L1) is fully faithful
  but not essentially surjective: not every presheaf is representable. This is
  made concrete by M2 refuted (`M2_unrestricted_false`) - there exists a presheaf
  Hom_L2(Delta(-), b) that no object of L1 represents - and the open content is
  the lift from representables to arbitrary I (M6'). Interpretation: this
  "Yoneda gap" (non-representable presheaves) is the formal locus of well-typed
  structure that no domain concept justifies, i.e. the hallucination detector.
  The glossary already uses the word "hallucinated" for instance residue.
- Source refs:
  `domainspec-formalization/lean-formalization/M2Counter.lean:54`,
  `domainspec-formalization/docs/paper.md:261`,
  `domainspec-formalization/docs/paper.md:273`,
  `domainspec-formalization/GLOSSARY.md:70`
- Authority level: source-backed for the math (M2 refuted, non-representability);
  the "= hallucination detector" reading is inference/synthesis
- Promotion owner: domainspec-formalization authors (math) + DomainSpec language
  design owner (the checkable-representability feature)
- Trace: `2026-06-21-category-theory-domainspec-language-synthesis`
- Residue: The leap from "non-representable presheaf" to "LLM hallucination" is
  interpretive; no formal model ties LLM outputs to presheaf representability yet.

## `schema-instance-orthogonality-two-budgets`

- ID: `schema-instance-orthogonality-two-budgets`
- Status: candidate
- Claim or candidate: DomainSpec has two orthogonal residue axes - a schema axis
  (SchemaCoreflective) and an instance axis (LanFaithful subset
  InstanceCoreflective) - "two layers, two conservation laws, two budgets - never
  one"; refuted M6 proves they do not reduce to one. Synthesis: this orthogonal
  pair IS the contract / schema / iteration split the DomainSpec language handoff
  demands - contract-vs-schema is the schema axis (concept erasure), populated
  data/iteration is the instance axis - so the language needs two separate
  validation tracks.
- Source refs:
  `domainspec-formalization/docs/paper.md:271`,
  `domainspec-formalization/docs/paper.md:133`,
  `domainspec-formalization/docs/domainspec-two-layer-framework.md:131`,
  `projects/framework-unification/layers/domainspec-language/DOMAINSPEC-LANGUAGE-HANDOFF.md:33-62`
- Authority level: source-backed (math, two independent axes); the identification
  with the language's three-layer split is synthesis
- Promotion owner: DomainSpec language design owner
- Trace: `2026-06-21-category-theory-domainspec-language-synthesis`
- Residue: The iteration layer maps to "instance axis over time" only loosely;
  the temporal dimension (M4) is a third axis not folded into this mapping.

## `presheaf-in-vect-latent-extension`

- ID: `presheaf-in-vect-latent-extension`
- Status: open-question
- Claim or candidate: The Lean formalization is entirely Set-valued (a copresheaf
  in Set^L1 is "populated domain data"). A proposed extension replaces the
  codomain Set with Vect (or a Metric-enriched category) so each concept maps to
  a region/vector in R^d - the LLM latent space. This gives a second sense of
  "orthogonal": perpendicular embedding subspaces = semantically independent
  concepts. Unifying the two senses of orthogonal (categorical axis-independence
  vs geometric perpendicularity) is open research, not a result.
- Source refs:
  `domainspec-formalization/GLOSSARY.md:34`,
  `domainspec-formalization/GLOSSARY.md:64`,
  `domainspec-formalization/docs/paper.md:18`
- Authority level: inference/extension - explicitly NOT in the proof
- Promotion owner: domainspec-formalization authors (would need a Vect-enriched
  formalization) before any claim is made
- Trace: `2026-06-21-category-theory-domainspec-language-synthesis`
- Residue: No Vect-valued formalization exists; the geometric/categorical
  orthogonality unification is unproven and may not hold.

## `cyberalchemy-pipeline-as-functor-chain`

- ID: `cyberalchemy-pipeline-as-functor-chain`
- Status: candidate
- Claim or candidate: cyberAlchemy ("the machine that turns user intent into
  finished code") is a staged translation intent -> L1 (domain) -> L2 (schema) ->
  ... -> code, where each step is a functor Delta_i. The DomainSpec residue audit
  then applies per step (what each translation loses), and the DomainSpec language
  is the notation that lets each layer L_i be written as a category so the audit
  becomes machine-checkable rather than prose.
- Source refs:
  `projects/framework-unification/README.md:3-10`,
  `projects/framework-unification/layers/domainspec-language/README.md:1-16`,
  `projects/framework-unification/layers/domainspec-language/DOMAINSPEC-LANGUAGE-HANDOFF.md:16-32`,
  `domainspec-formalization/docs/paper.md:18`
- Authority level: synthesis (the functor-chain reading of cyberAlchemy)
- Promotion owner: framework-unification owner + DomainSpec language design owner
- Trace: `2026-06-21-category-theory-domainspec-language-synthesis`
- Residue: cyberAlchemy stages are not yet declared as categories anywhere; the
  chain is a proposed reading, and the intermediate L_i are not enumerated.
