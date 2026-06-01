"""Tests for ``pipeline.memory.consolidate_index``.

Threshold gate
--------------
* 19 KB fixture → no-op (under default 20 KB threshold).
* Exactly threshold size → no-op (boundary condition).
* 25 KB fixture → fires; archive written; MEMORY.md shrinks below threshold.

Archive round-trip
------------------
* Archive content parses back to the same archived entries.
* Pointer line on rewritten MEMORY.md is unambiguous and present exactly once.

Lock-history hash-pin
---------------------
* Successful consolidation appends one JSON line with
  ``lock_class=memory_consolidation`` and matching SHA3-512 digests.

The fixtures are synthesized in-test so the suite is hermetic — no
dependency on the live MEMORY.md on disk.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest

from pipeline.memory.consolidate_index import (
    DEFAULT_THRESHOLD_BYTES,
    HARD_LOAD_LIMIT_BYTES,
    MemoryConsolidationError,
    POINTER_PREFIX,
    build_pointer_line,
    consolidate_index,
    parse_memory_index,
    render_archive_markdown,
    render_memory_markdown,
    run_consolidation,
)


# ---------------------------------------------------------------------------
# Fixture builders
# ---------------------------------------------------------------------------


def _make_entry(index: int, length: int) -> str:
    """Produce one realistic MEMORY.md index entry of approx ``length`` bytes.

    Format mirrors the live file: ``- [Title](file.md) — description``.
    """
    title = f"[Locked amendment {index:03d} 2026-05-{(index % 28) + 1:02d}]"
    target = f"(amendment_{index:03d}_locked.md)"
    pad_chars = max(0, length - len(f"- {title}{target} — "))
    body = ("payload " * ((pad_chars // 8) + 1))[: pad_chars]
    return f"- {title}{target} — {body}"


def _build_memory_text(target_size: int) -> str:
    """Build a MEMORY.md string close to ``target_size`` bytes."""
    entries: list[str] = []
    written = 0
    i = 0
    while written < target_size:
        # ~600 bytes per entry — yields enough entries for splitting.
        entry = _make_entry(i, 600)
        entries.append(entry)
        written += len(entry.encode("utf-8")) + 1  # +1 for newline
        i += 1
    text = "\n".join(entries) + "\n"
    return text


def _entries_in(text: str) -> list[str]:
    parsed = parse_memory_index(text)
    return list(parsed.entries)


# ---------------------------------------------------------------------------
# 1. Threshold gate tests
# ---------------------------------------------------------------------------


class TestThresholdGate:
    def test_19kb_input_does_not_fire(self) -> None:
        text = _build_memory_text(19 * 1024)
        size_bytes = len(text.encode("utf-8"))
        # Cap the fixture to <20 KB so we are below the default threshold.
        # (_build_memory_text overshoots by one entry's worth.)
        if size_bytes > DEFAULT_THRESHOLD_BYTES - 200:
            # Trim by dropping last entry to keep under threshold.
            parsed = parse_memory_index(text)
            trimmed = "\n".join(parsed.entries[:-1]) + "\n"
            text = trimmed
            size_bytes = len(text.encode("utf-8"))
        assert size_bytes < DEFAULT_THRESHOLD_BYTES

        result = consolidate_index(
            text,
            consolidation_date="2026-05-15",
        )

        assert result.fired is False
        assert result.original_size_bytes == size_bytes
        assert result.new_size_bytes == size_bytes
        assert result.new_memory_text == text
        assert result.archive_text == ""
        assert result.archive_filename == ""
        assert result.entries_kept == 0
        assert result.entries_archived == 0
        # Round-trip: source_hash equals new_hash on the no-op path.
        assert result.source_memory_sha3_512 == result.new_memory_sha3_512

    def test_boundary_exact_threshold_does_not_fire(self) -> None:
        """Threshold is inclusive — exactly threshold bytes is allowed."""
        text = _build_memory_text(DEFAULT_THRESHOLD_BYTES + 5000)
        # Trim to *exactly* DEFAULT_THRESHOLD_BYTES.
        encoded = text.encode("utf-8")[:DEFAULT_THRESHOLD_BYTES]
        # Recover a valid UTF-8 slice (decode-with-ignore).
        text = encoded.decode("utf-8", errors="ignore")
        size = len(text.encode("utf-8"))
        assert size <= DEFAULT_THRESHOLD_BYTES

        result = consolidate_index(
            text,
            threshold_bytes=size,  # exact boundary
            consolidation_date="2026-05-15",
        )
        assert result.fired is False

    def test_25kb_input_fires(self) -> None:
        text = _build_memory_text(25 * 1024)
        size_bytes = len(text.encode("utf-8"))
        assert size_bytes > DEFAULT_THRESHOLD_BYTES

        result = consolidate_index(
            text,
            consolidation_date="2026-05-15",
        )

        assert result.fired is True
        assert result.original_size_bytes == size_bytes
        assert result.new_size_bytes < size_bytes
        # The consolidation should not leave us above the threshold.
        assert result.new_size_bytes <= DEFAULT_THRESHOLD_BYTES
        assert result.entries_kept > 0
        assert result.entries_archived > 0
        # Split is roughly half-and-half; bottom-half is older entries.
        total = result.entries_kept + result.entries_archived
        assert result.entries_kept == total // 2
        assert result.entries_archived == total - (total // 2)


# ---------------------------------------------------------------------------
# 2. Archive content + round-trip
# ---------------------------------------------------------------------------


class TestArchiveRoundTrip:
    def test_archive_preserves_archived_entries_in_order(self) -> None:
        text = _build_memory_text(25 * 1024)
        original_entries = _entries_in(text)
        result = consolidate_index(
            text,
            consolidation_date="2026-05-15",
        )

        # Archive should parse back to the same archived-entry tail.
        archive_parsed = parse_memory_index(result.archive_text)
        # The archive carries a YAML frontmatter + intro paragraph; the
        # parsed entries list should exactly match the bottom half.
        archive_entries = list(archive_parsed.entries)

        kept_count = result.entries_kept
        expected_archived = original_entries[kept_count:]
        assert archive_entries == expected_archived

    def test_archive_carries_metadata_header(self) -> None:
        text = _build_memory_text(25 * 1024)
        result = consolidate_index(
            text,
            consolidation_date="2026-05-15",
        )
        # Frontmatter is present.
        assert result.archive_text.startswith("---\n")
        assert "archive_kind: memory_consolidation\n" in result.archive_text
        assert "consolidation_date: 2026-05-15\n" in result.archive_text
        assert (
            f"source_memory_sha3_512: {result.source_memory_sha3_512}\n"
            in result.archive_text
        )

    def test_archive_filename_is_date_stamped(self) -> None:
        text = _build_memory_text(25 * 1024)
        result = consolidate_index(
            text,
            consolidation_date="2026-05-15",
        )
        assert result.archive_filename == "_archive_2026-05-15.md"


# ---------------------------------------------------------------------------
# 3. Pointer line on rewritten MEMORY.md
# ---------------------------------------------------------------------------


class TestPointerLine:
    def test_pointer_line_present_exactly_once(self) -> None:
        text = _build_memory_text(25 * 1024)
        result = consolidate_index(
            text,
            consolidation_date="2026-05-15",
        )
        new_lines = result.new_memory_text.splitlines()
        pointer_hits = [ln for ln in new_lines if ln.startswith(POINTER_PREFIX)]
        assert len(pointer_hits) == 1

    def test_pointer_line_references_archive_filename(self) -> None:
        text = _build_memory_text(25 * 1024)
        result = consolidate_index(
            text,
            consolidation_date="2026-05-15",
        )
        # Pointer line is the very first line of the new file.
        first_line = result.new_memory_text.splitlines()[0]
        assert first_line.startswith(POINTER_PREFIX)
        assert result.archive_filename in first_line

    def test_pointer_line_is_grepable_unambiguous_token(self) -> None:
        """The pointer must be machine-distinguishable from a normal entry."""
        text = _build_memory_text(25 * 1024)
        result = consolidate_index(
            text,
            consolidation_date="2026-05-15",
        )
        # Single regex that matches our pointer but no plain index entry.
        pat = re.compile(r"^> ARCHIVED: older entries promoted to `[^`]+`")
        hits = [
            ln for ln in result.new_memory_text.splitlines() if pat.match(ln)
        ]
        assert len(hits) == 1


# ---------------------------------------------------------------------------
# 4. Re-consolidation idempotency
# ---------------------------------------------------------------------------


class TestReconsolidation:
    def test_reconsolidation_does_not_stack_pointers(self) -> None:
        text = _build_memory_text(25 * 1024)
        first = consolidate_index(
            text,
            consolidation_date="2026-05-15",
        )
        # Now grow it back over threshold by appending more entries.
        bumped = first.new_memory_text + "\n".join(
            _make_entry(900 + i, 600) for i in range(20)
        ) + "\n"
        assert len(bumped.encode("utf-8")) > DEFAULT_THRESHOLD_BYTES

        second = consolidate_index(
            bumped,
            consolidation_date="2026-05-16",
        )
        assert second.fired is True
        pointer_hits = [
            ln
            for ln in second.new_memory_text.splitlines()
            if ln.startswith(POINTER_PREFIX)
        ]
        assert len(pointer_hits) == 1


# ---------------------------------------------------------------------------
# 5. Filesystem orchestrator (run_consolidation)
# ---------------------------------------------------------------------------


class TestRunConsolidation:
    def test_run_writes_archive_and_rewrites_memory(self, tmp_path: Path) -> None:
        memory_dir = tmp_path / "memory"
        memory_dir.mkdir()
        memory_path = memory_dir / "MEMORY.md"
        memory_path.write_text(_build_memory_text(25 * 1024), encoding="utf-8")

        outcome = run_consolidation(
            memory_dir,
            consolidation_date="2026-05-15",
        )

        assert outcome.result.fired is True
        assert outcome.archive_path is not None
        assert outcome.archive_path.is_file()
        assert outcome.archive_path.name == "_archive_2026-05-15.md"
        rewritten = memory_path.read_text(encoding="utf-8")
        assert rewritten.splitlines()[0].startswith(POINTER_PREFIX)
        assert len(rewritten.encode("utf-8")) <= DEFAULT_THRESHOLD_BYTES

    def test_run_appends_lock_history_row(self, tmp_path: Path) -> None:
        memory_dir = tmp_path / "memory"
        memory_dir.mkdir()
        memory_path = memory_dir / "MEMORY.md"
        memory_path.write_text(_build_memory_text(25 * 1024), encoding="utf-8")

        lock_history = tmp_path / "lock_history.v1.jsonl"
        lock_history.write_text("", encoding="utf-8")

        outcome = run_consolidation(
            memory_dir,
            consolidation_date="2026-05-15",
            lock_history_path=lock_history,
        )

        assert outcome.lock_history_row_appended is True
        rows = [
            json.loads(ln)
            for ln in lock_history.read_text(encoding="utf-8").splitlines()
            if ln.strip()
        ]
        assert len(rows) == 1
        row = rows[0]
        assert row["lock_class"] == "memory_consolidation"
        assert row["consolidation_date"] == "2026-05-15"
        assert row["entries_kept"] == outcome.result.entries_kept
        assert row["entries_archived"] == outcome.result.entries_archived
        assert (
            row["source_memory_sha3_512"]
            == outcome.result.source_memory_sha3_512
        )
        assert (
            row["new_memory_sha3_512"]
            == outcome.result.new_memory_sha3_512
        )
        assert row["archive_sha3_512"] == outcome.result.archive_sha3_512

    def test_run_under_threshold_is_no_op(self, tmp_path: Path) -> None:
        memory_dir = tmp_path / "memory"
        memory_dir.mkdir()
        memory_path = memory_dir / "MEMORY.md"
        original_text = _build_memory_text(8 * 1024)
        memory_path.write_text(original_text, encoding="utf-8")

        lock_history = tmp_path / "lock_history.v1.jsonl"
        lock_history.write_text("", encoding="utf-8")

        outcome = run_consolidation(
            memory_dir,
            consolidation_date="2026-05-15",
            lock_history_path=lock_history,
        )

        assert outcome.result.fired is False
        assert outcome.lock_history_row_appended is False
        assert memory_path.read_text(encoding="utf-8") == original_text
        # No archive file written.
        archives = list(memory_dir.glob("_archive_*.md"))
        assert archives == []

    def test_run_dry_run_does_not_write(self, tmp_path: Path) -> None:
        memory_dir = tmp_path / "memory"
        memory_dir.mkdir()
        memory_path = memory_dir / "MEMORY.md"
        original = _build_memory_text(25 * 1024)
        memory_path.write_text(original, encoding="utf-8")

        outcome = run_consolidation(
            memory_dir,
            consolidation_date="2026-05-15",
            dry_run=True,
        )
        assert outcome.result.fired is True
        # Live file unchanged.
        assert memory_path.read_text(encoding="utf-8") == original
        # No archive emitted.
        assert not (memory_dir / "_archive_2026-05-15.md").exists()

    def test_run_uniquifies_archive_filename_on_collision(
        self, tmp_path: Path
    ) -> None:
        memory_dir = tmp_path / "memory"
        memory_dir.mkdir()
        memory_path = memory_dir / "MEMORY.md"
        memory_path.write_text(_build_memory_text(25 * 1024), encoding="utf-8")
        # Pre-existing collision.
        (memory_dir / "_archive_2026-05-15.md").write_text(
            "previously consolidated\n", encoding="utf-8"
        )

        outcome = run_consolidation(
            memory_dir,
            consolidation_date="2026-05-15",
        )
        assert outcome.archive_path is not None
        assert outcome.archive_path.name == "_archive_2026-05-15_002.md"


# ---------------------------------------------------------------------------
# 6. Input validation
# ---------------------------------------------------------------------------


class TestInputValidation:
    def test_invalid_threshold_zero_raises(self) -> None:
        with pytest.raises(MemoryConsolidationError):
            consolidate_index(
                "- entry\n",
                threshold_bytes=0,
                consolidation_date="2026-05-15",
            )

    def test_invalid_threshold_above_hard_cap_raises(self) -> None:
        with pytest.raises(MemoryConsolidationError):
            consolidate_index(
                "- entry\n",
                threshold_bytes=HARD_LOAD_LIMIT_BYTES + 1,
                consolidation_date="2026-05-15",
            )

    def test_invalid_date_raises(self) -> None:
        with pytest.raises(MemoryConsolidationError):
            consolidate_index(
                "- entry\n",
                consolidation_date="May 15 2026",
            )

    def test_oversize_with_single_entry_raises(self) -> None:
        # 25 KB of content folded into one entry — cannot split.
        single = "- " + ("x" * (25 * 1024))
        with pytest.raises(MemoryConsolidationError):
            consolidate_index(
                single,
                consolidation_date="2026-05-15",
            )

    def test_archive_filename_must_be_basename(self) -> None:
        text = _build_memory_text(25 * 1024)
        with pytest.raises(MemoryConsolidationError):
            consolidate_index(
                text,
                consolidation_date="2026-05-15",
                archive_filename="../escape.md",
            )

    def test_run_missing_memory_dir_raises(self, tmp_path: Path) -> None:
        with pytest.raises(MemoryConsolidationError):
            run_consolidation(
                tmp_path / "nonexistent_dir",
                consolidation_date="2026-05-15",
            )

    def test_run_missing_memory_file_raises(self, tmp_path: Path) -> None:
        memory_dir = tmp_path / "memory"
        memory_dir.mkdir()
        with pytest.raises(MemoryConsolidationError):
            run_consolidation(
                memory_dir,
                consolidation_date="2026-05-15",
            )


# ---------------------------------------------------------------------------
# 7. SHA3-512 binding
# ---------------------------------------------------------------------------


class TestHashBinding:
    def test_source_hash_matches_input_bytes(self) -> None:
        text = _build_memory_text(25 * 1024)
        result = consolidate_index(
            text,
            consolidation_date="2026-05-15",
        )
        expected = hashlib.sha3_512(text.encode("utf-8")).hexdigest()
        assert result.source_memory_sha3_512 == expected

    def test_new_hash_matches_new_text(self) -> None:
        text = _build_memory_text(25 * 1024)
        result = consolidate_index(
            text,
            consolidation_date="2026-05-15",
        )
        expected = hashlib.sha3_512(
            result.new_memory_text.encode("utf-8")
        ).hexdigest()
        assert result.new_memory_sha3_512 == expected

    def test_archive_hash_matches_archive_text(self) -> None:
        text = _build_memory_text(25 * 1024)
        result = consolidate_index(
            text,
            consolidation_date="2026-05-15",
        )
        expected = hashlib.sha3_512(
            result.archive_text.encode("utf-8")
        ).hexdigest()
        assert result.archive_sha3_512 == expected


# ---------------------------------------------------------------------------
# 8. Renderer building blocks
# ---------------------------------------------------------------------------


class TestRenderers:
    def test_build_pointer_line_format(self) -> None:
        line = build_pointer_line("_archive_2026-05-15.md")
        assert line.startswith("> ARCHIVED: older entries promoted to ")
        assert "`_archive_2026-05-15.md`" in line
        assert "lock_history" in line

    def test_render_memory_markdown_keeps_entry_order(self) -> None:
        kept = (
            "- [A](a.md) — alpha",
            "- [B](b.md) — beta",
            "- [C](c.md) — gamma",
        )
        rendered = render_memory_markdown(
            kept_entries=kept,
            pointer_line=build_pointer_line("_archive_2026-05-15.md"),
        )
        idx_a = rendered.find("- [A]")
        idx_b = rendered.find("- [B]")
        idx_c = rendered.find("- [C]")
        assert 0 < idx_a < idx_b < idx_c

    def test_render_archive_markdown_contains_entries(self) -> None:
        archived = (
            "- [X](x.md) — older entry one",
            "- [Y](y.md) — older entry two",
        )
        text = render_archive_markdown(
            archived_entries=archived,
            consolidation_date="2026-05-15",
            source_memory_sha3_512="a" * 128,
        )
        assert "- [X](x.md) — older entry one" in text
        assert "- [Y](y.md) — older entry two" in text
