---
tags: [domainspec-v2, discovery, meta-types, formal-cell, test-derivation-engine, typed-graph, spec-ontology-unification, subagents-dispatch, claim-le-proof]
node_type: conceptual
is_session: true
layer: architecture
nature: explanatory, reference
status: active
created: 2026-07-06
timestamp: 2026-07-06T21:04:27-03:00
expires: 2026-09-04
conversation_id: 2026-07-06-domainspec-v2-discovery
decisions_made: false
contradictions_found: false
specs_updated: [projects/domainspec-v2/discovery/domainspec-v2-discovery.md, telemetry/agents/subagents-dispatch.yaml]
promoted_candidates: []
expected_importance: 6
importance_rationale: "Produced a durable, adversarially-verified orientation doc that is the load-bearing upstream for the future view triad; reusable reference, but explanatory synthesis over existing artifacts, not a new proof or canonical mechanism."
---

# Understanding domainspec-v2 end-to-end, and authoring its discovery

## Summary

The session began as deep Q&A — the user opened `authority/AUTHORITY-MODEL.md` and then drilled progressively into what domainspec-v2 actually is and how it works, refusing jargon-reproduction and demanding grounded understanding. Working from the real source (`meta-types.yml`, the schemas, `rules/index.ts`, `formal/ast.ts`, `grammar/index.ts`, `ir/types.ts`, the code-tag tools, the invoke spell, the v2 README), we de-jargoned the core vocabulary: typing a node (a human/agent classification into one of a closed meta-type set, audited by a decidable table-walk), deriving obligations (the pure `derive(graph)` function), validating (shape + edge conformance), layering (the edge-law), drift (mostly a doc map, not a running engine), the Formal cell (the one prose→machine-evaluable bridge, from which expected test values are parsed), and the engine IR (the parsed, flattened typed graph, at finer granularity than the authored concept graph). We established the honest three-actor division — LLM agents author/classify at the edges, the deterministic engine checks and derives, the human owner ratifies — and that the engine is a dumb, deterministic compiler (no LLM/network/clock). Under repeated user pressure I corrected several of my own overclaims: "written by hand" → agent-authored via the `invoke define` spell (L0); `code_pattern` is prose, not an executable template nothing consumes; and the spec→code loop (the `spec-ontology-unification` tower) is a hypothesis under test, not an executed pipeline. The user then asked to write a discovery of domainspec-v2 and to use subagents to write and assess it. I pushed back: the named `domainspec-discovery-writer` agent would refuse (it needs a `findings.md` + a legal vault/feature path, and is a v1 artifact), and a blind writer would discard the synthesized understanding and its honesty caveats — so on the user's confirmation I authored the discovery and dispatched one adversarial reviewer instead. The discovery was written at `projects/domainspec-v2/discovery/domainspec-v2-discovery.md` (system-explanatory, matching v2's provenance-header convention), and the reviewer found one real overclaim (the "25 meta-types" are machine-backed for only the 14 backend types) plus two minor issues, all now fixed; the review dispatch was registered in telemetry. Finally we located the `system-view`/`ontology-view` skills (three variants each; the root variant applies to v2) and flagged that `engineer-view` may lack a root variant, and re-confirmed the close-session skill/repo mismatch (`docs/vault/` is absent; `sessions/` is the real convention).

## Open questions

- Which of the two central bets to attack first: prove the spec→code loop on one real feature (spec→code→drift), or harden `invoke define` from L0 to reliable? The loop-witness looks higher-information-per-effort, but the ordering is undecided.
- Does the `engineer-view` skill exist as a root-scoped variant, or only under `implementation/domainspec` and `validation/poker-team`? If the latter, the v2 view triad cannot be completed at the root until it is installed.

## Next steps

- Run the `test-derivation-engine` live over `impl/spec/features/financial-settlement/` and attach the result as evidence, upgrading the discovery's "exists and runs" claim from source/test-level to verified-running (the reviewer confirmed source+tests present but did not execute the suite).
- Defer pulling the view triad (`ontology-view`/`system-view`/`engineer-view`) over the discovery until it stabilizes — it just took three post-assessment fixes; authoring a view now only earns a reconcile next iteration.
- Reconcile the standing close-session skill mismatch (repo-root `.claude/skills/close-session` targets a non-existent `docs/vault/`; the umbrella uses `sessions/`) — carried unfixed from sessions 2026-07-03-2010 and -2014.

## Recommendation

- The keystone is the **live engine run** over financial-settlement: it is the cheapest move that converts the discovery's central evidence claim from "exists at source level" into "verified running," and it directly discharges the one caveat the adversarial reviewer flagged. This is licensed by that reviewer's explicit note (source + test files confirmed present, suite not executed) — a landed fact, not a hunch. The strategic bet-ordering (Open question 1) should wait behind it, since a working live run also informs which bet is cheaper to pursue.

## Files touched

- projects/domainspec-v2/discovery/domainspec-v2-discovery.md
- telemetry/agents/subagents-dispatch.yaml
