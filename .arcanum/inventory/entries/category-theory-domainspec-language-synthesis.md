---
tags: [inventory, formalization, category-theory, yoneda, residue, domainspec-language, latent-space, cyberalchemy-v2, findings, open-question]
node_type: synthesis
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

# Category Theory for the DomainSpec Language

- ID: `category-theory-domainspec-language-synthesis`
- Type: synthesis
- Status: candidate
- Tags: category-theory, yoneda, residue, domainspec-language, latent-space, cyberalchemy-v2
- Confidence: medium (math source-backed; mappings and Vect-extension are synthesis/inference)

## Summary

A session synthesis (2026-06-21) connecting the `domainspec-formalization`
category-theory results to two design targets: the **cyberAlchemy framework**
(intent-to-code machine) and the **DomainSpec language** (contract / schema /
iteration). The math is source-backed; the application is a proposal. Selector
cards:
[evidence-cards/2026-06-21-category-theory-domainspec-language-cards.md](evidence-cards/2026-06-21-category-theory-domainspec-language-cards.md).

## The four lenses

1. **Objects/classes as categories** — L1 objects are domain concepts, morphisms
   are functional aspects, each object has a meta-type, an edge law E governs
   admissible morphisms. The language should encode: artifact-kind = object,
   reference = morphism, contract = the structural commitment of the functor
   Delta. Card: `objects-as-categories-l1`.

2. **Yoneda — a concept is its arrows** — y(c) = Hom(c, -) determines c; M2's
   "b maps to G(b) extends by Yoneda" is the formalization using exactly this.
   Design rule: define concepts relationally, not by field lists; representable =
   losslessly recoverable. Card: `yoneda-concept-is-its-arrows`.

3. **Yoneda-incompleteness = hallucination detector** — the Yoneda embedding is
   fully faithful but not surjective; M2 refuted exhibits a non-representable
   presheaf; the lift to arbitrary I is open (M6'). The "Yoneda gap" is the
   formal locus of well-typed structure no concept justifies. The glossary
   already says instance residue is data "lost (or hallucinated)". Card:
   `yoneda-incompleteness-hallucination`.

4. **Orthogonality = two validation tracks** — schema axis ⊥ instance axis,
   "two budgets, never one" (refuted M6 proves independence). This pair IS the
   contract/schema/iteration split the language handoff demands. Card:
   `schema-instance-orthogonality-two-budgets`.

## The bridge to cyberAlchemy

cyberAlchemy is read as a chain of functors `intent -> L1 -> L2 -> ... -> code`;
the residue audit applies per step; the DomainSpec language is the notation that
writes each layer as a category so the audit is machine-checkable. Card:
`cyberalchemy-pipeline-as-functor-chain`.

## The extension not yet proved

Replacing the presheaf codomain **Set** with **Vect** (latent space) is the LLM
bridge: each concept maps to a region in R^d, and "orthogonal" gains a second,
geometric meaning. This is **not in the Lean** (which is Set-valued) and the
unification of categorical vs geometric orthogonality is open research. Card:
`presheaf-in-vect-latent-extension` (status: open-question).

## Open design question (carried, undecided)

Should the language treat **representability** (the "real concept vs
hallucination" test) as a **first-class check in the schema layer**, or as an
**annotation in the iteration layer** raised when an artifact is populated and
read back? Routes to `decision-gate` for the DomainSpec language design owner.

## Task fit

- DomainSpec language design (`projects/framework-unification/layers/domainspec-language/`):
  grounds the contract/schema/iteration model in the two orthogonal residue axes
  and supplies a representability-based hallucination check as a candidate feature.
- cyberAlchemy v2 authority/architecture work: supplies the functor-chain reading
  and the per-step residue audit framing.

## Residue

- The "non-representable presheaf = LLM hallucination" reading is interpretive;
  no formal model ties LLM outputs to presheaf representability.
- The iteration layer to instance-axis mapping omits the temporal axis (M4).
- No Vect-valued formalization exists; geometric/categorical orthogonality
  unification is unproven.
- This is a conversational synthesis, not a registered subagents-strategy
  dispatch; the `dispatch_id` is a trace handle only.
