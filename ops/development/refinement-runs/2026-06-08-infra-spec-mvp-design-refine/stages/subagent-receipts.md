# Subagent Receipts (delegated reviewers)

Authorization: operator approved "Run with subagents". Parallelism: fanout · Join: parent_synthesis · Dispatch: `2026-06-08-infra-spec-mvp-design-refine`

## Receipt — mvp-shape-tournament-reviewer
- agent_id: review-mvp-tournament · spawn: spawned · join: completed · close: closed · status: **pass**
- applies_to_steps: s05, s06, s10 · capability_ref: distill (review)
- findings: Tournament A (contract-spine) vs B (evidence-first) vs C (schema-only). **Winner A** — only shape independently useful with the repo's intent-without-instances evidence while still carrying the R3 invariant (promotion_gate + status floor = evidence≠authority from day one). B inverts the dependency DAG and risks runtime-evidence self-promotion before a gate exists; C drops evidence≠authority entirely.
- recomposition_proof: receipts/drift/signals attach additively along DAG edges N2→N7→N8/N9/N10 as optional-but-typed fields; no rename, no required-floor re-litigation.
- mvp_field_set: required floor (infra_spec_id, schema_version, project, runtime_profile, environments≥1, services≥1, gates≥1, residue≥1, promotion_status) + typed-when-present body. Defer: N12 reversal (net-new, keep but residue), event/queue, populated drift, runtime `actor`, ladder transition semantics.
- validation impact: adopt dispatch two-layer pattern (schema=shape, script=governance); namespacing of doc/gate/promotion status is the #1 rework risk.
- blocked_fields_or_no_block: **no-block** · residue: ladder transition rules unproven (keep enum, defer rules) · reroute: none

## Receipt — schema-evidence-discipline-reviewer
- agent_id: review-schema-discipline · spawn: spawned · join: completed · close: closed · status: **pass**
- applies_to_steps: s03, s06, s07 · capability_ref: interrogation (review)
- reuse_map: boundary → reuse-shape/redefine-kind; authority_map → reuse-with-infra-slots; receipt_expectation → reuse-with-changes; state_namespace → reuse-as-is; promotion_split → **reuse-as-is (the evidence≠authority enforcer)**; gate/gate_action → reuse, trim kind enum, adopt live gate ids; technique_ref → n/a.
- boundary_kind_enum: `network | secret | data_store | tenant | policy | environment` (NOT the dispatch capability enum).
- proposed_schema_fields: full YAML field spec (required floor + typed body + analogy_labels + promotion_status).
- discipline_checks: schema≠instance, evidence≠promotion-authority, status separation, analogy-labeling, counterexample (residue≥1), blocker≠failure.
- promotion_guardrail: `status_class: const candidate` required field → no schema path to author a non-candidate record; promotion gated by promotion_guardrail gate + promotion_split with on_violation=block.
- blocked_fields_or_no_block: **no-block** · residue: boundary.kind enum + 7-stage ladder remain candidate (need fixtures); Lean discipline is method-only (source absent) · reroute: none

## Receipt — fixture-falsification-reviewer
- agent_id: review-fixtures · spawn: spawned · join: completed · close: closed · status: **pass**
- applies_to_steps: s08, s09 · capability_ref: distill (review)
- fixture_plan: 1 PASS + 1 VIOLATION per kept axis; each names the validator layer (schema-shape vs governance-script) that must reject it.
- reversal_lifecycle_fixtures: rollback/migration/backup/retention/burn-rate pass+violation; promoted-without-rollback → governance block (the net-new must-add).
- minimum_fixture_set: 8 fixtures (spine-pass + v-empty-residue, v-unowned-state, v-spec-without-instance, v-no-rollback-on-promoted, v-self-promoting-gate, v-status-floor, v-collapsed-status).
- coverage_check: maps each violation to gap-hunt gaps (G1,G3,G4,G5,G6,G7); G9 event/queue intentionally NOT owed (DROP-deferred).
- risks: G7/G3/G10 need non-hermetic probes → downgrade to declared-contract fixtures or `flag`.
- validation impact: enums-as-shape + required-floor cardinality make several violations pure-schema catches; exit-code matrix (block→1, pass/flag→0) is the toy-game proof.
- blocked_fields_or_no_block: **no-block** · reroute: none

## Join synthesis
All three converge on Shape A with a self-consistent schema spec and fixture set. The schema-discipline reviewer's field spec + the fixture reviewer's 8-fixture set are directly authorable. Shape-layer fixtures are cheaply falsifiable now (jsonschema); governance-layer fixtures are specified with expected verdicts, pending the deferred `validate-infra-spec.py` (next route, not this candidate-only refine).
