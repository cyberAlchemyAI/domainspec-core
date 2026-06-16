---
tags: [domainspec, arcanum, lean, resonantos, fusion, framework-integration, two-axis, ontology-tower, residue, reflection-tower]
node_type: discovery
is_session: true
layer: ontology, architecture, application
nature: explanatory, procedural
status: active
created: 2026-06-15
timestamp: 2026-06-15T21:00:31-03:00
expires: 2026-08-14
conversation_id: 2026-06-15-framework-integration-two-axis-fusion
decisions_made: true
contradictions_found: true
specs_updated: [projects/cyber-alchemy-lean-fusion/framework-integration/DESIGN.md, projects/cyber-alchemy-lean-fusion/framework-integration/README.md]
promoted_candidates: []
expected_importance: 7
importance_rationale: "Establishes the two-axis (foundry × ontology-tower, residue as currency) spine for unifying the four repos, and produces + hardens the framework-integration seed packet that the unification map will extend."
---

# Framework Integration — two-axis fusion (high-level mapping session)

## Summary

High-level "look from above" session to converge four repos — `domainspec` (the framework: taxonomy/vault/pipeline), `domainspec-core` (host + research hub), `domainspec-lean-formalization` (typed-residue theory), and `Arcanum` (CyberAlchemy capability lifecycle) — toward a single conceptual map, around the core question: **how to turn a vague user intent into a useful artifact**, where "artifact" spans knowledge / ontology / formal model / spec, with code as only the tip.

The session landed a **two-axis frame** as the spine, profiled a comparable external system (ResonantOS), clarified the Lean program's structure, found that an **Arcanum × Lean fusion seed already existed** (`cyber-alchemy-lean-fusion/`), and **built + reviewed + corrected** a new `framework-integration/` packet adding the third pillar (the framework as the vertical axis). Dispatched 4 subagent runs (all registered + closed in the private domainspec dispatch ledger).

## Decisions & findings

- **The product concept already has a name** (from the existing seed): a **capability foundry** — every act of creation (intent→artifact) is *residue-accounted*. Killer feature = the **residue ledger** (typed account of what each transformation does not preserve).
- **Two-axis frame (the spine).** HORIZONTAL = foundry lifecycle (intent→artifact; Arcanum lifecycle + Lean epistemic core, already fused in the seed). VERTICAL = ontology tower (business→system→code; the DomainSpec framework). **Residue is the common currency at every boundary of both axes.** permguard sits on a third axis (capability tower).
- **Knowledge is layered (multiple ontologies), not one.** Business ontology (`domain_knowledge/`), system ontology (no dedicated home — only `@sys` tags + taxonomy "Primary Layer"), code ontology (`governance/tags/` `@biz`/`@sys`). The `@biz`/`@sys` code tags are the realized typed-edge between code↔domain floors.
- **Lean clarifications (candor — the repo separates what the user's framing merged):**
  - The ontology layers (meta-layers / "kinds": L0 domain → model → code → rules → foundations) are a **different axis** from the **reflection tower** (`L₁ⁿ⁺¹ = L₁ⁿ ⊕ Carrier(μₙ)`, self-application). The Lean repo keeps them distinct ("different axes"); only the *generating move* (each Δ loses residue) is shared.
  - **Tower direction:** climbing ADDS namability (upper floor names what the lower couldn't). For the ontology strata: business = rich top, code = lean bottom; Δ descends and drops residue.
  - **permguard** (`PermGuard.lean`, sorry-free, active) is an **engineering capability tower on owned/proved foundations — explicitly NOT a residue tower** (security returned a typed-residue null). It is the outermost executable layer with an "UNVERIFIED TRUST BORDER"; fails closed.
- **ResonantOS (external precedent).** Browser-first AI OS; real code (151 test files). Has the intent→spec gate (`GoalWorkspace` refuses vague intent), a `DelegationPacket`→`TASK.md` spec gate, a knowledge-vs-code artifact split, and a `Logician` verifier — but **flat memory, no ontology / typed knowledge graph.** Validates our differentiator: the iceberg below code (ontology / formal model / typed graph) is exactly what ResonantOS lacks.
- **Contradictions surfaced:** (1) framework `README.md` count drift — claims 24 meta-types / 26 edges; real headers show **25 (14+11) / 29 (15+8+6)**. (2) "domainspec" is overloaded — in `MAP.md`/views it means theorem+core; the new packet's subject is the FRAMEWORK. (3) Build over-attributed a thesis to `TO-VLAD2` (and cited a nonexistent `TO-VLAD1.md`) — corrected.
- **Packet hardened.** Adversarial review (2 auditors) caught real over-claiming; applied 9 corrections — most load-bearing: the "framework typed edges as a 2nd residue-type filler competing with the Lean type" is now marked the packet's own `[inference]` (the novel View-01 contribution), not a pointer to owned material; killer feature marked not-yet-constructible (needs the homeless system floor).

## Next Steps

- **Attack blocker #2 first (recommended): a `research` dispatch in the Lean repo on the residue-TYPE question (View 01)** — does an artifact-level residue carry a type that *mechanically fires* a gate? Start from the seed `DESIGN.md §7` candidate machinery: information-loss/MI (resource theories), codensity/nucleus, Grothendieck-fibration Σ-fibre, refinement types / proof-carrying code, Galois connections, residuality theory (Hopkins/Cook). The fusion `DESIGN.md §9` already prescribes this exact dispatch.
- **Park blocker #1 as a named open problem:** the system-ontology floor has no home (no `system_design_knowledge/`; only `@sys` + taxonomy "Primary Layer"). New finding this session — not named upstream. Resolve later (dedicated home vs `@sys`-only projection), ideally after #2's verdict.
- **Decide:** assemble the 4-pillar unification map in `domainspec-core` now, or wait for #2's verdict to fix the spine first.
- **Uncommitted:** the `framework-integration/` packet (in `core`) and the dispatch ledger (in `domainspec`) are not committed.
- **Backlog:** fix the framework `README.md` count drift (24/26 → 25/29).

## Open Questions

- **(i) vs (ii) — load-bearing design decision, still OPEN.** Does the product adopt the Lean repo's separation of axes (reflection-tower / capability-tower / ontology-tower as distinct), or deliberately fuse them into one layered architecture? The formal grounding (residue results) attaches differently depending on the answer.
- Is "business = rich top, code = lean bottom" the product's chosen tower orientation, or just the Lean repo's? → confirm.
- Does the framework's typed-edge surface mechanically fire a gate (View 01 fill), or only name relationships? → answered by the #2 research dispatch.

## Files touched

- Created: `projects/cyber-alchemy-lean-fusion/framework-integration/README.md`, `.../DESIGN.md` (the seed packet, built by 2 explorers + 1 writer).
- Edited: `.../framework-integration/DESIGN.md` — 9 corrections from adversarial review (citation fixes, killer-feature constructibility caveat, smallest-unit reposition, DCM pointers, EVIDENCE-column qualification, naming cleanup).
- Modified (in `domainspec`): `telemetry/agents/subagents-dispatch.yaml` — 4 dispatches registered + closed: `resonantos-probe`, `lean-tower-probe`, `framework-integration-build`, `framework-integration-review`.
- Removed: temp clones `~/.tmp-resonantos-a`, `~/.tmp-resonantos-b`.
