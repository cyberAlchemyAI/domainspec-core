# TASK-DVC-005: Frozen And Mutation Fixture Runner

- Slice/layer/wave: S1 / L1 / W1.
- Source: TASK-DVC-001 corpus and DVC-002/003/004 receipts.
- Dependency: DVC-004.
- Gap owned: DVC-G07.

## SWU-DVC-005

- Primary behavior: execute every frozen case and predicate mutation, comparing
  exact outputs and diagnostics.
- Independent acceptance: the runner returns nonzero on any missing case,
  changed expectation, surviving mutation, nondeterministic digest, or
  unexpected selection.
- Candidate splits: schema runner; frozen cases; mutation cases; summary.
- Retained boundary: one command must join all groups into one L1 gate.
- Write scope:
  `arcanum/spells/invoke/development/run-design-selection-fixtures.sh` and
  new files under
  `arcanum/spells/invoke/development/fixtures/design-selection/`.
- Execution owner: local fallback under Spellcraft.

## Ordered implementation

1. Validate schemas.
2. Verify frozen corpus digest.
3. Execute each manifest through extractor and validator.
4. Compare exact normalized result, selection set, evidence state, and
   diagnostic codes.
5. Generate one mutation per predicate and required field.
6. Require every mutation to fail for the expected reason.
7. Execute twice and compare output digests.
8. Emit machine JSON and human Markdown summaries.

## Validation

```bash
arcanum/spells/invoke/development/run-design-selection-fixtures.sh
arcanum/spells/invoke/development/run-design-selection-fixtures.sh --group mutations
git diff --check -- arcanum/spells/invoke/development/run-design-selection-fixtures.sh arcanum/spells/invoke/development/fixtures/design-selection
```

## Failure modes

- skipped fixture;
- order-dependent output;
- mutation generator mutates expected result instead of input;
- private evidence in public fixture;
- runner overwrites the frozen denominator.

## Closeout

Use the DVC-005 row and attach the exact runner summary plus corpus digest.

## Completion evidence

- Result: pass.
- Frozen cases: 28/28.
- Predicate and field mutations: 27/27.
- Corpus digest unchanged:
  `347618abe9ae700fb515a127d4d5a75a78665013dbc68fd637bd5bd7200a5c74`.
- Summaries:
  `../session-evidence/SWU-DVC-005/execution-receipt.json` and
  `../../../../../../arcanum/spells/invoke/development/fixtures/design-selection/results/`.
