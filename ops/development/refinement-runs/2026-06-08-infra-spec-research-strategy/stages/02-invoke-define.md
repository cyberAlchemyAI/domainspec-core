# Stage 02 — Invoke Define

Capability: `invoke` · Mode: `define` · Runtime: native (Claude Code) · Status: **pass (re-baselined)**
Inputs: corrected `context-builder-frame`, `REFINE-SEED-PROPOSAL.md`

## Definition: what we are refining

We are refining an **existing, well-developed research strategy** — not authoring one. The artifact pair (`infra-spec-research-strategy.md` + `.dispatch.json`, 2026-06-03) defines a 7-lane, path-cited, recursively-expandable research route whose output is "the route that makes the [future infra-spec] package worth creating." The operator request is "see if we can make it better."

**Make it better, defined as testable goals:**

- B1 (correctness): the dispatch route **passes the native dispatch validator** (it currently blocks). This satisfies the strategy's own non-negotiable.
- B2 (runnability): the strategy's documented self-test command points at a validator that exists in this checkout (currently points at the empty `arcanum/` submodule).
- B3 (unambiguity): the strategy states its scope boundary versus the adjacent `ops/` runtime-surface convergence program, so a reader (or agent) does not conflate the two — a failure that actually occurred in this run.
- B4 (no regression): the existing design strengths (7 lanes, Lean discipline, child-dispatch triggers, boundary_evidence, promotion guardrails, candidate concepts, expected artifacts) are preserved, not rewritten.

## What is already good (preserve)

- Clear thesis that infra-spec is a governed contract, not prettified deployment docs.
- Strong evidence discipline: path-cited claims, analogy labeling, runtime-evidence ≠ promotion authority.
- Owner-boundary awareness and a write boundary confined to `ops/development/infra-spec-*`.
- A genuine adversarial structure: zig-zag critique (skeptic + owner-boundary roles) and an interpretation tournament over 5 competing readings.
- Recursion control via explicit child-dispatch triggers and minimum child-dispatch fields.

## What is wrong or weak (the improvement surface)

1. **Blocks its own validation gate** (B1) — `subagent_strategy.receipt_requirements` lacks the native-receipt and lifecycle field tokens the validator requires; 4 steps use real-but-non-canonical skill handles (`x-ray`, `decision-gate`, `robot-talks`, `implementation-readiness`) without `capability_status`/`capability_metadata`.
2. **Broken self-test command** (B2) — `.md` validation command path is not runnable in this checkout.
3. **Scope ambiguity** (B3) — nothing in the strategy distinguishes infra-spec from runtime-surface convergence; the names and the `ops/development/` location collide.
4. **Cost/sequencing** (secondary) — 7 simultaneous lanes is a heavy first execution with no MVP-first ordering; a cheaper minimum first pass would de-risk before full fan-out.

## Smallest Coherent Unit (candidate for Distill)

> *"A validity-and-clarity repair: make the existing infra-spec research strategy pass the native validator, fix its self-test command, and add a one-paragraph scope boundary — preserving all existing lane design — with MVP-first lane ordering offered as a recommendation, not a forced change."*

## Definition of success (restated)

- B1–B3 are mechanically verifiable (validator `pass`; command runs; scope note present).
- B4 holds (diff is additive/surgical, not a rewrite).
- The MVP-first ordering is recorded as a design recommendation + residue, not imposed.

## Verdict

`pass` — the refinement target is now correctly scoped and bounded around concrete, testable improvements. Routed to Interrogation (Stage 03).
