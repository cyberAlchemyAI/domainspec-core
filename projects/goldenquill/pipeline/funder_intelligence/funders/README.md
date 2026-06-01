# funders/

One YAML per funder entity (agency / foundation / intermediary). Filename = canonical `funder_id` (e.g., `USDA-RD.yaml`, `HEINZ-FOUNDATION.yaml`).

Each file is operator-Ed25519-signed and verified at load via the FID publisher pubkey at `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml`.

## What lives here

Funder-level facts that span programs:

- Mission + civic-benefit framing
- Funder political dialect (per architecture v7.0.12 CLC-keyed register state — NOT the retired four-axis political enum)
- Funder-officer relationship notes (Tier-2 / Tier-3 only)
- Program roster (pointers into `programs/`)
- Compliance cascade defaults (pointers into `compliance_cascades/`)
- Historical award patterns (aggregate; per-program detail lives in `programs/`)
- Refresh cadence per Depth Charter

## What does NOT live here

- Program × cycle detail (lives in `programs/<program_id>.yaml`)
- Compliance framework detail (lives in `compliance_cascades/`)
- Reviewer-type patterns (lives in `reviewer_heuristics/`)
- Per-client / per-applicant content (lives in `orgs/<slug>/`)

## Schema

`_schema/fid_funder.schema.json` (lands at first artifact Pillar-3 closure).

## Phase 1 scope

Eight funders (per planning doc §4.2):

- USDA-RD
- USDA-NIFA
- USDA-AMS
- PA-DEPT-AG
- PA-DCED
- HEINZ-FOUNDATION
- NCBA-CLUSA
- ONE additional state foundation (operator picks at Pillar 1)
