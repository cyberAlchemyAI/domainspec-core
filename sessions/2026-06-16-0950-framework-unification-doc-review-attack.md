---
tags: [framework-unification, review, red-team, subagents, overclaim, sibling-repos]
node_type: discovery
is_session: true
layer: architecture
nature: procedural, technical
status: active
created: 2026-06-16
timestamp: 2026-06-16T09:50:56-03:00
expires: 2026-08-15
conversation_id: 2026-06-16-framework-unification-doc-review-attack
decisions_made: true
contradictions_found: true
specs_updated: [telemetry/agents/subagents-dispatch.yaml]
promoted_candidates: []
expected_importance: 6
importance_rationale: "A verified red-team of the orientation docs whose sibling-repo evidence corrects two load-bearing claims and resolves the OQ-5 gate, without yet editing the targets."
---

# Framework Unification — Document Review (Fresh Attack + Verification)

## Summary

Red-teamed the three orientation artifacts (RESEARCH.md, domainspec-findings.md, discovery.md) with a fresh 3-agent attack pass and a 2-agent adversarial verification gate (both registered in the dispatch ledger), avoiding the prior round's already-fixed findings. Then traced the "aspirational/missing/by-description" claims into the sibling clones of the uninitialized `arcanum` and `domainspec` submodules: the evidence **softened** two findings (pipeline-signals.jsonl is real-but-misrooted in the domainspec submodule; the Lean repo + `permguard.exe` are real and built) and **hardened** one (SCOPE §1 "sorry-free proofs" is an overclaim — 123/276 `.lean` carry `sorry`; only kernel files are clean). Net durable change-requests: 2 MAJORs in SCOPE.md plus an E-1 re-scope (a PostToolUse tool-events producer exists; the central sigil-invocations ledger still lacks a live dispatch producer). No target docs were edited — review only, per owner.

## Contradictions

- questions `projects/framework-unification/research/RESEARCH.md` — "central ledger has no producer / nothing feeds it" and the pipeline-signals "real" path are both contradicted by sibling-repo evidence (a tool-events hook exists; pipeline-signals.jsonl lives in the domainspec submodule).
- questions `projects/framework-unification/SCOPE.md` §1 — "sorry-free proofs" is an overclaim of the whole Lean program (123/276 `.lean` files carry `sorry`); only kernel files are clean.

## Next Steps

- Apply the 2 SCOPE.md MAJOR edits: "sorry-free proofs"→kernel-only, and resolve the §5 identity-vs-novelty reframe — projects/framework-unification/SCOPE.md §1.
- Re-scope E-1/F3/OQ-3 wording: a tool-events producer exists; the central ledger lacks a live *dispatch* producer — RESEARCH.md, research/domainspec-findings.md, discovery/discovery.md.
- Fix E-2 path note + T-3 Lean attribution (RESEARCH.md); fold IMPROVEMENTS OQ-i reframe into the A-1 body.
- Mark discovery OQ-5 resolvable — real engine/Lean code is available in sibling clones — discovery/discovery.md.
- Append close rows for both dispatches in telemetry/agents/subagents-dispatch.yaml.

## Open Questions

- Keep the §5 collapse-test bar in SCOPE §1, or assume "OQ discipline = residuality-spec per-artifact"? — SCOPE.md §1.
- Does the existing PostToolUse hook change OQ-3's producer scope (extend vs greenfield)? — discovery.md OQ-3.

## Files touched

- telemetry/agents/subagents-dispatch.yaml
