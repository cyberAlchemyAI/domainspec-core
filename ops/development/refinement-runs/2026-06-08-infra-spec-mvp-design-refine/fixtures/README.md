# Infra-Spec MVP Fixtures — Falsification Surface

Candidate schema: `../candidate/infra-spec.schema.json` (self-contained Draft 2020-12).
Two-layer discipline (from dispatch-spec): **shape** layer = JSON Schema; **governance** layer = `validate-infra-spec.py` (deferred next route, NOT built in this candidate-only refine).

Toy-game run (this refine): `python3 -c "Draft202012Validator(...)"` over all fixtures → **ALL EXPECTATIONS MET**.

| Fixture | Layer | Falsifies | Expected shape verdict | Result |
| --- | --- | --- | --- | --- |
| `spine-pass.json` | baseline | — (valid spine) | PASS | ✅ pass |
| `v-bad-runtime-profile.json` | shape | runtime_profile enum | FAIL | ✅ fail |
| `v-boundary-enum-leak.json` | shape | dispatch capability enum leaked into infra boundary.kind | FAIL | ✅ fail |
| `v-collapsed-status.json` | shape | collapsed bare `status` (namespacing) | FAIL | ✅ fail |
| `v-empty-environments.json` | shape | environments ≥1 | FAIL | ✅ fail |
| `v-empty-residue.json` | shape | residue ≥1 (counterexample discipline) | FAIL | ✅ fail |
| `v-missing-owner.json` | shape | service.owner required | FAIL | ✅ fail |
| `v-no-rollback-on-promoted.json` | governance | promoted without `reversal.rollback` (N12, gap G5) | shape PASS → needs script | ✅ shape-pass |
| `v-self-promoting-gate.json` | governance | promotion_guardrail `on_fail: flag` (evidence self-promotes, N11) | shape PASS → needs script | ✅ shape-pass |
| `v-status-floor.json` | governance | stage `validated` with no receipt/observability evidence (N5) | shape PASS → needs script | ✅ shape-pass |

## Governance rules the deferred `validate-infra-spec.py` must add
1. fail-closed gate: any `promotion_guardrail` (and `secret`/`data_store` boundary) must have `on_fail`/`on_violation: block`.
2. status-floor: `stage ≥ deployed` requires a matching receipt; `≥ validated` requires observability/SLO evidence; evidence_refs justify, never grant.
3. reversal obligation: `stage: promoted` (or a production env) requires `reversal.rollback`; every `data_store` boundary requires `reversal.backup`; every `migration.forward` requires `migration.reverse`.
4. unowned-state: every declared state path / `data_store` must appear in `state_namespaces` with exactly one owner.
5. analogy-labeling: borrowed-register vocabulary in free-text obligations requires an `analogy_labels[]` entry.
6. blocker≠failure: validator tooling errors surface as `VALIDATION=blocked`, distinct from governance `block`.
