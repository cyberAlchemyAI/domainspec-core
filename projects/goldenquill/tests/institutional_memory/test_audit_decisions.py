"""Tests for ``pipeline.institutional_memory._audit_decisions``.

Plumbing for the F-DIALECT-MIGRATION-INCOMPLETE gate per §4 v2.x
apolitical_dialect §4.X.6 (LOCKED 2026-05-16T14:00:00Z). Covers:

- ``read_admin_risk_register`` parses ``admin_risk_register.yaml`` into
  ``AdminRiskRegisterEntry`` instances.
- ``read_audit_decisions`` parses the Markdown table into
  ``AuditDecisionRow`` instances; raises ``FileNotFoundError`` on missing
  file (gate emits ``.audit_decisions_missing`` per C2-NEW-MED-4).
- ``compute_term_hash`` + ``canonical_decision_bytes`` produce stable
  identifiers + signed-payload bytes mirroring the gate.
- ``make_signature_verifier`` returns a callable that verifies real
  Ed25519 signatures + matches the gate's verifier Protocol.
- ``render_empty_decisions_template`` seeds the operator scaffold.
"""

from __future__ import annotations

from pathlib import Path

import pytest

# Skip the whole module if cryptography isn't available — the plumbing
# can be parsed but signature paths require Ed25519.
cryptography = pytest.importorskip("cryptography")
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from pipeline.institutional_memory._audit_decisions import (
    DEFAULT_ADMIN_RISK_REGISTER_PATH,
    DEFAULT_AUDIT_DECISIONS_PATH,
    canonical_decision_bytes,
    compute_term_hash,
    make_signature_verifier,
    read_admin_risk_register,
    read_audit_decisions,
    render_empty_decisions_template,
)
from pipeline.logician.gates.f_dialect_migration_incomplete import (
    AUDIT_STATUS_CONFIRMED_AVOID_ALL,
    AUDIT_STATUS_CONFIRMED_PER_CLC,
    AdminRiskRegisterEntry,
)
from pipeline.logician.gates.f_dialect_migration_incomplete import (
    _term_hash as gate_term_hash,
)


# ---------------------------------------------------------------------------
# Canonical helpers
# ---------------------------------------------------------------------------


def test_term_hash_matches_gate_implementation() -> None:
    """The plumbing's compute_term_hash MUST match the gate's _term_hash
    byte-for-byte; otherwise the gate's lookup keys won't match what the
    operator-signing path produces."""
    assert compute_term_hash("equity", "RED") == gate_term_hash("equity", "RED")
    assert compute_term_hash("equity", "YELLOW") == gate_term_hash("equity", "YELLOW")
    # Different severity → different hash (severity is part of the identity).
    assert compute_term_hash("equity", "RED") != compute_term_hash("equity", "YELLOW")
    # Hex digest is 64 chars (SHA3-256 = 32 bytes).
    assert len(compute_term_hash("equity", "RED")) == 64


def test_canonical_decision_bytes_sorted_keys() -> None:
    """Canonical bytes use sort_keys=True so signatures are stable."""
    a = canonical_decision_bytes(
        term="equity",
        term_hash="aa" * 32,
        audit_status=AUDIT_STATUS_CONFIRMED_AVOID_ALL,
    )
    # JSON keys sorted: audit_status, term, term_hash.
    assert a == (
        b'{"audit_status":"confirmed_avoid_all","term":"equity","term_hash":"'
        + b"aa" * 32
        + b'"}'
    )


def test_canonical_decision_bytes_handles_unicode_term() -> None:
    """ensure_ascii=False so non-ASCII terms serialize losslessly."""
    cb = canonical_decision_bytes(
        term="café-au-lait",
        term_hash="00" * 32,
        audit_status=AUDIT_STATUS_CONFIRMED_AVOID_ALL,
    )
    # Verify the unicode bytes are present (UTF-8 of é is 0xc3 0xa9).
    assert b"\xc3\xa9" in cb


# ---------------------------------------------------------------------------
# Signature verifier
# ---------------------------------------------------------------------------


def test_signature_verifier_valid_sig_passes() -> None:
    private = Ed25519PrivateKey.generate()
    from cryptography.hazmat.primitives import serialization

    pub_hex = private.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()
    cb = canonical_decision_bytes(
        term="equity",
        term_hash=compute_term_hash("equity", "RED"),
        audit_status=AUDIT_STATUS_CONFIRMED_AVOID_ALL,
    )
    sig_hex = private.sign(cb).hex()
    verify = make_signature_verifier()
    assert verify(
        term="equity",
        term_hash=compute_term_hash("equity", "RED"),
        audit_status=AUDIT_STATUS_CONFIRMED_AVOID_ALL,
        signature_hex=sig_hex,
        pubkey_hex=pub_hex,
    )


def test_signature_verifier_tampered_audit_status_fails() -> None:
    private = Ed25519PrivateKey.generate()
    from cryptography.hazmat.primitives import serialization

    pub_hex = private.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()
    cb = canonical_decision_bytes(
        term="equity",
        term_hash=compute_term_hash("equity", "RED"),
        audit_status=AUDIT_STATUS_CONFIRMED_AVOID_ALL,
    )
    sig_hex = private.sign(cb).hex()
    verify = make_signature_verifier()
    # Adversary flips audit_status to per-CLC; signature no longer covers it.
    assert not verify(
        term="equity",
        term_hash=compute_term_hash("equity", "RED"),
        audit_status=AUDIT_STATUS_CONFIRMED_PER_CLC,
        signature_hex=sig_hex,
        pubkey_hex=pub_hex,
    )


def test_signature_verifier_expected_pubkey_pin_enforced() -> None:
    """When ``expected_pubkey_hex`` is supplied, any other pubkey is rejected
    even with a valid math-correct signature."""
    legitimate = Ed25519PrivateKey.generate()
    adversary = Ed25519PrivateKey.generate()
    from cryptography.hazmat.primitives import serialization

    legit_pub_hex = legitimate.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()
    adv_pub_hex = adversary.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()
    cb = canonical_decision_bytes(
        term="equity",
        term_hash=compute_term_hash("equity", "RED"),
        audit_status=AUDIT_STATUS_CONFIRMED_AVOID_ALL,
    )
    adv_sig = adversary.sign(cb).hex()
    verify = make_signature_verifier(expected_pubkey_hex=legit_pub_hex)
    # Adversary's signature verifies cryptographically but the pubkey pin rejects.
    assert not verify(
        term="equity",
        term_hash=compute_term_hash("equity", "RED"),
        audit_status=AUDIT_STATUS_CONFIRMED_AVOID_ALL,
        signature_hex=adv_sig,
        pubkey_hex=adv_pub_hex,
    )


def test_signature_verifier_handles_invalid_hex_gracefully() -> None:
    verify = make_signature_verifier()
    assert not verify(
        term="equity",
        term_hash="00" * 32,
        audit_status=AUDIT_STATUS_CONFIRMED_AVOID_ALL,
        signature_hex="not-hex",
        pubkey_hex="00" * 32,
    )
    assert not verify(
        term="equity",
        term_hash="00" * 32,
        audit_status=AUDIT_STATUS_CONFIRMED_AVOID_ALL,
        signature_hex="aa" * 64,
        pubkey_hex="not-hex-either",
    )


def test_signature_verifier_handles_wrong_pubkey_length() -> None:
    verify = make_signature_verifier()
    assert not verify(
        term="equity",
        term_hash="00" * 32,
        audit_status=AUDIT_STATUS_CONFIRMED_AVOID_ALL,
        signature_hex="aa" * 64,
        # 30 bytes — wrong length for Ed25519 raw pubkey.
        pubkey_hex="00" * 30,
    )


# ---------------------------------------------------------------------------
# admin_risk_register reader
# ---------------------------------------------------------------------------


def test_read_admin_risk_register_live_yields_real_entries() -> None:
    """The live admin_risk_register.yaml parses; entries carry term + severity."""
    entries = list(read_admin_risk_register())
    assert len(entries) > 0, (
        f"expected non-empty admin_risk_register at {DEFAULT_ADMIN_RISK_REGISTER_PATH}"
    )
    # Every entry has term + severity + (defaulted) per_clc_register.
    for e in entries:
        assert isinstance(e.term, str) and e.term
        assert e.severity in {"RED", "YELLOW", "GREEN"}
        assert isinstance(e.per_clc_register, dict)


def test_read_admin_risk_register_pre_v7_0_12_entries_have_empty_per_clc() -> None:
    """The live admin_risk_register.yaml is pre-v7.0.12 (still carries
    `progressive_register`); every entry parses with empty per_clc_register.
    The gate treats that as 'unmigrated — requires audit-decision row.'"""
    entries = list(read_admin_risk_register())
    unmigrated = [e for e in entries if not e.per_clc_register]
    assert len(unmigrated) >= 1


def test_read_admin_risk_register_custom_path(tmp_path: Path) -> None:
    yaml_text = """
version: 3.0
entries:
  - term: equity
    severity: RED
    per_clc_register:
      public_purpose_works: AVOID
      sponsorship_corporate: OK
  - term: systemic
    severity: YELLOW
"""
    p = tmp_path / "tiny_register.yaml"
    p.write_text(yaml_text)
    entries = list(read_admin_risk_register(p))
    assert len(entries) == 2
    assert entries[0].term == "equity"
    assert entries[0].per_clc_register == {
        "public_purpose_works": "AVOID",
        "sponsorship_corporate": "OK",
    }
    assert entries[1].term == "systemic"
    assert entries[1].per_clc_register == {}


# ---------------------------------------------------------------------------
# audit_decisions reader
# ---------------------------------------------------------------------------


def test_read_audit_decisions_missing_file_raises_filenotfound() -> None:
    """C2-NEW-MED-4: the gate catches FileNotFoundError and emits the
    .audit_decisions_missing sub-tag. The reader propagates it."""
    with pytest.raises(FileNotFoundError):
        list(read_audit_decisions(Path("/nonexistent/path/does/not/exist.md")))


def test_read_audit_decisions_parses_well_formed_table(tmp_path: Path) -> None:
    md = (
        "# header\n"
        "\n"
        "| term | term_hash | audit_status | operator_ed25519_signature_hex | operator_pubkey_ed25519_hex |\n"
        "|------|-----------|--------------|--------------------------------|-----------------------------|\n"
        f"| equity | {compute_term_hash('equity', 'RED')} | confirmed_avoid_all | {'aa' * 64} | {'bb' * 32} |\n"
        f"| systemic | {compute_term_hash('systemic', 'YELLOW')} | <PENDING> | <PENDING> | <PENDING> |\n"
    )
    p = tmp_path / "decisions.md"
    p.write_text(md)
    rows = list(read_audit_decisions(p))
    assert len(rows) == 2
    assert rows[0].term == "equity"
    assert rows[0].audit_status == AUDIT_STATUS_CONFIRMED_AVOID_ALL
    assert rows[0].operator_ed25519_signature_hex == "aa" * 64
    # The pending row → audit_status passed-through, sig/pubkey normalized to None.
    assert rows[1].operator_ed25519_signature_hex is None
    assert rows[1].operator_pubkey_ed25519_hex is None


def test_read_audit_decisions_tolerates_extra_whitespace(tmp_path: Path) -> None:
    md = (
        "| term | term_hash | audit_status | operator_ed25519_signature_hex | operator_pubkey_ed25519_hex |\n"
        "|------|-----------|--------------|--------------------------------|-----------------------------|\n"
        "|  equity   |  abc123  |  confirmed_avoid_all  |  null  |  -  |\n"
    )
    p = tmp_path / "decisions.md"
    p.write_text(md)
    rows = list(read_audit_decisions(p))
    assert rows[0].term == "equity"
    assert rows[0].term_hash == "abc123"
    assert rows[0].audit_status == AUDIT_STATUS_CONFIRMED_AVOID_ALL
    assert rows[0].operator_ed25519_signature_hex is None
    assert rows[0].operator_pubkey_ed25519_hex is None


def test_read_audit_decisions_skips_prose_outside_table(tmp_path: Path) -> None:
    md = (
        "Some prose at the top.\n"
        "\n"
        "Another paragraph mentioning | pipes | that look like a table.\n"
        "\n"
        "| term | term_hash | audit_status | operator_ed25519_signature_hex | operator_pubkey_ed25519_hex |\n"
        "|------|-----------|--------------|--------------------------------|-----------------------------|\n"
        "| equity | abc | confirmed_avoid_all | aa | bb |\n"
    )
    p = tmp_path / "decisions.md"
    p.write_text(md)
    rows = list(read_audit_decisions(p))
    assert len(rows) == 1
    assert rows[0].term == "equity"


# ---------------------------------------------------------------------------
# Empty-template generator
# ---------------------------------------------------------------------------


def test_render_empty_decisions_template_one_row_per_entry() -> None:
    entries = [
        AdminRiskRegisterEntry(term="equity", severity="RED", per_clc_register={}),
        AdminRiskRegisterEntry(term="systemic", severity="YELLOW", per_clc_register={}),
    ]
    text = render_empty_decisions_template(entries=entries)
    # Header block + table header + 2 data rows.
    assert "| equity |" in text
    assert "| systemic |" in text
    # PENDING sentinels.
    assert "<PENDING>" in text
    # Canonical-bytes shape is documented in the operator instructions block.
    assert "audit_status" in text


def test_render_template_round_trips_through_reader(tmp_path: Path) -> None:
    """The generated template's data rows parse back as PENDING."""
    entries = [
        AdminRiskRegisterEntry(term="equity", severity="RED", per_clc_register={}),
    ]
    text = render_empty_decisions_template(entries=entries)
    p = tmp_path / "decisions.md"
    p.write_text(text)
    rows = list(read_audit_decisions(p))
    assert len(rows) == 1
    assert rows[0].term == "equity"
    # PENDING normalizes signature/pubkey to None.
    assert rows[0].operator_ed25519_signature_hex is None
    assert rows[0].operator_pubkey_ed25519_hex is None
    assert rows[0].audit_status == "<PENDING>"


# ---------------------------------------------------------------------------
# End-to-end: scaffold → sign → verify wires cleanly into the gate
# ---------------------------------------------------------------------------


def test_end_to_end_scaffold_sign_verify_through_gate(tmp_path: Path) -> None:
    """Operator workflow integration test: scaffold → operator fills
    audit_status → audit_term_signer signs → gate accepts."""
    from pipeline.logician.gates.f_dialect_migration_incomplete import run

    # Stage a fake register.
    register_yaml = """
entries:
  - term: equity
    severity: RED
  - term: systemic
    severity: YELLOW
"""
    register_path = tmp_path / "admin_risk_register.yaml"
    register_path.write_text(register_yaml)
    entries = list(read_admin_risk_register(register_path))
    assert len(entries) == 2

    # Operator decides audit_status for each term.
    private = Ed25519PrivateKey.generate()
    from cryptography.hazmat.primitives import serialization

    pub_hex = private.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()

    decisions_md_lines = [
        "| term | term_hash | audit_status | operator_ed25519_signature_hex | operator_pubkey_ed25519_hex |",
        "|------|-----------|--------------|--------------------------------|-----------------------------|",
    ]
    for e in entries:
        th = compute_term_hash(e.term, e.severity)
        cb = canonical_decision_bytes(
            term=e.term,
            term_hash=th,
            audit_status=AUDIT_STATUS_CONFIRMED_AVOID_ALL,
        )
        sig = private.sign(cb).hex()
        decisions_md_lines.append(
            f"| {e.term} | {th} | confirmed_avoid_all | {sig} | {pub_hex} |"
        )
    decisions_path = tmp_path / "decisions.md"
    decisions_path.write_text("\n".join(decisions_md_lines) + "\n")

    verify = make_signature_verifier(expected_pubkey_hex=pub_hex)
    result = run(
        admin_risk_register_reader=lambda: read_admin_risk_register(register_path),
        audit_decisions_reader=lambda: read_audit_decisions(decisions_path),
        signature_verifier=verify,
    )
    assert result.passed is True, (
        f"end-to-end happy path failed: {result.findings}"
    )
