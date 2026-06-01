"""Signature round-trip verifier for every Ed25519-signed asset on the repo.

Closes audit weakness #2 from ``docs/project_audit_2026-05-18.md`` §13 row 2 — the
ceremonial signing chain becomes verification, not narrative. Runs in CI on every
push and pull-request; intended as the ``signature-roundtrip`` required-status job.

Scope (every signed-asset family on current ``main``):

  1. ``vault_shared/cards/publisher_pubkey.signed.yaml`` — TOFU self-signed (YAML
     canonicalization recipe per ``pipeline/scripts/cards_publisher_key_rotation_
     ceremony_2026-05-17.py::update_pubkey_yaml_self_signature``).
  2. ``vault_shared/funder_intelligence/publisher_pubkey.signed.yaml`` — TOFU
     self-signed (JSON-canonical "Path 2" recipe per the file's documented
     algorithm).
  3. ``vault_shared/operator_attestation/publisher_pubkey.signed.yaml`` — TOFU
     self-signed (JSON-canonical recipe per the file's documented algorithm).
  4. Placeholder pubkey YAMLs (``program_rule_packs``, ``reflection_packet``,
     ``wpfa``) — detected and SKIPPED with INFO log; hard-fail only if a real
     non-placeholder signature appears that does not verify.
  5. ``pipeline/engineering/lock_history.v1.jsonl`` — every row whose
     ``ed25519_signature`` is set is verified against its declared
     ``publisher_pubkey_ed25519_hex`` (current pubkey for the new-key cohort,
     retired pubkey for the historical cohort; both pinned in the verifier and
     cross-checked against the rotation row ``old_pubkey_ed25519_hex`` /
     ``new_pubkey_ed25519_hex`` for drift detection).
  6. ``pipeline/cards/{CIC,CLC}/*.yaml`` — recomputes ``lifecycle.content_hash``
     (canonical-JSON SHA-256, mirroring ``pipeline/cards/loader.py::
     canonical_bytes_sha256``) and attempts Ed25519 verify of
     ``_research_metadata.ed25519_signature`` under the current cards-publisher
     pubkey.

Stale-by-design handling. The audit doc, the FID-publisher-pubkey YAML's "v0.2
NOTE", and the OD-C row 272 / OD-E precedent explicitly document a class of
embedded card signatures and Wave-1 ``card_cartridge`` lock_history rows whose
on-disk canonicalization is not reproducible at v0.1 (cards-publisher signed-
asset shape and Wave-1 card hashing have outstanding reconciliation slated for
v0.2 first-wave loader graduation). The verifier consults a checked-in
allowlist (``pipeline/scripts/signature_verification_deferred.yaml``) before
hard-failing on such an asset; allowlist entries are PASS-through with a clear
DEFERRED-V0.2-RECONCILIATION marker in the log. Any signature failure not on
the allowlist hard-fails the build — exactly the property the audit doc asked
for.

Exit codes:

  0 — full clean (every signed asset either verifies, is a documented
      placeholder, or is on the v0.2-reconciliation allowlist)
  1 — at least one unexpected verification failure
  2 — verifier internal error (file missing, parse error, pubkey hex bad)

Usage::

    python pipeline/scripts/verify_signed_assets.py [--verbose] [--dry-run]

"""

from __future__ import annotations

import argparse
import copy
import dataclasses
import hashlib
import json
import logging
import pathlib
import sys
from typing import Any

import yaml
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

# ─── repo layout ────────────────────────────────────────────────────────────
BASE = pathlib.Path(__file__).resolve().parent.parent.parent

CARDS_PUBKEY_YAML = BASE / "vault_shared" / "cards" / "publisher_pubkey.signed.yaml"
FID_PUBKEY_YAML = (
    BASE / "vault_shared" / "funder_intelligence" / "publisher_pubkey.signed.yaml"
)
OPERATOR_ATTESTATION_PUBKEY_YAML = (
    BASE / "vault_shared" / "operator_attestation" / "publisher_pubkey.signed.yaml"
)
PRP_PUBKEY_YAML = (
    BASE / "vault_shared" / "program_rule_packs" / "publisher_pubkey.signed.yaml"
)
REFLECTION_PACKET_PUBKEY_YAML = (
    BASE / "vault_shared" / "reflection_packet" / "producer_pubkey.signed.yaml"
)
WPFA_PUBKEY_YAML = BASE / "vault_shared" / "wpfa" / "sn_llc_pubkey.signed.yaml"

LOCK_HISTORY = BASE / "pipeline" / "engineering" / "lock_history.v1.jsonl"
CARDS_CIC_DIR = BASE / "pipeline" / "cards" / "CIC"
CARDS_CLC_DIR = BASE / "pipeline" / "cards" / "CLC"
DEFERRED_ALLOWLIST = (
    BASE / "pipeline" / "scripts" / "signature_verification_deferred.yaml"
)

# Cards-publisher pubkeys. The CURRENT pubkey is loaded from the signed YAML
# at runtime; the RETIRED pubkey is pinned here as a constant so the verifier
# can validate historical rows and CROSS-CHECK it against the
# ``old_pubkey_ed25519_hex`` field of the row-280 key_rotation event (drift
# detection — if the rotation row's recorded old pubkey diverges from this
# constant, something is wrong).
RETIRED_CARDS_PUBKEY_HEX = (
    "0b1a0bbfa5ee9149af2c4e6153ed037dd03c0d562c94d3eaefeaf798e6f375bd"
)
EXPECTED_CURRENT_CARDS_PUBKEY_HEX = (
    "c93f1881cbb7ff315b29f416c2f8bc16dc9e1d1576e743f63e577de992e41107"
)

# ─── logging ───────────────────────────────────────────────────────────────
log = logging.getLogger("verify_signed_assets")


# ─── canonical-bytes recipes (mirror existing ceremony scripts byte-for-byte) ─
def yaml_canonical_bytes(data: dict) -> bytes:
    """Cards-publisher self-signed-asset recipe.

    Mirrors ``pipeline/scripts/cards_publisher_key_rotation_ceremony_2026-05-17.py
    ::yaml_canonical_bytes``. ``data`` MUST already have
    ``publisher_signature_ed25519_hex`` AND ``canonical_bytes_sha3_512_hex``
    removed.
    """

    return yaml.safe_dump(data, sort_keys=True, default_flow_style=False).encode(
        "utf-8"
    )


def json_canonical_bytes(data: dict) -> bytes:
    """FID + operator-attestation self-signed-asset recipe.

    Mirrors the file-documented "Path 2" algorithm in
    ``vault_shared/funder_intelligence/publisher_pubkey.signed.yaml`` and
    ``vault_shared/operator_attestation/publisher_pubkey.signed.yaml``. ``data``
    MUST already have ``publisher_signature_ed25519_hex`` AND
    ``canonical_bytes_sha3_512_hex`` removed.
    """

    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def row_canonical_bytes(row: dict) -> bytes:
    """Lock_history-row recipe.

    Mirrors ``pipeline/scripts/cards_publisher_key_rotation_ceremony_2026-05-17.py
    ::row_canonical_bytes`` and ``pipeline/scripts/cards_embedded_re_sign_
    ceremony_2026-05-18.py::row_canonical_bytes``.
    """

    payload = dict(row)
    payload.pop("ed25519_signature", None)
    payload.pop("canonical_json_sha3_512", None)
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def card_canonical_bytes(card_body: dict) -> bytes:
    """Card embedded-signature recipe.

    Mirrors ``pipeline/cards/loader.py::canonical_bytes`` and
    ``pipeline/scripts/cards_embedded_re_sign_ceremony_2026-05-18.py::
    card_canonical_bytes``.
    """

    normalized = copy.deepcopy(dict(card_body))
    lifecycle = normalized.get("lifecycle")
    if isinstance(lifecycle, dict):
        lifecycle.pop("signature_status", None)
        lifecycle.pop("content_hash", None)
    research_metadata = normalized.get("_research_metadata")
    if isinstance(research_metadata, dict):
        research_metadata.pop("ed25519_signature", None)
    return json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


# ─── result accounting ─────────────────────────────────────────────────────
@dataclasses.dataclass
class Result:
    asset_id: str
    asset_kind: str
    status: str  # VERIFIED / DEFERRED_V0_2 / PLACEHOLDER / FAIL / INTERNAL_ERROR
    detail: str = ""

    def is_failure(self) -> bool:
        return self.status in ("FAIL", "INTERNAL_ERROR")


def _looks_like_placeholder(hex_or_value: str) -> bool:
    """Recognize a stub/placeholder pubkey or signature."""

    if hex_or_value == "" or hex_or_value is None:
        return True
    if hex_or_value.startswith("<PENDING"):
        return True
    if isinstance(hex_or_value, str) and len(hex_or_value) >= 8 and set(
        hex_or_value
    ) == {"0"}:
        return True
    return False


# ─── allowlist for documented-stale assets (v0.2 reconciliation deferred) ──
def load_deferred_allowlist() -> dict[str, Any]:
    """Load the checked-in v0.2-reconciliation allowlist.

    Format::

      lock_history_rows:
        - row: <declared row number>
          reason: <free text>
      card_embedded_signatures:
        - path: <repo-relative path to card YAML>
          reason: <free text>
    """

    if not DEFERRED_ALLOWLIST.exists():
        return {"lock_history_rows": [], "card_embedded_signatures": []}
    with DEFERRED_ALLOWLIST.open() as fh:
        data = yaml.safe_load(fh) or {}
    data.setdefault("lock_history_rows", [])
    data.setdefault("card_embedded_signatures", [])
    return data


# ─── pubkey loaders ────────────────────────────────────────────────────────
def load_current_cards_pubkey() -> tuple[Ed25519PublicKey, str]:
    """Load the current cards publisher pubkey from the pinned YAML asset."""

    with CARDS_PUBKEY_YAML.open() as fh:
        data = yaml.safe_load(fh)
    pubkey_hex = data["publisher_pubkey_ed25519_hex"]
    if pubkey_hex != EXPECTED_CURRENT_CARDS_PUBKEY_HEX:
        raise RuntimeError(
            f"cards publisher pubkey drift: pinned YAML carries "
            f"{pubkey_hex[:16]}... but verifier expected "
            f"{EXPECTED_CURRENT_CARDS_PUBKEY_HEX[:16]}..."
        )
    return Ed25519PublicKey.from_public_bytes(bytes.fromhex(pubkey_hex)), pubkey_hex


def load_retired_cards_pubkey() -> tuple[Ed25519PublicKey, str]:
    """Load the retired cards publisher pubkey + cross-check it against the
    row-280 key_rotation event ``old_pubkey_ed25519_hex`` field."""

    with LOCK_HISTORY.open() as fh:
        rows = [json.loads(line) for line in fh if line.strip()]
    rotation_rows = [
        r for r in rows if r.get("row") == 280 and r.get("lock_class") == "key_rotation"
    ]
    if not rotation_rows:
        raise RuntimeError(
            "expected exactly 1 key_rotation row at declared row 280; found 0 — "
            "verifier cannot cross-check retired pubkey"
        )
    rotation_row = rotation_rows[0]
    declared_old = rotation_row.get("old_pubkey_ed25519_hex")
    if declared_old != RETIRED_CARDS_PUBKEY_HEX:
        raise RuntimeError(
            f"retired cards pubkey drift: row-280 key_rotation event records "
            f"old_pubkey_ed25519_hex={declared_old[:16]}... but verifier "
            f"expected {RETIRED_CARDS_PUBKEY_HEX[:16]}..."
        )
    return (
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(RETIRED_CARDS_PUBKEY_HEX)),
        RETIRED_CARDS_PUBKEY_HEX,
    )


# ─── per-asset verifiers ───────────────────────────────────────────────────
def verify_pubkey_yaml(
    *, path: pathlib.Path, canonicalizer, label: str
) -> Result:
    """Verify a publisher/producer pubkey YAML self-signs."""

    with path.open() as fh:
        data = yaml.safe_load(fh)
    rel = path.relative_to(BASE).as_posix()

    pubkey_hex = data.get(
        "publisher_pubkey_ed25519_hex"
    ) or data.get("producer_pubkey_ed25519_hex") or data.get("pubkey_hex", "")
    sig_hex = data.get("publisher_signature_ed25519_hex") or data.get(
        "pinned_by_operator_ed25519", ""
    )
    hash_hex = data.get("canonical_bytes_sha3_512_hex", "")

    if (
        _looks_like_placeholder(pubkey_hex)
        and _looks_like_placeholder(sig_hex)
        and _looks_like_placeholder(hash_hex)
    ):
        return Result(
            asset_id=rel,
            asset_kind="pubkey_yaml",
            status="PLACEHOLDER",
            detail=f"{label}: pubkey/sig/hash fields are placeholders",
        )

    # Mixed-placeholder state: e.g., real pubkey but no signature, or any
    # subset. Hard-fail — the asset is mid-ceremony and CI should catch.
    if (
        _looks_like_placeholder(pubkey_hex)
        or _looks_like_placeholder(sig_hex)
        or _looks_like_placeholder(hash_hex)
    ):
        return Result(
            asset_id=rel,
            asset_kind="pubkey_yaml",
            status="FAIL",
            detail=(
                f"{label}: mixed placeholder/real fields "
                f"(pubkey={'placeholder' if _looks_like_placeholder(pubkey_hex) else 'real'}, "
                f"sig={'placeholder' if _looks_like_placeholder(sig_hex) else 'real'}, "
                f"hash={'placeholder' if _looks_like_placeholder(hash_hex) else 'real'}) "
                "— complete the ceremony or revert to a full-placeholder stub"
            ),
        )

    clone = copy.deepcopy(data)
    clone.pop("publisher_signature_ed25519_hex", None)
    clone.pop("canonical_bytes_sha3_512_hex", None)
    canon = canonicalizer(clone)
    recomputed_hash = hashlib.sha3_512(canon).hexdigest()
    if recomputed_hash != hash_hex:
        return Result(
            asset_id=rel,
            asset_kind="pubkey_yaml",
            status="FAIL",
            detail=(
                f"{label}: canonical_bytes_sha3_512_hex mismatch "
                f"(declared={hash_hex[:16]}... recomputed={recomputed_hash[:16]}...)"
            ),
        )
    try:
        pk = Ed25519PublicKey.from_public_bytes(bytes.fromhex(pubkey_hex))
        pk.verify(bytes.fromhex(sig_hex), canon)
    except (InvalidSignature, ValueError) as exc:
        return Result(
            asset_id=rel,
            asset_kind="pubkey_yaml",
            status="FAIL",
            detail=f"{label}: self-signature verify failed: {exc!s}",
        )
    return Result(
        asset_id=rel,
        asset_kind="pubkey_yaml",
        status="VERIFIED",
        detail=f"{label}: TOFU self-sign OK ({pubkey_hex[:16]}...)",
    )


def verify_lock_history_rows(
    *,
    current_pk: Ed25519PublicKey,
    current_pubkey_hex: str,
    retired_pk: Ed25519PublicKey,
    retired_pubkey_hex: str,
    deferred_rows: set,
    verbose: bool,
) -> list[Result]:
    """Verify every signed row in lock_history.v1.jsonl."""

    with LOCK_HISTORY.open() as fh:
        rows = [json.loads(line) for line in fh if line.strip()]

    results: list[Result] = []
    for idx, row in enumerate(rows, start=1):
        sig_hex = row.get("ed25519_signature")
        if not sig_hex:
            continue
        declared_row = row.get("row")
        declared_pubkey = row.get("publisher_pubkey_ed25519_hex")
        lock_class = row.get("lock_class")
        module = (
            row.get("module")
            or row.get("cartridge_slug")
            or row.get("blueprint_section", "")
        )
        asset_id = f"lock_history.v1.jsonl row={declared_row}"

        # Cross-check: declared pubkey must be one of the two we trust.
        if declared_pubkey == current_pubkey_hex:
            pk = current_pk
            pk_label = "current"
        elif declared_pubkey == retired_pubkey_hex:
            pk = retired_pk
            pk_label = "retired"
        else:
            results.append(
                Result(
                    asset_id=asset_id,
                    asset_kind="lock_history_row",
                    status="FAIL",
                    detail=(
                        f"row {declared_row} ({lock_class}, {module}) declares "
                        f"publisher_pubkey_ed25519_hex={(declared_pubkey or '<none>')[:16]}... "
                        f"which is neither the current nor the retired cards "
                        f"publisher pubkey"
                    ),
                )
            )
            continue

        canon = row_canonical_bytes(row)
        declared_hash = row.get("canonical_json_sha3_512")
        recomputed_hash = hashlib.sha3_512(canon).hexdigest()
        hash_ok = (recomputed_hash == declared_hash) if declared_hash else None
        try:
            pk.verify(bytes.fromhex(sig_hex), canon)
            sig_ok = True
            sig_err = ""
        except InvalidSignature as exc:
            sig_ok = False
            sig_err = str(exc) or "invalid signature"
        except ValueError as exc:
            sig_ok = False
            sig_err = f"signature hex parse error: {exc}"

        if sig_ok and hash_ok:
            if verbose:
                log.info(
                    "  VERIFIED row=%s lock_class=%s pubkey=%s",
                    declared_row,
                    lock_class,
                    pk_label,
                )
            results.append(
                Result(
                    asset_id=asset_id,
                    asset_kind="lock_history_row",
                    status="VERIFIED",
                    detail=f"{lock_class} signed by {pk_label} pubkey",
                )
            )
            continue

        # Failure path — consult deferred allowlist.
        if declared_row in deferred_rows:
            results.append(
                Result(
                    asset_id=asset_id,
                    asset_kind="lock_history_row",
                    status="DEFERRED_V0_2",
                    detail=(
                        f"row {declared_row} ({lock_class}, {module}) — "
                        f"on v0.2-reconciliation allowlist "
                        f"(hash_ok={hash_ok}, sig_ok={sig_ok}, "
                        f"sig_err={sig_err}); per "
                        f"signature_verification_deferred.yaml"
                    ),
                )
            )
            continue

        results.append(
            Result(
                asset_id=asset_id,
                asset_kind="lock_history_row",
                status="FAIL",
                detail=(
                    f"row {declared_row} ({lock_class}, {module}) signed by "
                    f"{pk_label} pubkey but verify failed "
                    f"(hash_ok={hash_ok}, sig_ok={sig_ok}, sig_err={sig_err})"
                ),
            )
        )

    return results


def verify_card_yaml(
    *,
    path: pathlib.Path,
    cards_pk: Ed25519PublicKey,
    deferred_card_paths: set,
    verbose: bool,
) -> list[Result]:
    """Verify a card YAML: content_hash recompute + embedded signature attempt."""

    rel = path.relative_to(BASE).as_posix()
    results: list[Result] = []
    with path.open() as fh:
        body = yaml.safe_load(fh)

    canon = card_canonical_bytes(body)
    recomputed_content_hash = "sha256:" + hashlib.sha256(canon).hexdigest()
    declared_content_hash = (body.get("lifecycle") or {}).get("content_hash", "")

    if recomputed_content_hash != declared_content_hash:
        results.append(
            Result(
                asset_id=rel,
                asset_kind="card_content_hash",
                status="FAIL",
                detail=(
                    f"{rel}: lifecycle.content_hash drift "
                    f"(declared={declared_content_hash[:24]}... "
                    f"recomputed={recomputed_content_hash[:24]}...) — "
                    f"this would also fail loader.enforce_lifecycle_truth"
                ),
            )
        )
    else:
        results.append(
            Result(
                asset_id=rel,
                asset_kind="card_content_hash",
                status="VERIFIED",
                detail=f"{rel}: content_hash matches canonical_bytes_sha256",
            )
        )

    sig_hex = (body.get("_research_metadata") or {}).get("ed25519_signature", "")
    if not sig_hex:
        results.append(
            Result(
                asset_id=rel,
                asset_kind="card_embedded_signature",
                status="FAIL",
                detail=f"{rel}: missing _research_metadata.ed25519_signature",
            )
        )
        return results
    try:
        cards_pk.verify(bytes.fromhex(sig_hex), canon)
        sig_ok = True
        sig_err = ""
    except InvalidSignature as exc:
        sig_ok = False
        sig_err = str(exc) or "invalid signature"
    except ValueError as exc:
        sig_ok = False
        sig_err = f"signature hex parse error: {exc}"

    if sig_ok:
        if verbose:
            log.info("  VERIFIED %s embedded signature (current pubkey)", rel)
        results.append(
            Result(
                asset_id=rel,
                asset_kind="card_embedded_signature",
                status="VERIFIED",
                detail=f"{rel}: embedded ed25519_signature verifies under current pubkey",
            )
        )
        return results

    if rel in deferred_card_paths:
        results.append(
            Result(
                asset_id=rel,
                asset_kind="card_embedded_signature",
                status="DEFERRED_V0_2",
                detail=(
                    f"{rel}: embedded signature does not verify (expected per "
                    f"signature_verification_deferred.yaml — Wave-1 cards "
                    f"deferred to v0.2 first-wave loader-realization). "
                    f"Authoritative provenance lives in lock_history "
                    f"card_cartridge_supersession rows under the current "
                    f"pubkey. sig_err={sig_err}"
                ),
            )
        )
        return results

    results.append(
        Result(
            asset_id=rel,
            asset_kind="card_embedded_signature",
            status="FAIL",
            detail=(
                f"{rel}: embedded signature verify failed and card is not on "
                f"the v0.2-reconciliation allowlist. sig_err={sig_err}"
            ),
        )
    )
    return results


# ─── orchestration ─────────────────────────────────────────────────────────
def collect_assets() -> dict[str, list[str]]:
    """Inventory the assets the verifier would touch (used by --dry-run)."""

    cic = sorted(p.relative_to(BASE).as_posix() for p in CARDS_CIC_DIR.glob("*.yaml"))
    clc = sorted(p.relative_to(BASE).as_posix() for p in CARDS_CLC_DIR.glob("*.yaml"))
    signed_rows = 0
    if LOCK_HISTORY.exists():
        with LOCK_HISTORY.open() as fh:
            for line in fh:
                if not line.strip():
                    continue
                row = json.loads(line)
                if row.get("ed25519_signature"):
                    signed_rows += 1
    return {
        "pubkey_yamls": [
            CARDS_PUBKEY_YAML.relative_to(BASE).as_posix(),
            FID_PUBKEY_YAML.relative_to(BASE).as_posix(),
            OPERATOR_ATTESTATION_PUBKEY_YAML.relative_to(BASE).as_posix(),
            PRP_PUBKEY_YAML.relative_to(BASE).as_posix(),
            REFLECTION_PACKET_PUBKEY_YAML.relative_to(BASE).as_posix(),
            WPFA_PUBKEY_YAML.relative_to(BASE).as_posix(),
        ],
        "lock_history_signed_rows": [str(signed_rows)],
        "card_yamls_cic": cic,
        "card_yamls_clc": clc,
    }


def run(*, dry_run: bool, verbose: bool) -> int:
    if verbose:
        logging.basicConfig(level=logging.INFO, format="%(message)s")
    else:
        logging.basicConfig(level=logging.WARNING, format="%(message)s")

    inv = collect_assets()
    log.warning("Signature round-trip verifier — repo=%s", BASE)
    log.warning(
        "Inventory: %d pubkey YAMLs, %s signed lock_history rows, %d CIC cards, %d CLC cards",
        len(inv["pubkey_yamls"]),
        inv["lock_history_signed_rows"][0],
        len(inv["card_yamls_cic"]),
        len(inv["card_yamls_clc"]),
    )

    if dry_run:
        log.warning("--dry-run: listing assets, skipping verification")
        for kind, items in inv.items():
            log.warning("  %s:", kind)
            for it in items:
                log.warning("    %s", it)
        return 0

    try:
        current_pk, current_pk_hex = load_current_cards_pubkey()
        retired_pk, retired_pk_hex = load_retired_cards_pubkey()
    except Exception as exc:
        log.error("INTERNAL_ERROR loading cards pubkey set: %s", exc)
        return 2

    allowlist = load_deferred_allowlist()
    deferred_rows = {
        int(entry["row"]) for entry in allowlist.get("lock_history_rows", [])
    }
    deferred_card_paths = {
        entry["path"] for entry in allowlist.get("card_embedded_signatures", [])
    }
    log.warning(
        "Allowlist: %d lock_history rows + %d card embedded sigs deferred to v0.2",
        len(deferred_rows),
        len(deferred_card_paths),
    )

    results: list[Result] = []

    # 1. Pubkey YAMLs.
    results.append(
        verify_pubkey_yaml(
            path=CARDS_PUBKEY_YAML,
            canonicalizer=yaml_canonical_bytes,
            label="cards-publisher",
        )
    )
    results.append(
        verify_pubkey_yaml(
            path=FID_PUBKEY_YAML,
            canonicalizer=json_canonical_bytes,
            label="FID-publisher",
        )
    )
    results.append(
        verify_pubkey_yaml(
            path=OPERATOR_ATTESTATION_PUBKEY_YAML,
            canonicalizer=json_canonical_bytes,
            label="operator-attestation",
        )
    )
    for path, label in (
        (PRP_PUBKEY_YAML, "PRP-publisher"),
        (REFLECTION_PACKET_PUBKEY_YAML, "reflection-packet-producer"),
        (WPFA_PUBKEY_YAML, "WPFA-SN-LLC"),
    ):
        # These three are documented placeholders — but we still feed them
        # through the verifier so we trip if a future commit accidentally
        # leaves them in a half-real state.
        results.append(
            verify_pubkey_yaml(
                path=path,
                canonicalizer=json_canonical_bytes,
                label=label,
            )
        )

    # 2. lock_history rows.
    results.extend(
        verify_lock_history_rows(
            current_pk=current_pk,
            current_pubkey_hex=current_pk_hex,
            retired_pk=retired_pk,
            retired_pubkey_hex=retired_pk_hex,
            deferred_rows=deferred_rows,
            verbose=verbose,
        )
    )

    # 3. Card YAMLs.
    for path in sorted(CARDS_CIC_DIR.glob("*.yaml")) + sorted(
        CARDS_CLC_DIR.glob("*.yaml")
    ):
        results.extend(
            verify_card_yaml(
                path=path,
                cards_pk=current_pk,
                deferred_card_paths=deferred_card_paths,
                verbose=verbose,
            )
        )

    # ─── tally + report ──────────────────────────────────────────────────
    by_status: dict[str, int] = {}
    by_kind_status: dict[tuple[str, str], int] = {}
    for r in results:
        by_status[r.status] = by_status.get(r.status, 0) + 1
        key = (r.asset_kind, r.status)
        by_kind_status[key] = by_kind_status.get(key, 0) + 1

    log.warning("")
    log.warning("=== Verification summary ===")
    log.warning(
        "Total: %d  |  VERIFIED: %d  DEFERRED_V0_2: %d  PLACEHOLDER: %d  FAIL: %d",
        len(results),
        by_status.get("VERIFIED", 0),
        by_status.get("DEFERRED_V0_2", 0),
        by_status.get("PLACEHOLDER", 0),
        by_status.get("FAIL", 0),
    )
    for (kind, status), count in sorted(by_kind_status.items()):
        log.warning("  %-30s %-16s %d", kind, status, count)

    fails = [r for r in results if r.is_failure()]
    if fails:
        log.warning("")
        log.warning("=== FAILURES ===")
        for r in fails:
            log.warning("  [%s] %s — %s", r.status, r.asset_id, r.detail)
        return 1

    if verbose:
        log.warning("")
        log.warning("=== DEFERRED / PLACEHOLDER detail ===")
        for r in results:
            if r.status in ("DEFERRED_V0_2", "PLACEHOLDER"):
                log.warning("  [%s] %s — %s", r.status, r.asset_id, r.detail)

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="list assets without performing verification",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="per-asset progress logging",
    )
    args = parser.parse_args(argv)
    return run(dry_run=args.dry_run, verbose=args.verbose)


if __name__ == "__main__":
    sys.exit(main())
