---
title: §0.5 v32 — paired-commit amendment for §18.6 v2 (OD-E CLC schema dual-track structural separation; Option A top-level track_a:/track_b: containers; marker-only sub-pattern)
filed: 2026-05-17
operator: Josh Inklovich
status: LOCKED 2026-05-17 — paired-commit with §18.6 v2 LOCK per §6.17 Option-B compound-commit pattern at 2026-05-17 OD-E ceremony. Self-LOCK per documentation-only-equivalent carve-out (companion-paired with schema-shape-extension amendment whose schema delta + 3 card restructures + 8/8 + 6/6 invariant tests landed pre-ceremony per OD-E dispatch + completion handoffs; operator selected PATH (a) minimal-stub for CLC-06 Track B at ceremony per operator-stated rationale on the credit-vs-grant axis asymmetry; FIVE-row compound LOCK fires at the same lock_timestamp_utc).
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_section_18_card_amendment.md         # §0.5 v25 LOCKED 2026-05-15 — hosts the `pipeline.cards._schema.card_clc` schema row that the §18.6 v2 extension lands under (per §18 v1.1 RT-02 precedent for item-shape extensions; same precedent extends to top-level-property extensions per operator-decision at this LOCK)
  - pipeline/blueprint/v0.1/section_00_5_section_18_v1_1_amendment.md         # §0.5 v26 LOCKED 2026-05-16 — narrow-corrective marker-only precedent (item-shape extension)
  - pipeline/blueprint/v0.1/section_00_5_apolitical_dialect_amendment.md      # §0.5 v28 LOCKED 2026-05-16T14:00:00Z (predecessor chain)
  - pipeline/blueprint/v0.1/section_00_5_cards_wave_2_amendment.md            # §0.5 v29 LOCKED 2026-05-16T16:00:00Z (Wave-2 signature_status unsigned→signed flip)
  - pipeline/blueprint/v0.1/section_00_5_section_18_11_v1_1_amendment.md      # §0.5 v30 LOCKED 2026-05-17T04:34:50Z row 271 (OD-D documentation-only marker-only paired-commit)
  - pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_7_amendment.md       # §0.5 v31 LOCKED 2026-05-17T05:30:00Z row 273 (OD-C marker-only paired-commit; immediate predecessor; runtime-live 540)
  - pipeline/blueprint/v0.1/section_18_6_v2_dual_track_amendment.md           # §18.6 v2 (paired-commit sibling — this amendment)
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_18_6_v2_dual_track_amendment.md  # paired-commit per §6.17 Option-B
companion_supersession_targets:
  - pipeline/cards/CLC/market_access.yaml          # Wave 2 LOCK row 258
  - pipeline/cards/CLC/credit_underwriting.yaml    # Wave 2 LOCK row 259
  - pipeline/cards/CLC/sponsorship_corporate.yaml  # Wave 2 LOCK row 260
compound_lock_with: section_18_6_v2_dual_track_amendment.md
parent_wins_discipline: the single row's parent_lock_version + parent_lock_commit_hash point at §18.6 v2; resolves to actual commit hash at LOCK ceremony.
row_delta: prior runtime-live total at §0.5 v31 LOCK 2026-05-17T05:30:00Z = 540 rows (per lock_history row 273 `runtime_live_total_after`). **§0.5 v32 amendment claims 1 row (marker only): row 541.** Schema extension on the `pipeline.cards._schema.card_clc` row 542 owner from §0.5 v25 extends in-place per §18 v1.1 RT-02 + §0.5 v26 narrow-corrective + schema-item-shape-extension precedent; NO new schema row. NO new failure-code row. NO new AST-lint row. NO new vocabulary kind. New runtime-live total at this LOCK = 541.
kind_of_amendment: row-append (marker only). NO new vocabulary kind — the marker row's `primitive_kind` resolves against the v5 + v6 + v17-v19 closed vocabulary.
dependency_order: §18.6 v2 LOCK + this §0.5 amendment + 3 × card_cartridge_supersession rows land as a single compound paired-commit at the same `lock_timestamp_utc` per §6.17 Option-B. FIVE rows total.
f_index_stale_preflight: F-INDEX-STALE PRE-gate fires at commit time; the 1 new marker row must be present in the index or the commit fails closed. The 3 supersession rows are NOT §0.5 index entries (they are card_cartridge_supersession rows, not primitive_id markers); F-INDEX-STALE does not enumerate supersession rows.
cross_family_posture: Self-LOCK per documentation-only-equivalent carve-out (companion to §18.6 v2 which is schema-shape-extension; the §0.5 paired-commit itself is marker-only; mirrors §0.5 v26 + v30 + v31 marker-only precedent). §18.6 v2 dispatch + completion handoffs document the schema delta + 3 card restructures + 8/8 + 6/6 invariant tests PASS in the Cowork session sandbox; per OD-E completion §INTERPRETER NOTE, .venv-pinned schema validation runs again at the operator's Mac post-ceremony for interpreter-pin compliance. L-005 strict two-cycle cross-family Thesis NOT dispatched per operator authorization mirroring OD-D self-LOCK precedent (zero new runtime enforcement teeth at the §0.5 paired-commit layer; schema-shape extension lands at the companion §18.6 v2 amendment which carries its own Thesis-equivalent evidence via the pre-LOCK test suite + the per-card backfill scan that landed via OD-C row 272 LOCK 2026-05-17T05:30:00Z).
narrow_corrective_precedent: §0.5 v26 (§18 v1.1 paired-commit, marker-only, schema-item-shape-extension under §0.5 v25 row 542 owner) — the schema-extension-under-existing-row precedent. §0.5 v30 (§18.11 v1.1 documentation-only paired-commit, marker-only) — the narrowest variant. §0.5 v31 (§4 v2.x.7 narrow-corrective paired-commit, marker-only sub-pattern when predicate body extends in an already-registered module) — the immediate predecessor. THIS v32 extends the precedent further: schema-shape extension at the TOP level (new optional top-level properties `track_a` + `track_b` + new $defs.track_container) rather than item-shape extension inside an existing array property. Per operator-decision at this LOCK, the same precedent applies — schema extensions of any depth (item-level OR top-level) land under the existing `pipeline.cards._schema.card_clc` schema row owner, not as a new schema row.
od_e_dispatch: pipeline/handoffs/od_e_dual_track_structural_separation_2026-05-16.md
od_e_completion: pipeline/handoffs/od_e_completion_2026-05-16.md
od_e_ceremony_handoff: pipeline/handoffs/od_e_paired_commit_lock_ceremony_2026-05-16.md
---

# Amendment intent

This amendment lands paired with §18.6 v2 LOCK per §6.17 Option-B compound-commit pattern. §18.6 v2 is a **schema-shape-extension amendment** (Option A — top-level `track_a:` / `track_b:` containers on multi-track CLC cards) introducing optional top-level multi-track container properties + a new `$defs.track_container` definition + a top-level `oneOf` with mutually-exclusive single-track / multi-track branches.

The amendment mirrors the §18 v1.1 + §0.5 v26 + §18.11 v1.1 + §0.5 v30 + §4 v2.x.7 + §0.5 v31 narrow-corrective + paired-commit precedent chain. The schema-shape extension at §18.6 v2 lands under the existing `pipeline.cards._schema.card_clc` schema row owner from §0.5 v25 — extending the schema's contract surface without modifying the §0.5 v25 row text in-place — per the §18 v1.1 RT-02 precedent for item-shape extensions, applied here at top-level shape extensions per operator-decision at this LOCK. The §18.6 v2 extension is **backward-compatible**: all eight existing CLC cards validate unchanged under the v2 schema (single-track branch matches); the validation outcome flips only when individual cards are restructured into the Option A multi-track shape.

Three of eight CLC cards (CLC-05 market_access, CLC-06 credit_underwriting, CLC-07 sponsorship_corporate) have been restructured into the Option A multi-track shape per OD-E dispatch 2026-05-16. The compound LOCK ceremony at this paired-commit fires FIVE rows at the same `lock_timestamp_utc`:

1. **blueprint** — §18.6 v2 amendment LOCK (lock_class: blueprint; companion_lock_with this §0.5 amendment + 3 supersession rows).
2. **blueprint-interface-index** — this §0.5 v32 paired-commit (lock_class: blueprint-interface-index; marker-only sub-pattern; ONE marker row only — `blueprint.amendment_anchor.s18_6_v2.v1`).
3. **card_cartridge_supersession** — market_access.yaml supersession-re-sign (parent_lock_row 258, Wave 2 LOCK 2026-05-16T16:00:00Z).
4. **card_cartridge_supersession** — credit_underwriting.yaml supersession-re-sign (parent_lock_row 259, Wave 2 LOCK 2026-05-16T16:00:00Z; operator selected PATH (a) minimal-stub for Track B per operator-stated rationale on the credit-vs-grant axis asymmetry — see ceremony summary).
5. **card_cartridge_supersession** — sponsorship_corporate.yaml supersession-re-sign (parent_lock_row 260, Wave 2 LOCK 2026-05-16T16:00:00Z).

Because the §18.6 v2 amendment lands under the existing §0.5 v25 `pipeline.cards._schema.card_clc` schema row owner (extension, not new row), this §0.5 paired-commit lands **one marker row only**: a §18.6 v2 amendment-anchor marker. The amendment-anchor namespace mirrors §0.5 v31's `blueprint.amendment_anchor.s4_v2_x_7.v1` form, indicating a schema-shape-extension amendment anchor under an existing schema row owner. The 3 supersession rows are NOT §0.5 index entries — they are card_cartridge_supersession rows in `pipeline/engineering/lock_history.v1.jsonl` per the §17 v1 / Wave 2 / OD-A / OD-D / OD-C strong-trust posture (signature_target_pubkey + publisher_pubkey_ed25519_hex + canonical_json_sha3_512 + ed25519_signature + per-file sha3_512).

The master `section_00_5_interface_index_locked.md` remains LOCKED v5 on-disk; this amendment file is runtime-live at compound LOCK with §18.6 v2. Future master re-author folds all v6-v32 amendment files into the master.

# §A — Row append (row 541)

The row enters §0.5 at `stability_tier = "STABLE"` at compound v2 LOCK (no PARENT_UNLOCKED transit since §18.6 v2 LOCKs in the same compound transaction).

**Marker (single row) — §18.6 v2 amendment anchor:**

| Row | primitive_id | defined_at | parent_lock_version | parent_lock_commit_hash | kind | seat_owner | stability_tier |
|---|---|---|---|---|---|---|---|
| 541 | `blueprint.amendment_anchor.s18_6_v2.v1` | `pipeline/blueprint/v0.1/section_18_6_v2_dual_track_amendment.md` | §18.6 v2 | `<resolved_at_commit>` | marker | cards | STABLE |

**Row 541 description:** Amendment anchor for the §18.6 v2 schema-shape-extension amendment landing the Option A top-level `track_a:` / `track_b:` containers on multi-track CLC cards. Schema delta lands on `pipeline/cards/_schema/card_clc.schema.json` (under existing §0.5 v25 row 542 owner — no new schema row); three CLC cards (CLC-05/06/07) restructure into the Option A multi-track shape; three card_cartridge_supersession rows in `pipeline/engineering/lock_history.v1.jsonl` re-sign the post-restructure canonical bytes against the cards-publisher Ed25519 key per the same trust posture as Wave 2 / OD-A / OD-D / OD-C ceremonies. Five existing single-track CLC cards (CLC-01/02/03/04/08) UNCHANGED at this amendment. Operator selected PATH (a) minimal-stub for CLC-06 Track B at this ceremony per operator-stated rationale on the credit-vs-grant axis asymmetry (credit underwriting is fundamentally a debt-side concept; grants do not have an analog underwriting process; the Track B asymmetry is GENUINE, not a content gap; v0.2 Wave 3 handback filed for substantive grant-track expansion when a real CDFI Fund / USDA RD grant cycle arrives at runtime).

The `seat_owner: cards` value mirrors §0.5 v25 cards.cic.* + cards.clc.* + cards.matrix.* rows + §0.5 v26 §18 v1.1 marker row + §0.5 v29 Wave 2 signature_status flips + §0.5 v30 §18.11 v1.1 section-anchor marker row. The §0.5 v31 marker row carried `seat_owner: logician` because its parent was a logician-family predicate-body graduation (§4 v2.x.7); this v32 marker carries `seat_owner: cards` because its parent is a cards-family schema-shape extension (§18.6 v2).

# §B — Row delta + invariants

- Runtime-live total at §0.5 v31 LOCK 2026-05-17T05:30:00Z = 540 rows (per lock_history row 273 `runtime_live_total_after`).
- This amendment adds 1 row (1 marker; no enforcement-infrastructure; no schema; no failure-code; no ast-lint; no card-namespace; no vocabulary kind).
- New runtime-live total at compound LOCK = 541 rows.
- Vocabulary preservation: the marker row's `primitive_kind` resolves against the v5 + v6 + v17-v19 closed vocabulary (`marker`).
- Seat_owner preservation: the row carries `seat_owner: cards` per §0.5 v20 RT-19/RT-C2-09 invariant (mirrors §0.5 v25 + v26 + v29 + v30 cards-family ownership).
- F-INDEX-STALE PRE-gate fires at commit time; the new marker row must be present in the index or the commit fails closed.
- F-CARDS-COUPLING-VIOLATION-EXTENSION PRE-gate fires on each restructured card pre-supersession-sign per the OD-C row 272 LOCK 2026-05-17T05:30:00Z three-layer scan (field-name registry + recursive value-position regex + matrix-card structural rule). All three restructured cards must clear the scan; if any card fails, the operator FIX-IN-PLACE-resolves at ceremony time mirroring OD-C sponsorship_corporate.yaml resolution (display-name swap for canonical slugs in value positions).

# §C — Schema-shape-extension precedent (extends §18 v1.1 RT-02 + §0.5 v26 narrow-corrective + schema-item-shape-extension precedent)

§18 v1.1 + §0.5 v26 paired-commit (LOCKED 2026-05-16 row 565) established the **schema-extension-under-existing-row precedent**: an amendment that refines a LOCKed schema's item shape (inner-property additions to existing top-level schema fields) lands under the existing `pipeline.cards._schema.card_clc` schema row owner from §0.5 v25, not as a new schema row. The §0.5 paired-commit lands ONE marker row only.

This v32 amendment EXTENDS the precedent further: schema-shape extension at the TOP level (new optional top-level properties `track_a` + `track_b` + new `$defs.track_container` + new top-level `oneOf` branch) rather than at item level inside an existing array property. Per operator-decision at this LOCK, the same precedent applies — schema extensions of any depth land under the existing schema row owner.

The distinction:

- **§18 v1.1 + §0.5 v26** — item-shape extension on existing array property (`common_funders_observed[].*`, `provenance_requirements[*].*`). One marker row only.
- **§18.6 v2 + §0.5 v32 (this amendment)** — top-level shape extension (new optional top-level `track_a` + `track_b` properties + new `$defs.track_container` + new top-level `oneOf` branch). One marker row only.

Both stay under the existing `pipeline.cards._schema.card_clc` schema row owner from §0.5 v25. Both land via the same compound paired-commit pattern per §6.17 Option-B. Both carry the marker-only sub-pattern per §0.5 v31 §D (when the corrective amendment extends an existing module's contract surface rather than introducing a NEW dedicated module file or schema row, the §0.5 paired-commit lands one marker row only).

The schema-extension precedent now spans three variants:

1. Item-shape extension (§18 v1.1 / §0.5 v26) — adds properties inside existing array/object items.
2. Top-level shape extension (§18.6 v2 / §0.5 v32, this amendment) — adds new top-level properties + new $defs + new oneOf branch.
3. Predicate-body graduation (§4 v2.x.7 / §0.5 v31) — graduates an existing module's predicate body from NotImplementedError to LIVE, extending sub-tag closure in-place.

Future contributors picking the wrong shape risk:

- Spurious new schema row (would generate row-count divergence at F-INDEX-STALE PRE-gate; the schema row 542 already exists at §0.5 v25 and owns the extension).
- Missing marker row (the amendment-anchor convention requires one marker per amendment file per §6.17 Option-B).
- Spurious supersession row count (one supersession row per restructured card; this amendment lands THREE supersession rows because THREE cards restructure; future amendments restructuring fewer/more cards land fewer/more supersession rows).

The marker-only-plus-N-supersession sub-pattern is correct when the schema-shape extension at the parent amendment requires re-signing N previously-LOCKed cards whose canonical bytes change at restructure.

# §D — Card supersession discipline (per §18.6 v2 §3 + OD-1 path (b) / vocab-scrub-precedent)

Three Wave 2 LOCK ceremony rows (258 market_access, 259 credit_underwriting, 260 sponsorship_corporate) require supersession-re-sign per OD-1 path (b) / vocab-scrub-precedent (lock_history rows 238-249, 2026-05-16T14:30:00Z). Each supersession row records:

- `parent_lock_row`: the Wave 2 ceremony row being superseded (258 / 259 / 260).
- `ceremony_parent_row`: the §18.6 v2 amendment's LOCK row (member 1 of the compound 5).
- `module`: the card slug.
- `amendment_file`: the card YAML path.
- `post_restructure_canonical_bytes_sha3_512_hex`: SHA3-512 over the post-restructure canonical-YAML bytes minus the embedded ed25519_signature field.
- `post_restructure_publisher_signature_ed25519_hex`: Ed25519 signature over the post-restructure canonical-JSON bytes (excluding the ed25519_signature + canonical_json_sha3_512 fields themselves; same shape as Wave 2 / OD-A / OD-D / OD-C strong-trust posture).
- `publisher_pubkey_ed25519_hex`: pinned cards-publisher pubkey `0b1a0bbfa5ee9149af2c4e6153ed037dd03c0d562c94d3eaefeaf798e6f375bd`.
- `post_restructure_file_size_bytes`: on-disk file size post-restructure.
- `verified_against_pinned_pubkey`: true (verified at ceremony post-sign round-trip).

The card's embedded ed25519_signature from Wave 2 LOCK becomes SUPERSEDED by the new sig recorded in the supersession row. The card's embedded sig is NOT re-issued at this ceremony — per the OD-C row 272 ceremony precedent (sponsorship_corporate.yaml fix-in-place left the embedded sig stale; loader-time re-validation deferred to v0.2 first-wave). The supersession row is the authoritative new sig until v0.2 first-wave loader graduation folds the embedded re-sign.

Historical Wave 2 LOCK rows 258/259/260 are preserved verbatim in `pipeline/engineering/lock_history.v1.jsonl`; the supersession rows append after the current tail (expected rows 276/277/278 after compound LOCK fires per the 5-row composition above).

# §E — Operator dispatch posture

Per the documentation-only-equivalent carve-out (no runtime enforcement teeth at the §0.5 paired-commit layer; schema-shape extension lands at the companion §18.6 v2 amendment which carries its own Thesis-equivalent evidence via the pre-LOCK test suite + the per-card backfill scan that landed via OD-C row 272 LOCK 2026-05-17T05:30:00Z), operator MAY elect:

1. **Self-LOCK** — operator confirms (a) §18.6 v2 schema delta is correct (8/8 + 6/6 invariant tests PASS); (b) three card restructures landed cleanly (per OD-E completion handoff); (c) operator-decision on CLC-06 Track B path (a) vs (b) — operator selected PATH (a) minimal-stub per operator-stated rationale on the credit-vs-grant axis asymmetry; (d) cards-publisher pubkey pinned at `vault_shared/cards/publisher_pubkey.signed.yaml` matches `0b1a0bbfa5ee9149af2c4e6153ed037dd03c0d562c94d3eaefeaf798e6f375bd`. LOCK fires immediately at the same `lock_timestamp_utc` as this §0.5 v32 paired-commit; audit trail at `pipeline/handoffs/od_e_completion_2026-05-16.md` + `pipeline/handoffs/od_e_paired_commit_lock_ceremony_2026-05-16.md` substitute for the formal L-005 Thesis audit row.

2. **L-005 strict two-cycle Thesis with FULL live cross-family rigor** — Editor + Judge + Red Team via the `mcp__Control_your_Mac__osascript` → `openclaw infer model run --gateway` bridge per AGENTS.md cross-family-review discipline; model dispatch on `pipeline/validation/section_18_v1_2_thesis_2026-05-16/dispatch_seat.sh` template; audit trail at `pipeline/validation/section_18_6_v2_thesis_<date>/` if elected. Cycle 1 + Cycle 2 verification per L-005.

OD-E was authorized self-LOCK by operator per parent ceremony dispatch 2026-05-17.

# §G — Domain rationale (operator 2026-05-17 directive folded at ceremony before signing)

Operator directive 2026-05-17 at this LOCK ceremony (verbatim, paraphrased into precedent text): grant logic and credit underwriting logic are objectively different mechanisms even though both are financial-access tools for clients. The real-world use case that exposes the distinction is **stacked funding** — a single applicant assembling a deal from multiple instruments simultaneously (e.g., VAPG grant + low-interest farm loan + PA tourism grant + PA small business loan + PA small business advantage grant), where each instrument carries its own matching logic and Tilth must route each to its own CLC at runtime. Conflating grant-side capital and credit underwriting into Track A / Track B of one CLC was therefore a category error, not a substance gap — credit underwriting evaluates repayment capacity / collateral / debt-service coverage on a return-stream basis, while grant matching evaluates mission-fit / capacity / outcomes / public benefit on an allocation basis, and the two mechanisms do not share scoring axes, evidence schemas, reviewer profiles, or commitment-tracking shapes. The operator-selected PATH (a) minimal-stub for CLC-06 Track B at this ceremony therefore documents a GENUINE asymmetry rather than papering over a content gap — and the v0.2 Wave 3 handback filed at this LOCK directs the card-research successor to plan a **separate CLC slug** (provisional name: `grant_side_credit_readiness` or `capital_readiness_grant`; final naming pending Wave 3 dispatch) for grant-side capital matching rather than expanding Track B of credit_underwriting. The lesson is a candidate for `/lessons.md` (L-024 placeholder, post-OD-E close, separate dispatch): "Don't conflate grant logic with credit underwriting logic; stacked funding stacks separate mechanisms — each instrument deserves its own CLC at runtime, not Track A / Track B of one CLC."

# §F — Cross-references

- §18.6 v2 amendment (companion blueprint amendment; LOCKs atomically with this §0.5 amendment): `pipeline/blueprint/v0.1/section_18_6_v2_dual_track_amendment.md`
- §18.6 v2 schema delta: `pipeline/cards/_schema/card_clc.schema.json` (top-level `track_a` + `track_b` optional properties + `$defs.track_container` + top-level `oneOf` with mutually-exclusive single-track / multi-track branches)
- Three restructured CLC cards:
  - `pipeline/cards/CLC/market_access.yaml` (CLC-05 — track_a: sbir_phase_ii / track_b: sbir_phase_iii)
  - `pipeline/cards/CLC/credit_underwriting.yaml` (CLC-06 — track_a: debt / track_b: grant — PATH (a) minimal-stub accepted at ceremony per operator-stated rationale on credit-vs-grant axis asymmetry)
  - `pipeline/cards/CLC/sponsorship_corporate.yaml` (CLC-07 — track_a: benefits_exchange / track_b: corp_foundation_grant)
- Pre-restructure backups: `pipeline/validation/od_e_dual_track_2026-05-16/backup/{market_access,credit_underwriting,sponsorship_corporate}_pre_restructure.yaml`
- OD-E dispatch handoff: `pipeline/handoffs/od_e_dual_track_structural_separation_2026-05-16.md`
- OD-E completion hand-back: `pipeline/handoffs/od_e_completion_2026-05-16.md`
- OD-E ceremony pre-staging handoff: `pipeline/handoffs/od_e_paired_commit_lock_ceremony_2026-05-16.md`
- Parent §0.5 v31 LOCK: `pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_7_amendment.md` (OD-C marker-only paired-commit, lock_history row 273, 2026-05-17T05:30:00Z)
- Predecessor chain: §0.5 v30 (`section_00_5_section_18_11_v1_1_amendment.md`, OD-D documentation-only, row 271, 2026-05-17T04:34:50Z) + §0.5 v29 (`section_00_5_cards_wave_2_amendment.md`, Wave 2 signature_status flip, row 262, 2026-05-16T16:00:00Z) + §0.5 v28 (apolitical_dialect compound, 2026-05-16T14:00:00Z) + §0.5 v27 (CC-007 §4 v2.x.5 paired-commit, row 233, 2026-05-16T08:00:00Z) + §0.5 v26 (§18 v1.1 paired-commit, row 565, 2026-05-16) + §0.5 v25 (Wave 1 cards paired-commit, runtime-live 564).
- Schema-extension-under-existing-row precedent: §18 v1.1 + §0.5 v26 paired-commit (LOCKED 2026-05-16 row 565) — item-shape extension under §0.5 v25 row 542 owner.
- Documentation-only narrow-corrective precedent (marker-only, narrowest): §18.11 v1.1 + §0.5 v30 paired-commit (LOCKED 2026-05-17 row 271).
- Marker-only sub-pattern precedent (predicate-body graduation under existing module): §4 v2.x.7 + §0.5 v31 paired-commit (LOCKED 2026-05-17 row 273).
- Vocab-scrub supersession-re-sign precedent: lock_history rows 238-249 (2026-05-16T14:30:00Z) — per-amendment-supersession-member pattern; OD-E this ceremony adds per-amendment-supersession-member-1-of-3 / 2-of-3 / 3-of-3 rows mirroring the same shape with `card_cartridge_supersession` lock_class.
- OD-C backfill scan precedent for value-position regex compliance: lock_history row 272 LOCK 2026-05-17T05:30:00Z + `outputs/od_c_backfill_scan.py` — surfaces operator-decision FIX-IN-PLACE vs supersession-re-sign for any LOCKed-card hits on the F-CARDS-COUPLING-VIOLATION-EXTENSION regex set.
- Five Operating Laws + Four Autonomy Rules: `/SOUL.md` (canonical) + `pipeline/SESSION_BOOTSTRAP.md` (summary).
