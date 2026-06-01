# _schema/

JSON Schema files for FID artifact families. Each schema lands at the first Pillar-3 closure for that family (not Phase-1 day-0 work).

Files (forward-declared per planning doc §2):

- `fid_funder.schema.json` — funder-level facts
- `fid_program.schema.json` — program × cycle facts
- `fid_compliance_cascade.schema.json` — compliance-framework facts
- `fid_reviewer_type.schema.json` — per-reviewer-type patterns
- `fid_capital_raise.schema.json` — capital-raise instruments (Reg CF / Reg A+ / Reg D 506(c)); added 2026-05-19 per operator P0 #3 resolution. Closed-set `platform` enum seeded with Republic / SeedInvest / StartEngine / Wefunder. Closed-set `instrument_type` enum: `reg_cf` / `reg_a_plus` / `reg_d_506c`. Required provenance: SEC EDGAR Form C/1-A/D filing pointer per Law 1.

## Schema discipline

Mirrors Cards (`pipeline/cards/_schema/`) byte-for-byte where overlap exists:

- Closed-set enums for any field that has a finite vocabulary.
- Item-shape validators (no array-element drift).
- Operator-Ed25519-signature field with `ed25519_signature` key excluded from canonical-JSON-bytes computation.
- Lifecycle field (`lifecycle.draft_status`: `draft → audited → field_tested → validated`).
- Provenance fields on every fact: `corpus_ref` + `verbatim_quote` (≤2 sentences).

## Validator runtime

JSON-Schema-2020-12 against the YAML loader's parsed dict at load time. Fail-closed loader raises `F-FID-SCHEMA-INVALID` (forward-declared; binds to `F-FID-*` family at first §4 v2.x.z follow-on amendment).
