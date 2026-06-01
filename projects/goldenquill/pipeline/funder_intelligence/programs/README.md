# programs/

One YAML per program × cycle pair. Filename = canonical `program_id` keyed by cycle (e.g., `USDA-RD-RBDG-FY26.yaml`, `USDA-AMS-VAPG-FY26.yaml`).

Each file is operator-Ed25519-signed and verified at load via the FID publisher pubkey at `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml`.

## What lives here

Program × cycle facts:

- NOFO / RFA / FOA identifier + URL + access date + SHA256 hash
- Eligibility rules (machine-parseable for Logician match-rule gates)
- Rubric weighted dimensions (scoring criteria + point allocations; cite source page/line)
- Required application elements (sections, attachments, certifications)
- Statutory cites (cite source page/line; ≤2-sentence verbatim quote)
- Compliance cascade pointers (`compliance_cascades/<framework_id>`)
- Reviewer-type pointers (`reviewer_heuristics/<type>` for this program's review process)
- Funder dialect notes specific to this program
- Post-award obligations (reporting cadence, beneficiary metrics, narrative shape)
- Endpoints + `live_check_url` for Scout VERIFY
- Refresh cadence per Depth Charter

## What does NOT live here

- Agency / foundation level facts (lives in `funders/<funder_id>.yaml`)
- Compliance framework detail (lives in `compliance_cascades/`)
- Reviewer-type patterns (lives in `reviewer_heuristics/`)

## Schema

`_schema/fid_program.schema.json` (lands at first artifact Pillar-3 closure).

## Phase 1 scope

Six programs (per planning doc §4.2):

- USDA-AMS-VAPG-FY26 (rubric already extracted at `pipeline/rubrics/vapg_fy26.json` — depth-reference)
- USDA-RD-RBDG-FY26 (operator soft-pick §11.6 first artifact)
- USDA-RD-RCDG-FY26
- USDA-NIFA-SARE-NE-FY26
- PA-DEPT-AG-AGINNOV-FY26
- USDA-RD-CFP-FY26 (Community Facilities)
