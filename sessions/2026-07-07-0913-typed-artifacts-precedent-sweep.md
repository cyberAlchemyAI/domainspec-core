---
tags: [domainspec-v2, typed-artifacts, precedent-sweep, assurance-case, sacm-gsn, claim-proof-interlock, subagents-dispatch, robot-talks, overclaim-check]
node_type: audit
is_session: true
layer: architecture
nature: explanatory, reference
status: active
created: 2026-07-07
timestamp: 2026-07-07T09:13:55-03:00
expires: 2026-09-05
conversation_id: 2026-07-07-typed-artifacts-precedent-sweep
decisions_made: true
contradictions_found: true
specs_updated: [projects/domainspec-v2/research/typed-artifacts-precedent/findings.md, projects/domainspec-v2/research/typed-artifacts-precedent/research.md, telemetry/agents/subagents-dispatch.yaml]
promoted_candidates: []
expected_importance: 7
importance_rationale: "Corrects DomainSpec-v2's central novelty claim with cited external evidence and narrows what the project may honestly ship, but is scoped to projects/domainspec-v2/research/ rather than a vault-wide constitution change."
---

# Typed-artifacts precedent sweep — who already owns DomainSpec-v2's typed-artifact bet

## Summary

The session moved from orientation to execution. The user first asked (in Portuguese) what DomainSpec-v2 is — objective, method, components — which I answered from the existing v2 documentation, with the caveat that v2 is mid-migration and that "v2" is ambiguous between the `projects/domainspec-v2/` tower and the `cyberAlchemy-v2/` authority spine. The user then asked what the literature says about "typing code"; I mapped five lineages (type theory/Curry-Howard, MDE+ontologies, formal spec, data provenance, LLM-era intent→code) and flagged the answer was training-memory, not verified citations. Asked to run a real research dispatch in `/domainspec-v2/research` via subagents (route 4), I loaded `domainspec-subagents-strategy`, pushed back that the research question had to be pinned, and reframed the goal per the `research` skill from "is this novel?" to "who already owns each component of v2's typed-artifact bet?" (owned = a win, not a kill). I proposed a `research` dispatch — 4 tensioned explorers (type theory / MDE-ontologies / provenance / LLM-era) → synthesizer → 3 skeptics (precedent/non-vacuity/definitional) — and the user amended it to `robot_talks: true` + zig-zag `loop_cap: 3`, which I accepted with rationale. On go-ahead I ran the check-tension gate (two independent agents, both PASS), registered the dispatch, and fired the four web-enabled explorers; they returned cited sweeps, the synthesizer built an all-GO verdict matrix, and two waves of robot_talks skeptic confrontation stress-tested it. The decisive result: the precedent skeptic found the lineage all four explorers had missed — the SACM/GSN/Isabelle-SACM assurance-case stack, which already owns typed claim-graphs, first-class residue nodes, and claim≤proof edges — which corrected `implements` and residue-as-typed-node from novel to build-from-owned and halved the claim≤proof claim. The honest verdict: v2's only live, witnessed novelty is component (e), a machine-enforced per-stage claim≤proof interlock orthogonal to type-checking (witnessed firing once, not proven-systemic); the "conservation loop" that would make the whole substrate novel is genuine in shape but currently unwired; and "all forbidden edges unconstructible" was killed as an overshoot (only structural prohibition holds). I authored the verbatim-returns and cited-findings artifacts, approved them as parent with the P9 citation check, and closed the dispatch (resolved, 8 agents, 2 loops) in the telemetry ledger.

## Contradictions

- questions `projects/domainspec-v2/definitions/relationships/relationships.yml` — the file tags both structural and relational/cross-feature forbidden edges (e.g. `reject_enforces_cross_label`, `require_cross_feature_saga_scope`) with the same `violation_class: "unconstructible-edge"`, but the sweep shows relational prohibitions are only validate-after-the-fact via a SHACL gate that v2's own R3 review confirms is not live — so the uniform "unconstructible" label overshoots (structural prohibition holds; relational does not).

## Open questions

- Is v2's genuine contribution worth staking on wiring the conservation loop (gate-failure ⇒ residue obligation ⇒ re-consumed at a later re-gate), which would make the whole a–f substrate novel, or should the composition-novelty be retired down to just the (e) interlock? Undecided which is worth the effort.

## Next steps

- Run the adopt-with-attribution citation sweep across v2 docs: every place touching claim-graphs, residue nodes, or provenance edges must cite SACM/GSN, PROV-O, and MOF/Ecore as prior art rather than present them as original (findings.md open item #5).
- Decide the relational-enforcement mechanism — dependent-type encoding (constructive, per E1) vs. fixing the not-yet-live SHACL gate — via a decision-gate (findings.md open item #2).
- Prove (e) systemic by exercising the machine-enforced claim≤proof interlock beyond the single witnessed counterexample, lifting "witnessed once" to recurrent (findings.md open item #4).
- Pin `cites` semantics — PROV `wasQuotedFrom` (derivational) vs CiTO (bibliographic) — in `relationships.yml` (findings.md open item #3).

## Recommendation

The keystone is the **adopt-with-attribution citation sweep**: it is the cheapest move that discharges the biggest risk this session surfaced — an originality claim that would collapse on external review. It is licensed by a landed fact this session produced, not a hunch: the SACM/GSN precedent discovery, adversarially verified across two robot_talks skeptic waves. The conservation-loop decision (Open question) should sit behind a decision-gate rather than be attacked first, because whether it is worth wiring depends on how much of v2's story must be original at all — which the citation sweep clarifies.

## Files touched

- projects/domainspec-v2/research/typed-artifacts-precedent/research.md
- projects/domainspec-v2/research/typed-artifacts-precedent/findings.md
- telemetry/agents/subagents-dispatch.yaml
