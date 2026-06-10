---
tags: [goldenquill, tilth, ontology, ontology-view, multi-agent, cic, clc, veracidade, conviccao, skill]
node_type: discovery
is_session: true
layer: domain, ontology
nature: technical, procedural
status: active
created: 2026-06-10
timestamp: 2026-06-10T13:55:47-03:00
expires: 2026-08-09
conversation_id: 2026-06-10-goldenquill-ontology-view-and-skill
decisions_made: true
contradictions_found: true
specs_updated: [projects/goldenquill/victor/ontology-view.md, projects/goldenquill/victor/discovery.md, projects/goldenquill/victor/system-view.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "Produced the GoldenQuill/Tilth ontology-view (typed nodes+edges with the CIC<->CLC forbidden-edge invariant) and a reusable ontology-view skill hardened by 88 agents, while surfacing a self-inconsistency in the vault constitution's edge count."
---

# GoldenQuill ontology-view + reusable ontology-view skill

## Summary

Formalized the GoldenQuill/Tilth knowledge graph as a typed-node + typed-edge `ontology-view.md`
— a 4th sibling to discovery/system-view/engineer-view — via a multi-agent orchestration
(6 explorers over domainspec/domainspec-theorem/Arcanum → summarizer → 3 anti-bias reviewer
layers with zig-zag → author → write-review), modeling the CIC↔CLC no-design-time-coupling
invariant as a forbidden edge + guard. Then generalized that work into a reusable `ontology-view`
SKILL.md package committed to the domainspec repo, hardened by 88 agents (3 review layers ×3 iters
+ a final 3-reviewer robot-talks). Verdict: GO under project-local-overlay governance (not promoted
to house doctrine until a first non-GoldenQuill run); applied the one required fix — dropped the
route-only `agent: domainspec-orchestrator` frontmatter binding.

## Contradictions

- questions `implementation/domainspec/vault/ontology-conventions.md` — its edge count is self-inconsistent (live tables 25 / Appendix-C header 22 / prose 21); canonical count indeterminate until reconciled.
- questions `projects/goldenquill/victor/ontology-view.md` — the skill brands its sole instance a partial counter-example to two of its own headline rules (version-resolution + live-count are transfer-asserted, not yet witnessed).

## Files touched

- projects/goldenquill/victor/ontology-view.md
- projects/goldenquill/victor/discovery.md
- projects/goldenquill/victor/system-view.md
- sessions/2026-06-09-1647-goldenquill-victor-two-view.md
- domainspec/.claude/skills/ontology-view/SKILL.md
- domainspec/.claude/skills/ontology-view/README.md
- domainspec/.claude/skills/ontology-view/templates/ontology-view-template.md
