---
tags: [domainspec-v2, test-derivation-engine, normalized-spec, structural-obligations, residue-receipt, provenance]
node_type: spec
is_session: true
layer: [architecture, application]
nature: technical
status: active
version: 0.1.0
last_updated: 2026-07-13
created: 2026-07-13
timestamp: 2026-07-13T11:26:43-03:00
expires: 2026-09-11
conversation_id: 2026-07-13-normalized-spec-residue-bridge
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 9
importance_rationale: "Establishes a non-vacuous operational bridge from the current normalized DomainSpec format to deterministic structural obligations and explicit translation accounting, while clearly leaving semantic refinement unresolved."
---

# Normalized SPEC residue bridge

## Summary

The session clarified that the newest feature pack is a typed graph rather than a full Spivak category and that the current generator emits verification artifacts rather than application implementations. The audit found that normalized `SPEC.md` was accepted by the validator but ignored by the derivation engine, so a valid current feature produced zero obligations. The user approved a bounded operational bridge for that gap. The parser now reads only explicit concepts, relationships, fields, attributes, and declared omissions, without inventing behavior or path equations. The newest agent-execution-orchestrator feature now deterministically yields 39 structural obligations, while the tested missing-table and undeclared-endpoint cases fail closed. A machine-readable residue receipt distinguishes 39 target declarations, 9 source-backed relationship rows, 3 explicitly omitted source rows, parser rejections, and binding-added commitments. Obligations are test requirements rather than necessarily runnable tests; `derive --out` persists them in `TEST-SPEC.engine.md` and maintains their identities in the feature id-map. Typechecking and all 100 tests outside the containment suite pass; the full suite is 103/104 because an unchanged Windows containment test passes an object to a string matcher. The package and source READMEs now document both input dialects, the source files, the persistence workflow, and the limits of structural accounting.

## Open questions

- What implementation object and validity semantics should support a future semantic notion of specification refinement?
- Should generated commitments be modeled as a separate object or fiber rather than combined with source-side omission residue?
- Should normalized `SPEC.md` replace the legacy aspect documents as the canonical derivation boundary, or remain a fallback dialect?

## Next steps

- Add an integration test for `receipt --out` when a reusable CLI harness is introduced.

## Recommendation

Treat the tested 39-obligation bridge and residue receipt as an executable observability layer, not as a proof that generation preserves meaning. Resolve the implementation-object and validity-semantics question before choosing a semantic refinement definition or expanding the proof program.

## Connections

No ontology edges are declared. This session changed non-vault implementation artifacts, whose edge semantics are not settled by the current convention; those artifacts are recorded below without inventing edge types.

## Files touched

- `projects/domainspec-v2/impl/test-derivation-engine/README.md`
- `projects/domainspec-v2/impl/test-derivation-engine/src/README.md`
- `projects/domainspec-v2/impl/test-derivation-engine/src/cli.ts`
- `projects/domainspec-v2/impl/test-derivation-engine/src/emit/spec.ts`
- `projects/domainspec-v2/impl/test-derivation-engine/src/grammar/index.ts`
- `projects/domainspec-v2/impl/test-derivation-engine/src/grammar/normalized-spec.test.ts`
- `projects/domainspec-v2/impl/test-derivation-engine/src/identity/human-id.ts`
- `projects/domainspec-v2/impl/test-derivation-engine/src/index.ts`
- `projects/domainspec-v2/impl/test-derivation-engine/src/ir/types.ts`
- `projects/domainspec-v2/impl/test-derivation-engine/src/provenance/index.ts`
- `projects/domainspec-v2/impl/test-derivation-engine/src/residue/receipt.ts`
- `projects/domainspec-v2/impl/test-derivation-engine/src/rules/index.ts`
