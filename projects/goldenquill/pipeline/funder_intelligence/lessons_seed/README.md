# lessons_seed/

Pre-Archivist lessons-memory seed. Bridge mechanism for v0.1 horizon until Archivist v1.x formalizes Lessons Memory.

## What lives here

Per-cycle lessons emitted from grant cycles:

- `<cycle_id>.yaml` — one file per closed grant cycle.

Each entry pairs with a `CycleReceipt` per §17 v1 WPFA (`orgs/<slug>/vault/operational/cycle_receipts/<cycle_id>.json`) but is FID-targeted: lessons that should update a FID artifact rather than a per-org file.

## Fields per entry (forward-spec)

- `cycle_id` — matches WPFA CycleReceipt `cycle_id`
- `closed_at` — UTC timestamp
- `lessons_emitted[]`:
  - `fid_target` — `funders/<id>` | `programs/<id>` | `compliance_cascades/<id>` | `reviewer_heuristics/<type>`
  - `kind` — `update_existing_fact` | `add_new_fact` | `flag_stale` | `flag_drift`
  - `proposed_change` — verbatim text of proposed amendment
  - `corpus_ref` — provenance pointer (real RFA / award / debrief letter / interview)
  - `operator_approval_required` — `true` (default — Archivist consumes; operator approves)

## Bridge → Archivist v1.x

When Archivist v1.x lands (§15 v2.x already SPEC-LOCKED), seed migrates to Archivist's canonical store. Bridge mechanism mirrors Reflection Packet v0.1-hook → v0.2-first-wave dormant→live transition (§16 v1 → v1.1 LOCK precedent).

## Anti-drift discipline

- No FID artifact gets updated from a lessons_seed entry without operator-Ed25519 sign-off.
- Re-signed FID artifact re-runs field-test (Track C synthetic panel; cheaper than Track A/B).
- Stale-detection PRE-gate `F-FID-STALE-RUBRIC` flags rubrics > 18 months old AND annually-cycled program.
