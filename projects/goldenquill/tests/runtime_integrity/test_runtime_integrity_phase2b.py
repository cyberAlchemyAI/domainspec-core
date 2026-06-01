"""Phase 2b Runtime Integrity tests — §4.16, §4.17, §4.2.1 Rows 22-23.

Blueprint §4 v2.5 LOCKED 2026-04-19.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile

import pytest

from pipeline.runtime_integrity import (
    FamilyCollisionResult,
    check_family_collision,
    F_ROUTER_FAMILY_COLLISION,
    KeyPresenceResult,
    check_key_presence,
    F_KEY_PRESENCE_PREFLIGHT_FAIL,
    RouterDriftResult,
    check_router_drift,
    canonical_bytes_sha3_512,
    F_RUNTIME_DRIFT_FROM_LOCKED_ROUTER,
    RailsReportResult,
    emit_rails_report,
    F_RAILS_REPORT_EMISSION_FAIL,
)


# ---------------------------------------------------------------------------
# §4.16 — Family Collision PRE-gate
# ---------------------------------------------------------------------------

class TestFamilyCollision:
    """§4.16: F-ROUTER-FAMILY-COLLISION invocation-time PRE-gate."""

    def test_no_collision_five_distinct_families(self):
        families = ["anthropic", "openai", "meta", "alibaba", "moonshot"]
        result = check_family_collision(families)
        assert not result.collision_detected
        assert result.failure_code is None

    def test_collision_detected_two_same(self):
        families = ["anthropic", "openai", "anthropic", "alibaba", "moonshot"]
        result = check_family_collision(families)
        assert result.collision_detected
        assert result.failure_code == F_ROUTER_FAMILY_COLLISION

    def test_collision_family_listed_in_colliding_families(self):
        families = ["anthropic", "anthropic", "meta", "alibaba", "moonshot"]
        result = check_family_collision(families)
        assert result.colliding_families is not None
        assert "anthropic" in result.colliding_families

    def test_collision_sub_tag_runtime(self):
        families = ["openai", "openai"]
        result = check_family_collision(families)
        assert result.detail is not None
        assert result.detail["sub_tag"] == "runtime_invocation_time"

    def test_no_collision_single_family(self):
        result = check_family_collision(["anthropic"])
        assert not result.collision_detected

    def test_empty_family_list_no_collision(self):
        result = check_family_collision([])
        assert not result.collision_detected

    def test_require_all_distinct_false_skips_check(self):
        # Even with colliding families, require_all_distinct=False passes
        families = ["anthropic", "anthropic", "openai"]
        result = check_family_collision(families, require_all_distinct=False)
        assert not result.collision_detected
        assert result.failure_code is None

    def test_collision_three_same_family(self):
        families = ["meta", "meta", "meta", "alibaba", "moonshot"]
        result = check_family_collision(families)
        assert result.collision_detected
        assert "meta" in result.colliding_families

    def test_multiple_collisions_in_one_call(self):
        families = ["anthropic", "anthropic", "openai", "openai"]
        result = check_family_collision(families)
        assert result.collision_detected
        assert len(result.colliding_families) == 2

    def test_result_is_frozen(self):
        result = check_family_collision(["anthropic"])
        with pytest.raises((AttributeError, TypeError)):
            result.collision_detected = True  # type: ignore[misc]

    def test_failure_code_constant(self):
        assert F_ROUTER_FAMILY_COLLISION == "F-ROUTER-FAMILY-COLLISION"


# ---------------------------------------------------------------------------
# §4.2.1 Row 22 — Key Presence preflight
# ---------------------------------------------------------------------------

class TestKeyPresence:
    """§4.2.1 Row 22: Key Presence preflight."""

    def test_all_keys_present(self):
        result = check_key_presence(
            {"scribe": "ANTHROPIC_KEY", "judge": "GROQ_KEY"},
            env={"ANTHROPIC_KEY": "sk-real", "GROQ_KEY": "gsk-real"},
        )
        assert result.all_present
        assert result.failure_code is None

    def test_key_absent_single(self):
        result = check_key_presence(
            {"scribe": "ANTHROPIC_KEY"},
            env={},
        )
        assert not result.all_present
        assert result.failure_code == F_KEY_PRESENCE_PREFLIGHT_FAIL

    def test_key_empty_single(self):
        result = check_key_presence(
            {"scribe": "ANTHROPIC_KEY"},
            env={"ANTHROPIC_KEY": ""},
        )
        assert not result.all_present
        assert result.failure_code == F_KEY_PRESENCE_PREFLIGHT_FAIL

    def test_key_absent_sub_tag(self):
        result = check_key_presence(
            {"scribe": "ANTHROPIC_KEY"},
            env={},
        )
        assert result.detail is not None
        assert result.detail["sub_tag"] == "key_absent"

    def test_key_empty_sub_tag(self):
        result = check_key_presence(
            {"scribe": "ANTHROPIC_KEY"},
            env={"ANTHROPIC_KEY": ""},
        )
        assert result.detail is not None
        assert result.detail["sub_tag"] == "key_empty"

    def test_missing_keys_listed(self):
        result = check_key_presence(
            {"scribe": "ANTHROPIC_KEY", "judge": "GROQ_KEY"},
            env={"ANTHROPIC_KEY": "sk-real"},
        )
        assert result.missing_keys is not None
        assert "GROQ_KEY" in result.missing_keys

    def test_empty_required_keys_passes(self):
        result = check_key_presence({}, env={})
        assert result.all_present

    def test_multiple_missing_keys(self):
        result = check_key_presence(
            {"scribe": "A_KEY", "judge": "B_KEY", "editor": "C_KEY"},
            env={},
        )
        assert not result.all_present
        assert result.missing_keys is not None
        assert len(result.missing_keys) == 3

    def test_partial_keys_present(self):
        result = check_key_presence(
            {"scribe": "A_KEY", "judge": "B_KEY"},
            env={"A_KEY": "present"},
        )
        assert not result.all_present
        assert "B_KEY" in result.missing_keys

    def test_result_is_frozen(self):
        result = check_key_presence({}, env={})
        with pytest.raises((AttributeError, TypeError)):
            result.all_present = False  # type: ignore[misc]

    def test_failure_code_constant(self):
        assert F_KEY_PRESENCE_PREFLIGHT_FAIL == "F-KEY-PRESENCE-PREFLIGHT-FAIL"

    def test_default_env_is_os_environ(self):
        # Just verifies the no-env path doesn't raise
        result = check_key_presence({})
        assert result.all_present is True


# ---------------------------------------------------------------------------
# §4.2.1 Row 23 — Drift-from-Locked-Router detection
# ---------------------------------------------------------------------------

class TestRouterDrift:
    """§4.2.1 Row 23: Drift-from-Locked-Router detection."""

    def _make_router_data(self) -> dict:
        return {"version": 1, "tilth": {"scribe": {"primary": "anthropic/claude-sonnet"}}}

    def _compute_hash(self, data: dict) -> str:
        return canonical_bytes_sha3_512(data)

    def test_no_drift_hash_matches(self):
        data = self._make_router_data()
        expected = self._compute_hash(data)
        result = check_router_drift(data, expected_hash=expected)
        assert not result.drift_detected
        assert result.failure_code is None

    def test_drift_detected_hash_mismatch(self):
        data = self._make_router_data()
        result = check_router_drift(data, expected_hash="deadbeef" * 16)
        assert result.drift_detected
        assert result.failure_code == F_RUNTIME_DRIFT_FROM_LOCKED_ROUTER

    def test_no_lock_manifest_passes_by_construction(self):
        data = self._make_router_data()
        result = check_router_drift(data, expected_hash=None)
        assert not result.drift_detected
        assert result.failure_code is None

    def test_no_lock_manifest_detail_reason(self):
        result = check_router_drift({}, expected_hash=None)
        assert result.detail is not None
        assert "no_lock_manifest" in result.detail["reason"]

    def test_operator_attested_passes_despite_mismatch(self):
        data = self._make_router_data()
        result = check_router_drift(
            data, expected_hash="different_hash", operator_attested=True
        )
        assert not result.drift_detected
        assert result.failure_code is None

    def test_operator_attested_detail_marks_hash_changed(self):
        data = self._make_router_data()
        result = check_router_drift(
            data, expected_hash="different_hash", operator_attested=True
        )
        assert result.detail is not None
        assert result.detail.get("hash_changed") is True

    def test_computed_hash_is_sha3_512_hex(self):
        data = self._make_router_data()
        expected = self._compute_hash(data)
        result = check_router_drift(data, expected_hash=expected)
        assert len(result.computed_hash) == 128  # SHA-3-512 = 64 bytes = 128 hex chars

    def test_canonical_bytes_deterministic(self):
        data = {"b": 2, "a": 1}  # keys out of order
        h1 = canonical_bytes_sha3_512(data)
        h2 = canonical_bytes_sha3_512({"a": 1, "b": 2})  # different insertion order
        assert h1 == h2  # sort_keys=True makes them identical

    def test_canonical_bytes_uses_sha3_512(self):
        data = {"key": "value"}
        canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        expected = hashlib.sha3_512(canonical.encode("utf-8")).hexdigest()
        assert canonical_bytes_sha3_512(data) == expected

    def test_result_is_frozen(self):
        result = check_router_drift({}, expected_hash=None)
        with pytest.raises((AttributeError, TypeError)):
            result.drift_detected = True  # type: ignore[misc]

    def test_failure_code_constant(self):
        assert F_RUNTIME_DRIFT_FROM_LOCKED_ROUTER == "F-RUNTIME-DRIFT-FROM-LOCKED-ROUTER"

    def test_drift_detail_contains_hashes(self):
        data = self._make_router_data()
        expected = "badhash"
        result = check_router_drift(data, expected_hash=expected)
        assert result.detail is not None
        assert result.detail["expected_hash"] == expected
        assert result.detail["computed_hash"] == result.computed_hash


# ---------------------------------------------------------------------------
# Adversarial: canonical_bytes_sha3_512 hardening — review round 2026-04-19
# F2 (NFC), F3 (non-str keys), F8 (NaN/Infinity).
# ---------------------------------------------------------------------------

class TestCanonicalBytesHardening:
    """Adversarial hardenings applied at the canonical-bytes boundary.

    Source findings: pipeline/validation/code_reviews/phase0_through_2b_2026-04-19
    GPT-OSS review — F2 (Unicode NFD collision), F3 (YAML int→str coercion),
    F8 (NaN/Infinity non-RFC serialization).
    """

    def test_nfc_normalization_closes_nfd_vs_nfc_divergence(self):
        # "café" can be written as u"caf\u00e9" (NFC) or u"cafe\u0301" (NFD).
        # Visually identical; byte-distinct. After NFC normalization both hash same.
        nfc_form = {"model": "caf\u00e9"}
        nfd_form = {"model": "cafe\u0301"}
        assert canonical_bytes_sha3_512(nfc_form) == canonical_bytes_sha3_512(nfd_form)

    def test_nfc_normalization_applies_to_dict_keys(self):
        nfc_key = {"caf\u00e9": 1}
        nfd_key = {"cafe\u0301": 1}
        assert canonical_bytes_sha3_512(nfc_key) == canonical_bytes_sha3_512(nfd_key)

    def test_nfc_normalization_applies_to_nested_str(self):
        nfc = {"a": {"b": ["caf\u00e9"]}}
        nfd = {"a": {"b": ["cafe\u0301"]}}
        assert canonical_bytes_sha3_512(nfc) == canonical_bytes_sha3_512(nfd)

    def test_int_key_rejected(self):
        with pytest.raises(TypeError, match="F-ROUTER-CANONICAL-BYTES-NONSTR-KEY"):
            canonical_bytes_sha3_512({1: "foo"})

    def test_bool_key_rejected(self):
        with pytest.raises(TypeError, match="F-ROUTER-CANONICAL-BYTES-NONSTR-KEY"):
            canonical_bytes_sha3_512({True: "foo"})

    def test_none_key_rejected(self):
        with pytest.raises(TypeError, match="F-ROUTER-CANONICAL-BYTES-NONSTR-KEY"):
            canonical_bytes_sha3_512({None: "foo"})

    def test_nested_nonstr_key_rejected(self):
        with pytest.raises(TypeError, match=r"\$\.tilth\.seat"):
            canonical_bytes_sha3_512({"tilth": {"seat": {1: "bad"}}})

    def test_nan_rejected(self):
        with pytest.raises(ValueError):
            canonical_bytes_sha3_512({"k": float("nan")})

    def test_infinity_rejected(self):
        with pytest.raises(ValueError):
            canonical_bytes_sha3_512({"k": float("inf")})

    def test_negative_infinity_rejected(self):
        with pytest.raises(ValueError):
            canonical_bytes_sha3_512({"k": float("-inf")})


# ---------------------------------------------------------------------------
# §4.17 — Rails Report POST-gate emission
# ---------------------------------------------------------------------------

class TestRailsReport:
    """§4.17: Rails Report text artifact POST-gate emission."""

    def _make_events(self, n: int = 2) -> list[dict]:
        return [
            {"gate": f"PRE-{i}", "result": "PASS", "failure_code": None, "detail": None}
            for i in range(n)
        ]

    def test_emit_succeeds(self, tmp_path):
        path = str(tmp_path / "rails_report.md")
        result = emit_rails_report("run-001", self._make_events(), path)
        assert result.emitted
        assert result.failure_code is None

    def test_emit_creates_file(self, tmp_path):
        path = str(tmp_path / "rails_report.md")
        emit_rails_report("run-001", self._make_events(), path)
        assert os.path.exists(path)

    def test_emit_file_contains_run_id(self, tmp_path):
        path = str(tmp_path / "rails_report.md")
        emit_rails_report("run-abc-123", [], path)
        content = open(path, encoding="utf-8").read()
        assert "run-abc-123" in content

    def test_emit_file_contains_gate_names(self, tmp_path):
        events = [{"gate": "PRE-GATE-7", "result": "FAIL",
                   "failure_code": "F-PRE-07", "detail": None}]
        path = str(tmp_path / "rails_report.md")
        emit_rails_report("run-001", events, path)
        content = open(path, encoding="utf-8").read()
        assert "PRE-GATE-7" in content

    def test_emit_file_contains_failure_code(self, tmp_path):
        events = [{"gate": "PRE-07", "result": "FAIL",
                   "failure_code": "F-PRE-07.rfa_hash_missing", "detail": None}]
        path = str(tmp_path / "rails_report.md")
        emit_rails_report("run-001", events, path)
        content = open(path, encoding="utf-8").read()
        assert "F-PRE-07.rfa_hash_missing" in content

    def test_emit_creates_parent_directories(self, tmp_path):
        path = str(tmp_path / "pipeline" / "runs" / "run-001" / "rails_report.md")
        result = emit_rails_report("run-001", [], path)
        assert result.emitted
        assert os.path.exists(path)

    def test_emit_fails_on_invalid_path_returns_failure_code(self):
        # Use a path with invalid characters or unwritable location
        path = "/dev/null/cannot_create_this/rails_report.md"
        result = emit_rails_report("run-001", [], path)
        assert not result.emitted
        assert result.failure_code == F_RAILS_REPORT_EMISSION_FAIL

    def test_emit_failure_detail_contains_exception(self):
        path = "/dev/null/cannot_create_this/rails_report.md"
        result = emit_rails_report("run-001", [], path)
        assert result.detail is not None
        assert "exception" in result.detail

    def test_emit_empty_events(self, tmp_path):
        path = str(tmp_path / "report.md")
        result = emit_rails_report("run-001", [], path)
        assert result.emitted

    def test_emit_output_path_in_result(self, tmp_path):
        path = str(tmp_path / "report.md")
        result = emit_rails_report("run-001", [], path)
        assert result.output_path == path

    def test_emit_with_detail_events(self, tmp_path):
        events = [{"gate": "PRE-22", "result": "PASS",
                   "failure_code": None, "detail": {"key": "value"}}]
        path = str(tmp_path / "report.md")
        result = emit_rails_report("run-001", events, path)
        assert result.emitted
        content = open(path, encoding="utf-8").read()
        assert "key" in content

    def test_result_is_frozen(self, tmp_path):
        path = str(tmp_path / "report.md")
        result = emit_rails_report("run-001", [], path)
        with pytest.raises((AttributeError, TypeError)):
            result.emitted = False  # type: ignore[misc]

    def test_failure_code_constant(self):
        assert F_RAILS_REPORT_EMISSION_FAIL == "F-RAILS-REPORT-EMISSION-FAIL"
