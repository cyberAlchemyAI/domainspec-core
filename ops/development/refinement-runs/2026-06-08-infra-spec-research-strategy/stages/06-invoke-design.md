# Stage 06 — Invoke Redefine / Design

Capability: `invoke` · Mode: `design` · Runtime: native · Status: **pass**
Inputs: distill-frame (selected unit A) · Overlay carry: `memory_residue_for_context_recovery`

## Design of the improved strategy (surgical, additive)

### Change 1 — Make the dispatch valid (B1)

**a. Subagent receipt-field completeness.** Append the validator-required field tokens to `subagent_strategy.receipt_requirements`, keeping the existing semantic requirements:

- native-receipt fields: `dispatch_id, step_id, capability_ref, status, artifacts, validation, observer_status, blockers, residue, handoff_note`
- lifecycle fields: `agent_id, role_id, spawn_status, join_status, close_status, reroute`

Rationale: the validator checks the receipt-requirement set for these structural tokens; the strategy's prose requirements (path-citing, claim classification, residue) are retained alongside them.

**b. Capability-handle metadata.** For the 4 steps whose `capability_ref` is a real installed skill outside the core dispatch set, add:

```json
"capability_status": "local-extension",
"capability_metadata": { "kind": "installed-native-skill", "provenance": ".claude/skills/<skill>", "note": "Real installed native skill beyond the core dispatch capability set; not a freeform/unknown handle." }
```

Steps: `xray-repository-shape`→`x-ray`, `child-dispatch-decision-gate`→`decision-gate`, `zigzag-lane-critique`→`robot-talks`, `handoff-next-route`→`implementation-readiness`. This is honest: each skill exists under `.claude/skills/`.

> Design proof: the repaired JSON was built and run through `validate-dispatch.py` → **VALIDATION=pass** (see `stages/infra-spec-research-strategy.dispatch.repaired.json`). The fix is verified before being proposed for promotion.

### Change 2 — Repair the self-test command (B2)

In `infra-spec-research-strategy.md` "Validation", replace the submodule path (empty in this checkout) with the in-checkout validator:

```bash
python3 .claude/skills/dispatch-spec/scripts/validate-dispatch.py \
  ops/development/infra-spec-research-strategy.dispatch.json
```

### Change 3 — Scope-boundary paragraph (B3)

Add a short "Scope Boundary" subsection to the `.md` clarifying that **infra-spec** (governed infrastructure/deployment/runtime contract) is distinct from the **runtime-surface convergence** program in `ops/` (skill install surfaces, skills-first policy, command deprecation). Both live under `ops/` and share the word "infra/runtime," which caused a real conflation in this refinement run (and in a delegated reviewer).

### Change 4 (recommendation only, not applied) — MVP-first ordering

Offer, as an explicit recommendation in the handoff, a cheaper first execution: run lanes **L1 (cartographer) + L2 (Lean translator) + L7 (gap hunter)** read-only first, then decide whether the full 7-lane fan-out (L3–L6) is warranted. Carried as residue; **not** edited into the route.

## No-regression guarantee (B4)

The repaired dispatch is byte-identical to the original except: (i) appended receipt-requirement tokens, (ii) added `capability_status`/`capability_metadata` on 4 steps. No lane, gate, boundary, guardrail, technique, overlay, or stop-condition is removed or reworded.

## Verdict

`pass` — design is surgical, verified to validate, and preserves the original design. Routed to design-review.
