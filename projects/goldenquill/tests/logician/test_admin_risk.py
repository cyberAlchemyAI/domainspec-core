"""Tests for pipeline.logician.admin_risk (M8 PRE-gate verifier).

§4.7 + §4.2.1 PRE-gate check #10. The verifier consumes the sovereignty-layer
ledger that Round F's `pipeline.sovereignty.admin_risk.record_admin_risk(...)`
produces, and surfaces a structured `MonotonicityResult` for the PRE-gate.

Sub-tag taxonomy (F-PRE-10.*):
* admin_risk_unreadable
* admin_risk_chain_break
* admin_risk_trailer_tamper
* admin_risk_watermark_regression
* admin_risk_non_monotonic   (specialisation of chain_break: seq_id != last+1)
* admin_risk_replayed_seq_id (duplicate seq_id)
"""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path

import pytest

from pipeline.logician.admin_risk import (
    F_PRE_10,
    AdminRiskMonotonicityFailed,
    EntryKindMeta,
    MonotonicityResult,
    SeverityClassification,
    classify_severity,
    count_unresolved_hard_blocks,
    entry_kind_meta,
    iter_admin_risk_entries,
    verify_admin_risk_ledger,
)
from pipeline.sovereignty.admin_risk import (
    AdminRiskEntry,
    record_admin_risk,
)


LKEY = b"L" * 32
WKEY = b"W" * 32


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    return tmp_path


def _record(
    repo: Path,
    *,
    severity: str = "GREEN",
    entry_kind: str = "flagged_term_substitution",
    payload: dict | None = None,
    retype: str | None = None,
) -> AdminRiskEntry:
    return record_admin_risk(
        repo_root=repo,
        entry_kind=entry_kind,
        severity=severity,
        payload=payload if payload is not None else {"term": "foo"},
        operator_retype_confirmation=retype,
        hmac_key=LKEY,
        watermarks_hmac_key=WKEY,
    )


def _ledger_path(repo: Path) -> Path:
    return repo / "sovereignty" / "ledgers" / "admin_risk.jsonl"


def _trailer_path(repo: Path) -> Path:
    return repo / "sovereignty" / "ledgers" / "admin_risk.hmac"


# ---------------------------------------------------------------------------
# Failure-code constant
# ---------------------------------------------------------------------------


class TestFailureCodeConstant:
    def test_f_pre_10_value(self) -> None:
        assert F_PRE_10 == "F-PRE-10"


# ---------------------------------------------------------------------------
# MonotonicityResult dataclass shape
# ---------------------------------------------------------------------------


class TestMonotonicityResultShape:
    def test_is_frozen(self, repo: Path) -> None:
        _record(repo)
        result = verify_admin_risk_ledger(repo_root=repo, hmac_key=LKEY)
        with pytest.raises(dataclasses.FrozenInstanceError):
            result.tail_seq_id = 99  # type: ignore[misc]

    def test_kw_only(self) -> None:
        with pytest.raises(TypeError):
            MonotonicityResult(True, 0, "", 0)  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Severity classification (blueprint §4.7.2)
# ---------------------------------------------------------------------------


class TestClassifySeverity:
    def test_red_maps_to_hard_block(self) -> None:
        c = classify_severity("RED")
        assert isinstance(c, SeverityClassification)
        assert c.emoji == "🔴"
        assert c.display_label == "HARD_BLOCK"
        assert c.is_hard_block is True

    def test_yellow_maps_to_memoed(self) -> None:
        c = classify_severity("YELLOW")
        assert c.emoji == "🟡"
        assert c.display_label == "MEMOED"
        assert c.is_hard_block is False

    def test_green_maps_to_precautionary(self) -> None:
        c = classify_severity("GREEN")
        assert c.emoji == "🟢"
        assert c.display_label == "PRECAUTIONARY"
        assert c.is_hard_block is False

    def test_unknown_severity_raises(self) -> None:
        with pytest.raises(ValueError):
            classify_severity("PURPLE")

    def test_classification_is_frozen(self) -> None:
        c = classify_severity("RED")
        with pytest.raises(dataclasses.FrozenInstanceError):
            c.emoji = "x"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Entry-kind metadata
# ---------------------------------------------------------------------------


class TestEntryKindMeta:
    def test_flagged_term_meta(self) -> None:
        m = entry_kind_meta("flagged_term_substitution")
        assert isinstance(m, EntryKindMeta)
        assert m.requires_operator_signature is False

    def test_review_seat_bypass_requires_signature(self) -> None:
        m = entry_kind_meta("review_seat_bypass")
        assert m.requires_operator_signature is True
        assert m.requires_retype_confirmation is True

    def test_unknown_entry_kind_raises(self) -> None:
        with pytest.raises(ValueError):
            entry_kind_meta("not-a-kind")


# ---------------------------------------------------------------------------
# Happy-path verify (uses Round F's writer)
# ---------------------------------------------------------------------------


class TestVerifyHappyPath:
    def test_empty_ledger_returns_zero(self, repo: Path) -> None:
        # No record_admin_risk calls — ledger absent. Verifier must surface
        # missing-ledger as a verifiable failure (PRE-gate must not assume).
        with pytest.raises(AdminRiskMonotonicityFailed) as exc:
            verify_admin_risk_ledger(repo_root=repo, hmac_key=LKEY)
        assert exc.value.code == F_PRE_10
        assert exc.value.sub_tag == "admin_risk_unreadable"

    def test_single_entry_verifies(self, repo: Path) -> None:
        _record(repo)
        result = verify_admin_risk_ledger(repo_root=repo, hmac_key=LKEY)
        assert result.ok is True
        assert result.tail_seq_id == 1
        assert result.entries_count == 1
        assert len(result.tail_entry_hash) == 128  # sha3-512 hex

    def test_many_entries_verify(self, repo: Path) -> None:
        for i in range(10):
            _record(repo, payload={"term": f"foo-{i}"})
        result = verify_admin_risk_ledger(repo_root=repo, hmac_key=LKEY)
        assert result.ok is True
        assert result.tail_seq_id == 10
        assert result.entries_count == 10

    def test_returns_monotonicity_result_type(self, repo: Path) -> None:
        _record(repo)
        result = verify_admin_risk_ledger(repo_root=repo, hmac_key=LKEY)
        assert isinstance(result, MonotonicityResult)


# ---------------------------------------------------------------------------
# Failure detection
# ---------------------------------------------------------------------------


class TestVerifyFailures:
    def test_chain_tamper_detected(self, repo: Path) -> None:
        _record(repo)
        _record(repo)
        # Tamper a single byte in the ledger body.
        p = _ledger_path(repo)
        body = p.read_bytes()
        # Flip a byte in the middle of the first line.
        bad = bytearray(body)
        # find first line content byte to corrupt
        first_open_brace = body.find(b"{")
        bad[first_open_brace + 5] = (bad[first_open_brace + 5] + 1) % 256
        p.write_bytes(bytes(bad))
        with pytest.raises(AdminRiskMonotonicityFailed) as exc:
            verify_admin_risk_ledger(repo_root=repo, hmac_key=LKEY)
        assert exc.value.code == F_PRE_10
        # Could surface as trailer_tamper or chain_break depending on which
        # check fires first; both are valid §4.7.3 sub-tags.
        assert exc.value.sub_tag in {
            "admin_risk_chain_break",
            "admin_risk_trailer_tamper",
        }

    def test_trailer_tamper_detected(self, repo: Path) -> None:
        _record(repo)
        # Swap the trailer body's last_entry_hash to break trailer-over-trailer.
        # Trailer file is two canonical-JSON lines (body, then {"trailer_hmac": ...}).
        tp = _trailer_path(repo)
        lines = tp.read_bytes().splitlines()
        body = json.loads(lines[0])
        body["last_entry_hash"] = "0" * 128
        lines[0] = json.dumps(body, separators=(",", ":"), sort_keys=True).encode("utf-8")
        tp.write_bytes(b"\n".join(lines) + b"\n")
        with pytest.raises(AdminRiskMonotonicityFailed) as exc:
            verify_admin_risk_ledger(repo_root=repo, hmac_key=LKEY)
        assert exc.value.code == F_PRE_10
        assert exc.value.sub_tag == "admin_risk_trailer_tamper"

    def test_seq_id_replay_detected(self, repo: Path) -> None:
        # Build a valid ledger then duplicate the last entry line — the
        # duplicate seq_id surfaces as chain_break at the recompute step.
        _record(repo)
        _record(repo)
        p = _ledger_path(repo)
        lines = p.read_bytes().splitlines()
        # Append a duplicate of the final line.
        new_body = b"\n".join(lines + [lines[-1]]) + b"\n"
        p.write_bytes(new_body)
        with pytest.raises(AdminRiskMonotonicityFailed) as exc:
            verify_admin_risk_ledger(repo_root=repo, hmac_key=LKEY)
        assert exc.value.code == F_PRE_10
        assert exc.value.sub_tag in {
            "admin_risk_replayed_seq_id",
            "admin_risk_chain_break",
            "admin_risk_trailer_tamper",
        }

    def test_wrong_hmac_key_detected(self, repo: Path) -> None:
        _record(repo)
        with pytest.raises(AdminRiskMonotonicityFailed) as exc:
            verify_admin_risk_ledger(
                repo_root=repo, hmac_key=b"X" * 32
            )
        assert exc.value.code == F_PRE_10
        assert exc.value.sub_tag == "admin_risk_trailer_tamper"

    def test_missing_trailer_detected(self, repo: Path) -> None:
        _record(repo)
        _trailer_path(repo).unlink()
        with pytest.raises(AdminRiskMonotonicityFailed) as exc:
            verify_admin_risk_ledger(repo_root=repo, hmac_key=LKEY)
        assert exc.value.code == F_PRE_10
        assert exc.value.sub_tag in {
            "admin_risk_unreadable",
            "admin_risk_trailer_tamper",
        }


# ---------------------------------------------------------------------------
# Type gates
# ---------------------------------------------------------------------------


class TestTypeGates:
    def test_repo_root_must_be_path(self, repo: Path) -> None:
        with pytest.raises(TypeError):
            verify_admin_risk_ledger(
                repo_root=str(repo),  # type: ignore[arg-type]
                hmac_key=LKEY,
            )

    def test_hmac_key_must_be_bytes(self, repo: Path) -> None:
        with pytest.raises(TypeError):
            verify_admin_risk_ledger(
                repo_root=repo,
                hmac_key="notbytes",  # type: ignore[arg-type]
            )


# ---------------------------------------------------------------------------
# iter_admin_risk_entries — non-verifying read for POST-gate scan
# ---------------------------------------------------------------------------


class TestIterEntries:
    def test_iterates_in_order(self, repo: Path) -> None:
        for i in range(5):
            _record(repo, payload={"term": f"foo-{i}"})
        entries = list(iter_admin_risk_entries(repo_root=repo))
        assert len(entries) == 5
        assert [e.seq_id for e in entries] == [1, 2, 3, 4, 5]

    def test_empty_ledger_yields_nothing(self, repo: Path) -> None:
        entries = list(iter_admin_risk_entries(repo_root=repo))
        assert entries == []

    def test_yields_admin_risk_entry_instances(self, repo: Path) -> None:
        _record(repo)
        entries = list(iter_admin_risk_entries(repo_root=repo))
        assert isinstance(entries[0], AdminRiskEntry)

    def test_repo_root_must_be_path(self) -> None:
        with pytest.raises(TypeError):
            list(iter_admin_risk_entries(repo_root="/tmp"))  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# count_unresolved_hard_blocks — POST-gate convenience
# ---------------------------------------------------------------------------


class TestCountUnresolvedHardBlocks:
    def test_zero_when_no_red(self, repo: Path) -> None:
        for _ in range(3):
            _record(repo, severity="GREEN")
        for _ in range(2):
            _record(repo, severity="YELLOW")
        entries = list(iter_admin_risk_entries(repo_root=repo))
        assert count_unresolved_hard_blocks(entries) == 0

    def test_counts_red_entries(self, repo: Path) -> None:
        for _ in range(3):
            _record(repo, severity="GREEN")
        _record(repo, severity="RED", retype="i-confirm")
        _record(repo, severity="RED", retype="i-confirm")
        entries = list(iter_admin_risk_entries(repo_root=repo))
        assert count_unresolved_hard_blocks(entries) == 2

    def test_rejects_non_iterable(self) -> None:
        with pytest.raises(TypeError):
            count_unresolved_hard_blocks(42)  # type: ignore[arg-type]

    def test_rejects_non_entry_items(self) -> None:
        with pytest.raises(TypeError):
            count_unresolved_hard_blocks([{"severity": "RED"}])  # type: ignore[list-item]


# ---------------------------------------------------------------------------
# Exception taxonomy
# ---------------------------------------------------------------------------


class TestExceptionTaxonomy:
    def test_admin_risk_monotonicity_failed_carries_sub_tag(
        self, repo: Path
    ) -> None:
        with pytest.raises(AdminRiskMonotonicityFailed) as exc:
            verify_admin_risk_ledger(repo_root=repo, hmac_key=LKEY)
        assert hasattr(exc.value, "code")
        assert hasattr(exc.value, "sub_tag")
        # Full failure ID is computed at the rails-report layer.
        assert exc.value.full_code == f"{F_PRE_10}.{exc.value.sub_tag}"
