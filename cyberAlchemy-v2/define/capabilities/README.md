# Define Shared Meaning Product Capability

Status: candidate instance
Owners: product meaning, Definition Pack shape, Define runtime, public Invoke
realization, and next-use suitability each follow the typed route in the Product
Capability record
Canonical definition: `CAV2-D67`
Shared schema: `cyberAlchemy-v2/capability/schemas/capability.schema.json`

This package is the first source-owned Product Capability instance validated by
the canonical Capability Ontology. It says what Define must make possible,
names its input and output contracts, applies one exact Context policy, maps a
candidate realization through public Invoke Define, and records the obligations
that later runtime evidence must test.

Machine-readable sources:

- `define-shared-meaning.product-capability.json`
- `contracts/define-shared-meaning.input-contract.json`
- `contracts/define-shared-meaning.definition-pack.output-contract.json`
- `contracts/define-shared-meaning.handled-registry.output-contract.json`
- `policies/define-shared-meaning.context-policy.json`
- `realizations/invoke-define.realization.json`
- `obligations/define-shared-meaning.obligations.json`
- `evidence/define-session-runtime/` — 23-row model coverage and a synthetic
  bidirectional OBL-011 evidence protocol

The package is intentionally not an adoption or conformance record. Public
Invoke Define is bound only as a source-described candidate partial
realization. Its implemented mode status does not prove this Product
Capability. Saved-session and question continuity across CLI and chat remains
a known product gap, not a failed conformance verdict.

The evidence subpackage separates model coverage from runtime proof. Its
synthetic fixtures validate only the expected evidence shape and five planted
failure modes. All 23 runtime evidence states remain `not_evaluable`; no
obligation status is changed.

Validate with:

```bash
python3 cyberAlchemy-v2/define/capabilities/scripts/validate.py
python3 cyberAlchemy-v2/define/capabilities/tests/test_negative_mutations.py
python3 cyberAlchemy-v2/define/capabilities/scripts/validate.py --write-receipt
```
