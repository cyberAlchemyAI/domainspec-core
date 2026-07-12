---
tags: [agents, dispatch, oss-tooling, subagents-strategy, duplicate-dispatch, pre-flight-check, cyberalchemy-v2, domainspec-v2, telemetry, adoption-guide]
node_type: audit
is_session: true
layer: architecture, ontology
nature: explanatory, technical
status: active
created: 2026-07-09
timestamp: 2026-07-09T16:31:12-03:00
expires: 2026-09-07
conversation_id: 2026-07-09-oss-tooling-sweep
decisions_made: true
contradictions_found: true
specs_updated: [cyberAlchemy-v2/research/oss-tooling-candidates/ADOPTION-GUIDE.md, telemetry/agents/subagents-dispatch.yaml]
promoted_candidates: []
expected_importance: 6
importance_rationale: "A governed 21-agent dispatch re-derived an already-committed research package because no pre-flight existing-work check ran, and only an incidental harness write-guard prevented the committed artifacts from being clobbered — the durable value is that near-miss and the new ADOPTION-GUIDE, not the (redundant) research content."
---

# OSS tooling sweep — a governed dispatch that re-derived already-committed work

## Summary

The session set out to survey domainspec-v2 and cyberAlchemy-v2 and propose a governed subagents strategy for researching open-source tools, reporting per tool: what it is, why it would help, where it plugs in, and whether we already do something similar. Two reconnaissance scouts mapped each system's seams, and the strategy was iterated with the owner across three rounds — the execution graph made explicit, `robot_talks` dropped in favour of per-lane synthesizer nodes, `zig-zag` placed on the synth↔reviewer edges, and a third lane added for agent running and orchestration. The `check-tension` gate split on the first pass, its reviewer reproving the final-reviewers pair for being written as parallel coverage rather than mutual exposure; the pair was rewritten and both gate agents passed on re-run, which is the gate doing exactly what it exists to do. The dispatch then ran three lanes of advocate⊥skeptic finders into a lane synthesizer and inflation⊥gap reviewers, followed by a final synthesizer and coherence⊥claim≤proof reviewers, closing `resolved` at 21 agent invocations. Its verdict was that almost nothing should be adopted: a single link checker gated on ratification, a handful of pilots, and two sequenced pilots — because both projects had already swept this space, in a frozen domainspec finding rejecting DSLs and solvers, and a cyberAlchemy finding instructing "cite the precedent, do not adopt." The reviewers earned their place by verifying claims against disk, killing a recommendation whose premise did not exist in the code, correcting a category error that had confused a wire format with a datastore, and striking a false fact about the dispatch ledger's shape. The long-standing D29↔D16 relator divergence was re-confirmed live and unfixed, and reframed as an unreconciled *soft* divergence rather than a hard contradiction, since D29 textually defers to D16. **Then, at session close, a pre-flight check that should have run first revealed the entire research package was already committed on 2026-07-08 as `7f26e738`, byte-identical to what this dispatch re-derived** — the session spent 21 agents rediscovering a committed result, and only a harness guard blocking subagent writes kept the committed artifacts from being overwritten. The net-new artifact is `ADOPTION-GUIDE.md`, a context-first explainer of what could be adopted and why, deliberately placed under the research folder with `status: candidate` rather than at the CAV2 root so that it cannot read as authority.

## Contradictions

- questions `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md` — the D29 (Axis Orthogonality Invariant) vs D16 (Typed Coupling Invariant) relator/field divergence was re-confirmed live and unfixed by two independent agents with line cites: D16 (≈L665-673) mandates a 7-field typed relation, while D29 (≈L1800-1804, L1827-1828) enumerates five relator kinds ("gate / validator / owner decision" among them) and lists only four fields. Reframed this session as an unreconciled *soft* divergence, not a hard contradiction, because D29 textually defers ("must be represented through `CAV2-D16` … before it can govern work"). **Not personally re-verified by the session author** — the claim rests on the two agents' reads.
- questions `cyberAlchemy-v2/authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md` — its OQ-1 (recommending Markdown link checks as the first deterministic validator) is status OPEN, not a ratified gate, and it directly gates the sweep's single "adopt." The tier was therefore renamed ADOPT-ON-RATIFICATION rather than ADOPT-NOW; adopting on an unratified open question would front-run the owner's own decision.
- questions `projects/domainspec-v2/development/meta-type-formalization/research/2026-07-02-formalism-and-primitives/findings.md` — its frozen "SMT — NO" verdict may be scoped too broadly. The advocate pitched two postures; the determinism argument kills the emit-path posture, but a CI-only differential oracle (never inlining a solver value into golden bytes) was collapsed into that rejection and **never independently rebutted**. Marked PLAUSIBLE; revisiting it requires first reopening the frozen finding.
- questions `.claude/skills/domainspec-subagents-strategy/SKILL.md` — its four dispatch triggers (synthesis, context protection, isolation, parallelism, at L25-28) say *when* to dispatch, but nothing in the Propose step obliges the strategist to check whether the answer is already committed in the repository. This session spent 21 agents re-deriving `7f26e738`; the router permitted it because no such precondition exists.
- validates `cyberAlchemy-v2/development/research/2026-06-24-ontology-engineering-precedent/findings.md` — this session's adversarial sweep across ~35 candidates converged on the same "cite the precedent, do not adopt" posture for the ontology, graph, and policy-as-code stack, reaching it from a different corpus and a different agent structure.

## Open questions

- Does `loops_used` uniformly 1 license the conclusion that crash-recovery is unneeded, or is it selection bias? No large multi-loop dispatch exists partly *because* interruption-survival does not — absence in the record may be an artifact of the missing capability rather than evidence of no need.
- Is "cheap-and-certain vs cheap-and-pointless" a sound general discriminator for piloting a zero-dependency native script that has no demonstrated pain? The index generator was piloted and the telemetry read-model deferred on the *same* "no proven pain" caveat, and the asymmetry currently rests on a judgment rather than a stated rule.

## Next steps

- Add a pre-flight existing-work check to the Propose step of `.claude/skills/domainspec-subagents-strategy/SKILL.md`, ahead of the `check-tension` gate: search the target `research/` and `development/` trees before shaping a fan-out.
- Read the D16 and D29 lines in `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md` directly and either confirm or retract §7.2 of `ADOPTION-GUIDE.md`; the SHACL regression-lock sequencing hangs on that divergence being live, and it is currently second-hand.
- Commit `ADOPTION-GUIDE.md` and the four appended ledger rows in a single parent commit; `cyberAlchemy-v2` is not a submodule, so the submodule-first rule does not apply.
- Surface OQ-1's ratification state in `STABLE-REPOSITORY-CONSTITUTION.md` before treating the link checker as adoptable.

## Recommendation

The keystone is the pre-flight gap, not the tool list. The licensing fact is landed and checkable: commit `7f26e738` predates this conversation and is byte-identical to what 21 agents re-derived — so the dispatch machinery is sound (the gate caught a real tension defect; the reviewers killed a manufactured recommendation and two factual errors) while the step *before* it is missing entirely. Attack that first: a search of the target tree is cheaper than any fan-out, and no amount of anti-bias rigour downstream recovers the cost of answering a question the repository had already answered. Second, verify D29↔D16 personally before scheduling any fix; that finding is the one place a deterministic tool beats a demonstrated failure of manual review, and it is the only load-bearing claim in `ADOPTION-GUIDE.md` that this session did not check with its own eyes.

## Files touched

- cyberAlchemy-v2/research/oss-tooling-candidates/ADOPTION-GUIDE.md
- telemetry/agents/subagents-dispatch.yaml
