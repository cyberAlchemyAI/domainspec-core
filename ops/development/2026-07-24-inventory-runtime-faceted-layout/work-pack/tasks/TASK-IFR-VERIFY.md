# TASK-IFR-VERIFY: Recomposition And Closure

## Objective

Verify the completed source and receipts against SPEC, architecture, layers,
public/private boundaries, and the accepted research claim ceiling.

## Smallest Working Unit Exemption

- Reason: closure-only verification task.
- Allowed because task ID contains `VERIFY`.
- No implementation source mutation is permitted.

## Inputs

- receipts for `SWU-IFR-001` through `SWU-IFR-007`;
- [TRACEABILITY.md](../shared/TRACEABILITY.md);
- public canonical and generated runtime diffs;
- isolated consumer proof.

## Checks

1. Every SPEC acceptance criterion maps to a passing durable receipt.
2. Every SWU touched only its declared write scope.
3. L0-L3 non-regression guarantees remain true.
4. Runtime manifests exclude consumer-owned state.
5. Legacy entries remain valid and unmoved.
6. No atomicity or currentness claim appears.
7. No private path/evidence appears in public Arcanum.
8. Canonical source, generated payload, tests, docs, and observability agree.
9. Existing canonical Inventory development package is reconciled rather than
   silently competing.

## Validation Surface

```sh
node --test arcanum/arcana/inventory/test/*.test.cjs
bash arcanum/arcana/inventory/scripts/validate-index-json.sh \
  arcanum/arcana/inventory/test/fixtures/installed-consumer/index.json
git diff --check -- arcanum/arcana/inventory \
  ops/development/2026-07-24-inventory-runtime-faceted-layout
```

## Output

One final audit receipt with `pass|flag|block`, exact evidence references,
residue, and next owner. Passing closure does not authorize release,
publication, or live consumer migration.

