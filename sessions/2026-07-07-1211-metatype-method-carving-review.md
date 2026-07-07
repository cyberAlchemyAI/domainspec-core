---
tags: [meta-types, domainspec-v2, method-carving, adversarial-review, node-collapse-discipline, saga-decomposition, robot-talks, definition-methodology, anti-bias-triangle, discovery-amendment]
node_type: audit
is_session: true
layer: architecture
nature: technical, reference
status: active
created: 2026-07-07
timestamp: 2026-07-07T12:11:44-03:00
expires: 2026-09-05
conversation_id: 2026-07-07-metatype-method-carving-soundness
decisions_made: false
contradictions_found: true
specs_updated: [projects/domainspec-v2/discovery/domainspec-v2-discovery.md, projects/domainspec-v2/development/meta-type-formalization/research/2026-07-07-method-carving-soundness-review/findings.md, projects/domainspec-v2/development/meta-type-formalization/research/2026-07-07-method-carving-soundness-review/research.md, telemetry/agents/subagents-dispatch.yaml]
promoted_candidates: []
expected_importance: 7
importance_rationale: "Surfaces a root-cause gate gap (node-level non-collapse) and a proven Saga over-cut that materially revise the live domainspec-v2 discovery's open questions, but scope was method-only so it does not itself resolve the carving."
---

# Adversarial soundness review of the meta-type + edge definition method

## Summary

This session ran an adversarial red-team review (dispatch_type: review, routed through `domainspec-subagents-strategy`) of DomainSpec v2's METHOD for defining its 25 meta-types and ~31 typed edges — the user narrowed scope twice, landing on "is the definition methodology sound and does the carving make sense," explicitly excluding the implementation. The attack was designed as a 3-attacker anti-bias triangle (Lawvere = completeness/inflate, Quine = parsimony/collapse, Wittgenstein = foundation/anti-collapse) plus a synthesizer and two verifiers; two helper agents critiqued the proposal first and re-vectored the initially-fake Quine↔Wittgenstein tension into a real one, after which the check-tension gate passed both agents on all four tests. The dispatch ran solo → robot-talks → synthesis → zig-zag verification and produced genuine collapse detection (Lawvere abandoned "add nodes" and all three converged on one structural root). The decisive event was verification: it REFUTED the two most dramatic solo-pass findings — the "Rule/Policy/Calculation trio is structurally unkeepable" claim attacks a promise the method's moat explicitly disclaims, and "vacuous discrimination (CRITICAL)" was downgraded to a MAJOR transparency finding — preventing an inflated verdict. What survived is the structural ROOT (D18's non-collapse discipline governs edges but exempts node formation, so no node-level non-collapse gate exists), a proven Saga over-cut (Saga = Workflow + a `scope` tag with byte-identical edge_participation, and compensation is not Saga-exclusive → default-merge), a missing "time" genre (no Schedule/Timer; a clock trigger is unconstructible), a Rule→Query authorization card-vs-law contradiction, and an over-stated "any domain" universality claim. The verdicts were FIX-with-mostly-KEEP: the methodology is sound at the edge layer and at the bar it set, the carving is ~90% right with two opposite-sign errors. The dispatch was registered and closed `resolved` (10 agents) in the telemetry ledger. At the user's request the review was then persisted as findings.md + research.md and five surgical edits were applied to the domainspec-v2 discovery — sharpen OQ-1 with the 11/14-attestation finding, add OQ-6 (the node-non-collapse root), add OQ-7 (the Saga/time carving errors with DEC-DSV2-SAGA-MERGE), reinforce §5, and update Status/Provenance. A single helper subagent reviewed the edited discovery (FIX-BEFORE-FINALIZE) and its one legitimate catch — §5 overstated Saga as a "proven false kind" when it is an open decision — was applied; nothing was committed.

## Contradictions

- validates `projects/domainspec-v2/discovery/domainspec-v2-discovery.md` (OQ-1) — the "semantic mistyping is invisible / shape not meaning" framing is confirmed correct and sits *inside* the conceded moat; the dramatic "method is structurally broken" reading was refuted at verification. The review sharpens it: 11 of 14 backend distinguishers validate at author-attestation strength, not structural.
- questions `projects/domainspec-v2/definitions/DEFINITIONS.md` (D18) — the non-collapse discipline governs edge/relationship promotion but explicitly exempts DS-D1 meta-type formation, and D6/D7 carry only coverage tests, so no node-level non-collapse gate exists. ROOT, CRITICAL, confirmed by the definitional verifier.
- questions `projects/domainspec-v2/definitions/relationships/relationships.yml` + `definitions/meta-types/meta-types.yml` — Workflow and Saga have byte-identical `edge_participation` and compensation is not Saga-exclusive, so Saga is structurally undistinguished from Workflow (open `DEC-DSV2-SAGA-MERGE`, default merge). CRITICAL-as-carving, survived.
- questions `projects/domainspec-v2/impl/spec/TAXONOMY.md` — the "25 building blocks for describing any domain" claim is over-stated; the 25 are visibly of the DDD/web genre, and the "time" genre is unconstructible. MEDIUM, survived.

## Next steps

- Resolve the review's deferred owner questions (can feature-ownership be a computed graph property? is Projection a node or a View-Model widening? is Schedule a node or an Operation attribute? is the D15 Formal-cell moat absolute?), then apply the highest-leverage change — install a **node non-collapse gate** (a clause extending `DEFINITIONS.md` D18 or a new D-section: every node type must exhibit a structural-table witness OR distinct structure-reading edge-participation) — followed by the carving edits in `relationships.yml`/`meta-types.yml` (merge Saga, admit Schedule, add `constrains`/`compensates`/`contains`-source-widen, resolve Rule→Query).
- Route the fine-grained edge decisions (`constrains`, `compensates`, `contains`-widen, the Projection node-vs-View-Model fork) into engineer-view / the `DEFINE.md` open-decisions block — deliberately kept OUT of the discovery.
- Commit this session's changes (submodule-first if `projects/domainspec-v2` is a submodule); nothing was committed.
- Fix the recurring close-session skill/repo mismatch (`.claude/skills/close-session` targets a non-existent `docs/vault/`; the umbrella uses `sessions/`) — now carried unfixed from 2026-07-03-2010, -2014, 2026-07-06-2104, and 2026-07-07-0025.

## Recommendation

- The keystone is installing the node non-collapse gate (discovery OQ-6) — the single highest-leverage change, since it simultaneously forces Saga to prove structure or merge, forces a time node to ship real structure, and turns the semantic trio into an explicit declared exception. It is licensed by the definitional verifier CONFIRMING the D18 node-formation exemption as the root and by the dispatch closing `resolved`. Attack it before the individual Saga/Schedule carving edits, because the gate is the rule that makes those edits principled rather than ad-hoc — the carving fixes are its first consumers, not independent decisions.

## Files touched

- projects/domainspec-v2/discovery/domainspec-v2-discovery.md
- projects/domainspec-v2/development/meta-type-formalization/research/2026-07-07-method-carving-soundness-review/findings.md
- projects/domainspec-v2/development/meta-type-formalization/research/2026-07-07-method-carving-soundness-review/research.md
- telemetry/agents/subagents-dispatch.yaml
