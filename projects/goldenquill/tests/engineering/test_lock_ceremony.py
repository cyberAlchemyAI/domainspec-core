"""Tests for pipeline.engineering.lock_ceremony — canonical LOCK entry point.

Covers ``lock()`` composition (verdict-then-append ordering, GateDenied
propagation, asymmetric-args ValueError), result-shape invariants, and the
production-wiring helpers (``make_atomic_jsonl_append``,
``make_daily_log_reader``, ``production_wiring`` tuple shape).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import pytest

from pipeline.engineering.lock_ceremony import (
    BLUEPRINT_DEPS,
    LockCeremonyResult,
    lock,
    make_atomic_jsonl_append,
    make_daily_log_reader,
    production_wiring,
)
from pipeline.harness.gates import (
    AppendLockHistoryResult,
    GateDenied,
    RecordVerdictResult,
)


# ---------------------------------------------------------------------------
# Test doubles (mirror tests/harness/test_gates.py conventions)
# ---------------------------------------------------------------------------


@dataclass
class _FakeClock:
    at: datetime

    def now_utc(self) -> datetime:
        return self.at


@dataclass
class _CapturingAppend:
    calls: list[tuple[str, str]]

    def __call__(self, *, path: str, jsonl_line: str) -> None:
        self.calls.append((path, jsonl_line))


def _fake_daily_log(text: str):
    def reader(today_iso: str) -> str:
        return text

    return reader


def _draft_reader_for(text: str):
    def reader(path: str) -> str:
        return text

    return reader


_CANONICAL_LOCK_BLOCK = """# 2026-04-29 daily log

## LOCK: pipeline.engineering.lock_ceremony

- `lock_timestamp_utc`: 2026-04-29T12:00:00Z
- `committee_round`: self-lock-mvp-run-budget
- `verdict`: SELF-LOCKED
- `code_sha3_512_prefix`: 0000000000000000
- `tests_added_this_module`: 24
- `lines_of_code`: 250
- `findings_surfaced_at_lock`: []
"""


def _canonical_staged_row(**overrides: Any) -> dict:
    row = {
        "module": "pipeline.engineering.lock_ceremony",
        "blueprint_section": "v2.2",
        "verdict": "SELF-LOCKED",
        "backfilled": False,
    }
    row.update(overrides)
    return row


def _ok_setup() -> tuple[_FakeClock, _CapturingAppend, Any]:
    clock = _FakeClock(at=datetime(2026, 4, 29, 12, 0, 0, tzinfo=timezone.utc))
    append = _CapturingAppend(calls=[])
    reader = _fake_daily_log(_CANONICAL_LOCK_BLOCK)
    return clock, append, reader


# ---------------------------------------------------------------------------
# BLUEPRINT_DEPS
# ---------------------------------------------------------------------------


def test_blueprint_deps_pins_v2_2_consolidated() -> None:
    assert "section_04_v2_2_consolidated_amendment.md" in BLUEPRINT_DEPS
    pin = BLUEPRINT_DEPS["section_04_v2_2_consolidated_amendment.md"]
    assert pin["version"] == "v2.2"
    assert pin["hash_sha3_512_prefix16"] == "b643d0540a509715"


# ---------------------------------------------------------------------------
# Happy path — no verdict (self-LOCK / backfill)
# ---------------------------------------------------------------------------


class TestLockHappyPathNoVerdict:
    def test_no_verdict_just_appends(self) -> None:
        clock, append, reader = _ok_setup()
        row = _canonical_staged_row()
        result = lock(
            row=row,
            lock_history_path="/tmp/lock_history.v1.jsonl",
            clock=clock,
            daily_log_reader=reader,
            append_callable=append,
        )
        assert isinstance(result, LockCeremonyResult)
        assert result.record_verdict_result is None
        assert isinstance(result.append_lock_history_result, AppendLockHistoryResult)
        assert len(append.calls) == 1
        path, jsonl_line = append.calls[0]
        assert path == "/tmp/lock_history.v1.jsonl"
        assert json.loads(jsonl_line.rstrip()) == row

    def test_jsonl_line_is_canonical_sorted(self) -> None:
        clock, append, reader = _ok_setup()
        # Out-of-order keys in the input.
        row = {
            "verdict": "SELF-LOCKED",
            "module": "pipeline.engineering.lock_ceremony",
            "blueprint_section": "v2.2",
            "backfilled": False,
        }
        lock(
            row=row,
            lock_history_path="/x",
            clock=clock,
            daily_log_reader=reader,
            append_callable=append,
        )
        _, line = append.calls[0]
        # Harness uses sort_keys=True — assert sorted serialization.
        assert line == json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n"


# ---------------------------------------------------------------------------
# Happy path — with verdict (committee LOCK, no draft)
# ---------------------------------------------------------------------------


class TestLockHappyPathWithVerdictNoDraft:
    def test_verdict_only_record_then_append(self) -> None:
        clock, append, reader = _ok_setup()
        row = _canonical_staged_row()
        result = lock(
            row=row,
            lock_history_path="/x",
            clock=clock,
            daily_log_reader=reader,
            append_callable=append,
            verdict_json={"blocking": False, "seat": "editor"},
        )
        assert result.record_verdict_result is not None
        assert isinstance(result.record_verdict_result, RecordVerdictResult)
        assert result.record_verdict_result.blocking is False
        assert result.record_verdict_result.citation_check_performed is False
        assert len(append.calls) == 1


# ---------------------------------------------------------------------------
# Happy path — with verdict + draft (Judge path, F-AMDT-03 fires)
# ---------------------------------------------------------------------------


class TestLockHappyPathWithDraft:
    def test_judge_verdict_with_citation_check(self) -> None:
        clock, append, reader = _ok_setup()
        # Verdict carries dimension scores citing draft evidence; F-AMDT-03 is
        # satisfied when each scored dimension's evidence string appears in
        # the draft text. Use a single-dimension trivial-pass shape.
        verdict = {
            "blocking": False,
            "dimensions": [
                {"name": "clarity", "score": 9, "evidence": "the quick brown fox"}
            ],
        }
        draft_text = "The quick brown fox jumps over the lazy dog."
        result = lock(
            row=_canonical_staged_row(),
            lock_history_path="/x",
            clock=clock,
            daily_log_reader=reader,
            append_callable=append,
            verdict_json=verdict,
            draft_path="/draft.md",
            draft_reader=_draft_reader_for(draft_text),
        )
        assert result.record_verdict_result is not None
        assert result.record_verdict_result.citation_check_performed is True
        assert len(append.calls) == 1


# ---------------------------------------------------------------------------
# Failure paths — F-AMDT-02 / F-AMDT-03 / F-AMDT-12 deny aborts append
# ---------------------------------------------------------------------------


class TestLockGateDenied:
    def test_f_amdt_02_deny_aborts_before_append(self) -> None:
        clock, append, reader = _ok_setup()
        with pytest.raises(GateDenied) as excinfo:
            lock(
                row=_canonical_staged_row(),
                lock_history_path="/x",
                clock=clock,
                daily_log_reader=reader,
                append_callable=append,
                verdict_json={"not_blocking_key": True},  # missing 'blocking'
            )
        assert excinfo.value.code == "F-AMDT-02"
        # Critical invariant: append must NOT have been invoked.
        assert append.calls == []

    def test_f_amdt_12_deny_when_daily_log_missing_block(self) -> None:
        clock, append, _ = _ok_setup()
        # Daily log present but lacks the canonical LOCK block.
        bad_log = "# 2026-04-29 daily log\n\nNothing relevant here.\n"
        with pytest.raises(GateDenied) as excinfo:
            lock(
                row=_canonical_staged_row(),
                lock_history_path="/x",
                clock=clock,
                daily_log_reader=_fake_daily_log(bad_log),
                append_callable=append,
            )
        assert excinfo.value.code.startswith("F-AMDT-12")
        assert append.calls == []

    def test_f_amdt_12_deny_when_required_fields_missing(self) -> None:
        clock, append, _ = _ok_setup()
        # Block heading present but only some of the 7 required fields.
        partial = (
            "# 2026-04-29\n\n"
            "## LOCK: pipeline.engineering.lock_ceremony\n\n"
            "- `lock_timestamp_utc`: 2026-04-29T12:00:00Z\n"
            "- `verdict`: SELF-LOCKED\n"
        )
        with pytest.raises(GateDenied) as excinfo:
            lock(
                row=_canonical_staged_row(),
                lock_history_path="/x",
                clock=clock,
                daily_log_reader=_fake_daily_log(partial),
                append_callable=append,
            )
        assert excinfo.value.code.startswith("F-AMDT-12")
        assert append.calls == []


# ---------------------------------------------------------------------------
# Programmer-error class (ValueError) — asymmetric draft args
# ---------------------------------------------------------------------------


class TestLockAsymmetricArgs:
    def test_draft_path_without_verdict_raises_value_error(self) -> None:
        clock, append, reader = _ok_setup()
        with pytest.raises(ValueError, match="without verdict_json"):
            lock(
                row=_canonical_staged_row(),
                lock_history_path="/x",
                clock=clock,
                daily_log_reader=reader,
                append_callable=append,
                draft_path="/draft.md",
                draft_reader=_draft_reader_for("text"),
            )
        assert append.calls == []  # nothing fired

    def test_draft_reader_without_verdict_raises_value_error(self) -> None:
        clock, append, reader = _ok_setup()
        with pytest.raises(ValueError, match="without verdict_json"):
            lock(
                row=_canonical_staged_row(),
                lock_history_path="/x",
                clock=clock,
                daily_log_reader=reader,
                append_callable=append,
                draft_reader=_draft_reader_for("text"),
            )

    def test_draft_path_without_draft_reader_raises_value_error(self) -> None:
        # record_verdict's own asymmetry check — draft_path supplied without
        # draft_reader (or vice versa) WHILE verdict_json IS supplied.
        clock, append, reader = _ok_setup()
        with pytest.raises(ValueError, match="must both be supplied"):
            lock(
                row=_canonical_staged_row(),
                lock_history_path="/x",
                clock=clock,
                daily_log_reader=reader,
                append_callable=append,
                verdict_json={"blocking": False},
                draft_path="/draft.md",  # no draft_reader
            )


# ---------------------------------------------------------------------------
# Production wiring helpers
# ---------------------------------------------------------------------------


class TestProductionWiring:
    def test_make_atomic_jsonl_append_writes_to_path(self, tmp_path: Path) -> None:
        target = tmp_path / "lock_history.v1.jsonl"
        appender = make_atomic_jsonl_append()
        appender(path=str(target), jsonl_line='{"a":1}\n')
        appender(path=str(target), jsonl_line='{"b":2}\n')
        content = target.read_text(encoding="utf-8")
        assert content == '{"a":1}\n{"b":2}\n'

    def test_make_atomic_jsonl_append_creates_file_if_absent(
        self, tmp_path: Path
    ) -> None:
        target = tmp_path / "fresh.jsonl"
        assert not target.exists()
        appender = make_atomic_jsonl_append()
        appender(path=str(target), jsonl_line='{"hello":"world"}\n')
        assert target.exists()
        assert target.read_text(encoding="utf-8") == '{"hello":"world"}\n'

    def test_make_daily_log_reader_reads_correct_path(self, tmp_path: Path) -> None:
        (tmp_path / "2026-04-29.md").write_text(
            "log contents", encoding="utf-8"
        )
        reader = make_daily_log_reader(str(tmp_path))
        assert reader("2026-04-29") == "log contents"

    def test_make_daily_log_reader_raises_on_missing(self, tmp_path: Path) -> None:
        reader = make_daily_log_reader(str(tmp_path))
        with pytest.raises(FileNotFoundError):
            reader("2999-12-31")

    def test_production_wiring_returns_4_tuple_with_correct_paths(
        self, tmp_path: Path
    ) -> None:
        clock, reader, appender, lock_history_path = production_wiring(
            repo_root=tmp_path
        )
        assert hasattr(clock, "now_utc")
        assert callable(reader)
        assert callable(appender)
        assert lock_history_path == str(
            tmp_path / "pipeline" / "engineering" / "lock_history.v1.jsonl"
        )

    def test_production_wiring_clock_returns_tz_aware_utc(self, tmp_path: Path) -> None:
        clock, _, _, _ = production_wiring(repo_root=tmp_path)
        now = clock.now_utc()
        assert now.tzinfo is not None
        # Should be very close to actual UTC now — not off by hours.
        delta = abs((datetime.now(tz=timezone.utc) - now).total_seconds())
        assert delta < 5.0


# ---------------------------------------------------------------------------
# End-to-end through production wiring
# ---------------------------------------------------------------------------


class TestEndToEndThroughProductionWiring:
    def test_full_e2e_with_real_filesystem(self, tmp_path: Path) -> None:
        """Dogfood: stand up a workspace layout, run the ceremony, observe
        the row landed in lock_history.v1.jsonl atomic-appended."""
        # Layout
        daily_logs = tmp_path / "daily_logs"
        daily_logs.mkdir()
        engineering = tmp_path / "pipeline" / "engineering"
        engineering.mkdir(parents=True)

        # Today's daily log with canonical LOCK block.
        from datetime import datetime, timezone

        today_iso = datetime.now(tz=timezone.utc).date().isoformat()
        log_text = (
            f"# {today_iso}\n\n"
            "## LOCK: e2e_test_module\n\n"
            f"- `lock_timestamp_utc`: {today_iso}T12:00:00Z\n"
            "- `committee_round`: e2e\n"
            "- `verdict`: SELF-LOCKED\n"
            "- `code_sha3_512_prefix`: deadbeefcafebabe\n"
            "- `tests_added_this_module`: 1\n"
            "- `lines_of_code`: 1\n"
            "- `findings_surfaced_at_lock`: []\n"
        )
        (daily_logs / f"{today_iso}.md").write_text(log_text, encoding="utf-8")

        clock, reader, appender, lock_history_path = production_wiring(
            repo_root=tmp_path
        )
        row = {"module": "e2e_test_module", "verdict": "SELF-LOCKED"}
        result = lock(
            row=row,
            lock_history_path=lock_history_path,
            clock=clock,
            daily_log_reader=reader,
            append_callable=appender,
        )
        # Result shape
        assert result.record_verdict_result is None
        assert result.append_lock_history_result.module == "e2e_test_module"
        # Filesystem
        landed = Path(lock_history_path).read_text(encoding="utf-8")
        assert landed == json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n"
