---
title: §0.5 Blueprint Interface Index — Cards Wave 1 paired-commit amendment (v25 — companion to TILTH-CIC-01 Food Systems + TILTH-CLC-03 Operating Capacity LOCKs 2026-05-15 PM)
filed: 2026-05-15
operator: Josh
status: paired-commit companion to the first card-class LOCK ceremony (lock_history rows 226 + 227). v25 in the §0.5 sequence. NO new vocabulary kind; this amendment introduces the **`card`** primitive_kind at v25, sanctioned as a closed-set extension to the v5/v6/v19 vocabulary (marker / schema / interface-contract / failure-code / ast-lint) per §0.5 v19 §B `ast-lint` precedent. Two new rows per card (one marker + one card) = four rows total; rows 534-537.
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md                                 # §0.5 v5 LOCKED 2026-04-19 — 101 master rows (vocabulary baseline: marker / schema / interface-contract / failure-code)
  - pipeline/blueprint/v0.1/section_00_5_section_17_wpfa_amendment.md                              # §0.5 v19 LOCKED 2026-05-11 — `ast-lint` vocabulary kind precedent for closed-set extension
  - pipeline/blueprint/v0.1/section_00_5_section_funding_goal_amendment.md                         # §0.5 v20 LOCKED 2026-05-11 — `seat_owner` row attribute extension precedent (RT-19 closure)
  - pipeline/blueprint/v0.1/section_00_5_section_16_v1_1_amendment.md                              # §0.5 v24 LOCKED 2026-05-15 (rows 509-533 from Reflection Packet v0.2 first wave compound quintuple)
  - pipeline/blueprint/v0.1/section_18_card_system.md                                    # §18 v1 DRAFT — card system specification authority
  - pipeline/cards/CIC/food_systems.yaml                                                           # TILTH-CIC-01 card — LOCKED 2026-05-15 PM (lock_history row 226)
  - pipeline/cards/CLC/operating_capacity.yaml                                                     # TILTH-CLC-03 card — LOCKED 2026-05-15 PM (lock_history row 227)
companion_artifacts_pinned_at_LOCK:
  - vault_shared/cards/publisher_pubkey.signed.yaml                                                # operator publisher pubkey, generated + self-signed at LOCK ceremony 2026-05-15 PM; mirrors v7.0.7 §6.1 router-template publisher pubkey trust mechanism byte-for-byte
row_delta: prior runtime-live total = 533 rows (after §0.5 v24 §16 packet v0.2 first wave LOCK at row 533). **§0.5 v25 amendment claims rows 534-537 (4 rows: 2 markers + 2 card).** Every row carries `seat_owner: "cards_loader"` per RT-19 extension landed at §0.5 v20. New runtime-live total at this LOCK = 537.
kind_of_amendment: row-append (2 markers + 2 card rows) + vocabulary extension (one new closed-set kind `card` per §0.5 v19 §B closed-set-extension precedent). No new schema / interface-contract / failure-code row at this amendment — F-CARDS-* family already registered at the §4 v2.x card-hardening amendment that ships with §18 v1 + architecture v7.0.11 (DRAFT cluster pending L-005 round; this LOCK amendment registers the **artifact-level** LOCK of the first two CIC + CLC cards, not the F-CARDS-* failure-code family itself).
numbering_note: §0.5 v25. Numbering is contiguous after §0.5 v24 (Reflection Packet v0.2 first wave compound quintuple at rows 509-533). Skipping v25 to v26 is NOT in scope at this LOCK.
seat_owner_attribute: every row in this amendment carries `seat_owner: "cards_loader"` per RT-19 extension. F-INDEX-STALE PRE-gate verifies seat_owner consistency at compound commit.
immutable_kind_attribute: every `card` row carries `immutable_kind: true` per RT-C2-04 closure landed at §0.5 v23 row 507. Any future amendment attempting to change a row's kind from `card` to another kind MUST be REJECTED at F-INDEX-STALE PRE-gate with sub-tag `.immutable_kind_change_attempted`.
cross_family_posture: paired-commit companion to artifact-level LOCKs that ALREADY underwent L-005 strict two-cycle FULL LIVE CROSS-FAMILY rigor at the Wave 1 Thesis dispatch (audit trails at `pipeline/validation/cards_wave_1_thesis_2026-05-15/CIC/food_systems/` + `.../CLC/operating_capacity/`). This §0.5 paired-commit is the registry-and-row-allocation sweep authorized by those LOCKs.
---

# Amendment intent

The first two cards (TILTH-CIC-01 Food Systems + TILTH-CLC-03 Operating Capacity) LOCKED 2026-05-15 PM at lock_history rows 226 + 227 after L-005 strict two-cycle cross-family Thesis at `pipeline/validation/cards_wave_1_thesis_2026-05-15/`. This §0.5 paired-commit:

1. **Introduces** the `card` primitive_kind as a closed-set vocabulary extension (mirrors §0.5 v19 §B `ast-lint` extension pattern; sanctioned by §0.5 v5 vocabulary closure).
2. **Registers** the two newly-LOCKED cards at the Index as row 535 (CIC-01) + row 537 (CLC-03), each preceded by an amendment-anchor `marker` row at 534 / 536 respectively.
3. **Pins** the operator publisher pubkey signed-asset path (`vault_shared/cards/publisher_pubkey.signed.yaml`) at this amendment's `companion_artifacts_pinned_at_LOCK` block — the white-glove deployment manifest reads this block to determine the integrity-target for `F-CARDS-SIGNATURE-INVALID` resolution.

The F-CARDS-* failure-code family is NOT re-registered here — those primitives land at the paired §4 v2.x card-hardening amendment that ships with §18 v1 + architecture v7.0.11 (DRAFT cluster pending L-005 round per `project_card_system_v7_0_11_DRAFT.md`).

# Amendment §A — vocabulary extension (closed-set sanctioned at LOCK)

The v5/v6/v19 closed vocabulary is extended with one new kind:

- **`card`** — signed Ed25519 artifact representing one CIC, CLC, or matrix card. File location: `pipeline/cards/{CIC,CLC,matrix}/<slug>.yaml`. Lifecycle states: `draft → reviewed → thesis_passed → signed → loaded → deprecated`. Each row carries `card_id` + `card_axis` + `card_slug` + `signature_target_pubkey` + `canonical_json_sha3_512` + `ed25519_signature` attributes in addition to the §0.5 baseline row attributes (`primitive_id`, `defined_at`, `kind`, `seat_owner`, `stability_tier`).

Rationale for closed-set extension: F-CARDS-* family is its own orthogonal failure-code family per Path B naming reconciliation (F-CARDS-* / F-PACKET-* / F-WPFA-* / F-REPORT-* / F-FG-* / F-DATACOLLECTOR-* / F-ARCHIVIST-* / F-REFLECTION-* are eight orthogonal families). The artifact-level LOCK is its own kind; conflating with `failure-code` or `interface-contract` would break F-INDEX-STALE PRE-gate dispatch.

# Amendment §B — row append (rows 534-537)

All rows enter §0.5 at `stability_tier = "STABLE"` at the artifact-level LOCK ceremony 2026-05-15 PM (lock_history rows 226 + 227 are the parents). No PARENT_UNLOCKED transit (the parents are not blueprint amendments themselves; they are artifact LOCKs).

| Row | primitive_id | defined_at | kind | seat_owner | Description |
|---|---|---|---|---|---|
| 534 | `cards.amendment_anchor.cards_wave_1_paired_commit.v1` | `section_00_5_section_18_cards_wave_1_paired_commit_amendment.md#Amendment intent` | marker | cards_loader | Amendment anchor for the §0.5 v25 paired-commit. Indexes the §18 v1 + lock_history rows 226 + 227 dependency surface. |
| 535 | `cards.card.cic.food_systems.v1` | `pipeline/cards/CIC/food_systems.yaml` | card | cards_loader | TILTH-CIC-01 Food Systems Wave 1 card. LOCKED 2026-05-15 PM. Signature target: `vault_shared/cards/publisher_pubkey.signed.yaml` publisher_pubkey_ed25519_hex `0b1a0bbfa5ee9149af2c4e6153ed037dd03c0d562c94d3eaefeaf798e6f375bd`. Canonical-JSON SHA3-512: `3122c0f4db7ddabdd44312d24dd142233928015753a2c28c0187c7a46dfa1c6c86122d78eb0a12e633161ba1f748e290ac1e27c9e42ceba81fa2f61d3443228c`. Ed25519 signature: `1169374ac700d1db3513ca1b0e065a4e85a98c274238296dc70140dc52273c6daefe1d68a361fab34c030b8cabc1c14be68922e38caa78075d1f968756589e09`. lifecycle.signature_status: signed; lifecycle.runtime_load_status: loaded. immutable_kind: true. |
| 536 | `cards.amendment_anchor.cards_wave_1_clc_paired_commit.v1` | `section_00_5_section_18_cards_wave_1_paired_commit_amendment.md#Amendment §B` | marker | cards_loader | Amendment anchor for the TILTH-CLC-03 row append (companion to the CIC marker at row 534). |
| 537 | `cards.card.clc.operating_capacity.v1` | `pipeline/cards/CLC/operating_capacity.yaml` | card | cards_loader | TILTH-CLC-03 Operating Capacity Wave 1 card. LOCKED 2026-05-15 PM. Signature target: same publisher pubkey as row 535. Canonical-JSON SHA3-512: `4f21a5d589f1c7034c5e307a74fd9a06d195a2345c3bc5a5b56e3c9ed6260e7daa81463d10431758e2d3f9d89f87df35b24858de9ea2bbc21072616e133fb0f4`. Ed25519 signature: `43f53d200257fa54a5f5062a5fb297f45568bd1b19ae8ea9d2079816b3268b2c171b0d454da89db5c298d1c12f4e6fe8779669cf1a52469da5655a1bad554501`. lifecycle.signature_status: signed; lifecycle.runtime_load_status: loaded. immutable_kind: true. OD-1 path (a) closure: admin_risk_term_register removed from card. OD-3 path (a) closure: evidence_weights.<kind>.source_citation extension dropped. OD-4 deferred to follow-on hygiene dispatch. |

**Runtime-live total at this LOCK: 537 rows** (533 + 4 new rows).

# Amendment §C — signed-asset pinning at the Index

`vault_shared/cards/publisher_pubkey.signed.yaml` is pinned at this amendment's `companion_artifacts_pinned_at_LOCK` block. White-glove deployment manifest (per Reflection Packet v0.2 first wave precedent + WPFA Coefficient Registry precedent) records:

- `publisher_pubkey_ed25519_hex` — the 32-byte raw pubkey hex (pin target for `F-CARDS-SIGNATURE-INVALID` resolution).
- `canonical_bytes_sha3_512_hex` — the SHA3-512 of the signed-asset's canonical bytes (excluding the signature + hash fields).
- `publisher_signature_ed25519_hex` — operator self-signed at LOCK ceremony (Trust-On-First-Use initial install per §16 v1.1 Reflection Packet pattern).

Rotation policy: HIGH-severity admin-risk ledger entry required; new pubkey co-signed by prior pubkey; no automatic rotation at v0.1 Beta.

# Amendment §D — F-INDEX-STALE PRE-gate verification at compound commit

The compound paired-commit at lock_timestamp_utc 2026-05-15T20:30:00Z spans:

- lock_history row 226 (TILTH-CIC-01 card artifact LOCK)
- lock_history row 227 (TILTH-CLC-03 card artifact LOCK)
- lock_history row 228 (this §0.5 v25 paired-commit)

F-INDEX-STALE PRE-gate verification at compound commit:

1. **seat_owner consistency** — all four §0.5 v25 rows (534-537) carry `seat_owner: "cards_loader"`. ✓
2. **immutable_kind enforcement** — rows 535 + 537 carry `immutable_kind: true`. Any future amendment attempting kind-change → fail-closed. ✓
3. **F-CIC-CLC-COUPLING-VIOLATION regression** — neither card contains `common_clc_patterns_observed` / `eligible_cic_subset` / `cic_allowlist` / `cic_denylist` / `preferred_cics` / `cic_win_rate` / `cic_ranking_preferences` fields. ✓
4. **Path B naming reconciliation** — F-CARDS-* family does NOT cross to other orthogonal F-* families (F-PACKET- / F-WPFA- / F-REPORT- / F-FG- / F-DATACOLLECTOR- / F-ARCHIVIST- / F-REFLECTION-). ✓
5. **Signature verification round-trip** — both cards' canonical-JSON SHA3-512 + Ed25519 signature verify against the pinned publisher pubkey. ✓ (Verified at LOCK ceremony 2026-05-15 PM via the operator-runnable verification script; see lock_history row 226/227 verdict fields.)

# Amendment §E — operator-decision queue closure summary

This amendment is the canonical Index-layer record of the following operator decisions at LOCK ceremony 2026-05-15 PM:

**Food Systems CIC:**
- Soul Fire Farm + NEFOC LT named-exemplar disposition: relocation to `_research_metadata.priors_consulted` (Cycle 2 fix-in-place C2-02) preserved. No further anonymization at LOCK. **CLOSED.**
- Judge transport dual-record artifact: documented in `FINAL_VERDICT.md` footer; not a LOCK blocker. **CLOSED.**

**Operating Capacity CLC:**
- OD-1 `admin_risk_term_register` schema-extension posture: path **(a)** — removed from CLC. **CLOSED at card layer.** Migration of CLC-03-specific terms to workspace-wide `admin_risk_register.yaml` v2.3 = follow-on dispatch.
- OD-2 equity reviewer_context refined framing: subsumed by OD-1 path (a) closure (the equity entry no longer exists in the card). **CLOSED.**
- OD-3 `evidence_weights.<kind>.source_citation` schema-extension posture: path **(a)** — optional source_citation dropped on every entry. **CLOSED.**
- OD-4 pre-LOCK Internet Archive snapshot pass on `_research_metadata.primary_sources` URLs: **deferred** to follow-on hygiene dispatch per operator default 2026-05-15 PM.

# Amendment §F — follow-on dispatches surfaced at this LOCK

1. **admin_risk_register.yaml v2.3 migration** — append CLC-03-specific terms `infrastructure` standalone, `scalability`, `capacity building`, `innovation`, `transformation`, `stakeholder` standalone to the workspace-wide register. Requires operator_approval_token flow per the register's existing approval discipline. Trichotomy (severity / federal_severity / progressive_register) preserved on the workspace-wide register.

2. **Internet Archive snapshot pass** — snapshot `_research_metadata.primary_sources` URLs from both cards (especially press-release / blog-style URLs prone to rotation); add `archived_url` field to each primary_sources entry. v1.x amendment-realization checklist binding.

3. **F-CARDS-PUBLISHER-PUBKEY-HASH-MISMATCH sub-tag realization** — at v0.2 first wave loader-realization, the loader compares `canonical_bytes_sha3_512_hex` from `publisher_pubkey.signed.yaml` against the white-glove-pinned hash. Sub-tag of `F-CARDS-SIGNATURE-INVALID`. Forward-binding at v1.x amendment-realization checklist.

# Amendment §G — verdict

**§0.5 v25 LOCKED 2026-05-15 PM** as paired-commit triple-member-3 with lock_history rows 226 + 227 at lock_timestamp_utc 2026-05-15T20:30:00Z per §6.17 Option-B. Four rows promoted PARENT_UNLOCKED → STABLE atomically. New runtime-live total: 537. First `card` primitive_kind landed at the Index. First card-class artifact LOCK precedent established for Wave 2+ card LOCKs.
