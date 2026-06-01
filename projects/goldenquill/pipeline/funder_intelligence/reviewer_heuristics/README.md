# reviewer_heuristics/

One YAML per reviewer type. Filename = canonical reviewer-type slug (e.g., `federal-program-officer.yaml`, `foundation-program-officer.yaml`, `peer-reviewer-academic.yaml`).

Each file is operator-Ed25519-signed and verified at load via the FID publisher pubkey at `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml`.

## What lives here

Per-reviewer-type patterns:

- Time budget per application (typical minutes per review)
- Top-10 reviewer heuristics (each with provenance: operator-verified interview OR documented public reviewer-debrief source; never fabricated per planning doc §2.2 `F-FID-REVIEWER-HEURISTIC-FABRICATION`)
- Common punishments (what triggers a low score; Red Team probe seeds)
- Common rewards (what lifts a score)
- Dialect cues this reviewer type responds to
- Capital stacking patterns this reviewer rewards or penalizes
- Denial-feedback distillation (from real debrief letters where available)
- Cross-references to programs that use this reviewer type

## What does NOT live here

- Individual reviewer-officer profiles (Tier-3 only; lives in `funders/<funder_id>.yaml` `funder_officer_relationship_notes`)
- Per-program scoring rubric (lives in `programs/<id>.yaml` `rubric`)

## Schema

`_schema/fid_reviewer_type.schema.json` (lands at first artifact Pillar-3 closure).

## Seed source

`skills/scribe-ghostwriter/references/reviewer_heuristics.md` (landed 2026-05-16) is the seed corpus for the per-type FID artifacts. Extends it; does not duplicate it. Skill stays as the how-to layer; FID stores the per-type structured data.

## Phase 1 scope

Four reviewer types (per planning doc §4.2):

- federal-program-officer (USDA-flavored)
- foundation-program-officer
- peer-reviewer-academic (SARE-flavored)
- state-program-officer (PA Dept of Ag)
