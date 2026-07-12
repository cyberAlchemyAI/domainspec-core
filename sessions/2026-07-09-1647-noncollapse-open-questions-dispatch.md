---
tags: [domainspec-v2, meta-type-formalization, node-noncollapse-gate, open-questions-closure, edge-witness, exception-lane, saga-workflow-merge, closure-invariant, feature-scope-collapse, subagents-dispatch]
node_type: audit
is_session: true
layer: architecture
nature: explanatory, technical
status: active
created: 2026-07-09
timestamp: 2026-07-09T16:47:42-03:00
expires: 2026-09-07
conversation_id: 2026-07-09-noncollapse-open-questions-dispatch
decisions_made: false
contradictions_found: true
specs_updated: [projects/domainspec-v2/development/meta-type-formalization/research/2026-07-08-open-questions-noncollapse/findings.md, projects/domainspec-v2/development/meta-type-formalization/research/2026-07-08-open-questions-noncollapse/research.md, telemetry/agents/subagents-dispatch.yaml]
promoted_candidates: []
expected_importance: 8
importance_rationale: "Falsifies the keystone total function and the closure invariant backing the node non-collapse gate design, and traces the sole Saga~Workflow collapse — the single blocker to D6 promotion — to a resolver that discards feature_scope, materially changing the promotion calculus without touching source."
---

# Node non-collapse open questions — answered, two keystones falsified, and the Saga~Workflow collapse traced to the resolver

## Summary

This session took the two open questions left by the 2026-07-08 node non-collapse gate build and ran a governed research dispatch to answer them: routed `domainspec-subagents-strategy` → `research`, passed the check-tension gate (both gate agents PASS), registered as `2026-07-08-open-questions-noncollapse`, and ran 8 agents — two tensioned explorer pairs (Church/Tarski on the exception lane; Spivak/Jacobs on the edge witness), a synthesizer, two confronting skeptics (Gödel/Taleb, `robot_talks`), and an auditor as `final_approver` (exit: `resolved`). The panel refuted two load-bearing claims rather than confirming them. "Certification is moat-forbidden" was **withdrawn**: testing the value↦verb functional dependency treats the declared value as an opaque equality key — `attribute-equals` is a lowercased string compare (`validate-content.ts:203-219`) — so the co-variation is shape-detectable with no Formal-cell read. The keystone total function `{boolean↦enforces, strategy↦applies, value↦calculates}` is **false at n=3**, because Calculation sources both `calculates→Operation` and `queries→Entity`; "permanent" was struck for the registry-relative "stable while D15 and the owner's laundering-judgment hold." On the edge witness, the closure invariant that would rescue authority-resolution was upgraded from "unsound now" to **ill-posed**: it quantifies over "composes into different code," while D3's own clean-widening corollary (`DEFINITIONS.md:115`) admits an endpoint *because* it composes into no different code, contradicting the admissibility law at `:111`. After the auditor's acceptance, the three items the dispatch had honestly declared unverified were closed in a follow-on verification pass. Two confirmed the panel — the magnitudes are exact (91 pairs = 36 exception-lane + 27 W-edge-only + 27 W-struct+W-edge + 1 no-witness) and `attribute-equals` is an opaque compare (the reviewer's locator `relationships.yml:17` was wrong; that line is `signature_count: 31`). The third **inverted** the synthesis: `buildEdgeMaps` keys on the signature id alone and never reads `feature_scope`, while `orchestrates` is two same-id rows (`Workflow`/`same-feature`, `Saga`/`cross-feature`), so both types receive `{orchestrates}`, the sets compare equal, `wEdge` returns false, and — both being attestation-only — they collapse. The sole Saga~Workflow collapse, the single blocker on D6 promotion via `DEC-DSV2-SAGA-MERGE` (default: merge), is therefore **manufactured by the resolver discarding the field that distinguishes the two types**, corroborated by the merge plan's own "Saga → Workflow *plus a `scope` flag*," which reintroduces the distinction it erases. No source tree was mutated: outputs are `research.md` + `findings.md` plus the two ledger appends.

## Contradictions

- contradicts `projects/domainspec-v2/definitions/reviews/2026-07-08-d6-node-noncollapse.md` — the panel withdrew its "certification is moat-forbidden" limit (`attribute-equals` is a confirmed opaque string compare, so co-variation is shape-detectable without a Formal-cell read) and struck its permanence language for "stable while D15 and the owner's laundering-judgment hold," resolving both of the note's open items rather than leaving them open.
- contradicts `projects/domainspec-v2/development/meta-type-formalization/research/2026-07-07-node-noncollapse-gate-redteam/DESIGN-SPEC-v2.md` — §8's laundering argument depends on the keystone total function `{boolean↦enforces, strategy↦applies, value↦calculates}` being total; it is false at n=3, since Calculation sources both `calculates→Operation` and `queries→Entity`.
- contradicts `projects/domainspec-v2/definitions/DEFINITIONS.md` — D3's clean-widening corollary (`:115`) admits an endpoint precisely because it composes into no different code, directly contradicting the admissibility law it derives from (`:111`).
- contradicts `projects/domainspec-v2/impl/tools/validate-meta-types-noncollapse.ts` — `buildEdgeMaps` (lines 109-112) keys edges on signature id alone and never reads `feature_scope`, manufacturing the sole Saga~Workflow collapse that `DEC-DSV2-SAGA-MERGE` was set up to adjudicate.

## Open questions

- Is the map from a declared return sort to its `(verb, target)` pair a *law* forced by something, or an artifact of the current fourteen rows — and is there any principle that would make it a law rather than a coincidence that a fifteenth type could break?
- Can a validator forbidden to read meaning ever certify its own non-laundering, or is certification irreducibly an owner act performed outside the validator?

## Next steps

1. Re-key the edge witness: make `buildEdgeMaps` (`impl/tools/validate-meta-types-noncollapse.ts:109-112`) key on `(edgeId, feature_scope)`, re-run `--report`, and record whether Saga~Workflow separates.
2. Rule `DEC-DSV2-SAGA-MERGE` only *after* (1) — if the collapse was spurious, D6's third challenge fires zero times and the confirm contract's "no open contradiction" clause is met without a merge.
3. Apply the `findings.md` corrections to `definitions/reviews/2026-07-08-d6-node-noncollapse.md`: strike "permanent," withdraw "certification is moat-forbidden," record the modal and empirical defeaters separately, and add the return-sort↦`(verb,target)` bijection as an explicit antecedent (already violated).
4. Add the bijection-monitor gate and the clean-widening non-separation fix to the checker; annotate `wEdge` as clause-2-only and `DEFAULT_EXCEPTION_ALLOWLIST` as a clause-3 proxy.
5. Resolve the D3 clean-widening contradiction (`DEFINITIONS.md:111` vs `:115`) through `decision-gate`.

## Recommendation

The keystone is Next step 1 — re-key the edge witness before anyone touches `DEC-DSV2-SAGA-MERGE`. This is licensed by a landed fact, not a hunch: `buildEdgeMaps:109-112` demonstrably adds `edgeId` alone, `orchestrates` demonstrably carries two same-id rows split only by `source_type` and `feature_scope`, and the checker's own `--report` shows Saga~Workflow as the sole `no witness` pair. The merge default is therefore not licensed by the evidence that was supposed to license it. The next session should re-key, re-run, and only then put the merge to the owner — with the fallback that if `feature_scope` is ruled *not* a distinguishing axis under D3, the merge proceeds on that stated ground rather than on a collapse the resolver invented.

## Files touched

- projects/domainspec-v2/development/meta-type-formalization/research/2026-07-08-open-questions-noncollapse/findings.md
- projects/domainspec-v2/development/meta-type-formalization/research/2026-07-08-open-questions-noncollapse/research.md
- telemetry/agents/subagents-dispatch.yaml
