---
id: domainspec-v2-evf-contract-completeness-gap-audit-result
kind: page
type: synthesis
title: DomainSpec v2 EVF contract-completeness gap audit result
updated: 2026-07-20
status: block
confidence: high
dispatch_id: 2026-07-20-evf-contract-completeness-gap-audit
dispatch_type: review
working_folder: projects/domainspec-v2/development/evolvable-validation-framework/reviews/2026-07-20-contract-completeness-gap-audit/
tags:
  - inventory
  - strategy-result
  - dispatch
  - subagents
  - review-change-request
  - audit
  - v2-repo
  - domainspec-implementation
  - validation-harness
  - claim-le-proof
  - machine-view
sources:
  - projects/domainspec-v2/development/evolvable-validation-framework/reviews/2026-07-20-contract-completeness-gap-audit/attacks.md
  - projects/domainspec-v2/development/evolvable-validation-framework/reviews/2026-07-20-contract-completeness-gap-audit/findings.md
  - projects/domainspec-v2/development/evolvable-validation-framework/reviews/2026-07-20-contract-completeness-gap-audit/gap-matrix.json
  - projects/domainspec-v2/definitions/minted-project/supported-profiles.yml
  - projects/domainspec-v2/impl/tools/minted-project/compiler.ts
  - projects/domainspec-v2/impl/tools/minted-project/meta-type-body-adapter.ts
  - projects/domainspec-v2/impl/tools/tests/minted-project-meta-type-body-adapter.test.ts
  - telemetry/agents/subagents-dispatch.yaml
selectors:
  - '#p1-trigger-and-dispatch-shape'
  - '#lanes-and-subagents'
  - '#verified-result'
  - '#final-auditor-rejection'
  - '#invoke-handoff'
  - '#gate-and-ledger-state'
evidence_card_ids: []
evidence_set_ids: []
residue:
  - review-evidence-is-not-machine-authority
  - dec-gcp-001-remains-pending
  - successor-completeness-remains-blocked
  - relationship-coverage-level-needs-owner-decision
  - pre-dispatch-double-pass-artifact-not-located
  - frozen-evidence-drifted-during-audit
  - old-gap-009-fixed-in-live-worktree-not-admitted-authority
  - exact-sixteen-criterion-compiler-parity-not-frozen
  - supported-v1-formation-schema-compatibility-unresolved
  - required-structure-not-evaluated-by-compiler
  - schema-digest-not-bound-through-profile-graph-or-receipt
  - dispatch-loop-ceiling-reached
  - ledger-close-row-is-stale
---

# DomainSpec v2 EVF contract-completeness gap audit result

This is a non-authority Inventory read model of a final-auditor-rejected review
dispatch. Its candidate gap set remains useful, but it is not accepted input to
Invoke because the attacked compiler changed after the evidence freeze. A
read-only live follow-up closes the old duplicate-evaluator allegation only in
the working tree and exposes replacement parity and v1 compatibility gaps that
must be frozen by a new audit.

## P1 trigger and dispatch shape

- Synthesis: 49 evidence records and three denominators had to be reconciled
  across 53 matrix rows and 12 proof-chain columns.
- Context protection: the raw attack and matrix evidence is much larger than the
  planning result a parent should carry.
- Isolation: the audit was read-only and independently falsifiable.
- Parallelism: computational, authority, and adversarial attacks ran
  independently before synthesis.

The P1 trigger passes on all four grounds. This was a real dispatch, not an
inline review.

## Lanes and subagents

1. `attackers`, parallel with robot talks: Ashby attacked computational
   causality, Smithe attacked formal ownership/provenance, and Lawvere attacked
   denominator false-greens. Anti-bias axis: computational execution versus
   formal ownership versus adversarial coverage.
2. `synthesizer`: Bourbaki reconciled attacks into `attacks.md`, `findings.md`,
   and `gap-matrix.json` without turning review evidence into authority.
3. `verifiers`, parallel with robot talks: Capucci attacked category/scope
   inflation while Rittel built concrete vacuity and false-green examples.
   Anti-bias axis: definitional scope versus counterexample non-vacuity.
4. `coverage_auditor`: Loregian independently rechecked denominators, matrix
   structure, evidence digests, test baselines, and the mutation boundary, then
   returned `REJECT` because two compiler evidence digests had drifted.

## Dependency flow

`attackers --sequential--> synthesizer --zig-zag(2)--> verifiers
--sequential--> coverage_auditor`, with one conditional auditor-to-synthesizer
feedback edge. Two whole-sequence loops were used. The second final audit
rejected the candidate, exhausting the registered loop ceiling.

## Verified result

- Frozen normative denominator: 13 backend kinds, 16 formation criteria, and 16
  owner-selected relationship families.
- Derived but unselected diagnostics: 21 endpoint pairs and 29 scoped variants.
- Matrix: 53 rows, 12 columns, 636 complete cells.
- Evidence catalog: structurally complete at 49 records, but no longer a live
  49/49 match. `COMPILER` and `T_COMPILER` drifted after the freeze.
- Surviving findings: 24; refuted `GAP-003`, `GAP-010`, and `GAP-015` are absent.
- Deferred and not-applicable cells all retain reason, owner, authority
  reference, promotion condition, and evidence.
- Baseline checks: `tools:test` 143/143 and `engine:test` 107/107.
- The frozen snapshot classified current experimental v1 as `KEEP`; that
  blanket verdict is not safe for the live worktree because the compiler's
  formation-validation route changed after the freeze.
- Successor completeness, S1, IOLM, and Body War terminal composition remain
  honestly blocked.

## Final auditor rejection

- `COMPILER`: recorded `7e0deaf9...6405`, live `842b86f7...e6a`.
- `T_COMPILER`: recorded `2448566a...441b`, live `3400ec96...04c8`.
- The compiler now imports `validateMintedNodeFormation` and removes its local
  evaluator, directly affecting `GAP-009`; a new adapter and test also changed
  after the matrix freeze.
- The matrix remains a rejected frozen snapshot. Its 24 findings cannot be
  promoted as a live complete denominator until the changed compiler cells and
  `GAP-009` are substantively reassessed.

## Live worktree follow-up

- The old `GAP-009` allegation is fixed in the current working tree: compiler
  formation validation now routes through the shared `evaluateCriteria` kernel
  via `meta-type-body-adapter.ts`.
- Adapter tests exercise all eight current criterion rule forms with both
  positive and discriminating-negative witnesses. Compiler-level integration,
  however, is explicitly demonstrated only for `Operation:writes_state`; exact
  end-to-end parity for all 16 criterion IDs is not frozen.
- The supported experimental v1 profile still declares four JSON
  `formation_schemas`. The compiler currently does not consume those paths,
  uses the canonical YAML criteria instead, and removes `$.body` violations
  from the base node JSON-schema result. The next audit must decide and prove
  whether that is an authorized replacement or a conformance regression.
- The adapter can fail on an expected YAML schema digest, but the compiler does
  not pass the expected digest from a profile owner and does not carry that
  binding through graph or receipt evidence.
- `required_structure` is present in all backend YAML schemas and parsed by the
  shared loader, but this compiler formation path evaluates only `criterion`.
- The compiler, adapter, and three relevant tests are modified or untracked
  working-tree evidence. None is committed authority or release admission.

## Invoke handoff

Invoke authoring is blocked on a fresh accepted audit. After the implementation
stabilizes, that audit must rebuild the complete frozen catalog, include the new
adapter and tests, mark old `GAP-009` fixed only if the frozen evidence still
supports it, prove exact 16-criterion compiler parity, and resolve the supported
v1 formation-schema, digest-binding, and `required_structure` gaps. A later
Invoke may then author definitions, requirements, architecture/design, machine
contracts, and the replacement work-pack inside `projects/domainspec-v2/`.

## Gate and ledger state

- Human confirmation and registration: completed before the original run.
- Check-tension: required by the constitution, but no separate double-pass
  artifact was located in the working folder; retain this as process residue.
- Registration: canonical dispatch row exists.
- Closeout defect: the append-only ledger row was written prematurely as
  `resolved` with one loop. It is stale and cannot be treated as the final
  dispatch outcome.
- Actual final state: `REJECT`; registered loop ceiling of two reached.

## Next human action

Let the DomainSpec v2 implementation stabilize, then confirm a new bounded audit
that refreezes the corpus and tests the compiler delta against the exact 16
criteria plus the supported v1 formation contract. Do not run the full Invoke
authoring pass from this rejected snapshot.
