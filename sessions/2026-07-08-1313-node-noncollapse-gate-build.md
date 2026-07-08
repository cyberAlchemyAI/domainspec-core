---
tags: [domainspec-v2, meta-type-formalization, non-collapse-gate, node-edge-collapse, red-team-review, d6-definitions, validator-checker, type-system-registry, saga-workflow-merge]
node_type: test
is_session: true
layer: architecture
nature: technical, procedural
status: active
created: 2026-07-08
timestamp: 2026-07-08T13:13:37-03:00
expires: 2026-09-06
conversation_id: 2026-07-08-node-noncollapse-gate-build
decisions_made: true
contradictions_found: true
specs_updated: [projects/domainspec-v2/definitions/DEFINITIONS.md, projects/domainspec-v2/definitions/reviews/2026-07-08-d6-node-noncollapse.md, projects/domainspec-v2/development/meta-type-formalization/research/2026-07-07-node-noncollapse-gate-redteam/DESIGN-SPEC-v2.md, projects/domainspec-v2/development/meta-type-formalization/research/2026-07-07-node-noncollapse-gate-redteam/findings.md, telemetry/agents/subagents-dispatch.yaml]
promoted_candidates: []
expected_importance: 7
importance_rationale: "Closes the OQ-6 structural gap with a red-teamed, corrected, and now-tested node non-collapse gate that D6 promotion depends on; docked because promotion itself stays blocked on the unresolved DEC-DSV2-SAGA-MERGE owner decision."
---

# Node non-collapse gate — red-teamed, built, hardened, and carded on D6

## Summary

This session turned the domainspec-v2 discovery's OQ-6 (nodes lack the non-collapse gate that edges have) into a built, tested, and carded rule. After I explained the edge admissibility law (domainspec-v2-D3) and designed a first node non-collapse gate with three witnesses, the user chose to red-team the design before building it. A review dispatch (routed domainspec-subagents-strategy → review → check-tension PASS/PASS → registered in telemetry) ran three tensioned attackers (vacuity/Taleb, definitional/Tarski, counter-example/Turing) + robot-talks + synthesizer + two verifiers + auditor, returning FIX (5 CRITICAL + 3 MAJOR, 2 dropped on refutation, closed resolved, 9 agents). The load-bearing findings: the rule was seated on the wrong card (b1 — D18 disclaims meta-type formation, so it belongs on D6), the edge witness read cheatable raw schema slices (a1), the design self-contradicted on Rule/Policy/Calculation (c1), and it miscounted the rule vocabulary (c2 — 7 on-disk keywords, not 4). An author agent rewrote it as DESIGN-SPEC-v2 resolving all 8 change-requests plus an honest residue (a semantic trio is non-collapse-checkable at the shape layer), and an independent validator confirmed READY-TO-INSTALL with no live authority touched. On "build the checker first," I implemented validate-meta-types-noncollapse.ts, which resolves edge witnesses through the DS-D8 relationship authority (not raw slices) and on the real 14-type registry fires exactly once (Saga~Workflow) with no over-rejection and all five acceptance checks passing. On "harden first," I split the logic into a testable lib + thin CLI and added 7 tests — an anti-cheat attestation-permutation invariance test, a fresh-duplicate test, and an exception-lane-mechanism test among them — all green with a clean typecheck, and I surfaced (did not fix) 6 pre-existing unrelated failures in validate-relationships.test.ts. Finally I added the third challenge (node non-collapse) to D6's challenge contract in DEFINITIONS.md — the node-side mirror of the D3 edge-law, pointing at the checker — keeping the card candidate and writing a residue note. Promotion of D6 to active remains blocked on a single owner decision: whether to merge Saga into Workflow (DEC-DSV2-SAGA-MERGE, default merge).

## Contradictions

- validates `projects/domainspec-v2/definitions/DEFINITIONS.md` (D6) — the built checker operationalizes D6's new third challenge (node non-collapse) and empirically confirms it fires exactly once on the live 14-type registry with no over-rejection.
- questions `projects/domainspec-v2/definitions/DEFINITIONS.md` (D18) — red-team finding b1 showed the original design wrongly seated the rule on D18, which disclaims DS-D1 meta-type formation; corrected to D6 this session (no change to D18 itself).

## Open questions

- Can mechanical non-laundering detection ever replace the owner-enumerated exception lane, or is the return-sort trio (Rule/Policy/Calculation) a permanent shape-layer exception because telling them apart requires meaning the D15 moat forbids the validator to read?
- Is "edge witness resolved through the DS-D8 authority" the right permanent reading of the edge witness, or must it tighten to "an edge exercised in a real aspect instance" once aspect files exist — the stricter reading over-rejects today because almost nothing is exercised yet?

## Next steps

- Rule on DEC-DSV2-SAGA-MERGE (default merge); if merged, apply Saga → Workflow + `scope` flag across `projects/domainspec-v2/definitions/meta-types/` and the schemas, then promote D6's third challenge candidate→active per its confirm contract.
- Wire the checker into the impl validate pipeline: add a `validate:noncollapse` script to `projects/domainspec-v2/impl/package.json` and include it in `npm run validate`.
- Triage the 6 pre-existing `validate-relationships.test.ts` failures (separate from this work; surfaced, not fixed).

## Recommendation

Keystone is the Saga → Workflow merge decision — it is the sole blocker to promoting D6's third challenge to active. This is licensed by a landed fact, not a hunch: the hardened checker fires exactly once (Saga~Workflow) with zero over-rejection and a green test suite. The next session should put DEC-DSV2-SAGA-MERGE to the owner and, if merged, apply the merge and promote D6; the checker is already built to gate the result.

## Files touched

- projects/domainspec-v2/definitions/DEFINITIONS.md
- projects/domainspec-v2/definitions/reviews/2026-07-08-d6-node-noncollapse.md
- projects/domainspec-v2/impl/tools/validate-meta-types-noncollapse.ts
- projects/domainspec-v2/impl/tools/lib/meta-type-noncollapse.ts
- projects/domainspec-v2/impl/tools/tests/validate-meta-types-noncollapse.test.ts
- projects/domainspec-v2/development/meta-type-formalization/research/2026-07-07-node-noncollapse-gate-redteam/DESIGN-SPEC.md
- projects/domainspec-v2/development/meta-type-formalization/research/2026-07-07-node-noncollapse-gate-redteam/attacks.md
- projects/domainspec-v2/development/meta-type-formalization/research/2026-07-07-node-noncollapse-gate-redteam/findings.md
- projects/domainspec-v2/development/meta-type-formalization/research/2026-07-07-node-noncollapse-gate-redteam/DESIGN-SPEC-v2.md
- telemetry/agents/subagents-dispatch.yaml
- projects/domainspec-v2/impl/package-lock.json
