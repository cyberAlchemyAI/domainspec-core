# TASK-DVC-008: Generic Live Recomposition Proof

- Slice/layer/wave: S3 / L3 / W3.
- Sources: complete DVC-001..007 receipt chain and `../../../DESIGN.md`.
- Dependency: DVC-007.
- Gap owned: DVC-G10.

## SWU-DVC-008

- Primary behavior: prove one generic Define → Design → Plan route selects
  exact bounded outputs and preserves evidence-state ceilings.
- Independent acceptance: positive and negative live cases reproduce frozen
  expectations, generated/runtime results match canonical behavior, and the
  final audit maps every requirement without a private leak.
- Candidate splits: live positive; live negative; boundary audit.
- Retained boundary: one topology proof needs both useful progress and retained
  fail-closed behavior.
- Write scope:
  `ops/development/2026-07-24-invoke-design-coverage-implementation/work-pack/session-evidence/SWU-DVC-008/`.
- Execution owner: local fallback under Spellcraft.

## Live cases

1. Static deterministic artifact: no UX/runtime extensions, exact N/A evidence.
2. Operator-visible governed state: UX, authority, state/failure, and validation
   outputs required.
3. Omitted second writer: block with unbound persistence/concurrency signal.
4. Planned fixture mislabeled executed: block illegal evidence state.

## Ordered proof

1. Bind exact canonical/generated/version digests.
2. Run Define and Design for every case.
3. Compare selections and diagnostics to the frozen corpus.
4. Route only validator-passed positive Design into Plan.
5. Confirm Plan begins at `plan-evidence-pending`.
6. Confirm blocked Design never routes as normal implementation readiness.
7. Run aggregate regression and public/private scan.
8. Map receipts to DVC-R01..R14 and record residue.

## Validation

```bash
arcanum/spells/invoke/development/run-design-selection-fixtures.sh
arcanum/spells/invoke/development/run-validation-fixtures.sh
git diff --check -- arcanum/spells/invoke .agents/skills/invoke .claude/skills/invoke
```

## Closeout

Return live inputs/outputs, exact digests, selection comparisons, evidence-state
trace, regressions, leakage result, and recomposition table. Use DVC-008 row.

## Completion evidence

- Pass: all four live cases reproduce the frozen expectations on canonical,
  repo-codex, and Claude runtime surfaces.
- Positive Designs route normally only at `design-validator-pass` and start
  Plan at `plan-evidence-pending`; blocked Designs never claim normal
  implementation readiness.
- The DVC/generated public scan is clean. Four pre-existing local-path
  references outside this task's write scope remain explicit final-audit
  residue.
- Receipt: `../session-evidence/SWU-DVC-008/execution-receipt.json`.
