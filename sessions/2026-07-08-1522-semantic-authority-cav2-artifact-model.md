---
tags: [definitions, cyberalchemy-v2, canonical-artifact, authority-kind, authority-state, semantic-authority, domainspec-v2, axiom]
node_type: conceptual
is_session: true
layer: ontology
nature: explanatory, technical
status: active
created: 2026-07-08
timestamp: 2026-07-08T15:22:00-03:00
expires: 2026-09-06
conversation_id: 2026-07-08-semantic-authority-cav2-artifact-model
decisions_made: true
contradictions_found: false
specs_updated: [cyberAlchemy-v2/authority/definitions/DEFINITIONS.md, cyberAlchemy-v2/authority/definitions/DEFINITION-SCHEMAS.md, cyberAlchemy-v2/ontology/CANONICAL-KINDS.md, cyberAlchemy-v2/authority/definitions/DEFINITION-DRIFT-AUDIT.md]
promoted_candidates: []
expected_importance: 6
importance_rationale: "Renamed the CAV2-D51 canonical-artifact schema fields for explicitness and extended the authority_state lifecycle with `demoted`, and settled the build-from-owned design (an instance-level derived property) for the still-unauthored repo-wide `semantic authority` term."
---

# Semantic authority, the canonical-artifact field rename, and the authority_state lifecycle

## Summary

This session opened as `/craft state @domainspec-v2` and surfaced that DomainSpec-v2's founding axioms are "homeless," leaning on ~12 undefined terms; we took the most load-bearing, "semantic authority" (Axiom A1), which pulled the work up into the CAV2 authority spine. Investigation established that semantic authority is *authority whose governed object is meaning* — a property of an artifact **instance** (gated by its kind, realized by `authority_state`), not of a type — and a repo-wide genus belonging in CAV2, build-from-owned on `CAV2-D34` and the new `CAV2-D51` canonical-artifact model. A two-agent review rejected an initial fat definition card (it duplicated Axiom A1 and re-encoded `CAV2-D3`), converging instead on a thin one-line predicate that rides the existing model. Along the way we proposed a `governs: meaning | execution | record` axis over the nine `CAV2-D49` authority-kinds (meaning = Definition/Spec; execution = Constitution/Decision/Discipline/Runtime-contract; record = Evidence/Projection/Residue), which mirrors the three-pillar model. Two concrete edits landed in the spine, both reviewed: first, the `CAV2-D51` record fields were renamed for explicitness — `fine_type → canonical_kind`, `coarse_group → authority_kind`, so each field names its own enumeration — with the prose reworded to "each canonical artifact declares…" and two opposed reviewers returning KEEP. Second, the `authority_state` enum was extended from `none | candidate | promoted` to add `demoted`, build-from-owned on `CAV2-D48`'s stop/demotion rule, recording the `promoted ≈ active` / `demoted ≈ deprecated` correspondence; a single assessor confirmed it OK. We confirmed the canonical≠authoritative decoupling with two worked examples: a draft axiom is canonical but `authority_state: candidate` (authoritative only once promoted), whereas research and discovery are `Evidence` (`authority_reachable = no`) and can never become authority. `CANONICAL-KINDS.md` Rule 3 was clarified to match (a candidate definition is still a definition, just not yet authority). All edits were synced to the schema registry and the drift audit; the semantic-authority card itself was **not** authored, pending the `governs` classification call, and nothing was committed.

## Open questions

- Which `CAV2-D49` authority-kinds are `governs: meaning` vs `governs: execution`? Definition and Spec are clearly meaning and Evidence is record, but Constitution (governs rules) and Decision (governs a choice) are the genuine boundary — the line drawn there *is* the scope of "semantic authority."

## Next steps

- Author the thin `semantic authority` card in CAV2 via `definitions-governance` once the `governs` line is drawn (a later `CAV2-D5x` id — `D53` axiom / `D54` invariant are now taken), then point DomainSpec-v2 Axiom A1 at it to close `GAP-SH-PROSE-HOMES` for that term.
- Optionally tighten the `CAV2-D51` prose where an artifact is said to "declare" its `authority_kind` — it is derived (`= rollup(canonical_kind)`), so an artifact declares its `canonical_kind` and *inherits* the `authority_kind`.
- Commit this session's changes (submodule-first if `cyberAlchemy-v2` is a submodule; `make bump-check` before pushing) — nothing was committed.

## Recommendation

The keystone is drawing the `governs` line, because it is the sole blocker on authoring the semantic-authority card — the term that started the session (DomainSpec-v2 Axiom A1). Licensing fact: the two spine edits this session are done and independently assessed OK, and the placement review established that semantic authority is a thin derived property over `CAV2-D51`, so only the meaning/execution boundary for Constitution and Decision remains undecided. Recommend the next session settle that boundary via `decision-gate` and then author the one-line card; that Constitution/Decision is the only real ambiguity is grounded in this session's usage analysis, not a landed test.

## Files touched

- cyberAlchemy-v2/authority/definitions/DEFINITIONS.md
- cyberAlchemy-v2/authority/definitions/DEFINITION-SCHEMAS.md
- cyberAlchemy-v2/ontology/CANONICAL-KINDS.md
- cyberAlchemy-v2/authority/definitions/DEFINITION-DRIFT-AUDIT.md
