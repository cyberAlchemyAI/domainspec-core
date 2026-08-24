# TASK-AKV-CONTRACTS — Query and relation semantics

## Objective

Turn the reviewed blueprint into executable, closed query and relation
contracts without populating official-source data.

## Source anchors

- Query matrix: `../../../refinement-runs/20260803T175423Z-animejs-blocking-defects/stages/08-query-contract-matrix.json`
- Relation matrix: `../../../refinement-runs/20260803T175423Z-animejs-blocking-defects/stages/08-relation-behavior-witness-matrix.json`
- Reviewed synthesis: `../../../research/2026-08-03-animejs-agent-knowledge-vault/receipts/knowledge-vault-synthesis-reviewer-repair.json`

## SWU-AKV-NV-001 — closed query contract

- Primary behavior: QRY-003 deterministically selects, conflicts, or abstains using only the declared code vocabulary.
- Inputs: normalized requested features, exact VersionContext, JS/WAAPI candidate facts, conflicts, and evidence gaps.
- Outputs: immutable QueryReceipt with selected IDs, nullable success code, one primary abstention code, subordinate gaps, graph digest, and algorithm version.
- Algorithm: validate context; generate JS/WAAPI candidates; reject unknown/stale facts; apply total primary-code precedence; co-select exact ties; emit `ABSTAIN_AMBIGUOUS_INTENT`; sort stable IDs; persist no authority effect.
- Edge cases: missing version, unknown requirement, conflict, performance claim without witness, exact tie, successful JS, successful WAAPI, multiple subordinate gaps.
- Write scope: `profile.json`, `contracts/query-contracts.json`, `schemas/query-receipt.schema.json`, `scripts/query.mjs`, `fixtures/query-cases.json`, `tests/query-contract.test.mjs`.
- Done: all eight planned terminal paths execute and historical receipt migration is versioned rather than rewritten.
- Validation: `node projects/animejs/ontology/agent-knowledge-vault/tests/query-contract.test.mjs`.
- Split analysis: schema, algorithm, and fixtures cannot pass independently because the acceptance boundary is executable receipt closure; source ingestion is independent and deferred.
- Execution owner: local fallback or one bounded lifecycle helper.

## SWU-AKV-NV-002 — relation canonicalization

- Primary behavior: admit exactly 17 retained relations, select one canonical representation for five merged rows, and exclude three deferred rows.
- Algorithm: start from the 25-row matrix; keep RETAIN rows; resolve MERGE rows as follows: `WorkEpisode.task_id` is canonical for addresses; `Attempt.episode_id` is canonical and `WorkEpisode.attempt_ids` derived for contains; `Outcome.attempt_id` is canonical and `Attempt.outcome_id` reverse-derived for yields; `NextQuestion.gap_id` is canonical and receipt question IDs derived for suggestsNextQuestion; `QueryReceipt.evidence_record_ids` is canonical for citesEvidence. Record `observes`, `applies`, and `exposesGap` as deferred residue and reject them as stored edges.
- Write scope: `contracts/relation-vocabulary.json`, `contracts/relation-decisions.json`, `schemas/relation.schema.json`, `scripts/validate-relations.mjs`.
- Done: relation IDs/names/endpoints are unique, five merge decisions cannot diverge, and no deferred relation is admitted.
- Validation: `node projects/animejs/ontology/agent-knowledge-vault/scripts/validate-relations.mjs --definitions-only`.
- Split analysis: merge and defer decisions jointly define the closed stored relation vocabulary; witness execution remains independently verifiable in 003.
- Execution owner: local fallback.

## SWU-AKV-NV-003 — relation mutation witnesses

- Primary behavior: every retained relation produces an observable baseline/mutant delta.
- Algorithm: load the 17 retained rows; construct one minimal fixture per row; run the declared consumer on baseline and one changed/removed edge; assert the planned output delta and failure assertion; fail on surviving, missing, or duplicate witnesses.
- Write scope: `fixtures/relation-witnesses.json`, `tests/relation-witnesses.test.mjs`.
- Done: exactly 17 witnesses execute, every mutant is killed, five merge and three deferred rows are absent from the retained witness set.
- Validation: `node projects/animejs/ontology/agent-knowledge-vault/tests/relation-witnesses.test.mjs`.
- Split analysis: each fixture is data, but the acceptance boundary is the closed all-retained relation gate; source coverage is independent and deferred.
- Execution owner: local fallback.
