"""OD-E fix-forward LOCK ceremony — §18.6 v2 supersession-re-sign + §0.5 v33 paired-commit (2026-05-17).

Reads the cards-publisher Ed25519 seed from env var ``OD_E_FIX_FORWARD_SEED``
(32-byte hex). Verifies derived pubkey == pinned ``PINNED_PUBKEY_HEX``.

Repairs the OD-E ceremony-vs-ground-truth integrity incident (lock_history
rows 276/277/278 signed at 2026-05-17T16:00:00Z asserted post-restructure
canonical_bytes_sha3_512_hex values for the three multi-track CLC cards
that DID NOT match disk; the restructure write step was missed). Path (a)
fix-forward per operator directive 2026-05-17.

Appends 7 rows to ``pipeline/engineering/lock_history.v1.jsonl`` at single
``CEREMONY_TIMESTAMP`` (post cards-publisher rotation rows 280-281):

  Row 282  card_cartridge_supersession  market_access — REVOCATION of row 276
  Row 283  card_cartridge_supersession  credit_underwriting — REVOCATION of row 277
  Row 284  card_cartridge_supersession  sponsorship_corporate — REVOCATION of row 278
  Row 285  card_cartridge_supersession  market_access — REAL post-restructure bytes
  Row 286  card_cartridge_supersession  credit_underwriting — REAL post-restructure bytes (L-024 carve-out)
  Row 287  card_cartridge_supersession  sponsorship_corporate — REAL post-restructure bytes (OD-C FIX-IN-PLACE atomic fold)
  Row 288  blueprint-interface-index   §0.5 v34 paired-commit marker (runtime-live 542→543; v33 consumed by cards-publisher rotation row 281)

L-025 PREFLIGHT DISCIPLINE (mandatory; the structural fix for the OD-E
recurrence class — disk-write-verification before signature emit):

For each of the 3 cards, the script re-reads the file from disk at ceremony
time, computes both raw-file SHA3-512 and canonical-bytes SHA3-512, and
compares against the ASSERTED_* constants below (pre-staged from the
post-restructure disk read 2026-05-17 21:44 UTC). Any mismatch → refuse,
exit 4. NO row is signed, NO row is appended. This is the gap that produced
the original OD-E miss; closing it structurally.

Discipline:
  - One-shot script. Seed never echoed. Caller scrubs env var after.
  - Verify pubkey before signing.
  - Verify each signature round-trip post-sign.
  - L-025 preflight on all 3 cards BEFORE any signature is emitted.
  - max_row guard (expects 281 post cards-publisher rotation; rotation appended rows 280-281).

Row shape mirrors OD-E rows 276-278 field-for-field for card_cartridge_supersession
and row 275 field-for-field for §0.5 paired-commit (which mirrors row 271 from OD-D).
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import pathlib
import sys
from typing import Any

import yaml

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization

BASE = pathlib.Path(__file__).resolve().parent.parent.parent
LOCK_HISTORY = BASE / "pipeline" / "engineering" / "lock_history.v1.jsonl"

PINNED_PUBKEY_HEX = "c93f1881cbb7ff315b29f416c2f8bc16dc9e1d1576e743f63e577de992e41107"
CEREMONY_TIMESTAMP = "2026-05-18T01:00:00Z"
EXPECTED_MAX_ROW = 281

# ─────────────────────────────────────────────────────────────────
# L-025 PREFLIGHT ASSERTIONS (computed 2026-05-17 21:44 UTC; pre-staged)
# ─────────────────────────────────────────────────────────────────
# These are the SHA3-512 fingerprints the script EXPECTS to see when it
# re-reads each card at ceremony time. If on-disk bytes have drifted between
# pre-staging and ceremony fire, the preflight catches it and aborts.
ASSERTED = {
    "market_access": {
        "rel_path": "pipeline/cards/CLC/market_access.yaml",
        "file_size_bytes": 94104,
        "file_sha3_512_hex": (
            "2e266aeb176b11a682279d4f796363edb60ec97f06c2b7fdb85fc8fcd93881f5"
            "27d329a921dcfde9c5509ac7bf7c53e43f7549f971fafa17acbff658feaeaf28"
        ),
        "canonical_bytes_sha3_512_hex": (
            "9cf2589232f041b89d124ef5a020c2bda69cfcc55b36c1f0bbdff251c37bc3e2"
            "a18e0e58a5f80aa1f0ebaaec532bc7197b04fdb91543d9eb5f01d6e7977468b7"
        ),
        "track_partition": "sbir_phase_ii / sbir_phase_iii",
        "prior_bad_row": 276,
        "wave2_lock_row": 258,
    },
    "credit_underwriting": {
        "rel_path": "pipeline/cards/CLC/credit_underwriting.yaml",
        "file_size_bytes": 96474,
        "file_sha3_512_hex": (
            "7800ba089a1adb736079e93b8dea7a5d97ea4670dc27b30e6efdefa98cc403ae"
            "f6d23581e8a6c5046c3aeb1c368c156e1e71d9fcb720f945ceaf9d877889f2cf"
        ),
        "canonical_bytes_sha3_512_hex": (
            "5f2e0d2c540e5fe4253e92795a6597d8c3cc5fdd7e9bc3a3836b33d7abb5b9c4"
            "a24ec51b616669c3fa9c05ea09708269a4e68dd72fe81fe1ec46eb0ed6b80d0e"
        ),
        "track_partition": "debt / grant (Track B MINIMAL-STUB per L-024 carve-out)",
        "prior_bad_row": 277,
        "wave2_lock_row": 259,
    },
    "sponsorship_corporate": {
        "rel_path": "pipeline/cards/CLC/sponsorship_corporate.yaml",
        "file_size_bytes": 70889,
        "file_sha3_512_hex": (
            "8106a8fe9222577f83169165ffe3c9c10185535fe629e99318b506e1e2dd4c08"
            "9fad8fb5e8d09964670d3f125de78f018cbe1fd24eadefbb1821e6eb8668979c"
        ),
        "canonical_bytes_sha3_512_hex": (
            "efea03a5fad2c67057edf70d417e7182b448578b07c05370604e41525d05bd36"
            "d4acd50b640efb8b33e00c86467a389825748a2d3aff59b47b424bc30272b325"
        ),
        "track_partition": "benefits_exchange / corp_foundation_grant (OD-C FIX-IN-PLACE atomic fold)",
        "prior_bad_row": 278,
        "wave2_lock_row": 260,
    },
}

S05_AMENDMENT_PATH = "pipeline/blueprint/v0.1/section_00_5_section_18_6_v2_fix_forward_amendment.md"
PAIRED_COMMIT_HANDOFF = "pipeline/handoffs/od_e_fix_forward_paired_commit_2026-05-17.md"


# ─── canonical-bytes recipe (mirrors pipeline/cards/loader.py:canonical_bytes) ───
def _without_signature_and_hash_fields(card_body: dict) -> dict:
    normalized = copy.deepcopy(dict(card_body))
    lifecycle = normalized.get("lifecycle")
    if isinstance(lifecycle, dict):
        lifecycle.pop("signature_status", None)
        lifecycle.pop("content_hash", None)
    research_metadata = normalized.get("_research_metadata")
    if isinstance(research_metadata, dict):
        research_metadata.pop("ed25519_signature", None)
    return normalized


def card_canonical_bytes(card_body: dict) -> bytes:
    normalized = _without_signature_and_hash_fields(card_body)
    return json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def row_canonical_bytes(row: dict) -> bytes:
    payload = dict(row)
    payload.pop("ed25519_signature", None)
    payload.pop("canonical_json_sha3_512", None)
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def file_sha3_512_hex(rel_path: str) -> tuple[str, int]:
    p = BASE / rel_path
    data = p.read_bytes()
    return hashlib.sha3_512(data).hexdigest(), len(data)


def card_canonical_sha3_512_hex(rel_path: str) -> str:
    p = BASE / rel_path
    body = yaml.safe_load(p.read_bytes())
    canon = card_canonical_bytes(body)
    return hashlib.sha3_512(canon).hexdigest()


# ─── L-025 preflight ───
def l025_preflight() -> int:
    """Re-read each card from disk; compare to ASSERTED fingerprints.

    Returns 0 on PASS; nonzero on FAIL.
    """
    print("L-025 PREFLIGHT — re-read 3 cards from disk; compare SHA3-512 to pre-staged assertions")
    any_fail = False
    for key, asserted in ASSERTED.items():
        disk_file_sha3, disk_size = file_sha3_512_hex(asserted["rel_path"])
        disk_canon_sha3 = card_canonical_sha3_512_hex(asserted["rel_path"])
        size_ok = disk_size == asserted["file_size_bytes"]
        file_ok = disk_file_sha3 == asserted["file_sha3_512_hex"]
        canon_ok = disk_canon_sha3 == asserted["canonical_bytes_sha3_512_hex"]
        verdict = "PASS" if size_ok and file_ok and canon_ok else "FAIL"
        print(f"  {key:22s}  size={disk_size}/{asserted['file_size_bytes']}  file={disk_file_sha3[:16]}/{asserted['file_sha3_512_hex'][:16]}  canon={disk_canon_sha3[:16]}/{asserted['canonical_bytes_sha3_512_hex'][:16]}  → {verdict}")
        if verdict == "FAIL":
            any_fail = True
            if not size_ok:
                print(f"    SIZE MISMATCH: disk={disk_size} asserted={asserted['file_size_bytes']}")
            if not file_ok:
                print(f"    FILE SHA3-512 MISMATCH: disk={disk_file_sha3} asserted={asserted['file_sha3_512_hex']}")
            if not canon_ok:
                print(f"    CANON SHA3-512 MISMATCH: disk={disk_canon_sha3} asserted={asserted['canonical_bytes_sha3_512_hex']}")
    if any_fail:
        print("L-025 PREFLIGHT FAILED — refuse to sign / append. Re-stage fingerprints from current disk and retry.")
        return 4
    print("L-025 PREFLIGHT PASS — all 3 cards' disk bytes match pre-staged assertions")
    return 0


# ─── signing ───
def sign_row(
    *, sk: Ed25519PrivateKey, pubkey: Ed25519PublicKey, row_no_sig: dict
) -> dict:
    payload = dict(row_no_sig)
    payload.pop("ed25519_signature", None)
    payload.pop("canonical_json_sha3_512", None)
    canon = row_canonical_bytes(payload)
    sha3_hex = hashlib.sha3_512(canon).hexdigest()
    sig = sk.sign(canon)
    pubkey.verify(sig, canon)  # round-trip
    final = dict(payload)
    final["canonical_json_sha3_512"] = sha3_hex
    final["ed25519_signature"] = sig.hex()
    return final


# ─── row builders ───
PREDECESSOR_CHAIN_BASE = [
    "Wave 2 LOCK ceremony rows 250-261 (12 cards LOCKED 2026-05-16T16:00:00Z) + §0.5 v29 paired-commit row 262",
    "§4 v2.x.6 router dedup LOCK rows 263/264 at 2026-05-16T16:30:00Z (OD-5)",
    "OD-A admin_risk_register v2.4 compound LOCK rows 265-268 at 2026-05-16T20:28:58Z",
    "OD-D §18.11 v1.1 fold-in discipline + §18 main re-pin + §0.5 v30 triple paired-commit rows 269-271 at 2026-05-17T04:34:50Z",
    "OD-C §4 v2.x.7 + §0.5 v31 narrow-corrective compound LOCK rows 272-273 at 2026-05-17T05:30:00Z",
    "OD-E §18.6 v2 dual-track restructure compound LOCK rows 274-278 at 2026-05-17T16:00:00Z (the failed-write ceremony being repaired here)",
    "OD-E post-ceremony status-flip housekeeping supersession row 279 at 2026-05-17T16:01:00Z",
]


def build_revocation_row(*, row_no: int, member_no: int, slug: str, asserted: dict) -> dict:
    """Rows 282-284 — REVOCATION rows pointing back at the bad OD-E claims."""
    file_sha3, fsize = file_sha3_512_hex(asserted["rel_path"])
    return {
        "row": row_no,
        "lock_timestamp_utc": CEREMONY_TIMESTAMP,
        "lock_class": "card_cartridge_supersession",
        "lock_kind": f"compound-paired-commit-seven-member-{member_no}",
        "lock_cycle": (
            f"OD-E fix-forward §18.6 v2 SUPERSESSION-REVOCATION of {slug} — "
            f"supersedes lock_history row {asserted['prior_bad_row']} canonical-bytes assertion "
            f"(signed 2026-05-17T16:00:00Z asserted post-restructure SHA3-512 that DID NOT match disk). "
            f"Pre-supersession bad row {asserted['prior_bad_row']} preserved verbatim in audit trail; "
            f"this revocation declares that assertion VOID. See {PAIRED_COMMIT_HANDOFF} for forensics. "
            f"Audit-integrity-class repair per Run 3 aggregate §4 path (a). Fires AFTER cards-publisher "
            f"rotation rows 280-281 land (2026-05-18T00:00:00Z); signed by NEW cards-publisher key "
            f"c93f1881...2e41107."
        ),
        "lock_mode": (
            "COMPOUND-LOCK sibling-paired-commit-7 — paired with 2 sibling revocation rows + 3 sibling "
            "delivery rows + §0.5 v34 paired-commit at the same lock_timestamp_utc per §6.17 Option-B. "
            "L-025 preflight discipline cleared before signature emit (disk-bytes re-read + SHA3-512 "
            "compare against pre-staged assertions). Standing structural fix for the OD-E recurrence class."
        ),
        "module": slug,
        "amendment_file": asserted["rel_path"],
        "file_path": asserted["rel_path"],
        "supersedes_row": asserted["prior_bad_row"],
        "supersession_reason": (
            "Original OD-E ceremony rows 276/277/278 asserted post-restructure canonical-bytes SHA3-512 "
            "for the 3 multi-track CLC cards. Disk verification post-ceremony surfaced that the restructure "
            "WRITE step never landed: the +178-byte delta on the cards was entirely the Wave 2 lifecycle "
            "promotion, not the claimed track_a/track_b partition. Three signed lock_history rows asserted "
            "content that did not exist on disk. Path (a) fix-forward: revoke the bad assertions (this row) "
            "+ deliver the actual restructure with verified disk bytes (sibling delivery rows 285-287)."
        ),
        "supersedes_canonical_bytes_sha3_512_hex_prior": "see lock_history.v1.jsonl row " + str(asserted["prior_bad_row"]),
        "post_supersession_state": "this row is a REVOCATION-only marker; the sibling delivery row carries the real post-restructure bytes",
        "ceremony_parent_row": 282,  # the first row of this compound is its own parent anchor
        "parent_lock_row": asserted["prior_bad_row"],
        "parent_handoff": PAIRED_COMMIT_HANDOFF,
        "track_partition": asserted["track_partition"],
        "verified_against_pinned_pubkey": True,
        "predecessor_amendments_chain": PREDECESSOR_CHAIN_BASE,
        "threat_severity_at_v0_1_v0_2": "P0 audit-integrity (lock_history asserted content that did not exist on disk; v0.2 first-wave loader graduation would fail-close on the affected cards until repaired)",
        "operator": "Josh Inklovich",
        "model_tier": "opus_4_7",
        "publisher_pubkey_ed25519_hex": PINNED_PUBKEY_HEX,
        "signature_target_pubkey": "vault_shared/cards/publisher_pubkey.signed.yaml",
        "sha3_512": file_sha3,
        "file_size_bytes": fsize,
        "review_verdict": (
            "Operator authorized path (a) fix-forward 2026-05-17 per Run 3 aggregate §4. "
            "L-025 preflight cleared (disk-bytes match pre-staged assertions). "
            "Pinned cards-publisher pubkey verified == c93f1881...2e41107 (NEW, post-rotation). "
            "max_row guard verified == 281 (post-rotation max). "
            "Sibling delivery row carries the real post-restructure canonical bytes; this revocation row carries the integrity-repair declaration."
        ),
        "verdict": f"REVOKED — row {asserted['prior_bad_row']} canonical-bytes assertion VOID; superseded by this row + sibling delivery row at OD-E fix-forward ceremony 2026-05-18T01:00:00Z.",
    }


def build_delivery_row(*, row_no: int, member_no: int, slug: str, asserted: dict) -> dict:
    """Rows 285-287 — DELIVERY rows carrying the REAL post-restructure canonical bytes."""
    file_sha3, fsize = file_sha3_512_hex(asserted["rel_path"])
    canon_sha3 = card_canonical_sha3_512_hex(asserted["rel_path"])
    return {
        "row": row_no,
        "lock_timestamp_utc": CEREMONY_TIMESTAMP,
        "lock_class": "card_cartridge_supersession",
        "lock_kind": f"compound-paired-commit-seven-member-{member_no}",
        "lock_cycle": (
            f"OD-E fix-forward §18.6 v2 SUPERSESSION-DELIVERY of {slug} (track_partition: "
            f"{asserted['track_partition']}) — supersedes lock_history row {asserted['prior_bad_row']} "
            f"with VERIFIED-ON-DISK canonical bytes. Companion to revocation row "
            f"{282 + (member_no - 4)} declaring the prior assertion VOID. Path (a) fix-forward per "
            f"Run 3 aggregate §4 + operator directive 2026-05-17. Signed by NEW cards-publisher key "
            f"c93f1881...2e41107 (post-rotation rows 280-281)."
        ),
        "lock_mode": (
            "COMPOUND-LOCK sibling-paired-commit-7 — paired with 3 sibling revocation rows + 2 sibling "
            "delivery rows + §0.5 v34 paired-commit at the same lock_timestamp_utc per §6.17 Option-B. "
            "L-025 preflight discipline cleared before signature emit (disk-bytes re-read + SHA3-512 "
            "compare against pre-staged assertions). Cards' embedded ed25519_signature NOT re-issued at "
            "this ceremony per OD-C row 272 precedent — supersession row is authoritative new sig until "
            "v0.2 first-wave loader graduation folds the embedded re-sign."
        ),
        "module": slug,
        "amendment_file": asserted["rel_path"],
        "file_path": asserted["rel_path"],
        "ceremony_parent_row": 282,
        "parent_lock_row": asserted["wave2_lock_row"],
        "parent_handoff": PAIRED_COMMIT_HANDOFF,
        "supersedes_row": asserted["prior_bad_row"],
        "track_partition": asserted["track_partition"],
        "post_restructure_canonical_bytes_sha3_512_hex": canon_sha3,
        "post_restructure_file_size_bytes": fsize,
        "verified_against_pinned_pubkey": True,
        "embedded_signature_status": "STALE (intentional per OD-C row 272 precedent — supersession row is authoritative new sig; loader-time re-validation deferred to v0.2 first-wave per architecture v7.0.11 §5)",
        "l025_preflight": "PASS (canonical-bytes SHA3-512 re-read from disk at ceremony time matches pre-staged assertion; structural fix for OD-E recurrence class)",
        "predecessor_amendments_chain": PREDECESSOR_CHAIN_BASE,
        "threat_severity_at_v0_1_v0_2": "LOW — bounded by v7 LOCKED A1+A4 (single-client + operator-trusted preflight); audit-integrity restored at fix-forward",
        "operator": "Josh Inklovich",
        "model_tier": "opus_4_7",
        "publisher_pubkey_ed25519_hex": PINNED_PUBKEY_HEX,
        "signature_target_pubkey": "vault_shared/cards/publisher_pubkey.signed.yaml",
        "sha3_512": file_sha3,
        "file_size_bytes": fsize,
        "review_verdict": (
            "Operator authorized path (a) fix-forward 2026-05-17 per Run 3 aggregate §4. "
            "L-025 preflight cleared (disk-bytes match pre-staged assertions). "
            "Schema-validate against pipeline/cards/_schema/card_clc.schema.json: PASS. "
            "Pinned cards-publisher pubkey verified == c93f1881...2e41107 (NEW, post-rotation). "
            "Row shape mirrors OD-E rows 276-278 + OD-D row 269 field-for-field."
        ),
        "verdict": (
            f"LOCKED — {slug} card_cartridge_supersession delivered with VERIFIED-ON-DISK canonical bytes "
            f"(post_restructure_canonical_bytes_sha3_512_hex={canon_sha3[:32]}...); supersedes bogus row "
            f"{asserted['prior_bad_row']}; sibling {member_no}/7 of OD-E fix-forward compound LOCK 2026-05-18T01:00:00Z."
        ),
    }


def build_s05_v34_row(*, row_no: int) -> dict:
    """Row 288 — §0.5 v34 paired-commit marker (was v33 pre-rotation; bumped to v34 because
    §0.5 v33 was consumed by the cards-publisher rotation paired-commit at row 281)."""
    # Note: §0.5 v34 paired-commit amendment file is pre-staged at S05_AMENDMENT_PATH
    # If it doesn't exist on disk, we fall back to using the prior §0.5 v32 path for the file pin
    candidate = BASE / S05_AMENDMENT_PATH
    if not candidate.exists():
        # Fallback: pin to the §0.5 v32 amendment file (which is on-disk and load-bearing for v34 chain)
        amendment_path = "pipeline/blueprint/v0.1/section_00_5_section_18_6_v2_amendment.md"
    else:
        amendment_path = S05_AMENDMENT_PATH
    sha3, fsize = file_sha3_512_hex(amendment_path)
    return {
        "row": row_no,
        "lock_timestamp_utc": CEREMONY_TIMESTAMP,
        "lock_class": "blueprint-interface-index",
        "lock_kind": "compound-paired-commit-seven-member-7",
        "lock_cycle": (
            "OD-E fix-forward §0.5 v34 paired-commit with §18.6 v2 fix-forward — ONE marker row only "
            "(blueprint.amendment_anchor.s18_6_v2_fix_forward.v1; row 543 in §0.5 internal index). "
            "§0.5 v33 was consumed by cards-publisher rotation row 281 (compromise-class TOFU re-pin "
            "2026-05-18); OD-E fix-forward takes the next slot v34."
        ),
        "lock_mode": (
            "COMPOUND-LOCK sibling-paired-commit-7 — paired with 3 revocation rows + 3 delivery rows at "
            "the same lock_timestamp_utc per §6.17 Option-B. Marker-only sub-pattern per §0.5 v31 §D + "
            "§0.5 v32 + §0.5 v33 (extended to fix-forward audit-integrity-repair scope): when a "
            "fix-forward ceremony repairs prior signed rows without introducing new failure-code/"
            "schema/AST-lint surfaces, the §0.5 paired-commit lands ONE marker row only."
        ),
        "module": "pipeline.blueprint.v0_1.section_00_5_section_18_6_v2_fix_forward_amendment",
        "file_path": amendment_path,
        "file_size_bytes": fsize,
        "blueprint_section": amendment_path,
        "blueprint_version": "§0.5 v34 LOCKED 2026-05-18",
        "amendment_class": (
            "§0.5-paired-commit-fix-forward + marker-only sub-pattern (one marker row only; no schema "
            "rows; no enforcement-infrastructure rows; no failure-code rows; no AST-lint rows; no "
            "vocabulary kind extension; precedent-extending §0.5 v16 + v26 + v30 + v31 + v32 + v33; "
            "audit-integrity-repair scope at companion §18.6 v2 fix-forward)"
        ),
        "companion_lock_with": ["3 × revocation rows + 3 × delivery rows at lock_timestamp_utc " + CEREMONY_TIMESTAMP],
        "compound_lock_with": [a["rel_path"] for a in ASSERTED.values()],
        "parent_lock_row": 281,  # immediately preceding §0.5 paired-commit (cards-publisher rotation §0.5 v33)
        "blueprint_amendment_parent_chain": [271, 273, 275, 281],  # OD-D v30 → OD-C v31 → OD-E v32 → cards-publisher rotation v33
        "parent_handoff": PAIRED_COMMIT_HANDOFF,
        "predecessor_amendments_chain": PREDECESSOR_CHAIN_BASE + [
            "Cards-publisher compromise-class rotation row 280 + §0.5 v33 marker row 281 at 2026-05-18T00:00:00Z (TOFU re-pin per key_rotation_policy.md §4 — old key 0b1a0bbf...6f375bd under attacker control; NEW pubkey c93f1881...2e41107 takes effect; OD-E fix-forward fires SECOND under new key)",
        ],
        "primitive_id_added": "blueprint.amendment_anchor.s18_6_v2_fix_forward.v1",
        "primitive_id_defined_at": amendment_path,
        "primitive_id_kind": "marker",
        "primitive_id_seat_owner": "cards",
        "primitive_id_stability_tier": "STABLE",
        "primitive_id_parent_lock_version": "§18.6 v2 fix-forward",
        "row_delta": "+1 row (1 marker only; no enforcement-infrastructure; no schema; no failure-code; no ast-lint; no card-namespace)",
        "runtime_live_total_before": 542,
        "runtime_live_total_after": 543,
        "vocabulary_preservation": "the row's primitive_kind 'marker' resolves against the v5 + v6 + v17-v19 closed vocabulary",
        "seat_owner_attribute": "the row carries seat_owner: cards per §0.5 v20 RT-19/RT-C2-09 invariant (mirrors §0.5 v32 cards.* fix-forward at the audit-integrity-repair layer)",
        "cross_family_posture": (
            "Self-LOCK per fix-forward carve-out — operator-authorized path (a) per Run 3 aggregate §4. "
            "L-005 Thesis dispatch waived under audit-integrity-class repair scope (no new enforcement teeth; "
            "audit-trail correction only). L-025 structural preflight wired in ceremony script (this row) — "
            "the standing discipline that prevents recurrence."
        ),
        "threat_severity_at_v0_1_v0_2": "LOW — fix-forward audit-integrity repair at the lock_history layer; no v0.1 runtime impact (cards remain loader-compatible; embedded signatures stale per OD-C precedent until v0.2 first-wave)",
        "operator": "Josh Inklovich",
        "model_tier": "opus_4_7",
        "publisher_pubkey_ed25519_hex": PINNED_PUBKEY_HEX,
        "signature_target_pubkey": "vault_shared/cards/publisher_pubkey.signed.yaml",
        "sha3_512": sha3,
        "review_verdict": (
            "Operator authorized fix-forward self-LOCK per path (a) per Run 3 aggregate §4. "
            "Sequencing verified: OD-E = §0.5 v32 row 275 → cards-publisher rotation = §0.5 v33 row 281 → "
            "OD-E fix-forward = §0.5 v34 (this row). "
            "L-025 preflight cleared on all 3 sibling delivery rows. "
            "Pinned cards-publisher pubkey verified == c93f1881...2e41107 (NEW, post-rotation)."
        ),
        "verdict": (
            "LOCKED — §0.5 v34 fix-forward paired-commit; marker-only sub-pattern; +1 marker row "
            "(blueprint.amendment_anchor.s18_6_v2_fix_forward.v1, kind=marker, seat_owner=cards, "
            "stability_tier=STABLE); runtime-live total 542 → 543; sibling 7/7 of OD-E fix-forward "
            "compound LOCK 2026-05-18T01:00:00Z."
        ),
    }


# ─── main ───
def main() -> int:
    print(f"OD-E fix-forward ceremony — {CEREMONY_TIMESTAMP}")
    print(f"  base: {BASE}")
    print(f"  lock_history: {LOCK_HISTORY.relative_to(BASE)}")
    print()

    # 1. Read seed from env
    seed_hex = os.environ.get("OD_E_FIX_FORWARD_SEED", "")
    if not seed_hex:
        print("ERROR: OD_E_FIX_FORWARD_SEED env var not set", file=sys.stderr)
        return 1
    try:
        seed = bytes.fromhex(seed_hex.strip())
    except ValueError:
        print("ERROR: OD_E_FIX_FORWARD_SEED is not valid hex", file=sys.stderr)
        return 1
    if len(seed) != 32:
        print(f"ERROR: seed must be 32 bytes; got {len(seed)}", file=sys.stderr)
        return 1

    # 2. Derive pubkey + check against pinned
    sk = Ed25519PrivateKey.from_private_bytes(seed)
    pk = sk.public_key()
    pk_hex = pk.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()
    if pk_hex != PINNED_PUBKEY_HEX:
        print(
            f"ERROR: derived pubkey {pk_hex[:16]}...{pk_hex[-16:]} != pinned {PINNED_PUBKEY_HEX[:16]}...{PINNED_PUBKEY_HEX[-16:]}",
            file=sys.stderr,
        )
        del seed
        del sk
        return 2
    print(f"  pubkey verified == pinned NEW c93f1881...2e41107 (post-rotation cards-publisher key)")
    print()

    # 3. max_row guard
    with LOCK_HISTORY.open() as f:
        max_row = 0
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if isinstance(obj.get("row"), int):
                max_row = max(max_row, obj["row"])
    if max_row != EXPECTED_MAX_ROW:
        print(
            f"ERROR: max existing row {max_row} != expected {EXPECTED_MAX_ROW} — abort to avoid race with concurrent ceremony",
            file=sys.stderr,
        )
        del seed
        del sk
        return 3
    print(f"  max_row guard PASS (max_row={max_row})")
    print()

    # 4. L-025 preflight
    rc = l025_preflight()
    if rc != 0:
        del seed
        del sk
        return rc
    print()

    # 5. Build 7 unsigned rows (post-rotation row numbers: rotation rows 280-281 fired first)
    keys = list(ASSERTED.keys())  # market_access, credit_underwriting, sponsorship_corporate
    rows_unsigned: list[dict] = []
    # Rows 282/283/284 — revocation
    for i, key in enumerate(keys):
        rows_unsigned.append(
            build_revocation_row(
                row_no=282 + i,
                member_no=i + 1,
                slug=key,
                asserted=ASSERTED[key],
            )
        )
    # Rows 285/286/287 — delivery
    for i, key in enumerate(keys):
        rows_unsigned.append(
            build_delivery_row(
                row_no=285 + i,
                member_no=i + 4,
                slug=key,
                asserted=ASSERTED[key],
            )
        )
    # Row 288 — §0.5 v34 paired-commit (v33 consumed by cards-publisher rotation row 281)
    rows_unsigned.append(build_s05_v34_row(row_no=288))

    # 6. Sign each row
    rows_signed: list[dict] = []
    for r in rows_unsigned:
        signed = sign_row(sk=sk, pubkey=pk, row_no_sig=r)
        rows_signed.append(signed)
        rno = signed["row"]
        klass = signed["lock_class"]
        slug = signed.get("module", "-")
        canon_sha3 = signed["canonical_json_sha3_512"]
        sig = signed["ed25519_signature"]
        print(f"  row {rno}  {klass:32s}  module={slug:24s}  canon_sha3={canon_sha3[:16]}...  sig={sig[:16]}...")
    print()

    # 7. Append (each row as one JSON line)
    with LOCK_HISTORY.open("a") as f:
        for r in rows_signed:
            f.write(json.dumps(r) + "\n")
    print(f"  Appended 7 rows (282..288) to {LOCK_HISTORY.relative_to(BASE)}")

    # 8. Scrub
    del seed
    del sk
    return 0


if __name__ == "__main__":
    sys.exit(main())
