# Stage 08 — Distill Repair (validate / toy-game)
Capability: `distill` · Mode: `validate` · Overlay: `toy_game_for_low_cost_falsification` · Status: **pass**

## Toy-game evidence (run)
`Draft202012Validator` over `candidate/infra-spec.schema.json` × all 10 fixtures → **ALL EXPECTATIONS MET**:
- `spine-pass` → shape PASS ✅
- 6 shape-layer violations → shape FAIL ✅ (enum/required/minItems/namespacing, each for the correct reason)
- 3 governance-layer violations → shape PASS ✅ (correctly NOT caught; require `validate-infra-spec.py`)

Evidence artifact: `fixtures/README.md` (expectation table) + this stage. Reproduce: load schema + iter_errors per fixture.

## Failure routing
If any expectation had mismatched, route back to Stage 06. None did.

## Residue carried
- Governance layer (`validate-infra-spec.py` + its 6 rules) is specified but unbuilt — the explicit next route.
- 7-stage ladder transition semantics + boundary.kind enum remain candidate pending governance fixtures.

## Verdict
`pass` — the candidate schema is falsified at the shape layer with verified evidence; governance layer cleanly delineated.
