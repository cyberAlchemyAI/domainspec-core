---
title: §0.5 v33 — paired-commit amendment for cards-publisher key rotation (compromise-class TOFU re-pin 2026-05-18)
filed: 2026-05-18
operator: Josh Inklovich
status: LOCKED 2026-05-18T00:00:00Z — paired-commit with key_rotation row 280 per §6.17 Option-B compound-commit pattern at 2026-05-18 cards-publisher rotation ceremony. Self-LOCK per compromise-response carve-out (key-management event riding the §6.17 Option-B paired-commit primitive; no new runtime enforcement teeth — audit-trail anchor only for the rotation event).
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_section_18_11_v1_1_amendment.md      # §0.5 v30 LOCKED 2026-05-17T04:34:50Z row 271 (OD-D documentation-only marker-only paired-commit)
  - pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_7_amendment.md       # §0.5 v31 LOCKED 2026-05-17T05:30:00Z row 273 (OD-C marker-only paired-commit)
  - pipeline/blueprint/v0.1/section_00_5_section_18_6_v2_amendment.md         # §0.5 v32 LOCKED 2026-05-17 row 275 (OD-E marker-only paired-commit; immediate predecessor)
companion_lock_with:
  - vault_shared/cards/publisher_pubkey.signed.yaml  # paired-commit per §6.17 Option-B — cards-publisher pubkey rotation
compromise_record: pipeline/handoffs/cards_publisher_key_rotation_2026-05-17/05_old_key_compromise_record.md
runbook_ref: vault_shared/key_rotation_policy.md §4 (compromise-response runbook)
row_delta: prior runtime-live total at §0.5 v32 LOCK 2026-05-17 = 541 rows (per lock_history row 275 `runtime_live_total_after`). **§0.5 v33 amendment claims 1 row (marker only): row 542.** NO new schema row. NO new failure-code row. NO new AST-lint row. NO new vocabulary kind. New runtime-live total at this LOCK = 542.
kind_of_amendment: row-append (marker only; compromise-response audit anchor). NO new vocabulary kind — the marker row's `primitive_kind` resolves against the v5 + v6 + v17-v19 closed vocabulary.
cross_family_posture: Self-LOCK per compromise-response carve-out — operator-authorized rotation per key_rotation_policy.md §4 runbook. L-005 Thesis dispatch waived under compromise-response-class scope (no new enforcement teeth at the §0.5 paired-commit layer; runtime impact lives in row 280's pubkey re-pin + the publisher_pubkey.signed.yaml update).
---

# Amendment intent

This amendment lands paired with the cards-publisher key_rotation row 280 per §6.17 Option-B compound-commit pattern. Row 280 retires the COMPROMISED pubkey `0b1a0bbfa5ee9149af2c4e6153ed037dd03c0d562c94d3eaefeaf798e6f375bd` and pins the NEW pubkey `c93f1881cbb7ff315b29f416c2f8bc16dc9e1d1576e743f63e577de992e41107` per the Trust-On-First-Use re-pin path (`key_rotation_policy.md` §4.1 step 5 second clause — old key under attacker control after exposure in Dispatch chat 2026-05-17).

The amendment mirrors the §0.5 v26 / v30 / v31 / v32 marker-only paired-commit precedent: a compromise-response audit anchor at the lock_history layer with no schema rows, no failure-code rows, no AST-lint rows, and no new vocabulary kinds.

# §A — Row append (row 542)

Primitive id: `blueprint.amendment_anchor.cards_publisher_rotation.v1`
Kind: `marker`
Seat owner: `cards`
Stability tier: `STABLE`
Parent lock version: cards-publisher TOFU re-pin (`key_rotation_policy.md` §4.1 step 5 second clause)
Defined at: `pipeline/blueprint/v0.1/section_00_5_cards_publisher_rotation_amendment.md`

Runtime-live total: 541 → **542**.

# §B — Retroactive validity preservation

All lock_history rows 226-279 signed under the prior pubkey `0b1a0bbf…6f375bd` remain audit-valid: at signing time the prior key was not yet exposed, and signature verification against the prior pubkey continues to succeed for any party that recorded the prior pubkey before its retirement. This rotation prevents FUTURE use of the compromised seed; it does NOT retroactively invalidate prior signatures.

The retired pubkey is preserved in `pipeline/handoffs/cards_publisher_key_rotation_2026-05-17/05_old_key_compromise_record.md` plus the `old_pubkey_ed25519_hex` field on lock_history row 280 for ongoing verification of historical rows.

# §C — Forward sequencing

After this paired-commit (row 281) lands, the next paired-commit version (§0.5 v34) lands paired with the OD-E fix-forward ceremony — see `pipeline/handoffs/od_e_fix_forward_paired_commit_2026-05-17.md` (rows 282-288 under the NEW cards-publisher key).
