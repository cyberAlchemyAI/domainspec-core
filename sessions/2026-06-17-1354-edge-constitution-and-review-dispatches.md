---
tags: [ontology, edges, constitution, review, subagents-dispatch]
node_type: constitution
is_session: true
layer: ontology
nature: procedural, technical
status: active
created: 2026-06-17
timestamp: 2026-06-17T13:54:45-03:00
expires: 2026-08-16
conversation_id: 2026-06-17-edge-constitution-and-review-dispatches
decisions_made: true
contradictions_found: false
specs_updated: [implementation/domainspec/vault/constitution/edge-constitution.md, implementation/domainspec/vault/constitution/edge-acyclicity-constitution.md]
promoted_candidates: []
expected_importance: 6
importance_rationale: "Creates the single governance home for the vault's typed-edge shape rules and exercises the review-dispatch loop end to end, but the doc is still exploratory and unenforced."
---

# Edge Constitution + Review Dispatches

## Summary

Confirmed no edges constitution existed in arcanum (only the constitution-governance machinery); authored `edge-constitution.md` in the implementation/domainspec vault, consolidating grammar + constructibility + acyclicity and superseding `edge-acyclicity-constitution.md`, built on conventions Appendix C as catalog of record (not copied, per DRY). Verified `house_project` carries only a stale v1.4.0 mirror of the vault, so nothing changed. Ran two governed `review` dispatches (red-team → fix → re-review): the first found 2 CRITICAL + 4 MAJOR (phantom validators, broken derives-from path, edge-count error, stipulated acyclicity, D1 asymmetry, "never copies" overclaim), all applied inline to v0.1.1; the fix-review confirmed all six RESOLVED and the verifier refuted the one new MAJOR, leaving 4 non-blocking MINOR residues.

## Next Steps

- Apply the 3 MINOR polish (R2 cardinality, R3 coverage footnote, R4 enforced-vs-pending split) to `edge-constitution.md` §5/§6 — offered, pending user go.
- Before promoting past `exploratory`: build the constructibility typecheck + grammar lint validators (§9 gate); only `cycles check --strict` and `edges-check` exist today.
- Reconcile the upstream forward-edge count (Appendix C 22 / §8 21 / row-count 25) in `ontology-conventions.md`.
- On ratification: set `edge-acyclicity-constitution.md` to `status: deprecated`.

## Open Questions

- True forward-edge count of Appendix C (21 vs 22 vs 25) — resolve in `ontology-conventions.md`.
- Acyclicity status of post-v0.1.0 edge types + the creates/modifies/continues-from stipulation — §5 pending-review.
- Predecessor's non-catalog `lenses` edge (R5) — drop or mark illustrative on deprecation?

## Files touched

- implementation/domainspec/vault/constitution/edge-constitution.md
- implementation/domainspec/vault/constitution/edge-acyclicity-constitution.md
- implementation/domainspec/docs/reviews/edge-constitution-2026-06-16/findings.md
- implementation/domainspec/docs/reviews/edge-constitution-2026-06-16/attacks.md
- implementation/domainspec/docs/reviews/edge-constitution-fix-review-2026-06-16/findings.md
- implementation/domainspec/docs/reviews/edge-constitution-fix-review-2026-06-16/attacks.md
- implementation/domainspec/telemetry/agents/subagents-dispatch.yaml
