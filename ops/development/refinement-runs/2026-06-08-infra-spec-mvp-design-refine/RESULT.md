# Refine Result: Infra-Spec MVP Design

- **Target:** infra-spec research synthesis corpus (`ops/development/infra-spec-*.md`)
- **Status:** **pass**
- **Preset:** full
- **Research:** research-if-gap-appears (no external research; prior submodule gaps now closed)
- **Run manifest:** `RUN-MANIFEST.md` · **Evidence index:** `evidence-index.json` · **Seed:** `REFINE-SEED-PROPOSAL.md`
- **Dispatch route:** `REFINE-DISPATCH.json` (validated `pass`) · **Runtime handoff:** `RUNTIME-HANDOFF.md`

## Dispatch strategy
- Overlays: `baseline_sequence`, `dialectic_for_tension`, `tournament_for_alternatives`, `toy_game_for_low_cost_falsification`, `memory_residue_for_context_recovery` (xray/route_menu/protected_context recorded as not-selected with reasons).
- Subagent strategy: recommended → operator authorized "Run with subagents" → 3 reviewers executed (fanout → parent_synthesis), all `pass`.

## Headline outcome
Turned the research synthesis into an MVP-ready, **buildable, candidate-only** infra-spec design:

- **Candidate schema** `candidate/infra-spec.schema.json` — self-contained JSON Schema for the operational-contract spine (runtime_profile → environments → services → boundaries → state_namespaces + fail-closed gates + 7-state status + typed residue + reversal). Reuses dispatch-spec `$def` shapes; redefines `boundary.kind` for infra; encodes evidence≠authority, schema≠instance, analogy-labeling, counterexample (residue≥1), status-namespacing.
- **Falsification surface** `fixtures/` — 10 fixtures (1 spine-pass + 6 shape-layer + 3 governance-layer) + expectation README.
- **Toy-game evidence** — `jsonschema` run over all fixtures → **ALL EXPECTATIONS MET** (spine passes; 6 shape violations rejected; 3 governance violations correctly pass shape, pending the deferred validator).
- **Non-executed plan** — build sequence to a package, each step owner-gated; nothing promoted.

## Stage evidence
- Context Builder: **pass** · Invoke Define: **pass** · Interrogation refine-review: **pass** (shape-vs-governance split clarified)
- Research decision: **pass** (no external) · Distill: **pass** (Shape A wins, recomposition proof)
- Invoke Design: **pass** (schema + fixtures emitted) · Interrogation design-review: **pass**
- Distill Repair (toy-game): **pass** (ALL EXPECTATIONS MET) · Invoke Plan: **pass** · Final + Synthesis: **pass**

## Subagent receipts
- `mvp-shape-tournament-reviewer` — **pass** (Shape A winner + recomposition proof)
- `schema-evidence-discipline-reviewer` — **pass** (full field spec + reuse map + discipline checks)
- `fixture-falsification-reviewer` — **pass** (8-fixture minimum set + reversal/lifecycle fixtures)
Full receipts: `stages/subagent-receipts.md`.

## Final synthesis
From "infra-spec is worth building as an evidence substrate" (prior research) to "here is the smallest buildable operational-contract spine — a runnable candidate schema, falsified at the shape layer, with the governance validator as the single next route." No package promoted; runtime evidence never self-promotes.

## Recommended next routes (not executed)
1. Build `validate-infra-spec.py` (the 6 governance rules) + wire the 3 governance fixtures to exit-1 — closes the falsification proof.
2. Promote candidate → `formulae/infra-spec/` (owner-gated) switching inlined `gate_action` to `$ref`.
3. Pilot on one real project (body-war or now-available `validation/poker-team`) to author a real instance and surface contract gaps.
4. (separate) re-run research lanes L3/L6 against the now-present submodules to deepen evidence.

## Residue
- Governance validator + 3 governance fixtures: specified, unbuilt.
- 7-stage ladder transition semantics + boundary.kind enum: candidate (need governance fixtures + a real traversal).
- event/queue, runtime `actor`, populated drift: deferred out of MVP.
