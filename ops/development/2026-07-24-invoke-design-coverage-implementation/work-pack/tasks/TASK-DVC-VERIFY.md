# TASK-DVC-VERIFY: Final Lifecycle Audit

## Smallest Working Unit Exemption

- Reason: closure-only verification task.
- Allowed because task ID contains `VERIFY`.

## Objective

Join the complete receipt chain, re-run required suites, verify traceability and
public/private boundaries, and assess Spellcraft promotion readiness without
performing promotion.

## Entry

- DVC-001..008 terminal receipts.
- No unresolved acceptance-critical blocker.
- Work-pack, tasks, manifest, and receipt paths agree.

## Checks

- DVC-R01..R14 each have version-bound evidence.
- frozen corpus expectations remain unchanged from W0;
- all mutation tests reject;
- Design/Plan evidence states remain separate;
- normal Plan handoff requires `design-validator-pass`;
- generated parity and source provenance pass;
- public scan is clean;
- full Invoke validation passes;
- Inventory and observability remain non-authoritative;
- no commit, push, release, or promotion is inferred.

## Output

`work-pack/session-evidence/final-audit.json` with pass, flag, or block,
traceability, validation, residue, and recommended next lifecycle decision.

## Completion evidence

- Audit result: `flag`.
- Implementation result: pass; 14/14 SWUs terminal, all 14 requirements
  recomposed, and canonical/generated/live validations pass.
- Promotion readiness: false until the public-hygiene owner classifies or
  repairs the four pre-existing local-path references identified by the
  repo-wide diagnostic.
- No promotion, release, commit, or push was inferred or performed.
