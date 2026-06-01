# compliance_cascades/

One YAML per cross-cutting compliance framework. Filename = canonical framework slug (e.g., `2-CFR-200-UG.yaml`, `DAVIS-BACON-PREVAILING-WAGE.yaml`, `SINGLE-AUDIT-A133.yaml`).

Each file is operator-Ed25519-signed and verified at load via the FID publisher pubkey at `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml`.

## What lives here

Compliance-framework facts that apply across multiple programs:

- Framework identifier + statutory cites (cite page/section)
- Trigger conditions (when does this cascade fire?)
- Mandatory gates (machine-parseable for Logician PRE-gate predicates)
- Failure modes (Red Team adversarial probe seeds)
- Audit + reporting obligations
- Cross-references to programs that invoke this cascade

## What does NOT live here

- Program × cycle detail (`programs/`)
- Case law interpretation (compliance-officer territory; out of scope per planning doc §3.2)
- Per-applicant compliance posture (lives in `orgs/<slug>/`)

## Schema

`_schema/fid_compliance_cascade.schema.json` (lands at first artifact Pillar-3 closure).

## Phase 1 scope

Three cascades (per planning doc §4.2):

- 2-CFR-200-UG (Uniform Guidance)
- DAVIS-BACON-PREVAILING-WAGE (touches Community Facilities)
- SINGLE-AUDIT-A133
