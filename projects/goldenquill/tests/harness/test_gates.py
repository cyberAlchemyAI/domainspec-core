"""Tests for pipeline.harness.gates — verdict-ingest + lock_history-append wrappers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping, Optional

import pytest

from pipeline.harness import (
    AppendLockHistoryResult,
    BLUEPRINT_DEPS,
    GateDenied,
    LockHistoryAppendCallable,
    RecordVerdictResult,
    append_lock_history,
    record_verdict,
)
from pipeline.harness import gates as harness_gates


# ---------------------------------------------------------------------------
# Test doubles
# ---------------------------------------------------------------------------


@dataclass
class _FakeClock:
    """Injected ClockProtocol double — returns a fixed UTC datetime."""

    at: datetime
    raise_exc: Optional[BaseException] = None

    def now_utc(self) -> datetime:
        if self.raise_exc is not None:
            raise self.raise_exc
        return self.at


@dataclass
class _CapturingAppend:
    """Injected LockHistoryAppendCallable double — records invocations."""

    calls: list[tuple[str, str]]
    raise_exc: Optional[BaseException] = None

    def __call__(self, *, path: str, jsonl_line: str) -> None:
        if self.raise_exc is not None:
            raise self.raise_exc
        self.calls.append((path, jsonl_line))


def _fake_daily_log(text: Optional[str]):
    """Return a DailyLogReaderCallable that returns ``text`` for every call."""

    def reader(today_iso: str) -> Optional[str]:
        return text

    return reader


def _raising_daily_log(exc: BaseException):
    def reader(today_iso: str) -> Optional[str]:
        raise exc

    return reader


def _draft_reader_for(text: str):
    def reader(path: str) -> str:
        return text

    return reader


def _raising_draft_reader(exc: BaseException):
    def reader(path: str) -> str:
        raise exc

    return reader


# Canonical 7-field LOCK block fixture — matches f_daily_log_lock_block_missing._REQUIRED_FIELDS
_CANONICAL_LOCK_BLOCK = """# 2026-04-21 daily log

## LOCK: pipeline.harness.gates

- `lock_timestamp_utc`: 2026-04-21T12:00:00Z
- `committee_round`: task1-v2-2-wire-2026-04-21
- `verdict`: LOCKED
- `code_sha3_512_prefix`: 0000000000000000
- `tests_added_this_module`: 42
- `lines_of_code`: 300
- `findings_surfaced_at_lock`: []
"""


def _canonical_staged_row(**overrides: Any) -> dict:
    row = {
        "module": "pipeline.harness.gates",
        "blueprint_section": "v2.2",
        "verdict": "LOCKED",
        "backfilled": False,
    }
    row.update(overrides)
    return row


# ===========================================================================
# record_verdict — F-AMDT-02 happy paths
# ===========================================================================


class TestRecordVerdictF_AMDT_02_Pass:
    def test_blocking_true_no_draft(self) -> None:
        result = record_verdict(verdict_json={"blocking": True})
        assert isinstance(result, RecordVerdictResult)
        assert result.blocking is True
        assert result.citation_check_performed is False
        assert result.verdict_json == {"blocking": True}

    def test_blocking_false_no_draft(self) -> None:
        result = record_verdict(verdict_json={"blocking": False})
        assert result.blocking is False
        assert result.citation_check_performed is False

    def test_verdict_dict_with_extra_keys_passes_through(self) -> None:
        verdict = {
            "blocking": True,
            "seat": "editor",
            "summary": "Clean pass",
            "findings": [],
        }
        result = record_verdict(verdict_json=verdict)
        assert result.verdict_json is verdict
        assert result.blocking is True


# ===========================================================================
# record_verdict — F-AMDT-02 fail paths
# ===========================================================================


class TestRecordVerdictF_AMDT_02_Fail:
    def test_non_dict_verdict_denies(self) -> None:
        with pytest.raises(GateDenied) as exc:
            record_verdict(verdict_json="not a dict")
        assert exc.value.code == "F-AMDT-02"
        assert "blocking-key check failed" in exc.value.summary
        assert "verdict_not_dict" in exc.value.summary

    def test_none_verdict_denies(self) -> None:
        with pytest.raises(GateDenied) as exc:
            record_verdict(verdict_json=None)
        assert exc.value.code == "F-AMDT-02"

    def test_dict_missing_blocking_denies(self) -> None:
        with pytest.raises(GateDenied) as exc:
            record_verdict(verdict_json={"seat": "judge"})
        assert exc.value.code == "F-AMDT-02"
        assert "blocking_key_absent" in exc.value.summary

    def test_blocking_string_denies(self) -> None:
        with pytest.raises(GateDenied) as exc:
            record_verdict(verdict_json={"blocking": "true"})
        assert exc.value.code == "F-AMDT-02"
        assert "blocking_value_not_bool" in exc.value.summary

    def test_blocking_int_denies(self) -> None:
        with pytest.raises(GateDenied) as exc:
            record_verdict(verdict_json={"blocking": 1})
        assert exc.value.code == "F-AMDT-02"

    def test_blocking_none_denies(self) -> None:
        with pytest.raises(GateDenied) as exc:
            record_verdict(verdict_json={"blocking": None})
        assert exc.value.code == "F-AMDT-02"

    def test_gate_result_carried_on_exception(self) -> None:
        with pytest.raises(GateDenied) as exc:
            record_verdict(verdict_json={"blocking": 42})
        assert exc.value.gate_result is not None
        from pipeline.logician.gates import BlockingMissingResult

        assert isinstance(exc.value.gate_result, BlockingMissingResult)
        assert exc.value.gate_result.failure_code == "F-AMDT-02"


# ===========================================================================
# record_verdict — F-AMDT-03 happy + fail paths
# ===========================================================================


class TestRecordVerdictF_AMDT_03:
    def _judge_verdict(self, **overrides: Any) -> dict:
        v = {
            "blocking": False,
            "dimensions": [
                {"name": "rigor", "evidence": "the draft says rigorous"},
                {"name": "novelty", "evidence": "draft says novel"},
            ],
        }
        v.update(overrides)
        return v

    def test_citation_check_skipped_when_no_draft_path(self) -> None:
        # Dimensions with broken evidence — but no draft_path → F-AMDT-03 not run
        verdict = {
            "blocking": False,
            "dimensions": [{"name": "x", "evidence": "nonexistent tokens"}],
        }
        result = record_verdict(verdict_json=verdict)
        assert result.citation_check_performed is False

    def test_citation_check_performed_when_draft_supplied(self) -> None:
        verdict = self._judge_verdict()
        result = record_verdict(
            verdict_json=verdict,
            draft_path="/fake/draft.md",
            draft_reader=_draft_reader_for(
                "the draft says rigorous and the draft says novel"
            ),
        )
        assert result.citation_check_performed is True
        assert result.blocking is False

    def test_missing_evidence_token_denies(self) -> None:
        verdict = self._judge_verdict(
            dimensions=[
                {"name": "x", "evidence": "tokens-not-in-draft"},
            ]
        )
        with pytest.raises(GateDenied) as exc:
            record_verdict(
                verdict_json=verdict,
                draft_path="/fake/draft.md",
                draft_reader=_draft_reader_for("completely unrelated text"),
            )
        assert exc.value.code == "F-AMDT-03"
        assert "1 dimension(s) failed citation check" in exc.value.summary

    def test_draft_reader_raises_denies(self) -> None:
        verdict = self._judge_verdict()
        with pytest.raises(GateDenied) as exc:
            record_verdict(
                verdict_json=verdict,
                draft_path="/fake/draft.md",
                draft_reader=_raising_draft_reader(FileNotFoundError("no draft")),
            )
        assert exc.value.code == "F-AMDT-03"
        assert "draft reader raised" in exc.value.summary
        assert "FileNotFoundError" in exc.value.summary

    def test_f_amdt_02_precedes_f_amdt_03(self) -> None:
        # Non-dict verdict — F-AMDT-02 fires first, F-AMDT-03 never invoked
        reader_calls: list[str] = []

        def counting_reader(path: str) -> str:
            reader_calls.append(path)
            return "whatever"

        with pytest.raises(GateDenied) as exc:
            record_verdict(
                verdict_json=None,
                draft_path="/fake/draft.md",
                draft_reader=counting_reader,
            )
        assert exc.value.code == "F-AMDT-02"
        assert reader_calls == []

    def test_dimensions_absent_with_draft_denies(self) -> None:
        # blocking=bool (F-AMDT-02 PASS) but dimensions key absent → F-AMDT-03 FAIL
        with pytest.raises(GateDenied) as exc:
            record_verdict(
                verdict_json={"blocking": True},
                draft_path="/fake/draft.md",
                draft_reader=_draft_reader_for(""),
            )
        assert exc.value.code == "F-AMDT-03"

    def test_empty_dimensions_passes(self) -> None:
        # blocking=bool + dimensions=[] — no dimensions to check → PASS
        result = record_verdict(
            verdict_json={"blocking": False, "dimensions": []},
            draft_path="/fake/draft.md",
            draft_reader=_draft_reader_for(""),
        )
        assert result.citation_check_performed is True
        assert result.blocking is False


# ===========================================================================
# record_verdict — asymmetric-args programmer-error path
# ===========================================================================


class TestRecordVerdictAsymmetricArgs:
    def test_draft_path_without_reader_raises_value_error(self) -> None:
        with pytest.raises(ValueError) as exc:
            record_verdict(
                verdict_json={"blocking": True},
                draft_path="/fake/draft.md",
            )
        assert "both be supplied or both be None" in str(exc.value)

    def test_reader_without_path_raises_value_error(self) -> None:
        with pytest.raises(ValueError):
            record_verdict(
                verdict_json={"blocking": True},
                draft_reader=_draft_reader_for(""),
            )

    def test_neither_supplied_ok(self) -> None:
        result = record_verdict(verdict_json={"blocking": True})
        assert result.citation_check_performed is False

    def test_both_supplied_ok(self) -> None:
        result = record_verdict(
            verdict_json={"blocking": True, "dimensions": []},
            draft_path="/fake",
            draft_reader=_draft_reader_for(""),
        )
        assert result.citation_check_performed is True

    def test_asymmetric_check_precedes_f_amdt_02(self) -> None:
        # Even with a bogus verdict, asymmetric-args error fires first
        # (it's a programmer-contract error, not a policy denial).
        with pytest.raises(ValueError):
            record_verdict(verdict_json="bogus", draft_path="/fake")


# ===========================================================================
# append_lock_history — F-AMDT-12 happy path + carve-out
# ===========================================================================


class TestAppendLockHistoryHappyPath:
    def _clock(self) -> _FakeClock:
        return _FakeClock(at=datetime(2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc))

    def test_pass_routes_to_append_callable(self) -> None:
        captured = _CapturingAppend(calls=[])
        row = _canonical_staged_row()
        result = append_lock_history(
            row=row,
            lock_history_path="/fake/lock_history.v1.jsonl",
            clock=self._clock(),
            daily_log_reader=_fake_daily_log(_CANONICAL_LOCK_BLOCK),
            append_callable=captured,
        )
        assert isinstance(result, AppendLockHistoryResult)
        assert result.module == "pipeline.harness.gates"
        assert result.today_iso == "2026-04-21"
        assert result.backfill_carveout_applied is False
        assert len(captured.calls) == 1
        path, line = captured.calls[0]
        assert path == "/fake/lock_history.v1.jsonl"
        # Round-trip JSON — sort_keys + compact separators
        parsed = json.loads(line)
        assert parsed == row
        # Canonical form check
        assert line.endswith("\n")
        assert ": " not in line  # compact separator convention

    def test_backfill_carveout_skips_daily_log_check(self) -> None:
        captured = _CapturingAppend(calls=[])
        row = _canonical_staged_row(
            backfilled=True, verdict="LOCKED-backfilled"
        )
        # Daily log is ABSENT (None) — but carve-out applies, so PASS
        result = append_lock_history(
            row=row,
            lock_history_path="/fake/lock_history.v1.jsonl",
            clock=self._clock(),
            daily_log_reader=_fake_daily_log(None),
            append_callable=captured,
        )
        assert result.backfill_carveout_applied is True
        assert result.today_iso is None  # skipped in carve-out branch
        assert len(captured.calls) == 1

    def test_half_backfill_marker_runs_full_gate(self) -> None:
        # backfilled=True but verdict != "LOCKED-backfilled" → full gate
        captured = _CapturingAppend(calls=[])
        row = _canonical_staged_row(backfilled=True, verdict="LOCKED")
        result = append_lock_history(
            row=row,
            lock_history_path="/fake/path",
            clock=self._clock(),
            daily_log_reader=_fake_daily_log(_CANONICAL_LOCK_BLOCK),
            append_callable=captured,
        )
        assert result.backfill_carveout_applied is False
        assert result.today_iso == "2026-04-21"

    def test_json_canonicalisation_is_stable(self) -> None:
        # Different insertion orders → same JSONL line
        captured_a = _CapturingAppend(calls=[])
        captured_b = _CapturingAppend(calls=[])
        row_a = {
            "module": "pipeline.harness.gates",
            "verdict": "LOCKED",
            "backfilled": False,
        }
        row_b = {
            "backfilled": False,
            "verdict": "LOCKED",
            "module": "pipeline.harness.gates",
        }
        for row, cap in ((row_a, captured_a), (row_b, captured_b)):
            append_lock_history(
                row=row,
                lock_history_path="/fake/p",
                clock=self._clock(),
                daily_log_reader=_fake_daily_log(_CANONICAL_LOCK_BLOCK),
                append_callable=cap,
            )
        assert captured_a.calls[0][1] == captured_b.calls[0][1]


# ===========================================================================
# append_lock_history — F-AMDT-12 fail paths
# ===========================================================================


class TestAppendLockHistoryFail:
    def _clock(self) -> _FakeClock:
        return _FakeClock(at=datetime(2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc))

    def test_missing_module_field_denies(self) -> None:
        captured = _CapturingAppend(calls=[])
        with pytest.raises(GateDenied) as exc:
            append_lock_history(
                row={"verdict": "LOCKED"},
                lock_history_path="/p",
                clock=self._clock(),
                daily_log_reader=_fake_daily_log(_CANONICAL_LOCK_BLOCK),
                append_callable=captured,
            )
        assert exc.value.code == "F-AMDT-12"
        assert "no 'module' field" in exc.value.summary
        assert captured.calls == []

    def test_empty_module_field_denies(self) -> None:
        with pytest.raises(GateDenied) as exc:
            append_lock_history(
                row={"module": ""},
                lock_history_path="/p",
                clock=self._clock(),
                daily_log_reader=_fake_daily_log(_CANONICAL_LOCK_BLOCK),
                append_callable=_CapturingAppend(calls=[]),
            )
        assert exc.value.code == "F-AMDT-12"

    def test_daily_log_absent_denies(self) -> None:
        with pytest.raises(GateDenied) as exc:
            append_lock_history(
                row=_canonical_staged_row(),
                lock_history_path="/p",
                clock=self._clock(),
                daily_log_reader=_fake_daily_log(None),
                append_callable=_CapturingAppend(calls=[]),
            )
        assert exc.value.code == "F-AMDT-12-MISSING"
        assert "2026-04-21 does not exist" in exc.value.summary

    def test_no_lock_heading_denies(self) -> None:
        log_text = "# 2026-04-21 daily log\n\nNo lock block today.\n"
        with pytest.raises(GateDenied) as exc:
            append_lock_history(
                row=_canonical_staged_row(),
                lock_history_path="/p",
                clock=self._clock(),
                daily_log_reader=_fake_daily_log(log_text),
                append_callable=_CapturingAppend(calls=[]),
            )
        assert exc.value.code == "F-AMDT-12-MISSING"
        assert "no '## LOCK: pipeline.harness.gates' heading" in exc.value.summary

    def test_malformed_block_missing_fields_denies(self) -> None:
        log_text = (
            "# 2026-04-21 daily log\n\n"
            "## LOCK: pipeline.harness.gates\n\n"
            "- `lock_timestamp_utc`: 2026-04-21T12:00:00Z\n"
            # ... missing the other 6 fields ...
        )
        with pytest.raises(GateDenied) as exc:
            append_lock_history(
                row=_canonical_staged_row(),
                lock_history_path="/p",
                clock=self._clock(),
                daily_log_reader=_fake_daily_log(log_text),
                append_callable=_CapturingAppend(calls=[]),
            )
        assert exc.value.code == "F-AMDT-12-MALFORMED"
        assert "malformed" in exc.value.summary.lower()
        assert "committee_round" in exc.value.summary

    def test_clock_raises_denies_with_reader_fail_code(self) -> None:
        bad_clock = _FakeClock(
            at=datetime(2026, 4, 21, tzinfo=timezone.utc),
            raise_exc=RuntimeError("clock broken"),
        )
        with pytest.raises(GateDenied) as exc:
            append_lock_history(
                row=_canonical_staged_row(),
                lock_history_path="/p",
                clock=bad_clock,
                daily_log_reader=_fake_daily_log(_CANONICAL_LOCK_BLOCK),
                append_callable=_CapturingAppend(calls=[]),
            )
        assert exc.value.code == "F-AMDT-12-READER-FAIL"
        assert "clock raised" in exc.value.summary
        assert "clock broken" in exc.value.summary

    def test_daily_log_reader_raises_denies(self) -> None:
        with pytest.raises(GateDenied) as exc:
            append_lock_history(
                row=_canonical_staged_row(),
                lock_history_path="/p",
                clock=self._clock(),
                daily_log_reader=_raising_daily_log(
                    PermissionError("forbidden")
                ),
                append_callable=_CapturingAppend(calls=[]),
            )
        assert exc.value.code == "F-AMDT-12-READER-FAIL"
        assert "daily log reader raised" in exc.value.summary
        assert "PermissionError" in exc.value.summary

    def test_denial_never_invokes_append_callable(self) -> None:
        captured = _CapturingAppend(calls=[])
        with pytest.raises(GateDenied):
            append_lock_history(
                row=_canonical_staged_row(),
                lock_history_path="/p",
                clock=self._clock(),
                daily_log_reader=_fake_daily_log(None),
                append_callable=captured,
            )
        assert captured.calls == []

    def test_gate_result_carried_on_exception(self) -> None:
        from pipeline.logician.gates import DailyLogBlockResult

        with pytest.raises(GateDenied) as exc:
            append_lock_history(
                row=_canonical_staged_row(),
                lock_history_path="/p",
                clock=self._clock(),
                daily_log_reader=_fake_daily_log(None),
                append_callable=_CapturingAppend(calls=[]),
            )
        assert isinstance(exc.value.gate_result, DailyLogBlockResult)
        assert exc.value.gate_result.failure_code == "F-AMDT-12-MISSING"


# ===========================================================================
# append_lock_history — append_callable failure propagates
# ===========================================================================


class TestAppendLockHistoryAppendFailure:
    def _clock(self) -> _FakeClock:
        return _FakeClock(at=datetime(2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc))

    def test_append_callable_exception_propagates_unwrapped(self) -> None:
        appender = _CapturingAppend(
            calls=[], raise_exc=OSError("disk full")
        )
        with pytest.raises(OSError) as exc:
            append_lock_history(
                row=_canonical_staged_row(),
                lock_history_path="/p",
                clock=self._clock(),
                daily_log_reader=_fake_daily_log(_CANONICAL_LOCK_BLOCK),
                append_callable=appender,
            )
        # NOT wrapped in GateDenied — append failure is the ceremony's fault
        # category, not a gate denial.
        assert "disk full" in str(exc.value)

    def test_append_callable_exception_is_not_gate_denied(self) -> None:
        appender = _CapturingAppend(calls=[], raise_exc=OSError("boom"))
        with pytest.raises(OSError):
            append_lock_history(
                row=_canonical_staged_row(),
                lock_history_path="/p",
                clock=self._clock(),
                daily_log_reader=_fake_daily_log(_CANONICAL_LOCK_BLOCK),
                append_callable=appender,
            )
        # Confirm it's truly not GateDenied
        with pytest.raises(OSError) as exc:
            append_lock_history(
                row=_canonical_staged_row(),
                lock_history_path="/p",
                clock=self._clock(),
                daily_log_reader=_fake_daily_log(_CANONICAL_LOCK_BLOCK),
                append_callable=appender,
            )
        assert not isinstance(exc.value, GateDenied)


# ===========================================================================
# GateDenied shape
# ===========================================================================


class TestGateDenied:
    def test_is_runtime_error(self) -> None:
        e = GateDenied(code="F-AMDT-02", gate_result=None, summary="x")
        assert isinstance(e, RuntimeError)

    def test_carries_code_result_summary(self) -> None:
        e = GateDenied(code="F-AMDT-12", gate_result={"x": 1}, summary="hello")
        assert e.code == "F-AMDT-12"
        assert e.gate_result == {"x": 1}
        assert e.summary == "hello"

    def test_str_includes_code_and_summary(self) -> None:
        e = GateDenied(code="F-AMDT-03", gate_result=None, summary="missing evidence")
        assert "F-AMDT-03" in str(e)
        assert "missing evidence" in str(e)


# ===========================================================================
# LockHistoryAppendCallable Protocol isinstance behaviour
# ===========================================================================


class TestLockHistoryAppendCallableProtocol:
    def test_function_passes_isinstance(self) -> None:
        def appender(*, path: str, jsonl_line: str) -> None:
            return None

        assert isinstance(appender, LockHistoryAppendCallable)

    def test_capturing_dataclass_passes_isinstance(self) -> None:
        assert isinstance(_CapturingAppend(calls=[]), LockHistoryAppendCallable)

    def test_plain_object_fails_isinstance(self) -> None:
        assert not isinstance(object(), LockHistoryAppendCallable)


# ===========================================================================
# Public surface contract
# ===========================================================================


class TestPublicSurface:
    def test_all_exports_importable(self) -> None:
        from pipeline.harness import __all__ as exports

        for name in exports:
            assert hasattr(harness_gates, name) or name in {
                "BLUEPRINT_DEPS",
            }

    def test_blueprint_deps_carries_v2_2_pin(self) -> None:
        assert "section_04_v2_2_consolidated_amendment.md" in BLUEPRINT_DEPS
        entry = BLUEPRINT_DEPS["section_04_v2_2_consolidated_amendment.md"]
        assert entry["hash_sha3_512_prefix16"] == "b643d0540a509715"
        assert entry["version"] == "v2.2 LOCKED 2026-04-21"
        wired = entry["gates_wired"]
        assert isinstance(wired, tuple)
        assert any("F-AMDT-02" in g for g in wired)
        assert any("F-AMDT-03" in g for g in wired)
        assert any("F-AMDT-12" in g for g in wired)

    def test_record_verdict_result_is_frozen(self) -> None:
        r = RecordVerdictResult(
            verdict_json={"blocking": True},
            blocking=True,
            citation_check_performed=False,
        )
        with pytest.raises(Exception):
            r.blocking = False  # type: ignore[misc]

    def test_append_lock_history_result_is_frozen(self) -> None:
        r = AppendLockHistoryResult(
            module="x", today_iso="2026-04-21", backfill_carveout_applied=False
        )
        with pytest.raises(Exception):
            r.module = "y"  # type: ignore[misc]


# ===========================================================================
# Adversarial / integration
# ===========================================================================


class TestAdversarial:
    def _clock(self) -> _FakeClock:
        return _FakeClock(at=datetime(2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc))

    def test_verdict_with_embedded_newlines_serialises(self) -> None:
        captured = _CapturingAppend(calls=[])
        row = _canonical_staged_row(notes="line1\nline2")
        append_lock_history(
            row=row,
            lock_history_path="/p",
            clock=self._clock(),
            daily_log_reader=_fake_daily_log(_CANONICAL_LOCK_BLOCK),
            append_callable=captured,
        )
        # json.dumps escapes newlines → single-line JSONL
        line = captured.calls[0][1]
        assert line.count("\n") == 1  # only the trailing one
        assert "\\n" in line

    def test_record_verdict_judge_end_to_end_pass(self) -> None:
        # Full Judge-shaped verdict with multi-token evidence
        draft = (
            "The applicant demonstrates rigor through empirical data. "
            "Novelty is shown by three prior-art citations."
        )
        verdict = {
            "blocking": False,
            "dimensions": [
                {"name": "rigor", "evidence": "demonstrates rigor through"},
                {"name": "novelty", "evidence": "three prior-art citations"},
            ],
        }
        result = record_verdict(
            verdict_json=verdict,
            draft_path="/mock/draft.md",
            draft_reader=_draft_reader_for(draft),
        )
        assert result.citation_check_performed is True
        assert result.blocking is False

    def test_lock_history_atomic_serialisation_round_trip(self) -> None:
        captured = _CapturingAppend(calls=[])
        row = _canonical_staged_row(
            module="pipeline.harness.gates",
            lines_of_code=287,
            tests_added=42,
            blueprint_section="§4 v2.2",
        )
        append_lock_history(
            row=row,
            lock_history_path="/abs/path.jsonl",
            clock=self._clock(),
            daily_log_reader=_fake_daily_log(_CANONICAL_LOCK_BLOCK),
            append_callable=captured,
        )
        parsed = json.loads(captured.calls[0][1])
        assert parsed == row

    def test_summary_covers_all_daily_log_reason_tags(self) -> None:
        # Exercise every non-pragma summary branch in _summarize_daily_log_block
        from pipeline.harness.gates import _summarize_daily_log_block
        from pipeline.logician.gates import DailyLogBlockDetail, DailyLogBlockResult

        def mk(reason: str, **k: Any) -> DailyLogBlockResult:
            defaults: dict[str, Any] = {
                "reason_tag": reason,
                "staged_module": "m",
                "today_iso": "2026-04-21",
                "missing_fields": (),
                "reader_error": None,
            }
            defaults.update(k)
            return DailyLogBlockResult(
                success=False,
                failure_code="F-AMDT-12",
                detail=DailyLogBlockDetail(**defaults),
            )

        assert "malformed" in _summarize_daily_log_block(
            mk(
                "lock_block_required_fields_missing",
                missing_fields=("a", "b"),
            )
        ).lower()
        assert "heading" in _summarize_daily_log_block(
            mk("lock_block_heading_not_found")
        )
        assert "does not exist" in _summarize_daily_log_block(
            mk("daily_log_absent_for_today")
        )
        assert "no 'module' field" in _summarize_daily_log_block(
            mk("staged_row_module_missing")
        )
        assert "clock raised" in _summarize_daily_log_block(
            mk("clock_raised", reader_error="broken")
        )
        assert "daily log reader raised" in _summarize_daily_log_block(
            mk("daily_log_reader_raised", reader_error="nope")
        )

    def test_summary_covers_citation_reason_tags(self) -> None:
        from pipeline.harness.gates import _summarize_citation
        from pipeline.logician.gates import (
            CitationMissingDetail,
            CitationMissingResult,
            DimensionCitationFailure,
        )

        # Reader-raised
        r1 = CitationMissingResult(
            success=False,
            failure_code="F-AMDT-03",
            detail=CitationMissingDetail(
                reason_tag="draft_reader_raised",
                failed_dimensions=(),
                reader_error="FileNotFoundError: x",
            ),
        )
        assert "draft reader raised" in _summarize_citation(r1)

        # Structural (no failed dimensions)
        r2 = CitationMissingResult(
            success=False,
            failure_code="F-AMDT-03",
            detail=CitationMissingDetail(
                reason_tag="dimensions_key_absent",
                failed_dimensions=(),
                reader_error=None,
            ),
        )
        assert "dimensions_key_absent" in _summarize_citation(r2)

        # With failed dimensions
        r3 = CitationMissingResult(
            success=False,
            failure_code="F-AMDT-03",
            detail=CitationMissingDetail(
                reason_tag="evidence_tokens_unresolved",
                failed_dimensions=(
                    DimensionCitationFailure(
                        dimension_index=0,
                        dimension_name="rigor",
                        reason_tag="evidence_tokens_unresolved",
                        missing_tokens=("foo", "bar"),
                    ),
                ),
                reader_error=None,
            ),
        )
        assert "1 dimension(s) failed" in _summarize_citation(r3)
