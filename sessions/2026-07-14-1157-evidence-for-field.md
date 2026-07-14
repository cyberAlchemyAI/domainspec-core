---
tags: [ontology, canonical-kinds, authority-kinds, evidence-contract, definitions-governance]
node_type: discovery
is_session: true
layer: ontology
nature: explanatory
status: active
created: 2026-07-14
timestamp: 2026-07-14T11:57:00-03:00
expires: 2026-09-12
conversation_id: 54aff843-d26a-4a20-8c8d-bbf02187c2e4
decisions_made: true
contradictions_found: true
specs_updated: [cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md]
promoted_candidates: []
expected_importance: 7
importance_rationale: "Retired a contested layer enumeration from the canonical Evidence-kind contract and replaced it with evidence_for on the closed authority-kind enumeration, changing how Evidence nodes attach across the authority spine."
---

# evidence_for replaces authority_layer in the Evidence instance contract

## Summary

The session set out to clarify the canonical-kinds instance contract for the four Evidence kinds — how discovery, research, findings, and session are defined, their frontmatter, and their edges. Comparing the contract against the retired ZefraHub frontmatter cheatsheet established which old fields die (node_type, is_session, status, veracidade/convicção, nature, version) and what replaces them. `last_updated` was reinstated into the core contract, initialized equal to `created` and flagged as a coarse signal only, since git remains the event log. Interrogating authority_kind against authority_layer exposed a three-way enumeration disagreement — CAV2-D3 lists 5 layers, CAV2-C2 lists 10 and self-contradicts on observability, and the contract used 7 — and showed the field was formalized only in the candidate instance contract, with no definition card. The owner first conformed the enum to D3's five, accepting that evidence targeting the ontology or implementation surfaces would have no legal value. Testing that against a real case — a discovery improving the research skill — exposed the gap immediately. The owner then replaced `authority_layer` with `evidence_for`, valued with the six authority-bearing Tier-2 authority kinds (Definition, Constitution, Discipline, Decision, Spec, Runtime contract), a closed enumeration under CAV2-D49, retiring the contract's dependency on the contested layer vocabulary. The field is deliberately not named authority_kind — that name would reopen the rule-4 self-promotion hole — and excludes Evidence, Projection, and Residue as values. Producer mirrors were updated and historical records left untouched. The D3-vs-C2 layer disagreement remains open, routed to definitions-governance, and the new field does not yet have a definition card of its own.

## Contradictions

> All three targets below live under `cyberAlchemy-v2/**` and carry **no `node_type`** — the CAV2
> authority spine uses its own `Status:`/`Owner:` scheme, not the vault's. Appendix C's target
> classes are defined over vault node types, and `ontology-conventions.md` explicitly defers
> non-vault paths (its own OQ-C). These verbs are therefore used **descriptively**, pending that
> resolution; they are not claims of catalog conformance. This gap predates the session.

- surfaces-conflict cyberAlchemy-v2/authority/definitions/DEFINITIONS.md — CAV2-D3's five-layer enumeration excludes the ontology and implementation surfaces, leaving evidence aimed at them no legal value to declare, and disagrees with CAV2-C2's ten-layer enumeration.
- surfaces-conflict cyberAlchemy-v2/authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md — CAV2-C2 lists observability as an authority layer while its own non-example forbids observability signals from becoming authority, and disagrees with CAV2-D3's five-layer enumeration.
- opens-question cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md — is a skill's rule-set a Runtime contract before promotion, or only after task-session owner gates pass? evidence_for: [Runtime contract] was valued for a skill-improvement case without examining the promotion boundary.

## Next steps

- Propagate `evidence_for` to every producer that emits Evidence frontmatter: the research and review type skills' output templates and the close-session node template, so no new artifact is born carrying `authority_layer`.

## Recommendation

Run the definitions-governance pass next: settle the CAV2-D3 vs CAV2-C2 layer enumeration (the two surfaces-conflict edges above) and give the `evidence_for` field the definition card the Summary notes it lacks. License: the owner decision recorded here — evidence_for adopted on the closed CAV2-D49 kind enumeration — leaves the layer disagreement as the only live defect between two active authority artifacts; direction, not outcome.

## Files touched

- cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md
- .claude/skills/custom/domainspec-discovery-writing.md
