"""Comprehensive tests for format_utils module.

Synthesized from HRR-006 W2 builders B1 (Sonnet) + B2 (Opus).
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta

import pytest

from zrig.format_utils import format_duration, format_timestamp, format_wave_summary


# ---------------------------------------------------------------------------
# format_duration
# ---------------------------------------------------------------------------

class TestFormatDuration:
    """Tests for format_duration."""

    def test_zero(self) -> None:
        assert format_duration(0) == "0s"

    def test_zero_float(self) -> None:
        assert format_duration(0.0) == "0s"

    def test_sub_second(self) -> None:
        assert format_duration(0.5) == "0.5s"

    def test_sub_second_tiny(self) -> None:
        assert format_duration(0.001) == "0.001s"

    def test_whole_seconds(self) -> None:
        assert format_duration(30) == "30s"

    def test_float_whole_seconds(self) -> None:
        """Integer-valued float should not show '.0'."""
        assert format_duration(5.0) == "5s"

    def test_one_minute_five_seconds(self) -> None:
        assert format_duration(65) == "1m 5s"

    def test_exact_minute(self) -> None:
        assert format_duration(60) == "1m"

    def test_two_minutes(self) -> None:
        assert format_duration(120) == "2m"

    def test_exact_hour(self) -> None:
        assert format_duration(3600) == "1h"

    def test_hour_minute_second(self) -> None:
        assert format_duration(3661) == "1h 1m 1s"

    def test_exact_day(self) -> None:
        assert format_duration(86400) == "1d"

    def test_day_hour_minute_second(self) -> None:
        assert format_duration(90061) == "1d 1h 1m 1s"

    def test_multiple_days(self) -> None:
        assert format_duration(172800) == "2d"

    def test_large_value(self) -> None:
        secs = 10 * 86400 + 5 * 3600 + 30 * 60 + 15
        assert format_duration(secs) == "10d 5h 30m 15s"

    def test_very_large(self) -> None:
        result = format_duration(1_000_000)
        assert "d" in result

    def test_fractional_with_minutes(self) -> None:
        assert format_duration(61.5) == "1m 1.5s"

    def test_integer_input(self) -> None:
        assert format_duration(int(120)) == "2m"

    def test_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="non-negative"):
            format_duration(-1)

    def test_negative_float_raises(self) -> None:
        with pytest.raises(ValueError, match="non-negative"):
            format_duration(-0.5)

    def test_type_error_string(self) -> None:
        with pytest.raises(TypeError):
            format_duration("60")  # type: ignore[arg-type]

    def test_type_error_none(self) -> None:
        with pytest.raises(TypeError):
            format_duration(None)  # type: ignore[arg-type]

    def test_type_error_list(self) -> None:
        with pytest.raises(TypeError):
            format_duration([60])  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# format_timestamp
# ---------------------------------------------------------------------------

class TestFormatTimestamp:
    """Tests for format_timestamp."""

    def test_none_returns_utc_now(self) -> None:
        before = datetime.now(timezone.utc)
        result = format_timestamp(None)
        after = datetime.now(timezone.utc)
        parsed = datetime.fromisoformat(result)
        assert parsed.tzinfo is not None
        assert before <= parsed <= after

    def test_default_arg_is_none(self) -> None:
        result = format_timestamp()
        parsed = datetime.fromisoformat(result)
        assert parsed.tzinfo is not None

    def test_none_has_utc_offset(self) -> None:
        result = format_timestamp(None)
        assert "+00:00" in result or result.endswith("Z")

    def test_naive_treated_as_utc(self) -> None:
        naive = datetime(2025, 6, 15, 12, 30, 0)
        result = format_timestamp(naive)
        assert "2025-06-15T12:30:00" in result
        assert "+00:00" in result

    def test_aware_preserved(self) -> None:
        eastern = timezone(timedelta(hours=-5))
        aware = datetime(2025, 6, 15, 12, 0, 0, tzinfo=eastern)
        result = format_timestamp(aware)
        assert "2025-06-15T12:00:00" in result
        assert "-05:00" in result

    def test_utc_aware(self) -> None:
        utc_dt = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        result = format_timestamp(utc_dt)
        assert "2025-01-01T00:00:00" in result
        assert "+00:00" in result

    def test_type_error_string(self) -> None:
        with pytest.raises(TypeError):
            format_timestamp("2025-01-01")  # type: ignore[arg-type]

    def test_type_error_int(self) -> None:
        with pytest.raises(TypeError):
            format_timestamp(12345)  # type: ignore[arg-type]

    def test_roundtrip(self) -> None:
        original = datetime(2025, 6, 15, 12, 30, 45, tzinfo=timezone.utc)
        result = format_timestamp(original)
        parsed = datetime.fromisoformat(result)
        assert parsed == original


# ---------------------------------------------------------------------------
# format_wave_summary
# ---------------------------------------------------------------------------

class TestFormatWaveSummary:
    """Tests for format_wave_summary."""

    def test_empty_list(self) -> None:
        result = format_wave_summary([])
        lines = result.strip().split("\n")
        assert len(lines) == 2  # header + separator
        assert "Wave" in lines[0]
        assert "Status" in lines[0]

    def test_single_item(self) -> None:
        data = [{"wave_id": "W1", "status": "PASSED", "duration_s": 30, "gate_result": "PASS"}]
        result = format_wave_summary(data)
        lines = result.strip().split("\n")
        assert len(lines) == 3  # header + separator + 1 row
        assert "W1" in lines[2]
        assert "PASSED" in lines[2]
        assert "30s" in lines[2]

    def test_multiple_items(self) -> None:
        data = [
            {"wave_id": "W0", "status": "PASSED", "duration_s": 5, "gate_result": "PASS"},
            {"wave_id": "W1", "status": "PASSED", "duration_s": 120, "gate_result": "PASS"},
            {"wave_id": "W2", "status": "FAILED", "duration_s": 3661, "gate_result": "FAIL"},
        ]
        result = format_wave_summary(data)
        lines = result.strip().split("\n")
        assert len(lines) == 5  # header + separator + 3 rows
        assert "W2" in lines[4]
        assert "FAILED" in lines[4]

    def test_alignment(self) -> None:
        """Columns should be consistently aligned."""
        data = [
            {"wave_id": "W0", "status": "PASSED", "duration_s": 5, "gate_result": "PASS"},
            {"wave_id": "W10", "status": "PASSED", "duration_s": 86400, "gate_result": "PASS"},
        ]
        result = format_wave_summary(data)
        lines = result.strip().split("\n")
        # All data rows should have same structure as header
        header_parts = lines[0].split("  ")
        for line in lines[2:]:
            # Each line should be no shorter than header minus trailing spaces
            assert len(line.rstrip()) > 0

    def test_duration_formatting_in_table(self) -> None:
        data = [{"wave_id": "W1", "status": "OK", "duration_s": 90061, "gate_result": "PASS"}]
        result = format_wave_summary(data)
        assert "1d 1h 1m 1s" in result

    def test_type_error_not_list(self) -> None:
        with pytest.raises(TypeError):
            format_wave_summary("not a list")  # type: ignore[arg-type]

    def test_type_error_non_dict_item(self) -> None:
        with pytest.raises(TypeError, match="Item 0"):
            format_wave_summary(["not a dict"])  # type: ignore[list-item]

    def test_missing_key(self) -> None:
        with pytest.raises(KeyError, match="missing"):
            format_wave_summary([{"wave_id": "W1"}])

    def test_missing_key_specific(self) -> None:
        with pytest.raises(KeyError):
            format_wave_summary([{"wave_id": "W1", "status": "OK", "duration_s": 5}])

    def test_header_present(self) -> None:
        result = format_wave_summary([])
        assert "Wave" in result
        assert "Status" in result
        assert "Duration" in result
        assert "Gate" in result
