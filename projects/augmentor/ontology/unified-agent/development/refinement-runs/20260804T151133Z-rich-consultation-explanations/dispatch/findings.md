# Findings: Rich Consultation Explanations

## Per-Artifact Findings

| # | File or boundary | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| 1 | `explanations/beginner.json` to compiler | Seven useful fields are authored; only label, summary, process, and boundary cross. | major | Add a closed explanation-support mapping with structured example kind, analogy limitation, scoped posture, glossary refs, and keywords. |
| 2 | projection bundle | Projection and future glossary can drift independently. | major | Bind projection plus glossary with one bundle digest, manifest version, and atomic install. |
| 3 | consumer freshness | Emitted statements are labeled current from projection freshness alone. | major | Distinguish source freshness from modeled/current-state scope and verification. |
| 4 | evidence/prose handoff | API-generated prose would collapse current evidence and answering-agent ownership. | major | Keep final prose outside the API; return only typed explanation support and answer policy. |
| 5 | retrieved rich text | More free text increases instruction-shaped content exposure. | major | Give all rich text a non-instruction role and add adversarial field fixtures plus caller conformance tests. |
| 6 | response truncation | Current truncation drops statements and records, not coherent explanation units. | major | Truncate whole packs; report omitted sections; never orphan a limitation or provenance binding. |
| 7 | schema versions | Repository JSON projection schema says `@0.1.0`; compiler and consumer use `@1.0.0`. | major | Reconcile and pin one producer/consumer schema family before extension. |
| 8 | glossary | No contract exists; a future glossary could become accidental definition authority. | major | Add an evidence-linked, authority-none glossary schema and return only two to five referenced entries. |

## Verdicts

- Beginner corpus: KEEP as source substrate; FIX its structured metadata.
- Compiler and projection contract: FIX.
- Consultation service: KEEP its read-only and answer-policy boundaries; FIX its optional explanation-support handling and semantic truncation.
- Answer policy: KEEP; add composition-profile conformance tests without adding prose generation.
- API page/agent contract: FIX to expose and render explanation support.

## Accepted Change-Request List

1. Reconcile the schema version owner and baseline.
2. Define closed glossary, explanation-pack, and bundle-manifest contracts.
3. Add structured source content and compiler mapping under the private ontology owner.
4. Extend leakage, provenance, drift, and adversarial validators.
5. Add optional `brief`, `guided`, and `deep` support selection without changing evidence truth.
6. Return packs atomically and truncate only whole units.
7. Keep final prose agent-owned and validate response composition.
8. Update the page contract, deterministic scenarios, and measured overhead checks.

Parent final-approver verdict: accepted as the input to the repaired Refine design. `FIX` describes the planned product changes; it does not mean the review dispatch failed.
