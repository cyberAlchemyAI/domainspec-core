---
title: §0.5 v31 — paired-commit amendment for §4 v2.x.7 (OD-C F-CARDS-COUPLING-VIOLATION-EXTENSION value-position extension)
filed: 2026-05-16
locked: 2026-05-17
operator: Josh
status: LOCKED — paired-commit with §4 v2.x.7 LOCK per §6.17 Option-B compound-commit pattern at 2026-05-17 OD-C ceremony. Self-LOCK per documentation-only carve-out (companion-paired with narrow-corrective predicate body graduation already covered by §4 v2.x.7 Thesis-equivalent backfill scan; predicate body is LIVE on disk). L-005 strict two-cycle Thesis NOT dispatched — operator authorized OD-C ceremony per parent handoff `pipeline/handoffs/od_c_completion_2026-05-16.md` (predicate body + tests + 14-card backfill scan landed pre-ceremony; one operator-decision surface FIX-IN-PLACE-resolved at ceremony time).
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_1_amendment.md       # §0.5 v16 LOCKED 2026-05-10 — rows 377-378; CANONICAL narrow-corrective + sub-tag-extension precedent
  - pipeline/blueprint/v0.1/section_00_5_section_18_card_amendment.md         # §0.5 v25 LOCKED 2026-05-15 — hosts row 562 `F-CARDS-COUPLING-VIOLATION-EXTENSION` failure-code primitive
  - pipeline/blueprint/v0.1/section_00_5_cards_wave_2_amendment.md            # §0.5 v29 LOCKED 2026-05-16 — Wave-2 signature_status unsigned→signed flip
  - pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_6_amendment.md       # §0.5 v28 LOCKED 2026-05-16 — most-recent §4-family paired-commit (router-dedup)
  - pipeline/blueprint/v0.1/section_00_5_section_18_11_v1_1_amendment.md      # §0.5 v30 LOCKED 2026-05-17 (row 271) — immediate predecessor; OD-D documentation-only paired-commit; runtime-live total 539
  - pipeline/blueprint/v0.1/section_04_v2_x_7_card_coupling_value_position_amendment.md  # §4 v2.x.7 (paired-commit sibling — this amendment)
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_04_v2_x_7_card_coupling_value_position_amendment.md  # paired-commit per §6.17 Option-B
compound_lock_with: section_04_v2_x_7_card_coupling_value_position_amendment.md
parent_wins_discipline: each row's parent_lock_version + parent_lock_commit_hash point at §4 v2.x.7; resolves to actual commit hash at LOCK ceremony.
row_delta: prior runtime-live total at §0.5 v30 LOCK 2026-05-17 = 539 rows (per lock_history row 271 `runtime_live_total_after`). **§0.5 v31 amendment claims 1 row (marker only): row 540.** Sub-tag set on row 562 extends in-place per §4 v2.x.1 row-198 precedent; NO new failure-code row. New runtime-live total at this LOCK = 540.
kind_of_amendment: row-append (marker only). NO new vocabulary kind — the marker row's `primitive_kind` resolves against the v5 + v6 closed vocabulary.
dependency_order: §4 v2.x.7 LOCK + this §0.5 amendment land as a single compound paired-commit at the same `lock_timestamp_utc` per §6.17 Option-B.
f_index_stale_preflight: F-INDEX-STALE PRE-gate fires at commit time; the 1 new row must be present in the index or the commit fails closed. Sub-tag set on row 562 is annotation-only (§B below); F-INDEX-STALE does not enumerate sub-tags.
cross_family_posture: Self-LOCK per parent-handoff carve-out. The §4 v2.x.7 narrow-corrective amendment is THESIS-EQUIVALENT-COVERED via (a) 36/36 PASS on `tests/logician/gates/test_f_cards_coupling_violation_extension.py`, (b) 1965 PASS + 7 environmental skips at `tests/logician/gates/` + `tests/cards/`, (c) 14-card backfill scan completed with the one FIX-IN-PLACE operator-decision surface resolved at ceremony time (sponsorship_corporate.yaml display-name swap; backfill re-run 14/14 PASS). Audit trail: `pipeline/handoffs/od_c_completion_2026-05-16.md` substitutes for formal L-005 Thesis row.
narrow_corrective_precedent: §4 v2.x.1 (rows 198/199; sub-tag-extension on row 301 owner) — same shape: corrective extension of an already-LOCKed predicate body via in-place module edit + paired-commit §0.5 marker row + no new top-level failure-code row.
---

# §0.5 v31 — paired-commit amendment for §4 v2.x.7 (OD-C value-position extension)

## §0. Amendment intent

This amendment lands paired with §4 v2.x.7 LOCK per §6.17 Option-B compound-commit pattern. §4 v2.x.7 is a **narrow-corrective amendment** graduating the F-CARDS-COUPLING-VIOLATION-EXTENSION predicate body (row 562) from `NotImplementedError` to LIVE three-layer scanning (field-name + value-position + matrix-structural), AND extending the sub-tag closure with four new value-position sub-tags. It mirrors the §4 v2.x.1 row-198 narrow-corrective + sub-tag-extension precedent byte-for-byte:

- Predicate body extension on an already-LOCKed failure code → in-place module edit (no new module file at this amendment).
- Sub-tag set extends in-place at row 562's narrative cell → in-place annotation; no new failure-code row.
- §0.5 paired-commit lands one marker row only (the amendment anchor) → no new failure-code row, no new enforcement-infrastructure row.

Because this amendment graduates an existing module's body rather than landing a NEW dedicated module, the §0.5 paired-commit lands **one row only** (the marker), not the two-row shape of §4 v2.x.1 which landed both a marker AND an enforcement-infrastructure row for the new `r_archivist_no_canonical_mutate.py` module. The module file `f_cards_coupling_violation_extension.py` already exists on disk per §0.5 v25 row 562's `defined_at` reference; this amendment extends it without adding a new on-disk binary.

The master `section_00_5_interface_index_locked.md` remains LOCKED v5 on-disk; this amendment file is runtime-live at compound LOCK with §4 v2.x.7. Future master re-author folds all v6-v31 amendment files into the master.

# §A. Row append (row 540)

All rows enter §0.5 at `stability_tier = "STABLE"` at compound v2.x.7 LOCK (no PARENT_UNLOCKED transit since §4 v2.x.7 LOCKs in the same compound transaction).

**Marker (row 540) — §4 v2.x.7 amendment anchor:**

| Row | primitive_id | defined_at | parent_lock_version | parent_lock_commit_hash | kind | seat_owner | stability_tier |
|---|---|---|---|---|---|---|---|
| 540 | `blueprint.amendment_anchor.s4_v2_x_7.v1` | `pipeline/blueprint/v0.1/section_04_v2_x_7_card_coupling_value_position_amendment.md` | §4 v2.x.7 | `<resolved_at_commit>` | marker | logician | STABLE |

**Row 540 description:** Amendment anchor for the §4 v2.x.7 narrow-corrective amendment closing the OD-C design-time CIC × CLC coupling vector. Graduates F-CARDS-COUPLING-VIOLATION-EXTENSION predicate body (row 562) from `NotImplementedError` to LIVE three-layer scan: top-level field-name registry against `FORBIDDEN_FIELD_REGISTRY[axis]` + recursive value-position regex over all string values + matrix-card structural rule (`binding_eligibility: true` / `status != "FORWARD_COMPAT_ONLY"`). Path-level allowlist exempts `_*` underscore-prefixed top-level subtrees + the three self-identifying canonical-ID paths (`card_id`, `tilth_cic_id`, `tilth_clc_id`). Sub-tag closure on row 562 extends with four new value-position sub-tags per §B below.

# §B. Row 562 sub-tag closure extension (annotation; not a row mutation)

Per §4 v2.x.1 row-198 sub-tag-extension precedent — in-place narrative annotation on existing rows under their original owners. **NOT** a new row, **NOT** re-parenting.

Row 562 (`F-CARDS-COUPLING-VIOLATION-EXTENSION`, §0.5 v25, parent §4 v2.x card-hardening §4.X.1.7) — sub-tag set extends with **4 NEW value-position sub-tags** + **3 GRADUATED-to-LIVE sub-tags** (the prior-spec'd field-name + two matrix sub-tags whose predicate body graduates from NotImplementedError at this amendment):

NEW value-position sub-tags (per §4 v2.x.7 §3):

- `.value_literal_cic_slug` — any string value (recursively, outside exempt subtrees) matches `TILTH-CIC-\d{2}`.
- `.value_literal_clc_slug` — any string value (recursively, outside exempt subtrees) matches `TILTH-CLC-\d{2}`.
- `.value_literal_capital_logic_phrase` — any string value (recursively, outside exempt subtrees) matches `[Cc]apital [Ll]ogic`.
- `.value_literal_customer_identity_phrase` — any string value (recursively, outside exempt subtrees) matches `[Cc]ustomer [Ii]dentity`.

GRADUATED-to-LIVE sub-tags (prior-spec'd at §4 v2.x §4.X.1.7; predicate body graduates from NotImplementedError to LIVE at this amendment):

- `.forbidden_field_name_for_axis` — top-level field name in `card_body.keys()` matches `FORBIDDEN_FIELD_REGISTRY[axis]`.
- `.matrix_binding_eligibility_true` — matrix card declares `binding_eligibility: true` pre-v1.x matrix-phase amendment.
- `.matrix_status_not_forward_compat_only` — matrix card omits `status: "FORWARD_COMPAT_ONLY"` pre-v1.x matrix-phase amendment.

Row 562 narrative sub-tag-closure count after this amendment: **7** total (4 NEW value-position + 3 GRADUATED).

Consumers of the §0.5 Index that resolve row 562's sub-tag set must consult both the §0.5 v25 amendment row 562 narrative AND the §4 v2.x.7 amendment text at §3 + the on-disk `_VALUE_POSITION_PATTERNS` constant in `pipeline/logician/gates/f_cards_coupling_violation_extension.py` for the canonical seven-sub-tag enumeration. Drift between the §B annotation here, the §4 v2.x.7 §3 table, and the on-disk module is itself a §0.5 v31 defect; the module file is canonical per §4 v2.x.7 §10 cross-reference.

# §C. Row delta + invariants

- Runtime-live total at §0.5 v30 LOCK 2026-05-17 = 539 rows (per lock_history row 271 `runtime_live_total_after`).
- This amendment adds 1 row (marker only).
- New runtime-live total at compound LOCK = 540 rows.
- Vocabulary preservation: the marker row's `primitive_kind` resolves against the v5 + v6 closed vocabulary (marker).
- F-INDEX-STALE PRE-gate fires at commit time; the 1 new row must be present in the index or the commit fails closed.

# §D. Sub-tag-extension precedent (extends §C of §0.5 v16)

§0.5 v16 (paired-commit with §4 v2.x.1) established the narrow-corrective + sub-tag-extension §0.5 paired-commit pattern (§C of that amendment). This amendment follows it AND adds a sub-pattern: **when the corrective amendment graduates an existing module's predicate body** (rather than introducing a NEW dedicated module file), the §0.5 paired-commit lands **one marker row only**, not the two-row marker + enforcement-infrastructure shape.

The distinction:

- §4 v2.x.1 paired §0.5 v16 → 2 rows (marker + enforcement-infrastructure for `r_archivist_no_canonical_mutate.py` NEW module).
- §4 v2.x.7 paired §0.5 v31 → 1 row (marker only; `f_cards_coupling_violation_extension.py` already exists at row 562's `defined_at` per §0.5 v25).

Future contributors picking the wrong shape risk:

- Spurious new enforcement-infrastructure row (would generate row-count divergence at F-INDEX-STALE PRE-gate if the module already exists at the row 562 owner).
- Missing marker row (the amendment-anchor convention requires one marker per amendment file per §6.17 Option-B).

The marker-only sub-pattern is correct when the predicate-body extension lands in an already-registered module owned by an existing failure-code row.

# §E. Cross-references

- §4 v2.x.7 LOCK: `pipeline/blueprint/v0.1/section_04_v2_x_7_card_coupling_value_position_amendment.md` (DRAFT 2026-05-16)
- Audit trail substitute (parent-handoff carve-out): `pipeline/handoffs/od_c_completion_2026-05-16.md`
- Lock history rows (2026-05-17 OD-C ceremony): §4 v2.x.7 LOCK = row 272; §0.5 v31 paired-commit LOCK = row 273
- Predecessor handoff (OD-C disposition packet): `pipeline/handoffs/od_c_coupling_violation_extension_2026-05-16.md`
- Predecessor surfacing (Wave 1 + Wave 2 review cycles): `pipeline/validation/cards_wave_2_thesis_2026-05-15/WAVE_2_CLOSE_SYNTHESIS.md` §CC-3 + Wave 1 food_systems Cycle 2 FIX-IN-PLACE record
- Parent F-CARDS-COUPLING-VIOLATION-EXTENSION primitive row: §0.5 v25 row 562 at `pipeline/blueprint/v0.1/section_00_5_section_18_card_amendment.md` line 109
- Narrow-corrective + sub-tag-extension precedent: §0.5 v16 paired-commit with §4 v2.x.1 at `pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_1_amendment.md`
- Body-graduation precedent (HORIZON→ACTIVE-AT-§14-v1-LOCK): §4 v2.x.3 §2 + §0.5 v23 paired-commit at `pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_3_amendment.md`
- Companion runtime code landed at this amendment: `pipeline/logician/gates/f_cards_coupling_violation_extension.py` (UPDATED — predicate body LIVE) + `tests/logician/gates/test_f_cards_coupling_violation_extension.py` (REPLACED — 36-test surface)
- Backfill scan tool (operator-runnable; pre-staged under outputs/ at draft time): `outputs/od_c_backfill_scan.py` — surfaces operator-decision FIX-IN-PLACE vs supersession-re-sign for any LOCKed-card hits. One hit recorded at LOCKed `sponsorship_corporate.yaml` (TILTH-CLC-07).
