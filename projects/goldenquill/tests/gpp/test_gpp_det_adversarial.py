"""
Phase 0 GPP Hardening — Tier 1 DET adversarial tests
======================================================

Complements tests/gpp/test_gpp_phase0.py with hostile-input probes
per pipeline/validation/gpp_phase0_adversarial_test_specs.md §Tier 1.

Attack classes covered:
  ADV-DET-01  canonical-bytes collision
  ADV-DET-02  SHA-3-512 drift
  ADV-DET-03  JSON parser evasion (canonical-bytes recipe contract)
  ADV-DET-04  existence-check bypass

Test names follow test_adv_<attack-class>_<probe-detail> per spec.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Import under test (mirror test_gpp_phase0.py resolution)
# ---------------------------------------------------------------------------

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

import gpp_det  # noqa: E402
import gpp_manifest  # noqa: E402  (uses the canonical-bytes recipe)


# ===========================================================================
# ADV-DET-01 — canonical-bytes collision
# ===========================================================================
#
# The §0.5 v4 canonical-bytes recipe is:
#   json.dumps(obj, sort_keys=True, separators=(",",":"), ensure_ascii=False)
#     .encode("utf-8") → SHA-3-512
# Lives in gpp_manifest.canonical_bytes.  These probes confirm the recipe is
# collision-resistant against plausibly-equivalent variants.


def test_adv_dict_key_reorder_produces_identical_bytes() -> None:
    """sort_keys=True eliminates key-order variance — two dicts with the same
    keys in different orders produce IDENTICAL canonical bytes (by design)."""
    a = {"alpha": 1, "beta": 2, "gamma": 3}
    b = {"gamma": 3, "alpha": 1, "beta": 2}
    assert gpp_manifest.canonical_bytes(a) == gpp_manifest.canonical_bytes(b)


def test_adv_whitespace_in_string_values_preserved() -> None:
    """Trailing whitespace in a string VALUE is preserved — canonical bytes
    must distinguish 'foo' vs 'foo '."""
    a = {"k": "foo"}
    b = {"k": "foo "}
    assert gpp_manifest.canonical_bytes(a) != gpp_manifest.canonical_bytes(b)


def test_adv_unicode_nfc_vs_nfd_forms_produce_distinct_bytes() -> None:
    """Normalization is NOT applied silently.  'café' in NFC (precomposed)
    and NFD (decomposed) produce distinct canonical bytes because the
    recipe does not call unicodedata.normalize."""
    import unicodedata
    nfc = unicodedata.normalize("NFC", "café")    # U+00E9
    nfd = unicodedata.normalize("NFD", "café")    # U+0065 U+0301
    assert nfc != nfd  # sanity
    a = {"k": nfc}
    b = {"k": nfd}
    assert gpp_manifest.canonical_bytes(a) != gpp_manifest.canonical_bytes(b)


def test_adv_nested_dict_order_irrelevant() -> None:
    """Deep keys are also sorted — nested dict order does not affect bytes."""
    a = {"outer": {"a": 1, "b": 2}, "z": [1, 2, 3]}
    b = {"z": [1, 2, 3], "outer": {"b": 2, "a": 1}}
    assert gpp_manifest.canonical_bytes(a) == gpp_manifest.canonical_bytes(b)


def test_adv_int_vs_float_distinct() -> None:
    """1 and 1.0 serialize differently in JSON and must produce distinct bytes."""
    a = {"x": 1}
    b = {"x": 1.0}
    assert gpp_manifest.canonical_bytes(a) != gpp_manifest.canonical_bytes(b)


def test_adv_list_order_preserved() -> None:
    """List order is semantic — [1, 2, 3] ≠ [3, 2, 1] in canonical bytes."""
    a = {"items": [1, 2, 3]}
    b = {"items": [3, 2, 1]}
    assert gpp_manifest.canonical_bytes(a) != gpp_manifest.canonical_bytes(b)


def test_adv_null_vs_missing_key_distinct() -> None:
    """A key mapped to None is distinct from an absent key."""
    a = {"k": None}
    b = {}
    assert gpp_manifest.canonical_bytes(a) != gpp_manifest.canonical_bytes(b)


# ===========================================================================
# ADV-DET-02 — SHA-3-512 drift
# ===========================================================================


def test_adv_hash_is_sha3_512_not_sha256() -> None:
    """Confirm hashlib.sha3_512 is the backend — SHA-3 ≠ SHA-2."""
    data = b"the quick brown fox"
    sha3 = gpp_manifest.sha3_512_hex(data)
    sha256 = hashlib.sha256(data).hexdigest()
    sha2_512 = hashlib.sha512(data).hexdigest()
    assert sha3 != sha256
    assert sha3 != sha2_512
    # Confirmed match against hashlib.sha3_512 directly
    assert sha3 == hashlib.sha3_512(data).hexdigest()


def test_adv_hash_output_is_128_hex_chars() -> None:
    """SHA-3-512 produces 64 bytes == 128 hex chars exactly."""
    data = b"x"
    h = gpp_manifest.sha3_512_hex(data)
    assert len(h) == 128
    int(h, 16)  # must be valid hex


def test_adv_hash_deterministic_across_runs() -> None:
    """Same input → same hash across 1000 invocations (determinism check)."""
    data = b"deterministic sample"
    baseline = gpp_manifest.sha3_512_hex(data)
    for _ in range(1000):
        assert gpp_manifest.sha3_512_hex(data) == baseline


def test_adv_hash_sensitive_to_single_bit_flip() -> None:
    """One-bit flip in input produces a completely different hash (avalanche)."""
    a = b"adversarial sample A"
    b = b"adversarial sample B"  # single byte diff
    ha = gpp_manifest.sha3_512_hex(a)
    hb = gpp_manifest.sha3_512_hex(b)
    assert ha != hb
    # Avalanche sanity: differ in at least ~40 nibbles out of 128
    diffs = sum(1 for x, y in zip(ha, hb) if x != y)
    assert diffs >= 40, f"Avalanche weaker than expected: {diffs} nibble diffs"


def test_adv_file_hash_matches_inline_hash(tmp_path: Path) -> None:
    """file_sha3_512_hex matches inline sha3_512 of the same bytes."""
    p = tmp_path / "sample.bin"
    content = b"sample file bytes\nline 2\n"
    p.write_bytes(content)
    assert gpp_manifest.file_sha3_512_hex(p) == hashlib.sha3_512(content).hexdigest()


# ===========================================================================
# ADV-DET-03 — JSON parser / canonical-bytes recipe evasion
# ===========================================================================
#
# json.dumps in the canonical-bytes recipe uses Python's strict stdlib JSON
# encoder.  These probes confirm the encoder's behavior under hostile input.


def test_adv_nan_inf_rejected() -> None:
    """canonical_bytes over NaN/Inf must either reject or be documented.
    Python's json.dumps allows NaN/Inf by default via allow_nan=True.
    The recipe does NOT pass allow_nan=False — document this.

    This test PINS the current behavior: Python encodes NaN as 'NaN'
    (non-RFC-8259).  If the spec later requires strict rejection, this test
    flips to pytest.raises.
    """
    import math
    # Document the current Python behavior — NaN passes through as 'NaN'
    out = gpp_manifest.canonical_bytes({"x": math.nan})
    assert b"NaN" in out, "Current recipe permits NaN; if spec tightens, flip this test"


def test_adv_duplicate_keys_impossible_in_python_dict() -> None:
    """Python dicts cannot contain duplicate keys — last-wins on literal.
    This is a native language-level guarantee; canonical-bytes inherits it."""
    d = {"k": 1, "k": 2}  # noqa: F601 - intentional test
    assert d == {"k": 2}
    out = gpp_manifest.canonical_bytes(d)
    assert out == gpp_manifest.canonical_bytes({"k": 2})


def test_adv_ensure_ascii_false_preserves_utf8() -> None:
    """ensure_ascii=False means non-ASCII UTF-8 is encoded raw, not \\uXXXX."""
    d = {"greeting": "你好"}
    raw = gpp_manifest.canonical_bytes(d)
    # UTF-8 bytes for 你好 — must appear directly (not as \\u sequences)
    assert "你好".encode("utf-8") in raw
    assert b"\\u" not in raw, "ensure_ascii=False must not emit unicode escapes"


def test_adv_canonical_bytes_round_trip_stable() -> None:
    """Round-trip stability: canonical_bytes(parse(canonical_bytes(m))) == canonical_bytes(m)."""
    original = {
        "gpp_spec_version": "v1",
        "plan_artifact_set": ["a.md", "b.md"],
        "nested": {"keys": [1, 2, 3], "more": "data"},
    }
    bytes1 = gpp_manifest.canonical_bytes(original)
    parsed = json.loads(bytes1.decode("utf-8"))
    bytes2 = gpp_manifest.canonical_bytes(parsed)
    assert bytes1 == bytes2


def test_adv_no_collision_for_distinct_manifests() -> None:
    """No two semantically-distinct manifests collide under canonical_bytes.
    Property: a != b → canonical_bytes(a) != canonical_bytes(b)."""
    samples = [
        {"a": 1},
        {"a": 2},
        {"a": "1"},           # string vs int
        {"a": [1]},           # list vs scalar
        {"a": [1, 1]},        # length differs
        {"a": {"b": 1}},      # dict vs scalar
        {"b": 1},             # different key
        {},
    ]
    encodings = [gpp_manifest.canonical_bytes(s) for s in samples]
    assert len(set(encodings)) == len(samples), "Collision detected"


# ===========================================================================
# ADV-DET-04 — existence-check bypass (CITE-RESOLVE hostile paths)
# ===========================================================================


def test_adv_symlink_to_missing_target_fails(tmp_path: Path) -> None:
    """A symlink whose target does not exist: Path.exists() returns False,
    so CITE-RESOLVE correctly flags the cite as missing."""
    (tmp_path / "router.yaml").touch()
    (tmp_path / "pipeline").mkdir()
    target = tmp_path / "pipeline" / "missing_target.md"
    link = tmp_path / "pipeline" / "broken_link.md"
    os.symlink(str(target), str(link))
    assert link.is_symlink()
    assert not link.exists(), "symlink to missing target should report not-exists"

    plan_doc = tmp_path / "01_plan.md"
    plan_doc.write_text("See pipeline/broken_link.md for details.\n")
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_cite_resolve(docs, tmp_path)
    assert result["status"] == "FAIL"
    assert any("broken_link" in f["cite"] for f in result["findings"])


def test_adv_zero_byte_file_passes_existence_check(tmp_path: Path) -> None:
    """Zero-byte file: Path.exists() returns True.  CITE-RESOLVE does NOT
    reject these — this is documented behavior, not a bug.  If future spec
    requires non-empty files, this test flips to a FAIL expectation."""
    (tmp_path / "router.yaml").touch()
    (tmp_path / "pipeline").mkdir()
    (tmp_path / "pipeline" / "empty.md").touch()  # zero bytes

    plan_doc = tmp_path / "01_plan.md"
    plan_doc.write_text("See pipeline/empty.md for details.\n")
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_cite_resolve(docs, tmp_path)
    assert result["status"] == "PASS", (
        "Zero-byte files pass existence check; if spec tightens, update this test"
    )


def test_adv_directory_where_file_expected_passes_existence_check(tmp_path: Path) -> None:
    """When the cite path resolves to a directory (not a file): Path.exists()
    returns True.  Current behavior — document.  Future spec may require
    is_file() for .md citations."""
    (tmp_path / "router.yaml").touch()
    (tmp_path / "pipeline").mkdir()
    # Create a DIRECTORY at the path that looks like a .md file
    (tmp_path / "pipeline" / "tricky.md").mkdir()

    plan_doc = tmp_path / "01_plan.md"
    plan_doc.write_text("See pipeline/tricky.md for details.\n")
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_cite_resolve(docs, tmp_path)
    # Path.exists() returns True for dirs → PASS under current code
    assert result["status"] == "PASS", (
        "Current code tolerates dir-where-file-expected; if spec tightens, flip this test"
    )


def test_adv_dotdot_in_cite_does_not_escape_repo_root(tmp_path: Path) -> None:
    """A cite containing '..' should not be resolvable above the repo root.
    Current regex does not match paths with '..' so they're ignored."""
    (tmp_path / "router.yaml").touch()
    plan_doc = tmp_path / "01_plan.md"
    plan_doc.write_text("See pipeline/../../../etc/passwd for details.\n")
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_cite_resolve(docs, tmp_path)
    # Either PASS (regex didn't match) or FAIL with specific reason —
    # critical invariant: no silent traversal to /etc/passwd.
    for f in result.get("findings", []):
        assert "etc/passwd" not in f.get("cite", ""), "dotdot traversal detected"


def test_adv_extract_cites_rejects_angle_bracket_placeholders() -> None:
    """extract_cites skips any cite containing < or > (placeholder guard)."""
    text = "Use `pipeline/<plan-dir>/gpp_det.py` and `pipeline/SESSION.md` for refs.\n"
    cites = gpp_det.extract_cites(text)
    # The placeholder one should be filtered out
    assert not any("<" in c or ">" in c for c in cites)


# ===========================================================================
# Additional hardening — check_cite_resolve against tricky recurring text
# ===========================================================================


def test_adv_repeated_cite_in_same_doc_fails_once(tmp_path: Path) -> None:
    """A missing cite that appears 10x in the same doc produces findings but
    status must still be FAIL (not silently-PASS on dedup)."""
    (tmp_path / "router.yaml").touch()
    plan_doc = tmp_path / "01_plan.md"
    plan_doc.write_text(
        "\n".join(["See pipeline/does_not_exist_xyz.md"] * 10) + "\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_cite_resolve(docs, tmp_path)
    assert result["status"] == "FAIL"


def test_adv_hash_pin_recomputes_on_file_mutation(tmp_path: Path) -> None:
    """If a plan sub-doc is mutated between runs, HASH-PIN produces a
    different hash — no caching holdover."""
    (tmp_path / "router.yaml").touch()
    p = tmp_path / "01_plan.md"
    p.write_text("version 1\n")
    r1 = gpp_det.check_hash_pin({p: p.read_text()}, tmp_path)
    p.write_text("version 2\n")
    r2 = gpp_det.check_hash_pin({p: p.read_text()}, tmp_path)
    rel = "01_plan.md"
    assert r1["hashes"][rel] != r2["hashes"][rel]
