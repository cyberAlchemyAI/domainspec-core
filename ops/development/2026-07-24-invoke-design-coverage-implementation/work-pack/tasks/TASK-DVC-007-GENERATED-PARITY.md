# TASK-DVC-007: Generated Runtime Parity

- Slice/layer/wave: S3 / L3 / W3.
- Source: validated W2 canonical receipts.
- Dependencies: DVC-006A..E.
- Gap owned: DVC-G09.

## SWU-DVC-007

- Primary behavior: regenerate runtime profiles from accepted canonical Invoke
  sources and prove parity.
- Independent acceptance: generated Invoke surfaces contain the accepted
  contract, no generated-only semantic delta, and no private content.
- Candidate splits: generate; parity compare; public scan.
- Retained boundary: generation without parity and leakage checks is not a
  valid synchronization receipt.
- Write scope: `.agents/skills/invoke/` and `.claude/skills/invoke/`.
- Forbidden scope: `arcanum/spells/invoke/` canonical sources.
- Execution owner: local fallback under Spellcraft/bootstrap owner.

## Ordered implementation

1. Verify canonical W2 receipt digests.
2. Capture generated-surface baselines.
3. Run the repository bootstrap/profile generator into a fresh temporary
   staging directory.
4. Compare staged `.agents/skills/invoke/` and `.claude/skills/invoke/` against
   the live generated directories.
5. Copy only those two Invoke directories through the owner-approved sync
   operation.
6. Enumerate exactly changed generated paths.
7. Compare semantic fields and required new contract sections.
8. Scan for private package IDs, paths, owner names, and witnesses.
9. Run generated parity and Invoke validation.

## Validation

```bash
stage_dir=$(mktemp -d)
bash arcanum/tools/bootstrap_arcanum.sh --target "$stage_dir" --profile repo-codex,claude --sigils all --spells invoke --force
arcanum/spells/invoke/development/run-validation-fixtures.sh
make bump-check
```

The staged generation command does not authorize copying any path except the
two declared Invoke directories. `make bump-check` is diagnostic only in this
SWU; it does not authorize commit, push, or parent-pointer mutation.

## Failure modes

- generator changes canonical source;
- unrelated generated edits absorbed;
- parity inferred from matching file count;
- private authoring text copied into public output;
- parent gitlink changed.

## Closeout

Return changed generated paths, canonical/source digests, parity checks, leakage
result, and residue through the DVC-007 row.

## Completion evidence

- Pass: both generated Invoke directories exactly match a fresh staged
  repo-codex/Claude bootstrap.
- The sync admitted and changed only 22 DVC-related generated files; existing
  generated edits were already reproduced by canonical generation and were
  preserved.
- The scoped DVC/generated public scan, aggregate Invoke validation, diff
  check, and `make bump-check` pass.
- A broader diagnostic found pre-existing local-path references in canonical
  Invoke development documentation outside this SWU's generated/write scope;
  the live/final boundary audit retains them as explicit residue.
- Receipt:
  `../session-evidence/SWU-DVC-007/execution-receipt.json`.
