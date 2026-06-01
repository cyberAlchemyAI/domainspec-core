"""MEMORY.md auto-consolidation.

Scope
-----
The Cowork auto-memory loader reads ``MEMORY.md`` at every session start.
The loader hard-caps the file at ~24.4 KB; anything past that is silently
dropped (observed live on 2026-05-15 — see assessment Dim 8 / Tier-0 item
3 of 3). This module promotes the bottom-half oldest entries into a
date-stamped archive index whenever ``MEMORY.md`` exceeds a configurable
soft threshold (default 20 KB).

Discipline
----------
* Pure-Python; no third-party imports. (Avoids substrate-pin drag at v0.1
  Beta finalization.)
* Hash-pin each consolidation as a lock_history row of
  ``lock_class=memory_consolidation`` for audit-trail discipline (parallels
  the WS-L precedent for non-blueprint LANDED events).
* Deterministic ordering — entries are emitted to the archive in the same
  index order they appeared in MEMORY.md, after stable splitting at the
  midpoint.
* Round-trippable — the archive file is itself a Markdown index that can
  be re-loaded and (in principle) consolidated again. The pointer line on
  MEMORY.md is unambiguous and grep-able.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Sequence


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


# The Cowork auto-memory loader's observed hard cap. Documented in the
# 2026-05-11 assessment Dim 8 evidence pack.
HARD_LOAD_LIMIT_BYTES: int = 24576  # 24 KiB; the loader log says "24.4 KB"
                                    # → ceil(24400/1024)*1024 == 24 KiB rounded


# Default soft threshold — safety margin under the hard cap. Configurable
# via ``run_consolidation(threshold_bytes=...)``.
DEFAULT_THRESHOLD_BYTES: int = 20480  # 20 KiB


# Sentinel prefix prepended to MEMORY.md after consolidation. Unambiguous
# and machine-parseable. Single-line.
POINTER_PREFIX: str = "> ARCHIVED: older entries promoted to "


# Sentinel suffix in the pointer line — closes the human prose.
POINTER_SUFFIX: str = (
    " — call `tilth memory consolidate-index` to re-roll; "
    "see lock_history for hash-pin."
)


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class MemoryConsolidationError(Exception):
    """Raised when MEMORY.md cannot be consolidated cleanly."""


# ---------------------------------------------------------------------------
# Parsed-index dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ParsedMemoryIndex:
    """Parsed MEMORY.md state.

    Attributes
    ----------
    preamble_lines
        Lines preceding the first index entry. May include a prior pointer
        line; consolidation strips and re-emits a fresh pointer to keep
        the file unambiguous (no stacked pointers).
    entries
        Each index entry as a single source-form string (newline-stripped).
        Order is preserved exactly as in the input.
    trailing_lines
        Lines after the last entry — typically empty or a single trailing
        blank. Preserved for round-trip safety.
    """

    preamble_lines: tuple[str, ...] = field(default_factory=tuple)
    entries: tuple[str, ...] = field(default_factory=tuple)
    trailing_lines: tuple[str, ...] = field(default_factory=tuple)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def parse_memory_index(text: str) -> ParsedMemoryIndex:
    """Parse a MEMORY.md source string into preamble / entries / trailer.

    An "entry" is a top-level Markdown list item — a line starting with
    ``- `` (dash + space) at column zero. Continuation lines (indented or
    blank lines inside an entry) are folded into the entry that precedes
    them, preserving the original whitespace.

    Pointer lines (``POINTER_PREFIX``) and the legacy WARNING blockquote
    are stripped from the preamble on parse so that re-consolidation does
    not stack pointer lines or rewrite the warning twice.
    """
    lines = text.splitlines(keepends=False)
    preamble: list[str] = []
    entries: list[str] = []
    trailing: list[str] = []

    i = 0
    n = len(lines)

    # 1) Collect preamble (everything before the first ``- `` line).
    while i < n and not lines[i].startswith("- "):
        preamble.append(lines[i])
        i += 1

    # 2) Walk entries — each starts at ``- `` column zero; continuation
    #    lines (indented or empty mid-entry) fold into the current entry.
    current: list[str] = []
    while i < n:
        line = lines[i]
        if line.startswith("- "):
            if current:
                entries.append("\n".join(current))
                current = []
            current.append(line)
            i += 1
            continue
        if line.startswith(("  ", "\t")) or line.strip() == "":
            # Continuation OR mid-entry blank — fold in.
            current.append(line)
            i += 1
            continue
        # Non-entry, non-continuation — end of index region.
        break
    if current:
        entries.append("\n".join(current))

    # 3) Collect trailing lines (everything else).
    while i < n:
        trailing.append(lines[i])
        i += 1

    # Strip a stale pointer line and the legacy WARNING blockquote from
    # the preamble — re-consolidation re-emits both deterministically.
    cleaned_preamble = tuple(
        ln
        for ln in preamble
        if not ln.startswith(POINTER_PREFIX)
        and not ln.startswith("> WARNING: MEMORY.md is")
    )

    # Strip trailing-region pointer / WARNING leftovers too (defensive —
    # the live MEMORY.md observed 2026-05-15 has the WARNING after the
    # entries, not before).
    cleaned_trailing = tuple(
        ln
        for ln in trailing
        if not ln.startswith(POINTER_PREFIX)
        and not ln.startswith("> WARNING: MEMORY.md is")
    )

    # Collapse trailing all-blank runs to a single blank for stable render.
    while cleaned_trailing and cleaned_trailing[-1].strip() == "":
        cleaned_trailing = cleaned_trailing[:-1]

    return ParsedMemoryIndex(
        preamble_lines=cleaned_preamble,
        entries=tuple(entries),
        trailing_lines=cleaned_trailing,
    )


# ---------------------------------------------------------------------------
# Splitting
# ---------------------------------------------------------------------------


def _split_bottom_half_oldest(
    entries: Sequence[str],
    *,
    threshold_bytes: Optional[int] = None,
    overhead_bytes: int = 0,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Return (kept_at_top, archived_at_bottom).

    MEMORY.md convention: newest entries appear at the top (operators
    prepend new index lines per the guidance in CLAUDE.md auto-memory
    section). The bottom half of the list is therefore the *oldest*
    entries by convention.

    The split is *at least* the bottom half (contract: bottom-half oldest
    entries are always promoted). When ``threshold_bytes`` is supplied and
    the kept half still exceeds the threshold (entries are unusually long
    — observed live on 2026-05-15 with ~36 KB of long lock-LOCK summary
    entries), the splitter promotes additional oldest entries from the
    kept set one-at-a-time until the kept portion fits OR only one entry
    remains. This honors the "consolidation actually brings MEMORY.md
    below threshold" intent of the discipline.

    ``overhead_bytes`` is the size of the pointer line + preamble +
    trailer + structural newlines that the renderer adds on top of the
    kept entries; the caller supplies it so the size check matches the
    real rendered output, not just the raw entry byte count.
    """
    n = len(entries)
    if n <= 1:
        return tuple(entries), ()
    midpoint = n // 2
    kept = list(entries[:midpoint])
    archived = list(entries[midpoint:])

    if threshold_bytes is not None:
        # Greedy step: while the kept portion (plus structural overhead)
        # still exceeds the threshold, promote one more oldest entry
        # from the tail of kept into the head of archived.
        while len(kept) > 1:
            kept_size = (
                sum(len(e.encode("utf-8")) for e in kept)
                + max(0, len(kept) - 1)  # newlines between entries
                + overhead_bytes
            )
            if kept_size <= threshold_bytes:
                break
            archived.insert(0, kept.pop())

    return tuple(kept), tuple(archived)


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def build_pointer_line(archive_filename: str) -> str:
    """Render the single pointer line prepended to MEMORY.md."""
    return f"{POINTER_PREFIX}`{archive_filename}`{POINTER_SUFFIX}"


def render_memory_markdown(
    kept_entries: Sequence[str],
    *,
    pointer_line: str,
    preamble_lines: Sequence[str] = (),
    trailing_lines: Sequence[str] = (),
) -> str:
    """Render the rewritten MEMORY.md with pointer line on top."""
    parts: list[str] = [pointer_line, ""]
    if preamble_lines:
        parts.extend(preamble_lines)
        if preamble_lines and preamble_lines[-1].strip() != "":
            parts.append("")
    parts.extend(kept_entries)
    if trailing_lines:
        # Ensure a separating blank between last entry and trailer.
        if kept_entries:
            parts.append("")
        parts.extend(trailing_lines)
    # Always emit exactly one trailing newline.
    return "\n".join(parts).rstrip("\n") + "\n"


def render_archive_markdown(
    archived_entries: Sequence[str],
    *,
    consolidation_date: str,
    source_memory_sha3_512: str,
    parent_archive_filename: Optional[str] = None,
) -> str:
    """Render the archive file.

    Carries a YAML-frontmatter-style header with consolidation metadata so
    consumers (and future re-consolidations) can trace the chain.
    """
    header: list[str] = [
        "---",
        f"archive_kind: memory_consolidation",
        f"consolidation_date: {consolidation_date}",
        f"source_memory_sha3_512: {source_memory_sha3_512}",
    ]
    if parent_archive_filename is not None:
        header.append(f"parent_archive: {parent_archive_filename}")
    header.append("---")
    header.append("")
    header.append("# Archived MEMORY.md index entries")
    header.append("")
    header.append(
        f"Promoted out of MEMORY.md on {consolidation_date} by "
        "`tilth memory consolidate-index`. Original order preserved."
    )
    header.append("")

    body = "\n".join(archived_entries)
    return "\n".join(header) + body + "\n"


# ---------------------------------------------------------------------------
# Pure consolidation (no I/O)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MemoryConsolidationResult:
    """Result of one consolidation pass.

    Attributes
    ----------
    fired
        True iff input size exceeded the threshold and an archive was
        produced. When ``fired`` is False, ``new_memory_text`` is the
        input unchanged.
    threshold_bytes
        The threshold gate used.
    original_size_bytes
        Byte length of the input ``memory_text`` (UTF-8).
    new_size_bytes
        Byte length of the rewritten MEMORY.md (UTF-8).
    archive_filename
        Basename of the archive (e.g., ``_archive_2026-05-15.md``); empty
        string when ``fired`` is False.
    archive_text
        Full archive content; empty string when ``fired`` is False.
    new_memory_text
        Rewritten MEMORY.md content.
    entries_kept
        Count of entries left on MEMORY.md.
    entries_archived
        Count of entries promoted to the archive.
    source_memory_sha3_512
        Hex digest of the pre-consolidation MEMORY.md bytes — feeds the
        lock_history hash-pin row.
    new_memory_sha3_512
        Hex digest of the post-consolidation MEMORY.md bytes.
    archive_sha3_512
        Hex digest of the archive bytes (empty when not fired).
    """

    fired: bool
    threshold_bytes: int
    original_size_bytes: int
    new_size_bytes: int
    archive_filename: str
    archive_text: str
    new_memory_text: str
    entries_kept: int
    entries_archived: int
    source_memory_sha3_512: str
    new_memory_sha3_512: str
    archive_sha3_512: str


def _sha3_512_hex(data: bytes) -> str:
    return hashlib.sha3_512(data).hexdigest()


def consolidate_index(
    memory_text: str,
    *,
    threshold_bytes: int = DEFAULT_THRESHOLD_BYTES,
    consolidation_date: str,
    archive_filename: Optional[str] = None,
) -> MemoryConsolidationResult:
    """Pure consolidation — no I/O.

    Parameters
    ----------
    memory_text
        Source ``MEMORY.md`` content.
    threshold_bytes
        Soft threshold; consolidation only fires when the input exceeds
        this byte count (UTF-8).
    consolidation_date
        ``YYYY-MM-DD`` stamp used in the archive filename and metadata.
    archive_filename
        Override the default ``_archive_<date>.md`` basename. If a file
        with the default name already exists in the live memory directory,
        callers can pass a uniquified name (``_archive_<date>_001.md``).
    """
    if threshold_bytes <= 0:
        raise MemoryConsolidationError(
            f"threshold_bytes must be positive (got {threshold_bytes!r})"
        )
    if threshold_bytes > HARD_LOAD_LIMIT_BYTES:
        raise MemoryConsolidationError(
            f"threshold_bytes ({threshold_bytes}) must be <= "
            f"HARD_LOAD_LIMIT_BYTES ({HARD_LOAD_LIMIT_BYTES}) — the "
            "Cowork auto-memory loader truncates above this"
        )
    if not (len(consolidation_date) == 10 and consolidation_date[4] == "-"
            and consolidation_date[7] == "-"):
        raise MemoryConsolidationError(
            f"consolidation_date must be YYYY-MM-DD (got "
            f"{consolidation_date!r})"
        )

    source_bytes = memory_text.encode("utf-8")
    original_size = len(source_bytes)
    source_hash = _sha3_512_hex(source_bytes)

    if original_size <= threshold_bytes:
        # No-op path — threshold gate not crossed.
        return MemoryConsolidationResult(
            fired=False,
            threshold_bytes=threshold_bytes,
            original_size_bytes=original_size,
            new_size_bytes=original_size,
            archive_filename="",
            archive_text="",
            new_memory_text=memory_text,
            entries_kept=0,
            entries_archived=0,
            source_memory_sha3_512=source_hash,
            new_memory_sha3_512=source_hash,
            archive_sha3_512="",
        )

    parsed = parse_memory_index(memory_text)
    if len(parsed.entries) < 2:
        raise MemoryConsolidationError(
            f"MEMORY.md exceeds threshold ({original_size} > "
            f"{threshold_bytes}) but has fewer than 2 entries to split — "
            "operator intervention required"
        )

    if archive_filename is None:
        archive_filename = f"_archive_{consolidation_date}.md"

    # Estimate structural overhead (pointer line + preamble + trailer +
    # blank separators) so the greedy step in the splitter knows how
    # many entries it can keep before re-crossing the threshold.
    pointer_overhead = (
        len(build_pointer_line(archive_filename).encode("utf-8")) + 2
    )  # pointer line + blank separator
    preamble_overhead = (
        sum(len(ln.encode("utf-8")) + 1 for ln in parsed.preamble_lines)
        + (1 if parsed.preamble_lines else 0)
    )
    trailer_overhead = (
        sum(len(ln.encode("utf-8")) + 1 for ln in parsed.trailing_lines)
        + (1 if parsed.trailing_lines else 0)
    )
    structural_overhead = pointer_overhead + preamble_overhead + trailer_overhead

    kept, archived = _split_bottom_half_oldest(
        parsed.entries,
        threshold_bytes=threshold_bytes,
        overhead_bytes=structural_overhead,
    )
    if "/" in archive_filename or "\\" in archive_filename:
        raise MemoryConsolidationError(
            f"archive_filename must be a basename (got {archive_filename!r})"
        )

    archive_text = render_archive_markdown(
        archived_entries=archived,
        consolidation_date=consolidation_date,
        source_memory_sha3_512=source_hash,
    )

    pointer_line = build_pointer_line(archive_filename)
    new_memory_text = render_memory_markdown(
        kept_entries=kept,
        pointer_line=pointer_line,
        preamble_lines=parsed.preamble_lines,
        trailing_lines=parsed.trailing_lines,
    )

    new_memory_bytes = new_memory_text.encode("utf-8")
    archive_bytes = archive_text.encode("utf-8")

    return MemoryConsolidationResult(
        fired=True,
        threshold_bytes=threshold_bytes,
        original_size_bytes=original_size,
        new_size_bytes=len(new_memory_bytes),
        archive_filename=archive_filename,
        archive_text=archive_text,
        new_memory_text=new_memory_text,
        entries_kept=len(kept),
        entries_archived=len(archived),
        source_memory_sha3_512=source_hash,
        new_memory_sha3_512=_sha3_512_hex(new_memory_bytes),
        archive_sha3_512=_sha3_512_hex(archive_bytes),
    )


# ---------------------------------------------------------------------------
# Orchestrator (touches the filesystem)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RunConsolidationOutcome:
    """Filesystem-aware outcome of one ``run_consolidation`` call."""

    result: MemoryConsolidationResult
    memory_path: Path
    archive_path: Optional[Path]
    lock_history_row_appended: bool
    lock_history_path: Optional[Path]


def run_consolidation(
    memory_dir: Path,
    *,
    threshold_bytes: int = DEFAULT_THRESHOLD_BYTES,
    consolidation_date: Optional[str] = None,
    lock_history_path: Optional[Path] = None,
    dry_run: bool = False,
    repo_root: Optional[Path] = None,
) -> RunConsolidationOutcome:
    """Read ``memory_dir/MEMORY.md``, consolidate, write outputs.

    Parameters
    ----------
    memory_dir
        Directory containing ``MEMORY.md``. The archive file is written
        as a sibling inside the same directory.
    threshold_bytes
        Soft threshold (see ``consolidate_index``).
    consolidation_date
        Defaults to today's UTC date in ``YYYY-MM-DD`` form.
    lock_history_path
        Path to ``pipeline/engineering/lock_history.v1.jsonl``. When
        omitted, the orchestrator derives it from ``repo_root`` or skips
        the hash-pin row.
    dry_run
        When True, no files are written; the outcome reports what would
        happen.
    repo_root
        Workspace root used to derive ``lock_history_path`` when not
        supplied explicitly.
    """
    if not memory_dir.is_dir():
        raise MemoryConsolidationError(
            f"memory_dir does not exist or is not a directory: "
            f"{memory_dir!s}"
        )

    memory_path = memory_dir / "MEMORY.md"
    if not memory_path.is_file():
        raise MemoryConsolidationError(
            f"MEMORY.md not found at {memory_path!s}"
        )

    text = memory_path.read_text(encoding="utf-8")

    if consolidation_date is None:
        consolidation_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Uniquify archive filename if the default already exists.
    archive_filename = f"_archive_{consolidation_date}.md"
    counter = 1
    while (memory_dir / archive_filename).exists():
        counter += 1
        archive_filename = f"_archive_{consolidation_date}_{counter:03d}.md"

    result = consolidate_index(
        text,
        threshold_bytes=threshold_bytes,
        consolidation_date=consolidation_date,
        archive_filename=archive_filename,
    )

    archive_path: Optional[Path] = None
    lock_row_appended = False
    resolved_lock_history_path: Optional[Path] = lock_history_path

    if result.fired and not dry_run:
        archive_path = memory_dir / result.archive_filename
        archive_path.write_text(result.archive_text, encoding="utf-8")
        memory_path.write_text(result.new_memory_text, encoding="utf-8")

        if resolved_lock_history_path is None and repo_root is not None:
            candidate = repo_root / "pipeline" / "engineering" / "lock_history.v1.jsonl"
            if candidate.is_file():
                resolved_lock_history_path = candidate
        if resolved_lock_history_path is not None and resolved_lock_history_path.is_file():
            row = _build_lock_history_row(
                result=result,
                consolidation_date=consolidation_date,
                memory_path=memory_path,
                archive_path=archive_path,
            )
            with open(resolved_lock_history_path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            lock_row_appended = True

    elif result.fired and dry_run:
        archive_path = memory_dir / result.archive_filename

    return RunConsolidationOutcome(
        result=result,
        memory_path=memory_path,
        archive_path=archive_path,
        lock_history_row_appended=lock_row_appended,
        lock_history_path=resolved_lock_history_path,
    )


def _build_lock_history_row(
    *,
    result: MemoryConsolidationResult,
    consolidation_date: str,
    memory_path: Path,
    archive_path: Path,
) -> dict:
    """Construct the lock_history JSON row for one consolidation.

    Schema parallels existing ``lock_class`` rows but uses a dedicated
    ``lock_class=memory_consolidation`` discriminator so consumers can
    filter cleanly.
    """
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "lock_timestamp_utc": now_utc,
        "lock_class": "memory_consolidation",
        "lock_kind": "auto-trigger-over-threshold",
        "lock_mode": "operator-invoked-cli",
        "module": "pipeline.memory.consolidate_index",
        "memory_path": str(memory_path),
        "archive_path": str(archive_path),
        "consolidation_date": consolidation_date,
        "threshold_bytes": result.threshold_bytes,
        "original_size_bytes": result.original_size_bytes,
        "new_size_bytes": result.new_size_bytes,
        "entries_kept": result.entries_kept,
        "entries_archived": result.entries_archived,
        "source_memory_sha3_512": result.source_memory_sha3_512,
        "new_memory_sha3_512": result.new_memory_sha3_512,
        "archive_sha3_512": result.archive_sha3_512,
        "review_verdict": "AUTO — pure-Python consolidation; no LOCK ceremony",
    }
