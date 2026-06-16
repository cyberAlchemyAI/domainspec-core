---
tags: [schema, domainspec-language, validator, arcanum, subagents-review]
node_type: discovery
is_session: true
layer: architecture, ontology
nature: explanatory, reference
status: active
created: 2026-06-15
timestamp: 2026-06-15T20:57:55-03:00
expires: 2026-08-14
conversation_id: 2026-06-15-schema-generalization-domainspec-language
decisions_made: true
contradictions_found: true
specs_updated: [projects/domainspec-language/SCHEMA-INVENTORY.md]
promoted_candidates: []
expected_importance: 7
importance_rationale: "Sets direction for the schema-generalization effort and surfaced prior decided work that redirects it away from a fresh private build."
---

# Schema Generalization — domainspec-language as Home

## Summary

Explored how to generalize "schemas for everything that needs a schema" across domainspec-core, ../domainspec, arcanum, and the Lean repo; identified `domainspec-language` as the existing home and drafted a Phase-1 schema inventory plus a candidate "node envelope" (validator-first target, DomainSpec-only scope). A 3-agent adversarial review (FIX ×3) found factual errors in the inventory, a category-error in the proposed epistemic-tag unification, and — decisively — that the project already holds a decided validator architecture (DEC-CONV-01 compiler-pair) and a prior decision (F0) that the generic stage contract is framework-generic and belongs public in Arcanum, contradicting the private-moat premise. Concluded the next move is reconciliation of the two prior decisions, not building.

## Contradictions

- contradicts `projects/domainspec-language/SCHEMA-INVENTORY.md` private-moat premise — ../domainspec `F0-prove-of-instance.md` already decided the generic contract is framework-generic (shape→Arcanum/public, instance+enforcement→domainspec/private).
- questions `projects/domainspec-language/SCHEMA-INVENTORY.md` — adversarial review found factual errors (research node_type, enforcement column, non-reproducible grep counts) and a flawed envelope/epistemic premise.

## Next Steps

- Write a short reconciliation doc in `projects/domainspec-language/` locking DEC-CONV-01 + F0 and forcing the public-vs-private fork.
- Decide the boundary: accept F0's split (shape public / instance+enforcement private) or override it with a new rationale.
- Fix or retire `SCHEMA-INVENTORY.md` — correct facts and demote the envelope to "shared frontmatter lint", or mark superseded.
- Split the epistemic tag into its three distinct concepts (provenance enum / belief 2×2 / proof obligation) before any validator work.
- Optionally register the review dispatch in `telemetry/agents/subagents-dispatch.yaml` (anti_bias axis: methodology).

## Open Questions

- Public or private: accept F0's shape-public/enforcement-private split, or keep all private with a new justification? → reconciliation doc.
- Canonical epistemic grade: `observed|stated|hypothesized` vs `veracidade/convicção`? → `projects/domainspec-language/`.
- Does the "one envelope" actually collapse, given F0 documented a real divergence (anti-digest vs `frame`)? → `../domainspec/.../F0-prove-of-instance.md`.

## Files touched

- projects/domainspec-language/SCHEMA-INVENTORY.md
- sessions/2026-06-15-2057-schema-generalization-domainspec-language.md
