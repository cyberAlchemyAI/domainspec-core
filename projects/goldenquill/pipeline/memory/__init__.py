"""Memory consolidation utilities (``tilth memory`` CLI namespace).

The auto-memory ``MEMORY.md`` file is loaded into context at every session
start and is hard-capped at 24.4 KB by the Cowork runtime. When it overflows
the loader silently truncates, which degrades retrieval. This package owns
the consolidation logic that keeps the file under threshold by archiving
the bottom-half oldest entries into a date-stamped sibling archive index
and prepending a single pointer line to the live MEMORY.md.

Public surface
--------------
``consolidate_index`` — pure consolidation function (in-memory, no I/O).
``run_consolidation`` — orchestrator (reads MEMORY.md, writes archive +
  rewritten MEMORY.md, appends lock_history row).
``MemoryConsolidationResult`` — typed result.
``MemoryConsolidationError`` — raised on malformed inputs.

Threshold defaults
------------------
``DEFAULT_THRESHOLD_BYTES = 20480`` (20 KB) — chosen as a safety margin
under the 24.4 KB hard load limit observed live on 2026-05-15.
"""

from __future__ import annotations

from pipeline.memory.consolidate_index import (
    DEFAULT_THRESHOLD_BYTES,
    HARD_LOAD_LIMIT_BYTES,
    MemoryConsolidationError,
    MemoryConsolidationResult,
    ParsedMemoryIndex,
    build_pointer_line,
    consolidate_index,
    parse_memory_index,
    render_archive_markdown,
    render_memory_markdown,
    run_consolidation,
)

__all__ = [
    "DEFAULT_THRESHOLD_BYTES",
    "HARD_LOAD_LIMIT_BYTES",
    "MemoryConsolidationError",
    "MemoryConsolidationResult",
    "ParsedMemoryIndex",
    "build_pointer_line",
    "consolidate_index",
    "parse_memory_index",
    "render_archive_markdown",
    "render_memory_markdown",
    "run_consolidation",
]
