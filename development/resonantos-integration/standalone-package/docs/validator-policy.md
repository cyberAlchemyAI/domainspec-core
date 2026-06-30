# Validator Policy

## Policy

This package copies the public inventory schemas and validator scripts so a host collaborator can
run checks without reaching back into the private parent checkout.

## Copied Files

- `contracts/evidence-card.schema.yml`
- `contracts/evidence-set.schema.yml`
- `contracts/index.schema.yml`
- `tools/validate-evidence-card-slice.sh`
- `tools/validate-evidence-card-fixtures.sh`
- `tools/validate-index-json.sh`

## Validation Command

```bash
bash tools/validate-evidence-card-slice.sh fixtures/evidence-card
```

## Boundary

Passing these validators means the package fixtures conform to the expected contract shape. It does
not promote any candidate or prove the host-side trusted-write provider body.
