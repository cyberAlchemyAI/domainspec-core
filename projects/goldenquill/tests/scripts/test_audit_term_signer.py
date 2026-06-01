"""Tests for ``pipeline.scripts.audit_term_signer`` CLI."""

from __future__ import annotations

from pathlib import Path

import pytest

cryptography = pytest.importorskip("cryptography")
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from pipeline.institutional_memory._audit_decisions import (
    canonical_decision_bytes,
    compute_term_hash,
    read_audit_decisions,
)
from pipeline.logician.gates.f_dialect_migration_incomplete import (
    AUDIT_STATUS_CONFIRMED_AVOID_ALL,
    AUDIT_STATUS_CONFIRMED_PER_CLC,
)
from pipeline.scripts.audit_term_signer import build_parser, main


def _write_key(tmp_path: Path) -> tuple[Path, str]:
    """Generate an Ed25519 keypair, write the seed to disk, return
    (key_path, pub_hex)."""
    from cryptography.hazmat.primitives import serialization

    private = Ed25519PrivateKey.generate()
    seed = private.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    key_path = tmp_path / "operator.key"
    key_path.write_text(seed.hex())
    pub_hex = private.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()
    return key_path, pub_hex


def _write_register(tmp_path: Path) -> Path:
    yaml_text = """
entries:
  - term: equity
    severity: RED
  - term: systemic
    severity: YELLOW
  - term: marginalized
    severity: YELLOW
"""
    p = tmp_path / "admin_risk_register.yaml"
    p.write_text(yaml_text)
    return p


# ---------------------------------------------------------------------------
# Parser surface
# ---------------------------------------------------------------------------


def test_parser_exposes_three_subcommands() -> None:
    parser = build_parser()
    args_scaffold = parser.parse_args(["scaffold"])
    assert args_scaffold.cmd == "scaffold"
    args_sign = parser.parse_args(["sign", "--key", "/dev/null"])
    assert args_sign.cmd == "sign"
    args_verify = parser.parse_args(["verify"])
    assert args_verify.cmd == "verify"


# ---------------------------------------------------------------------------
# scaffold subcommand
# ---------------------------------------------------------------------------


def test_scaffold_creates_empty_decisions_template(tmp_path: Path) -> None:
    register_path = _write_register(tmp_path)
    decisions_path = tmp_path / "decisions.md"
    rc = main(
        [
            "scaffold",
            "--register",
            str(register_path),
            "--decisions",
            str(decisions_path),
        ]
    )
    assert rc == 0
    assert decisions_path.exists()
    rows = list(read_audit_decisions(decisions_path))
    assert {r.term for r in rows} == {"equity", "systemic", "marginalized"}
    # Every row starts as PENDING.
    assert all(r.operator_ed25519_signature_hex is None for r in rows)


def test_scaffold_refuses_to_overwrite_without_force(tmp_path: Path) -> None:
    register_path = _write_register(tmp_path)
    decisions_path = tmp_path / "decisions.md"
    decisions_path.write_text("pre-existing content")
    rc = main(
        [
            "scaffold",
            "--register",
            str(register_path),
            "--decisions",
            str(decisions_path),
        ]
    )
    assert rc == 2
    # Content not overwritten.
    assert decisions_path.read_text() == "pre-existing content"


def test_scaffold_overwrites_with_force(tmp_path: Path) -> None:
    register_path = _write_register(tmp_path)
    decisions_path = tmp_path / "decisions.md"
    decisions_path.write_text("pre-existing")
    rc = main(
        [
            "scaffold",
            "--register",
            str(register_path),
            "--decisions",
            str(decisions_path),
            "--force",
        ]
    )
    assert rc == 0
    assert "equity" in decisions_path.read_text()


# ---------------------------------------------------------------------------
# sign subcommand
# ---------------------------------------------------------------------------


def test_sign_signs_non_pending_rows(tmp_path: Path) -> None:
    register_path = _write_register(tmp_path)
    decisions_path = tmp_path / "decisions.md"
    key_path, pub_hex = _write_key(tmp_path)
    # Scaffold + manually fill audit_status on two of three rows.
    main(
        [
            "scaffold",
            "--register",
            str(register_path),
            "--decisions",
            str(decisions_path),
        ]
    )
    text = decisions_path.read_text()
    text = text.replace(
        "| equity | ", "| equity-MARK | ", 1
    )  # marker for replacement
    # Fill audit_status on equity + systemic rows.
    new_lines = []
    for line in text.splitlines():
        if line.startswith("| equity-MARK |"):
            line = line.replace(
                "equity-MARK", "equity", 1
            ).replace(
                "| <PENDING> | <PENDING> | <PENDING> |",
                "| confirmed_avoid_all | <PENDING> | <PENDING> |",
                1,
            )
        elif line.startswith("| systemic |"):
            line = line.replace(
                "| <PENDING> | <PENDING> | <PENDING> |",
                "| confirmed_per_clc | <PENDING> | <PENDING> |",
                1,
            )
        new_lines.append(line)
    decisions_path.write_text("\n".join(new_lines))

    rc = main(
        [
            "sign",
            "--key",
            str(key_path),
            "--register",
            str(register_path),
            "--decisions",
            str(decisions_path),
        ]
    )
    assert rc == 0
    # Verify the file now has signatures for the two non-PENDING rows.
    rows = list(read_audit_decisions(decisions_path))
    by_term = {r.term: r for r in rows}
    assert by_term["equity"].audit_status == AUDIT_STATUS_CONFIRMED_AVOID_ALL
    assert by_term["equity"].operator_ed25519_signature_hex is not None
    assert by_term["equity"].operator_pubkey_ed25519_hex == pub_hex
    assert by_term["systemic"].audit_status == AUDIT_STATUS_CONFIRMED_PER_CLC
    assert by_term["systemic"].operator_ed25519_signature_hex is not None
    # marginalized stays PENDING (no audit_status filled).
    assert by_term["marginalized"].operator_ed25519_signature_hex is None


def test_sign_idempotent_on_already_signed_rows(tmp_path: Path) -> None:
    """Second invocation of sign on the same file is a no-op."""
    register_path = _write_register(tmp_path)
    decisions_path = tmp_path / "decisions.md"
    key_path, _ = _write_key(tmp_path)
    main(
        [
            "scaffold",
            "--register",
            str(register_path),
            "--decisions",
            str(decisions_path),
        ]
    )
    # Fill audit_status on equity row.
    text = decisions_path.read_text().replace(
        "| equity | ", "| equity | ", 1
    )
    text = text.replace(
        "| <PENDING> | <PENDING> | <PENDING> |",
        "| confirmed_avoid_all | <PENDING> | <PENDING> |",
        1,
    )
    decisions_path.write_text(text)

    main(["sign", "--key", str(key_path), "--register", str(register_path),
          "--decisions", str(decisions_path)])
    after_first = decisions_path.read_text()
    main(["sign", "--key", str(key_path), "--register", str(register_path),
          "--decisions", str(decisions_path)])
    after_second = decisions_path.read_text()
    assert after_first == after_second, (
        "second sign invocation should be a no-op on already-signed rows"
    )


def test_sign_rejects_short_key_file(tmp_path: Path) -> None:
    register_path = _write_register(tmp_path)
    decisions_path = tmp_path / "decisions.md"
    main(
        [
            "scaffold",
            "--register",
            str(register_path),
            "--decisions",
            str(decisions_path),
        ]
    )
    # Operator hands a clearly-wrong key file.
    bad_key = tmp_path / "bad.key"
    bad_key.write_text("aabbcc")  # 3 bytes, not 32
    with pytest.raises(SystemExit) as excinfo:
        main(
            [
                "sign",
                "--key",
                str(bad_key),
                "--register",
                str(register_path),
                "--decisions",
                str(decisions_path),
            ]
        )
    assert excinfo.value.code == 1 or "32-byte" in str(excinfo.value)


# ---------------------------------------------------------------------------
# verify subcommand
# ---------------------------------------------------------------------------


def test_verify_returns_zero_when_all_signatures_valid(tmp_path: Path) -> None:
    register_path = _write_register(tmp_path)
    decisions_path = tmp_path / "decisions.md"
    key_path, pub_hex = _write_key(tmp_path)
    main(
        [
            "scaffold",
            "--register",
            str(register_path),
            "--decisions",
            str(decisions_path),
        ]
    )
    text = decisions_path.read_text().replace(
        "| <PENDING> | <PENDING> | <PENDING> |",
        "| confirmed_avoid_all | <PENDING> | <PENDING> |",
    )
    decisions_path.write_text(text)
    main(["sign", "--key", str(key_path), "--register", str(register_path),
          "--decisions", str(decisions_path)])
    rc = main(["verify", "--decisions", str(decisions_path)])
    assert rc == 0


def test_verify_returns_nonzero_on_tampered_signature(tmp_path: Path) -> None:
    register_path = _write_register(tmp_path)
    decisions_path = tmp_path / "decisions.md"
    key_path, _ = _write_key(tmp_path)
    main(
        [
            "scaffold",
            "--register",
            str(register_path),
            "--decisions",
            str(decisions_path),
        ]
    )
    text = decisions_path.read_text().replace(
        "| <PENDING> | <PENDING> | <PENDING> |",
        "| confirmed_avoid_all | <PENDING> | <PENDING> |",
    )
    decisions_path.write_text(text)
    main(["sign", "--key", str(key_path), "--register", str(register_path),
          "--decisions", str(decisions_path)])

    # Tamper with the audit_status column AFTER signing — signature now
    # covers stale bytes.
    text = decisions_path.read_text().replace(
        "| confirmed_avoid_all |", "| confirmed_per_clc |", 1
    )
    decisions_path.write_text(text)
    rc = main(["verify", "--decisions", str(decisions_path)])
    assert rc == 1
