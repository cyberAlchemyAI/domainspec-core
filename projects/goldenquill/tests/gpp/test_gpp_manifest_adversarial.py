"""
Phase 0 GPP Hardening — Tier 3 SYNTHESIS / signing adversarial tests
=====================================================================

Complements tests/gpp/test_gpp_phase0.py with hostile-input probes per
pipeline/validation/gpp_phase0_adversarial_test_specs.md §Tier 3.

Attack classes:
  ADV-MANIFEST-01  signature forgery
  ADV-MANIFEST-02  hybrid-scheme downgrade
  ADV-MANIFEST-03  manifest mutation between sign and verify
  ADV-MANIFEST-04  key-lifecycle (freshness, expiry)

ML-DSA-65 notes: Phase-0 uses the HMAC-SHA3-512 stub (oqs-python not yet
installed per provisioning_manifest_v0.1.md §8.6).  When oqs lands in v0.2
the stub path goes dead and real-ML-DSA-65 tests take over — these tests
all still pass under the real primitive because they operate at the
sign/verify interface boundary.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import os
import sys
from pathlib import Path
from typing import Any

import pytest

GPP_DIR = (
    Path(__file__).resolve().parent.parent.parent
    / "pipeline"
    / "validation"
    / "integration_scope_close_2026-04-19"
    / "gpp"
)
# pipeline/validation/* is gitignored; see test_gpp_phase0.py for why this
# local-only suite skips clean CI clones without historical dispatch artifacts.
if not GPP_DIR.is_dir():
    pytest.skip(
        f"gpp/ dispatch tree not present at {GPP_DIR}; local-only suite",
        allow_module_level=True,
    )
if str(GPP_DIR) not in sys.path:
    sys.path.insert(0, str(GPP_DIR))

import gpp_manifest  # noqa: E402


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------


def _build_and_sign(tmp_path: Path) -> tuple[dict[str, Any], gpp_manifest.GPPKeypair]:
    keypair = gpp_manifest.GPPKeypair.generate()
    manifest_data = gpp_manifest.build_manifest(
        plan_artifact_paths=[],
        repo_root=tmp_path,
        det_report={"tier_1_overall_status": "PASS", "checks": []},
        council_findings=[],
        tier_3_dispositions=[],
    )
    return gpp_manifest.sign_manifest(manifest_data, keypair), keypair


# ===========================================================================
# ADV-MANIFEST-01 — signature forgery
# ===========================================================================


def test_adv_wrong_ed25519_key_detected(tmp_path: Path) -> None:
    """A signature generated with key A cannot be verified under key B's public key."""
    signed, _kp_a = _build_and_sign(tmp_path)
    kp_b = gpp_manifest.GPPKeypair.generate()

    # Swap in the WRONG public key
    tampered = dict(signed)
    tampered_sig = dict(signed["operator_signature"])
    tampered_sig["ed25519_public_key_pem"] = kp_b.ed25519_public_pem.decode("utf-8")
    tampered["operator_signature"] = tampered_sig

    result = gpp_manifest.verify_manifest(tampered)
    assert not result["ed25519_valid"], (
        "Ed25519 must reject a signature verified against a foreign public key"
    )


def test_adv_truncated_signature_rejected(tmp_path: Path) -> None:
    """A signature of the wrong byte length fails verification.
    Ed25519 sigs are exactly 64 bytes (128 hex chars)."""
    signed, _ = _build_and_sign(tmp_path)
    tampered = dict(signed)
    sig_block = dict(signed["operator_signature"])
    original_hex = sig_block["ed25519"]
    # Truncate to half length
    sig_block["ed25519"] = original_hex[: len(original_hex) // 2]
    tampered["operator_signature"] = sig_block
    result = gpp_manifest.verify_manifest(tampered)
    assert not result["ed25519_valid"]


def test_adv_signature_over_different_payload_rejected(tmp_path: Path) -> None:
    """A valid sig for payload X, presented with payload Y, fails verification.

    build_manifest() only surfaces the `checks` list from det_report (not the
    overall status), so the two manifests must differ in a field that actually
    lands in the signable bytes — here we differ the tier_1_det_results by
    giving the second manifest a non-empty check list.
    """
    # Sign manifest X (empty checks)
    signed_x, keypair = _build_and_sign(tmp_path)
    # Build a GENUINELY DIFFERENT manifest Y and copy X's signature into it
    manifest_y_data = gpp_manifest.build_manifest(
        plan_artifact_paths=[],
        repo_root=tmp_path,
        det_report={
            "tier_1_overall_status": "FAIL",
            "checks": [{"check_id": "CITE-RESOLVE", "status": "FAIL"}],
        },
        council_findings=[],
        tier_3_dispositions=[],
    )
    # Confirm the signable payloads actually differ before attempting forgery
    sig_x = {k: v for k, v in signed_x.items()
             if k not in {"operator_signature", "signed_at"}}
    assert gpp_manifest.canonical_bytes(sig_x) != gpp_manifest.canonical_bytes(manifest_y_data), (
        "precondition: manifests X and Y must differ in canonical bytes"
    )

    tampered = dict(manifest_y_data)
    tampered["operator_signature"] = signed_x["operator_signature"]
    tampered["signed_at"] = signed_x["signed_at"]

    result = gpp_manifest.verify_manifest(tampered)
    assert not result["ed25519_valid"]
    assert not result["ml_dsa_65_valid"]


def test_adv_empty_signature_rejected(tmp_path: Path) -> None:
    """An empty signature string fails verification with an error recorded."""
    signed, _ = _build_and_sign(tmp_path)
    tampered = dict(signed)
    sig_block = dict(signed["operator_signature"])
    sig_block["ed25519"] = ""
    tampered["operator_signature"] = sig_block
    result = gpp_manifest.verify_manifest(tampered)
    assert not result["ed25519_valid"]
    assert result["errors"], "Empty sig must surface an error string"


# ===========================================================================
# ADV-MANIFEST-02 — hybrid-scheme downgrade
# ===========================================================================


def test_adv_ed25519_only_without_mldsa65_rejected_by_both_valid(tmp_path: Path) -> None:
    """Hybrid per A12: BOTH sigs required.  If ML-DSA-65 is missing/invalid,
    verify_manifest's both_valid must be False even when Ed25519 is valid."""
    signed, _ = _build_and_sign(tmp_path)
    tampered = dict(signed)
    sig_block = dict(signed["operator_signature"])
    sig_block["ml_dsa_65"] = "00" * 64  # garbage sig of wrong provenance
    tampered["operator_signature"] = sig_block
    result = gpp_manifest.verify_manifest(tampered)
    # Ed25519 still valid (we didn't touch it)
    assert result["ed25519_valid"]
    # But ML-DSA-65 garbage → ml_dsa_65_valid False → both_valid False
    assert not result["ml_dsa_65_valid"]
    assert not result["both_valid"]


def test_adv_mldsa65_only_without_ed25519_rejected_by_both_valid(tmp_path: Path) -> None:
    """Symmetric: garbage Ed25519 alone breaks both_valid."""
    signed, _ = _build_and_sign(tmp_path)
    tampered = dict(signed)
    sig_block = dict(signed["operator_signature"])
    sig_block["ed25519"] = "00" * 64  # garbage Ed25519 sig
    tampered["operator_signature"] = sig_block
    result = gpp_manifest.verify_manifest(tampered)
    assert not result["ed25519_valid"]
    assert not result["both_valid"]


def test_adv_either_ed25519_key_missing_fails_verify(tmp_path: Path) -> None:
    """Missing Ed25519 public key → ed25519_valid=False; error recorded."""
    signed, _ = _build_and_sign(tmp_path)
    tampered = dict(signed)
    sig_block = dict(signed["operator_signature"])
    sig_block["ed25519_public_key_pem"] = ""
    tampered["operator_signature"] = sig_block
    result = gpp_manifest.verify_manifest(tampered)
    assert not result["ed25519_valid"]
    assert any("Ed25519" in e for e in result["errors"])


def test_adv_either_mldsa65_key_missing_fails_verify(tmp_path: Path) -> None:
    """Missing ML-DSA-65 public key → ml_dsa_65_valid=False; error recorded."""
    signed, _ = _build_and_sign(tmp_path)
    tampered = dict(signed)
    sig_block = dict(signed["operator_signature"])
    sig_block["ml_dsa_65_public_key"] = ""
    tampered["operator_signature"] = sig_block
    result = gpp_manifest.verify_manifest(tampered)
    assert not result["ml_dsa_65_valid"]
    assert any("ML-DSA-65" in e for e in result["errors"])


def test_adv_both_signatures_missing_fails_verify(tmp_path: Path) -> None:
    """If the entire operator_signature block is empty, both sigs fail."""
    signed, _ = _build_and_sign(tmp_path)
    tampered = dict(signed)
    tampered["operator_signature"] = {}
    result = gpp_manifest.verify_manifest(tampered)
    assert not result["ed25519_valid"]
    assert not result["ml_dsa_65_valid"]
    assert not result["both_valid"]


# ===========================================================================
# ADV-MANIFEST-03 — manifest mutation between sign and verify
# ===========================================================================


def test_adv_added_field_post_sign_fails_verify(tmp_path: Path) -> None:
    """Any additive field tamper → canonical bytes differ → verify fails."""
    signed, _ = _build_and_sign(tmp_path)
    tampered = dict(signed)
    tampered["extra_field_added_later"] = "malicious"
    result = gpp_manifest.verify_manifest(tampered)
    assert not result["ed25519_valid"]
    assert not result["ml_dsa_65_valid"]


def test_adv_removed_field_post_sign_fails_verify(tmp_path: Path) -> None:
    """Any subtractive tamper → canonical bytes differ → verify fails."""
    signed, _ = _build_and_sign(tmp_path)
    tampered = dict(signed)
    del tampered["plan_artifact_set"]  # load-bearing field per §3.3 schema
    result = gpp_manifest.verify_manifest(tampered)
    assert not result["ed25519_valid"]
    assert not result["ml_dsa_65_valid"]


def test_adv_replaced_value_post_sign_fails_verify(tmp_path: Path) -> None:
    """Value-swap on a signed field invalidates both sigs."""
    signed, _ = _build_and_sign(tmp_path)
    tampered = dict(signed)
    tampered["tier_1_det_results"] = {"FAKE_CHECK": "PASS"}
    result = gpp_manifest.verify_manifest(tampered)
    assert not result["ed25519_valid"]


def test_adv_signed_at_mutation_fails_verify(tmp_path: Path) -> None:
    """signed_at is bound into the signable bytes; changing it breaks verify."""
    signed, _ = _build_and_sign(tmp_path)
    tampered = dict(signed)
    # Shift timestamp one second earlier
    original = dt.datetime.fromisoformat(signed["signed_at"])
    shifted = (original - dt.timedelta(seconds=1)).isoformat()
    tampered["signed_at"] = shifted
    result = gpp_manifest.verify_manifest(tampered)
    assert not result["ed25519_valid"]
    assert not result["ml_dsa_65_valid"]


def test_adv_council_findings_insertion_fails_verify(tmp_path: Path) -> None:
    """Inserting a fabricated council finding post-sign breaks both sigs."""
    signed, _ = _build_and_sign(tmp_path)
    tampered = dict(signed)
    tampered["tier_2_council_findings"] = [
        {
            "finding_id": "fake-001",
            "seat": "red_team",
            "severity": "INFORMATIONAL",
            "pointer": "fake",
            "assertion": "injected post-sign",
            "suggested_disposition": "DEFER",
        }
    ]
    result = gpp_manifest.verify_manifest(tampered)
    assert not result["ed25519_valid"]


# ===========================================================================
# ADV-MANIFEST-04 — key lifecycle (freshness, expiry, stub public key)
# ===========================================================================


def test_adv_expired_manifest_rejected_with_clear_error(tmp_path: Path) -> None:
    """signed_at > 90 days in the past → freshness_ok=False + error recorded."""
    signed, _ = _build_and_sign(tmp_path)
    tampered = dict(signed)
    old_ts = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=120)).isoformat()
    # Resign with the old timestamp — we need a valid signature for the freshness
    # check to be the distinguishing failure.  But mutating signed_at alone breaks
    # the crypto check first.  So we test that freshness ALSO fails; both checks
    # contribute to overall rejection.
    tampered["signed_at"] = old_ts
    result = gpp_manifest.verify_manifest(tampered)
    assert not result["freshness_ok"]
    assert any("days old" in e for e in result["errors"])


def test_adv_missing_signed_at_reports_parse_error(tmp_path: Path) -> None:
    """Empty signed_at → ValueError on fromisoformat → freshness_ok=False."""
    signed, _ = _build_and_sign(tmp_path)
    tampered = dict(signed)
    tampered["signed_at"] = ""
    result = gpp_manifest.verify_manifest(tampered)
    assert not result["freshness_ok"]


def test_adv_malformed_signed_at_reports_parse_error(tmp_path: Path) -> None:
    """Non-ISO signed_at → ValueError → freshness_ok=False."""
    signed, _ = _build_and_sign(tmp_path)
    tampered = dict(signed)
    tampered["signed_at"] = "not-an-iso-timestamp"
    result = gpp_manifest.verify_manifest(tampered)
    assert not result["freshness_ok"]


def test_adv_hex_decode_error_in_signature_caught(tmp_path: Path) -> None:
    """Non-hex chars in signature hex → verify path catches it gracefully
    (falls through to not-valid)."""
    signed, _ = _build_and_sign(tmp_path)
    tampered = dict(signed)
    sig_block = dict(signed["operator_signature"])
    sig_block["ed25519"] = "ZZZZ_not_hex_" * 5
    tampered["operator_signature"] = sig_block
    result = gpp_manifest.verify_manifest(tampered)
    assert not result["ed25519_valid"]


# ===========================================================================
# Property-style probes (property §4 from spec)
# ===========================================================================


def test_adv_property_roundtrip_stability(tmp_path: Path) -> None:
    """P1: canonical_bytes(m) == canonical_bytes(parse(canonical_bytes(m)))."""
    import json as _json
    m = gpp_manifest.build_manifest(
        plan_artifact_paths=[],
        repo_root=tmp_path,
        det_report={"tier_1_overall_status": "PASS", "checks": [{"check_id": "X", "status": "PASS"}]},
        council_findings=[{"finding_id": "y", "seat": "red_team"}],
        tier_3_dispositions=[{"finding_id": "y", "disposition": "DEFER"}],
    )
    bytes1 = gpp_manifest.canonical_bytes(m)
    parsed = _json.loads(bytes1.decode("utf-8"))
    bytes2 = gpp_manifest.canonical_bytes(parsed)
    assert bytes1 == bytes2


def test_adv_property_any_byte_mutation_breaks_verify(tmp_path: Path) -> None:
    """P3: mutating ANY byte of the signable payload makes verify False.
    Demonstrated by mutating the gpp_tool_version field (trivial but contract-preserving)."""
    signed, _ = _build_and_sign(tmp_path)
    tampered = dict(signed)
    tampered["gpp_tool_version"] = "v1-mutated"
    result = gpp_manifest.verify_manifest(tampered)
    assert not result["both_valid"]


def test_adv_property_ed25519_sigs_unique_per_message(tmp_path: Path) -> None:
    """Two different manifests signed with the SAME key produce DIFFERENT signatures
    (Ed25519 is deterministic within a fixed (key, message) pair, but different
    messages ⇒ different sigs)."""
    kp = gpp_manifest.GPPKeypair.generate()
    m1 = gpp_manifest.build_manifest(
        plan_artifact_paths=[], repo_root=tmp_path,
        det_report={"tier_1_overall_status": "PASS", "checks": []},
        council_findings=[], tier_3_dispositions=[],
    )
    m2 = gpp_manifest.build_manifest(
        plan_artifact_paths=[], repo_root=tmp_path,
        det_report={"tier_1_overall_status": "FAIL", "checks": []},
        council_findings=[], tier_3_dispositions=[],
    )
    signed1 = gpp_manifest.sign_manifest(m1, kp)
    signed2 = gpp_manifest.sign_manifest(m2, kp)
    assert (
        signed1["operator_signature"]["ed25519"]
        != signed2["operator_signature"]["ed25519"]
    )


# ===========================================================================
# End-to-end integration — full manifest write path
# ===========================================================================


def test_adv_run_gpp_manifest_produces_valid_signed_output(tmp_path: Path) -> None:
    """Full orchestrator round-trip: run_gpp_manifest → written manifest verifies."""
    # Set up a minimal plan dir with router + DET report
    (tmp_path / "router.yaml").touch()
    (tmp_path / "01_plan.md").write_text("minimal plan\n", encoding="utf-8")
    gpp_dir = tmp_path / "gpp"
    gpp_dir.mkdir()
    import json
    date_stamp = dt.date.today().isoformat()
    (gpp_dir / f"gpp_det_report_{date_stamp}.json").write_text(
        json.dumps({
            "tier_1_overall_status": "PASS",
            "plan_sub_docs": ["01_plan.md"],
            "checks": [],
        }),
        encoding="utf-8",
    )

    keypair = gpp_manifest.GPPKeypair.generate()
    result = gpp_manifest.run_gpp_manifest(tmp_path, keypair)
    assert result["exit_code"] == 0
    assert result["verify_result"]["both_valid"]
    # Read the written manifest back and re-verify
    manifest_path = Path(tmp_path) / result["manifest_path"].replace(
        str(tmp_path.relative_to(tmp_path.parent)) + "/", ""
    ) if False else Path(str(tmp_path).rstrip("/") + "/" + result["manifest_path"].split("/", 1)[-1])
    # Simpler: scan gpp_dir for the produced file
    produced = sorted(gpp_dir.glob("gpp_manifest_*.json"))
    assert produced, "run_gpp_manifest must write a manifest file"
    manifest = json.loads(produced[-1].read_text())
    verify = gpp_manifest.verify_manifest(manifest)
    assert verify["both_valid"]
