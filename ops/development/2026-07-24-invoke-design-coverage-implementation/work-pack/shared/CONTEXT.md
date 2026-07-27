# Shared Context: Invoke Design Coverage

## Source contracts

- `../../../DEFINE.md`: requirements DVC-R01..R14 and public boundary.
- `../../../DESIGN.md`: component contracts and deterministic algorithms.
- `../../../DESIGN-SCOPE-MANIFEST.yaml`: authored target footprint and current
  source digests.
- `../../../CONCERN-LEDGER.md`: primary ownership and current dispositions.
- `../../../UX-PLAN.md`: human semantic contract.
- `../../../GAPS.md`: implementation gaps and dirty-baseline residue.
- accepted research:
  `../../../2026-07-24-invoke-lifecycle-progress-update/research/2026-07-24-design-phase-coverage/findings.md`.

## Authority precedence

1. Canonical public Arcanum source.
2. Spellcraft lifecycle decisions and validation receipts.
3. This approved private Define/Design/Plan package.
4. Execution receipts.
5. Generated profiles, Inventory, and observability as non-authoritative
   projections.

## Global constraints

- One SWU per execution handoff.
- Capture the live baseline before every write.
- Preserve unrelated dirty changes; do not rewrite or normalize them.
- New public artifacts contain generic identifiers and synthetic data only.
- Frozen expected fixture results cannot be changed inside implementation SWUs.
- Plan evidence and promotion remain separate from Design validation.

## Expected SWU result

```yaml
swu_id: string
result: pass | flag | block | interrupted
capability_ref: spellcraft
receipt_kind: native-stage | local-fallback | blocked
receipt_artifact: path-or-none
files_touched: [path]
validation: [command-and-result]
blockers: [item]
residue: [item]
reroute: owner-or-none
handoff_note: string
```
